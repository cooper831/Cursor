# PRD-2: RevenueCat 存储订阅服务


| 字段     | 内容                                           |
| ------ | -------------------------------------------- |
| 文档版本   | v2.0                                         |
| 创建日期   | 2026-04-03                                   |
| 最近重建   | 2026-04-22（从归档 PRD + 对话记录恢复，流程图统一迁移至 drawio） |
| 文档状态   | Draft                                        |
| 产品负责人  | TBD                                          |
| 技术负责人  | TBD                                          |
| 设计负责人  | TBD                                          |
| 目标上线日期 | TBD（PRD-1 上线后 4~6 周）                         |
| 前置文档   | PRD-1: RevenueCat SDK 接入与课程内购                |
| 配套文档   | RevenueCat-Pre-Dev-Setup-Checklist           |


**变更记录**


| 版本   | 日期         | 变更人 | 变更说明                                                          |
| ---- | ---------- | --- | ------------------------------------------------------------- |
| v1.0 | 2026-04-03 | —   | 从综合 PRD 拆分，聚焦存储订阅                                             |
| v1.1 | 2026-04-03 | —   | 并入 F6a「我的购买」页 + `purchase_log` 表 + F9 购买记录查询 API；扩展 F7 订阅事件处理 |
| v2.0 | 2026-04-22 | —   | 文档重建；全部 Mermaid 流程图迁移为 `flowcharts/prd2-*.drawio` 统一版式        |


**术语表（订阅增量）**


| 术语                          | 定义                                                                       |
| --------------------------- | ------------------------------------------------------------------------ |
| Auto-renewable Subscription | 自动续期订阅；到期自动扣费续订，是本 PRD 的核心产品类型                                           |
| Free Trial                  | 免费试用期；试用期内拥有权益但不扣费                                                       |
| Grace Period                | 宽限期；续费失败后平台给用户一段时间补缴，期间保留权益                                              |
| Billing Retry               | 续费重试；Apple/Google 在续费失败后的自动重试窗口                                          |
| Proration                   | 升降级按比例结算；如月转年时自动折算                                                       |
| Introductory Offer          | 首次订阅的促销价（试用、折扣、按量付费首次）                                                   |
| Promotional Offer           | 向老用户发放的针对性挽留优惠（由 App 主动触发）                                               |
| Link-out                    | Apple External Purchase Link；引导用户跳出 App 在网页完成支付，避开 30% 税（2025 年起对数字商品放开） |


---

## 1. 项目背景与价值

### 1.1 本 PRD 的定位与前置依赖

PRD-2 在 PRD-1 已经交付的基础设施之上，**新增存储订阅业务能力**，并把「我的购买」页面作为两类产品的统一入口落地。

> 架构全景图：见 `[flowcharts/prd2-01-scope.drawio](./flowcharts/prd2-01-scope.drawio)`

**强依赖 PRD-1 已经交付的能力**：

- RevenueCat SDK 双端（iOS + Android + RN）已集成、用户身份体系已打通
- 后端 `/api/v1/revenuecat/webhook` 端点、幂等 + Authorization 校验、`rc_webhook_events` 表已上线
- RevenueCat Dashboard Project / Public API Keys / Secret API Key 已配置

**PRD-2 新增的业务能力**：


| 能力                   | 说明                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------- |
| 存储订阅产品               | `storage_pro` entitlement + 月/年 2 个 package，含免费试用                                            |
| 订阅完整生命周期             | 试用 → 活跃 → 取消 / 宽限 / 过期 / 恢复，全部由 RC 管理                                                        |
| 订阅权益由 RC 授权          | `CustomerInfo.entitlements.active["storage_pro"]` 是权威来源                                      |
| 订阅事件 Webhook 扩展      | 在 PRD-1 的 webhook 端点上新增 RENEWAL / CANCELLATION / EXPIRATION / BILLING_ISSUE / PRODUCT_CHANGE |
| 「我的购买」页              | F6a：同时展示课程（PRD-1）+ 订阅（PRD-2）的购买历史，PRD-1 阶段不建                                                 |
| `purchase_log` 业务流水表 | 随 F6a 一起落地；PRD-1 期间的数据从 `rc_webhook_events.raw_payload` 回溯补录                                 |
| Link-out Stripe 支付   | Phase 2（落在 PRD-2 内部），暂不纳入 MVP，但架构保留位                                                         |


### 1.2 业务价值

- **MRR 收入渠道**：订阅是可预测的经常性收入，显著提升 LTV / 用户粘性
- **产品能力补齐**：云端存储 Pro 是 App 现有免费存储的付费升级款，增加用户留存
- **一站式购买中心**：「我的购买」让用户在任何渠道都能看到自己的全部数字产品
- **Phase 2 Link-out**：为未来降低 Apple 30% 税负、对接独立站订阅体系预埋位

---

## 2. 项目目标与阶段划分

### 2.1 核心目标


