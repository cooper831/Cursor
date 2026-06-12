#!/usr/bin/env python3
# Generate docs/flowcharts/momcozy-2026-commercial-roadmap.drawio
from datetime import date
from xml.sax.saxutils import escape as xml_esc


def _attr_escape(text):
    """XML-escape mxCell value= attribute; draw.io decodes &lt;br/&gt; as HTML when style has html=1."""
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def gen():
    def d(s):
        return date.fromisoformat(s)

    o = date(2026, 5, 1)

    def pos(dt):
        return (dt - o).days

    TW = 1100
    TMAX = 275
    SCALE = TW / TMAX
    X0 = 400

    def bar_geom(start, end):
        s = pos(d(start))
        e = pos(d(end))
        w = e - s + 1
        bx = X0 + s * SCALE
        width = max(w * SCALE, 10)
        return int(round(bx)), int(round(width))

    def mile_x(ds):
        day = pos(d(ds))
        return int(round(X0 + day * SCALE - 6))

    sections = [
        ("一次性购买（IAP）", "#CA8A04", "#FEF9C3", [
            ("开发收尾 & QA", "2026-05-01", "2026-05-31", "#FDE68A", "#CA8A04"),
            ("场景扩展 / 转化优化迭代", "2026-06-16", "2026-12-31", "#FACC15", "#CA8A04"),
        ]),
        ("订阅（Subscription）", "#1D4ED8", "#DBEAFE", [
            ("价值评审文档准备", "2026-05-01", "2026-05-25", "#93C5FD", "#2563EB"),
            ("价值评审 + 调研验证", "2026-05-26", "2026-06-20", "#BFDBFE", "#2563EB"),
            ("PRD + 需求评审", "2026-06-21", "2026-07-15", "#60A5FA", "#1D4ED8"),
            ("开发 + QA + 灰度", "2026-07-16", "2026-09-05", "#3B82F6", "#1E40AF"),
            ("续订 / 留存优化", "2026-09-11", "2026-12-31", "#93C5FD", "#1D4ED8"),
        ]),
        ("商城 · V1 H5 优化", "#15803D", "#DCFCE7", [
            ("调研 + 方案设计", "2026-05-15", "2026-07-31", "#BBF7D0", "#15803D"),
            ("V1 文档准备", "2026-08-01", "2026-08-25", "#86EFAC", "#15803D"),
            ("V1 评审 + 开发", "2026-08-26", "2026-10-15", "#4ADE80", "#166534"),
        ]),
        ("商城 · V2 耗材原生化", "#047857", "#D1FAE5", [
            ("V2 文档准备", "2026-09-15", "2026-10-25", "#6EE7B7", "#047857"),
            ("V2 评审 + 开发", "2026-10-26", "2026-12-25", "#34D399", "#065F46"),
        ]),
        ("商城 · V3 整站原生化", "#0F766E", "#CCFBF1", [
            ("V3 调研立项 → 2027", "2026-11-01", "2027-01-31", "#5EEAD4", "#0D9488"),
        ]),
    ]

    milestones = [
        ("M1 IAP 上线", "2026-06-15", "#DC2626"),
        ("M3 整体方案 Review", "2026-07-31", "#EA580C"),
        ("M2 订阅上线", "2026-09-10", "#DC2626"),
        ("M4 商城 V1", "2026-10-20", "#EA580C"),
        ("M5 商城 V2", "2026-12-30", "#EA580C"),
    ]

    months = [
        ("2026-05", 0),
        ("2026-06", 31),
        ("2026-07", 61),
        ("2026-08", 92),
        ("2026-09", 123),
        ("2026-10", 153),
        ("2026-11", 184),
        ("2026-12", 214),
        ("2027-01", 245),
    ]

    cid = [0]

    def new_id():
        cid[0] += 1
        return f"c{cid[0]}"

    def cell(i, label, style, gx, gy, gw, gh, parent="1", raw_html=False):
        if not label:
            val = ""
        elif raw_html:
            val = _attr_escape(label)
        else:
            val = xml_esc(label)
        return (
            f'        <mxCell id="{i}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
            f'          <mxGeometry x="{gx}" y="{gy}" width="{gw}" height="{gh}" as="geometry" />\n'
            f"        </mxCell>"
        )

    def edge(i, style, src, tgt, parent="1"):
        return (
            f'        <mxCell id="{i}" style="{style}" edge="1" parent="{parent}" source="{src}" target="{tgt}">\n'
            f'          <mxGeometry relative="1" as="geometry" />\n        </mxCell>'
        )

    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append(
        '<mxfile host="app.diagrams.net" agent="momcozy-roadmap-gen" version="24.0.0" type="device">'
    )

    # ----- Page 1: Gantt -----
    out.append('  <diagram id="gantt-2026" name="01 全年甘特">')
    out.append(
        '    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
        'fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">'
    )
    out.append("      <root>")
    out.append('        <mxCell id="0" />')
    out.append('        <mxCell id="1" parent="0" />')

    out.append(
        cell(
            new_id(),
            "momcozy 商业化 2026 全年排期（甘特）",
            "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=18;fontStyle=1;fontColor=#1F2937;",
            40,
            20,
            1520,
            36,
        )
    )
    out.append(
        cell(
            new_id(),
            "基准日 2026-05-01  |  可与 checklist-02-gantt.drawio 同版式对齐编辑",
            "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=11;fontStyle=2;fontColor=#6B7280;",
            40,
            52,
            1520,
            20,
        )
    )
    out.append(
        cell(
            new_id(),
            "",
            "rounded=0;fillColor=#F9FAFB;strokeColor=#E5E7EB;",
            40,
            78,
            1520,
            32,
        )
    )
    out.append(
        cell(
            new_id(),
            "工作流 / 任务",
            "text;html=1;align=left;fontSize=12;fontStyle=1;fontColor=#374151;spacingLeft=12;",
            48,
            82,
340,
            24,
        )
    )

    for i, (mlab, day_start) in enumerate(months):
        nxt = [m[1] for m in months if m[1] > day_start]
        day_end = (nxt[0] - 1) if nxt else TMAX
        gx = int(X0 + day_start * SCALE)
        gw = int((day_end - day_start + 1) * SCALE)
        out.append(
            cell(
                new_id(),
                mlab,
                "text;html=1;align=center;fontSize=10;fontColor=#374151;",
                gx,
                82,
                gw,
                24,
            )
        )

    for _, day_start in months[1:]:
        gx = int(X0 + day_start * SCALE)
        out.append(
            cell(
                new_id(),
                "",
                "rounded=0;fillColor=#E5E7EB;strokeColor=none;",
                gx,
                78,
                2,
                800,
            )
        )

    y = 118
    for sec_title, stroke_col, fill_col, rows in sections:
        out.append(
            cell(
                new_id(),
                sec_title,
                f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill_col};strokeColor={stroke_col};"
                f"fontSize=12;fontStyle=1;align=left;spacingLeft=10;fontColor=#1F2937;",
                40,
                y,
                1520,
                24,
            )
        )
        y += 32
        for rname, s, e, fcol, scol in rows:
            out.append(
                cell(
                    new_id(),
                    rname,
                    "text;html=1;align=left;fontSize=11;fontColor=#374151;spacingLeft=12;",
                    48,
                    y + 2,
                    340,
                    22,
                )
            )
            xb, wb = bar_geom(s, e)
            bar_lbl = f"{s[5:].replace('-', '.')} → {e[5:].replace('-', '.')}"
            out.append(
                cell(
                    new_id(),
                    bar_lbl,
                    f"rounded=1;whiteSpace=wrap;html=1;fillColor={fcol};strokeColor={scol};"
                    f"fontSize=9;fontColor=#111827;",
                    xb,
                    y,
                    wb,
                    22,
                )
            )
            y += 30
        y += 8

    out.append(
        cell(
            new_id(),
            "关键里程碑 ◆（红=上线类；橙=方案/商城节点）",
            "text;html=1;align=left;fontSize=12;fontStyle=1;fontColor=#991B1B;spacingLeft=8;",
            48,
            y,
            720,
            22,
        )
    )
    y += 28
    out.append(
        cell(
            new_id(),
            "",
            "rounded=0;fillColor=#FEF2F2;strokeColor=#FECACA;",
            X0,
            y,
            TW,
            22,
        )
    )
    for mlab, ds, col in milestones:
        mx = mile_x(ds)
        out.append(
            cell(
                new_id(),
                "",
                f"triangle;direction=north;fillColor={col};strokeColor={col};",
                mx,
                y + 4,
                12,
                12,
            )
        )
    y += 36
    for mlab, ds, col in milestones:
        mx = mile_x(ds)
        dshort = ds[5:].replace("-", ".")
        out.append(
            cell(
                new_id(),
                f"{mlab}<br/>{dshort}",
                "text;html=1;fontSize=9;fontColor=#374151;align=center;",
                mx - 44,
                y,
                104,
                36,
                raw_html=True,
            )
        )

    y += 48
    out.append(
        cell(
            new_id(),
            "<b>图例</b><br/>色条=任务周期；◆=里程碑。<br/>"
            "若 Markdown 中 Mermaid 报错，请用 diagrams.net 打开本文件编辑导出 PNG。",
            "text;html=1;strokeColor=#E5E7EB;fillColor=#F9FAFB;align=left;rounded=1;fontSize=10;spacing=12;fontColor=#374151;",
            40,
            y,
            1520,
            56,
            raw_html=True,
        )
    )

    out.append("      </root>")
    out.append("    </mxGraphModel>")
    out.append("  </diagram>")

    # ----- Page 2: Dependencies -----
    out.append('  <diagram id="deps" name="02 跨部门依赖">')
    out.append(
        '    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" pageWidth="1200" pageHeight="700" math="0" shadow="0">'
    )
    out.append("      <root>")
    out.append('        <mxCell id="0" />')
    out.append('        <mxCell id="d1" parent="0" />')

    out.append(
        cell(
            new_id(),
            "momcozy 商业化 · 跨部门依赖（与规划文档 §5.2 一致）",
            "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=16;fontStyle=1;fontColor=#1F2937;",
            40,
            24,
            1120,
            32,
        )
    )

    comm = new_id()
    out.append(
        cell(
            comm,
            "<b>商业化中心</b>",
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;strokeWidth=2;fontSize=12;fontColor=#78350F;",
            520,
            120,
            160,
            56,
            raw_html=True,
        )
    )

    boxes = [
        ("b_dev", "App 研发", 280, 280, "#DBEAFE", "#2563EB", "#1E3A8A"),
        ("b_ind", "独立站团队", 520, 280, "#DCFCE7", "#15803D", "#14532D"),
        ("b_sup", "供应链", 760, 280, "#D1FAE5", "#059669", "#064E3B"),
        ("b_cs", "客服", 200, 420, "#FEE2E2", "#DC2626", "#991B1B"),
        ("b_fin", "财务", 360, 420, "#E0E7FF", "#4F46E5", "#312E81"),
        ("b_gr", "增长运营", 520, 420, "#FFEDD5", "#C2410C", "#7C2D12"),
        ("b_data", "数据中心", 680, 420, "#E0F2FE", "#0284C7", "#0C4A6E"),
        ("b_law", "法务合规", 840, 420, "#F3E8FF", "#7C3AED", "#4C1D95"),
    ]

    for bid, label, gx, gy, fill, stroke, tc in boxes:
        out.append(
            cell(
                bid,
                f'<span style="color:{tc}"><b>{xml_esc(label)}</b></span>',
                f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=11;",
                gx,
                gy,
                120,
                44,
                raw_html=True,
            )
        )

    # edges from Comm
    links = [
        ("e1", comm, "b_dev"),
        ("e2", comm, "b_ind"),
        ("e3", comm, "b_sup"),
        ("e4", comm, "b_cs"),
        ("e5", comm, "b_fin"),
        ("e6", comm, "b_gr"),
        ("e7", comm, "b_data"),
        ("e8", comm, "b_law"),
        ("e9", "b_ind", "b_data"),
        ("e10", "b_sup", "b_ind"),
        ("e11", "b_cs", comm),
    ]
    for eid, a, b in links:
        out.append(
            edge(
                eid,
                "endArrow=classic;html=1;strokeWidth=2;strokeColor=#6B7280;rounded=1;",
                a,
                b,
                "d1",
            )
        )

    out.append(
        cell(
            new_id(),
            "Indie→Data、Supply→Indie、CS→Comm 为原文依赖方向。",
            "text;html=1;align=left;fontSize=10;fontColor=#6B7280;fillColor=#FAFAFA;strokeColor=#E5E7EB;rounded=1;",
            40,
            520,
            560,
            40,
        )
    )

    out.append("      </root>")
    out.append("    </mxGraphModel>")
    out.append("  </diagram>")

    # ----- Page 3: PM flow -----
    out.append('  <diagram id="pm-flow" name="03 PM 人力配置">')
    out.append(
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" pageWidth="900" pageHeight="520" math="0" shadow="0">'
    )
    out.append("      <root>")
    out.append('        <mxCell id="0" />')
    out.append('        <mxCell id="p1" parent="0" />')

    out.append(
        cell(
            new_id(),
            "PM 人力配置路径（规划文档 §7.4）",
            "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=15;fontStyle=1;",
            40,
            20,
            820,
            28,
        )
    )

    n1, n2, n3, n4 = new_id(), new_id(), new_id(), new_id()
    out.append(
        cell(
            n1,
            "当前 5 月<br/>仅商业化负责人 1 人",
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#F3F4F6;strokeColor=#6B7280;fontSize=11;",
            360,
            80,
            180,
            56,
            raw_html=True,
        )
    )
    out.append(
        cell(
            n2,
            "Q2：立即招聘<br/>+1 中高级 PM",
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#2563EB;fontSize=11;fontStyle=1;",
            360,
            180,
            180,
            56,
            raw_html=True,
        )
    )
    out.append(
        cell(
            n3,
            "Q3：评估再补<br/>+1 PM 或外部 BA",
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#15803D;fontSize=11;fontStyle=1;",
            360,
            280,
            180,
            56,
            raw_html=True,
        )
    )
    out.append(
        cell(
            n4,
            "Q4：稳定运营态<br/>PM 团队 2–3 人",
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontSize=11;fontStyle=1;",
            360,
            380,
            180,
            56,
            raw_html=True,
        )
    )

    for a, b, eid in [(n1, n2, "pf1"), (n2, n3, "pf2"), (n3, n4, "pf3")]:
        out.append(
            edge(
                eid,
                "endArrow=classic;html=1;strokeWidth=2;strokeColor=#374151;exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
                a,
                b,
                "p1",
            )
        )

    out.append("      </root>")
    out.append("    </mxGraphModel>")
    out.append("  </diagram>")

    out.append("</mxfile>")
    return "\n".join(out)


if __name__ == "__main__":
    p = __file__.replace("_gen_momcozy_2026_drawio.py", "momcozy-2026-commercial-roadmap.drawio")
    with open(p, "w", encoding="utf-8") as f:
        f.write(gen())
    print("Wrote", p)
