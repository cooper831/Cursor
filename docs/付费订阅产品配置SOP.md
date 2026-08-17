# 付费订阅产品配置 SOP（App Store Connect / Google Play / RevenueCat）

| 字段 | 内容 |
| ---- | ---- |
| 文档版本 | v1.0 |
| 创建日期 | 2026-08-14 |
| 文档状态 | Draft（待技术负责人 Review） |
| 适用范围 | 自动续期订阅产品的**首次配置**与**新增档位配置**；覆盖 App Store Connect、Google Play Console、RevenueCat Dashboard、Paywall、我的订阅页 |
| 目标读者 | 第一次做订阅配置的产品 / iOS / Android / 后端 / 运营同学 |
| 使用方式 | 按 §1 → §9 顺序执行，每节结尾有 Gate 检查；`〔待填〕` 是需要你补齐的项目取值 |
| 关联文档 | [PRD-2 存储订阅 V2](./PRD-2-RevenueCat-Storage-Subscription-V2.md) · [PRD-1 课程内购](./PRD-1-RevenueCat-Course-IAP.md) · [开发前配置清单](./RevenueCat-Pre-Dev-Setup-Checklist.md) |

---

## 0. 先读这一节

### 0.1 这份 SOP 解决什么问题

订阅配置的难点不是某一步很难，而是**三个平台互相有依赖**，顺序错了就要返工，且有两类"硬阻塞"（财务协议、构建包）会让你卡住一整天。本文按依赖顺序拆成 9 步，每步给出：**在哪里操作 → 填什么字段 → 字段规则 → 常见坑 → 产出什么**。

### 0.2 执行顺序与依赖关系

| 阶段 | 内容 | 依赖 | 能否并行 | 预计耗时 |
| --- | --- | --- | --- | --- |
| §1 | 前置准备（账号 / 权限 / 财务 / 物料 / 法务 / 定价） | 无 | — | 3–5 天（法务与财务是长尾） |
| §2 | 命名规范与产品矩阵定稿 | §1 定价确认 | — | 0.5 天 |
| §3 | App Store Connect 配置 | §1 + §2 | ✅ 与 §4 并行 | 0.5 天 + 审核 24–48h |
| §4 | Google Play Console 配置 | §1 + §2 + 已上传签名包 | ✅ 与 §3 并行 | 0.5 天 + 凭证生效 ≤36h |
| §5 | RevenueCat 配置 | **必须** §3 §4 的产出（Product ID、密钥） | ❌ | 0.5 天 |
| §6 | Paywall 配置与接入 | §5 的 Offering | 部分并行（设计可提前） | 1–2 天 |
| §7 | 我的订阅配置与接入 | §5 + §6 | 部分并行 | 1 天 |
| §8 | 沙盒联调与验收 | §3–§7 全部完成 | ❌ | 1–2 天 |
| §9 | 灰度上线 | §8 通过 | ❌ | 按发版节奏 |

**三条关键路径，必须提前启动：**

1. **Apple Paid Applications Agreement + 税务银行信息** —— 未完成时 App Store Connect 里**看不到 Subscriptions 入口**，且无法测试内购。需要 Account Holder 本人操作，跨财务与法务，通常最慢。
2. **Google Service Account 凭证生效** —— 上传到 RevenueCat 后官方口径**最长 36 小时**才激活，§5 的 Android 商品导入会一直失败。请在 §4 一开始就做，不要留到最后。
3. **Apple / Google 商品审核 24–48h** —— 订阅商品要随 App 版本一起过审，建议整体配置比预定提测日**提前 1 周**启动。

### 0.3 术语对照（先看懂这 5 个词，后面才不会绕）

| 术语 | 属于 | 一句话解释 | 本项目示例 |
| --- | --- | --- | --- |
| Product / SKU | Apple / Google | 用户真正掏钱买的那个东西，一个周期一个 | `storage_pro_monthly_iap` |
| Entitlement（权益） | RevenueCat | 「买了之后解锁什么」，代码里判断的就是它 | `storage_pro` |
| Package（套餐） | RevenueCat | 把各平台同周期的 Product 打成一包，客户端不用关心 iOS/Android 差异 | `$rc_monthly` |
| Offering（陈列） | RevenueCat | 一屏 Paywall 上要展示的 Package 集合，可远程换 | `default` |
| Paywall | RevenueCat | 付费墙 UI，可在 Dashboard 可视化搭建并远程下发，改文案改样式不用发版 | 绑定在 `default` 上 |

**心法**：客户端代码里只硬编码 **Entitlement ID** 一个常量，其余（价格、文案、套餐、UI）全部通过 Offering / Paywall 远程下发。任何让你在 App 里硬编码价格或 Product ID 的方案都是错的。

---

## 1. Phase 0 · 配置依赖项与前置准备

> **这一节不做完，后面每一步都会卡住。** 建议把本节做成一张共享表格，逐项打勾后再进 §3。

### 1.1 账号与权限矩阵

| 平台 | 需要的角色 | 谁来批 | 能做什么 / 不给会怎样 |
| --- | --- | --- | --- |
| Apple Developer Program | 会员资格有效（未过期） | 公司 IT / 运营 | 过期则所有商品与构建操作全部冻结 |
| App Store Connect | **Account Holder** | 公司主体持有人 | 只有他能签 Paid Applications Agreement、填银行税务 |
| App Store Connect | **Admin** | Account Holder | 创建 In-App Purchase Key（Users and Access → Integrations）、管理 Sandbox 账号 |
| App Store Connect | **App Manager**（至少） | Admin | 创建 / 编辑订阅商品、提交审核 |
| App Store Connect | Finance | Admin | 查看结算报表（运营 / 财务需要） |
| Google Play Console | **Admin（账号级）** | 账号所有者 | 邀请 Service Account、配置 Users & Permissions |
| Google Play Console | 应用级：查看应用信息 / 查看财务数据 / 管理订单与订阅 | Play Admin | Service Account 必须拿到这三项，缺一项 RevenueCat 凭证校验就红 |
| Google Play Console | Payments profile 管理 | 账号所有者 | 未激活商家账户无法销售付费商品 |
| Google Cloud Console | 项目 Owner，或 `Service Account Admin` + `Service Account Key Admin` | 云平台管理员 | 创建 Service Account 与 JSON 密钥 |
| Google Cloud Console | Organization Policy Administrator（**可能需要**） | 云平台管理员 | 2024-05-03 之后创建的组织默认禁止建 Service Account 密钥、默认开启域名共享限制，需临时放开 |
| RevenueCat | **Admin / Owner** | 技术负责人 | 只有 Admin 能配置 App 凭证与 Service Credentials |
| RevenueCat | Member(Edit) | RC Admin | 产品 / 客户端负责人配 Offering、Paywall |
| RevenueCat | Member(Read Only) | RC Admin | QA、客服、运营查交易与客户 |

> **提前踩坑提醒**：Google Cloud 组织策略 `iam.disableServiceAccountKeyCreation` 与 `constraints/iam.allowedPolicyMemberDomains`（域名限制共享）会分别让你**建不出 JSON 密钥**和**连不上 Pub/Sub**。如果你们组织是 2024 年 5 月之后建的，请在 §1 阶段就找云平台管理员确认，别等到 §4 报错才发现。

### 1.2 财务与商务前置（硬阻塞，最先启动）

| 项 | 平台 | 位置 | 负责人 | 不做的后果 |
| --- | --- | --- | --- | --- |
| Paid Applications Agreement 已签署最新版 | Apple | App Store Connect → Business（旧版为 Agreements, Tax, and Banking） | Account Holder + 法务 | **侧边栏看不到 Subscriptions**，且无法测试任何内购 |
| 银行账户已绑定且状态为 Clear | Apple | 同上 → Banking | 财务 | 同上 |
| 税务表单已提交（W-8BEN / W-9 等） | Apple | 同上 → Tax | 财务 | 商品无法上架 |
| Tax Category 已确认 | Apple | App / 商品级 Tax Category | 财务 | 税率错误，事后调整影响结算 |
| Payments profile（商家账户）已激活 | Google | Play Console → 设置 → 付款配置 | 财务 | 无法创建付费商品 |
| 银行账户与税务信息已填写 | Google | 同上 | 财务 | 无法收款 |

### 1.3 产品与定价信息（产品 + 财务提供）

| 项 | 说明 | 本项目取值 |
| --- | --- | --- |
| 订阅产品对外名称 | 用户在 App Store / Play / 系统订阅管理里看到的名字，各平台需一致 | 〔待填，如 Storage Pro〕 |
| 权益边界 | 订阅解锁哪些功能、免费版保留哪些，必须先定死，Paywall 文案与门控都依赖它 | 参见 PRD-2 §6.2.4 |
| 计费周期 | 建议起步只上月 + 年两档，档位越多测试与后续实验成本越高 | 月 + 年 |
| 各周期价格（基准货币） | Apple / Google 都按基准价自动换算其他区域 | 月 `〔待填〕` / 年 `〔待填〕` |
| 目标销售市场 | 决定定价表与本地化语言数量 | US / CA / UK / FR / DE / IT / ES / AE / SA（9 市场） |
| 免费试用时长 | 常见 7 / 14 / 30 天。**注意**：试用长度直接影响试用转化率与退款率，定了以后改会影响历史用户 | 〔待填，PRD-2 建议 7 天〕 |
| 年付折扣话术 | 「省 X%」需要财务复核，且 Paywall 上写死百分比在多币种下可能不成立，建议用 RC 变量动态计算 | 〔待填〕 |
| 挽留优惠（可选） | 我的订阅页做挽留时要用的促销优惠，见 §7.3 | 〔待填〕 |

