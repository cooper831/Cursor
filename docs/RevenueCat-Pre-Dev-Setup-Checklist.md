# RevenueCat 接入 — 开发前配置计划与清单


| 字段   | 内容                                           |
| ---- | -------------------------------------------- |
| 文档版本 | v1.1                                         |
| 创建日期 | 2026-04-03（v1.1 于 2026-04-22 更新，流程图转 drawio） |
| 文档状态 | Draft                                        |
| 适用范围 | PRD-1（课程内购）+ PRD-2（存储订阅）共用的前置配置              |
| 负责人  | 产品（总协调）+ 技术负责人                               |


**本文档用途：**

1. 梳理 **App Store Connect / Google Play Console / RevenueCat Dashboard** 三方的完整配置清单
2. 规划配置顺序与时间计划（含依赖关系）
3. 明确各团队（产品 / 法务 / 设计 / 财务 / 运营 / 技术）需要提供的信息清单
4. 最终产出一份交付给**开发团队**的配置结果清单（API Key、Product ID 等）

---

## 0. 配置总览

### 0.1 三方配置依赖关系图

> 📎 交互式流程图：`[flowcharts/checklist-01-dependency.drawio](./flowcharts/checklist-01-dependency.drawio)` · 用 Draw.io Integration 插件打开

**要点速览**

- **Phase 0 前置准备**（黄）→ 所有平台配置的前置条件，产品/法务/设计/财务/运营/技术六方协同
- **Phase 1 App Store Connect**（蓝）& **Phase 2 Google Play Console**（绿）→ **可并行执行**，缩短整体周期
- **Phase 3 RevenueCat Dashboard**（紫）→ 需要汇总 Phase 1/2 的产出（Product ID、Shared Secret、Service Account JSON 等）才能开始
- **Phase 4 交付开发团队**（橙）→ 最终产出：Public/Secret API Key、Webhook URL/Token、Product ID、Entitlement ID
- ⚠️ **关键路径**：Apple / Google 商品审核 24-48h，建议配置工作提前 1 周启动

### 0.2 时间规划（建议 1 周完成）

> 📎 交互式甘特图：`[flowcharts/checklist-02-gantt.drawio](./flowcharts/checklist-02-gantt.drawio)` · 用 Draw.io Integration 插件打开

**排期速览（基准起始 2026-04-06 周一）**


| Day       | Phase 0 前置         | Phase 1 App Store                            | Phase 2 Google Play                                  | Phase 3 RC                | 验证/交付                        |
| --------- | ------------------ | -------------------------------------------- | ---------------------------------------------------- | ------------------------- | ---------------------------- |
| Day 1 Mon | 账号 / 素材 / 法务 Start | —                                            | —                                                    | —                         | —                            |
| Day 2 Tue | 法务 Done            | 创建 IAP & 订阅商品                                | 创建 In-app & Subscription                             | —                         | —                            |
| Day 3 Wed | —                  | 🔴 Apple 审核 (Crit) · Shared Secret · Sandbox | 🔴 Google 审核 (Crit) · Service Account · License Test | —                         | —                            |
| Day 4 Thu | —                  | 🔴 Apple 审核 (Crit) 继续                        | 🔴 Google 审核 (Crit) 继续                               | Project / App 关联          | —                            |
| Day 5 Fri | —                  | —                                            | —                                                    | Entitlement & Offering 配置 | —                            |
| Day 6 Sat | —                  | —                                            | —                                                    | Webhook 配置 & Test Event   | —                            |
| Day 7 Sun | —                  | —                                            | —                                                    | —                         | **Sandbox 端到端测试 + 🏁 交付里程碑** |


> 🔴 = 关键路径（Apple / Google 商品审核通常 24~48 小时），该阶段可并行推进 RC 账号初始化节省等待时间。

---

## 1. Phase 0: 前置准备（所有团队输入）

**这一阶段必须在其他 Phase 之前完成。所有信息收集齐全后再开始平台配置，避免反复。**

### 1.1 账号与权限准备