| 目标  | 描述              | 可衡量结果                                              | 优先级 |
| --- | --------------- | -------------------------------------------------- | --- |
| G1  | 订阅产品上线          | `storage_pro` 月/年方案通过 Apple + Google 审核并上架         | P0  |
| G2  | 订阅权益由 RC 管理     | 客户端 100% 通过 `CustomerInfo.entitlements` 判断存储服务是否解锁 | P0  |
| G3  | 完整生命周期          | 试用、续费、取消、宽限、过期、升降级、退款，全部可通过 Webhook 正确落库           | P0  |
| G4  | 我的购买页           | 同时展示课程 + 订阅的购买记录，后端提供 `GET /user/{id}/purchases`   | P1  |
| G5  | 免费试用            | 首次订阅支持 7 天免费试用，且仅 1 次试用资格                          | P1  |
| G6  | Link-out Stripe | Phase 2 交付，独立站网页完成 Stripe 支付后权益自动同步至 App           | P2  |


### 2.2 范围边界

> PRD-2 范围图：见 `[flowcharts/prd2-01-scope.drawio](./flowcharts/prd2-01-scope.drawio)`


| 包含（In Scope）                        | 不包含（Out of Scope）                            |
| ----------------------------------- | -------------------------------------------- |
| `storage_pro` 月/年订阅产品配置             | 订阅优惠码 / 促销码（Promotional Offer）本 PRD 不做       |
| 订阅 UI（方案选择、试用引导、管理页）                | 家庭共享                                         |
| 订阅生命周期完整事件处理                        | 多币种运营定价（首期沿用默认定价矩阵）                          |
| 订阅权益门控（存储 Pro 功能）                   | 订阅数据的 BI 自建看板（使用 RC Dashboard）               |
| 「我的购买」页 + `purchase_log` 表 + 查询 API | 订阅退款的用户自助页（Apple / Google 自带）                |
| 订阅升降级（月↔年）                          | 订阅转移 / 合并（TRANSFER 事件仅记录日志，不做业务处理）           |
| Link-out Stripe 支付（Phase 2）         | Apple External Purchase Link 的合规申请（由单独合规项推进） |


### 2.3 阶段划分

- **Phase 1（本 PRD 主交付）**：IAP + GPB 订阅 + 完整生命周期 + 我的购买页
- **Phase 2（本 PRD 延伸）**：Link-out Stripe 支付，独立站 Web 下单后同步至 App

---

## 3. 里程碑与排期


| 里程碑 | 时间       | 主要交付物                                                                                                                                                           |
| --- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M1  | Week 1   | 存储订阅产品配置完成（App Store + Google Play + RC Dashboard）+ 订阅 UI 完成设计稿                                                                                                 |
| M2  | Week 2   | 订阅方案选择页 + 试用引导 UI + 订阅管理页；客户端订阅权益门控                                                                                                                             |
| M3  | Week 3   | 后端 Webhook 新增事件处理（RENEWAL / CANCELLATION / EXPIRATION / BILLING_ISSUE / PRODUCT_CHANGE / REFUND）+ `user_entitlement` + `user_subscription` + `purchase_log` 三张表 |
| M4  | Week 4   | 「我的购买」页（客户端 + 后端 API）+ `purchase_log` 历史数据回溯补录                                                                                                                  |
| M5  | Week 5–6 | Sandbox 全链路测试（试用、续费、退款、升降级、宽限期）+ 双端提审 + 灰度                                                                                                                      |
| M6  | Phase 2  | Link-out Stripe 接入（独立站 Checkout + Stripe → RevenueCat Web Billing）                                                                                              |


> 里程碑甘特图：见 `[flowcharts/prd2-02-milestones.drawio](./flowcharts/prd2-02-milestones.drawio)`

---

## 4. 业务流程图

### 4.1 业务模型定义

#### 4.1.1 订阅产品层级

`storage_pro` 权益通过多个平台 SKU 实现，全部在 default Offering 的 Package 层聚合，客户端无需关心具体 SKU。

> 订阅产品层级：见 `[flowcharts/prd2-03-product-hierarchy.drawio](./flowcharts/prd2-03-product-hierarchy.drawio)`


| Entitlement   | Package               | Product / SKU                | 平台          | 计费周期 | 状态      |
| ------------- | --------------------- | ---------------------------- | ----------- | ---- | ------- |
| `storage_pro` | `storage_pro_monthly` | `storage_pro_monthly_iap`    | iOS IAP     | 月    | Phase 1 |
| `storage_pro` | `storage_pro_monthly` | `storage_pro_monthly_gpb`    | Android GPB | 月    | Phase 1 |
| `storage_pro` | `storage_pro_yearly`  | `storage_pro_yearly_iap`     | iOS IAP     | 年    | Phase 1 |
| `storage_pro` | `storage_pro_yearly`  | `storage_pro_yearly_gpb`     | Android GPB | 年    | Phase 1 |
| `storage_pro` | `storage_pro_monthly` | `storage_pro_monthly_stripe` | Stripe Web  | 月    | Phase 2 |
| `storage_pro` | `storage_pro_yearly`  | `storage_pro_yearly_stripe`  | Stripe Web  | 年    | Phase 2 |


