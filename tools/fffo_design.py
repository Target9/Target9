"""Fælles design-hjælpere til PowerPoint og plancher (python-pptx)."""

import math
import random

from pptx.chart.data import CategoryChartData, XyChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

NAVY = RGBColor(0x1B, 0x2A, 0x41)
INK = RGBColor(0x22, 0x2B, 0x38)
GREY = RGBColor(0x6B, 0x75, 0x85)
LIGHT = RGBColor(0xF3, 0xF5, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xD5, 0xDB, 0xE5)

BIO = RGBColor(0x2E, 0x9E, 0x6A)
FYS = RGBColor(0x2F, 0x6F, 0xDE)
KEM = RGBColor(0xD6, 0x45, 0x45)
GEO = RGBColor(0xE8, 0x8A, 0x1A)
PURPLE = RGBColor(0x7B, 0x4F, 0xC9)

SUBJECT = {
    "bio": (BIO, "BIOLOGI"),
    "fys": (FYS, "FYSIK"),
    "kem": (KEM, "KEMI"),
    "geo": (GEO, "GEOGRAFI"),
    "all": (NAVY, "FÆLLES"),
}

FONT = "Calibri"


def tint(color, amount):
    """Lys en farve op mod hvid (amount 0..1)."""
    r, g, b = color[0], color[1], color[2]
    return RGBColor(
        int(r + (255 - r) * amount),
        int(g + (255 - g) * amount),
        int(b + (255 - b) * amount),
    )


def rect(shapes, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, line_w=1.0):
    s = shapes.add_shape(shape, Emu(int(x)), Emu(int(y)), Emu(int(w)), Emu(int(h)))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


def text(
    shapes,
    x,
    y,
    w,
    h,
    content,
    size=18,
    color=INK,
    bold=False,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
    italic=False,
    line_spacing=1.08,
    margin=0,
):
    """Tekstboks. content kan være str eller liste af linjer/(tekst, opts)-tupler.

    Linjer der starter med '• ' får hængende indrykning. '**x**' er ikke understøttet;
    brug tupler: ("tekst", {"bold": True, "color": RGB, "size": 14}).
    En linje kan også være en liste af runs: [("Fed ", {"bold": True}), ("normal", {})].
    """
    tb = shapes.add_textbox(Emu(int(x)), Emu(int(y)), Emu(int(w)), Emu(int(h)))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Emu(int(margin)))
    lines = content if isinstance(content, list) else [content]
    for idx, line in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = Pt(0) if idx == 0 else Pt(size * 0.3)
        p.alignment = align
        p.line_spacing = line_spacing
        runs = line
        if isinstance(line, str):
            runs = [(line, {})]
        elif isinstance(line, tuple):
            runs = [line]
        for run_text, opts in runs:
            r = p.add_run()
            r.text = run_text
            f = r.font
            f.name = FONT
            f.size = Pt(opts.get("size", size))
            f.bold = opts.get("bold", bold)
            f.italic = opts.get("italic", italic)
            f.color.rgb = opts.get("color", color)
    return tb


def bullets(shapes, x, y, w, h, items, size=18, color=INK, bullet_color=None, gap=0.45):
    """Punktliste. items: str eller (fed_del, resten)."""
    tb = shapes.add_textbox(Emu(int(x)), Emu(int(y)), Emu(int(w)), Emu(int(h)))
    tf = tb.text_frame
    tf.word_wrap = True
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Emu(0))
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(size * gap) if i else Pt(0)
        p.line_spacing = 1.05
        r = p.add_run()
        r.text = "■  "
        r.font.size = Pt(size * 0.6)
        r.font.color.rgb = bullet_color or color
        r.font.name = FONT
        if isinstance(item, tuple):
            head, rest = item
            r1 = p.add_run()
            r1.text = head
            r1.font.bold = True
            r1.font.size = Pt(size)
            r1.font.color.rgb = color
            r1.font.name = FONT
            r2 = p.add_run()
            r2.text = rest
            r2.font.size = Pt(size)
            r2.font.color.rgb = color
            r2.font.name = FONT
        else:
            r1 = p.add_run()
            r1.text = item
            r1.font.size = Pt(size)
            r1.font.color.rgb = color
            r1.font.name = FONT
    return tb