| 项                            | 责任方         | 要求                        | 产出          |
| ---------------------------- | ----------- | ------------------------- | ----------- |
| Apple Developer Program 企业账号 | 运营 / IT     | 已有账号，确认 Admin 角色          | 账号主体信息      |
| Google Play Developer 账号     | 运营 / IT     | 已有账号，确认 Admin 角色          | 账号主体信息      |
| RevenueCat 账号                | 技术负责人       | 注册新账号或复用现有                | 账号邮箱 + 初始密码 |
| App Store Connect 访问权限       | iOS 负责人     | 获得 Admin 或 App Manager 权限 | 账号添加        |
| Google Play Console 访问权限     | Android 负责人 | 获得 Admin 权限               | 账号添加        |
| Google Cloud 访问权限            | Android 负责人 | 用于创建 Service Account      | 项目访问        |


### 1.2 产品信息（产品团队提供）


| 项                         | 责任方     | 示例 / 说明                                               | 状态  |
| ------------------------- | ------- | ----------------------------------------------------- | --- |
| **课程产品正式名称**              | 产品      | 如 "Yoga Ball Prenatal Course"                         | 待定  |
| **课程英文描述**（短版 ≤45 字 + 长版） | 产品 + 内容 | 用于 App Store/Google Play 商品页                          | 待定  |
| **9 市场课程定价**              | 产品 + 财务 | 见 PRD-1 §8.5（US/CA/UK/FR/DE/IT/ES/AE/SA）              | 待定  |
| **订阅产品名称**（PRD-2）         | 产品      | 如 "Storage Pro"                                       | 待定  |
| **订阅方案与定价**（月/年）          | 产品 + 财务 | 月度价格、年度价格、年度折扣比例                                      | 待定  |
| **免费试用期时长**（PRD-2）        | 产品      | 推荐 7 天 / 14 天 / 30 天                                  | 待定  |
| **Product ID 命名规范**（技术建议） | 技术      | 推荐：`yoga_ball_course_iap` / `storage_pro_monthly_iap` | 技术定 |


### 1.3 设计素材（设计团队提供）


| 项                 | 规格                       | 责任方       | 状态  |
| ----------------- | ------------------------ | --------- | --- |
| App Store IAP 商品图 | 640x900 或 1024x1024（PNG） | 设计        | 待提供 |
| Google Play 商品图   | 540x300（PNG/JPG）         | 设计        | 待提供 |
| 课程预览视频（≥1 段）      | MP4，2~5 分钟               | 内容 + 视频团队 | 待提供 |
| 课程封面图（App 内展示）    | 多尺寸适配                    | 设计        | 待提供 |
| 订阅方案选择页设计稿（PRD-2） | Figma / 设计规范             | 设计        | 待提供 |


### 1.4 法务文档（法务团队提供）


| 文档                     | 责任方     | 要求                                | 状态  |
| ---------------------- | ------- | --------------------------------- | --- |
| Terms of Service       | 法务 + 产品 | 必须包含数字产品销售条款、订阅条款（PRD-2）          | 待定稿 |
| Privacy Policy         | 法务 + 产品 | **必须包含 RevenueCat 作为第三方数据处理方的说明** | 待定稿 |
| 订阅合规文案模板（PRD-2）        | 法务      | Apple 要求的订阅告知条款（见 PRD-2 §8.2）     | 待定稿 |
| Terms / Privacy 公网 URL | 产品 + 技术 | 文档托管在品牌官网的可访问 URL                 | 待上线 |