#### 4.1.2 订阅生命周期（核心状态机）

订阅的所有状态及其流转、以及对应的 Webhook 事件，全部由 RevenueCat 管理。客户端只需读取 `CustomerInfo.entitlements.active["storage_pro"]`，后端只需监听 Webhook 入库。

> 订阅生命周期状态机：见 `[flowcharts/prd2-04-subscription-lifecycle.drawio](./flowcharts/prd2-04-subscription-lifecycle.drawio)`


| 状态           | 权益  | 扣费             | 触发 Webhook                                 |
| ------------ | --- | -------------- | ------------------------------------------ |
| 未订阅          | ✗   | ✗              | —                                          |
| 免费试用中        | ✓   | ✗              | `INITIAL_PURCHASE`（`is_trial_period=true`） |
| 活跃订阅（付费）     | ✓   | ✓              | `RENEWAL`                                  |
| 已取消（周期内仍有权益） | ✓   | ✗              | `CANCELLATION`                             |
| 账单问题（宽限期）    | ✓   | —              | `BILLING_ISSUE`                            |
| 已过期          | ✗   | ✗              | `EXPIRATION`                               |
| 升级 / 降级      | ✓   | ✓（按 proration） | `PRODUCT_CHANGE`                           |
| 退款           | ✗   | 退回             | `REFUND`                                   |


#### 4.1.3 权益管理职责

> 混合权益架构（与 PRD-1 一致）：见 `[flowcharts/prd2-05-entitlement-split.drawio](./flowcharts/prd2-05-entitlement-split.drawio)`

- **课程权益**：现有后端系统（延续 PRD-1 的混合架构），RC 仅用于支付与数据分析
- **订阅权益**：RevenueCat **权威管理**
  - 客户端：`Purchases.getCustomerInfo()` 是唯一真理来源
  - 后端：`user_entitlement` 表由 Webhook 自动维护，用于服务端验权、「我的购买」页、对账

### 4.2 核心业务流程

#### 4.2.1 订阅购买流程（IAP / GPB）

含免费试用的完整购买主链路，四泳道时间网格：用户 / App（RC SDK）/ 商店 / RC + 品牌后端。

> 订阅购买流程：见 `[flowcharts/prd2-06-subscription-purchase.drawio](./flowcharts/prd2-06-subscription-purchase.drawio)`

**要点**：

- 订阅支付成功后，**客户端不需要**像课程那样立即调后端开通，`CustomerInfo` 就是权威
- 后端通过 `INITIAL_PURCHASE` Webhook 落库 `user_entitlement` + `user_subscription`，用于服务端验权和购买记录展示
- 免费试用：`INITIAL_PURCHASE` 事件的 `is_trial_period=true`，`expiration_at_ms` 为试用到期时间

#### 4.2.2 订阅权益验证流程

> 订阅权益验证：见 `[flowcharts/prd2-07-entitlement-check.drawio](./flowcharts/prd2-07-entitlement-check.drawio)`

- **客户端**：`CustomerInfo.entitlements.active["storage_pro"].isActive` 决定存储功能是否解锁
- **服务端**：`user_entitlement` 表（由 Webhook 维护）决定「查看存储文件 / 上传 / 下载」等受控接口是否放行

#### 4.2.3 Link-out Stripe 支付流程（Phase 2）

> Link-out 流程：见 `[flowcharts/prd2-08-linkout-stripe.drawio](./flowcharts/prd2-08-linkout-stripe.drawio)`

核心数据流：App → 展示合规提示 → 跳 Web Checkout → Stripe 支付 → Stripe ↔ RevenueCat Web Billing 集成 → RC 自动授权 → 用户返回 App → SDK 刷新 `CustomerInfo` → 解锁。

#### 4.2.4 Webhook 事件处理流程（订阅增量）

> Webhook 处理流程：见 `[flowcharts/prd2-09-webhook-flow.drawio](./flowcharts/prd2-09-webhook-flow.drawio)`

在 PRD-1 已经建好的 `/api/v1/revenuecat/webhook` 端点上，新增下列订阅事件的业务处理。所有事件**先**写入 `rc_webhook_events`（由 PRD-1 建），**再**分派到对应的业务表。


