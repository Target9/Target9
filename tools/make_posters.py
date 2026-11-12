"""Genererer 06-plancher/FFFO-plancher.pptx (A3 stående – kan skaleres til A2/A1 ved print).

Kør:  python3 tools/make_posters.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu

from fffo_design import (
    BIO, FYS, GEO, GREY, INK, KEM, LIGHT, NAVY, PURPLE, WHITE,
    arrow, bar_chart, bullets, cells_diagram, hemoglobin_diagram, hill, label_box,
    line_chart, oximeter_diagram, placeholder, ppg_points, rect, table, text, tint, xy_chart,
)

IN = 914400
W, H = 11.69 * IN, 16.54 * IN
M = 0.6 * IN
CW = W - 2 * M
OUT = Path(__file__).resolve().parent.parent / "06-plancher" / "FFFO-plancher.pptx"
YELLOW = RGBColor(0xFF, 0xD6, 0x4A)

prs = Presentation()
prs.slide_width = Emu(int(W))
prs.slide_height = Emu(int(H))
BLANK = prs.slide_layouts[6]


def poster(color, tag, title, question):
    s = prs.slides.add_slide(BLANK)
    sh = s.shapes
    rect(sh, 0, 0, W, 3.1 * IN, fill=color)
    text(sh, M, 0.45 * IN, CW, 0.5 * IN, tag, size=22, bold=True, color=tint(color, 0.6))
    text(sh, M, 0.95 * IN, CW, 1.0 * IN, title, size=50, bold=True, color=WHITE)
    text(sh, M, 2.0 * IN, CW, 1.0 * IN, question, size=19, italic=True, color=WHITE)
    rect(sh, 0, H - 0.5 * IN, W, 0.5 * IN, fill=NAVY)
    text(sh, M, H - 0.5 * IN, CW, 0.5 * IN, "FFFO · AI i sundhed – fra hudkræft til iltmætning · [navne] · 9.[x]",
         size=13, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    return s, sh


def heading(sh, x, y, w, label, color):
    rect(sh, x, y + 0.08 * IN, 0.12 * IN, 0.42 * IN, fill=color)
    text(sh, x + 0.25 * IN, y, w, 0.6 * IN, label, size=26, bold=True, color=NAVY)


def conclusion(sh, color, body, y=None):
    y = y or H - 2.15 * IN
    rect(sh, M, y, CW, 1.45 * IN, fill=tint(color, 0.82), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(sh, M + 0.3 * IN, y, CW - 0.6 * IN, 1.45 * IN,
         [[("Konklusion: ", {"bold": True, "color": color}), (body, {})]], size=18, anchor=MSO_ANCHOR.MIDDLE)


def tag_example(sh, x, y):
    t = rect(sh, x, y, 2.9 * IN, 0.38 * IN, fill=YELLOW, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    t.adjustments[0] = 0.5
    text(sh, x, y, 2.9 * IN, 0.38 * IN, "EKSEMPELDATA – udskift", size=13, bold=True, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)


half = (CW - 0.4 * IN) / 2
X2 = M + half + 0.4 * IN

# ============================================================================ 0 OVERBLIK
s, sh = poster(NAVY, "FÆLLESFAGLIGT FOKUSOMRÅDE", "AI i sundhed",
               "Hvordan kan kunstig intelligens hjælpe med at opdage sygdom og afvigelser i kroppen – og hvem får gavn af det?")
items = [("BIOLOGI", BIO, "Hvordan adskiller kræftceller i huden sig fra raske celler – og i hvor høj grad kan AI genkende hudkræft ud fra billeder?",
          "Liveforsøg: AI analyserer hudbilleder"),
         ("FYSIK", FYS, "Hvordan måler en pulsoximeter puls og iltmætning med lys – og hvordan kan AI bruge data til at opdage afvigelser?",
          "Ugeforsøg: puls og iltmætning"),
         ("KEMI", KEM, "Hvordan binder hæmoglobin ilt i blodet – og hvorfor ændrer iltmætningen sig ved fysisk aktivitet?",
          "Ugeforsøg: forklarer resultaterne"),
         ("GEOGRAFI", GEO, "Hvilke faktorer afgør, om et lands befolkning får gavn af AI i sundhed – og hvad betyder det for kræftdiagnosticering?",
          "Model + perspektivering")]
y = 3.5 * IN
for tagn, c, q, link in items:
    rect(sh, M, y, CW, 1.95 * IN, fill=tint(c, 0.88))
    rect(sh, M, y, 2.3 * IN, 1.95 * IN, fill=c)
    text(sh, M, y, 2.3 * IN, 1.95 * IN, tagn, size=24, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
    text(sh, M + 2.6 * IN, y + 0.2 * IN, CW - 2.9 * IN, 1.2 * IN, q, size=18)
    text(sh, M + 2.6 * IN, y + 1.35 * IN, CW - 2.9 * IN, 0.5 * IN, "→ " + link, size=17, bold=True, color=c)
    y += 2.12 * IN
heading(sh, M, y + 0.1 * IN, CW, "Den røde tråd", NAVY)
chain = [("Sygdom", "kræftceller ændrer huden", BIO), ("Måling", "lys gennem fingeren", FYS),
         ("Forklaring", "hæmoglobin binder ilt", KEM), ("Hvem får gavn?", "lande og hudtyper", GEO)]
bw = (CW - 3 * 0.35 * IN) / 4
for i, (h, d, c) in enumerate(chain):
    x = M + i * (bw + 0.35 * IN)
    rect(sh, x, y + 0.85 * IN, bw, 1.5 * IN, fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(sh, x + 0.1 * IN, y + 0.85 * IN, bw - 0.2 * IN, 1.5 * IN, [(h, {"bold": True, "size": 19}), (d, {"size": 14})],
         color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < 3:
        arrow(sh, x + bw + 0.03 * IN, y + 1.6 * IN, x + bw + 0.32 * IN, y + 1.6 * IN, color=NAVY, width=3)
conclusion(sh, NAVY, "AI er et stærkt hjælpeværktøj – ikke en læge. Den er kun så god som dens data og det sundhedssystem, den bruges i.",
           y=H - 2.2 * IN)

# ============================================================================ 1 BIOLOGI
s, sh = poster(BIO, "BIOLOGI", "Kræftceller og AI",
               "Hvordan adskiller kræftceller i huden sig fra raske celler – og i hvor høj grad kan AI genkende hudkræft ud fra billeder?")
y = 3.4 * IN
heading(sh, M, y, CW, "Rask hudcelle vs. kræftcelle", BIO)
cells_diagram(sh, M, y + 0.75 * IN, half, 2.6 * IN, cancer=False)
cells_diagram(sh, X2, y + 0.75 * IN, half, 2.6 * IN, cancer=True, seed=11)
text(sh, M, y + 3.4 * IN, half, 0.4 * IN, "Rask: ordnede lag, små runde kerner", size=16, bold=True, color=BIO,
     align=PP_ALIGN.CENTER)
text(sh, X2, y + 3.4 * IN, half, 0.4 * IN, "Kræft: stor uregelmæssig kerne + invasion", size=16, bold=True, color=KEM,
     align=PP_ALIGN.CENTER)
y += 3.95 * IN
label_box(sh, M, y, half, 2.6 * IN, "Bilmodellen",
          ["• Speeder = proto-onkogener", "• Bremse = tumorsuppressorgener (p53)", "• Mekaniker = DNA-reparation",
           "• Skrotplads = apoptose", "• Kræft: speeder i bund + ingen bremse"], BIO, size=15)
label_box(sh, X2, y, half, 2.6 * IN, "ABCDE-reglen",
          ["• Asymmetri", "• Border: uregelmæssig kant", "• Color: flere farver", "• Diameter > 6 mm",
           "• Evolution: ændrer sig"], BIO, size=15)
y += 2.9 * IN
heading(sh, M, y, CW, "Liveforsøg: AI analyserer hudbilleder", BIO)
tag_example(sh, W - M - 2.9 * IN, y + 0.1 * IN)
pw = (CW - 3 * 0.25 * IN) / 4
for i, (lbl, c) in enumerate((("godartet", BIO), ("melanom", KEM), ("svært", GEO), ("AI tager fejl", PURPLE))):
    placeholder(sh, M + i * (pw + 0.25 * IN), y + 0.75 * IN, pw, 1.4 * IN, lbl, color=c, size=13)
rows = [["", "AI: ondartet", "AI: godartet"], ["Er ondartet", "17 (SP)", "3 (FN)"], ["Er godartet", "4 (FP)", "16 (SN)"]]
table(sh, M, y + 2.35 * IN, half, 1.35 * IN, rows, BIO, size=15, first_col_bold=True)
text(sh, X2, y + 2.3 * IN, half, 1.5 * IN,
     [[("Træfsikkerhed ", {"bold": True}), ("82,5 %", {"bold": True, "color": BIO})],
      [("Sensitivitet ", {"bold": True}), ("85 % ", {"bold": True, "color": BIO}), ("(17/20 fundet)", {"color": GREY})],
      [("Specificitet ", {"bold": True}), ("80 % ", {"bold": True, "color": BIO}), ("(16/20 frikendt)", {"color": GREY})]],
     size=17)
conclusion(sh, BIO, "AI kan genkende hudkræft lige så godt som hudlæger på gode billeder – men kun så godt som dens træningsdata. "
                    "Diagnosen stilles ved biopsi.")

# ============================================================================ 2 FYSIK
s, sh = poster(FYS, "FYSIK", "Pulsoximeteret",
               "Hvordan måler en pulsoximeter puls og iltmætning med lys – og hvordan kan AI bruge data til at opdage afvigelser?")
y = 3.4 * IN
heading(sh, M, y, CW, "Sådan virker det", FYS)
oximeter_diagram(sh, M + 0.4 * IN, y + 0.8 * IN, 2.3 * IN, 2.4 * IN, size=14)
xy_chart(sh, X2 + 0.2 * IN, y + 0.65 * IN, half - 0.2 * IN, 2.75 * IN, [("PPG", ppg_points(n=3))], [FYS], y_min=6.6,
         y_max=8.2, legend=False, size=12, x_title="tid (s)", x_min=0, x_max=2.4, title="PPG-signal: AC pulserer, DC konstant")
y += 3.5 * IN
rows = [["", "Rødt 660 nm", "IR 940 nm"], ["Hb (uden ilt)", "MEGET", "lidt"], ["HbO₂ (med ilt)", "meget lidt", "lidt mere"]]
table(sh, M, y, half, 1.5 * IN, rows, FYS, size=15, first_col_bold=True)
fb = rect(sh, X2, y, half, 1.5 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, X2, y, half, 1.5 * IN, [("E = h·c / λ", {"size": 28, "bold": True}), ("puls = 60 / T", {"size": 22, "bold": True}),
                                  ("SpO₂ ≈ 110 − 25·R", {"size": 18})], color=WHITE, align=PP_ALIGN.CENTER,
     anchor=MSO_ANCHOR.MIDDLE, line_spacing=0.95)
y += 1.85 * IN
heading(sh, M, y, CW, "Ugeforsøg: Find din egen normal", FYS)
tag_example(sh, W - M - 2.9 * IN, y + 0.1 * IN)
bar_chart(sh, M, y + 0.65 * IN, half, 2.85 * IN, ["rød", "grøn", "blå"], (235, 40, 5), FYS, title="Mobil-PPG: lys gennem fingeren (DC)",
          size=11, y_max=255, point_colors=[KEM, BIO, FYS])
bar_chart(sh, X2, y + 0.65 * IN, half, 2.85 * IN, ["Morgen", "Skole", "Efter akt.", "Aften"], (66, 73, 131, 69), PURPLE,
          title="Måledagbog: gns. puls · SpO₂ stabil 97–98 %", size=11, y_max=150)
y += 3.65 * IN
label_box(sh, M, y, half, 1.85 * IN, "AI-blindtest (8 fejlmålinger)",
          ["• Gruppemodel: fandt 4 af 8", "• Personlig model: fandt 8 af 8", "• Færre falske alarmer efter aktivitet"], PURPLE, size=14)
label_box(sh, X2, y, half, 1.85 * IN, "Fejlkilder",
          ["• Bevægelse og kolde fingre", "• Neglelak og lys udefra", "• Mørk hud (bias)"], KEM, size=14)
conclusion(sh, FYS, "Blodet absorberer lys forskelligt afhængigt af bølgelængden – mobilen kunne måle pulsen, men ikke ilten. "
                    "SpO₂ var stabil, så AI'en fandt fejlmålingerne bedst, når den kendte personens egen normal og situationen.")

# ============================================================================ 3 KEMI
s, sh = poster(KEM, "KEMI", "Hæmoglobin og ilt",
               "Hvordan binder hæmoglobin ilt i blodet – og hvorfor ændrer iltmætningen sig ved fysisk aktivitet?")
y = 3.4 * IN
heading(sh, M, y, CW, "Hæmoglobin", KEM)
hemoglobin_diagram(sh, M + 0.3 * IN, y + 0.8 * IN, 3.6 * IN, oxygen=4, size=15)
bullets(sh, X2 - 0.3 * IN, y + 0.85 * IN, half + 0.3 * IN, 3.6 * IN,
        [("Protein ", "i de røde blodlegemer"), ("4 kæder ", "(2 α + 2 β)"), ("Hæmgruppe ", "med jern-ion Fe²⁺"),
         ("4 × O₂ ", "pr. hæmoglobin"), ("Reversibel ", "binding – fanges i lungerne, slippes i musklerne")],
        size=17, bullet_color=KEM)
y += 4.7 * IN
eq = rect(sh, M, y, CW, 0.9 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, M, y, CW, 0.9 * IN, "Hb + 4 O₂  ⇌  Hb(O₂)₄", size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
     anchor=MSO_ANCHOR.MIDDLE)
y += 1.1 * IN
curve_n = [(p / 4, round(hill(p / 4, 3.6), 2)) for p in range(0, 61)]
curve_w = [(p / 4, round(hill(p / 4, 4.4), 2)) for p in range(0, 61)]
xy_chart(sh, M, y, half, 3.4 * IN, [("Hvile", curve_n), ("Arbejde (Bohr)", curve_w)], [KEM, PURPLE],
         x_min=0, x_max=15, y_min=0, y_max=100, size=10, x_title="pO₂ (kPa)", y_title="iltmætning (%)",
         title="S-formet bindingskurve", dashed=[False, True])
line_chart(sh, X2, y, half, 3.4 * IN, ["20 °C", "30 °C", "40 °C"], [("Tid", (61.7, 32.7, 16.7))], [KEM], y_min=0, y_max=70,
           title="Den blå flaske: tid til farveløs (s)", size=10, legend=False)
tag_example(sh, W - M - 3.0 * IN, y + 0.6 * IN)
y += 3.55 * IN
bullets(sh, M, y, CW, 1.3 * IN,
        [("Lunger: ", "meget O₂ → Hb binder (97 %) · Muskler: lidt O₂ → afgiver · Bohr: CO₂, H⁺ og varme → slipper ilt lettere"),
         ("Blå flaske: ", "ryst = ilt ind (lunger), glukose = iltforbrug (respiration). Varmere → hurtigere forbrug → ryst oftere.")],
        size=14, bullet_color=KEM, gap=0.4)
conclusion(sh, KEM, "SpO₂ var stabil i alle situationer: Arterieblodet bliver mættet i lungerne (flad top), og vejrtrækningen "
                    "følger med forbruget – ligesom den blå flaske forbliver blå, når man ryster oftere. Iltafgivelsen sker i musklerne (Bohr).")

# ============================================================================ 4 GEOGRAFI
s, sh = poster(GEO, "GEOGRAFI", "Hvem får gavn af AI?",
               "Hvilke faktorer afgør, om et lands befolkning får gavn af AI i sundhed – og hvad betyder det for kræftdiagnosticering?")
y = 3.4 * IN
heading(sh, M, y, CW, "Hvor er hudkræft mest udbredt?", GEO)
placeholder(sh, M, y + 0.75 * IN, CW, 3.0 * IN, "verdenskort: modermærkekræft pr. 100.000 (GLOBOCAN) – farvelæg selv", color=GEO)
y += 4.0 * IN
heading(sh, M, y, CW, "AI-parathedsmodellen", GEO)
rows = [["Faktor", "DK", "AUS", "USA", "IND", "NGA"], ["Økonomi", "5", "5", "5", "2", "1"],
        ["Infrastruktur", "5", "5", "4", "3", "2"], ["Personale", "5", "5", "4", "2", "1"],
        ["Lige adgang", "5", "4", "2", "2", "1"], ["Data (hudtype)", "5", "5", "3", "2", "1"],
        ["Lovgivning", "5", "4", "4", "3", "2"], ["I alt / 30", "30", "28", "22", "14", "8"]]
table(sh, M, y + 0.75 * IN, half, 3.6 * IN, rows, GEO, size=14, col_widths=[2.4, 0.8, 0.8, 0.8, 0.8, 0.8],
      first_col_bold=True)
bar_chart(sh, X2, y + 0.65 * IN, half, 3.8 * IN, ["DK", "AUS", "USA", "IND", "NGA"], (30, 28, 22, 14, 8), GEO,
          size=12, y_max=30, point_colors=[GEO, tint(GEO, 0.15), tint(GEO, 0.35), tint(KEM, 0.2), KEM],
          title="AI-parathed")
y += 4.65 * IN
label_box(sh, M, y, half, 2.35 * IN, "AI-paradokset",
          ["• Størst behov: få læger", "• Men dårligst adgang", "• Bias: AI trænet på lys hud"], GEO, size=15)
label_box(sh, X2, y, half, 2.35 * IN, "Kræftdiagnose",
          ["• DK: triage, kortere ventetid", "• Indien: smartphone-AI i landsbyer", "• Kræver behandling bagefter"], GEO, size=15)
conclusion(sh, GEO, "Økonomi, infrastruktur, sundhedspersonale, lige adgang og data om alle hudtyper afgør, om AI gavner. "
                    "Uden det risikerer AI at øge den globale ulighed i kræftdiagnosticering.")

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print("Gemt:", OUT, "plancher:", len(prs.slides))