def label_box(shapes, x, y, w, h, title, body, color, size=16, title_size=None, fill_tint=0.88):
    """Kort med farvet topbånd + tekst."""
    title_size = title_size or size + 2
    band = title_size * 12700 * 2.1
    rect(shapes, x, y, w, h, fill=tint(color, fill_tint), shape=MSO_SHAPE.RECTANGLE)
    rect(shapes, x, y, w, band, fill=color)
    text(shapes, x, y, w, band, title, size=title_size, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    pad = size * 12700 * 0.7
    if isinstance(body, list) and body and not isinstance(body[0], list) and all(
        isinstance(b, (str, tuple)) for b in body
    ) and any(isinstance(b, str) and b.startswith("• ") for b in body):
        items = [b[2:] if isinstance(b, str) and b.startswith("• ") else b for b in body]
        bullets(shapes, x + pad, y + band + pad, w - 2 * pad, h - band - 2 * pad, items,
                size=size, bullet_color=color, gap=0.3)
    else:
        text(shapes, x + pad, y + band + pad * 0.6, w - 2 * pad, h - band - 2 * pad, body,
             size=size)


def arrow(shapes, x1, y1, x2, y2, color=GREY, width=2.0):
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1)), Emu(int(y1)),
                             Emu(int(x2)), Emu(int(y2)))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    tail = ln.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd",
                          {"type": "triangle", "w": "med", "len": "med"})
    ln.append(tail)
    return c


def table(shapes, x, y, w, h, rows, header_color, size=14, col_widths=None,
          first_col_bold=False, zebra=True, header_size=None):
    nrows, ncols = len(rows), len(rows[0])
    gt = shapes.add_table(nrows, ncols, Emu(int(x)), Emu(int(y)), Emu(int(w)), Emu(int(h)))
    tbl = gt.table
    if col_widths:
        total = sum(col_widths)
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = Emu(int(w * cw / total))
    for r in range(nrows):
        tbl.rows[r].height = Emu(int(h / nrows))
        for c in range(ncols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Emu(int(size * 12700 * 0.5))
            cell.margin_top = cell.margin_bottom = Emu(int(size * 12700 * 0.2))
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            val = rows[r][c]
            tf = cell.text_frame
            tf.word_wrap = True
            tf.text = ""
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = str(val)
            run.font.name = FONT
            if r == 0:
                run.font.size = Pt(header_size or size)
                run.font.bold = True
                run.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            else:
                run.font.size = Pt(size)
                run.font.color.rgb = INK
                run.font.bold = first_col_bold and c == 0
                cell.fill.solid()
                cell.fill.fore_color.rgb = tint(header_color, 0.9) if (zebra and r % 2 == 0) else WHITE
    return tbl


def line_chart(shapes, x, y, w, h, categories, series, colors, y_min=None, y_max=None,
               title=None, size=12, legend=True, y_title=None, x_title=None):
    cd = CategoryChartData()
    cd.categories = categories
    for name, values in series:
        cd.add_series(name, values)
    gf = shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Emu(int(x)), Emu(int(y)),
                          Emu(int(w)), Emu(int(h)), cd)
    ch = gf.chart
    _style_chart(ch, title, size, legend)
    for i, s in enumerate(ch.series):
        s.format.line.color.rgb = colors[i]
        s.format.line.width = Pt(2.75)
        s.smooth = False
        s.marker.style = XL_MARKER_STYLE.CIRCLE
        s.marker.size = 7
        s.marker.format.fill.solid()
        s.marker.format.fill.fore_color.rgb = colors[i]
        s.marker.format.line.color.rgb = colors[i]
    va = ch.value_axis
    if y_min is not None:
        va.minimum_scale = y_min
    if y_max is not None:
        va.maximum_scale = y_max
    _axis_titles(ch, x_title, y_title, size)
    return ch