| 事件                                | 业务处理            | 本地数据操作                                                                                                  |
| --------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------- |
| `INITIAL_PURCHASE`（订阅首购 / 试用首次激活） | 记录购买 + 激活权益     | INSERT `purchase_log` + INSERT/UPDATE `user_entitlement` + INSERT `user_subscription`                   |
| `RENEWAL`                         | 续费成功，延长权益有效期    | INSERT `purchase_log` + UPDATE `user_entitlement.expires_at` + UPDATE `user_subscription`               |
| `CANCELLATION`                    | 用户取消续订，当前周期仍有权益 | UPDATE `user_entitlement.auto_renew=false` + UPDATE `user_subscription.status='cancelled_in_cycle'`     |
| `EXPIRATION`                      | 订阅到期，撤销权益       | UPDATE `user_entitlement.is_active=false, expires_at=now` + UPDATE `user_subscription.status='expired'` |
| `BILLING_ISSUE`                   | 进入宽限期，保留权益并告警   | UPDATE `user_subscription.status='grace_period'` + 触发告警 / 站内信                                           |
| `PRODUCT_CHANGE`                  | 升降级（月↔年），更新档位   | UPDATE `user_entitlement.product_id` + UPDATE `user_subscription.plan`                                  |
| `REFUND`                          | 退款，撤销权益         | UPDATE `user_entitlement.is_active=false` + INSERT `purchase_log(type='refund', amount负值)`              |
| `TRANSFER`                        | 权益转移（跨账号）       | 仅记录到 `rc_webhook_events`，MVP 不做业务处理，观察后续诉求                                                              |


---

## 5. 用户画像与 User Story

### 5.1 用户画像（订阅相关）

- **存储升级用户**：已经在使用免费存储，需要更大空间或高级功能
- **首次订阅试用用户**：通过免费试用评估是否长期订阅
- **订阅老用户**：已订阅，定期打开「我的购买」查账单 / 升级 / 取消
- **跨渠道购买用户**：App 内买过课程 + 订阅，需要「我的购买」统一入口查看

### 5.2 User Stories

- **US-201**：作为普通用户，我想在「存储 Pro」页看到月/年两个方案 + 是否有免费试用，以便选择合适的订阅方案
- **US-202**：作为新用户，我想用 7 天免费试用先体验，试用期内可以随时取消不扣费
- **US-203**：作为订阅用户，我想看到下次续费时间与金额，并能直接跳转到系统订阅管理页取消
- **US-204**：作为订阅用户，续费失败进入宽限期时，我希望在 App 内收到清晰的提醒，告诉我如何补缴
- **US-205**：作为订阅用户，我想从月订阅升级到年订阅，差价按 proration 折算
- **US-206**：作为退款用户，Apple / Google 处理退款后，我不应再拥有存储 Pro 功能
- **US-104**（原 PRD-1 移入）：作为用户，我打开「我的购买」能看到我买过的所有课程和订阅、购买时间、金额、订阅状态

---

## 6. 功能需求详述

### 6.1 功能拆分总览

> 功能拆分图：见 `[flowcharts/prd2-10-feature-map.drawio](./flowcharts/prd2-10-feature-map.drawio)`


| 域       | 功能编号    | 功能名                                                                                           |
| ------- | ------- | --------------------------------------------------------------------------------------------- |
| 客户端     | F1-Sub  | 订阅方案选择页                                                                                       |
| 客户端     | F2-Sub  | 订阅购买流程（含免费试用）                                                                                 |
| 客户端     | F3-Sub  | 订阅管理页（我的订阅）                                                                                   |
| 客户端     | F4-Sub  | 订阅权益门控（存储功能）                                                                                  |
| 客户端     | F6a     | **我的购买**页（课程 + 订阅统一）                                                                          |
| 客户端     | F6c     | 宽限期 / 续费失败提醒                                                                                  |
| 后端      | F7-Sub  | Webhook 订阅事件处理（RENEWAL / CANCELLATION / EXPIRATION / BILLING_ISSUE / PRODUCT_CHANGE / REFUND） |
| 后端      | F8-Sub  | `user_entitlement` + `user_subscription` + `purchase_log` 三张表                                 |
| 后端      | F9      | 购买记录查询 API `GET /api/v1/user/{userId}/purchases`（原 PRD-1 移入）                                  |
| 后端      | F10-Sub | 订阅退款联动（REFUND → 撤销 `user_entitlement`）                                                        |
| 后端      | F11-Sub | `purchase_log` 历史回溯补录脚本（从 PRD-1 期 `rc_webhook_events.raw_payload`）                            |
| Phase 2 | F12     | Link-out Stripe 支付（独立站 Checkout + Web Billing 同步）                                             |


### 6.2 客户端功能详述

#### F1-Sub · 订阅方案选择页

**入口**：

- 存储服务主页的"升级到 Pro"CTA
- 存储容量提示条"你的存储快满了，升级 Pro"
- 设置 > 订阅服务

**页面结构**：

- 标题 + 订阅价值主张（3 条核心卖点）
- 两个方案卡片：月（默认）/ 年（带"更划算"角标，折合月价）
- 首次订阅：显示"7 天免费试用"标签 + 细则说明
- 合规区：自动续费条款、隐私政策、使用条款（按 Apple / Google 要求）
- CTA：Start Free Trial（首次）/ Subscribe Now（非首次）

