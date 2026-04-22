# Momcozy App — 场景入口与场景详情（线框 / 可配置方案）PRD


| 项目     | 说明                                          |
| ------ | ------------------------------------------- |
| 文档版本   | v1.0                                        |
| 对应代码目录 | `momcozy-app-scene-prototype/`              |
| 状态     | 静态原型；**与 Shopify 独立站 / 中台未打通**，价格、集合、加购均为占位 |


---

## 1. 背景与目标

### 1.1 背景

App 在特定用户旅程（如孕期、哺乳、产后恢复等）完成后，在首页 Feed 以**横向滑动场景卡片**露出「Cozy × 场景」心智；用户进入**原生场景详情页**，阅读品牌叙事并浏览按主题分组的商品推荐，最终可跳转至 DTC 集合页（当前为演示）。

### 1.2 目标

- 统一五套场景（Pregnancy / Feeding / Recovery / Outing / Parenting）的**入口展示**与**详情页结构**。
- 将详情页所有可展示内容**字段化**，便于后续由 **CMS / 配置服务 / JSON** 驱动，而非写死在 HTML 中。
- 明确与 **Momcozy.com（独立站）** 打通前的占位行为与打通后的接口契约。

### 1.3 非目标（当前版本）

- 真实登录、个性化推荐算法、A/B 实验平台接入。
- 与 Shopify Storefront API / Cart / Checkout 的联调（仅预留 URL 与交互占位）。
- 多语言发布管线（文案可为英文；字段设计支持未来 `locale`）。

---

## 2. 范围：页面清单


| 页面   | 文件                  | 说明                              |
| ---- | ------------------- | ------------------------------- |
| 场景入口 | `index.html`        | 横向 scroll-snap 卡片列表，点击进入详情      |
| 场景详情 | `scene-detail.html` | 查询参数 `?scene=<slug>` 切换场景；客户端渲染 |
| 全局样式 | `wireframe.css`     | 排版、玻璃拟态、轮播与 Hero 裁切等            |
| 静态资源 | `assets/*.png`      | 各场景 Hero / 卡片用图                 |


设计预览用顶部场景切换：`scene-detail.html` 内 `nav.wf-scene-switch`（生产可隐藏或仅限内测）。

---

## 3. 与独立站「未打通」时的行为说明


| 能力                  | 当前行为                                                       | 打通后预期                                    |
| ------------------- | ---------------------------------------------------------- | ---------------------------------------- |
| 商品价格                | 静态展示字符串（如 `$89.99`）                                        | 由商品中心 / Storefront 返回展示价（含币种、划线价）        |
| 商品主图                | 卡片内占位块「Image」或线框说明                                         | `imageUrl` + CDN 多尺寸                     |
| 「Learn more」        | `alert` 演示 PDP 跳转                                          | 打开 App 内 WebView 或 Universal Link 至 PDP  |
| 底部「Go to the store」 | `alert` + 拼接 `https://momcozy.com/collections/{storePath}` | 同一 URL 规则，由配置下发；可增加 UTM / 归因参数           |
| `collection` 字段     | 占位锚点如 `#p-pillow`                                          | Shopify Collection GID / handle 或内部类目 ID |


PRD 要求：**所有面向用户的字符串与 URL 规则均可配置**，代码中仅保留默认值或 fallback。

---

## 4. 场景详情页 — 全字段配置规格

以下为一组**场景（Scene）**的完整数据模型，与当前 `scene-detail.html` 内 `SCENES` 对象一致；实施时可映射为 CMS Collection、单条 JSON 或数据库行 + 子表。

### 4.1 场景根对象 `Scene`


| 字段              | 类型               | 必填  | 说明                                                                      | 当前示例                                                      |
| --------------- | ---------------- | --- | ----------------------------------------------------------------------- | --------------------------------------------------------- |
| `id`            | string (slug)    | 是   | URL 与逻辑主键，建议小写、无空格                                                      | `pregnancy`, `feeding`, `recovery`, `outing`, `parenting` |
| `name`          | string           | 是   | 详情页 Hero 区主标题（品牌场景名）                                                    | `Cozy Pregnancy`                                          |
| `accent`        | string (hex)     | 是   | 主强调色，用于左边框、按钮描边、部分 UI                                                   | `#8b7cb5`                                                 |
| `accentSoft`    | string (hex)     | 是   | 浅强调色；详情页整屏背景渐变上段与中段（与 `accent` 一并由 CSS 使用）                              | `#ede9f5`                                                 |
| `keywords`      | string[]         | 是   | Hero 下标签列表；建议 3 条，每条短词组                                                 | `["Smooth transition", "Ease", "Relax"]`                  |
| `manifesto`     | string (长文本)     | 是   | 「Brand manifesto」区块正文；支持换行由 CMS 控制                                      | 见代码内各场景                                                   |
| `storePath`     | string           | 是   | **独立站集合路径片段**（不含域名）；打通后用于 `https://momcozy.com/collections/{storePath}` | `cozy-pregnancy`                                          |
| `productGroups` | `ProductGroup[]` | 是   | 商品分组列表；见 4.3                                                            | 多组，每组 4 个 SKU 卡片                                          |