def xy_chart(shapes, x, y, w, h, series, colors, x_min=None, x_max=None, y_min=None,
             y_max=None, title=None, size=12, legend=True, x_title=None, y_title=None,
             line_w=2.75, dashed=None):
    cd = XyChartData()
    for name, pts in series:
        s = cd.add_series(name)
        for px, py in pts:
            s.add_data_point(px, py)
    gf = shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS, Emu(int(x)), Emu(int(y)),
                          Emu(int(w)), Emu(int(h)), cd)
    ch = gf.chart
    _style_chart(ch, title, size, legend)
    for i, s in enumerate(ch.series):
        s.format.line.color.rgb = colors[i]
        s.format.line.width = Pt(line_w)
        s.marker.style = XL_MARKER_STYLE.NONE
        if dashed and dashed[i]:
            from pptx.enum.dml import MSO_LINE_DASH_STYLE
            s.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    if x_min is not None:
        ch.category_axis.minimum_scale = x_min
    if x_max is not None:
        ch.category_axis.maximum_scale = x_max
    if y_min is not None:
        ch.value_axis.minimum_scale = y_min
    if y_max is not None:
        ch.value_axis.maximum_scale = y_max
    _axis_titles(ch, x_title, y_title, size)
    return ch


def bar_chart(shapes, x, y, w, h, categories, values, color, title=None, size=12,
              y_max=None, point_colors=None, horizontal=False):
    cd = CategoryChartData()
    cd.categories = categories
    cd.add_series("Point", values)
    kind = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = shapes.add_chart(kind, Emu(int(x)), Emu(int(y)), Emu(int(w)), Emu(int(h)), cd)
    ch = gf.chart
    _style_chart(ch, title, size, legend=False)
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.has_data_labels = True
    plot.data_labels.font.size = Pt(size + 2)
    plot.data_labels.font.bold = True
    plot.data_labels.font.color.rgb = INK
    s = ch.series[0]
    s.format.fill.solid()
    s.format.fill.fore_color.rgb = color
    if point_colors:
        for i, pc in enumerate(point_colors):
            pt = s.points[i]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = pc
    if y_max is not None:
        ch.value_axis.maximum_scale = y_max
        ch.value_axis.minimum_scale = 0
    return ch


def _style_chart(ch, title, size, legend):
    ch.font.size = Pt(size)
    ch.font.name = FONT
    ch.font.color.rgb = INK
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        tp = ch.chart_title.text_frame.paragraphs[0]
        tp.runs[0].font.size = Pt(size + 3)
        tp.runs[0].font.bold = True
    else:
        ch.has_title = False
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(size)
    try:
        ch.value_axis.major_gridlines.format.line.color.rgb = LINE
        ch.value_axis.format.line.color.rgb = LINE
        ch.category_axis.format.line.color.rgb = GREY
    except Exception:
        pass


def _axis_titles(ch, x_title, y_title, size):
    if x_title:
        ax = ch.category_axis
        ax.has_title = True
        ax.axis_title.text_frame.text = x_title
        ax.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(size)
        ax.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
    if y_title:
        ax = ch.value_axis
        ax.has_title = True
        ax.axis_title.text_frame.text = y_title
        ax.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(size)
        ax.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False