**数据来源**：`Purchases.getOfferings()` 的 `default.availablePackages`

**异常**：Offerings 加载失败 → 错误占位 + Retry；Package 为空 → "Coming Soon"

#### F2-Sub · 订阅购买流程

> 完整流程见 §4.2.1 的 drawio；此处只列关键 API 与 UI 状态

```ts
const { customerInfo } = await Purchases.purchasePackage(selectedPackage);
const hasStoragePro = customerInfo.entitlements.active["storage_pro"] !== undefined;
if (hasStoragePro) navigateToSuccessPage(customerInfo);
```

**要点**：

- 订阅与课程**不同**：支付成功后**不需要**调后端开通权限，`CustomerInfo` 即为权威
- 后端 `INITIAL_PURCHASE` Webhook 异步落库 `user_entitlement` + `user_subscription` + `purchase_log`
- UI 状态：`Idle → Loading → PaymentSheet → Success / UserCancel / PaymentFail`

#### F3-Sub · 订阅管理页（我的订阅）

**信息展示**：

- 当前订阅方案（月 / 年）+ 状态（试用中 / 活跃 / 已取消周期内 / 宽限期 / 已过期）
- 下次续费时间 + 金额
- "管理订阅"按钮 → 跳转 `https://apps.apple.com/account/subscriptions`（iOS）或 Google Play 订阅设置（Android）
- 升降级入口：月 → 年升级

**数据来源**：

- `CustomerInfo.entitlements.active["storage_pro"]`: `expirationDate` / `willRenew` / `productIdentifier` / `periodType`

#### F4-Sub · 订阅权益门控

- 客户端：`storage_pro.isActive` 判断是否解锁存储 Pro 功能
- 触发点：存储功能入口、文件上传时、超出免费额度时
- 缓存策略：App 启动调用 `Purchases.getCustomerInfo()` 刷新；关键操作前（上传大文件）二次刷新

#### F6a · 我的购买页（核心功能，课程 + 订阅统一）

**入口**：

- 用户中心 > 我的购买
- 设置 > 我的购买

**页面结构**：

- Tab 切换：全部 / 课程 / 订阅
- 每条记录卡片展示：
  - 产品名 + 图标 + 平台（App Store / Play Store / Stripe）
  - 类型标签：一次性 / 订阅
  - 购买时间、金额（含币种）
  - 订阅特有：状态、下次续费时间 / 到期时间
  - 退款标识（若有）
- 下拉刷新：触发 `Purchases.getCustomerInfo(fetchPolicy: .fetchCurrent)` + 调 `GET /api/v1/user/{id}/purchases` 拉后端流水

**数据来源（混合）**：

- 课程：后端 `GET /api/v1/user/{id}/purchases` 从 `purchase_log` 返回
- 订阅（实时状态）：`CustomerInfo` 作为权威展示状态 + 下次续费
- 历史流水（所有事件）：后端 `purchase_log` 返回

#### F6c · 宽限期 / 续费失败提醒

- 触发：客户端启动时检测 `CustomerInfo.entitlements.active["storage_pro"].billingIssueDetectedAt != null` 或后端 `user_subscription.status='grace_period'`
- 文案：标准化多语言文案，指引用户"在系统订阅设置中更新付款方式"
- 频率：每日最多 1 次，提示 7 天或到宽限期结束

### 6.3 后端功能详述

#### F7-Sub · Webhook 订阅事件处理（详见 §4.2.4 表 + drawio）

伪代码（在 PRD-1 F7 的基础上扩展事件分发）：

```java
// 已在 PRD-1 中实现的：401 鉴权 + event.id 幂等 + INSERT rc_webhook_events
switch (eventType) {
    case "INITIAL_PURCHASE":
        if (isSubscriptionEntitlement(entitlementId)) {
            insertPurchaseLog(event, /*type*/ isTrial ? "trial_start" : "purchase");
            upsertUserEntitlement(userId, "storage_pro", expiresAt, isActive=true);
            insertUserSubscription(userId, productId, periodType, startAt, expiresAt);
        } else {
            // 课程场景：沿用 PRD-1 的 L3 兜底逻辑
        }
        break;
    case "RENEWAL":
        insertPurchaseLog(event, "renewal");
        updateUserEntitlementExpiresAt(userId, "storage_pro", newExpiresAt);
        updateUserSubscriptionOnRenewal(userId, newExpiresAt);
        break;
    case "CANCELLATION":
        updateUserEntitlementAutoRenew(userId, "storage_pro", false);
        updateUserSubscriptionStatus(userId, "cancelled_in_cycle");
        break;
    case "EXPIRATION":
        updateUserEntitlementActive(userId, "storage_pro", false, /*expiresAt=*/now);
        updateUserSubscriptionStatus(userId, "expired");
        break;
    case "BILLING_ISSUE":
        updateUserSubscriptionStatus(userId, "grace_period");
        triggerBillingIssueAlert(userId);
        break;
    case "PRODUCT_CHANGE":
        updateUserEntitlementProduct(userId, "storage_pro", newProductId);
        updateUserSubscriptionPlan(userId, newProductId, newPeriodType);
        break;
    case "REFUND":
        if (isSubscriptionEntitlement(entitlementId)) {
            insertPurchaseLog(event, "refund", /*amount*/ -event.price);
            updateUserEntitlementActive(userId, "storage_pro", false, /*expiresAt=*/now);
            updateUserSubscriptionStatus(userId, "refunded");
        } else {
            // 课程退款：沿用 PRD-1 的撤销逻辑
        }
        break;
    case "TRANSFER":
        log.info("TRANSFER event observed but not processed in MVP");
        break;
}
return 200;
```

