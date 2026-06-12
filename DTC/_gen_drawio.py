"""Generate DTC 5-layer architecture as a draw.io diagram.

Output: /Users/lute/AI/Cursor/DTC/momcozy-dtc-architecture.drawio

设计原则：
- 主架构 5 层 (L1-L5) 与右侧 5 项横切层 1:1 对齐成 5x6 网格
- 每层用「色带 header + 浅色 tint 容器」做色码，5 层一眼分得清
- 模块格收紧到 96px 高，文字间距贴合，无多余留白
"""
from __future__ import annotations
from pathlib import Path
from textwrap import dedent

OUT = Path("/Users/lute/AI/Cursor/DTC/momcozy-dtc-architecture.drawio")

# ---------- 数据 ---------------------------------------------------

STRATEGIES = [
    ("品牌战略", "母婴关怀心智 / 全周期陪伴"),
    ("DTC 占比目标", "一级 OKR / 季度复盘"),
    ("全球化布局", "北美 · 欧洲 · 日韩 · DACH"),
    ("组织模型", "DTC 独立 BU + 中台共享"),
]

# 每层一个色码：主色 + 浅色 tint（用于容器背景）
LAYERS = [
    {
        "code": "L1",
        "name": "流量获取  GTM / Acquisition",
        "goal": "把对的人，用最低 CAC 带到自有阵地",
        "color": "#2563EB",
        "tint":  "#EFF6FF",
        "modules": [
            ("付费投流", ["Meta / Google / TikTok / Pinterest", "信息流 · 搜索 · 购物广告", "再营销 Retargeting"]),
            ("SEO / 内容站", ["关键词矩阵", "母婴长尾内容", "对比 · 评测 · 教程"]),
            ("红人 / 联盟", ["KOL 头部背书", "妈妈 KOC 矩阵", "Affiliate 分销"]),
            ("PR / 品牌", ["奖项 · 媒体公关", "跨界联名", "线下展会 · 母婴展"]),
        ],
    },
    {
        "code": "L2",
        "name": "体验与转化  Experience & Conversion",
        "goal": "在自有阵地把流量转为订单与 ARPU",
        "color": "#7C3AED",
        "tint":  "#F5F3FF",
        "modules": [
            ("独立站 / App", ["Shopify+ · Headless", "App 内购 + 订阅", "多端一致体验"]),
            ("内容 / 落地页", ["场景化 PDP", "视频 · 3D · AR 演示", "对比 · 选购助手"]),
            ("推荐 / 搜索", ["个性化推荐", "智能搜索 + 引导", "购物车挽回"]),
            ("支付 / 履约", ["多币种 · 本地支付", "海外仓 · 极速达", "Klarna · Afterpay 分期"]),
        ],
    },
    {
        "code": "L3",
        "name": "客户服务  Pre & Post-Sales",
        "goal": "用服务体验拉开与平台货的差距",
        "color": "#059669",
        "tint":  "#ECFDF5",
        "modules": [
            ("售前咨询", ["AI 客服 + Live Chat", "母婴专家 1v1", "选购顾问 · 工程师"]),
            ("售后服务", ["RMA 退换货", "保修 · 维修 · 配件", "本地化退仓"]),
            ("客户成功", ["开箱引导", "月龄使用方案", "新生儿陪伴"]),
            ("VOC 反馈", ["NPS / CSAT", "工单语义分析", "差评闭环"]),
        ],
    },
    {
        "code": "L4",
        "name": "营销与触达  Marketing / CRM",
        "goal": "用生命周期提升复购、LTV、唤醒沉睡",
        "color": "#DC2626",
        "tint":  "#FEF2F2",
        "modules": [
            ("生命周期营销", ["Welcome · Onboarding", "Win-back 唤回", "Cross-sell · Upsell"]),
            ("内容营销", ["博客 · 视频 · 教程", "妈妈故事 · UGC", "节日 · 月龄主题"]),
            ("活动促销", ["新品发布 · 闪购", "黑五 · Prime 节奏", "Bundle 套装"]),
            ("个性化沟通", ["EDM · SMS · Push", "标签分层触达", "AI 文案生成"]),
        ],
    },
    {
        "code": "L5",
        "name": "社区与会员增长  Community & Loyalty",
        "goal": "把用户变成共创者与传播者，反哺 DTC",
        "color": "#D97706",
        "tint":  "#FFFBEB",
        "modules": [
            ("品牌社区", ["妈妈论坛 · 群组", "Discord · FB Group", "线下妈妈聚会"]),
            ("UGC 生态", ["创作激励", "晒单 · 评测打卡", "孕产成长日记"]),
            ("会员体系", ["等级 · 积分 · 权益", "生日 · 月龄关怀", "App 端独享"]),
            ("订阅 / 复购", ["耗材订阅 · 自动续订", "周期购 · 套装", "Refer-a-friend"]),
        ],
    },
]