**Hero 大图（与 `id` 绑定，当前为前端映射表）**

当前实现为 `heroPhotoMap[id]`，等价于下列配置（建议并入 `Scene` 或独立 `sceneHeroAssets` 配置）：


| 字段                   | 类型                 | 必填  | 说明                                                                  |
| -------------------- | ------------------ | --- | ------------------------------------------------------------------- |
| `heroImageUrl`       | string (URL 或相对路径) | 否   | 若空则显示灰色占位 Hero                                                      |
| `heroImageCropClass` | string             | 否   | 可选 CSS 修饰类，用于 `object-position` 微调（如 `wf-hero-ph--scene-pregnancy`） |


当前各场景资源路径（相对 `scene-detail.html`）：


| `id`      | `heroImageUrl`                            | `heroImageCropClass`（详情 Hero） |
| --------- | ----------------------------------------- | ----------------------------- |
| pregnancy | `assets/hero-cozy-pregnancy-scene.png`    | `wf-hero-ph--scene-pregnancy` |
| feeding   | `assets/hero-cozy-feeding-feed-scene.png` | （无额外类）                        |
| recovery  | `assets/hero-cozy-recovery-scene.png`     | `wf-hero-ph--scene-recovery`  |
| outing    | `assets/hero-cozy-outing-scene.png`       | `wf-hero-ph--scene-outing`    |
| parenting | `assets/hero-cozy-parenting-scene.png`    | `wf-hero-ph--scene-parenting` |


### 4.2 详情页固定模块（非 `Scene` 内逐条配置，但可复制/开关建议）


| 模块                 | 配置建议                                           | 当前行为                                 |
| ------------------ | ---------------------------------------------- | ------------------------------------ |
| Hero 模块            | 绑定 `heroImageUrl` + `name` + `keywords`        | 有图则照片 Hero，否则占位灰块                    |
| Brand manifesto    | 标题文案可 i18n key：`detail.manifesto.title`        | 固定英文标题「Brand manifesto」              |
| 商品编辑区 `aria-label` | 可配置无障碍名称                                       | 固定为「Product edit」                    |
| Load more          | 首屏组数、每次加载组数                                    | 首屏 1 组；每点击追加 1 组；仅 1 组时隐藏按钮并显示 `end` |
| 全局 CTA 主文案         | 模板字符串：`Go to the store — {name} full range >>` | 与 `name` 拼接；样式为黑底白字全宽按钮              |
| 设计导航               | 是否显示 `wf-scene-switch`                         | 仅原型；生产建议 `false`                     |


### 4.3 商品分组 `ProductGroup`


| 字段      | 类型              | 必填  | 说明                                                  |
| ------- | --------------- | --- | --------------------------------------------------- |
| `title` | string          | 是   | 分组小标题（每组上方展示）                                       |
| `items` | `ProductCard[]` | 是   | **当前线框约束：每组恰好 4 条**（便于 2×2 栅格）；产品化时可放宽为 1–n，需前端布局策略 |


### 4.4 商品卡片 `ProductCard`


| 字段           | 类型     | 必填  | 说明                                                                               |
| ------------ | ------ | --- | -------------------------------------------------------------------------------- |
| `name`       | string | 是   | 商品名                                                                              |
| `line`       | string | 是   | 一行短描述（副标题）                                                                       |
| `price`      | string | 是   | **展示用**价格字符串；未打通前不校验格式；打通后建议拆为 `amountMinor` + `currency` + `displayPrice`       |
| `collection` | string | 否   | 当前为占位（`#` 锚点）；打通后可为 **Shopify collection handle** 或 **product handle** / **GID** |


**卡片 CTA**

- 文案：当前固定为「Learn more →」（弱 CTA，下划线文字按钮风格）。
- 行为：占位 `alert`；打通后：`deepLink` 或 `productUrl` 字段优先。

建议在 `ProductCard` 上扩展（PRD 预留，代码可后续加）：