#### F8-Sub · 数据表

`**user_entitlement` — 权益当前状态（订阅场景唯一事实表）**


| 字段             | 类型           | 说明                                                 |
| -------------- | ------------ | -------------------------------------------------- |
| id             | BIGINT AI    | 主键                                                 |
| app_user_id    | VARCHAR(128) | 品牌用户 ID                                            |
| entitlement_id | VARCHAR(64)  | `storage_pro` / `yoga_ball_course`（后者 PRD-1 可不用此表） |
| product_id     | VARCHAR(128) | 当前订阅的 SKU                                          |
| period_type    | VARCHAR(16)  | monthly / yearly / lifetime                        |
| is_active      | BOOLEAN      | 是否当前有效                                             |
| auto_renew     | BOOLEAN      | 是否自动续订                                             |
| expires_at     | DATETIME     | 到期时间（lifetime 为 NULL）                              |
| granted_at     | DATETIME     | 首次授予时间                                             |
| updated_at     | DATETIME     | 最近一次 Webhook 事件时间                                  |


索引：UNIQUE(app_user_id, entitlement_id)

`**user_subscription` — 订阅快照（按订阅而非按事件）**


| 字段                   | 类型           | 说明                                                                         |
| -------------------- | ------------ | -------------------------------------------------------------------------- |
| id                   | BIGINT AI    | 主键                                                                         |
| app_user_id          | VARCHAR(128) |                                                                            |
| product_id           | VARCHAR(128) | 当前 SKU                                                                     |
| period_type          | VARCHAR(16)  | monthly / yearly                                                           |
| status               | VARCHAR(24)  | trialing / active / cancelled_in_cycle / grace_period / expired / refunded |
| is_trial             | BOOLEAN      | 首次是否为试用开始                                                                  |
| original_purchase_at | DATETIME     | 首次订阅时间                                                                     |
| current_period_start | DATETIME     | 当前周期起始                                                                     |
| current_period_end   | DATETIME     | 当前周期到期                                                                     |
| cancelled_at         | DATETIME     | 用户取消时间（可为 NULL）                                                            |
| last_event_at        | DATETIME     | 最近一次 Webhook 事件时间                                                          |


索引：INDEX(app_user_id, status) / INDEX(current_period_end)

`**purchase_log` — 业务流水（课程 + 订阅统一）**


| 字段             | 类型            | 说明                                                              |
| -------------- | ------------- | --------------------------------------------------------------- |
| id             | BIGINT AI     | 主键                                                              |
| app_user_id    | VARCHAR(128)  |                                                                 |
| type           | VARCHAR(24)   | purchase / trial_start / renewal / refund / upgrade / downgrade |
| entitlement_id | VARCHAR(64)   | `yoga_ball_course` / `storage_pro`                              |
| product_id     | VARCHAR(128)  | SKU                                                             |
| store          | VARCHAR(16)   | APP_STORE / PLAY_STORE / STRIPE                                 |
| transaction_id | VARCHAR(128)  | 交易 ID（幂等）                                                       |
| amount         | DECIMAL(10,2) | 金额；退款为负                                                         |
| currency       | VARCHAR(3)    | USD / GBP / EUR …                                               |
| country        | VARCHAR(2)    | 用户国家                                                            |
| event_at       | DATETIME      | 事件发生时间                                                          |
| rc_event_id    | VARCHAR(64)   | 对应 `rc_webhook_events.rc_event_id`，便于回溯                         |


索引：UNIQUE(transaction_id, type) / INDEX(app_user_id, event_at DESC)

> **表关系全景图**：见 `[flowcharts/prd2-11-table-relationship.drawio](./flowcharts/prd2-11-table-relationship.drawio)`

#### F9 · 购买记录查询 API（原 PRD-1 移入）