HORIZONTAL = [
    {
        "name": "数据中台 / CDP",
        "role": "为所有层提供统一用户与归因数据",
        "items": ["统一用户 ID", "全渠道归因", "标签 · 客群 · 看板", "AB 实验平台", "用户画像 · 旅程地图"],
        "color": "#0EA5E9",
    },
    {
        "name": "AI / 算法",
        "role": "为获客、转化、服务、复购提供智能能力",
        "items": ["推荐 · 搜索", "AI 客服 · 文案", "选购助手 · 月龄推荐", "智能投放 · 智能定价", "向量搜索 · 多模态"],
        "color": "#8B5CF6",
    },
    {
        "name": "合规 / 支付 / 跨境",
        "role": "跨境业务的合规底座与多支付能力",
        "items": ["GDPR / CCPA", "本地化税务", "退税 · 反欺诈", "多支付通道", "VAT/IOSS · SCA 合规"],
        "color": "#10B981",
    },
    {
        "name": "供应链 / 履约",
        "role": "海外仓、柔性供应、退货逆向的承接",
        "items": ["海外仓布局", "C2M · 柔性供应", "时效与库存", "退货逆向", "新品试销快反"],
        "color": "#F59E0B",
    },
    {
        "name": "组织与人才",
        "role": "DTC 独立 BU + 全球本地团队 + 文化",
        "items": ["DTC 独立 BU", "全球化本地团队", "PM · 增长 · CRM 配比", "数据驱动文化", "OKR · 增长黑客"],
        "color": "#EF4444",
    },
]

# ---------- 布局 ---------------------------------------------------
PAGE_W, PAGE_H = 1700, 1060

MAR = 32

# 主列：4 模块 + 3 gap + 2 内边距
PAD_INNER = 13     # 容器左右内边距
MOD_GAP_X = 10
MOD_W = 281        # (1180 - 2*13 - 3*10) / 4
MAIN_W = MOD_W * 4 + MOD_GAP_X * 3 + PAD_INNER * 2  # 1180
MAIN_X = MAR

# 右列
COL_GAP_X = 20
SIDE_X = MAIN_X + MAIN_W + COL_GAP_X    # 32 + 1180 + 20 = 1232
SIDE_W = PAGE_W - SIDE_X - MAR          # 1700 - 1232 - 32 = 436

# 标题
TITLE_Y, TITLE_H_MAIN, TITLE_H_SUB = 14, 32, 18
TITLE_BLOCK_H = TITLE_H_MAIN + TITLE_H_SUB + 8   # 58

# L0
L0_Y = TITLE_Y + TITLE_BLOCK_H + 16              # 88
L0_HEADER_H = 34
L0_CHIP_H = 46
L0_H = L0_HEADER_H + 6 + L0_CHIP_H + 6           # 92

# 主层 L1-L5
LAYER_HEADER_H = 38
LAYER_GAP_Y_INNER = 6
LAYER_BOT_PAD = 8
MOD_H = 100
LAYER_H = LAYER_HEADER_H + LAYER_GAP_Y_INNER + MOD_H + LAYER_BOT_PAD   # 152
LAYER_GAP = 12
LAYERS_START_Y = L0_Y + L0_H + 16                # 196

# 横切支撑列（与 L0 + 5 层 1:1 对齐）
SIDE_TITLE_Y = L0_Y
SIDE_TITLE_H = L0_H                              # 92
ENABLER_BODY_PAD = 12

# 图脚
LAYERS_END_Y = LAYERS_START_Y + 5 * LAYER_H + 4 * LAYER_GAP  # 196 + 760 + 48 = 1004
LEGEND_Y = LAYERS_END_Y + 14                                  # 1018
LEGEND_H = 30

# ---------- XML 工具 ----------------------------------------------

cells: list[str] = []
_id = 0


def nid(prefix: str = "n") -> str:
    global _id
    _id += 1
    return f"{prefix}{_id}"


def rect(cell_id: str, x: int, y: int, w: int, h: int, value: str, style: str) -> None:
    cells.append(
        f'<mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        f'</mxCell>'
    )