def placeholder(shapes, x, y, w, h, label, color=GREY, size=14):
    """Stiplet felt hvor eleverne selv skal indsætte et billede."""
    s = rect(shapes, x, y, w, h, fill=LIGHT, line=color, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line_w=1.5)
    s.adjustments[0] = 0.06
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    text(shapes, x, y, w, h, [("BILLEDE", {"bold": True, "size": size, "color": color}),
                              (label, {"size": size - 2, "color": GREY})],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return s


# --------------------------------------------------------------------------- diagrammer

def cells_diagram(shapes, x, y, w, h, cancer=False, color=BIO, seed=3):
    """Tegn et udsnit af hudceller: pæne lag (rask) eller kaos med invasion (kræft)."""
    rnd = random.Random(seed)
    rect(shapes, x, y, w, h, fill=tint(color, 0.93), line=tint(color, 0.5))
    membrane_y = y + h * 0.78
    vessel_h = h * 0.12
    rows, cols = 4, 7
    cw, chh = w / cols, (membrane_y - y) / rows
    cell_fill = RGBColor(0xF6, 0xD9, 0xC8)
    cell_line = RGBColor(0xC8, 0x8E, 0x74)
    nuc_ok = RGBColor(0x6A, 0x4C, 0x9C)
    nuc_bad = RGBColor(0x3B, 0x1F, 0x5C)
    for r in range(rows):
        for c in range(cols):
            if not cancer:
                cx, cy = x + c * cw + cw * 0.06, y + r * chh + chh * 0.08
                rect(shapes, cx, cy, cw * 0.88, chh * 0.84, fill=cell_fill, line=cell_line,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE, line_w=0.75)
                nd = min(cw, chh) * 0.28
                rect(shapes, cx + cw * 0.44 - nd / 2, cy + chh * 0.42 - nd / 2, nd, nd,
                     fill=nuc_ok, shape=MSO_SHAPE.OVAL)
            else:
                sc = rnd.uniform(0.7, 1.25)
                ww, hh = cw * 0.85 * sc, chh * 0.8 * rnd.uniform(0.75, 1.2)
                cx = x + c * cw + rnd.uniform(-0.1, 0.15) * cw
                cy = y + r * chh + rnd.uniform(-0.05, 0.1) * chh
                ww = min(ww, x + w - cx - 2000)
                rect(shapes, cx, cy, ww, hh, fill=cell_fill, line=cell_line, shape=MSO_SHAPE.OVAL,
                     line_w=0.75)
                nd = min(ww, hh) * rnd.uniform(0.45, 0.62)
                nshape = MSO_SHAPE.OVAL if rnd.random() > 0.35 else MSO_SHAPE.WAVE
                rect(shapes, cx + ww / 2 - nd / 2, cy + hh / 2 - nd / 2, nd, nd * rnd.uniform(0.8, 1.1),
                     fill=nuc_bad, shape=nshape)
    # basalmembran
    mem = rect(shapes, x, membrane_y, w, h * 0.025, fill=RGBColor(0x8A, 0x6A, 0x3A))
    # blodkar
    vessel = rect(shapes, x + w * 0.05, y + h * 0.84, w * 0.9, vessel_h, fill=RGBColor(0xE0, 0x6B, 0x6B),
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    vessel.adjustments[0] = 0.5
    text(shapes, x + w * 0.05, y + h * 0.84, w * 0.9, vessel_h, "blodkar", size=10, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if cancer:
        # celler der bryder gennem membranen = invasion/metastase
        for i, fx in enumerate((0.35, 0.62)):
            d = cw * 0.55
            rect(shapes, x + w * fx, membrane_y - d * 0.3, d, d * 0.85, fill=cell_fill, line=KEM,
                 shape=MSO_SHAPE.OVAL, line_w=1.5)
            rect(shapes, x + w * fx + d * 0.25, membrane_y - d * 0.05, d * 0.5, d * 0.4, fill=nuc_bad,
                 shape=MSO_SHAPE.OVAL)
        d = cw * 0.4
        rect(shapes, x + w * 0.75, y + h * 0.855, d, d * 0.7, fill=cell_fill, line=KEM, shape=MSO_SHAPE.OVAL,
             line_w=1.5)
    return mem


def hemoglobin_diagram(shapes, x, y, s, oxygen=4, size=14):
    """Hæmoglobin: 4 kæder (2 α, 2 β) med hæm + Fe²⁺ og O₂."""
    half = s / 2
    chains = [("α", PURPLE), ("β", KEM), ("β", KEM), ("α", PURPLE)]
    for i, (name, col) in enumerate(chains):
        cx = x + (i % 2) * half
        cy = y + (i // 2) * half
        blob = rect(shapes, cx + s * 0.02, cy + s * 0.02, half - s * 0.04, half - s * 0.04,
                    fill=tint(col, 0.55), line=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line_w=1.5)
        blob.adjustments[0] = 0.35
        text(shapes, cx + s * 0.05, cy + s * 0.04, half * 0.4, half * 0.3, name, size=size + 4, bold=True,
             color=col)
        hx, hy, hd = cx + half * 0.32, cy + half * 0.36, half * 0.42
        rect(shapes, hx, hy, hd, hd, fill=RGBColor(0xB0, 0x2E, 0x2E), shape=MSO_SHAPE.OCTAGON)
        fd = hd * 0.45
        rect(shapes, hx + hd / 2 - fd / 2, hy + hd / 2 - fd / 2, fd, fd, fill=RGBColor(0xF2, 0xB7, 0x05),
             shape=MSO_SHAPE.OVAL)
        text(shapes, hx, hy, hd, hd, "Fe²⁺", size=max(size - 5, 7), bold=True, color=INK,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < oxygen:
            od = hd * 0.36
            ox = hx + hd * 0.78
            oy = hy - od * 0.55
            for k in range(2):
                rect(shapes, ox + k * od * 0.8, oy, od, od, fill=FYS, line=WHITE, shape=MSO_SHAPE.OVAL,
                     line_w=0.75)
            text(shapes, ox - od * 0.1, oy - od * 0.05, od * 2, od, "O₂", size=max(size - 6, 7), bold=True,
                 color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def oximeter_diagram(shapes, x, y, w, h, size=14):
    """Skitse af fingerclip: LED (rød + IR) over fingeren, fotodiode under."""
    clip_col = RGBColor(0x3A, 0x47, 0x5C)
    top = rect(shapes, x, y, w, h * 0.22, fill=clip_col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    top.adjustments[0] = 0.4
    bot = rect(shapes, x, y + h * 0.78, w, h * 0.22, fill=clip_col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    bot.adjustments[0] = 0.4
    finger = rect(shapes, x - w * 0.08, y + h * 0.3, w * 1.0, h * 0.4, fill=RGBColor(0xF1, 0xC2, 0xA4),
                  line=RGBColor(0xC8, 0x8E, 0x74), shape=MSO_SHAPE.ROUNDED_RECTANGLE, line_w=1.25)
    finger.adjustments[0] = 0.5
    art = rect(shapes, x + w * 0.02, y + h * 0.47, w * 0.85, h * 0.06, fill=RGBColor(0xD9, 0x3B, 0x3B),
               shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    art.adjustments[0] = 0.5
    text(shapes, x + w * 0.02, y + h * 0.395, w * 0.85, h * 0.07, "arterie (pulserer)", size=size - 3,
         color=RGBColor(0x9B, 0x1C, 0x1C), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    ld = h * 0.11
    led_x = x + w * 0.55
    rect(shapes, led_x, y + h * 0.15, ld, ld, fill=RGBColor(0xFF, 0x2D, 0x2D), line=WHITE,
         shape=MSO_SHAPE.OVAL)
    rect(shapes, led_x + ld * 1.3, y + h * 0.15, ld, ld, fill=RGBColor(0x7A, 0x1F, 0x3D), line=WHITE,
         shape=MSO_SHAPE.OVAL)
    sensor = rect(shapes, led_x + ld * 0.2, y + h * 0.75, ld * 2.1, ld * 0.6, fill=RGBColor(0x1E, 0x1E, 0x1E),
                  line=WHITE)
    for k, col in ((0, RGBColor(0xFF, 0x2D, 0x2D)), (1, RGBColor(0x7A, 0x1F, 0x3D))):
        cx = led_x + ld * 0.5 + k * ld * 1.3
        arrow(shapes, cx, y + h * 0.27, cx, y + h * 0.74, color=col, width=2.5)
    text(shapes, x + w * 1.02, y + h * 0.08, w * 0.9, h * 0.25,
         [("LED: rød 660 nm", {"bold": True, "color": RGBColor(0xD0, 0x1E, 0x1E)}),
          ("LED: infrarød 940 nm", {"bold": True, "color": RGBColor(0x7A, 0x1F, 0x3D)})], size=size)
    text(shapes, x + w * 1.02, y + h * 0.74, w * 0.9, h * 0.25,
         [("Fotodiode", {"bold": True}), ("måler lyset der kommer igennem", {"color": GREY})], size=size)


def ppg_points(n=4, beats_per_sec=1.25, dc=8.0, ac=1.0, steps=24):
    """Syntetisk PPG-kurve (lys der slipper igennem) til illustration."""
    pts = []
    total = n / beats_per_sec
    for i in range(int(steps * n) + 1):
        t = total * i / (steps * n)
        phase = (t * beats_per_sec) % 1.0
        pulse = math.exp(-((phase - 0.18) ** 2) / 0.012) + 0.35 * math.exp(-((phase - 0.45) ** 2) / 0.01)
        pts.append((round(t, 3), round(dc - ac * pulse, 3)))
    return pts


def hill(p, p50, n=2.7):
    return 100 * p ** n / (p50 ** n + p ** n)