### 1.4 内容与物料清单（设计 + 内容提供）

| 物料 | 规格要求 | 用在哪 | 缺失后果 |
| --- | --- | --- | --- |
| **IAP 审核截图** | 至少 640×920 PNG，需真实展示 Paywall | App Store Connect 商品的 Review Information | **没有它无法提交商品审核**（最高频漏项）；测试阶段可先放占位图，提审前必须换成真实 Paywall 截图 |
| Paywall 主视觉 | 图片或视频，建议 2x/3x，单张 ≤1MB；视频注意首帧与体积 | RevenueCat Paywall 媒体库 | Paywall 观感差，转化受损 |
| 权益图标 | RC 自带图标库可用；自定义图标需 SVG/PNG | Paywall Feature list 组件 | 可用内置图标兜底 |
| 品牌色与字体 | 主色、CTA 色、深浅两套；自定义字体需上传字体文件 | Paywall Branding 面板 | 会退化为默认样式；且自定义字体**跨项目复制 Paywall 时不会带过去** |
| 订阅显示名与描述 | Apple：Display Name + Description，按语言各一份；Google：Name ≤55 字符，Benefits 最多 4 条、每条 ≤40 字符 | 商店商品页 + 系统订阅管理页 | 商品无法提审 / 用户看到英文兜底 |
| 多语言文案表 | 覆盖 §1.3 的市场；含 Paywall 全部文案、状态文案、错误文案 | Paywall Localization + App | 非英语市场体验割裂 |
| 客服支持邮箱 | 一个真实可响应的邮箱 | 我的订阅（Customer Center）支持入口 | 用户找不到人，转差评 |

### 1.5 法务与合规文案（法务提供）

| 项 | 要求 | 状态 |
| --- | --- | --- |
| Terms of Service 公网 URL | 含数字商品与订阅条款 | 〔待填〕 |
| Privacy Policy 公网 URL | **必须写明 RevenueCat 作为第三方数据处理方**，否则 App Store 审核可能被拒 | 〔待填〕 |
| 自动续费披露文案 | Apple / Google 均要求 Paywall 上明示：订阅名称、时长、价格、自动续费至取消、如何取消 | 见 §6.1 |
| 试用转正付披露 | 明示试用时长、试用结束后的扣费价格与时间 | 见 §6.1 |
| App 隐私问卷 / Data Safety | Apple App Privacy 与 Google Data Safety 需勾选购买记录相关数据项 | 〔待填〕 |

### 1.6 技术前置（客户端 + 后端）

| 项 | 要求 | 备注 |
| --- | --- | --- |
| iOS Bundle ID | 已在 App Store Connect 创建对应 App | 大小写必须与 RC 中填写的完全一致 |
| Android Package Name | 已创建应用 | 同上 |
| **已上传签名的 APK / AAB 到至少一条测试轨道** | Google Play 的硬性前置：**没有构建包就创建不了内购商品** | 请在 §1 就安排，不要等到 §4 |
| SDK 版本 | `react-native-purchases` 最新稳定版；Paywall 与我的订阅需额外装 `react-native-purchases-ui`（我的订阅要求 **≥ 8.7.0**） | 原生项目对应 iOS SDK ≥ 5.x / Android SDK ≥ 7.x |
| Webhook 端点 | HTTPS + TLS 1.2+，返回 200，支持幂等 | 如 `https://api.brand.com/v1/revenuecat/webhook` |
| Webhook Authorization Token | ≥32 位强随机串，存 KMS/Vault | 不要写进代码仓库 |
| 密钥管理 | Secret API Key、.p8、Service Account JSON 全部进 KMS | 见 §5.8 分级表 |

### 1.7 Gate ①：准备完成检查

以下全部为「是」才进入 §2，否则你会在后面返工：

- [ ] Apple Paid Applications Agreement 已签、银行状态 Clear、税务已提交
- [ ] Google Payments profile 已激活
- [ ] Apple / Google / Google Cloud / RevenueCat 四套账号权限已到位（对照 §1.1）
- [ ] Google Cloud 组织策略确认不阻止创建 Service Account 密钥
- [ ] 已上传签名包到 Google Play 测试轨道
- [ ] 定价、周期、试用时长、销售市场已由产品 + 财务书面确认
- [ ] ToS / Privacy Policy 已上线公网且 Privacy 含 RevenueCat 条款
- [ ] IAP 审核截图（≥640×920）已到位
- [ ] Webhook 端点已上线并可返回 200

---

## 2. 命名规范与产品矩阵定稿

> 命名是**一次性决策**：Apple 与 Google 的 Product ID **一旦使用就永久占用，删掉也不能复用**。定稿后请在本节表格里落值，后续所有平台都照抄。

### 2.1 命名规范

```
{业务域}_{档位}_{周期}_{平台后缀}
```

| 部分 | 规则 | 示例 |
| --- | --- | --- |
| 业务域 | 小写英文，标识业务线 | `storage` |
| 档位 | 权益等级 | `pro` |
| 周期 | `monthly` / `yearly` | `monthly` |
| 平台后缀 | `_iap`（App Store）/ `_gpb`（Google Play）/ `_stripe`（Web，Phase 2） | `_iap` |

**其他命名约束**

- Entitlement ID：与档位同名、不带平台后缀、不带周期 —— `storage_pro`
- Offering ID：`default` 为主陈列；实验用 `exp_<假设>`；挽留用 `winback_<场景>`。**Offering Identifier 创建后不可修改**
- Package Identifier：优先用 RC 预置值 `$rc_monthly` / `$rc_annual`，Paywall 模板与图表统计都依赖它识别周期
- Google Base Plan ID：`{周期}-autorenewing`，如 `monthly-autorenewing`

### 2.2 产品矩阵（本次要配的全部对象）

| Entitlement | Package | 平台 | 商店侧对象 | RevenueCat 中的 Product 标识 | 周期 | 价格 |
| --- | --- | --- | --- | --- | --- | --- |
| `storage_pro` | `$rc_monthly` | App Store | Product ID `storage_pro_monthly_iap` | `storage_pro_monthly_iap` | 月 | 〔待填〕 |
| `storage_pro` | `$rc_annual` | App Store | Product ID `storage_pro_yearly_iap` | `storage_pro_yearly_iap` | 年 | 〔待填〕 |
| `storage_pro` | `$rc_monthly` | Google Play | Subscription `storage_pro_gpb` + Base Plan `monthly-autorenewing` | `storage_pro_gpb:monthly-autorenewing` | 月 | 〔待填〕 |
| `storage_pro` | `$rc_annual` | Google Play | Subscription `storage_pro_gpb` + Base Plan `yearly-autorenewing` | `storage_pro_gpb:yearly-autorenewing` | 年 | 〔待填〕 |

### 2.3 两个必须知道的口径差异

**① Apple 与 Google 的商品模型不一样，不要指望 Product ID 完全对称。**

- Apple：一个 **Subscription Group** 里放多个 **Subscription**，每个 Subscription 自己就是一个可购买商品，所以月/年是两个独立 Product ID。同组内可自由升降级。
- Google：一个 **Subscription** 下挂多个 **Base Plan**，用户买的其实是 Base Plan。所以推荐**一个 Subscription（`storage_pro_gpb`）+ 两个 Base Plan**，而不是建两个 Subscription。
- 因此 RevenueCat 里 Google 侧的 Product 标识形如 `<subscription_id>:<base_plan_id>`，天然带冒号，和 iOS 的扁平 ID 不一样。**这是正常现象，不要试图把它改成一致。**

> **与 PRD-2 的口径差异**：PRD-2 §4.1.1 把 Android 侧写成 `storage_pro_monthly_gpb` / `storage_pro_yearly_gpb` 两个独立商品。本 SOP 推荐改为「单 Subscription + 双 Base Plan」，理由是符合 Google 现行订阅模型、升降级与 proration 由 Google 原生处理、后续加档位不必新建商品。**请在配置前与 PRD 责任人确认采用哪一种并同步更新 PRD**；若沿用 PRD-2 写法，则 §4 中每个 Subscription 各建一个 Base Plan，其余步骤不变。

**② Apple 的凭证方式已经变了。**
早期文档里的 **App-Specific Shared Secret** 已不是主路径。使用 StoreKit 2（iOS SDK 5.x+ / React Native SDK 8.x+）时，RevenueCat **要求配置 In-App Purchase Key**，否则**交易会记录失败，用户付了钱拿不到权益**。请按 §3.9 配置 In-App Purchase Key + Issuer ID。

### 2.4 Gate ②

- [ ] §2.2 表格中所有 `〔待填〕` 已落值，且经产品 + 技术双方确认
- [ ] Google 商品结构（单 Subscription 双 Base Plan / 双 Subscription）已决策并同步 PRD
- [ ] 命名已复核：无大小写混用、无中文、无空格、未与历史商品重名

