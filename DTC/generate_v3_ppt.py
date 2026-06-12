#!/usr/bin/env python3
"""
Momcozy DTC 三大痛点解决方案 · v3 —— PPT 生成脚本（原生可编辑）

收敛 v2 范围至三大痛点：用户体验 / 数据打通 / 内容社区
解决方案：3 个中台（用户资产 / 内容 / 增长）+ 1 个独立站×APP 联合工作组
APP 生态能力作为"证明"贯穿始终

- 16:9 画布
- 全部原生 shape，可在 Keynote / PPT 内直接编辑
- 输出：/Users/lute/AI/Cursor/DTC/DTC大部门战略提案_v3.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ====================== 配色（深绿主色 · 与用户上传图一致） ======================
C_GREEN_D   = RGBColor(0x1F, 0x4E, 0x2C)
C_GREEN     = RGBColor(0x2E, 0x7D, 0x32)
C_GREEN_M   = RGBColor(0x66, 0xBB, 0x6A)
C_GREEN_LT  = RGBColor(0xE8, 0xF5, 0xE9)
C_GREEN_LL  = RGBColor(0xF1, 0xF8, 0xE9)
C_RED       = RGBColor(0xC0, 0x3A, 0x2B)
C_RED_LT    = RGBColor(0xFB, 0xE5, 0xE1)
C_ORANGE    = RGBColor(0xE6, 0x7E, 0x22)
C_ORANGE_LT = RGBColor(0xFD, 0xEB, 0xD0)
C_BLUE      = RGBColor(0x1F, 0x4E, 0x79)
C_BLUE_LT   = RGBColor(0xDE, 0xEB, 0xF7)
C_PURPLE    = RGBColor(0x5B, 0x2E, 0x8A)
C_PURPLE_LT = RGBColor(0xE8, 0xDE, 0xF0)
C_DARK      = RGBColor(0x1A, 0x1A, 0x1A)
C_GRAY_D    = RGBColor(0x33, 0x33, 0x33)
C_GRAY      = RGBColor(0x66, 0x66, 0x66)
C_GRAY_LT   = RGBColor(0xF2, 0xF2, 0xF2)
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "PingFang SC"
OUT_PATH = "/Users/lute/AI/Cursor/DTC/DTC大部门战略提案_v3.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL_PAGES = 13

# ====================== 通用辅助函数 ======================
def new_slide(bg=C_WHITE):
    s = prs.slides.add_slide(BLANK)
    b = s.background; b.fill.solid(); b.fill.fore_color.rgb = bg
    return s

def textbox(slide, left, top, width, height, text, *, size=14, bold=False,
            color=C_GRAY_D, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
            fill=None, border=None, border_w=1, font=FONT, italic=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    if fill: box.fill.solid(); box.fill.fore_color.rgb = fill
    else: box.fill.background()
    if border: box.line.color.rgb = border; box.line.width = Pt(border_w)
    else: box.line.fill.background()
    tf = box.text_frame
    tf.margin_left = Pt(6); tf.margin_right = Pt(6)
    tf.margin_top = Pt(3); tf.margin_bottom = Pt(3)
    tf.word_wrap = True; tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    return box, tf

def add_para(tf, text, *, size=14, bold=False, italic=False, color=C_GRAY_D,
             align=PP_ALIGN.LEFT, font=FONT, space_before=0, bullet=False):
    p = tf.add_paragraph(); p.alignment = align
    if space_before: p.space_before = Pt(space_before)
    r = p.add_run()
    r.text = (("• " + text) if bullet else text)
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    return p

def rect(slide, left, top, width, height, *, fill=C_WHITE, border=C_GRAY,
         border_w=1, text="", text_size=14, text_color=C_GRAY_D,
         text_bold=False, text_align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, rounded=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, left, top, width, height)
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb = fill
    if border is None: s.line.fill.background()
    else: s.line.color.rgb = border; s.line.width = Pt(border_w)
    s.shadow.inherit = False
    if text:
        tf = s.text_frame
        tf.margin_left = Pt(6); tf.margin_right = Pt(6)
        tf.margin_top = Pt(4); tf.margin_bottom = Pt(4)
        tf.word_wrap = True; tf.vertical_anchor = anchor
        p = tf.paragraphs[0]; p.alignment = text_align
        r = p.add_run(); r.text = text
        r.font.size = Pt(text_size); r.font.bold = text_bold
        r.font.color.rgb = text_color; r.font.name = FONT
    return s

def oval(slide, left, top, width, height, *, fill=C_WHITE, border=C_GRAY,
         border_w=1, text="", text_size=14, text_color=C_GRAY_D, text_bold=False):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, width, height)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if border is None: s.line.fill.background()
    else: s.line.color.rgb = border; s.line.width = Pt(border_w)
    s.shadow.inherit = False
    if text:
        tf = s.text_frame; tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = text
        r.font.size = Pt(text_size); r.font.bold = text_bold
        r.font.color.rgb = text_color; r.font.name = FONT
    return s

def line(slide, x1, y1, x2, y2, *, color=C_GRAY, width=1.5):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb = color; c.line.width = Pt(width)
    return c

def arrow(slide, left, top, width, height, *, fill=C_ORANGE, direction="right"):
    sm = {"right": MSO_SHAPE.RIGHT_ARROW, "down": MSO_SHAPE.DOWN_ARROW}
    s = slide.shapes.add_shape(sm[direction], left, top, width, height)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.fill.background()
    return s

def table(slide, left, top, width, height, data, *, headers=None,
          header_fill=C_GREEN_D, header_color=C_WHITE, row_fills=None,
          header_size=12, body_size=11, first_col_bold=False, col_widths=None):
    rows = len(data) + (1 if headers else 0)
    cols = len(data[0]) if data else (len(headers) if headers else 1)
    shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    tbl = shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = w
    def set_cell(cell, text, *, size=11, bold=False, color=C_GRAY_D,
                 fill=None, align=PP_ALIGN.LEFT):
        cell.margin_left = Pt(6); cell.margin_right = Pt(6)
        cell.margin_top = Pt(4); cell.margin_bottom = Pt(4)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if fill: cell.fill.solid(); cell.fill.fore_color.rgb = fill
        tf = cell.text_frame; tf.word_wrap = True; tf.clear()
        p = tf.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = str(text) if text is not None else ""
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = FONT
    if headers:
        for j, h in enumerate(headers):
            set_cell(tbl.cell(0, j), h, size=header_size, bold=True,
                     color=header_color, fill=header_fill, align=PP_ALIGN.CENTER)
    for i, row in enumerate(data):
        row_i = i + (1 if headers else 0)
        rfill = row_fills[i] if row_fills and i < len(row_fills) else None
        for j, ct in enumerate(row):
            b = first_col_bold and j == 0
            set_cell(tbl.cell(row_i, j), ct, size=body_size, bold=b, fill=rfill)
    return tbl

def page_header(slide, title, *, subtitle=None, page=None):
    rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.7),
         fill=C_GREEN_D, border=None)
    textbox(slide, Inches(0.4), Inches(0.18), Inches(11), Inches(0.45),
            title, size=20, bold=True, color=C_WHITE)
    if page is not None:
        textbox(slide, Inches(11.5), Inches(0.22), Inches(1.5), Inches(0.4),
                f"{page}/{TOTAL_PAGES}", size=11, color=C_GREEN_LT,
                align=PP_ALIGN.RIGHT)
    if subtitle:
        textbox(slide, Inches(0.4), Inches(0.85), Inches(12.5), Inches(0.4),
                subtitle, size=12, italic=True, color=C_GRAY)
        return Inches(1.35)
    return Inches(0.95)

def page_footer(slide, text="APP 事业部 · DTC 三大痛点解决方案 · v3 · 2026/05/12"):
    textbox(slide, Inches(0.4), Inches(7.18), Inches(12.5), Inches(0.27),
            text, size=9, color=C_GRAY, align=PP_ALIGN.RIGHT, italic=True)

# ==================================================================
#                              页面设计
# ==================================================================

# ============ 封面 ============
def slide_cover():
    s = new_slide(C_GREEN_D)
    # 顶部橙色装饰
    rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.15),
         fill=C_ORANGE, border=None)
    # 左侧装饰
    rect(s, Inches(0.8), Inches(2.3), Inches(0.1), Inches(3.2),
         fill=C_ORANGE, border=None)
    # 主标题
    textbox(s, Inches(1.2), Inches(2.1), Inches(11), Inches(1.0),
            "Momcozy DTC 三大痛点解决方案", size=38, bold=True, color=C_WHITE)
    # v3
    rect(s, Inches(1.2), Inches(3.0), Inches(0.9), Inches(0.4),
         fill=C_ORANGE, border=None, text="v3", text_size=18,
         text_bold=True, text_color=C_WHITE, rounded=True)
    # 副标题
    textbox(s, Inches(1.2), Inches(3.55), Inches(11.3), Inches(0.7),
            "用户体验 · 数据打通 · 内容社区 —— 聚焦三大核心痛点 · 一揽子解决",
            size=17, color=C_GREEN_LT, italic=True)
    # 解决方案结构
    textbox(s, Inches(1.2), Inches(4.7), Inches(11.3), Inches(0.5),
            "3 个中台  ·  1 个联合工作组",
            size=15, color=C_WHITE, bold=True)
    # 分隔
    rect(s, Inches(1.2), Inches(5.5), Inches(3), Inches(0.03),
         fill=C_ORANGE, border=None)
    # 汇报信息
    _, tf = textbox(s, Inches(1.2), Inches(5.7), Inches(11), Inches(1.5),
                    "汇报人：APP 事业部", size=13, color=C_WHITE)
    add_para(tf, "汇报对象：创始人 / 高管团队", size=13, color=C_WHITE,
             space_before=4)
    add_para(tf, "立场：不代表 APP 部门利益 · 代表「用户视角 + 全局视角」",
             size=12, italic=True, color=C_ORANGE_LT, space_before=8)
    textbox(s, Inches(1.2), Inches(6.9), Inches(11.3), Inches(0.3),
            "2026/05/12", size=11, color=C_GREEN_LT)

# ============ P1 开篇 · 立场与逻辑链 ============
def slide_1():
    s = new_slide()
    page_header(s, "开篇 · 本次汇报的立场与逻辑",
                subtitle="聚焦 DTC 三大核心痛点 · 一揽子解决 · 组织与业务同步落地",
                page=1)
    # 立场 box
    box = rect(s, Inches(0.4), Inches(1.55), Inches(12.5), Inches(1.2),
               fill=C_GREEN_LT, border=C_GREEN_D, border_w=2, rounded=True)
    tf = box.text_frame
    tf.margin_left=Pt(24); tf.margin_top=Pt(12); tf.word_wrap=True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "立场"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_GREEN_D; r.font.name = FONT
    add_para(tf, "我作为 APP 事业部负责人提出这个方案 ——",
             size=16, bold=True, color=C_DARK, space_before=4)
    add_para(tf, "不代表 APP 部门利益，代表「用户视角」与「公司全局视角」",
             size=18, bold=True, color=C_GREEN_D, space_before=4)

    # 逻辑链
    textbox(s, Inches(0.4), Inches(3.0), Inches(12.5), Inches(0.4),
            "本次汇报逻辑链", size=14, bold=True, color=C_DARK)
    steps = [
        ("① 现状", "产品侧漏斗 + 组织侧分散", C_GRAY),
        ("② 痛点", "用户体验 · 数据打通 · 内容社区", C_RED),
        ("③ 方案", "3 中台 + 1 联合工作组", C_GREEN_D),
        ("④ 证明", "APP 生态能力承接", C_ORANGE),
        ("⑤ 目标", "DTC 占比提升 · 转化率恢复", C_BLUE),
    ]
    x0 = Inches(0.4); w = (Inches(12.5) - Inches(0.4)) / 5
    gap = Inches(0.1); y = Inches(3.55)
    for i, (name, body, color) in enumerate(steps):
        x = x0 + (w + gap - Inches(0.02)) * i
        rect(s, x, y, w, Inches(0.55), fill=color, border=None,
             text=name, text_size=13, text_bold=True, text_color=C_WHITE,
             rounded=True)
        rect(s, x, y + Inches(0.6), w, Inches(0.75), fill=C_WHITE,
             border=color, border_w=1, text=body, text_size=11,
             text_color=C_DARK, rounded=True)

    # 核心主张
    main_box = rect(s, Inches(0.4), Inches(5.2), Inches(12.5), Inches(1.8),
                    fill=C_WHITE, border=C_GREEN_D, border_w=2, rounded=True)
    tf2 = main_box.text_frame
    tf2.margin_left=Pt(24); tf2.margin_right=Pt(24); tf2.margin_top=Pt(14)
    tf2.word_wrap=True
    p = tf2.paragraphs[0]
    r = p.add_run(); r.text = "核心主张"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_GREEN_D; r.font.name = FONT
    add_para(tf2,
             "三大痛点根因同源 —— 组织按「触点」切，不按「用户旅程」切；",
             size=14, color=C_DARK, space_before=6)
    add_para(tf2,
             "因此解决方案必须是 —— 3 个中台统一底层能力 + 1 个联合工作组专攻独立站转化。",
             size=14, bold=True, color=C_GREEN_D, space_before=4)
    add_para(tf2,
             "APP 事业部过去 2 年在用户资产、内容、数据、AI 能力上的沉淀，是这 3 个中台能快速跑通的底座。",
             size=12, italic=True, color=C_GRAY, space_before=8)
    page_footer(s)

# ============ P2 现状一 · 产品侧转化漏斗（还原图1） ============
def slide_2():
    s = new_slide()
    page_header(s, "现状一 · 产品侧：转化漏斗",
                subtitle="流量池极大 · 但 Add-to-Cart 和 Checkout/Purchase 环节严重流失",
                page=2)

    # 左：漏斗图（5 层递减宽度的矩形）
    funnel_layers = [
        ("Session Start", "20,296,273", 1.00, C_GREEN_LT, C_GREEN_D),
        ("View Product",  "8,524,113",  0.80, C_GREEN_M,  C_WHITE),
        ("Add to Cart",   "720,154",    0.60, RGBColor(0x43,0xA0,0x47), C_WHITE),
        ("Checkout",      "316,431",    0.45, C_GREEN,    C_WHITE),
        ("Purchase",      "131,670",    0.30, C_GREEN_D,  C_WHITE),
    ]
    # 漏斗画法：5 层居中递减矩形
    fx_center = 2.6  # inches
    max_w = 4.2
    layer_h = 0.75
    gap_in = 0.05
    y_top = 1.55
    for i, (label, value, ratio, fill, tc) in enumerate(funnel_layers):
        w = max_w * ratio
        x = fx_center - w/2
        y = y_top + (layer_h + gap_in) * i
        box = rect(s, Inches(x), Inches(y), Inches(w), Inches(layer_h),
                   fill=fill, border=None)
        tf = box.text_frame
        tf.margin_top=Pt(4); tf.margin_bottom=Pt(4); tf.word_wrap=True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = label
        r.font.size = Pt(10); r.font.bold = True
        r.font.color.rgb = tc; r.font.name = FONT
        add_para(tf, value, size=15, bold=True, color=tc,
                 align=PP_ALIGN.CENTER, space_before=2)

    # 右：分层诊断
    diag_items = [
        ("优秀", C_GREEN, "1. Session Start",
         "流量池极大",
         "CVR: 100%  |  表现评价：流量基数极高"),
        ("合格", C_GREEN, "2. View Product",
         "转化稳定",
         "CVR: 42.0%  (Benchmark: 30%-45%)"),
        ("预警", C_RED, "3. Add to Cart",
         "产品表达力不足",
         "CVR: 8.4%  (Benchmark: 10%-15%)  |  诊断：信任度不足"),
        ("严重", C_RED, "4 & 5. Checkout & Purchase",
         "流失极大",
         "加购后流失：CVR 43.9% vs BM 50-60%\n支付/物流门槛过高：CVR 41.6% vs BM 50-70%"),
    ]
    dx = Inches(5.5); dw = Inches(7.4); dy = Inches(1.55); dh = Inches(1.3)
    for i, (badge, badge_color, title, sub, body) in enumerate(diag_items):
        y = dy + (dh + Inches(0.1)) * i - Inches(0.05) * i
        # 背景
        bg_color = C_RED_LT if badge_color == C_RED else C_GREEN_LT
        border_color = badge_color
        box = rect(s, dx, y, dw, dh, fill=bg_color, border=border_color,
                   border_w=1, rounded=True)
        # 徽章
        rect(s, dx + Inches(0.15), y + Inches(0.15),
             Inches(0.5), Inches(0.35), fill=badge_color, border=None,
             text=badge, text_size=10, text_bold=True, text_color=C_WHITE,
             rounded=True)
        # 标题
        textbox(s, dx + Inches(0.75), y + Inches(0.12),
                dw - Inches(0.9), Inches(0.35),
                f"{title}  ·  {sub}", size=13, bold=True, color=C_DARK)
        # 正文
        textbox(s, dx + Inches(0.75), y + Inches(0.48),
                dw - Inches(0.9), Inches(0.75),
                body, size=10.5, color=C_GRAY_D)

    # 底部数据来源
    textbox(s, Inches(0.4), Inches(7.18), Inches(12.5), Inches(0.27),
            "* 数据来源 GA（最近一年）",
            size=9, italic=True, color=C_GRAY, align=PP_ALIGN.RIGHT)

# ============ P3 现状二 · 组织侧分散作战（还原图2） ============
def slide_3():
    s = new_slide()
    page_header(s, "现状二 · 组织侧：分散作战",
                subtitle="各部门本位视角 · 业务按触点切 · 缺乏统一目标",
                page=3)

    # 四个痛点卡片（2×2 网格）
    pains = [
        ("痛点 1 · 体验割裂", "用户流失风险",
         "账号与数据未完全打通；面向用户体验各自设计，风格体验流程各异；品牌体验一致性较弱",
         "无品牌官网属性产品，统一传达品牌理念；APP 累计消费 $800 用户回独立站仍按「新客」对待；APP 跳转直独立站，体验割裂——用户反馈：「是不是两个品牌？」",
         "基础体验割裂 · NPS 受损 · 高价值用户流失"),
        ("痛点 2 · 资源浪费", "重复投入",
         "独立站与 APP 分别有 Community；各自规划，未充分考虑其他业务线调用与扩展；素材规划未充分考虑多个触点，无法重复使用",
         "两个社区及团队；APP 接入商城",
         "两个社区用户理解难度大，投入资源重复，未全局考量的架构方案导致新场景额外投入"),
        ("痛点 3 · 决策延迟", "错失市场窗口",
         "快赢创新策略无法快速实施验证，需要多方评估、排期；新品大促、会员活动需协调多个部门，节奏慢，决策与实施周期拉长 1-2 周；步调排期统一难",
         None,
         "痛点不能快速产品化传达给用户，资源利用 ROI 低"),
        ("痛点 4 · SOP 化率低", "持续效率低、提效难",
         "日常活动、大促、内容管理、资源利用与调配等，无法形成高质量的 SOP，每一次都如第一次，缺乏有条不紊的节奏感，执行效果与团队士气双杀",
         None,
         "每一次都如第一次一样的投入，质量不稳定，单个环节提效无意义化"),
    ]
    # 上排三个 + 下排一个
    positions = [
        (Inches(0.4), Inches(1.55), Inches(4.05), Inches(3.7)),
        (Inches(4.65), Inches(1.55), Inches(4.05), Inches(3.7)),
        (Inches(8.9), Inches(1.55), Inches(4.05), Inches(3.7)),
    ]
    for i, ((name, sub, fact, case, cost), (x, y, w, h)) in \
            enumerate(zip(pains[:3], positions)):
        # 头
        rect(s, x, y, w, Inches(0.5), fill=C_GREEN_D, border=None,
             text=name, text_size=13, text_bold=True, text_color=C_WHITE,
             rounded=False)
        rect(s, x, y + Inches(0.5), w, Inches(0.4),
             fill=C_GREEN_LT, border=None,
             text=f"→  {sub}", text_size=12, text_bold=True,
             text_color=C_GREEN_D)
        # 主卡
        box = rect(s, x, y + Inches(0.95), w, h - Inches(0.95),
                   fill=C_GREEN_LL, border=C_GREEN_M, border_w=1)
        tf = box.text_frame
        tf.margin_left=Pt(10); tf.margin_right=Pt(10); tf.margin_top=Pt(8)
        tf.word_wrap=True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = "● 事实"
        r.font.size = Pt(11); r.font.bold = True
        r.font.color.rgb = C_GREEN_D; r.font.name = FONT
        add_para(tf, fact, size=9.5, color=C_GRAY_D, space_before=2)
        if case:
            add_para(tf, "● 典型", size=11, bold=True, color=C_GREEN_D,
                     space_before=8)
            add_para(tf, case, size=9.5, color=C_GRAY_D, space_before=2)
        add_para(tf, "● 隐形成本", size=11, bold=True, color=C_GREEN_D,
                 space_before=8)
        add_para(tf, cost, size=9.5, color=C_GRAY_D, space_before=2)

    # 下排痛点 4（左 1/3 是卡片头，右 2/3 是内容）
    p4 = pains[3]
    py = Inches(5.4); ph = Inches(1.45)
    # 左头
    rect(s, Inches(0.4), py, Inches(4.05), ph,
         fill=C_GREEN_LL, border=C_GREEN_M, border_w=1, rounded=False)
    rect(s, Inches(0.4), py, Inches(4.05), Inches(0.5),
         fill=C_GREEN_D, border=None,
         text=p4[0], text_size=13, text_bold=True, text_color=C_WHITE)
    rect(s, Inches(0.4), py + Inches(0.5), Inches(4.05), Inches(0.4),
         fill=C_GREEN_LT, border=None,
         text=f"→  {p4[1]}", text_size=12, text_bold=True,
         text_color=C_GREEN_D)
    # 右内容
    box4 = rect(s, Inches(4.65), py, Inches(8.25), ph,
                fill=C_GREEN_LL, border=C_GREEN_M, border_w=1)
    tf4 = box4.text_frame
    tf4.margin_left=Pt(12); tf4.margin_right=Pt(12); tf4.margin_top=Pt(10)
    tf4.word_wrap=True
    p = tf4.paragraphs[0]
    r = p.add_run(); r.text = "● 事实"
    r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = C_GREEN_D
    r.font.name = FONT
    add_para(tf4, p4[2], size=10, color=C_GRAY_D, space_before=2)
    add_para(tf4, "● 隐形成本", size=11, bold=True, color=C_GREEN_D,
             space_before=6)
    add_para(tf4, p4[4], size=10, color=C_GRAY_D, space_before=2)

    # 底部总结
    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="分散作战，缺乏统一目标、全局组织、高效协作",
         text_size=14, text_bold=True, text_color=C_WHITE)

# ============ P4 解决方案总览（三大痛点 → 三中台 + 一联合组） ============
def slide_4():
    s = new_slide()
    page_header(s, "解决方案 · 总览",
                subtitle="3 个中台统一底层能力 · 1 个联合工作组专攻独立站转化漏斗",
                page=4)

    # 三大痛点（顶部横排）
    textbox(s, Inches(0.4), Inches(1.4), Inches(12.5), Inches(0.4),
            "① 三大痛点（收敛范围）", size=14, bold=True, color=C_DARK)
    pains = [
        ("用户体验", "体验割裂 · 转化流失", C_RED),
        ("数据打通", "统一用户数据与洞察", C_ORANGE),
        ("内容与社区", "统一内容与社区", C_BLUE),
    ]
    pw = (Inches(12.5) - Inches(0.3)) / 3; py = Inches(1.85); ph = Inches(0.65)
    for i, (name, desc, color) in enumerate(pains):
        x = Inches(0.4) + (pw + Inches(0.15)) * i
        rect(s, x, py, pw, ph, fill=color, border=None,
             text=f"痛点 {i+1}  ·  {name}",
             text_size=14, text_bold=True, text_color=C_WHITE, rounded=True)
        textbox(s, x, py + ph + Inches(0.05), pw, Inches(0.3),
                desc, size=11, color=color, align=PP_ALIGN.CENTER, italic=True)

    # 向下箭头
    for i in range(3):
        x = Inches(0.4) + (pw + Inches(0.15)) * i + pw/2
        arrow(s, x - Inches(0.15), Inches(3.0), Inches(0.3), Inches(0.35),
              fill=C_ORANGE, direction="down")

    # 三个中台（中间横排）
    textbox(s, Inches(0.4), Inches(3.55), Inches(12.5), Inches(0.4),
            "② 三个中台（统一底层能力 · 服务整个 DTC 业务）",
            size=14, bold=True, color=C_DARK)
    zhongtai = [
        ("用户资产中台", "One-ID · CDP · 会员 · 生命周期",
         "统一用户资产 · 跨触点识别",
         C_RED, C_RED_LT),
        ("内容中台", "PGC · UGC · AIGC · 社区",
         "内容与社区统一运营",
         C_BLUE, C_BLUE_LT),
        ("增长中台", "SEM · SEO · 红人 · 私域 · 归因",
         "全域投放 · 数据洞察",
         C_ORANGE, C_ORANGE_LT),
    ]
    zy = Inches(4.0); zh = Inches(1.3)
    for i, (name, detail, role, color, color_lt) in enumerate(zhongtai):
        x = Inches(0.4) + (pw + Inches(0.15)) * i
        rect(s, x, zy, pw, Inches(0.5), fill=color, border=None,
             text=name, text_size=14, text_bold=True, text_color=C_WHITE,
             rounded=True)
        rect(s, x, zy + Inches(0.55), pw, zh - Inches(0.55),
             fill=color_lt, border=color, border_w=1, rounded=True)
        textbox(s, x + Inches(0.1), zy + Inches(0.62),
                pw - Inches(0.2), Inches(0.3),
                detail, size=10, color=color, bold=True,
                align=PP_ALIGN.CENTER)
        textbox(s, x + Inches(0.1), zy + Inches(0.92),
                pw - Inches(0.2), Inches(0.3),
                role, size=10, color=C_GRAY_D, align=PP_ALIGN.CENTER,
                italic=True)

    # 联合工作组（底部整条）
    textbox(s, Inches(0.4), Inches(5.5), Inches(12.5), Inches(0.4),
            "③ 独立站 × APP 联合工作组（专攻独立站转化漏斗）",
            size=14, bold=True, color=C_DARK)
    box = rect(s, Inches(0.4), Inches(5.95), Inches(12.5), Inches(0.85),
               fill=C_GREEN_D, border=None, rounded=True)
    tf = box.text_frame
    tf.margin_left=Pt(20); tf.margin_right=Pt(20); tf.margin_top=Pt(8)
    tf.word_wrap=True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "独立站 × APP 联合工作组"
    r.font.size = Pt(14); r.font.bold = True
    r.font.color.rgb = C_WHITE; r.font.name = FONT
    add_para(tf,
             "优化现有独立站体验 · 提升转化 · 同时适配 APP · 提升 DTC 整体业务占比",
             size=11, color=C_GREEN_LT, align=PP_ALIGN.CENTER, space_before=4)

    # 底部一句话
    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_LT, border=C_GREEN_D, border_w=1, rounded=True,
         text="中台解决「底层能力统一」 · 联合工作组解决「顶层业务爆发力」",
         text_size=12, text_bold=True, text_color=C_GREEN_D)

# ============ P5 痛点 1 · 用户体验 → 用户资产中台 ============
def slide_5():
    s = new_slide()
    page_header(s, "方案 1 · 用户体验 → 用户资产中台",
                subtitle="解决「体验割裂」· 承接 Add-to-Cart 信任度不足 + Checkout 流失",
                page=5)

    # 左：现状痛点 + 中台职能
    # 现状
    rect(s, Inches(0.4), Inches(1.4), Inches(5.8), Inches(0.4),
         fill=C_RED, border=None, rounded=True,
         text="✕  现状痛点", text_size=12, text_bold=True, text_color=C_WHITE)
    box1 = rect(s, Inches(0.4), Inches(1.85), Inches(5.8), Inches(1.85),
                fill=C_RED_LT, border=C_RED, border_w=1, rounded=True)
    tf1 = box1.text_frame
    tf1.margin_left=Pt(14); tf1.margin_right=Pt(14); tf1.margin_top=Pt(10)
    tf1.word_wrap=True
    p = tf1.paragraphs[0]
    r = p.add_run(); r.text = "跨触点身份与数据分裂"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_RED; r.font.name = FONT
    add_para(tf1, "独立站 ID-A / APP ID-B / 会员系统 ID-C 互不互通",
             size=10.5, color=C_GRAY_D, space_before=6, bullet=True)
    add_para(tf1, "APP 累计消费 $800 用户回独立站被识别为「新客」",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf1, "会员等级 / 积分 / 优惠券跨触点不识别",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf1, "→  直接拉低 Add-to-Cart（8.4% vs BM 10-15%）的信任度",
             size=11, bold=True, color=C_RED, space_before=8)

    # 中台职能
    rect(s, Inches(0.4), Inches(3.9), Inches(5.8), Inches(0.4),
         fill=C_GREEN_D, border=None, rounded=True,
         text="✓  用户资产中台 · 职能", text_size=12, text_bold=True,
         text_color=C_WHITE)
    data = [
        ["One-ID 体系", "站 / APP / 小程序 / 会员系统 统一身份"],
        ["CDP 用户画像", "行为 + 购买 + 设备数据统一沉淀"],
        ["会员体系全局化", "等级 / 积分 / 权益跨触点识别"],
        ["生命周期管理", "孕期 → 哺乳 → 断奶 → 二胎 精准标签"],
        ["数据洞察服务", "服务所有业务部门的数据底座"],
    ]
    table(s, Inches(0.4), Inches(4.35), Inches(5.8), Inches(2.55), data,
          headers=None, first_col_bold=True, body_size=10,
          row_fills=[C_GREEN_LT, C_WHITE, C_GREEN_LT, C_WHITE, C_GREEN_LT],
          col_widths=[Inches(1.8), Inches(4.0)])

    # 右：APP 能力证明
    rect(s, Inches(6.4), Inches(1.4), Inches(6.5), Inches(0.4),
         fill=C_ORANGE, border=None, rounded=True,
         text="★ APP 生态能力证明 · 为什么 APP 是天然底座",
         text_size=12, text_bold=True, text_color=C_WHITE)
    caps = [
        ("APP 会员体系已成型", "积分 + 等级 + 权益已运行 · 是 One-ID 的天然起点"),
        ("IoT 设备绑定数据", "M5 / M6 / M9 设备型号、使用时长、固件版本 —— 独立站从未拥有"),
        ("生命周期行为数据", "吸奶记录 / 喂养 / 睡眠 / 生长曲线 —— 独有的生命周期信号"),
        ("AI Agent 已上线", "智能客服 / 个性化推荐 · 可直接为独立站提供能力"),
        ("高频触达能力", "Push / 站内信 · 触达成本近 0 · 独立站做不到"),
    ]
    cy = Inches(1.85); ch = Inches(0.95)
    for i, (name, body) in enumerate(caps):
        y = cy + (ch + Inches(0.06)) * i
        rect(s, Inches(6.4), y, Inches(0.5), ch, fill=C_ORANGE, border=None,
             text=f"✓{i+1}", text_size=13, text_bold=True, text_color=C_WHITE)
        box = rect(s, Inches(6.95), y, Inches(5.95), ch, fill=C_WHITE,
                   border=C_ORANGE, border_w=1)
        tf = box.text_frame
        tf.margin_left=Pt(10); tf.margin_top=Pt(6); tf.word_wrap=True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = name
        r.font.size = Pt(12); r.font.bold = True
        r.font.color.rgb = C_DARK; r.font.name = FONT
        add_para(tf, body, size=9.5, color=C_GRAY_D, space_before=2)

    # 底部核心主张
    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="用户资产中台的底层能力，APP 生态已跑通 60%+ —— 整合即用，无需从零建",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ P6 痛点 2 · 数据打通 → 增长中台 + 用户资产中台协同 ============
def slide_6():
    s = new_slide()
    page_header(s, "方案 2 · 数据打通 → 增长中台",
                subtitle="解决「决策延迟 + 快赢难验证」· 投放统一 + 归因 + AB + AI 洞察",
                page=6)

    # 左：现状
    rect(s, Inches(0.4), Inches(1.4), Inches(5.8), Inches(0.4),
         fill=C_RED, border=None, rounded=True,
         text="✕  现状痛点", text_size=12, text_bold=True, text_color=C_WHITE)
    box1 = rect(s, Inches(0.4), Inches(1.85), Inches(5.8), Inches(1.85),
                fill=C_RED_LT, border=C_RED, border_w=1, rounded=True)
    tf1 = box1.text_frame
    tf1.margin_left=Pt(14); tf1.margin_right=Pt(14); tf1.margin_top=Pt(10)
    tf1.word_wrap=True
    p = tf1.paragraphs[0]
    r = p.add_run(); r.text = "数据散落 · 决策慢 · 无法快赢验证"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_RED; r.font.name = FONT
    add_para(tf1, "投放 / 归因 / AB 数据散在各部门，没有统一口径",
             size=10.5, color=C_GRAY_D, space_before=6, bullet=True)
    add_para(tf1, "新品大促 / 会员活动需协调多部门，决策周期 1-2 周",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf1, "快赢创新策略无法快速实施验证 —— 窗口过了才上线",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf1, "→  ROAS 被内部互拍拉低，快赢 ROI 持续偏低",
             size=11, bold=True, color=C_RED, space_before=8)

    # 中台职能
    rect(s, Inches(0.4), Inches(3.9), Inches(5.8), Inches(0.4),
         fill=C_GREEN_D, border=None, rounded=True,
         text="✓  增长中台 · 职能", text_size=12, text_bold=True,
         text_color=C_WHITE)
    data = [
        ["全域投放", "SEM / SEO / Meta / TikTok / 红人统一调度"],
        ["统一归因", "跨触点归因模型 · 避免内部抢量"],
        ["AB 实验平台", "任何触点都能快速跑 AB · 快赢验证 < 3 天"],
        ["私域 / EDM / Push", "自动化营销引擎"],
        ["增长数据洞察", "每周一张表 · CEO 只看一张表"],
    ]
    table(s, Inches(0.4), Inches(4.35), Inches(5.8), Inches(2.55), data,
          headers=None, first_col_bold=True, body_size=10,
          row_fills=[C_GREEN_LT, C_WHITE, C_GREEN_LT, C_WHITE, C_GREEN_LT],
          col_widths=[Inches(1.8), Inches(4.0)])

    # 右：APP 能力证明
    rect(s, Inches(6.4), Inches(1.4), Inches(6.5), Inches(0.4),
         fill=C_ORANGE, border=None, rounded=True,
         text="★ APP 生态能力证明 · 数据与快赢验证",
         text_size=12, text_bold=True, text_color=C_WHITE)
    caps = [
        ("APP 是高频数据源", "DAU / 停留 / 行为事件埋点齐全 · 独立站只有 Session 和订单"),
        ("AB 实验已跑通", "APP 端每周上线多个 AB · 快赢验证周期 < 3 天"),
        ("AI Agent 数据闭环", "用户对话 + 反馈回流 · 产品 / 内容 / 投放 三方受益"),
        ("CDP 用户分层", "APP 端已完成基础用户标签体系 · 可直接输出给投放"),
        ("Push 作为营销工具", "触达时机 / 频次 / 转化 可被精细度量"),
    ]
    cy = Inches(1.85); ch = Inches(0.95)
    for i, (name, body) in enumerate(caps):
        y = cy + (ch + Inches(0.06)) * i
        rect(s, Inches(6.4), y, Inches(0.5), ch, fill=C_ORANGE, border=None,
             text=f"✓{i+1}", text_size=13, text_bold=True, text_color=C_WHITE)
        box = rect(s, Inches(6.95), y, Inches(5.95), ch, fill=C_WHITE,
                   border=C_ORANGE, border_w=1)
        tf = box.text_frame
        tf.margin_left=Pt(10); tf.margin_top=Pt(6); tf.word_wrap=True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = name
        r.font.size = Pt(12); r.font.bold = True
        r.font.color.rgb = C_DARK; r.font.name = FONT
        add_para(tf, body, size=9.5, color=C_GRAY_D, space_before=2)

    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="增长中台的核心是「快赢验证」—— APP 是目前集团内唯一跑通快速 AB 的业务",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ P7 痛点 3 · 内容社区 → 内容中台 ============
def slide_7():
    s = new_slide()
    page_header(s, "方案 3 · 内容与社区 → 内容中台",
                subtitle="解决「两个社区重复投入」· UGC 资产化 · AI 创作工具化",
                page=7)

    # 左：现状
    rect(s, Inches(0.4), Inches(1.4), Inches(5.8), Inches(0.4),
         fill=C_RED, border=None, rounded=True,
         text="✕  现状痛点", text_size=12, text_bold=True, text_color=C_WHITE)
    box1 = rect(s, Inches(0.4), Inches(1.85), Inches(5.8), Inches(1.85),
                fill=C_RED_LT, border=C_RED, border_w=1, rounded=True)
    tf1 = box1.text_frame
    tf1.margin_left=Pt(14); tf1.margin_right=Pt(14); tf1.margin_top=Pt(10)
    tf1.word_wrap=True
    p = tf1.paragraphs[0]
    r = p.add_run(); r.text = "两个社区 · 两个团队 · 两套资产"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_RED; r.font.name = FONT
    add_para(tf1, "独立站社区与 APP 社区各自规划 · 内容池不互通",
             size=10.5, color=C_GRAY_D, space_before=6, bullet=True)
    add_para(tf1, "素材规划未充分考虑多个触点 · 无法重复使用",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf1, "创作者 / UGC 身份被分裂，头部难被跨触点识别",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf1, "→  资源重复投入 · 品牌声音不统一 · UGC 无法资产化",
             size=11, bold=True, color=C_RED, space_before=8)

    # 中台职能
    rect(s, Inches(0.4), Inches(3.9), Inches(5.8), Inches(0.4),
         fill=C_GREEN_D, border=None, rounded=True,
         text="✓  内容中台 · 职能", text_size=12, text_bold=True,
         text_color=C_WHITE)
    data = [
        ["统一内容池", "PGC / UGC / AIGC 全部沉淀到中台"],
        ["双社区整合", "独立站社区 + APP 社区 → 一个品牌社区"],
        ["创作者激励体系", "积分 / 打赏 / 分级 · 跨触点统一"],
        ["AI 创作工具", "AI 一键生成多触点素材（图 / 视频 / 文案）"],
        ["内容数据服务", "为投放 / 落地页 / Push 输出高转化素材"],
    ]
    table(s, Inches(0.4), Inches(4.35), Inches(5.8), Inches(2.55), data,
          headers=None, first_col_bold=True, body_size=10,
          row_fills=[C_GREEN_LT, C_WHITE, C_GREEN_LT, C_WHITE, C_GREEN_LT],
          col_widths=[Inches(1.8), Inches(4.0)])

    # 右：APP 能力证明
    rect(s, Inches(6.4), Inches(1.4), Inches(6.5), Inches(0.4),
         fill=C_ORANGE, border=None, rounded=True,
         text="★ APP 生态能力证明 · 内容与社区运营",
         text_size=12, text_bold=True, text_color=C_WHITE)
    caps = [
        ("APP 社区已沉淀头部创作者", "妈妈圈 / UGC / 问答 / 话题 持续运营 · 头部账号已成型"),
        ("工具库反哺内容", "8 个育儿计算器 / 吸奶记录 · 天然产生用户数据内容"),
        ("AI 创作能力已就绪", "AI Agent 可自动生成多格式素材（图文 / 短视频脚本）"),
        ("内容分发矩阵", "Push / Feed / 个性化推荐 · 已验证转化能力"),
        ("生命周期内容推送", "孕期 / 哺乳 / 断奶 精准内容 · 独立站 EDM 做不到"),
    ]
    cy = Inches(1.85); ch = Inches(0.95)
    for i, (name, body) in enumerate(caps):
        y = cy + (ch + Inches(0.06)) * i
        rect(s, Inches(6.4), y, Inches(0.5), ch, fill=C_ORANGE, border=None,
             text=f"✓{i+1}", text_size=13, text_bold=True, text_color=C_WHITE)
        box = rect(s, Inches(6.95), y, Inches(5.95), ch, fill=C_WHITE,
                   border=C_ORANGE, border_w=1)
        tf = box.text_frame
        tf.margin_left=Pt(10); tf.margin_top=Pt(6); tf.word_wrap=True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = name
        r.font.size = Pt(12); r.font.bold = True
        r.font.color.rgb = C_DARK; r.font.name = FONT
        add_para(tf, body, size=9.5, color=C_GRAY_D, space_before=2)

    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="APP 社区是更活跃、更高频、更有 UGC 积累的一侧 —— 由 APP 主导内容中台最合理",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ P8 APP 生态六大底层能力（一张总览） ============
def slide_8():
    s = new_slide()
    page_header(s, "APP 生态 · 六大底层能力总览",
                subtitle="为什么 APP 是承接 3 个中台的天然底座 —— 过去 2 年已经搭完一半",
                page=8)

    caps = [
        ("📱\n高频触达", "Push / 站内信 / 站内弹窗\n触达成本近 0",
         C_ORANGE),
        ("🔐\n会员与 One-ID", "积分 / 等级 / 权益已跑通\n跨触点识别的起点",
         C_RED),
        ("🏷️\n行为数据 & CDP", "设备 + 行为 + 生命周期\n独立站无法独立拥有",
         C_BLUE),
        ("🤖\nAI Agent & 推荐", "智能客服 / 个性化内容\n已上线 · 可复用",
         C_PURPLE),
        ("👥\n社区与 UGC", "妈妈圈 / 问答 / 话题\n头部创作者已沉淀",
         C_GREEN),
        ("🧪\n快赢 AB 实验", "每周跑多个 AB\n快赢验证周期 < 3 天",
         C_ORANGE),
    ]
    # 2 行 3 列
    cw = (Inches(12.5) - Inches(0.4)) / 3; ch = Inches(2.2); gap = Inches(0.2)
    x0 = Inches(0.4); y0 = Inches(1.5)
    for i, (title, body, color) in enumerate(caps):
        r, c = i // 3, i % 3
        x = x0 + (cw + gap) * c
        y = y0 + (ch + Inches(0.2)) * r
        # 卡片外框
        rect(s, x, y, cw, ch, fill=C_WHITE, border=color, border_w=2,
             rounded=True)
        # 顶色条
        rect(s, x, y, cw, Inches(0.08), fill=color, border=None)
        # Icon + 标题
        textbox(s, x + Inches(0.15), y + Inches(0.25), cw - Inches(0.3),
                Inches(1.2), title, size=22, bold=True, color=color,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 正文
        textbox(s, x + Inches(0.15), y + Inches(1.45), cw - Inches(0.3),
                Inches(0.7), body, size=12, color=C_GRAY_D,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)

    # 底部结论
    rect(s, Inches(0.4), Inches(6.7), Inches(12.5), Inches(0.6),
         fill=C_GREEN_LT, border=C_GREEN_D, border_w=2, rounded=True,
         text="这六大能力不是「APP 部门的能力」—— 是「公司 DTC 底层资产」\n"
              "3 个中台只需要把这些能力从 APP 放大到全触点，无需从零建设",
         text_size=12, text_bold=True, text_color=C_GREEN_D)

# ============ P9 独立站 × APP 联合工作组 · 专攻转化漏斗 ============
def slide_9():
    s = new_slide()
    page_header(s, "独立站 × APP 联合工作组 · 专攻转化漏斗",
                subtitle="针对 Add-to-Cart 预警 + Checkout/Purchase 严重流失 · 3 个月快赢",
                page=9)

    # 顶部目标
    rect(s, Inches(0.4), Inches(1.35), Inches(12.5), Inches(0.5),
         fill=C_ORANGE, border=None, rounded=True,
         text="目标：3 个月内 Add-to-Cart CVR 8.4% → 12% · Checkout 43.9% → 52% · 最终 DTC 占比提升 3-5 pp",
         text_size=13, text_bold=True, text_color=C_WHITE)

    # 针对漏斗 3 个薄弱环节 × 行动方案
    textbox(s, Inches(0.4), Inches(2.0), Inches(12.5), Inches(0.3),
            "工作组聚焦 3 个漏斗环节 · APP 能力直接回灌独立站",
            size=13, bold=True, color=C_DARK)
    actions = [
        ("🚨 Add to Cart",
         "CVR 8.4% → 目标 12%",
         "信任度不足",
         [
             "APP 真实妈妈 UGC 回灌独立站 PDP（详情页）",
             "APP 识别「用户已有 M5」→ 独立站精准推荐配件",
             "APP 会员等级带回独立站，不再被当「新客」",
             "APP AI 客服 SDK 嵌入独立站 PDP · 答疑秒回",
         ],
         C_RED),
        ("⚠️ Checkout",
         "CVR 43.9% → 目标 52%",
         "支付 / 登录门槛高",
         [
             "APP 一键登录独立站（Sign in with Momcozy）",
             "APP 已存地址 / 支付方式 / 收货信息同步",
             "APP 已领取的优惠券在独立站结算自动识别",
             "APP Push 购物车召回（弃单用户 2h 内推送）",
         ],
         C_ORANGE),
        ("⚠️ Purchase",
         "CVR 41.6% → 目标 55%",
         "物流 / 最后一步门槛",
         [
             "物流透明化 · APP 订单查询与独立站统一",
             "APP 内会员价在独立站结算同步呈现",
             "APP 积分可在独立站抵扣 · 拉高转化动机",
             "失败订单回流 APP 继续推荐 · 不流失用户",
         ],
         C_GREEN),
    ]
    aw = (Inches(12.5) - Inches(0.3)) / 3; ay = Inches(2.45); ah = Inches(4.4)
    for i, (stage, target, reason, items, color) in enumerate(actions):
        x = Inches(0.4) + (aw + Inches(0.15)) * i
        # 头
        rect(s, x, ay, aw, Inches(0.5), fill=color, border=None,
             text=stage, text_size=13, text_bold=True, text_color=C_WHITE,
             rounded=True)
        # 目标
        rect(s, x, ay + Inches(0.55), aw, Inches(0.4),
             fill=C_WHITE, border=color, border_w=1, rounded=True,
             text=target, text_size=12, text_bold=True, text_color=color)
        # 原因
        textbox(s, x, ay + Inches(1.0), aw, Inches(0.3),
                f"根因：{reason}", size=10, italic=True, color=C_GRAY,
                align=PP_ALIGN.CENTER)
        # 行动列表
        box = rect(s, x, ay + Inches(1.35), aw, ah - Inches(1.35),
                   fill=C_GREEN_LL, border=color, border_w=1, rounded=True)
        tf = box.text_frame
        tf.margin_left=Pt(10); tf.margin_right=Pt(10); tf.margin_top=Pt(10)
        tf.word_wrap=True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = "APP 能力回灌独立站"
        r.font.size = Pt(11); r.font.bold = True
        r.font.color.rgb = color; r.font.name = FONT
        for j, item in enumerate(items):
            add_para(tf, item, size=10, color=C_GRAY_D,
                     space_before=6 if j == 0 else 5, bullet=True)

    # 底部
    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="联合工作组 = 独立站转化 + APP 能力 · 独立站负责页面，APP 负责身份 / 数据 / 内容 / 智能",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ P10 新组织架构（3 中台 + 1 联合工作组） ============
def slide_10():
    s = new_slide()
    page_header(s, "新组织架构 · 3 中台 + 1 联合工作组",
                subtitle="能力沉淀到中台 · 业务爆发靠联合组 · 现有部门「再定位」",
                page=10)

    # 战略委员会顶
    rect(s, Inches(2.5), Inches(1.35), Inches(8.3), Inches(0.5),
         fill=C_DARK, border=None, rounded=True,
         text="DTC 战略委员会（创始人 + DTC Leader + CMO + CTO）",
         text_size=12, text_bold=True, text_color=C_WHITE)
    line(s, Inches(6.65), Inches(1.85), Inches(6.65), Inches(2.1),
         color=C_DARK, width=2)

    # DTC 事业部
    rect(s, Inches(2.5), Inches(2.1), Inches(8.3), Inches(0.5),
         fill=C_GREEN_D, border=None, rounded=True,
         text="DTC 事业部（一个 Leader 统管）",
         text_size=13, text_bold=True, text_color=C_WHITE)

    # 主干横线
    line(s, Inches(1.5), Inches(2.95), Inches(11.83), Inches(2.95),
         color=C_GREEN_D, width=2)
    # 从 DTC 事业部到主干
    line(s, Inches(6.65), Inches(2.6), Inches(6.65), Inches(2.95),
         color=C_GREEN_D, width=2)

    # 3 个中台（左中右）+ 联合工作组（最右）
    centers = [
        ("用户资产中台",
         "Head of CRM & Data",
         "One-ID · CDP\n会员 · 生命周期",
         "LTV · 复购 · 会员渗透",
         C_RED),
        ("内容中台",
         "Head of Content",
         "PGC · UGC · AIGC\n社区 · 创作者",
         "DAU · UGC · 内容 ROI",
         C_BLUE),
        ("增长中台",
         "Head of Growth",
         "SEM · SEO · 红人\n归因 · AB · 私域",
         "CAC · ROAS · AB 频次",
         C_ORANGE),
        ("独立站 × APP\n联合工作组",
         "Head of DTC Commerce",
         "转化漏斗优化\n独立站 × APP 适配",
         "独立站 GMV · 转化率",
         C_GREEN_D),
    ]
    cw = Inches(2.85); ch = Inches(2.5); gap = Inches(0.13)
    x0 = Inches(0.5); y0 = Inches(3.1)
    total_w = cw * 4 + gap * 3
    x0 = (Inches(13.333) - total_w) / 2
    for i, (name, head, func, kpi, color) in enumerate(centers):
        x = x0 + (cw + gap) * i
        # 竖线：主干到卡片
        line(s, x + cw/2, Inches(2.95), x + cw/2, y0,
             color=color, width=1.5)
        # 头
        rect(s, x, y0, cw, Inches(0.7), fill=color, border=None,
             text=name, text_size=13, text_bold=True, text_color=C_WHITE,
             rounded=False)
        # 负责人
        rect(s, x, y0 + Inches(0.7), cw, Inches(0.35),
             fill=C_GRAY_LT, border=color, border_w=1,
             text=head, text_size=10, text_color=color, text_bold=True)
        # 职能
        rect(s, x, y0 + Inches(1.05), cw, Inches(0.85),
             fill=C_WHITE, border=color, border_w=1,
             text=func, text_size=10, text_color=C_GRAY_D)
        # KPI
        rect(s, x, y0 + Inches(1.9), cw, Inches(0.55),
             fill=C_GRAY_LT, border=color, border_w=1,
             text="KPI\n" + kpi, text_size=9, text_color=color)

    # 现状部门"再定位"说明
    textbox(s, Inches(0.4), Inches(5.75), Inches(12.5), Inches(0.3),
            "现状部门的「再定位」（不是合并、不是裁撤）",
            size=12, bold=True, color=C_DARK)
    data = [
        ["流量部 → 增长中台", "独立站部 → 联合工作组", "独立站社区 → 内容中台",
         "APP 部 → 拆分：底层能力进 3 中台 · 业务协同进联合组",
         "APP 社区 → 内容中台", "会员部 → 用户资产中台"],
    ]
    # 6 个标签横排
    tags = data[0]
    tw = (Inches(12.5) - Inches(0.25)) / 6
    for i, tag in enumerate(tags):
        x = Inches(0.4) + (tw + Inches(0.05)) * i
        rect(s, x, Inches(6.1), tw, Inches(0.7),
             fill=C_GREEN_LT, border=C_GREEN, border_w=1, rounded=True,
             text=tag, text_size=9, text_color=C_GREEN_D, text_bold=True)

    # 底部
    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="统一目标 · 全局组织 · 高效协作 —— 正面回应现状图的「分散作战」",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ P11 预期成果 / KPI ============
def slide_11():
    s = new_slide()
    page_header(s, "预期成果 · 转化漏斗修复路径 + DTC 占比提升",
                subtitle="3 个月快赢 · 6 个月见效 · 12 个月质变",
                page=11)

    # 左：漏斗 Before/After 对比
    textbox(s, Inches(0.4), Inches(1.3), Inches(6), Inches(0.3),
            "转化漏斗 · 现状 → 12 个月后", size=13, bold=True, color=C_DARK)
    headers = ["环节", "现状", "12 月目标", "提升来源"]
    data = [
        ["Session Start", "20.3M", "22M+", "增长中台优化投放质量"],
        ["View Product", "42.0%", "45%", "落地页素材（内容中台）"],
        ["Add to Cart", "8.4% 🚨", "12% ✓", "APP 信任背书 + UGC 回灌"],
        ["Checkout", "43.9% 🚨", "52% ✓", "APP 一键登录 / 支付 / 地址"],
        ["Purchase", "41.6% 🚨", "55% ✓", "积分抵扣 + 会员价识别"],
        ["最终转化", "0.65%", "1.5%+", "整体 2.3x 提升"],
    ]
    row_fills = [C_WHITE, C_WHITE, C_RED_LT, C_RED_LT, C_RED_LT, C_GREEN_LT]
    table(s, Inches(0.4), Inches(1.7), Inches(6.2), Inches(3.3),
          data, headers=headers, header_fill=C_GREEN_D,
          first_col_bold=True, header_size=11, body_size=10,
          row_fills=row_fills,
          col_widths=[Inches(1.4), Inches(1.0), Inches(1.1), Inches(2.7)])

    # 右：DTC 占比提升阶段
    textbox(s, Inches(6.8), Inches(1.3), Inches(6), Inches(0.3),
            "DTC 占比提升 · 阶段路径（24 个月）",
            size=13, bold=True, color=C_DARK)
    stages = [
        ("阶段 1 · 基建", "0–3 月", "10% → 11%",
         "联合工作组立项 · 3 中台筹建 · One-ID 启动", C_BLUE),
        ("阶段 2 · 快赢", "3–6 月", "11% → 13%",
         "漏斗修复首轮 · Add-to-Cart 破 10%", C_ORANGE),
        ("阶段 3 · 协同", "6–12 月", "13% → 16%",
         "3 中台全运转 · APP 能力全量回灌独立站", C_PURPLE),
        ("阶段 4 · 放大", "12–24 月", "16% → 20%+",
         "AI Agent 全量驱动 · 站 / APP 深度融合", C_GREEN_D),
    ]
    sy = Inches(1.7); sh = Inches(0.82)
    for i, (name, period, ratio, body, color) in enumerate(stages):
        y = sy + (sh + Inches(0.05)) * i
        rect(s, Inches(6.8), y, Inches(1.2), sh, fill=color, border=None,
             text=name, text_size=11, text_bold=True, text_color=C_WHITE)
        rect(s, Inches(8.05), y, Inches(1.0), sh, fill=C_WHITE,
             border=color, border_w=1, text=period,
             text_size=10, text_color=color, text_bold=True)
        rect(s, Inches(9.1), y, Inches(1.3), sh, fill=C_GREEN_LT,
             border=color, border_w=1, text=ratio,
             text_size=12, text_bold=True, text_color=color)
        rect(s, Inches(10.45), y, Inches(2.45), sh, fill=C_WHITE,
             border=color, border_w=1, text=body,
             text_size=9.5, text_color=C_GRAY_D, text_align=PP_ALIGN.LEFT)

    # 底部核心信息
    rect(s, Inches(0.4), Inches(5.3), Inches(12.5), Inches(0.5),
         fill=C_ORANGE_LT, border=C_ORANGE, border_w=2, rounded=True,
         text="关键判断：这些提升不是「独立站更努力」就能得到 —— 必须靠 3 中台 + 联合工作组同步运行",
         text_size=13, text_bold=True, text_color=C_ORANGE)

    # 三大配套 KPI
    textbox(s, Inches(0.4), Inches(5.95), Inches(12.5), Inches(0.3),
            "三大中台各自的 Year 1 KPI 承诺",
            size=12, bold=True, color=C_DARK)
    kpis = [
        ["用户资产中台", "One-ID 打通率 ≥ 80% · 会员 GMV 渗透率 ≥ 50% · 复购 +25%"],
        ["内容中台", "双社区合并 · UGC 月产 +200% · 内容驱动转化率 +15%"],
        ["增长中台", "CAC -15~20% · 归因覆盖 ≥ 90% · AB 频次 ≥ 50/季"],
    ]
    table(s, Inches(0.4), Inches(6.3), Inches(12.5), Inches(0.85),
          kpis, headers=None, first_col_bold=True, body_size=10,
          row_fills=[C_RED_LT, C_BLUE_LT, C_ORANGE_LT],
          col_widths=[Inches(2.5), Inches(10.0)])
    page_footer(s)

# ============ P12 下一步 / 待决议题 ============
def slide_12():
    s = new_slide()
    page_header(s, "下一步 · 三个待决议题",
                subtitle="本次汇报期待创始人与高管团队在以下 3 个议题上形成共识",
                page=12)

    items = [
        ("01", "方向决议",
         "是否将「3 中台 + 1 联合工作组」列入 2026 DTC 战略重点？",
         "本月", "创始人 / 战略委员会", C_GREEN_D),
        ("02", "人选讨论",
         "三个中台 Head + 联合工作组 Head 人选如何确定？\n（内部竞聘 + 外部招募 · APP 事业部内部储备）",
         "1 个月内", "创始人 + HR", C_ORANGE),
        ("03", "过渡期方案",
         "90 天过渡期：组织切换、KPI 双轨、首战验证\n（联合工作组 3 个月内出转化漏斗修复首战果）",
         "2 个月内", "候选 Leader + HR", C_BLUE),
    ]
    y0 = Inches(1.4); h = Inches(1.65)
    for i, (n, title, body, when, who, color) in enumerate(items):
        y = y0 + (h + Inches(0.15)) * i
        # 编号圆
        oval(s, Inches(0.4), y + Inches(0.3), Inches(1.0), Inches(1.0),
             fill=color, border=None, text=n, text_size=26,
             text_color=C_WHITE, text_bold=True)
        # 主卡
        box = rect(s, Inches(1.6), y, Inches(8.8), h,
                   fill=C_WHITE, border=color, border_w=2, rounded=True)
        tf = box.text_frame
        tf.margin_left=Pt(16); tf.margin_right=Pt(16); tf.margin_top=Pt(12)
        tf.word_wrap=True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title
        r.font.size = Pt(15); r.font.bold = True
        r.font.color.rgb = color; r.font.name = FONT
        add_para(tf, body, size=11.5, color=C_GRAY_D, space_before=6)
        # 右侧 when + who
        rect(s, Inches(10.55), y, Inches(2.35), h/2 - Inches(0.05),
             fill=C_GRAY_LT, border=color, border_w=1, rounded=True,
             text=f"⏰  {when}", text_size=11, text_bold=True,
             text_color=color)
        rect(s, Inches(10.55), y + h/2 + Inches(0.05),
             Inches(2.35), h/2 - Inches(0.05),
             fill=C_GRAY_LT, border=color, border_w=1, rounded=True,
             text=f"👤  {who}", text_size=11, text_bold=True,
             text_color=color)

    # 底部
    rect(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.35),
         fill=C_GREEN_D, border=None, rounded=True,
         text="立场诚恳 · 提案中立 · 只为公司战略做对的事 —— 期待讨论",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ 封底 ============
def slide_back():
    s = new_slide(C_GREEN_D)
    rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.18),
         fill=C_ORANGE, border=None)
    textbox(s, Inches(1), Inches(2.3), Inches(11.3), Inches(0.5),
            "汇报结束", size=16, italic=True, color=C_ORANGE_LT,
            align=PP_ALIGN.CENTER)
    textbox(s, Inches(1), Inches(3.0), Inches(11.3), Inches(1.5),
            "期待讨论", size=52, bold=True, color=C_WHITE,
            align=PP_ALIGN.CENTER)
    rect(s, Inches(5.67), Inches(4.8), Inches(2), Inches(0.03),
         fill=C_ORANGE, border=None)
    # 三个核心议题
    textbox(s, Inches(1), Inches(5.0), Inches(11.3), Inches(0.4),
            "① 3 中台 + 1 联合工作组 是否列入战略重点", size=13,
            color=C_GREEN_LT, align=PP_ALIGN.CENTER)
    textbox(s, Inches(1), Inches(5.4), Inches(11.3), Inches(0.4),
            "② 中台 / 联合组 Head 人选", size=13,
            color=C_GREEN_LT, align=PP_ALIGN.CENTER)
    textbox(s, Inches(1), Inches(5.8), Inches(11.3), Inches(0.4),
            "③ 90 天过渡期方案", size=13,
            color=C_GREEN_LT, align=PP_ALIGN.CENTER)
    # 签名
    textbox(s, Inches(1), Inches(6.8), Inches(11.3), Inches(0.4),
            "APP 事业部  ·  代表「用户视角 + 全局视角」  ·  2026/05/12",
            size=11, color=RGBColor(0xC8,0xE6,0xC9), align=PP_ALIGN.CENTER,
            italic=True)

# ==================================================================
#                                 BUILD
# ==================================================================
def build():
    slide_cover()
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    slide_5()
    slide_6()
    slide_7()
    slide_8()
    slide_9()
    slide_10()
    slide_11()
    slide_12()
    slide_back()
    prs.save(OUT_PATH)
    print(f"✅ Generated: {OUT_PATH}")
    print(f"   Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    build()