```
GET /api/v1/user/{userId}/purchases?type=all|course|subscription&cursor=&limit=20
Authorization: Bearer {user_jwt}

Response:
{
  "items": [
    {
      "type": "subscription",
      "product_name": "Storage Pro · Yearly",
      "entitlement_id": "storage_pro",
      "store": "APP_STORE",
      "amount": 39.99,
      "currency": "USD",
      "event_at": "2026-04-03T10:30:00Z",
      "subscription": {
        "status": "active",
        "current_period_end": "2027-04-03T10:30:00Z",
        "auto_renew": true
      }
    },
    {
      "type": "course",
      "product_name": "Yoga Ball Course",
      "entitlement_id": "yoga_ball_course",
      "store": "APP_STORE",
      "amount": 49.99,
      "currency": "USD",
      "event_at": "2026-03-15T08:12:00Z"
    }
  ],
  "next_cursor": "..."
}
```

数据源：`purchase_log` + `user_subscription`（实时状态关联） + `user_entitlement`

#### F11-Sub · `purchase_log` 历史回溯补录

PRD-1 阶段仅建了 `rc_webhook_events`，PRD-2 上线时 `purchase_log` 首次建表。需要一次性脚本把 PRD-1 阶段的购买事件从 `rc_webhook_events.raw_payload` 解析并补录到 `purchase_log`。

- 范围：PRD-1 上线日 ~ PRD-2 上线日
- 事件：`INITIAL_PURCHASE` / `REFUND`（课程相关）
- 幂等：以 `rc_event_id` 作为冲突键，脚本可重复执行
- 验收：`purchase_log` 中 PRD-1 期数据条数 = `rc_webhook_events` 中对应事件条数

---

## 7. 数据埋点需求


| 埋点编号   | 事件名                             | 触发点                      | 关键属性                                 |
| ------ | ------------------------------- | ------------------------ | ------------------------------------ |
| TE-S01 | `subscription_plan_view`        | 进入订阅方案页                  | source（入口位置）                         |
| TE-S02 | `subscription_plan_selected`    | 用户点击月 / 年卡片              | plan（monthly / yearly）               |
| TE-S03 | `subscription_purchase_start`   | 调 `purchasePackage()` 发起 | plan / is_trial                      |
| TE-S04 | `subscription_purchase_success` | SDK 回调成功                 | plan / price / currency / is_trial   |
| TE-S05 | `subscription_purchase_fail`    | SDK 回调失败                 | error_code / error_msg               |
| TE-S06 | `subscription_manage_click`     | 点击管理订阅                   | action（cancel / upgrade / downgrade） |
| TE-S07 | `billing_issue_shown`           | 宽限期提示展示                  |                                      |
| TE-S08 | `my_purchases_view`             | 进入我的购买页                  | tab（all / course / subscription）     |
| TE-S09 | `linkout_start`                 | Phase 2，跳转外部支付           | plan / currency                      |
| TE-S10 | `linkout_return`                | Phase 2，从外部支付返回 App      | result（detected / not_detected）      |


---

## 8. 非功能需求


| 维度   | 指标                                                       |
| ---- | -------------------------------------------------------- |
| 性能   | Webhook 端点 P95 ≤ 1s；「我的购买」首屏 ≤ 1.5s                      |
| 可用性  | Webhook 端点全年可用 ≥ 99.9%                                   |
| 一致性  | 订阅权益状态 `user_entitlement` 与 RC CustomerInfo 的偏差 ≤ 1% / 日 |
| 可观测性 | 每种 Webhook 事件类型有独立处理成功率告警，低于 99% 发飞书                     |
| 安全   | Webhook Authorization 强制校验；对账 API 要求用户 JWT 一致            |
| 合规   | 订阅方案页 100% 包含 Apple / Google 要求的自动续费披露、ToS、隐私政策          |
| 国际化  | 9 市场本地化价格；宽限期 / 试用期等文案多语言                                |


---

## 9. 上线运营策略

- **灰度发布**：5% → 20% → 50% → 100%，每阶段观察 24h 核心指标（支付成功率、续费 Webhook 入库率）
- **订阅功能运营**：上线即刻开启免费试用，首 3 个月关注 T+1 / T+7 / T+30 留存
- **客服预案**：
  - 用户投诉宽限期扣费：引导到系统订阅设置查看；后端查 `user_subscription.status`
  - 用户投诉退款后仍有权益：排查 REFUND Webhook 是否成功；必要时手动 UPDATE `user_entitlement.is_active=false`
  - 用户反馈"我的购买"看不到某笔：对比 `rc_webhook_events` vs `purchase_log`，若前者有后者无，说明分派处理失败，补录

---

## 10. 前置配置事项

全部配置项参见：`[RevenueCat-Pre-Dev-Setup-Checklist.md](./RevenueCat-Pre-Dev-Setup-Checklist.md)`

**PRD-2 特有的追加配置**：

- App Store Connect：创建 `storage_pro_monthly_iap` / `storage_pro_yearly_iap` 自动续期订阅产品 + Subscription Group + Introductory Offer（7 天免费试用）
- Google Play Console：创建 `storage_pro_monthly_gpb` / `storage_pro_yearly_gpb` 订阅产品 + Base Plan + Offer（免费试用）
- RevenueCat Dashboard：
  - 新建 Entitlement `storage_pro`
  - 关联 4 个订阅 Product
  - 新建 Package `storage_pro_monthly` / `storage_pro_yearly`
  - 在 default Offering 中加入上述 Package
  - 扩展 Webhook 订阅事件清单
