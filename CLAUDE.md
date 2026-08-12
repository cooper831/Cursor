# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 项目概览

这是一个 **产品原型 + PM 工具库** 项目，用于支持产品经理的商业化决策和原型设计工作。

| 维度 | 说明 |
|------|------|
| **主要产出** | 交互式原型（HTML/React）、PM 评估工具、商业化规划文档 |
| **目标用户** | 电商 PM、增值服务 PM、产品团队 |
| **技术栈** | HTML5 + CSS3 / React + TypeScript（可选）/ 纯文档（Markdown） |
| **协作方式** | 原型评审、面试工具、竞品分析、商业计划迭代 |

---

## 目录结构

```
/Users/lute/AI/Cursor/
├── PM面试评估手册.md                    # 电商/增值服务 PM 招聘评估系统（60 min 结构化面试）
├── index.html                          # 项目主入口（原型导航）
├── momcozy-*.html                      # Momcozy App 各场景原型（仪表板、推荐、投票等）
├── scene-detail.html                   # 细节页面原型
├── docs/                               # 产品文档库（需求、流程、数据字典）
├── Competitive product research/       # 竞品分析报告
├── commercialization planning/         # 商业化规划（定价、渠道、运营）
├── Skill production/                   # Skill 工程化文档（Prompt 工程、评估标准）
├── momcozy-app-scene-prototype/        # React 原型项目（组件化方案）
├── recommendations/                    # 推荐算法决策文档
└── promo-cards/                        # 促销卡片设计素材
```

---

## 工作流与任务类型

### 1. 原型开发（最常见）

**场景**：基于 PRD 生成交互原型，评审 → 迭代。

**输入形式**：Markdown PRD 或截图  
**输出格式**：HTML 原型或 React 组件  
**关键要求**：
- 三栏布局（左侧导航 / 中央预览 / 右侧文档）
- 页面间跳转导航栈
- 状态标签（设计中 / 评审中 / 已确认）
- 支持缩放（50% / 75% / 100% / 125%）

**参考资源**：见下方"原型制作指南"章节

---

### 2. PM 面试与评估

**场景**：招聘或内部评估产品经理能力。

**核心文件**：`PM面试评估手册.md`
- **EC PM**（电商）：25% 专业深度 + 20% 技术协同 + 15% 数据 & 监控
- **VAS PM**（增值服务）：偏向商业设计 + 合规灵活度
- **评分维度**：7 维能力模型，每维 1-5 分

**使用方式**：
- 60 分钟结构化面试框架（STAR 法 + 场景模拟）
- 按候选人方向（EC / VAS）深挖垂直能力
- 重点追问：决策逻辑、跨部门协作、风险感知

---

### 3. 商业化分析

**典型任务**：
- 竞品分析（`Competitive product research/`）
- 定价 / 渠道 / 运营策略（`commercialization planning/`）
- 推荐算法设计（`recommendations/`）

**输出格式**：Markdown 文档或 Excel 对标表

---

## 原型制作指南

当你接到"请基于 PRD 生成原型"的任务时，遵循以下流程：

### Step 1: 分析 PRD 文档

提取关键信息：
- **产品形态**：移动 App（375×812）/ 桌面 Web（1440×900）/ 小程序（375×667）
- **页面清单**：名称、功能、关键字段、跳转关系
- **设计规范**：配色、字号、圆角、组件风格

### Step 2: 补全缺失信息

若 PRD 中无指定，使用默认值（注释标注 `[AI 补全]`）：

```css
--background: #F8FAFC
--foreground: #1E293B
--primary: #2563EB
--accent: #F97316
--border: #E2E8F0
--muted: #64748B
```

### Step 3: 构建页面数据结构

```typescript
interface IPageItem {
  id: string;                    // 'login', 'home', 等
  name: string;                  // "登录页"
  path: string;                  // '/login'
  type: 'page' | 'modal' | 'flow';
  status: 'designing' | 'reviewing' | 'confirmed';
  isHome?: boolean;              // 标记首页
  prototype: React.FC;           // 原型组件
  prdContent: string;            // PRD Markdown
  notes?: string;                // [AI 补全] 标注
}
```

### Step 4: 实现原型组件

**必须满足**：
- 容器尺寸严格 1:1（375×812 for 移动端）
- 所有按钮/列表可点击 → 触发 `onNavigate(pageId)`
- 返回按钮基于导航栈 → `onBack()`
- 未定义页面 → Toast 提示，不白屏

**微交互**：`cursor-pointer` + `hover:bg-primary/5` + `transition-all duration-200`

### Step 5: 组装三栏布局

| 栏位 | 宽度 | 功能 |
|-----|------|------|
| 左栏 | 240px | 页面清单 + 流程图切换 + 状态标签 |
| 中栏 | flex-1 | 原型预览 + 缩放 + 设备外壳 |
| 右栏 | 420px（可拖拽） | PRD 文档 + 评论 Tab |

### Step 6: 输出单文件

生成 `PrototypeReviewPage.tsx`，包含：
- 所有页面原型组件
- `pageData` 数组
- 三栏布局主组件
- 辅助组件（Toast、缩放、Markdown 渲染等）

---

## 代码规范

### 文件组织

- 优先编辑已有文件，避免创建新文件
- 原型放在 `momcozy-*` 命名的文件夹或 `.html` 文件
- 文档（需求/设计方案）放在 `docs/` 下

### 技术选择

