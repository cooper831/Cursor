#!/usr/bin/env python3
"""
Momcozy DTC 大部门战略提案 v2 —— PPT 生成脚本（原生可编辑）

- 基于 /Users/lute/AI/Cursor/DTC/DTC大部门战略提案_v2.md
- 16:9 画布（13.333 x 7.5 inch）
- 每个元素都是 python-pptx 原生 shape / table / textbox，可在 Keynote / PPT 内任意编辑
- 立场：APP 事业部代表「用户视角 + 全局视角」，中立、克制、数据驱动
- 配色：以蓝色（专业）为主，红色仅用于关键数字和痛点强调
- 输出：/Users/lute/AI/Cursor/DTC/DTC大部门战略提案_v2.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# ====================== 配色 ======================
# 主色：蓝（专业中立） / 红（关键痛点） / 绿（机会） / 紫（数据/AI）
C_BLUE      = RGBColor(0x1F, 0x4E, 0x79)   # 深蓝（主色）
C_BLUE_MID  = RGBColor(0x2E, 0x75, 0xB6)   # 中蓝
C_BLUE_LT   = RGBColor(0xDE, 0xEB, 0xF7)   # 浅蓝
C_RED       = RGBColor(0xC0, 0x3A, 0x2B)   # 深红（痛点/关键）
C_RED_LT    = RGBColor(0xFB, 0xE5, 0xE1)   # 浅红
C_GREEN     = RGBColor(0x38, 0x76, 0x1D)   # 深绿（机会）
C_GREEN_LT  = RGBColor(0xE2, 0xEF, 0xDA)   # 浅绿
C_ORANGE    = RGBColor(0xD9, 0x7B, 0x1F)   # 橙（数据/强调）
C_ORANGE_LT = RGBColor(0xFC, 0xE4, 0xC7)   # 浅橙
C_PURPLE    = RGBColor(0x5B, 0x2E, 0x8A)   # 紫（AI/数据）
C_PURPLE_LT = RGBColor(0xE8, 0xDE, 0xF0)
C_DARK      = RGBColor(0x1A, 0x1A, 0x1A)
C_GRAY_D    = RGBColor(0x33, 0x33, 0x33)
C_GRAY      = RGBColor(0x66, 0x66, 0x66)
C_GRAY_LT   = RGBColor(0xF2, 0xF2, 0xF2)
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "PingFang SC"
OUT_PATH = "/Users/lute/AI/Cursor/DTC/DTC大部门战略提案_v2.pptx"

# ====================== 初始化 ======================
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

TOTAL_PAGES = 13  # Cover + 10 内容 + 总结 + Back

# ====================== 通用辅助函数 ======================
def new_slide(bg=C_WHITE):
    s = prs.slides.add_slide(BLANK)
    b = s.background; b.fill.solid(); b.fill.fore_color.rgb = bg
    return s

def textbox(slide, left, top, width, height, text, *, size=14, bold=False,
            color=C_GRAY_D, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
            fill=None, border=None, border_w=1, font=FONT, italic=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    if fill:
        box.fill.solid(); box.fill.fore_color.rgb = fill
    else:
        box.fill.background()
    if border:
        box.line.color.rgb = border; box.line.width = Pt(border_w)
    else:
        box.line.fill.background()
    tf = box.text_frame
    tf.margin_left = Pt(6); tf.margin_right = Pt(6)
    tf.margin_top  = Pt(3); tf.margin_bottom = Pt(3)
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
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if border is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = border; s.line.width = Pt(border_w)
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
         border_w=1, text="", text_size=14, text_color=C_GRAY_D,
         text_bold=False):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, width, height)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if border is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = border; s.line.width = Pt(border_w)
    s.shadow.inherit = False
    if text:
        tf = s.text_frame
        tf.margin_left = Pt(3); tf.margin_right = Pt(3)
        tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = text
        r.font.size = Pt(text_size); r.font.bold = text_bold
        r.font.color.rgb = text_color; r.font.name = FONT
    return s

def line(slide, x1, y1, x2, y2, *, color=C_GRAY, width=1.5):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb = color; c.line.width = Pt(width)
    return c

def arrow(slide, left, top, width, height, *, fill=C_ORANGE,
          direction="right"):
    shape_map = {
        "right": MSO_SHAPE.RIGHT_ARROW,
        "down": MSO_SHAPE.DOWN_ARROW,
    }
    s = slide.shapes.add_shape(shape_map[direction], left, top, width, height)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.fill.background()
    return s

def table(slide, left, top, width, height, data, *, headers=None,
          header_fill=C_BLUE, header_color=C_WHITE, row_fills=None,
          header_size=12, body_size=11, first_col_bold=False,
          col_widths=None):
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
        cell.margin_top  = Pt(4); cell.margin_bottom = Pt(4)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if fill:
            cell.fill.solid(); cell.fill.fore_color.rgb = fill
        tf = cell.text_frame; tf.word_wrap = True; tf.clear()
        p = tf.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = str(text) if text is not None else ""
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = FONT

    if headers:
        for j, h in enumerate(headers):
            set_cell(tbl.cell(0, j), h, size=header_size, bold=True,
                     color=header_color, fill=header_fill,
                     align=PP_ALIGN.CENTER)
    for i, row in enumerate(data):
        row_i = i + (1 if headers else 0)
        rfill = row_fills[i] if row_fills and i < len(row_fills) else None
        for j, cell_text in enumerate(row):
            b = first_col_bold and j == 0
            set_cell(tbl.cell(row_i, j), cell_text, size=body_size,
                     bold=b, fill=rfill)
    return tbl

def page_header(slide, title, *, subtitle=None, page=None, part=None):
    """顶部蓝条 + 品牌 + 页码 + 主副标题"""
    rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.1),
         fill=C_BLUE, border=None)
    textbox(slide, Inches(0.4), Inches(0.18), Inches(6), Inches(0.3),
            "MOMCOZY  DTC 大部门战略提案 · v2", size=10, bold=True,
            color=C_BLUE)
    if page is not None:
        txt = f"Part {part} · {page}/{TOTAL_PAGES}" if part else f"{page}/{TOTAL_PAGES}"
        textbox(slide, Inches(7.5), Inches(0.18), Inches(5.4), Inches(0.3),
                txt, size=10, color=C_GRAY, align=PP_ALIGN.RIGHT)
    textbox(slide, Inches(0.4), Inches(0.55), Inches(12.5), Inches(0.7),
            title, size=26, bold=True, color=C_DARK)
    if subtitle:
        textbox(slide, Inches(0.4), Inches(1.25), Inches(12.5), Inches(0.5),
                subtitle, size=13, italic=True, color=C_GRAY)
        return Inches(1.85)
    return Inches(1.5)

def page_footer(slide, text="APP 事业部 · 代表「用户视角 + 全局视角」 · 2026/05/11"):
    textbox(slide, Inches(0.4), Inches(7.15), Inches(12.5), Inches(0.3),
            text, size=9, color=C_GRAY, align=PP_ALIGN.RIGHT, italic=True)

# ==================================================================
#                              页面设计
# ==================================================================

# ============ 封面 ============
def slide_cover():
    s = new_slide(C_BLUE)
    rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.18),
         fill=C_ORANGE, border=None)
    # 左侧装饰竖条
    rect(s, Inches(0.8), Inches(2.3), Inches(0.1), Inches(3.2),
         fill=C_ORANGE, border=None)
    # 主标题
    textbox(s, Inches(1.2), Inches(2.1), Inches(11), Inches(1.0),
            "Momcozy DTC 大部门战略提案", size=42, bold=True, color=C_WHITE)
    # 版本号
    rect(s, Inches(1.2), Inches(3.0), Inches(0.9), Inches(0.4),
         fill=C_ORANGE, border=None, text="v2", text_size=18,
         text_bold=True, text_color=C_WHITE, rounded=True)
    # 副标题
    textbox(s, Inches(1.2), Inches(3.55), Inches(11), Inches(0.7),
            "站在公司全局视角 · 分析 DTC 整合的战略价值与组织优化建议",
            size=18, color=C_BLUE_LT, italic=True)
    # 逻辑链
    textbox(s, Inches(1.2), Inches(4.7), Inches(11), Inches(0.5),
            "行业趋势  →  现状问题  →  目标拆解  →  解决方案",
            size=14, color=C_WHITE, bold=True)
    # 分隔
    rect(s, Inches(1.2), Inches(5.5), Inches(3), Inches(0.03),
         fill=C_ORANGE, border=None)
    # 汇报信息
    _, tf = textbox(s, Inches(1.2), Inches(5.7), Inches(11), Inches(1.5),
                    "汇报人：APP 事业部", size=13, color=C_WHITE)
    add_para(tf, "汇报对象：创始人 / 高管团队", size=13, color=C_WHITE,
             space_before=4)
    add_para(tf, "核心立场：不代表 APP 部门利益，代表「用户视角」与「公司全局视角」",
             size=12, italic=True, color=C_ORANGE_LT, space_before=8)
    # 日期
    textbox(s, Inches(1.2), Inches(6.9), Inches(11), Inches(0.3),
            "2026/05/11", size=11, color=C_GRAY_LT)

# ============ Slide 0 · 开篇立场 + 逻辑链 ============
def slide_opening():
    s = new_slide()
    page_header(s, "开篇 · 本次汇报的立场与逻辑",
                subtitle="不为部门发言 · 为公司全局发言",
                page=1)
    # 立场（大字）
    box = rect(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(1.4),
               fill=C_BLUE_LT, border=C_BLUE, border_w=2, rounded=True)
    tf = box.text_frame
    tf.margin_left = Pt(24); tf.margin_right = Pt(24)
    tf.margin_top = Pt(12); tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "立场"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_BLUE; r.font.name = FONT
    add_para(tf, "我作为 APP 事业部负责人提出这个方案 ——",
             size=16, bold=True, color=C_DARK, space_before=6)
    add_para(tf, "不代表 APP 部门利益，代表「用户视角」与「公司全局视角」。",
             size=18, bold=True, color=C_BLUE, space_before=4)

    # 逻辑链（四步流程）
    textbox(s, Inches(0.4), Inches(3.6), Inches(12.5), Inches(0.4),
            "汇报逻辑链", size=14, bold=True, color=C_DARK)
    steps = [
        ("① 行业趋势", "为什么必须做", C_BLUE),
        ("② 现状问题", "为什么现在做", C_RED),
        ("③ 目标拆解", "做到什么程度", C_ORANGE),
        ("④ 解决方案", "怎么做", C_GREEN),
    ]
    x0 = Inches(0.4); w = Inches(2.9); gap = Inches(0.15); y = Inches(4.2)
    for i, (title, desc, color) in enumerate(steps):
        x = x0 + (w + gap) * i
        # 主卡片
        rect(s, x, y, w, Inches(0.7), fill=color, border=None,
             text=title, text_size=15, text_bold=True, text_color=C_WHITE,
             rounded=True)
        rect(s, x, y + Inches(0.75), w, Inches(0.7), fill=C_WHITE,
             border=color, border_w=1, text=desc, text_size=13,
             text_color=C_DARK, rounded=True)
        # 连接箭头
        if i < 3:
            ax = x + w + Inches(0.005)
            arrow(s, ax, y + Inches(0.4), gap - Inches(0.01),
                  Inches(0.35), fill=C_ORANGE)

    # 涵盖的 4 部分 × 8 Slide 一览
    textbox(s, Inches(0.4), Inches(5.9), Inches(12.5), Inches(0.4),
            "对应的 4 个部分 · 8 个核心 Slide",
            size=13, bold=True, color=C_DARK)
    data_map = [
        ["第一部分 · 战略势能", "Slide 1 范式转移", "Slide 2 DTC 本质"],
        ["第二部分 · 现状剖析", "Slide 3 业务全景图", "Slide 4 三大隐形成本"],
        ["第三部分 · 目标设定", "Slide 5 北极星 + 增长公式", "Slide 6 效率提升测算"],
        ["第四部分 · 解决方案", "Slide 7 组织架构（中台+Pod+Squad）", "Slide 8 资源统筹与决策"],
    ]
    table(s, Inches(0.4), Inches(6.35), Inches(12.5), Inches(0.75),
          data_map, headers=None, first_col_bold=True,
          body_size=10, header_size=10,
          row_fills=[C_BLUE_LT, C_RED_LT, C_ORANGE_LT, C_GREEN_LT],
          col_widths=[Inches(3.0), Inches(4.8), Inches(4.7)])
    page_footer(s)

# ============ Slide 1 · 全球品牌出海的范式转移 ============
def slide_1():
    s = new_slide()
    page_header(s, "Slide 1 · 全球品牌出海的范式转移",
                subtitle="从「渠道思维」到「品牌思维」 · DTC 占比已成品牌力核心指标",
                page=2, part="I")

    # 上下半场对照表
    textbox(s, Inches(0.4), Inches(1.95), Inches(6), Inches(0.35),
            "范式对比：上半场 vs 下半场", size=13, bold=True, color=C_DARK)
    data = [
        ["核心战场", "Amazon / 第三方平台", "DTC 独立站 + APP + 私域"],
        ["用户关系", "平台的用户，品牌「租用」", "品牌的用户，沉淀为资产"],
        ["核心指标", "GMV、广告 ROI", "LTV、复购率、NPS"],
        ["竞争壁垒", "流量 + 供应链", "品牌 + 用户资产 + 数据"],
        ["估值逻辑", "PE 8–15x", "PE 25–40x（DTC 品牌溢价）"],
    ]
    table(s, Inches(0.4), Inches(2.35), Inches(6.2), Inches(3.2),
          data, headers=["维度", "上半场  2015-2022", "下半场  2023+"],
          header_fill=C_BLUE, first_col_bold=True,
          header_size=11, body_size=10,
          row_fills=[C_GRAY_LT, C_WHITE, C_GRAY_LT, C_WHITE, C_RED_LT],
          col_widths=[Inches(1.2), Inches(2.4), Inches(2.6)])

    # 行业标杆对标
    textbox(s, Inches(6.8), Inches(1.95), Inches(6.1), Inches(0.35),
            "行业标杆 DTC 占比对标", size=13, bold=True, color=C_DARK)
    data2 = [
        ["拓竹 Bambu Lab", "~50%", "用户社区 + 独立站 + APP 三位一体"],
        ["大疆 DJI", "~38%", "旗舰店 + APP + 会员体系闭环"],
        ["Anker 安克", "~35%", "强 DTC 投入，独立站 + 品牌站矩阵"],
        ["SHARGE 闪极", "~40%+", "独立站 + APP + 社区一体化"],
        ["Momcozy 当前", "~10%", "显著低于头部品牌，存在 3–4x 提升空间"],
    ]
    table(s, Inches(6.8), Inches(2.35), Inches(6.1), Inches(3.2),
          data2, headers=["品牌", "DTC 占比", "启示"],
          header_fill=C_BLUE, first_col_bold=True,
          header_size=11, body_size=10,
          row_fills=[C_GRAY_LT, C_WHITE, C_GRAY_LT, C_WHITE, C_RED_LT],
          col_widths=[Inches(1.8), Inches(1.2), Inches(3.1)])

    # 关键数字大字板
    rect(s, Inches(0.4), Inches(5.75), Inches(12.5), Inches(0.8),
         fill=C_RED_LT, border=C_RED, border_w=2, rounded=True)
    textbox(s, Inches(0.6), Inches(5.8), Inches(4.5), Inches(0.7),
            "关键差距", size=11, bold=True, color=C_RED)
    textbox(s, Inches(0.6), Inches(6.0), Inches(4.5), Inches(0.5),
            "10% → 20%", size=32, bold=True, color=C_RED)
    textbox(s, Inches(5.0), Inches(5.85), Inches(7.7), Inches(0.7),
            "24 个月内，DTC 占比从 ~10% 提升至 20%",
            size=14, bold=True, color=C_DARK)
    textbox(s, Inches(5.0), Inches(6.22), Inches(7.7), Inches(0.4),
            "这不是「高目标」——是出海品牌进入第二梯队的入场券",
            size=11, italic=True, color=C_GRAY_D)

    # 核心信息
    rect(s, Inches(0.4), Inches(6.7), Inches(12.5), Inches(0.4),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板的核心信息：DTC 占比 = 品牌资产健康度",
         text_size=12, text_bold=True, text_color=C_BLUE)
    page_footer(s)

# ============ Slide 2 · DTC 的本质 ============
def slide_2():
    s = new_slide()
    page_header(s, "Slide 2 · DTC 的本质 · 品牌护城河与用户资产",
                subtitle="DTC ≠ 一个销售渠道 · DTC = 品牌的用户资产运营中心",
                page=3, part="I")

    # 重新定义 block
    box = rect(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(0.9),
               fill=C_BLUE_LT, border=C_BLUE, border_w=2, rounded=True)
    tf = box.text_frame
    tf.margin_left = Pt(20); tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "重新定义 DTC：　"
    r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_BLUE
    r.font.name = FONT
    r2 = p.add_run(); r2.text = "DTC ≠ 销售渠道"
    r2.font.size = Pt(16); r2.font.bold = True; r2.font.color.rgb = C_GRAY
    r2.font.name = FONT
    r3 = p.add_run(); r3.text = "　·　"
    r3.font.size = Pt(14); r3.font.color.rgb = C_GRAY
    r4 = p.add_run(); r4.text = "DTC = 品牌的用户资产运营中心"
    r4.font.size = Pt(18); r4.font.bold = True; r4.font.color.rgb = C_RED
    r4.font.name = FONT

    # 三个本质价值（并列卡片）
    textbox(s, Inches(0.4), Inches(3.0), Inches(12.5), Inches(0.4),
            "三个本质价值", size=14, bold=True, color=C_DARK)

    values = [
        ("价值 1 · First-party Data",
         "AI 时代唯一的护城河",
         C_PURPLE, C_PURPLE_LT,
         "平台数据：用户属于平台，品牌「借用」",
         "DTC 数据：用户行为 / 偏好 / 生命周期阶段",
         "—— 这是 2026 AI Agent 战略的唯一弹药",
         "没有 DTC 数据闭环\nAI 投入无法兑现价值"),
        ("价值 2 · LTV > GMV",
         "LTV 取代 GMV 成为北极星",
         C_BLUE, C_BLUE_LT,
         "平台思维：单次 GMV、ROAS",
         "DTC 思维：24 月 LTV、复购率",
         "—— 当 LTV 被准确度量，CAC 天花板就被打开",
         "这是 DTC 品牌跑得过\n平台品牌的根本原因"),
        ("价值 3 · 估值溢价",
         "品牌溢价的资本市场定价",
         C_ORANGE, C_ORANGE_LT,
         "DTC 占比 +10% → 估值乘数 +1.5–2x",
         "参考：Anker / 安踏 / Lululemon 上市估值逻辑",
         "—— DTC 不只是利润中心",
         "是未来融资 / 上市的\n估值基础"),
    ]
    x0 = Inches(0.4); w = Inches(4.05); gap = Inches(0.15); y = Inches(3.45)
    h = Inches(3.3)
    for i, (name, sub, color, color_lt, p1, p2, p3, highlight) in enumerate(values):
        x = x0 + (w + gap) * i
        # 头
        rect(s, x, y, w, Inches(0.55), fill=color, border=None,
             text=name, text_size=13, text_bold=True, text_color=C_WHITE)
        # 副标
        rect(s, x, y + Inches(0.55), w, Inches(0.45), fill=color_lt,
             border=color, border_w=1, text=sub, text_size=12,
             text_bold=True, text_color=color)
        # 正文
        box = rect(s, x, y + Inches(1.05), w, h - Inches(1.05),
                   fill=C_WHITE, border=color, border_w=1)
        tf = box.text_frame
        tf.margin_left = Pt(12); tf.margin_right = Pt(12)
        tf.margin_top = Pt(10); tf.word_wrap = True
        add_para(tf, p1, size=10, color=C_GRAY_D, space_before=0,
                 bullet=True)
        add_para(tf, p2, size=10, color=C_GRAY_D, space_before=6,
                 bullet=True)
        add_para(tf, p3, size=10, italic=True, color=color,
                 space_before=8, bold=True)
        # 关键洞察
        rect(s, x + Inches(0.15), y + h - Inches(1.0),
             w - Inches(0.3), Inches(0.9),
             fill=color_lt, border=None, text=highlight, text_size=10.5,
             text_bold=True, text_color=color, text_align=PP_ALIGN.CENTER)

    # 核心信息
    rect(s, Inches(0.4), Inches(6.9), Inches(12.5), Inches(0.4),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板的核心信息：DTC 不是一个部门的事 —— 是 Momcozy 从「母婴品牌」升级为「用户资产平台」的战略基础设施",
         text_size=12, text_bold=True, text_color=C_BLUE)
    page_footer(s)

# ============ Slide 3 · 当前业务全景图 ============
def slide_3():
    s = new_slide()
    page_header(s, "Slide 3 · 当前业务全景图 · 中立呈现",
                subtitle="问题不在于「谁做得不好」 · 而在于「组织结构与业务本质不匹配」",
                page=4, part="II")

    # 用户生命周期 + 当前组织切割
    rect(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(0.45),
         fill=C_BLUE, border=None,
         text="用户全生命周期：认知 → 兴趣 → 首购 → 使用 → 复购 → 忠诚 → 推荐",
         text_size=13, text_bold=True, text_color=C_WHITE)
    # 用户旅程阶段（7 段）
    stages = ["认知", "兴趣", "首购", "使用", "复购", "忠诚", "推荐"]
    sw = Inches(12.5) / 7; sy = Inches(2.4); sh = Inches(0.4)
    for i, stage in enumerate(stages):
        rect(s, Inches(0.4) + sw * i, sy, sw - Inches(0.03), sh,
             fill=C_BLUE_LT, border=C_BLUE, border_w=1,
             text=stage, text_size=11, text_bold=True, text_color=C_BLUE)

    # 当前部门切割
    textbox(s, Inches(0.4), Inches(2.95), Inches(12.5), Inches(0.3),
            "当前组织切割（按触点 · 非按旅程）",
            size=12, bold=True, color=C_RED)
    depts = [
        ("流量部", "认知-兴趣", C_ORANGE),
        ("独立站部", "兴趣-首购", C_BLUE_MID),
        ("独立站社区", "首购-使用", C_BLUE_MID),
        ("APP 部\n（含 APP 社区）", "使用-复购-忠诚", C_PURPLE),
        ("会员部", "复购-忠诚", C_GREEN),
    ]
    dw = Inches(12.5) / 5; dy = Inches(3.3); dh = Inches(0.85)
    for i, (name, cover, color) in enumerate(depts):
        x = Inches(0.4) + dw * i
        rect(s, x + Inches(0.05), dy, dw - Inches(0.1), dh,
             fill=color, border=None, text=name, text_size=11,
             text_bold=True, text_color=C_WHITE, rounded=True)
        textbox(s, x + Inches(0.05), dy + dh + Inches(0.05),
                dw - Inches(0.1), Inches(0.25),
                f"触点：{cover}", size=9, color=C_GRAY,
                align=PP_ALIGN.CENTER, italic=True)

    # 各部门表现（中立陈述）
    textbox(s, Inches(0.4), Inches(4.75), Inches(12.5), Inches(0.3),
            "中立判断：各部门在各自领域表现优秀",
            size=12, bold=True, color=C_DARK)
    data = [
        ["流量部", "SEM / SEO / 红人投放经验丰富，CAC 控制在行业合理水平"],
        ["独立站部", "站点 UX、转化漏斗持续优化，独立站社区已积累内容"],
        ["APP 部", "已升级为生态平台（IoT + AI + 社区 + 商城 + 会员），陪伴属性强"],
        ["会员部", "会员体系成型，私域召回能力建立"],
    ]
    table(s, Inches(0.4), Inches(5.1), Inches(7), Inches(1.55),
          data, headers=["部门", "优势 / 成果（事实陈述）"],
          header_fill=C_GREEN, first_col_bold=True,
          header_size=11, body_size=10,
          row_fills=[C_GREEN_LT, C_WHITE, C_GREEN_LT, C_WHITE],
          col_widths=[Inches(1.2), Inches(5.8)])

    # 局部 vs 全局
    box = rect(s, Inches(7.6), Inches(5.1), Inches(5.3), Inches(1.55),
               fill=C_RED_LT, border=C_RED, border_w=2, rounded=True)
    tf = box.text_frame
    tf.margin_left = Pt(14); tf.margin_right = Pt(14)
    tf.margin_top = Pt(10); tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "但缺乏「全局最优解」"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_RED; r.font.name = FONT
    add_para(tf, "业务本质：一个用户的「全生命周期」",
             size=10, color=C_GRAY_D, space_before=6, bullet=True)
    add_para(tf, "组织现状：切成 4 段，每段背独立 KPI",
             size=10, color=C_GRAY_D, space_before=3, bullet=True)
    add_para(tf, "必然结果：局部最优 ≠ 全局最优",
             size=11, color=C_RED, space_before=6, bold=True)

    # 核心信息
    rect(s, Inches(0.4), Inches(6.8), Inches(12.5), Inches(0.4),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板：这不是「批评谁」的汇报 —— 是「当业务规模到某个阶段，组织结构必须升级」的汇报",
         text_size=12, text_bold=True, text_color=C_BLUE)
    page_footer(s)

# ============ Slide 4 · 三大隐形成本 ============
def slide_4():
    s = new_slide()
    page_header(s, "Slide 4 · 三大隐形成本 · 散兵作战的代价",
                subtitle="体验割裂 · 资源浪费 · 决策延迟 —— 都指向同一个组织问题",
                page=5, part="II")

    pains = [
        ("痛点 1 · 体验割裂", "用户流失风险", C_RED,
         [("事实", "用户在独立站 ID-A / APP ID-B / 会员系统 ID-C ——\n会员等级、成长值、黑卡身份互不互通"),
          ("典型", "APP 累计消费 $800 的用户，回独立站仍按「新客」对待\n—— 用户反馈：「是不是两个品牌？」"),
          ("隐形成本", "ID 打通率 < 30% · NPS 受损 · 高价值用户流失")]),
        ("痛点 2 · 资源浪费", "CAC 被内部抬升", C_ORANGE,
         [("事实", "流量部买「baby bottle」 · APP 部买「baby tracker」\n两个关键词在 Google Ads 后台互相竞价"),
          ("典型", "2025 Q4 某月，独立站与 APP 在 Meta 投放受众重合 40%+\n单次拉新成本环比 +18%（内部抢量造成）"),
          ("隐形成本", "预算利用率 -15~20% · 不是市场没人，是我们自己挤自己")]),
        ("痛点 3 · 决策延迟", "错失市场窗口", C_PURPLE,
         [("事实", "一个大促需协调 4 个部门（流量 + 独立站 + APP + 会员）\n决策周期 10–14 天"),
          ("典型", "2025 黑五：立项到上线 11 天 · APP 资源位排期冲突延期 3 天\n最终 ROI 比预期低 22%"),
          ("隐形成本", "大促筹备期被内部流程吃掉 40% 时间 · 各打各的")]),
    ]
    x0 = Inches(0.4); w = Inches(4.05); gap = Inches(0.15); y = Inches(1.9)
    for i, (name, sub, color, items) in enumerate(pains):
        x = x0 + (w + gap) * i
        # 顶部编号
        rect(s, x, y, w, Inches(0.5), fill=color, border=None,
             text=name, text_size=13, text_bold=True, text_color=C_WHITE)
        rect(s, x, y + Inches(0.5), w, Inches(0.45),
             fill=C_WHITE, border=color, border_w=1,
             text=f"→  {sub}", text_size=12, text_bold=True,
             text_color=color)
        # 主体卡片
        box = rect(s, x, y + Inches(1.0), w, Inches(3.4),
                   fill=C_WHITE, border=color, border_w=1)
        tf = box.text_frame
        tf.margin_left = Pt(10); tf.margin_right = Pt(10)
        tf.margin_top = Pt(8); tf.word_wrap = True
        for j, (label, body) in enumerate(items):
            if j == 0:
                p = tf.paragraphs[0]
                r = p.add_run(); r.text = f"● {label}"
                r.font.size = Pt(11); r.font.bold = True
                r.font.color.rgb = color; r.font.name = FONT
            else:
                add_para(tf, f"● {label}", size=11, bold=True,
                         color=color, space_before=10)
            add_para(tf, body, size=9.5, color=C_GRAY_D, space_before=2)

    # 本质归因表
    textbox(s, Inches(0.4), Inches(5.5), Inches(12.5), Inches(0.3),
            "三大痛点的本质归因（回到同一个根因）",
            size=13, bold=True, color=C_DARK)
    data = [
        ["体验割裂", "系统没打通", "没有 One-ID 战略的组织主体"],
        ["资源浪费", "投放重复", "预算按部门切，不按 LTV 切"],
        ["决策延迟", "协作慢", "战役指挥权分散在 4 个部门"],
    ]
    table(s, Inches(0.4), Inches(5.85), Inches(12.5), Inches(1.1), data,
          headers=["痛点", "表面问题", "本质问题"],
          header_fill=C_DARK, first_col_bold=True,
          header_size=11, body_size=10.5,
          row_fills=[C_RED_LT, C_RED_LT, C_RED_LT],
          col_widths=[Inches(2.0), Inches(3.5), Inches(7.0)])

    # 核心信息
    rect(s, Inches(0.4), Inches(7.0), Inches(12.5), Inches(0.35),
         fill=C_RED, border=None, rounded=True,
         text="给老板：三大痛点的根因都指向同一个问题 —— 组织没有「全局指挥官」",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ Slide 5 · 北极星目标 + 增长公式 ============
def slide_5():
    s = new_slide()
    page_header(s, "Slide 5 · 北极星目标 · 20% 的增长公式",
                subtitle="24 个月内 DTC 占比从 ~10% → 20% · 四个杠杆同时拉动",
                page=6, part="III")

    # 北极星大字板
    nb = rect(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(1.2),
              fill=C_RED_LT, border=C_RED, border_w=2, rounded=True)
    tf = nb.text_frame
    tf.margin_left = Pt(20); tf.margin_right = Pt(20)
    tf.margin_top = Pt(10); tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "北极星目标（North Star Metric）"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_RED; r.font.name = FONT
    add_para(tf,
             "将 Momcozy 的 DTC 占比从 ~10% 提升至 20%（24 个月内）",
             size=19, bold=True, color=C_DARK, space_before=6)
    add_para(tf,
             "这不是靠「独立站更努力」达成 —— 是靠「四个杠杆同时拉动」达成",
             size=12, italic=True, color=C_GRAY_D, space_before=4)

    # 增长公式
    textbox(s, Inches(0.4), Inches(3.25), Inches(6.5), Inches(0.35),
            "增长公式（DTC GMV 拆解）", size=13, bold=True, color=C_DARK)
    formula_y = Inches(3.65)
    parts = [
        ("新客", "增长中台", C_ORANGE),
        ("首购 ARPU", "首购 Pod", C_BLUE_MID),
        ("(1 + 复购)", "留存 Pod", C_PURPLE),
        ("留存率", "生态 Pod", C_GREEN),
    ]
    pw = Inches(1.4); pgap = Inches(0.18); px0 = Inches(0.5)
    # DTC GMV =
    textbox(s, px0, formula_y + Inches(0.1), Inches(0.8), Inches(0.5),
            "DTC GMV =", size=12, bold=True, color=C_DARK,
            anchor=MSO_ANCHOR.MIDDLE)
    for i, (t, pod, color) in enumerate(parts):
        x = px0 + Inches(0.9) + (pw + pgap) * i
        rect(s, x, formula_y, pw, Inches(0.6), fill=color, border=None,
             text=t, text_size=13, text_bold=True, text_color=C_WHITE,
             rounded=True)
        textbox(s, x, formula_y + Inches(0.62), pw, Inches(0.3),
                pod, size=9, color=color, italic=True,
                align=PP_ALIGN.CENTER, bold=True)
        if i < 3:
            textbox(s, x + pw, formula_y + Inches(0.1),
                    pgap, Inches(0.5),
                    "×", size=15, bold=True, color=C_GRAY,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # 三条增长曲线
    textbox(s, Inches(0.4), Inches(4.7), Inches(6.5), Inches(0.3),
            "三条增长曲线（24 个月路径）",
            size=12, bold=True, color=C_DARK)
    data_curve = [
        ["基建期", "0–6 月", "10% → 12%", "One-ID 打通 · 组织整合落地"],
        ["协同期", "6–12 月", "12% → 16%", "战役制跑通 · UGC 反哺独立站"],
        ["放大期", "12–24 月", "16% → 20%+", "APP 生态价值释放 · AI Agent 驱动复购"],
    ]
    table(s, Inches(0.4), Inches(5.05), Inches(6.5), Inches(1.4),
          data_curve, headers=["阶段", "时间", "DTC 占比", "核心动作"],
          header_fill=C_BLUE, first_col_bold=True,
          header_size=10, body_size=9.5,
          row_fills=[C_BLUE_LT, C_ORANGE_LT, C_GREEN_LT],
          col_widths=[Inches(1.0), Inches(1.0), Inches(1.3), Inches(3.2)])

    # 四个杠杆
    textbox(s, Inches(7.1), Inches(3.25), Inches(6.0), Inches(0.3),
            "关键增长杠杆（按优先级）", size=13, bold=True, color=C_DARK)
    data_lever = [
        ["① APP 用户回流独立站复购", "复购率 +30%", "One-ID 打通"],
        ["② 独立站首购用户激活 APP", "APP MAU +40%", "战役制协同"],
        ["③ 社区 UGC 反哺独立站落地页", "独立站转化率 +15%", "内容中台"],
        ["④ AI Agent 驱动跨触点推荐", "LTV +20%", "数据中台"],
    ]
    table(s, Inches(7.1), Inches(3.65), Inches(6.0), Inches(2.8),
          data_lever, headers=["杠杆", "提升预期", "依赖条件"],
          header_fill=C_ORANGE, first_col_bold=True,
          header_size=10, body_size=10,
          row_fills=[C_ORANGE_LT, C_WHITE, C_ORANGE_LT, C_WHITE],
          col_widths=[Inches(3.0), Inches(1.5), Inches(1.5)])

    # 核心信息
    rect(s, Inches(0.4), Inches(6.6), Inches(12.5), Inches(0.55),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板：20% 不是靠「独立站更努力」达成的 —— 四个杠杆都依赖「组织整合」",
         text_size=12, text_bold=True, text_color=C_BLUE)
    page_footer(s)

# ============ Slide 6 · 整合后的效率提升 ============
def slide_6():
    s = new_slide()
    page_header(s, "Slide 6 · 整合后的效率提升 · 保守估计",
                subtitle="每项收益都有明确的来源与测算 · 12 个月 ROI 即为正",
                page=7, part="III")

    headers = ["指标", "现状", "整合后（12 个月）", "提升幅度", "收益来源"]
    data = [
        ["独立站转化率", "[基准]", "+10% ~ +15%", "中",
         "社区 UGC 反哺 + APP 数据驱动推荐"],
        ["复购率", "[基准]", "+25% ~ +35%", "高",
         "One-ID 打通后跨触点召回"],
        ["CAC", "[基准]", "-15% ~ -20%", "中",
         "投放统一调度，避免内部互拍"],
        ["大促 ROI", "[基准]", "+20% ~ +25%", "高",
         "战役制，多触点合力"],
        ["营销人力成本", "[基准]", "-10% ~ -15%", "中",
         "内容 / 投放能力沉淀到中台"],
        ["决策周期", "10–14 天", "2–3 天", "高",
         "统一指挥，减少跨部门会议"],
        ["用户 NPS", "[基准]", "+10 ~ +15 分", "中",
         "体验一致性提升"],
        ["LTV（24 个月）", "[基准]", "+20% ~ +30%", "★ 极高",
         "全生命周期运营"],
    ]
    row_fills = [C_WHITE, C_GREEN_LT, C_WHITE, C_GREEN_LT,
                 C_WHITE, C_GREEN_LT, C_WHITE, C_RED_LT]
    table(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(3.8),
          data, headers=headers, header_fill=C_BLUE,
          first_col_bold=True, header_size=11, body_size=10.5,
          row_fills=row_fills,
          col_widths=[Inches(2.0), Inches(1.0), Inches(2.3),
                      Inches(1.2), Inches(6.0)])

    # 投入产出
    textbox(s, Inches(0.4), Inches(5.85), Inches(12.5), Inches(0.3),
            "投入产出测算", size=13, bold=True, color=C_DARK)
    data2 = [
        ["One-ID 技术建设", "工程资源 3–6 个月", "6 个月见效"],
        ["组织调整", "过渡期 3 个月 · 5–10% 人员流动", "6–12 个月见效"],
        ["中台搭建", "团队 + 工具采购", "9–12 个月见效"],
        ["新 DTC Leader 招募 / 任命", "1–2 个月", "立即见效"],
    ]
    table(s, Inches(0.4), Inches(6.2), Inches(12.5), Inches(0.85),
          data2, headers=["项目", "投入", "回报周期"],
          header_fill=C_ORANGE, first_col_bold=True,
          header_size=10, body_size=10,
          row_fills=[C_ORANGE_LT, C_WHITE, C_ORANGE_LT, C_WHITE],
          col_widths=[Inches(3.5), Inches(5.0), Inches(4.0)])

    rect(s, Inches(0.4), Inches(7.1), Inches(12.5), Inches(0.3),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板：这不是「赌一把」—— 即便按保守估计，12 个月 ROI 也是正的",
         text_size=11, text_bold=True, text_color=C_BLUE)

# ============ Slide 7 · 推荐的组织架构 ★ 视觉重点 ============
def slide_7():
    s = new_slide()
    page_header(s, "Slide 7 · 推荐架构 · 中台 + Pod + Squad",
                subtitle="从「按职能切」到「按用户周期切」 · 字节 / 阿里 / 美团反复验证的组织形态",
                page=8, part="IV")

    # 战略委员会顶
    rect(s, Inches(2.5), Inches(1.9), Inches(8.3), Inches(0.5),
         fill=C_DARK, border=None, rounded=True,
         text="DTC 战略委员会（创始人 + DTC Leader + CMO + CTO）",
         text_size=12, text_bold=True, text_color=C_WHITE)
    # 连线 → DTC 事业部
    line(s, Inches(6.65), Inches(2.4), Inches(6.65), Inches(2.65),
         color=C_DARK, width=2)
    # DTC 事业部容器（外框）
    rect(s, Inches(0.4), Inches(2.65), Inches(12.5), Inches(3.65),
         fill=C_BLUE_LT, border=C_BLUE, border_w=2, rounded=True,
         text="", )
    # DTC 事业部 标题
    rect(s, Inches(0.55), Inches(2.75), Inches(12.2), Inches(0.4),
         fill=C_BLUE, border=None, rounded=True,
         text="DTC 事业部（一个 Leader 统管）",
         text_size=13, text_bold=True, text_color=C_WHITE)

    # 横向中台（4 个）
    textbox(s, Inches(0.55), Inches(3.2), Inches(12.2), Inches(0.3),
            "【横向中台】统一能力 · 服务所有 Pod",
            size=11, bold=True, color=C_BLUE, italic=True)
    zhongtai = [
        ("用户资产中台", "One-ID / CDP / 会员", C_PURPLE),
        ("内容中台", "PGC / UGC / AIGC", C_ORANGE),
        ("增长中台", "SEM / SEO / 红人 / 私域", C_RED),
        ("产品技术中台", "独立站 / APP / 数据", C_GREEN),
    ]
    zw = (Inches(12.2) - Inches(0.3)) / 4
    zy = Inches(3.55)
    for i, (name, detail, color) in enumerate(zhongtai):
        x = Inches(0.55) + (zw + Inches(0.1)) * i
        rect(s, x, zy, zw, Inches(0.4), fill=color, border=None,
             text=name, text_size=11, text_bold=True, text_color=C_WHITE)
        rect(s, x, zy + Inches(0.4), zw, Inches(0.55), fill=C_WHITE,
             border=color, border_w=1, text=detail, text_size=10,
             text_color=C_GRAY_D)

    # 纵向 Pod（3 个）
    textbox(s, Inches(0.55), Inches(4.65), Inches(12.2), Inches(0.3),
            "【纵向 Pod】按用户旅程切分 · 端到端 KPI",
            size=11, bold=True, color=C_BLUE, italic=True)
    pods = [
        ("拉新 Pod", "独立站主", "认知 → 首购",
         "新客 GMV · CAC · 首购转化", C_BLUE_MID),
        ("留存 Pod", "APP 主", "首购 → 复购",
         "MAU · 次购率 · LTV", C_PURPLE),
        ("生态 Pod", "社区 + 私域", "忠诚 → 推荐",
         "NPS · UGC 产出 · 老带新率", C_GREEN),
    ]
    pw = (Inches(12.2) - Inches(0.2)) / 3
    py = Inches(5.0); ph = Inches(1.2)
    for i, (name, owner, stage, kpi, color) in enumerate(pods):
        x = Inches(0.55) + (pw + Inches(0.1)) * i
        # 头
        rect(s, x, py, pw, Inches(0.42), fill=color, border=None,
             text=name + "  ·  " + owner, text_size=11, text_bold=True,
             text_color=C_WHITE)
        # 旅程阶段
        rect(s, x, py + Inches(0.42), pw, Inches(0.3),
             fill=C_WHITE, border=color, border_w=1,
             text=stage, text_size=10, text_color=color, text_bold=True)
        # KPI
        rect(s, x, py + Inches(0.72), pw, ph - Inches(0.72),
             fill=C_WHITE, border=color, border_w=1,
             text="KPI\n" + kpi, text_size=9.5, text_color=C_GRAY_D)

    # 战役 Squad 底
    line(s, Inches(6.65), Inches(6.3), Inches(6.65), Inches(6.55),
         color=C_DARK, width=2)
    rect(s, Inches(0.4), Inches(6.55), Inches(12.5), Inches(0.55),
         fill=C_ORANGE, border=None, rounded=True,
         text="【战役制 Campaign Squad】大促 / 新品上市临时组队：Pod 出 PM + 中台出资源 · 打完即散 · 避免常设组织僵化",
         text_size=11, text_bold=True, text_color=C_WHITE)

    # 核心信息
    rect(s, Inches(0.4), Inches(7.15), Inches(12.5), Inches(0.3),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="能力沉淀到中台 · 指挥统一到 Pod · 战役灵活到 Squad",
         text_size=11, text_bold=True, text_color=C_BLUE)

# ============ Slide 7.5 / 辅助 · 现状部门如何「再定位」 ============
# 已合并入 Slide 7 尾部说明 —— 另做一页更清晰
def slide_7b():
    s = new_slide()
    page_header(s, "Slide 7（续）· 现状部门的「再定位」",
                subtitle="对所有现有部门是「再定位」 · 不是「谁吃掉谁」",
                page=9, part="IV")
    headers = ["现状部门", "在新架构中的位置", "能力去向", "说明"]
    data = [
        ["流量部", "增长中台", "横向能力沉淀",
         "SEM / SEO / 红人经验服务所有 Pod"],
        ["独立站部", "主导 拉新 Pod", "端到端首购旅程",
         "独立站仍是首购主阵地"],
        ["独立站社区", "合并入 内容中台", "内容资产统一",
         "UGC 资产全链路打通"],
        ["APP 部", "主导 留存 Pod", "APP 生态价值释放",
         "IoT + AI + 内容 + 会员 合力"],
        ["APP 社区", "合并入 内容中台", "一个社区，统一品牌声音",
         "避免两个社区内部博弈"],
        ["会员部", "进入 用户资产中台", "会员体系全局化",
         "One-ID 的承载主体"],
    ]
    row_fills = [C_ORANGE_LT, C_BLUE_LT, C_BLUE_LT,
                 C_PURPLE_LT, C_PURPLE_LT, C_GREEN_LT]
    table(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(3.2),
          data, headers=headers, header_fill=C_BLUE,
          first_col_bold=True, header_size=12, body_size=11,
          row_fills=row_fills,
          col_widths=[Inches(2.0), Inches(2.8), Inches(2.5), Inches(5.2)])

    # 中立说明
    box = rect(s, Inches(0.4), Inches(5.3), Inches(12.5), Inches(1.6),
               fill=C_GREEN_LT, border=C_GREEN, border_w=2, rounded=True)
    tf = box.text_frame
    tf.margin_left = Pt(20); tf.margin_right = Pt(20)
    tf.margin_top = Pt(12); tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "关键说明（中立性承诺）"
    r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = C_GREEN; r.font.name = FONT
    add_para(tf,
             "这是「能力沉淀到中台、指挥统一到 Pod」的组织升级，不是部门合并或权力再分配。",
             size=13, bold=True, color=C_DARK, space_before=6)
    add_para(tf,
             "任何一个现有负责人都可能成为 Pod Leader / 中台 Head / 甚至 DTC Leader —— 我支持公司做最有利战略的选择。",
             size=11, color=C_GRAY_D, space_before=6)
    add_para(tf,
             "这是过去 5 年互联网行业（字节 / 阿里 / 美团）反复验证的高效组织形态。",
             size=11, italic=True, color=C_GRAY, space_before=6)

    # 底部核心信息
    rect(s, Inches(0.4), Inches(7.05), Inches(12.5), Inches(0.35),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板：架构的本质是 —— 让能力沉淀到中台、让指挥统一到 Pod、让战役灵活到 Squad",
         text_size=11, text_bold=True, text_color=C_BLUE)

# ============ Slide 8 · 资源统筹与决策机制 ============
def slide_8():
    s = new_slide()
    page_header(s, "Slide 8 · 资源统筹与决策机制 · 三大统一",
                subtitle="预算池 · 数据看板 · 战役指挥 —— 把权力 / 预算 / 数据统一到一个 Leader",
                page=10, part="IV")

    # 三大统一并列
    unities = [
        ("统一 1 · 预算池",
         [("现状", "按部门切（流量部 X / 独立站部 Y / APP 部 Z）"),
          ("整合后", "按 LTV 切（拉新 / 留存 / 生态 Pod）"),
          ("调度", "季度动态调整，依 ROI 再分配"),
          ("决策人", "DTC Leader + 战略委员会")],
         C_ORANGE),
        ("统一 2 · 数据看板",
         [("核心", "一张表：One-ID 下的用户分层 + LTV + 跨触点行为"),
          ("节奏", "创始人 / CEO 每周只看一张表"),
          ("转变", "独立站 GMV / APP MAU 从「KPI」变「结果指标」"),
          ("工具", "CDP + BI + 统一归因模型")],
         C_PURPLE),
        ("统一 3 · 战役指挥",
         [("拍板人", "大促 / 新品节奏由 DTC Leader 拍板"),
          ("触点", "独立站首屏 / APP 开屏 / Feed / 会员 Push 统一编排"),
          ("决策周期", "14 天 → 2 天"),
          ("配套", "战役制 Squad · 打完即散")],
         C_GREEN),
    ]
    x0 = Inches(0.4); w = Inches(4.05); gap = Inches(0.15); y = Inches(1.9)
    for i, (title, items, color) in enumerate(unities):
        x = x0 + (w + gap) * i
        rect(s, x, y, w, Inches(0.5), fill=color, border=None,
             text=title, text_size=13, text_bold=True, text_color=C_WHITE)
        box = rect(s, x, y + Inches(0.5), w, Inches(2.5),
                   fill=C_WHITE, border=color, border_w=1)
        tf = box.text_frame
        tf.margin_left = Pt(10); tf.margin_right = Pt(10)
        tf.margin_top = Pt(8); tf.word_wrap = True
        for j, (label, body) in enumerate(items):
            if j == 0:
                p = tf.paragraphs[0]
                r = p.add_run(); r.text = label
                r.font.size = Pt(10); r.font.bold = True
                r.font.color.rgb = color; r.font.name = FONT
            else:
                add_para(tf, label, size=10, bold=True, color=color,
                         space_before=8)
            add_para(tf, body, size=9.5, color=C_GRAY_D, space_before=2)

    # 权力下放
    textbox(s, Inches(0.4), Inches(4.5), Inches(6.5), Inches(0.3),
            "权力下放原则", size=12, bold=True, color=C_DARK)
    data_power = [
        ["DTC Leader", "季度战略 · 预算分配 · 战役指挥 · Pod/中台负责人任命"],
        ["Pod 负责人", "Pod 内人员/资源调度 · 季度 KPI 达成路径"],
        ["中台负责人", "中台能力建设 · SLA · 服务标准"],
        ["Squad PM", "单次战役内的快速决策"],
    ]
    table(s, Inches(0.4), Inches(4.85), Inches(6.5), Inches(1.8),
          data_power, headers=["层级", "决策权"],
          header_fill=C_BLUE, first_col_bold=True,
          header_size=10, body_size=10,
          row_fills=[C_BLUE_LT, C_WHITE, C_BLUE_LT, C_WHITE],
          col_widths=[Inches(1.5), Inches(5.0)])

    # DTC Leader 画像
    box = rect(s, Inches(7.1), Inches(4.5), Inches(5.8), Inches(2.2),
               fill=C_RED_LT, border=C_RED, border_w=2, rounded=True)
    tf = box.text_frame
    tf.margin_left = Pt(14); tf.margin_right = Pt(14)
    tf.margin_top = Pt(10); tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "DTC Leader 人选关键要素"
    r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = C_RED; r.font.name = FONT
    add_para(tf, "全局视角 —— 不能是某触点出身的「部门墙」思维",
             size=10.5, color=C_GRAY_D, space_before=6, bullet=True)
    add_para(tf, "数据驱动 —— 懂 LTV / CAC / 用户分层",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf, "战役指挥经验 —— 有端到端跑通大项目的能力",
             size=10.5, color=C_GRAY_D, space_before=4, bullet=True)
    add_para(tf, "建议：内部竞聘 + 外部物色，并行推进",
             size=11, bold=True, color=C_RED, space_before=8)

    # 90 天过渡期
    rect(s, Inches(7.1), Inches(6.8), Inches(5.8), Inches(0.3),
         fill=C_ORANGE_LT, border=C_ORANGE, border_w=1, rounded=True,
         text="90 天过渡：Day 0-30 组织稳定 · Day 31-60 中台 MVP · Day 61-90 首战验证",
         text_size=10, text_color=C_ORANGE, text_bold=True)
    rect(s, Inches(0.4), Inches(6.8), Inches(6.5), Inches(0.3),
         fill=C_BLUE_LT, border=C_BLUE, border_w=1, rounded=True,
         text="给老板：核心是「权力 / 预算 / 数据三件事统一到一个 Leader」",
         text_size=10, text_color=C_BLUE, text_bold=True)
    page_footer(s)

# ============ Slide 9 · 总结 · 三句话 + 下一步 ============
def slide_9():
    s = new_slide()
    page_header(s, "总结 · 本次汇报的核心结论",
                subtitle="三句话 + 三个待决议题",
                page=11)

    # 三句话
    textbox(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(0.4),
            "三句话", size=15, bold=True, color=C_DARK)
    three = [
        ("01", "DTC 是必选项", C_BLUE,
         "行业范式已切换，20% 占比是出海品牌的入场券 —— Momcozy 当前 ~10% 显著落后头部"),
        ("02", "根因是组织", C_RED,
         "体验割裂 / 资源浪费 / 决策延迟 —— 三大痛点都指向「组织没有全局指挥官」"),
        ("03", "解决方案是组织升级", C_GREEN,
         "成立 DTC 大部门 · 「中台 + Pod + Squad」三层架构 · 统一预算 / 数据 / 指挥"),
    ]
    y = Inches(2.35)
    for i, (n, title, color, body) in enumerate(three):
        yy = y + Inches(0.85) * i
        oval(s, Inches(0.4), yy, Inches(0.7), Inches(0.7), fill=color,
             border=None, text=n, text_size=16, text_color=C_WHITE,
             text_bold=True)
        box = rect(s, Inches(1.25), yy, Inches(11.65), Inches(0.7),
                   fill=C_WHITE, border=color, border_w=1, rounded=True)
        tf = box.text_frame
        tf.margin_left = Pt(14); tf.margin_right = Pt(14)
        tf.margin_top = Pt(6); tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title + "   —   "
        r.font.size = Pt(14); r.font.bold = True
        r.font.color.rgb = color; r.font.name = FONT
        r2 = p.add_run(); r2.text = body
        r2.font.size = Pt(11); r2.font.color.rgb = C_GRAY_D
        r2.font.name = FONT

    # 建议下一步
    textbox(s, Inches(0.4), Inches(5.05), Inches(12.5), Inches(0.4),
            "建议下一步 · 三个待决议题", size=15, bold=True, color=C_DARK)
    data_next = [
        ["议题 1", "是否将 DTC 整合列入 2026 战略重点", "本月", "创始人 / 战略委员会"],
        ["议题 2", "DTC Leader 人选讨论（内部竞聘 or 外部招募）", "1 个月内", "创始人"],
        ["议题 3", "90 天过渡期方案细化", "2 个月内", "候选 DTC Leader + HR"],
    ]
    table(s, Inches(0.4), Inches(5.5), Inches(12.5), Inches(1.5),
          data_next, headers=["#", "议题", "时间", "决策人"],
          header_fill=C_BLUE, first_col_bold=True,
          header_size=12, body_size=11,
          row_fills=[C_BLUE_LT, C_WHITE, C_ORANGE_LT],
          col_widths=[Inches(0.8), Inches(7.7), Inches(1.5), Inches(2.5)])

    # 底部
    rect(s, Inches(0.4), Inches(7.1), Inches(12.5), Inches(0.3),
         fill=C_BLUE, border=None, rounded=True,
         text="汇报结束 · 期待讨论",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ Slide 10 · 中立陈述（收尾） ============
def slide_10():
    s = new_slide()
    page_header(s, "最后的话 · 中立陈述（APP 负责人自白）",
                subtitle="我为什么会提出这个方案 · 以及我对结果的承诺",
                page=12)

    # 大引用块
    box = rect(s, Inches(0.4), Inches(1.9), Inches(12.5), Inches(4.5),
               fill=C_WHITE, border=C_BLUE, border_w=2, rounded=True)
    rect(s, Inches(0.6), Inches(2.1), Inches(0.08), Inches(4.1),
         fill=C_BLUE, border=None)
    tf = box.text_frame
    tf.margin_left = Pt(36); tf.margin_right = Pt(24)
    tf.margin_top = Pt(24); tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "我作为 APP 负责人提出这个方案 ——"
    r.font.size = Pt(17); r.font.bold = True
    r.font.color.rgb = C_DARK; r.font.name = FONT

    add_para(tf, "不是为了让 APP 部门做大。", size=20, bold=True,
             color=C_RED, space_before=10)
    add_para(tf, "", size=6, color=C_GRAY)

    add_para(tf, "而是因为 ——",
             size=14, color=C_GRAY_D, space_before=6)
    add_para(tf, "APP 已升级为「用户陪伴 + 工具 + 内容 + 商城 + 会员」的资产平台",
             size=13, color=C_GRAY_D, space_before=6, bullet=True)
    add_para(tf, "如果不整合：APP 生态价值将被组织墙锁死，2026 AI Agent 战略无法兑现",
             size=13, color=C_RED, space_before=6, bullet=True, bold=True)
    add_para(tf, "如果整合：整合后的 DTC 大部门 Leader 可以是任何最合适的人 —— 我支持公司做最有利战略的选择",
             size=13, color=C_GREEN, space_before=6, bullet=True, bold=True)

    # 签名行
    textbox(s, Inches(0.4), Inches(6.55), Inches(12.5), Inches(0.4),
            "—— 立场诚恳 · 提案中立 · 只为公司战略做对的事",
            size=13, italic=True, color=C_GRAY, align=PP_ALIGN.RIGHT)
    # 底部一行
    rect(s, Inches(0.4), Inches(7.05), Inches(12.5), Inches(0.35),
         fill=C_ORANGE, border=None, rounded=True,
         text="APP 事业部 · 代表「用户视角」与「公司全局视角」",
         text_size=12, text_bold=True, text_color=C_WHITE)

# ============ 封底 ============
def slide_back():
    s = new_slide(C_BLUE)
    rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.18),
         fill=C_ORANGE, border=None)
    # 中央大字
    textbox(s, Inches(1), Inches(2.5), Inches(11.3), Inches(0.5),
            "汇报结束", size=16, italic=True, color=C_ORANGE_LT,
            align=PP_ALIGN.CENTER)
    textbox(s, Inches(1), Inches(3.2), Inches(11.3), Inches(1.8),
            "期待讨论",
            size=52, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    # 分隔
    rect(s, Inches(5.67), Inches(5.1), Inches(2), Inches(0.03),
         fill=C_ORANGE, border=None)
    # 三个议题
    textbox(s, Inches(1), Inches(5.4), Inches(11.3), Inches(0.4),
            "① DTC 整合是否列入 2026 战略重点     "
            "② DTC Leader 人选     "
            "③ 90 天过渡期方案",
            size=13, color=C_BLUE_LT, align=PP_ALIGN.CENTER)
    # 签名
    textbox(s, Inches(1), Inches(6.8), Inches(11.3), Inches(0.4),
            "APP 事业部  ·  代表「用户视角 + 全局视角」  ·  2026/05/11",
            size=11, color=C_GRAY_LT, align=PP_ALIGN.CENTER, italic=True)

# ==================================================================
#                                 BUILD
# ==================================================================
def build():
    slide_cover()
    slide_opening()
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    slide_5()
    slide_6()
    slide_7()
    slide_7b()
    slide_8()
    slide_9()
    slide_10()
    slide_back()
    prs.save(OUT_PATH)
    print(f"✅ Generated: {OUT_PATH}")
    print(f"   Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    build()