def html_value(html: str) -> str:
    """draw.io expects HTML-as-attr-value: encode &, <, > and quotes."""
    return (html.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def module_html(title: str, items: list[str]) -> str:
    rows = "<br/>".join(f"· {it}" for it in items)
    return html_value(
        f"<div style='font-size:13px;font-weight:600;color:#0F172A;margin-bottom:6px'>{title}</div>"
        f"<div style='font-size:11px;color:#475569;line-height:1.55'>{rows}</div>"
    )


def chip_html(title: str, sub: str) -> str:
    return html_value(
        f"<div style='font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:2px'>{title}</div>"
        f"<div style='font-size:11px;color:#94A3B8'>{sub}</div>"
    )


def enabler_html(name: str, role: str, items: list[str], color: str) -> str:
    rows = "<br/>".join(f"· {it}" for it in items)
    return html_value(
        f"<div style='font-size:13px;font-weight:600;color:{color};margin-bottom:2px'>{name}</div>"
        f"<div style='font-size:10px;font-style:italic;color:#94A3B8;margin-bottom:8px'>{role}</div>"
        f"<div style='font-size:11px;color:#475569;line-height:1.6'>{rows}</div>"
    )


def header_html(code: str, name: str, goal: str) -> str:
    return html_value(
        f"<div style='display:flex;justify-content:space-between'>"
        f"<span style='font-size:14px;font-weight:700;color:#FFFFFF'>"
        f"<span style='background:rgba(255,255,255,0.18);padding:2px 8px;border-radius:4px;margin-right:10px'>{code}</span>"
        f"{name}</span>"
        f"<span style='font-size:11px;font-style:italic;color:#E0E7FF;align-self:center'>{goal}</span>"
        f"</div>"
    )


def side_title_html() -> str:
    return html_value(
        f"<div style='font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:6px'>横切支撑层  Horizontal Enablers</div>"
        f"<div style='font-size:11px;color:#94A3B8;line-height:1.55'>"
        f"贯穿所有 5 层主架构的中台能力<br/>缺一层则对应业务层成「孤岛」</div>"
    )


def l0_header_html() -> str:
    return html_value(
        f"<span style='font-size:14px;font-weight:700;color:#FFFFFF'>"
        f"<span style='background:rgba(255,255,255,0.18);padding:2px 8px;border-radius:4px;margin-right:10px'>L0</span>"
        f"战略与组织  Strategy &amp; Organization</span>"
    )


# ---------- 样式预设 ----------------------------------------------
STYLE_PLAIN = "rounded=1;whiteSpace=wrap;html=1;arcSize=4;fillColor=#FFFFFF;strokeColor=none;"

STYLE_TITLE = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=22;fontStyle=1;fontColor=#0F172A;"
STYLE_SUBTITLE = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=12;fontStyle=2;fontColor=#64748B;"

STYLE_LAYER_CONTAINER = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=4;fillColor={tint};strokeColor={stroke};strokeWidth=1;"
)
STYLE_LAYER_HEADER = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=4;fillColor={fill};strokeColor={fill};"
    "fontColor=#FFFFFF;align=left;verticalAlign=middle;spacingLeft=14;spacingRight=14;"
)

STYLE_MODULE = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=3;fillColor=#FFFFFF;strokeColor=#E2E8F0;strokeWidth=1;"
    "align=left;verticalAlign=top;spacingLeft=11;spacingRight=11;spacingTop=9;spacingBottom=9;"
)

STYLE_L0_CONTAINER = "rounded=1;whiteSpace=wrap;html=1;arcSize=4;fillColor=#0F172A;strokeColor=#0F172A;"
STYLE_L0_HEADER = (
    "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=14;"
)
STYLE_L0_CHIP = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=6;fillColor=#1E293B;strokeColor=#334155;strokeWidth=1;"
    "align=left;verticalAlign=middle;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;"
)

STYLE_SIDE_TITLE = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=4;fillColor=#0F172A;strokeColor=#0F172A;"
    "align=left;verticalAlign=middle;spacingLeft=16;spacingRight=14;spacingTop=14;spacingBottom=14;"
)
STYLE_ENABLER = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize=4;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=2;"
    "align=left;verticalAlign=top;spacingLeft=14;spacingRight=12;spacingTop=12;spacingBottom=12;"
)

# ---------- 渲染：标题 -------------------------------------------
rect(nid("t"), MAR, TITLE_Y, PAGE_W - 2 * MAR, TITLE_H_MAIN,
     "全球 DTC 业务核心架构图  ·  Momcozy 重构参考",
     STYLE_TITLE)