- Phase 2（Link-out）：Stripe 账户 + Stripe ↔ RevenueCat Web Billing 集成 + 独立站 Checkout 页 + Apple External Purchase Link 合规申请

---

## 11. 风险与缓解


| 风险                      | 影响      | 概率  | 缓解方案                                               |
| ----------------------- | ------- | --- | -------------------------------------------------- |
| Apple / Google 订阅审核未通过  | 阻塞上线    | 中   | 严格遵循自动续费披露模板；安排审核 buffer                           |
| Webhook 丢失 / 延迟         | 订阅状态不同步 | 低   | RC 自动重试；定时对账脚本（每日比对 `user_entitlement` vs RC REST） |
| 宽限期处理不当                 | 用户投诉    | 中   | 明确文案；提前 24h 推送提醒                                   |
| 升降级 proration 计算异常      | 用户投诉金额  | 低   | 全部委托 Apple / Google 原生 proration；不自行计算             |
| Phase 2 Link-out 合规申请被拒 | 延期      | 中   | 提前启动合规材料准备；Phase 1 完全不依赖                           |
| `purchase_log` 历史补录遗漏   | 我的购买有缺条 | 低   | 补录脚本 + 验收比对 + 上线后 7 天内观察用户反馈                       |


---

## 12. 成功指标

### 12.1 上线验证（Go / No-Go）

- 订阅购买成功率 ≥ 95%（不含用户主动取消）
- 试用期转化率 ≥ 40%（行业基准）
- `RENEWAL` Webhook 入库成功率 ≥ 99.9%
- `user_entitlement` 与 RC CustomerInfo 一致率 ≥ 99%

### 12.2 业务指标（首 3 个月）

- 订阅 MRR 月增长率 ≥ 20%
- 取消率 ≤ 10% / 月
- 退款率 ≤ 3%
- 「我的购买」页进入率 ≥ 10%（订阅用户）

### 12.3 长期北极星

- 订阅 LTV / CAC ≥ 3
- 课程 + 订阅组合购买用户占比 ≥ 15%

---

## 附录 A · RevenueCat 关键文档

- Webhook Events: [https://docs.revenuecat.com/docs/webhooks](https://docs.revenuecat.com/docs/webhooks)
- iOS Subscriptions: [https://docs.revenuecat.com/docs/ios-native-subscriptions](https://docs.revenuecat.com/docs/ios-native-subscriptions)
- Android Subscriptions: [https://docs.revenuecat.com/docs/android-native-subscriptions](https://docs.revenuecat.com/docs/android-native-subscriptions)
- Restoring Purchases: [https://docs.revenuecat.com/docs/restoring-purchases](https://docs.revenuecat.com/docs/restoring-purchases)
- Web Billing (Stripe): [https://docs.revenuecat.com/docs/web-billing](https://docs.revenuecat.com/docs/web-billing)
- Promotional Offers: [https://docs.revenuecat.com/docs/ios-subscription-offers](https://docs.revenuecat.com/docs/ios-subscription-offers)

## 附录 B · 流程图索引（全部 drawio）


| 编号      | 文件                                                 | 说明                                               |
| ------- | -------------------------------------------------- | ------------------------------------------------ |
| prd2-01 | `flowcharts/prd2-01-scope.drawio`                  | PRD-2 范围与 PRD-1 的关系                              |
| prd2-02 | `flowcharts/prd2-02-milestones.drawio`             | 里程碑甘特                                            |
| prd2-03 | `flowcharts/prd2-03-product-hierarchy.drawio`      | 订阅产品层级（Entitlement / Package / Product）          |
| prd2-04 | `flowcharts/prd2-04-subscription-lifecycle.drawio` | **订阅生命周期状态机**                                    |
| prd2-05 | `flowcharts/prd2-05-entitlement-split.drawio`      | 混合权益职责分工（与 PRD-1 一致）                             |
| prd2-06 | `flowcharts/prd2-06-subscription-purchase.drawio`  | **订阅购买主链路（4 泳道时间网格）**                            |
| prd2-07 | `flowcharts/prd2-07-entitlement-check.drawio`      | 订阅权益验证流程                                         |
| prd2-08 | `flowcharts/prd2-08-linkout-stripe.drawio`         | Phase 2 Link-out Stripe 支付流程                     |
| prd2-09 | `flowcharts/prd2-09-webhook-flow.drawio`           | **订阅事件 Webhook 处理流程**                            |
| prd2-10 | `flowcharts/prd2-10-feature-map.drawio`            | PRD-2 功能拆分                                       |
| prd2-11 | `flowcharts/prd2-11-table-relationship.drawio`     | 三张表（entitlement / subscription / purchase_log）关系 |