> **⚠️ 重要**：Privacy Policy 必须包含 RevenueCat 相关条款，否则 App Store 审核可能被拒。参考 [RevenueCat 数据处理说明](https://www.revenuecat.com/privacy)。

### 1.5 银行与税务（财务团队提供）


| 项                             | 责任方 | 说明                                   | 状态  |
| ----------------------------- | --- | ------------------------------------ | --- |
| Apple Paid Applications 协议已签署 | 财务  | 在 App Store Connect 的 Agreements 页面  | 待确认 |
| Apple 银行账户信息已填写               | 财务  | 支付结算用                                | 待确认 |
| Apple 税务表单已提交                 | 财务  | US W-8BEN / W-9 等                    | 待确认 |
| Google Play 商家账户已激活           | 财务  | Google Play Console Payments profile | 待确认 |
| Google 银行账户信息已填写              | 财务  | 同上                                   | 待确认 |


> **⚠️ 未完成以上财务配置，无法上架付费商品。**

### 1.6 后端技术准备（后端团队）


| 项                           | 责任方     | 说明                                              | 状态      |
| --------------------------- | ------- | ----------------------------------------------- | ------- |
| Webhook 端点域名                | 后端 + IT | HTTPS，TLS 1.2+                                  | 待准备     |
| Webhook 端点 URL              | 后端      | 如 `https://api.brand.com/v1/revenuecat/webhook` | 待准备     |
| Webhook Authorization Token | 后端      | 生成强随机 Token（≥32 字符）用于 RC 验证                     | 待生成     |
| 密钥管理方案                      | 后端      | 环境变量 / KMS / Vault 存储 Secret Key                | 待定      |
| 现有课程权益接口文档                  | 后端      | 查询 / 开通 / 撤销 三个接口（PRD-1 附录 D #6-9）              | **待调研** |


---

## 2. Phase 1: App Store Connect 配置

**前置条件**：Phase 0 全部完成 + iOS Bundle ID 已创建。

### 2.1 PRD-1（课程 IAP）配置步骤


| #   | 步骤                            | 输入（来自 Phase 0）                    | 产出                              | 负责方      |
| --- | ----------------------------- | --------------------------------- | ------------------------------- | -------- |
| 1   | 创建 Non-Consumable IAP         | Product ID：`yoga_ball_course_iap` | —                               | iOS      |
| 2   | 填写 Reference Name             | 产品团队提供的正式名称                       | —                               | iOS + 运营 |
| 3   | 填写 Display Name               | 同上（可按市场本地化）                       | —                               | iOS + 运营 |
| 4   | 填写 Description                | Phase 0 §1.2 的课程描述                | —                               | iOS + 运营 |
| 5   | 上传商品图                         | 设计提供的 1024x1024 图                 | —                               | iOS + 设计 |
| 6   | 配置 9 市场定价                     | 财务提供的本地化价格                        | —                               | iOS + 财务 |
| 7   | 提交审核                          | —                                 | **Product ID（课程 IAP）**          | iOS      |
| 8   | 生成 App-Specific Shared Secret | App > App Information             | **Shared Secret**               | iOS      |
| 9   | 创建 App Store Connect API Key  | Users and Access > Keys           | **Key ID + Issuer ID + .p8 文件** | iOS      |
| 10  | 添加 Sandbox Tester 账号（≥2 个）    | Users and Access > Sandbox        | **Sandbox 测试账号**                | iOS      |


### 2.2 PRD-2（存储订阅）配置步骤


| #   | 步骤                            | 输入                        | 产出                        | 负责方      |
| --- | ----------------------------- | ------------------------- | ------------------------- | -------- |
| 1   | 创建 Subscription Group         | Group Name：`Storage Pro`  | —                         | iOS      |
| 2   | 创建 Auto-Renewable：月度          | `storage_pro_monthly_iap` | —                         | iOS      |
| 3   | 创建 Auto-Renewable：年度          | `storage_pro_yearly_iap`  | —                         | iOS      |
| 4   | 配置 Introductory Offer         | 免费试用 X 天（Phase 0 §1.2）    | —                         | iOS + 产品 |
| 5   | 配置 9 市场定价                     | 财务提供的价格                   | —                         | iOS + 财务 |
| 6   | 填写 Display Name + Description | 产品提供                      | —                         | iOS + 运营 |
| 7   | 提交审核                          | —                         | **Product ID（月度 + 年度订阅）** | iOS      |


> PRD-2 可与 PRD-1 同批次配置，减少审核等待。

### 2.3 Phase 1 产出清单（需要传递到 Phase 3）

```
iOS 产出信息
──────────────────────────────────
✓ Product ID:
  - yoga_ball_course_iap
  - storage_pro_monthly_iap  (PRD-2)
  - storage_pro_yearly_iap   (PRD-2)
✓ App-Specific Shared Secret:      xxxx (保密)
✓ App Store Connect API:
  - Key ID:                        xxxx
  - Issuer ID:                     xxxx
  - .p8 私钥文件:                  xxxx.p8 (保密)
✓ Bundle ID:                       com.brand.app
✓ Sandbox Tester 账号（≥2 个）:    test@xxx.com / ...
```

---

## 3. Phase 2: Google Play Console 配置

**前置条件**：Phase 0 全部完成 + Android App 已上传到 Google Play Console（至少内测轨道）。

### 3.1 PRD-1（课程一次性购买）配置步骤


| #   | 步骤                          | 输入                                | 产出                 | 负责方          |
| --- | --------------------------- | --------------------------------- | ------------------ | ------------ |
| 1   | 创建 In-app Product（One-time） | Product ID：`yoga_ball_course_gpb` | —                  | Android      |
| 2   | 填写 Name + Description       | 产品提供                              | —                  | Android + 运营 |
| 3   | 配置 9 市场定价                   | 财务提供的价格                           | —                  | Android + 财务 |
| 4   | 上传商品图                       | 设计提供                              | —                  | Android + 设计 |
| 5   | 激活商品                        | —                                 | **Product ID（课程）** | Android      |


### 3.2 PRD-2（存储订阅）配置步骤


| #   | 步骤                              | 输入                        | 产出  | 负责方          |
| --- | ------------------------------- | ------------------------- | --- | ------------ |
| 1   | 创建 Subscription                 | `storage_pro`             | —   | Android      |
| 2   | 添加 Base Plan：Monthly            | `storage_pro_monthly_gpb` | —   | Android      |
| 3   | 添加 Base Plan：Yearly             | `storage_pro_yearly_gpb`  | —   | Android      |
| 4   | 为 Base Plan 添加 Offer：Free Trial | 试用天数                      | —   | Android + 产品 |
| 5   | 配置 9 市场定价                       | 财务提供                      | —   | Android + 财务 |


### 3.3 Service Account 配置（RC 对接必需）


| #   | 步骤                                        | 产出                        | 负责方          |
| --- | ----------------------------------------- | ------------------------- | ------------ |
| 1   | Google Cloud 创建 Service Account           | **Service Account Email** | Android + IT |
| 2   | 授予 "Financial Data" + "Manage Orders" 权限  | —                         | Android      |
| 3   | 导出 JSON Key 文件                            | **service-account.json**  | Android      |
| 4   | Google Play Console 激活 Play Developer API | —                         | Android      |
| 5   | 添加 License Test 账号                        | **测试账号列表**                | Android      |


### 3.4 Phase 2 产出清单

```
Android 产出信息
──────────────────────────────────
✓ Product ID:
  - yoga_ball_course_gpb
  - storage_pro_monthly_gpb   (PRD-2)
  - storage_pro_yearly_gpb    (PRD-2)
✓ Package Name:                    com.brand.app
✓ Service Account Email:           xxx@xxx.iam.gserviceaccount.com
✓ Service Account JSON Key:        service-account.json (保密)
✓ License Test 账号（≥2 个）:      test@xxx.com / ...
```

---

## 4. Phase 3: RevenueCat Dashboard 配置

**前置条件**：Phase 1 + Phase 2 全部完成，产出信息齐全。

### 4.1 项目初始化


| #   | 步骤                 | 输入                                            | 产出              | 负责方   |
| --- | ------------------ | --------------------------------------------- | --------------- | ----- |
| 1   | 登录 RevenueCat 注册账号 | 邮箱                                            | —               | 技术负责人 |
| 2   | 创建 Project         | 项目名：如 "Brand App"                             | Project ID      | 技术    |
| 3   | 添加 iOS App         | Bundle ID + Shared Secret + APNs Key + .p8 文件 | iOS App 已关联     | 技术    |
| 4   | 添加 Android App     | Package Name + Service Account JSON           | Android App 已关联 | 技术    |


### 4.2 Entitlement（权益）配置


| #   | 步骤                                  | 说明   | 产出    | 负责方 |
| --- | ----------------------------------- | ---- | ----- | --- |
| 1   | 创建 Entitlement：`yoga_ball_course`   | 课程权益 | 权益 ID | 技术  |
| 2   | 创建 Entitlement：`storage_pro`（PRD-2） | 订阅权益 | 权益 ID | 技术  |


### 4.3 Product 导入与关联


| #   | 步骤                                  | 说明                                                                   | 负责方 |
| --- | ----------------------------------- | -------------------------------------------------------------------- | --- |
| 1   | 导入 iOS Products                     | 从 App Store Connect 自动拉取或手动录入                                        | 技术  |
| 2   | 导入 Android Products                 | 同上                                                                   | 技术  |
| 3   | 关联 Products → Entitlements          | `yoga_ball_course_iap` + `yoga_ball_course_gpb` → `yoga_ball_course` | 技术  |
| 4   | PRD-2：关联订阅 Products → `storage_pro` | 4 个订阅 Product 关联到同一权益                                                | 技术  |


### 4.4 Offering 配置


| #   | 步骤                              | 说明                                                 | 负责方 |
| --- | ------------------------------- | -------------------------------------------------- | --- |
| 1   | 创建 Offering：`default`           | 默认套餐                                               | 技术  |
| 2   | 添加 Package：课程                   | 关联 `yoga_ball_course_iap` + `yoga_ball_course_gpb` | 技术  |
| 3   | PRD-2：添加 Package：monthly        | 关联月度订阅 Products                                    | 技术  |
| 4   | PRD-2：添加 Package：yearly         | 关联年度订阅 Products                                    | 技术  |
| 5   | 设置 `default` 为 Current Offering | —                                                  | 技术  |


### 4.5 Webhook 配置


| #   | 步骤                                          | 输入（来自后端）                               | 负责方     |
| --- | ------------------------------------------- | -------------------------------------- | ------- |
| 1   | Integrations > Webhooks > Add Configuration | —                                      | 技术      |
| 2   | 填写 Webhook URL                              | Phase 0 §1.6 后端提供的 URL                 | 技术 + 后端 |
| 3   | 填写 Authorization Header                     | `Bearer {token}`（Phase 0 §1.6 的 Token） | 技术 + 后端 |
| 4   | 选择环境                                        | 勾选 Production + Sandbox                | 技术      |
| 5   | 发送 Test Event                               | 后端接收到 TEST 事件，返回 200                   | 技术 + 后端 |


### 4.6 API Key 生成与记录


| #   | 步骤                          | 产出              | 用途            | 负责方 |
| --- | --------------------------- | --------------- | ------------- | --- |
| 1   | 记录 Public API Key (iOS)     | `appl_xxxxxxxx` | 给 iOS 客户端     | 技术  |
| 2   | 记录 Public API Key (Android) | `goog_xxxxxxxx` | 给 Android 客户端 | 技术  |
| 3   | 生成 Secret API Key（v2）       | `sk_xxxxxxxx`   | 给后端服务器（批量授权等） | 技术  |


> **⚠️ Secret Key 只在生成时显示一次，必须立即保存到密钥管理系统。**

### 4.7 Phase 3 产出清单

```
RevenueCat 产出信息
──────────────────────────────────
✓ Project ID:                      xxxx
✓ Entitlement:
  - yoga_ball_course
  - storage_pro                    (PRD-2)
✓ Offering:                        default
  - Packages: course / monthly / yearly
✓ Public API Key (iOS):            appl_xxxxxxxx
✓ Public API Key (Android):        goog_xxxxxxxx
✓ Secret API Key (v2):             sk_xxxxxxxx (保密)
✓ Webhook:
  - URL:                           https://api.brand.com/v1/revenuecat/webhook
  - Auth Token:                    Bearer xxxx (保密)
  - Test Event 验证:               通过 ✅
```

---

## 5. Phase 4: 交付给开发团队的配置产出清单

### 5.1 给 iOS 客户端开发


| 项                       | 值                   | 存储位置                   |
| ----------------------- | ------------------- | ---------------------- |
| Public API Key (iOS)    | `appl_xxxxxxxx`     | Info.plist / 配置文件（明文可） |
| Entitlement ID          | `yoga_ball_course`  | 代码常量                   |
| Offering Identifier     | `default`           | 代码常量                   |
| Package Identifier (课程) | 由 Offering 返回，无需硬编码 | —                      |
| Bundle ID               | `com.brand.app`     | Xcode                  |
| Sandbox Tester 账号       | 测试用                 | 团队共享文档                 |


### 5.2 给 Android 客户端开发


| 项                        | 值                  | 存储位置                |
| ------------------------ | ------------------ | ------------------- |
| Public API Key (Android) | `goog_xxxxxxxx`    | gradle / 配置文件（明文可）  |
| Entitlement ID           | `yoga_ball_course` | 代码常量                |
| Offering Identifier      | `default`          | 代码常量                |
| Package Name             | `com.brand.app`    | AndroidManifest.xml |
| License Test 账号          | 测试用                | 团队共享文档              |


### 5.3 给 React Native 层开发


| 项   | 说明                                        |
| --- | ----------------------------------------- |
| 依赖  | `react-native-purchases ≥ 7.x`            |
| 初始化 | 不重复 configure，复用原生层实例                     |
| 常量  | Entitlement ID / Offering ID 通过 RN 配置文件同步 |


### 5.4 给后端开发


| 项                           | 值                                             | 存储方式                      |
| --------------------------- | --------------------------------------------- | ------------------------- |
| Secret API Key (v2)         | `sk_xxxxxxxx`                                 | **环境变量 / KMS（必须加密）**      |
| Webhook URL                 | `https://api.brand.com/v1/revenuecat/webhook` | 已对外                       |
| Webhook Authorization Token | `xxxx`                                        | **环境变量 / KMS**            |
| Entitlement ID              | `yoga_ball_course` + `storage_pro`            | 代码常量                      |
| Product ID 映射表              | Product ID → Course ID / Subscription Plan    | 配置表                       |
| App Store Shared Secret     | `xxxx`                                        | **KMS**（如需后端直接验证 Receipt） |


### 5.5 Product ID 映射表（关键配置）


| RevenueCat Entitlement | Store      | Product ID                | 业务 ID                            |
| ---------------------- | ---------- | ------------------------- | -------------------------------- |
| `yoga_ball_course`     | APP_STORE  | `yoga_ball_course_iap`    | course:yoga_ball_course          |
| `yoga_ball_course`     | PLAY_STORE | `yoga_ball_course_gpb`    | course:yoga_ball_course          |
| `storage_pro`          | APP_STORE  | `storage_pro_monthly_iap` | subscription:storage_pro:monthly |
| `storage_pro`          | APP_STORE  | `storage_pro_yearly_iap`  | subscription:storage_pro:yearly  |
| `storage_pro`          | PLAY_STORE | `storage_pro_monthly_gpb` | subscription:storage_pro:monthly |
| `storage_pro`          | PLAY_STORE | `storage_pro_yearly_gpb`  | subscription:storage_pro:yearly  |


### 5.6 给 QA 测试团队


| 项                       | 说明                          |
| ----------------------- | --------------------------- |
| iOS Sandbox Tester 账号   | Phase 1 §2.1 产出，测试 IAP 用    |
| Android License Test 账号 | Phase 2 §3.3 产出，测试 GPB 用    |
| RC Dashboard 只读账号       | 用于查看交易记录                    |
| Webhook 事件日志位置          | 后端提供（`rc_webhook_events` 表） |


---

## 6. 验收 Checklist

**所有项目必须勾选通过，才算配置完成。**

### 6.1 App Store Connect

- 课程 IAP Product 已创建且通过审核
- PRD-2 订阅 Products 已创建（可与课程同批审核）
- 9 市场定价已配置
- App-Specific Shared Secret 已生成并安全保存
- App Store Connect API Key 已生成，`.p8` 文件安全保存
- ≥2 个 Sandbox Tester 账号已添加
- Paid Applications Agreement 已签署
- 银行账户与税务信息已完成

### 6.2 Google Play Console

- 课程 In-app Product 已创建并激活
- PRD-2 Subscription + Base Plans 已创建
- 9 市场定价已配置
- Service Account 已创建并授予权限
- JSON Key 已下载并安全保存
- Play Developer API 已激活
- ≥2 个 License Test 账号已添加
- Payments profile 已激活

### 6.3 RevenueCat Dashboard

- Project 已创建
- iOS App + Android App 已关联（状态为绿色/Active）
- Entitlement `yoga_ball_course` 已创建
- Entitlement `storage_pro` 已创建（PRD-2）
- 全部 Products 已导入并关联到对应 Entitlement
- Offering `default` 已创建并设为 Current
- Offering 包含 3 个 Package（课程 + 月 + 年）
- Webhook URL 已配置
- Webhook Authorization Token 已配置
- Test Event 已成功投递（后端返回 200）
- Public API Keys + Secret API Key 已生成并分发

### 6.4 后端准备

- Webhook 端点已上线（HTTPS）
- Authorization Token 已存入 KMS
- `rc_webhook_events` 表已建
- `course_grant_log` 表已建
- 幂等去重逻辑已实现
- RC 测试事件处理返回 200

### 6.5 法务与合规

- Terms of Service 已上线公网 URL
- Privacy Policy 已上线公网 URL（含 RC 条款）
- 订阅合规文案模板已确认（PRD-2）

### 6.6 端到端连通性测试

- iOS Sandbox 账号购买课程 → 支付成功 → RC 收到 → Webhook 推送 → 后端 200
- Android License Test 账号购买课程 → 同上
- 跨端测试：iOS 购买后 Android 登录同账号，`CustomerInfo` 有该课程记录

---

## 7. 信息安全与访问管理

### 7.1 密钥分级


| 密钥                           | 敏感级别            | 存储位置        | 可见范围       |
| ---------------------------- | --------------- | ----------- | ---------- |
| Public API Key (iOS/Android) | 低（嵌入 App 二进制即可） | 代码配置文件      | 全体客户端      |
| Secret API Key (v2)          | **高**           | KMS / Vault | 后端服务 + 运维  |
| Webhook Auth Token           | **高**           | KMS / Vault | 后端服务 + 运维  |
| App Store Shared Secret      | **高**           | KMS / Vault | 仅后端（可选）    |
| App Store Connect API .p8    | **高**           | KMS / Vault | 技术负责人 + 运维 |
| Google Service Account JSON  | **高**           | KMS / Vault | 技术负责人 + 运维 |
| Sandbox Tester 账号密码          | 中               | 团队共享加密文档    | 开发 + QA    |


### 7.2 RevenueCat Dashboard 权限分配


| 角色     | 权限级别      | 人员                            |
| ------ | --------- | ----------------------------- |
| Owner  | Admin     | 技术负责人                         |
| Member | Edit      | 产品负责人 + iOS/Android Tech Lead |
| Member | Read Only | QA + 客服 + 运营                  |


---

## 8. 风险与注意事项


| #   | 风险                                    | 缓解方案                                 |
| --- | ------------------------------------- | ------------------------------------ |
| R1  | Apple/Google IAP 产品审核延迟 1~3 天         | 配置工作尽量提前 1 周启动                       |
| R2  | Paid Applications Agreement 未签，无法上架商品 | Phase 0 必须先完成财务签约                    |
| R3  | Privacy Policy 未包含 RC 条款，审核被拒         | 法务审稿阶段必须 Review                      |
| R4  | Product ID 命名不规范导致 PRD-2 扩展困难         | 统一命名规范：`<product>_<variant>_<store>` |
| R5  | Webhook Token 泄露                      | 定期轮换，仅存 KMS                          |
| R6  | 多个团队同步成本高，配置进度卡壳                      | 建立每日 Standup，本文档作为共享 Checklist       |


---

## 9. 交付物清单（最终归档）

配置完成后，以下材料应归档并同步至开发团队：

1. 本文档（填写完实际值后的完整版）
2. 所有 Product ID 映射表（Markdown/Confluence）
3. 所有 API Key 与 Secret 的 KMS 引用路径
4. Webhook URL + Token（记录至 RC Dashboard，不外发）
5. Sandbox / License Test 账号密码表（加密分享）
6. RevenueCat Dashboard 访问指南 + 权限分配表
7. Terms of Service + Privacy Policy 最终 URL

---

*文档结束 — 如有疑问请联系技术负责人*