rect(nid("t"), MAR, TITLE_Y + TITLE_H_MAIN + 4, PAGE_W - 2 * MAR, TITLE_H_SUB,
     "5 层主架构 + 5 项横切支撑层 · 对标 DJI / Bambu Lab · 2026-05",
     STYLE_SUBTITLE)

# ---------- 渲染：L0 战略层 -------------------------------------
rect(nid("L0c"), MAIN_X, L0_Y, MAIN_W, L0_H, "", STYLE_L0_CONTAINER)
rect(nid("L0h"), MAIN_X, L0_Y, MAIN_W, L0_HEADER_H,
     l0_header_html(), STYLE_L0_HEADER)

chip_y = L0_Y + L0_HEADER_H + 6
chip_w = MOD_W
for i, (title, sub) in enumerate(STRATEGIES):
    cx = MAIN_X + PAD_INNER + i * (chip_w + MOD_GAP_X)
    rect(nid("L0i"), cx, chip_y, chip_w, L0_CHIP_H,
         chip_html(title, sub), STYLE_L0_CHIP)

# ---------- 渲染：L1-L5 ------------------------------------------
for li, layer in enumerate(LAYERS):
    ly = LAYERS_START_Y + li * (LAYER_H + LAYER_GAP)
    # 容器（浅色 tint）
    rect(nid("Lc"), MAIN_X, ly, MAIN_W, LAYER_H, "",
         STYLE_LAYER_CONTAINER.format(tint=layer["tint"], stroke=layer["color"]))
    # 色带 header（code 徽标 + 名称 + 右侧 italic 目标）
    rect(nid("Lh"), MAIN_X, ly, MAIN_W, LAYER_HEADER_H,
         header_html(layer["code"], layer["name"], layer["goal"]),
         STYLE_LAYER_HEADER.format(fill=layer["color"]))
    # 4 个模块
    my = ly + LAYER_HEADER_H + LAYER_GAP_Y_INNER
    for mi, (mtitle, mitems) in enumerate(layer["modules"]):
        mx = MAIN_X + PAD_INNER + mi * (MOD_W + MOD_GAP_X)
        rect(nid("Lm"), mx, my, MOD_W, MOD_H,
             module_html(mtitle, mitems), STYLE_MODULE)

# ---------- 渲染：横切支撑列 -------------------------------------
rect(nid("St"), SIDE_X, SIDE_TITLE_Y, SIDE_W, SIDE_TITLE_H,
     side_title_html(), STYLE_SIDE_TITLE)

for i, e in enumerate(HORIZONTAL):
    by = LAYERS_START_Y + i * (LAYER_H + LAYER_GAP)
    rect(nid("Se"), SIDE_X, by, SIDE_W, LAYER_H,
         enabler_html(e["name"], e["role"], e["items"], e["color"]),
         STYLE_ENABLER.format(stroke=e["color"]))

# ---------- 渲染：图脚 -------------------------------------------
rect(nid("ln"), MAR, LEGEND_Y, PAGE_W - 2 * MAR, LEGEND_H,
     html_value(
         "<span style='font-size:11px;color:#475569'>"
         "<b>读图：</b>纵向 5 层 = 用户旅程主链路（自上而下：战略 → 流量 → 转化 → 服务 → 营销 → 社区）；"
         "右侧 5 项 = 贯穿所有层的横切中台能力，缺一项则对应业务层会变成「孤岛」。"
         "</span><br/>"
         "<span style='font-size:10px;font-style:italic;color:#94A3B8'>"
         "v1.1 · 2026-05-11 · 配套：dtc-architecture-framework.canvas.tsx · momcozy-商业化2026规划-完整版.md"
         "</span>"
     ),
     "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;")

# ---------- 输出 ---------------------------------------------------
xml = dedent(f"""\
<mxfile host="65bd71144e" agent="Cursor Agent">
    <diagram id="dtc-5-layer" name="DTC 5层架构 + 横切支撑">
        <mxGraphModel dx="{PAGE_W}" dy="{PAGE_H}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
""")
xml += "\n".join("                " + c for c in cells)
xml += dedent("""
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
""")

OUT.write_text(xml, encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  size: {len(xml):,} bytes, cells: {len(cells)}")
print(f"  page: {PAGE_W} x {PAGE_H}")
print(f"  main col: x={MAIN_X} w={MAIN_W}, side col: x={SIDE_X} w={SIDE_W}")
print(f"  layer h={LAYER_H}, module={MOD_W}x{MOD_H}, last layer ends y={LAYERS_END_Y}")