| 场景 | 推荐方案 |
|------|--------|
| 快速原型（< 5 页） | 纯 HTML + Tailwind CDN |
| 中等规模（5-15 页） | React + TypeScript + Tailwind |
| 复杂交互（嵌套流程、动画） | React + Framer Motion + 组件库 |

### CSS 规范

```css
/* 使用 CSS 变量统一配色 */
background-color: var(--background);
color: var(--foreground);
border-color: var(--border);
```

### 组件库

- **图标**：`lucide-react`（16/20/24 默认尺寸）
- **Markdown**：`react-markdown` + `remark-gfm`（支持表格、任务列表）
- **无需**：react-flow（简单 SVG 连线即可）

---

## 常见任务命令

### Vercel 文档发布（默认）

仓库内生成的 **`.md` / `.html` 文档**会在 push 后由 Vercel 自动构建并发布（需先在 Vercel 绑定 GitHub 仓库）。

| 操作 | 命令 / 链接 |
|------|-------------|
| 本地构建 | `npm run build:vercel` |
| 本地预览 | `npm run preview:vercel` → 打开 `http://localhost:3456/` |
| 站点目录 | `https://<project>.vercel.app/` |
| Markdown 阅读 | `https://<project>.vercel.app/read/docs/xxx.md` |
| HTML 直链 | `https://<project>.vercel.app/docs/xxx.html` |
| 链接清单 | 构建产物 `public/_site/LINKS.md`、`manifest.json` |

**自动收录范围**：`docs/`、`Skill production/`、`html/`、`commercialization planning/`、`Competitive product research/`、`全球市场母婴付费订阅调研/`、`DTC/` 及根目录下的 `.md` / `.html`。

**不收录**：交互原型目录（`momcozy-app-scene-prototype/` 等）、`CLAUDE.md`、根目录 `index.html`。

**AI 生成文档时**：优先输出到上述目录；push 后即自动上线，无需手工维护链接列表。

### 启动本地原型预览

```bash
# 如果是纯 HTML，用任意 HTTP 服务
python -m http.server 8000

# 或用 VSCode Live Server 扩展
```

### 验证原型完整性

- [ ] 所有页面渲染无错
- [ ] 导航跳转正确，未定义页面有 Toast 兜底
- [ ] 返回按钮按导航栈正确出栈
- [ ] 缩放 4 档位（50% / 75% / 100% / 125%）正常
- [ ] 右栏 PRD Tab 的 Markdown 表格、任务列表渲染正确
- [ ] 左右栏可折叠，右栏可拖拽宽度 320–600px
- [ ] URL 与 `currentPageId` 双向同步

### 更新原型文件

```bash
# 修改后立即刷新浏览器
# 或配置 VSCode 文件监听 + 自动重载
```

---

## 评审流程

### 左栏导航与状态

- **当前选中项**：左侧 3px 主色色条 + `bg-primary/8` 背景
- **状态圆点**：
  - 灰色 `designing`（设计中）
  - 黄色 `reviewing`（评审中）
  - 绿色 `confirmed`（已确认）
- **流程子节点**：缩进 16px 显示

### 流程图视图

点击左栏"流程图"按钮切换到可视化流程，显示：
- 各页面节点 + 跳转箭头
- 点击节点直接切换 `currentPageId`

### 右栏评论

在当前页面下添加文字评论（本地 state 即可），支持：
- 页面级别的反馈
- Markdown 格式

---

## 设计决策参考

### 为什么是三栏布局？

- **左栏**：快速定位页面，评审时可一览全景
- **中栏**：完整还原原型，尺寸 1:1、交互完善
- **右栏**：PRD 与评论并行，即时反馈

### 为什么需要导航栈？

- 还原真实 App 的返回行为
- 支持评审时"跳转播放"的完整叙事链路
- URL 同步便于分享和恢复

### 关于"[AI 补全]"标注

- 表示 PRD 中未指定、由 AI 合理推断的内容
- 方便产品经理快速识别需要确认的决策点

---

## 关键决策原则

| 原则 | 说明 |
|------|------|
| **真实比例** | 原型尺寸严格 1:1 对标目标设备 |
| **可交互** | 每个按钮、列表、Tab 都能点击跳转 |
| **评审导向** | 状态、评论、流程图服务于评审，非展示 |
| **文档对齐** | 右栏 PRD 与中栏原型严格对应当前页 |
| **容错设计** | 未定义页面不白屏，用 Toast 提示 |
| **可恢复** | URL 同步保证刷新 / 分享时状态不丢 |

---

## 有用的资源

- **PM 评估**：见 `PM面试评估手册.md` 中的 7 维能力模型
- **竞品分析**：`Competitive product research/` 下的对标模板
- **商业化规划**：`commercialization planning/` 中的定价 / 渠道决策
- **Skill 工程化**：`Skill production/` 下的 Prompt 工程标准

---

## 问题排查

### 原型页面白屏

- 检查 `pageData` 中是否有对应的 `id`
- 确认组件的 `prototype` 是否正确导出
- 查看浏览器控制台 for 错误

### 导航卡死

- 确认 `onNavigate` 和 `onBack` 正确更新 `navStack`
- 确认首页 (`isHome: true`) 被正确标记

### 右栏 Markdown 渲染异常

- 确认 `remark-gfm` 已安装
- 检查 `prdContent` 是否为有效 Markdown

### 样式显示不对

- 确认 Tailwind CSS 已正确引入（CDN 或 build）
- 检查 CSS 变量 `--primary`, `--background` 等是否定义

---

**最后更新**：2026-05-09