| 字段              | 类型     | 说明                                             |
| --------------- | ------ | ---------------------------------------------- |
| `productHandle` | string | Shopify product handle，用于 `/products/{handle}` |
| `variantId`     | string | 默认变体，加购用                                       |
| `sku`           | string | ERP / 运营对账                                     |
| `imageUrl`      | string | 替换卡片内「Image」占位块                                |


### 4.5 JSON 配置示例（单场景节选）

```json
{
  "id": "feeding",
  "name": "Cozy Feeding",
  "accent": "#c45c4a",
  "accentSoft": "#fbeae7",
  "keywords": ["Efficiency", "Freedom", "Simplify"],
  "manifesto": "Feeding is a full-time rhythm...",
  "storePath": "cozy-feeding",
  "heroImageUrl": "assets/hero-cozy-feeding-feed-scene.png",
  "heroImageCropClass": "",
  "productGroups": [
    {
      "title": "Wearable pumping",
      "items": [
        {
          "name": "Hands-Free Wearable Pump",
          "line": "Quiet sessions under a loose tee.",
          "price": "$299.99",
          "collection": "#f-pump",
          "productHandle": null,
          "imageUrl": null
        }
      ]
    }
  ]
}
```

---

## 5. 场景入口页（Index）— 字段与配置说明

每条入口卡片对应一个 `Scene.id`，但**入口专用文案与详情 `name` 可不同**（当前为独立维护在 HTML 中）。建议 CMS 结构：

### 5.1 `FeedSceneCard`（入口卡片）


| 字段                   | 类型           | 必填  | 说明                                                 |
| -------------------- | ------------ | --- | -------------------------------------------------- |
| `sceneId`            | string       | 是   | 与详情 `Scene.id` 一致                                  |
| `href`               | string       | 是   | 默认 `scene-detail.html?scene={sceneId}`；App 内可为原生路由 |
| `cardImageUrl`       | string       | 否   | 与详情 Hero 可同图或独立 4:3 裁切图                            |
| `cardImageCropClass` | string       | 否   | 如 `wf-ph--scene-pregnancy`，对应 `wireframe.css`      |
| `kicker`             | string       | 是   | 小标签，如 `Cozy Pregnancy`                             |
| `kickerAccent`       | string (hex) | 是   | 内联强调色，与 `Scene.accent` 建议同源配置                      |
| `title`              | string       | 是   | 卡片主标题                                              |
| `description`        | string       | 是   | 副文案                                                |
| `ctaLabel`           | string       | 否   | 如 `Start soft →`；纯展示，点击整卡进详情                       |


> 说明：当前入口页**不展示**「Trigger: …」类 pill 标签；若运营后续需要，可再启用独立字段或 metafield。

**顺序**：由 Feed 配置数组顺序决定；当前为固定 5 张卡片顺序。

---

## 6. 前端技术说明

### 6.1 技术栈

- 纯静态 **HTML + CSS + 原生 JavaScript**（无构建工具、无框架）。
- 字体：**Google Fonts**（Playfair Display + DM Sans），需外网或自建字体镜像。

### 6.2 路由与参数

- 详情页：`scene-detail.html?scene=<slug>`。
- 非法 `slug`：渲染错误提示区块（未知场景 + 合法枚举提示）。

### 6.3 运行时行为

1. 读取 `scene` 查询参数 → 查 `SCENES[id]`。
2. 写入 CSS 变量 `--accent`、`--accent-soft` 至 `document.documentElement`。
3. 拼接 Hero、Manifesto、商品区 DOM；`setupLoadMore` 绑定首组与按钮。
4. 商品卡片点击委托：`.wf-ess-buy` → 占位弹窗。
5. 全局 CTA：`#global-cta` → 占位弹窗（含 collections URL 文案）。

### 6.4 关键 DOM / ID（勿随意改名，以免破坏脚本）


| ID / 选择器        | 用途           |
| --------------- | ------------ |
| `#detail-root`  | 详情主挂载点       |
| `#ess-section`  | 商品区块 section |
| `#groups-mount` | 分组卡片插入点      |
| `#wf-load-more` | Load more 按钮 |
| `#wf-load-end`  | 全部加载完显示「end」 |
| `#global-cta`   | 跳转独立站集合（占位）  |


### 6.5 样式与裁切类名

- 全局：`wireframe.css`。
- 场景 Hero / 卡片缩略图裁切：`.wf-hero-ph--scene-`*、`.wf-ph--scene-*` 内 `object-position` 可按场景调参。

---

## 7. 后端与配置服务说明（当前与目标）

### 7.1 当前（原型阶段）