---

## 3. App Store Connect 配置

**入口**：[App Store Connect](https://appstoreconnect.apple.com/) → Apps → 选择你的 App → 左侧 **Monetization → Subscriptions**（部分账号显示在 Features 分组下）。

> 看不到 Subscriptions 入口？100% 是 §1.2 的协议/税务/银行没齐。回去补，不要在这里找原因。

### 3.1 创建 Subscription Group（订阅组）

点 Subscriptions 页的 `+`。

| 字段 | 必填 | 规则 | 本项目取值 |
| --- | --- | --- | --- |
| Reference Name | ✅ | **内部名**，用户看不到，出现在 Apple 销售报表中 | `Storage Pro Group` |

**为什么要有组**：同一个组内的订阅，用户可以自由升级/降级/交叉切换，且 Apple 保证同组内**只有一个订阅生效**。月付与年付必须放在同一组，否则用户可能同时买上两个。

### 3.2 创建自动续期订阅

在组内点 `+` → Create Auto-Renewable Subscription。

| 字段 | 必填 | 规则 | 本项目取值 |
| --- | --- | --- | --- |
| Reference Name | ✅ | 内部名，≤64 字符，出现在 Sales and Trends 报表 | `Storage Pro Monthly` |
| Product ID | ✅ | 唯一，字母数字与下划线；**一经使用永久占用，删除也不可复用** | `storage_pro_monthly_iap` |

月付与年付各建一次。

### 3.3 设置订阅时长

商品创建后，在 **Subscription Duration** 下拉中选择周期（1 周 / 1 / 2 / 3 / 6 个月 / 1 年），点 Save。

> 时长在有用户订阅后不可更改。选错只能新建商品。

### 3.4 设置价格

**Subscription Prices** 区域点 `+` → 选择基准货币下的价格 → Next → Apple 自动生成全部区域价格。

| 要点 | 说明 |
| --- | --- |
| 自动换算 | Apple 按汇率与税率生成各区域价格，**建议直接采用默认值**，除非财务有明确的心理价位要求（如印度、巴西需本地化定价） |
| 逐区域改价 | 可在生成后手动覆盖个别区域 |
| 生效范围 | 只影响新订阅；对存量用户涨价需走 Apple 的价格变更流程并征得用户同意 |
| 别忘了 | 改完必须点 **Save**，Apple 这一页不会自动保存 |

### 3.5 配置免费试用（Introductory Offer）

在同一页的 **Introductory Offers** 标签点 `+`，依次经过三屏：

| 屏 | 字段 | 建议填法 |
| --- | --- | --- |
| 1 | Countries or Regions | 除非要做区域差异化，选择全部区域 |
| 2 | Start Date / End Date | Start = 今天，End = **No End Date**（长期开放试用） |
| 3 | Type | **Free**（免费试用）；另有 Pay as you go（低价续订若干期）、Pay up front（一次性折扣价） |
| 3 | Duration | 3 天 / 1 周 / 2 周 / 1 / 2 / 3 / 6 个月 / 1 年 中选择，对齐 §1.3 |

**关键规则**：Introductory Offer 的资格由 Apple 判定，**同一订阅组内一个用户一生只能用一次**。所以 Paywall 上「7 天免费试用」的字样必须按资格动态显示 —— 用 RevenueCat Paywall 的试用变量，不要写死（见 §6.3）。

### 3.6 商品本地化

**App Store Information → Localization** 点 `+`，为每个语言各填一份：

| 字段 | 必填 | 规则 | 建议 |
| --- | --- | --- | --- |
| Subscription Display Name | ✅ | 用户在 App Store 与**系统订阅管理页**看到的名称 | 短，描述解锁的权益等级；**同一权益等级的所有商品（月/年）用同一个名字** |
| Description | ✅ | 权益描述 | 一句话说清解锁什么，不要塞营销词 |

> 月付和年付用同一个 Display Name，用户订阅列表才干净；不同名字会让用户以为买了两个东西。

### 3.7 订阅组本地化（最容易漏）

Apple 会提示 *"Before you can submit your in-app purchase for review, you must add at least one localization to your subscription group."*

进入 Subscription Group 配置页，添加本地化：

| 字段 | 必填 | 规则 |
| --- | --- | --- |
| Subscription Group Display Name | ✅ | 用户可见的组名，描述该组解锁的权益等级 |
| App Name | ✅ | 用户订阅里显示的 App 名。可选 App Store 上架名，或填 Custom Name（当上架名带副标题时更干净，如上架名 `Momcozy - Baby Care` 可自定义为 `Momcozy`） |

### 3.8 审核信息

同一商品页的 **Review Information**：

| 字段 | 必填 | 规则 |
| --- | --- | --- |
| Screenshot | ✅ | **不填无法提审**。≥640×920。开发期可放占位图；**提审前必须替换为真实 Paywall 截图**，且截图里要能看到自动续费披露与价格 |
| Review Notes | ⭕ | 写清测试路径：如何进入 Paywall、需要什么测试账号、有无地区限制 |

### 3.9 生成 In-App Purchase Key（RevenueCat 必需）

**位置**：App Store Connect → **Users and Access → Integrations → In-App Purchase**（需要 Admin 角色）

1. 点 **Generate In-App Purchase Key**（已有则点 Active 旁的 `+`），填一个 Key 名称
2. 生成后点 **Download API Key** 下载 `.p8` 文件 —— **只有一次下载机会**，立刻存入 KMS
3. 记录同一页顶部的 **Issuer ID**

| 产出 | 说明 |
| --- | --- |
| `.p8` 私钥文件 | 上传到 RevenueCat（§5.2） |
| Issuer ID | 填入 RevenueCat |

> **Issuer ID 不显示？** 去创建一个任意名称、任意权限的 App Store Connect API Key，创建完 Issuer ID 就会出现在页面顶部（两种 Key 共用同一个 Issuer ID）。
>
> 同一个 App Store Connect 账号下的所有 App 可以共用一把 In-App Purchase Key。

### 3.10 配置 App Store Server Notifications（推荐）

订阅状态本身不依赖它，但配了可以：加快 Webhook 与图表的时效、启用 Refund Control、让退款自动同步。

- **推荐做法**：在 RevenueCat Dashboard → Apps → 你的 iOS App → *Apple Server to Server notification settings* 点 **Apply in App Store Connect**，RC 会自动把 URL 写入 Production 与 Sandbox 两个环境（此步在 §5.2 之后做）
- 手动做法：复制 RC 提供的 **Apple Server Notification URL**，粘贴到 ASC → App Information → App Store Server Notifications 的 Production 与 Sandbox 两个字段
- **版本选 Version 2**（V1 已被 Apple 弃用；V2 才支持自动识别价格变更、退款检测更可靠）

> Apple 每个环境只允许一个通知 URL。如果你的后端也想收，**不要**让后端占用这个 URL，而是填 RC 的地址，再在 RC 里配置 *Apple Server Notification Forwarding URL* 转发给你的后端。

### 3.11 Sandbox 测试账号

**位置**：Users and Access → Sandbox → Test Accounts，创建 ≥2 个。

| 要点 | 说明 |
| --- | --- |
| 邮箱 | 用未注册过 Apple ID 的邮箱；企业邮箱可用 `+` 别名批量造号 |
| 地区 | 至少准备 1 个美国 + 1 个目标市场账号，用于验证多币种 |
| 使用方式 | iOS 15+ 在 设置 → App Store → Sandbox Account 登录；**不要**用沙盒账号登录真实 App Store |
| 试用资格重置 | 沙盒账号的试用资格可在 ASC 的 Sandbox 账号管理里清除，便于反复测试首购 |

### 3.12 Gate ③：App Store Connect 完成检查

- [ ] Subscription Group 已建且**已添加本地化**（Group Display Name + App Name）
- [ ] 月 / 年两个订阅商品已建，Product ID 与 §2.2 完全一致
- [ ] 时长、价格（全区域）已保存
- [ ] Introductory Offer（免费试用）已配置，时长正确
- [ ] 每个商品的 Display Name / Description 已按语言填齐
- [ ] Review Screenshot 已上传（提审前替换为真实 Paywall 图）
- [ ] 商品状态为 Ready to Submit / 已随版本提交
- [ ] In-App Purchase Key `.p8` 已下载入库，Issuer ID 已记录
- [ ] ≥2 个 Sandbox 测试账号已创建

---

## 4. Google Play Console 配置

**前置**：已上传签名 APK/AAB 到至少一条测试轨道（内测即可）。没有构建包，Play 不允许创建内购商品。

### 4.1 创建订阅

**位置**：Play Console → 选择应用 → 左侧 **Monetize（获利）→ Products → Subscriptions** → Create subscription。

| 字段 | 必填 | 规则 | 本项目取值 |
| --- | --- | --- | --- |
| Product ID | ✅ | 即 Subscription ID。**创建后不可修改，一经使用永久占用** | `storage_pro_gpb` |
| Name | ✅ | ≤55 字符，用户可见，展示在 Play 与系统订阅管理 | `Storage Pro` |
| Benefits | ⭕ | 最多 4 条，每条 ≤40 字符，展示在 Play 订阅页 | 权益要点 4 条 |

### 4.2 创建 Base Plan（用户实际购买的对象）

在订阅详情页点 **Add base plan**，月/年各建一个。

| 字段 | 必填 | 规则 | 本项目取值 |
| --- | --- | --- | --- |
| Base plan ID | ✅ | 创建后不可修改。命名要能自解释 | `monthly-autorenewing` / `yearly-autorenewing` |
| Renewal type | ✅ | **Auto-renewing**（自动续期）或 Prepaid（预付，不自动续） | Auto-renewing |
| Billing period | ✅ | 周 / 月 / 3 月 / 6 月 / 年 | 月 / 年 |
| Grace period | ⭕ | 扣款失败后仍保留权益的天数，**强烈建议开启（如 7 天）**，能显著降低因支付失败造成的非自愿流失 | 7 天 |
| Resubscribe | ⭕ | 允许用户从 Play 订阅页直接重新订阅 | 开启 |
| Tags | ⭕ | 供 Play 端筛选，不影响功能 | 可留空 |
| Regional availability & pricing | ✅ | 选择销售国家 + 定价；可设基准价批量换算 | 对齐 §1.3 的 9 市场 |

创建完必须点 **Activate**，未激活的 Base Plan 无法购买、RevenueCat 也拉不到。

> **向后兼容开关**：如果 App 里还存在使用旧版 RevenueCat SDK（v6 以前）的用户，这些版本不支持「一个订阅多个 Base Plan」，只能看到被标记为向后兼容的那一个。在 Base Plan 的 `⋮` 菜单选 **Use for deprecated billing methods** 来标记，且**每个订阅只能标记一个**。新项目可忽略此项。

### 4.3 创建 Offer（免费试用）

在订阅页点 **Add offer**，为指定 Base Plan 创建。

| 字段 | 必填 | 规则 | 建议 |
| --- | --- | --- | --- |
| Offer ID | ✅ | 不可修改 | `freetrial-7d` |
| 适用 Base Plan | ✅ | 选择要挂载的 Base Plan | 月 / 年各挂一个 |
| Eligibility criteria | ✅ | `New customer acquisition`（新用户首订）/ `Upgrade`（从其他档位升级）/ `Win-back`（召回流失用户） | 首次试用选 New customer acquisition |
| Offer phases | ✅ | 可组合多阶段：**Free trial**（免费）/ Single payment（一次性特价）/ Discounted period（若干周期折扣） | 单阶段 Free trial，时长对齐 §1.3 |
| Regions | ✅ | 选择生效区域 | 全部销售区域 |

创建后同样需要 **Activate**。向后兼容同理：`⋮` → Use for deprecated billing methods，每个 Base Plan 只能标一个 Offer。

### 4.4 创建 Google Cloud Service Account（RevenueCat 对接必需）

> 这一步产出的 JSON 上传到 RC 后**最长需要 36 小时激活**，请优先执行。

**A. 启用 API**（Google Cloud Console，注意选对项目）

1. 启用 [Google Play Android Developer API](https://console.cloud.google.com/apis/library/androidpublisher.googleapis.com)
2. 启用 [Google Play Developer Reporting API](https://console.cloud.google.com/apis/library/playdeveloperreporting.googleapis.com)
3. 顺手启用 [Cloud Pub/Sub API](https://console.cloud.google.com/flows/enableapi?apiid=pubsub)（§4.6 的实时通知要用）

**B. 创建 Service Account**：IAM & Admin → Service Accounts → Create Service Account

| 步骤 | 填写 |
| --- | --- |
| 名称 | 如 `revenuecat-integration` |
| 授予角色（第 2 步） | **Pub/Sub Editor**（启用平台服务器通知）+ **Monitoring Viewer**（监控通知队列）。若创建 Topic 时报权限错误，把 Pub/Sub Editor 换成 **Pub/Sub Admin** |
| 第 3 步 | 可跳过，点 Done |

**C. 下载 JSON 密钥**：在 Service Account 列表 → `⋮` → Manage Keys → Add Key → Create new key → 选 **JSON** → 下载。

> 报 `iam.disableServiceAccountCreation` 或 `iam.disableServiceAccountKeyCreation` 错误 = 组织策略限制。到 IAM & Admin → Organization Policies 临时关闭对应约束（需云平台管理员）。

**D. 记录 Service Account 邮箱**：形如 `xxx@xxx.iam.gserviceaccount.com`，下一步要用。

### 4.5 把 Service Account 邀请进 Play Console

**位置**：Play Console → Users and permissions → Invite user

1. 邮箱填 §4.4D 的 Service Account 邮箱
2. **App permissions**：添加你的应用
3. **Account permissions**：必须勾选以下三项，缺任何一项 RevenueCat 凭证校验都会失败

| 权限 | RevenueCat 用它做什么 | 缺失时的报错 |
| --- | --- | --- |
| View app information and download bulk reports (read-only) | 读取商品信息 | inappproducts API 校验失败 |
| View financial data, orders, and cancellation survey response | 读取订单与财务数据 | subscriptions / monetization API 校验失败 |
| Manage orders and subscriptions | 校验购买、处理退款联动 | subscriptions API 校验失败 |

4. 点 Invite user，返回列表确认账号状态为 Active

### 4.6 配置 Real-Time Developer Notifications（RTDN，强烈建议）

同样不是必需，但能提升价格准确性、加快 Webhook 与图表时效，并让退款/撤单自动同步。

1. 确认 Cloud Pub/Sub API 已启用（§4.4A）
2. **RevenueCat Dashboard** → 你的 Play App 设置 → Service Credentials 下方 → 点 **Connect to Google**，复制生成的 **Pub/Sub Topic ID**
3. **Play Console** → Monetize → **Monetization setup** → Real-time developer notifications：
   - Topic name：粘贴上一步的 Topic ID
   - Notification content：选 **Subscriptions, voided purchases, and all one-time products**
   - 页面右下角 Save changes
4. 点 **Send test notification**，回到 RevenueCat 对应页面确认出现 *Last received* 及最新时间戳

> 测试通知失败时：到 Google Cloud 的该 Topic → Permissions → Add Principal，添加 `google-play-developer-notifications@system.gserviceaccount.com` 并授予 **Pub/Sub Publisher** 角色。若加不进去，是「域名限制共享」组织策略在拦，需临时放开。

### 4.7 License Testing 账号

**位置**：Play Console → 账号级 Settings → License testing，加入 ≥2 个 Google 账号（需为该 Google 账号的真实邮箱）。

| 要点 | 说明 |
| --- | --- |
| 作用 | 测试购买不真实扣款，且续订周期被 Google 压缩到分钟级 |
| 前提 | 测试账号还需加入对应的测试轨道（内测名单） |
| 常见坑 | 测试机上的 Google 账号必须与名单一致；换账号后需清理 Play 商店缓存 |

### 4.8 Gate ④：Google Play 完成检查

- [ ] 签名包已上传并在测试轨道可用
- [ ] Subscription 已创建，Product ID 与 §2.2 一致，Name / Benefits 已填
- [ ] 月 / 年 Base Plan 已创建并 **Activate**，Grace period 已开启
- [ ] Free trial Offer 已创建并 Activate，资格条件与时长正确
- [ ] 定价覆盖全部销售区域
- [ ] Service Account 已创建，角色为 Pub/Sub Editor + Monitoring Viewer，JSON 已入库
- [ ] Service Account 已在 Play Console 获得三项必需权限且状态 Active
- [ ] RTDN Topic 已配置，测试通知在 RC 侧可见
- [ ] ≥2 个 License Testing 账号已配置并加入测试轨道

---

## 5. RevenueCat 配置

**入口**：[app.revenuecat.com](https://app.revenuecat.com/)

### 5.1 创建 Project

| 字段 | 说明 | 本项目取值 |
| --- | --- | --- |
| Project name | 一个 Project 代表一个产品，跨平台共用 | 〔待填〕 |

> 一个 Project 内可挂 iOS / Android / Web 多个 App，它们共享 Entitlement、Offering、Customer。**不要为 iOS 和 Android 各建一个 Project**，否则跨端权益打不通。

### 5.2 添加 App 并录入凭证

Project → **Apps** → 新增。

**iOS App**

| 字段 | 来源 | 注意 |
| --- | --- | --- |
| App name | 自填 | — |
| App Bundle ID | §1.6 | **大小写必须完全一致**，错一个字母凭证校验就失败 |
| In-app purchase key（.p8） | §3.9 | 直接上传下载的原文件，不要改文件名 |
| Issuer ID | §3.9 | — |
| Apple Server Notification URL | RC 自动生成 | 点 **Apply in App Store Connect** 一键写回（§3.10） |

填完点 **Save changes**，RC 会自动校验凭证；出现 **Valid credentials** 且权限项全绿才算通过。

> Save changes 按钮灰掉 = 有必填项没填，逐个展开分区检查。

**Android App**

| 字段 | 来源 | 注意 |
| --- | --- | --- |
| Google Play package name | §1.6 | 与 build.gradle 一致 |
| Service Account Credentials JSON | §4.4C | 上传后**最长 36 小时**激活 |
| Pub/Sub Topic | RC 生成 | 见 §4.6 |

> **加速凭证生效的土办法**：在 Play Console 里随便改一下某个商品的描述并保存，再改回来，通常能让新凭证立刻生效。不保证成功，但值得一试。

**Project 级设置：Restore / Transfer behavior**

在 Project Settings 里确认购买转移策略（如「Transfer if there are no active subscriptions」）。这决定了同一笔商店购买在多个 App User ID 之间如何归属，**上线后再改会影响存量用户**，务必与后端确认账号模型后再定。

### 5.3 导入 Products

Project → **Products** → Import / New。

| 步骤 | 说明 |
| --- | --- |
| 导入 iOS | 凭证正常时可从 App Store Connect 自动拉取；也可手动录入 Product ID |
| 导入 Android | 自动拉取 Base Plan；确认标识为 `storage_pro_gpb:monthly-autorenewing` 形式 |
| 核对 | 4 条记录（iOS 月/年 + Android 月/年）全部出现，且与 §2.2 一致 |

> Android 商品拉不到，99% 是 Service Account 凭证未生效或权限缺失，回 §4.4 / §4.5 复查，不要在这里反复点刷新。

### 5.4 创建 Entitlement

Project → **Entitlements** → New。

| 字段 | 规则 | 本项目取值 |
| --- | --- | --- |
| Identifier | 客户端代码里唯一硬编码的常量，**创建后不要改** | `storage_pro` |
| Description | 内部说明 | 云存储 Pro 权益 |

建好后把 §5.3 的 **4 个 Product 全部 Attach 到这一个 Entitlement**。

> 判断标准：能不能用「买了之后解锁的东西是否相同」来分组。月付和年付解锁的功能一样 → 同一个 Entitlement。只有权益档位不同（如 Plus vs Premium）才需要多个 Entitlement。

### 5.5 创建 Offering 与 Packages

Project → **Offerings** → `+ New`。

| 字段 | 规则 | 本项目取值 |
| --- | --- | --- |
| Identifier | **创建后不可修改** | `default` |
| Description | 内部说明 | 默认订阅陈列 |

进入 Offering → **+ Add package**：

| 字段 | 规则 | 月 | 年 |
| --- | --- | --- | --- |
| Identifier | 从下拉里选与周期匹配的预置值 | `$rc_monthly` | `$rc_annual` |
| Description | 内部说明 | 月付 | 年付 |
| Products | 挂上该周期的 iOS + Android 商品 | 2 个 | 2 个 |

最后把该 Offering 设为 **Default Offering**（Current）。

| 要点 | 说明 |
| --- | --- |
| 排序即展示顺序 | Package 在表格里的拖拽顺序会原样传给 SDK，决定 Paywall 上的默认排列。**建议年付在前**（客单价更高，且能锚定月付价格） |
| 用 current 而非硬编码 | 客户端读 `offerings.current`，之后你就能在 Dashboard 直接换陈列、做 Targeting 与 A/B 实验，全都不用发版 |
| 可随时增删 | 从 Offering 移除 Package 不会删除商品、不影响已有交易与权益 |

### 5.6 配置 Webhook

Project → **Integrations → Webhooks → Add Configuration**。

| 字段 | 填写 | 来源 |
| --- | --- | --- |
| Webhook URL | `https://api.brand.com/v1/revenuecat/webhook` | §1.6 |
| Authorization header | `Bearer {token}` | §1.6 的强随机 Token |
| Environment | **同时勾选 Production 与 Sandbox** | — |
| Event types | 至少覆盖 PRD-2 §4.2.4 的事件清单 | — |

配置完点 **Send Test Event**，确认后端返回 200。

**必须处理的事件**（详见 PRD-2 §4.2.4）：

| 事件 | 业务含义 | 后端动作 |
| --- | --- | --- |
| `INITIAL_PURCHASE` | 首购或试用激活（`is_trial_period` 区分） | 记录流水 + 激活权益 |
| `RENEWAL` | 续费成功 | 延长权益有效期 |
| `CANCELLATION` | 用户关闭自动续费（**本周期仍有权益**） | 标记 `auto_renew=false`，**不要立即收权益** |
| `EXPIRATION` | 到期 | 撤销权益 |
| `BILLING_ISSUE` | 扣款失败进入宽限期 | 保留权益 + 触发提醒 |
| `PRODUCT_CHANGE` | 升降级 | 更新档位 |
| `REFUND` | 退款 | 撤销权益 + 负向流水 |
| `TRANSFER` | 跨账号权益转移 | 至少落库留痕 |

> **最容易出的业务 bug**：把 `CANCELLATION` 当成立即失效。用户取消后到期前仍然享有权益，提前收回会直接引发投诉与退款。

### 5.7 获取 API Keys

Project → **API Keys**。

| Key | 形态 | 给谁 | 敏感级别 |
| --- | --- | --- | --- |
| Public API Key (iOS) | `appl_xxx` | iOS 客户端，可明文进包 | 低 |
| Public API Key (Android) | `goog_xxx` | Android 客户端，可明文进包 | 低 |
| Secret API Key (v2) | `sk_xxx` | 仅后端 | **高，只显示一次** |

### 5.8 密钥分级与存放

| 密钥 | 级别 | 存放 | 可见范围 |
| --- | --- | --- | --- |
| Public API Key | 低 | 代码配置文件 | 全体开发 |
| Secret API Key (v2) | 高 | KMS / Vault | 后端 + 运维 |
| Webhook Auth Token | 高 | KMS / Vault | 后端 + 运维 |
| In-App Purchase Key `.p8` | 高 | KMS / Vault | 技术负责人 + 运维 |
| Service Account JSON | 高 | KMS / Vault | 技术负责人 + 运维 |
| 测试账号密码 | 中 | 团队加密文档 | 开发 + QA |

### 5.9 Gate ⑤：RevenueCat 完成检查

- [ ] Project 已建，iOS + Android App 均在同一 Project 下
- [ ] iOS 凭证显示 **Valid credentials**，权限项全绿
- [ ] Android Service Credentials 已激活（不再报凭证错误）
- [ ] 4 个 Product 已导入且标识与 §2.2 一致
- [ ] Entitlement `storage_pro` 已建并关联全部 4 个 Product
- [ ] Offering `default` 含 `$rc_monthly` + `$rc_annual`，已设为 Current
- [ ] Webhook 已配置（含 Sandbox），Test Event 返回 200
- [ ] API Keys 已分发，高敏感密钥已入 KMS
- [ ] Restore / Transfer behavior 已与后端确认

---

## 6. Paywall 配置与接入

> RevenueCat Paywall 可在 Dashboard 可视化搭建并远程下发：**改文案、改样式、换套餐都不用发版**。这是它相对自研 Paywall 最大的价值，也是本节推荐的默认方案。

### 6.1 内容清单：Paywall 上必须有的元素

以下几项由 Apple / Google 审核硬性要求，**缺失会被拒审**，请在设计阶段就写进设计稿：

| 元素 | 要求 | 常见拒审原因 |
| --- | --- | --- |
| 订阅名称 | 与商店商品的 Display Name 一致 | 名称对不上 |
| 时长与价格 | 明确写出计费周期与价格，多币种需动态取值 | 写死美元价，其他区域价格不符 |
| 自动续费披露 | 明示「到期自动续费直至取消」，说明如何取消 | 完全没写，或藏在折叠区 |
| 试用条款 | 明示试用时长 + 结束后扣费金额与时间 | 只写「免费试用」不写后续扣费 |
| Terms of Service 链接 | 可点击、可打开 | 死链 |
| Privacy Policy 链接 | 可点击、可打开 | 死链 |
| **Restore purchases（恢复购买）** | 必须有明显入口 | **iOS 高频拒审点**，尤其是换机 / 重装用户 |
| 关闭按钮 | 用户能退出 Paywall（除非是完全 Hard Paywall 且业务上成立） | 无法关闭被判为强制付费 |

### 6.2 在 Dashboard 搭建 Paywall

Project → **Paywalls** → **Create paywall**，四种起步方式：

| 方式 | 适用场景 |
| --- | --- |
| **Use a template** | 首次配置**推荐**：官方模板已内建合规区、恢复购买、套餐选择等结构，最快上线 |
| **Generate with AI**（beta） | 有明确风格描述时，用自然语言生成整屏 |
| **Import from Figma** | 设计稿已定稿，用 RevenueCat Figma 插件导入 frame |
| Create from scratch | 有非常特殊的布局要求时才用 |

**编辑器结构**

| 区域 | 作用 |
| --- | --- |
| 左侧 Add component / Layers | 增删组件、调整层级与顺序（拖拽纵向排序，横向缩进决定父子关系） |
| 左侧 Branding | 品牌色与字体，配置一次全局复用 |
| 左侧 Media gallery | 图片 / 视频素材 |
| 左侧 Localization | 多语言文案，新增语言在这里 |
| 左侧 Paywall logic | 条件显隐与变体（如仅对有试用资格的用户显示试用文案） |
| 左侧 Paywall settings | 绑定 Offering、默认语言、Exit offer |
| 中部 Preview | 实时预览，可切换语言 / 深浅色 / 全屏与 Sheet 视图；也能用 RevenueCat 手机 App 真机预览 |
| 右侧 Component properties | 选中组件的样式与行为属性 |

**常用组件**

| 组件 | 用途 |
| --- | --- |
| Package | 可选中的套餐卡片（月 / 年） |
| Purchase button | 触发购买当前选中套餐的 CTA |
| Text / Image / Video / Icon | 基础内容 |
| Stack / Header / Footer | 布局容器；Footer 可固定在底部放合规文案 |
| Feature list | 权益清单 |
| Timeline | 「今天开始试用 → 第 5 天提醒 → 第 7 天扣费」这类试用说明，对降低试用焦虑很有效 |
| Social proof / Award | 评价与奖项，用于增强信任 |
| Tabs / Switch | 多档位或月/年切换 |
| Carousel | 单屏内可横滑的多页内容 |
| Button | 跳转链接（ToS / Privacy）、多页导航、关闭 |

> **安全区规则**：普通组件不会占用顶部安全区；只有「首个占据纵向空间且宽度撑满」的图片会被识别为 Header 图并延伸到顶部。Footer 会自动避让底部安全区。想做通屏头图，就把图片放在最上面并设为满宽。

### 6.3 变量与本地化（不要写死价格）

在 Text 组件中使用变量，价格与周期会随用户所在区域自动本地化：

| 变量 | 输出 |
| --- | --- |
| `{{ product.price }}` | 本地化价格字符串（含货币符号） |
| `{{ product.relative_discount }}` | 相对折扣（用于「年付省 X%」，自动按实际价格算，避免多币种失真） |
| `{{ custom.<key> }}` | 客户端传入的自定义变量（如用户名，用于个性化文案） |

**本地化步骤**：Localization 面板 → 添加语言 → 逐条翻译。默认语言在 Paywall settings 里设置。上线前用 Preview 的语言切换逐个走查，重点看**德语 / 法语等长词语言是否把按钮文案挤破行**。

### 6.4 发布状态

| 状态 | 含义 |
| --- | --- |
| Inactive（草稿） | SDK 拉不到，等同未上线。点 **Save to draft** 进入此状态 |
| Published | SDK 可获取。点 **Publish Paywall** 发布 |

**能否真正被用户看到 = Published + 其绑定的 Offering 是 Current（或通过 Targeting / Experiment 命中）。** 两个条件缺一不可 —— 排查「Paywall 不显示」时先查这两项。

### 6.5 可选：Exit Offer（挽留优惠）

用户关闭 Paywall 未购买时自动弹出备用优惠：

1. 单独建一个 Offering（放折扣或替代定价的 Package）并为它做一个 Paywall
2. 主 Paywall → Paywall settings → Exit offer → 选择该 Offering

> **限制**：Exit Offer 仅在使用 `presentPaywall` / `presentPaywallIfNeeded` 这类**方法调用式**展示时生效；把 `<RevenueCatUI.Paywall>` 组件直接嵌进页面的用法**不支持**。

### 6.6 客户端接入

**依赖**

```json
{
  "dependencies": {
    "react-native-purchases": "<latest>",
    "react-native-purchases-ui": "<latest>"
  }
}
```

**初始化（App 启动时一次）**

```ts
import Purchases from 'react-native-purchases';

Purchases.configure({
  apiKey: Platform.OS === 'ios' ? IOS_PUBLIC_KEY : ANDROID_PUBLIC_KEY,
  appUserID: currentUser.id, // 用你自己的用户 ID，未登录时传 null 用匿名 ID
});
```

**方式 A：按权益自动展示（最省事，推荐用于功能门控入口）**

```tsx
import RevenueCatUI, { PAYWALL_RESULT } from 'react-native-purchases-ui';

const result = await RevenueCatUI.presentPaywallIfNeeded({
  requiredEntitlementIdentifier: 'storage_pro',
});
```

已有权益时不展示，直接返回 `NOT_PRESENTED`。

**方式 B：主动展示（用于「升级」按钮等明确入口）**

```tsx
const result: PAYWALL_RESULT = await RevenueCatUI.presentPaywall();
// 指定非默认陈列：await RevenueCatUI.presentPaywall({ offering });

switch (result) {
  case PAYWALL_RESULT.PURCHASED:
  case PAYWALL_RESULT.RESTORED:
    // 解锁功能
    break;
  case PAYWALL_RESULT.CANCELLED:
  case PAYWALL_RESULT.ERROR:
  case PAYWALL_RESULT.NOT_PRESENTED:
    // 保持原状
    break;
}
```

**方式 C：嵌入式（需要自己控制导航与转场时）**

```tsx
<RevenueCatUI.Paywall
  onPurchaseCompleted={({ customerInfo }) => {/* ... */}}
  onRestoreCompleted={({ customerInfo }) => {/* ... */}}
  onDismiss={() => navigation.goBack()}
/>
```

可用监听器：`onPurchaseStarted` / `onPurchaseCompleted` / `onPurchaseError` / `onPurchaseCancelled` / `onRestoreStarted` / `onRestoreCompleted` / `onRestoreError` / `onDismiss`。

> 原生项目对应 API：iOS SwiftUI 用 `.presentPaywallIfNeeded(requiredEntitlementIdentifier:)` 或 `PaywallView`；Android 用 `PaywallDialog` / `PaywallActivity` 或 Compose `Paywall`。

**权益判断（全 App 唯一判据）**

```ts
const info = await Purchases.getCustomerInfo();
const isPro = typeof info.entitlements.active['storage_pro'] !== 'undefined';
```

> 订阅与一次性课程购买不同：**购买成功后客户端不需要再调后端开通**，`CustomerInfo` 就是权威。后端通过 Webhook 异步落库，用于服务端验权与购买记录展示。

### 6.7 触发点配置（产品侧决策）

Paywall 放在哪里，比 Paywall 长什么样更影响转化。建议在 SOP 执行时同步确认下表：

| 入口 | 触发时机 | Paywall 形态 | 本项目取值 |
| --- | --- | --- | --- |
| Onboarding | 首次启动引导结束 | Soft（可跳过） | 〔待填〕 |
| 功能门控 | 用户触碰付费功能时 | 按权益自动展示 | 〔待填〕 |
| 容量 / 额度提示 | 免费额度即将用尽 | Soft + 用量上下文 | 〔待填〕 |
| 设置页入口 | 主动点「订阅服务」 | 主动展示 | 〔待填〕 |
| 设备绑定后 | 硬件激活成功 | 赠送试用引导 | 〔待填〕 |

### 6.8 埋点核对

Paywall 相关埋点见 PRD-2 §7（`subscription_plan_view` / `subscription_purchase_start` / `subscription_purchase_success` 等）。使用 RevenueCat Paywall 时，RC 侧会自动统计 Paywall 曝光、转化、放弃率与 LTV 图表；**自研 Paywall 则需要手动上报曝光**，否则 RC 的 Paywall 图表全是空的。

### 6.9 Gate ⑥：Paywall 完成检查

- [ ] §6.1 的 9 项合规元素逐项在 Paywall 上可见（尤其恢复购买）
- [ ] 价格与折扣使用变量，未硬编码
- [ ] 全部目标语言已翻译，且长词语言无截断
- [ ] 深色 / 浅色模式均已走查
- [ ] Paywall 状态为 **Published** 且绑定的 Offering 为 Current
- [ ] 客户端能取到 Offering 并正常拉起 Paywall
- [ ] 试用资格文案按资格动态显示（有资格 / 无资格两种账号都验过）
- [ ] Paywall 真实截图已回填到 App Store Connect 的 Review Screenshot

---

## 7. 「我的订阅」配置与接入

### 7.1 先做方案选择

| 方案 | 内容 | 成本 | 建议 |
| --- | --- | --- | --- |
| **A. RevenueCat Customer Center** | 官方预置的订阅管理界面：取消、恢复购买、退款申请（iOS）、换套餐（iOS）、挽留优惠、流失原因调研，全部在 Dashboard 配置 | 低（几乎无客户端代码） | **首次上线推荐**。自带挽留能力与调研数据，自研要做很久 |
| B. 自研订阅管理页 | 自己读 `CustomerInfo` 渲染 | 高 | 品牌一致性要求极高、或需与其他账户信息深度融合时才选 |

两者可以共存：外层用自研页面展示订阅概览，「管理订阅」按钮拉起 Customer Center。

### 7.2 方案 A：配置 Customer Center

**位置**：Project Settings → **Monetization Tools → Customer Center**

**默认已配置的四条路径**

| 路径 | 平台 | 作用 |
| --- | --- | --- |
| Cancellation（取消订阅） | iOS / Android | 引导取消，可挂调研与挽留优惠 |
| Missing Purchases（找不到购买） | iOS / Android | 恢复购买，换机 / 重装的主要自助入口 |
| Refund Request（申请退款） | **仅 iOS** | 直接发起 Apple 退款申请 |
| Plan Changes（更换套餐） | **仅 iOS** | 月 ↔ 年切换 |

> **Android 差异必须提前告知产品与客服**：换套餐与退款在 Android 上没有对应能力，需要跳转 Play 订阅管理页处理。UI 上不要在 Android 显示这两个入口。

**可配置项**

| 配置项 | 位置 | 说明 |
| --- | --- | --- |
| 管理选项增删与排序 | Configuration 标签 | 可增删路径、调整顺序、改标题（标题需引用已存在的本地化 key） |
| 无订阅用户的界面 | Configuration 标签 | 另一套屏幕，通常只提供「恢复购买」 |
| Custom URL | 管理选项类型 | 跳外链或 App 内 deeplink（如跳自己的帮助中心） |
| Custom Action | 管理选项类型 | 挂自定义标识，由客户端回调里执行自己的逻辑 |
| 流失原因调研 | 任意管理选项 | 自定义问题与选项；默认取消调研含「太贵了 / 用不上 / 误购」 |
| 支持邮箱 | 设置项 | 用户恢复购买失败、或在错误平台管理订阅时的求助出口。**不填则不显示求助入口** |
| 版本过旧提示 | 设置项 | 仅 iOS（RevenueCatUI iOS ≥ 5.14.0） |
| 购买历史入口 | 设置项 | 仅 iOS（RevenueCatUI iOS ≥ 5.15.1） |
| 颜色 | 设置项 | Accent Color 全局生效；其余颜色**仅作用于促销优惠界面**，深浅两套可分别设置 |
| 本地化 | Localization 标签 | 官方已内置 32 种语言，只在需要改写措辞时才动 |

**调研结果查看**：RevenueCat → Charts → Customer Center Survey Responses。这是理解流失原因最便宜的数据来源，上线后建议每周看一次。

### 7.3 挽留优惠（有前置依赖，别漏）

Customer Center 默认在取消与退款路径上挂了 `Cancellation Retention Discount` 与 `Refund Retention Discount`，但**这两个优惠不会自动存在**，需要：

1. **先在 App Store Connect / Google Play Console 创建促销优惠**（Promotional Offer / Win-back Offer），记下 offer id
2. RevenueCat → **Lifecycle → Retention → Customer Center 标签**，编辑对应优惠，把「商店商品 → 促销优惠 ID」的映射填进去
3. 可设置资格条件：**First Seen**（首次出现时间）或 **Time Since First Purchase**（首购至今时长），支持「早于 / 晚于」比较，用来只对老用户发券

> **行为提醒**：如果 SDK 找不到与当前订阅匹配的促销优惠 ID，会**直接跳过调研与挽留**，按用户意图执行取消或退款。也就是说：忘了配映射，挽留功能就静默失效，且没有任何报错。这是最隐蔽的一个坑。

### 7.4 接入代码

**依赖**：`react-native-purchases-ui` **≥ 8.7.0**

```tsx
import RevenueCatUI from 'react-native-purchases-ui';

await RevenueCatUI.presentCustomerCenter();
```

带事件监听（用于埋点与自有逻辑）：

```tsx
await RevenueCatUI.presentCustomerCenter({
  callbacks: {
    onFeedbackSurveyCompleted: ({ feedbackSurveyOptionId }) => {/* 上报流失原因 */},
    onShowingManageSubscriptions: () => {/* 用户进入系统订阅管理 */},
    onRestoreStarted: () => {},
    onRestoreCompleted: ({ customerInfo }) => {/* 刷新本地权益 */},
    onRestoreFailed: ({ error }) => {},
    onRefundRequestStarted: ({ productIdentifier }) => {/* 仅 iOS */},
    onRefundRequestCompleted: ({ productIdentifier, refundRequestStatus }) => {/* 仅 iOS */},
    onManagementOptionSelected: ({ option, url }) => {/* url 仅 custom_url 时存在 */},
  },
});
```

### 7.5 方案 B：自研页面的字段映射

若自研，页面数据全部来自 `CustomerInfo`，**不要另建一套订阅状态存储**：

| UI 展示 | 数据来源 | 说明 |
| --- | --- | --- |
| 是否订阅中 | `entitlements.active['storage_pro']` 是否存在 | 唯一判据 |
| 当前套餐 | `entitlements.active['storage_pro'].productIdentifier` | 映射为「月付 / 年付」展示名 |
| 是否试用中 | `periodType === 'TRIAL'` | 决定是否显示「试用中」标签 |
| 下次续费 / 到期时间 | `expirationDate` | 文案随 `willRenew` 变化 |
| 是否自动续费 | `willRenew` | `false` 时显示「将于 X 日到期」 |
| 是否账单异常 | `billingIssueDetectedAt` | 非空则展示宽限期提醒 |
| 购买平台 | `store` | 用于「在 iOS 购买的订阅需到 iOS 设备管理」提示 |

**状态文案矩阵**（建议直接抄）

| 状态 | 判断条件 | 主文案 | 主要 CTA |
| --- | --- | --- | --- |
| 试用中 | active + `periodType=TRIAL` | 试用中，X 月 X 日结束后按 `{price}` 续费 | 管理订阅 |
| 活跃自动续费 | active + `willRenew=true` | 下次续费：X 月 X 日 `{price}` | 管理订阅 / 升级年付 |
| 已取消未到期 | active + `willRenew=false` | 已关闭自动续费，X 月 X 日到期 | 重新开启订阅 |
| 宽限期 | active + `billingIssueDetectedAt` 非空 | 续费失败，请更新支付方式，否则将于 X 日失去权益 | 更新支付方式 |
| 已过期 | 无 active 权益且有历史 | 订阅已到期 | 重新订阅（进 Paywall） |
| 从未订阅 | 无任何记录 | — | 了解订阅权益（进 Paywall） |

**跳转系统订阅管理**

| 平台 | 目标 |
| --- | --- |
| iOS | `https://apps.apple.com/account/subscriptions` |
| Android | Play 订阅管理 deep link（带 package 与 sku 参数直达该订阅） |
| 兜底 | 深链失败时给出文字路径指引，不要留白屏 |

> **合规提醒**：Apple 与 Google 都不允许 App 内直接完成"取消订阅"的最终动作，必须跳转到系统订阅管理页。App 内的「取消」按钮只能是引导。

### 7.6 Gate ⑦：我的订阅完成检查

- [ ] 方案 A / B 已决策
- [ ] （A）Customer Center 路径、调研、支持邮箱、颜色、本地化已配置
- [ ] （A）挽留优惠已在商店创建，且在 Lifecycle → Retention 完成商品映射
- [ ] （A）Android 上未显示 iOS 独有的换套餐 / 退款入口
- [ ] （B）六种状态文案均已实现并自测
- [ ] 「管理订阅」能正确跳到系统订阅页，深链失败有兜底文案
- [ ] 恢复购买路径在换机 / 重装场景验证通过
- [ ] 宽限期提醒可正常展示

---

## 8. 沙盒联调与验收

### 8.1 环境准备

| 平台 | 要点 |
| --- | --- |
| iOS | 真机 + Sandbox 账号（设置 → App Store → Sandbox Account 登录）。模拟器可用 StoreKit Configuration File，但**不会产生 RevenueCat 侧数据**，联调必须用真机 |
| Android | License Testing 账号 + 该账号已加入测试轨道，安装的是测试轨道的包 |
| RevenueCat | 顶部环境切到 **Sandbox** 才能看到测试交易；Webhook 需勾选 Sandbox |

**Apple 沙盒续订加速（参考值，Apple 可能调整）**

| 真实周期 | 沙盒实际时长 |
| --- | --- |
| 1 周 | 3 分钟 |
| 1 个月 | 5 分钟 |
| 2 个月 | 10 分钟 |
| 3 个月 | 15 分钟 |
| 6 个月 | 30 分钟 |
| 1 年 | 1 小时 |

沙盒订阅最多自动续订 12 次后停止。Google 侧同样会压缩测试续订周期到分钟级，具体以 Google 官方文档为准。

### 8.2 测试用例

| # | 用例 | 步骤 | 预期 |
| --- | --- | --- | --- |
| T01 | 首购月付（含试用） | 新沙盒账号 → Paywall → 开始试用 | 支付成功；`storage_pro` 生效；`periodType=TRIAL`；收到 `INITIAL_PURCHASE`（`is_trial_period=true`）；后端落库 |
| T02 | 首购年付 | 同上选年付 | 权益生效；Product ID 为年付；价格与区域一致 |
| T03 | 试用转正付 | 等待沙盒试用到期 | 自动扣费；收到 `RENEWAL`；`periodType` 变为 `NORMAL` |
| T04 | 自动续费 | 等待一个续订周期 | 收到 `RENEWAL`；到期时间延长 |
| T05 | 取消订阅 | 系统订阅页取消 | 收到 `CANCELLATION`；**周期内权益仍在**；我的订阅显示「X 日到期」 |
| T06 | 到期失效 | 取消后等到期 | 收到 `EXPIRATION`；权益关闭；门控生效 |
| T07 | 升级（月→年） | 我的订阅 → 换套餐（iOS）/ Play 内变更 | 收到 `PRODUCT_CHANGE`；proration 由商店处理；档位更新 |
| T08 | 降级（年→月） | 同上 | 下个周期生效；权益不中断 |
| T09 | 扣款失败宽限期 | 沙盒模拟支付失败 | 收到 `BILLING_ISSUE`；权益保留；宽限期提醒展示 |
| T10 | 退款 | 通过 iOS 退款申请 / 后台退款 | 收到 `REFUND`；权益撤销；流水为负 |
| T11 | 恢复购买 | 删除重装后恢复 | 权益恢复；不重复扣费 |
| T12 | 跨端权益 | iOS 购买后 Android 登录同账号 | `CustomerInfo` 中权益一致 |
| T13 | 试用资格 | 已用过试用的账号再次进 Paywall | 不显示试用文案，CTA 变为「立即订阅」 |
| T14 | 多语言 / 多币种 | 切换不同区域沙盒账号 | 价格与文案本地化正确，无截断 |
| T15 | 弱网与异常 | 断网进 Paywall、支付中断网 | 有错误占位与重试，不白屏、不重复扣款 |
| T16 | 未登录 | 游客点付费入口 | 走登录门禁，登录后回到原上下文 |

### 8.3 Gate ⑧：上线前验收

- [ ] T01–T16 全部通过并留存记录
- [ ] RevenueCat Sandbox 中能看到全部测试交易
- [ ] 每类 Webhook 事件后端均返回 200，且业务表数据正确
- [ ] `user_entitlement` 与 RC `CustomerInfo` 抽样一致
- [ ] Paywall 转化漏斗埋点可见数据
- [ ] 客服已拿到常见问题处理手册（宽限期、退款、恢复购买）
- [ ] 对账脚本已就绪（每日比对本地权益与 RC）

---

## 9. 上线与运营配置

| 项 | 建议 |
| --- | --- |
| 灰度节奏 | 5% → 20% → 50% → 100%，每档观察 24h：支付成功率、Webhook 入库率、崩溃率 |
| 上线首日监控 | 购买成功率、Paywall 曝光→购买转化、Webhook 失败率（低于 99% 告警） |
| 可远程调整的手段 | 换 Current Offering、改 Paywall 文案样式、开关 Exit Offer、调整 Customer Center 路径 —— **均不需发版**，出问题优先用这些手段止损 |
| 需要发版才能改的 | Entitlement ID、SDK 初始化逻辑、门控位置、埋点 |
| 上线后 1 周内 | 看 Customer Center 流失原因调研，据此调整定价或权益边界 |

---

## 10. 常见故障排查

| 症状 | 最可能原因 | 处理 |
| --- | --- | --- |
| ASC 侧边栏没有 Subscriptions | Paid Applications Agreement / 税务 / 银行未完成 | 回 §1.2 |
| 商品无法提交审核 | 缺 Review Screenshot，或订阅组未做本地化 | §3.7 / §3.8 |
| RevenueCat 里 iOS 凭证校验失败 | Bundle ID 大小写不符 / Issuer ID 错 / In-App Purchase Key 已被吊销 | §3.9 复查，重新上传 `.p8` |
| 交易在 RC 里没记录，但用户已付款 | **未配置 In-App Purchase Key**（StoreKit 2 必需） | §3.9，这是最严重的一类配置缺失 |
| Android 商品导入失败 | Service Credentials 未生效（≤36h）/ 三项权限缺失 | §4.4 §4.5；用 §5.2 的改描述小技巧加速 |
| RTDN 测试通知收不到 | Pub/Sub API 未启用 / 缺 Publisher 角色 / 域名限制共享策略 | §4.6 |
| `getOfferings()` 返回空 | Offering 未设为 Current / Package 未挂 Product / 商品未激活 | §5.5，Android 还要确认 Base Plan 已 Activate |
| Paywall 不显示 | Paywall 仍是 Inactive，或其 Offering 不是 Current，或 SDK 版本过低 | §6.4 |
| 价格显示为占位或异常 | 商品未过审 / 该区域未定价 / 未用变量取价 | §3.4 §4.2 §6.3 |
| 试用文案对所有人都显示 | 未按试用资格做条件显隐 | §6.3 Paywall logic |
| 取消后用户立刻失去权益 | 后端把 `CANCELLATION` 当作立即失效 | §5.6，改为仅置 `auto_renew=false` |
| 退款后用户仍有权益 | `REFUND` Webhook 未处理成功 | 查 `rc_webhook_events`，必要时手工撤销并补处理逻辑 |
| Customer Center 里挽留优惠不出现 | 商店未创建促销优惠，或 Lifecycle → Retention 未做商品映射 | §7.3，注意失败是静默的 |
| Exit Offer 不生效 | 用了嵌入式 `<RevenueCatUI.Paywall>` 组件 | 改用 `presentPaywall` / `presentPaywallIfNeeded` |
| 同一用户被扣了两笔 | 月/年商品未放在同一个 Subscription Group | §3.1 |

---

## 11. 交付物清单（配置完成后归档）

| # | 交付物 | 交给谁 |
| --- | --- | --- |
| 1 | 本 SOP 填完实际值的版本 | 全体 |
| 2 | Product ID / Entitlement / Package 映射表（§2.2 定稿版） | 客户端 + 后端 + QA |
| 3 | Public API Key（iOS / Android） | 客户端 |
| 4 | Secret API Key、Webhook URL 与 Token 的 KMS 引用路径 | 后端 + 运维 |
| 5 | In-App Purchase Key `.p8`、Issuer ID、Service Account JSON 的 KMS 路径 | 技术负责人 + 运维 |
| 6 | Sandbox / License Testing 账号清单（加密分享） | QA |
| 7 | Paywall 与 Customer Center 配置说明 + 可远程调整项清单 | 产品 + 运营 |
| 8 | 测试用例执行记录（T01–T16） | QA + 产品 |
| 9 | 客服处理手册（宽限期 / 退款 / 恢复购买 / 跨平台订阅） | 客服 |
| 10 | ToS / Privacy Policy 最终 URL | 法务 + 产品 |

---

## 附录 A · 角色分工速查

| 阶段 | 产品 | 财务 | 法务 | 设计 | iOS | Android | 后端 | 运营 | QA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| §1 准备 | 主 | 主 | 主 | 主 | 协 | 协 | 协 | 协 | — |
| §2 命名定稿 | 主 | 协 | — | — | 协 | 协 | 协 | — | — |
| §3 App Store | 协 | 协 | — | 协 | 主 | — | — | 协 | — |
| §4 Google Play | 协 | 协 | — | 协 | — | 主 | 协 | 协 | — |
| §5 RevenueCat | 协 | — | — | — | 协 | 协 | 主 | — | — |
| §6 Paywall | 主 | — | 协 | 主 | 主 | 主 | — | 协 | — |
| §7 我的订阅 | 主 | — | — | 主 | 主 | 主 | 协 | 协 | — |
| §8 联调验收 | 协 | — | — | — | 协 | 协 | 协 | — | 主 |
| §9 上线 | 主 | — | — | — | 协 | 协 | 协 | 主 | 协 |

## 附录 B · 官方文档索引

**RevenueCat**

- [iOS 商品配置](https://www.revenuecat.com/docs/getting-started/entitlements/ios-products) · [Android 商品配置](https://www.revenuecat.com/docs/getting-started/entitlements/android-products)
- [In-App Purchase Key 配置](https://www.revenuecat.com/docs/service-credentials/itunesconnect-app-specific-shared-secret/in-app-purchase-key-configuration) · [Play Service Credentials](https://www.revenuecat.com/docs/service-credentials/creating-play-service-credentials)
- [Apple Server Notifications](https://www.revenuecat.com/docs/platform-resources/server-notifications/apple-server-notifications) · [Google RTDN](https://www.revenuecat.com/docs/platform-resources/server-notifications/google-server-notifications)
- [Offerings](https://www.revenuecat.com/docs/offerings/overview) · [创建 Paywall](https://www.revenuecat.com/docs/tools/paywalls/creating-paywalls) · [展示 Paywall](https://www.revenuecat.com/docs/tools/paywalls/displaying-paywalls)
- [Customer Center 配置](https://www.revenuecat.com/docs/tools/customer-center/customer-center-configuration) · [Customer Center RN 接入](https://www.revenuecat.com/docs/tools/customer-center/customer-center-react-native)
- [Webhooks](https://www.revenuecat.com/docs/integrations/webhooks) · [恢复购买](https://www.revenuecat.com/docs/getting-started/restoring-purchases) · [Google Play 配置检查清单](https://www.revenuecat.com/docs/service-credentials/creating-play-service-credentials/google-play-checklists)

**平台**

- [Apple 自动续期订阅](https://developer.apple.com/app-store/subscriptions/) · [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications/enabling-app-store-server-notifications)
- [Google Play Billing 订阅](https://developer.android.com/google/play/billing/subscriptions) · [RTDN](https://developer.android.com/google/play/billing/realtime_developer_notifications)

**项目内部**

- [PRD-2 存储订阅 V2](./PRD-2-RevenueCat-Storage-Subscription-V2.md)：功能详卡、Webhook 事件表、埋点、数据表
- [PRD-1 课程内购](./PRD-1-RevenueCat-Course-IAP.md)：混合权益架构
- [开发前配置清单](./RevenueCat-Pre-Dev-Setup-Checklist.md)：按团队分工的准备清单与排期
- [订阅生命周期流程图](./flowcharts/storage-subscription-lifecycle.drawio)：完整状态机与数据生命周期

---

*文档结束 · 执行中发现与实际平台界面不一致的地方，请直接更新本文档并记录版本，避免下一个人重复踩坑。*