- **无后端**：数据在 `scene-detail.html` 的 `SCENES` 字面量中；入口文案在 `index.html`。
- 部署：任意静态文件托管（S3 + CloudFront、GitHub Pages、Nginx、`python3 -m http.server` 等）。

### 7.2 推荐演进


| 阶段      | 做法                                                                                                  |
| ------- | --------------------------------------------------------------------------------------------------- |
| Phase A | 将 `SCENES` 抽为 `scenes.json`，构建或运行时 `fetch`（需解决 CORS 与路径）                                            |
| Phase B | Headless CMS（Contentful / Sanity / Strapi）建模：`Scene`、`ProductGroup`、`ProductCard`；发布 Webhook 刷新 CDN |
| Phase C | 后端 BFF：`GET /api/v1/scenes/{id}` 聚合 CMS + Shopify Storefront（库存、价、图）                                |


### 7.3 BFF 响应示例（打通独立站后）

```json
{
  "scene": { "id": "feeding", "name": "Cozy Feeding", "accent": "#c45c4a", "...": "..." },
  "hero": { "imageUrl": "https://cdn.../feeding.jpg" },
  "productGroups": [
    {
      "title": "Wearable pumping",
      "items": [
        {
          "name": "Hands-Free Wearable Pump",
          "line": "Quiet sessions under a loose tee.",
          "displayPrice": "$299.99",
          "currencyCode": "USD",
          "productHandle": "hands-free-wearable-pump",
          "productUrl": "https://momcozy.com/products/hands-free-wearable-pump",
          "imageUrl": "https://cdn.../pump.jpg"
        }
      ]
    }
  ],
  "store": {
    "collectionUrl": "https://momcozy.com/collections/cozy-feeding",
    "collectionHandle": "cozy-feeding"
  }
}
```

**校验规则建议**

- `keywords.length`：建议 3，允许 2–5；超出则折叠或横向滚动（需设计）。
- `productGroups[].items.length`：当前前端假设 4；若变更需改栅格与 `setupLoadMore` 逻辑。
- `accent` / `accentSoft`：hex 正则校验，防止 XSS 注入 style。

---

## 8. 配置与运维说明

### 8.1 本地预览

在目录 `momcozy-app-scene-prototype` 下执行：

```bash
./serve.sh
```

- 默认从 **8765** 起查找空闲端口；亦可 `./serve.sh 8800` 指定端口。
- 浏览器访问终端打印的 `http://127.0.0.1:<PORT>/index.html`。

**注意**：勿将仓库上一级目录作为网站根目录打开，否则 `assets/`、`wireframe.css` 相对路径会 404。

### 8.2 静态资源

- 路径：相对 HTML 的 `assets/`。
- 新场景图：命名建议 `hero-cozy-{scene}-scene.png`，并在 `heroPhotoMap`（或未来 JSON）与入口 `index.html` 同步引用。

### 8.3 环境变量（未来 App 壳内嵌 H5）


| 变量                   | 说明                            |
| -------------------- | ----------------------------- |
| `MOMCOZY_WEB_ORIGIN` | 独立站域名，如 `https://momcozy.com` |
| `MOMCOZY_UTM_SOURCE` | 从 App 出站跳转统一 UTM              |


---

## 9. 无障碍与合规注意点

- Hero 图当前 `alt` 为空；生产应配置 **场景描述 alt** 或 `aria-labelledby` 指向标题。
- 场景切换导航：键盘焦点顺序与 `aria-current="page"` 建议补齐。
- 价格与促销：打通后需符合各司法辖区展示规则（含税、划线价依据等）。

---

## 10. 验收标准（本 PRD 对应原型）

- 五场景入口卡片均可进入对应详情且 Hero、色板、文案正确。
- 详情页每组商品为 **4 卡片栅格**；多组时 **Load more** 逐组加载，最后一组后出现 **end**。
- 商品弱 CTA「Learn more →」可点击并触发占位逻辑（或已替换为真实路由）。
- 全局 CTA 拼接 `storePath` 与独立站集合 URL 规则正确（打通前可为弹窗确认文案）。
- `./serve.sh` 在端口占用时可自动递增或手动指定成功启动。

---

## 11. 文档维护

- 代码变更 `SCENES` / `heroPhotoMap` / 入口 HTML 时，**同步更新本 PRD 表格与 JSON 示例**。
- 与 Shopify 打通后，新增一节「Storefront 字段映射表（GraphQL 字段 ↔ ProductCard）」。

---

*本文档基于仓库内 `momcozy-app-scene-prototype` 当前实现整理。*