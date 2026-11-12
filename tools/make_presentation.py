"""Genererer 05-powerpoint/FFFO-praesentation.pptx.

Kør:  python3 tools/make_presentation.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

from fffo_design import (
    BIO, FYS, GEO, GREY, INK, KEM, LIGHT, LINE, NAVY, PURPLE, SUBJECT, WHITE,
    arrow, bar_chart, bullets, cells_diagram, hemoglobin_diagram, hill, label_box,
    line_chart, oximeter_diagram, placeholder, ppg_points, rect, table, text, tint, xy_chart,
)

IN = 914400
W, H = 13.333 * IN, 7.5 * IN
OUT = Path(__file__).resolve().parent.parent / "05-powerpoint" / "FFFO-praesentation.pptx"

prs = Presentation()
prs.slide_width = Emu(int(W))
prs.slide_height = Emu(int(H))
BLANK = prs.slide_layouts[6]
slide_no = [0]


def new_slide(subject, title, notes, subtitle=None):
    slide_no[0] += 1
    s = prs.slides.add_slide(BLANK)
    color, tag = SUBJECT[subject]
    sh = s.shapes
    rect(sh, 0, 0, 0.16 * IN, H, fill=color)
    text(sh, 0.6 * IN, 0.32 * IN, 6 * IN, 0.3 * IN, tag, size=13, bold=True, color=color)
    text(sh, 0.6 * IN, 0.58 * IN, 12.2 * IN, 0.75 * IN, title, size=32, bold=True, color=NAVY)
    if subtitle:
        text(sh, 0.6 * IN, 1.28 * IN, 12.2 * IN, 0.4 * IN, subtitle, size=16, color=GREY)
    rect(sh, 0.6 * IN, 7.0 * IN, 12.1 * IN, 0.012 * IN, fill=LINE)
    text(sh, 0.6 * IN, 7.06 * IN, 8 * IN, 0.3 * IN, "FFFO · AI i sundhed – fra hudkræft til iltmætning",
         size=11, color=GREY)
    text(sh, 11.7 * IN, 7.06 * IN, 1.0 * IN, 0.3 * IN, str(slide_no[0]), size=11, color=GREY,
         align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes.strip()
    return s, sh, color


def example_tag(sh, x, y, w=2.6):
    tag = rect(sh, x, y, w * IN, 0.34 * IN, fill=RGB_YELLOW, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tag.adjustments[0] = 0.5
    text(sh, x, y, w * IN, 0.34 * IN, "EKSEMPELDATA – udskift", size=12, bold=True, color=INK,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


from pptx.dml.color import RGBColor  # noqa: E402

RGB_YELLOW = RGBColor(0xFF, 0xD6, 0x4A)

# ============================================================================ 1 TITEL
slide_no[0] += 1
s = prs.slides.add_slide(BLANK)
sh = s.shapes
rect(sh, 0, 0, W, H, fill=NAVY)
for i, c in enumerate((BIO, FYS, KEM, GEO)):
    rect(sh, i * W / 4, H - 0.22 * IN, W / 4, 0.22 * IN, fill=c)
text(sh, 0.9 * IN, 1.2 * IN, 11 * IN, 0.5 * IN, "FÆLLESFAGLIGT FOKUSOMRÅDE · BIOLOGI · FYSIK/KEMI · GEOGRAFI",
     size=15, bold=True, color=tint(FYS, 0.45))
text(sh, 0.9 * IN, 1.85 * IN, 11.5 * IN, 2.2 * IN,
     [("AI i sundhed", {"size": 66, "bold": True, "color": WHITE}),
      ("fra hudkræft til iltmætning", {"size": 40, "color": tint(GEO, 0.35)})], line_spacing=0.95)
text(sh, 0.9 * IN, 4.6 * IN, 11 * IN, 0.9 * IN,
     "Hvordan kan kunstig intelligens hjælpe med at opdage sygdom og afvigelser i kroppen – og hvem får gavn af det?",
     size=20, italic=True, color=tint(NAVY, 0.75))
text(sh, 0.9 * IN, 5.9 * IN, 11 * IN, 0.5 * IN, "[Navn 1] · [Navn 2] · [Navn 3] · [Navn 4]   |   9. [x] · [Skole] · 2026",
     size=18, color=WHITE)
s.notes_slide.notes_text_frame.text = (
    "P1: Hej, og velkommen. Vi er [navne], og vores emne er AI i sundhed – fra hudkræft til iltmætning.\n"
    "Kunstig intelligens bruges mere og mere på hospitaler – vi ville finde ud af, hvordan det virker, og om det virker lige godt for alle.\n\n"
    "STIKORD: navne · AI i sundhed · virker det for alle?"
)

# ============================================================================ 2 PROBLEMFORMULERING
s, sh, col = new_slide("all", "Problemformulering", """
P1: Overordnet problemformulering: Hvordan kan kunstig intelligens hjælpe med at opdage sygdom og afvigelser i kroppen – og hvem får gavn af det?
Fire underspørgsmål – ét pr. fag. Biologi = liveforsøg. Fysik = pulsoximeter + AI. Kemi = hæmoglobin forklarer ugeforsøget. Geografi = hvilke lande får gavn.
Rød tråd: AI skal kende forskel på NORMALT og AFVIGENDE ud fra DATA.
OVERGANG: "Vi starter med biologien – hvad er det egentlig, AI'en skal finde?"
""")
q = rect(sh, 0.6 * IN, 1.45 * IN, 12.1 * IN, 1.05 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
q.adjustments[0] = 0.15
text(sh, 0.9 * IN, 1.45 * IN, 11.6 * IN, 1.05 * IN,
     "Hvordan kan kunstig intelligens hjælpe med at opdage sygdom og afvigelser i kroppen – og hvem får gavn af det?",
     size=22, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
cards = [
    ("BIOLOGI", BIO, "Hvordan adskiller kræftceller i huden sig fra raske celler – og i hvor høj grad kan AI genkende hudkræft ud fra billeder?", "Liveforsøg: AI analyserer hudbilleder"),
    ("FYSIK", FYS, "Hvordan måler en pulsoximeter puls og iltmætning med lys – og hvordan kan AI bruge data til at opdage afvigelser?", "Ugeforsøg: puls og iltmætning"),
    ("KEMI", KEM, "Hvordan binder hæmoglobin ilt i blodet – og hvorfor ændrer iltmætningen sig ved fysisk aktivitet?", "Ugeforsøg: forklarer resultaterne"),
    ("GEOGRAFI", GEO, "Hvilke faktorer afgør, om et lands befolkning får gavn af AI i sundhed – og hvad betyder det for kræftdiagnosticering?", "Model + perspektivering"),
]
cw = 2.9 * IN
for i, (tag, c, qq, link) in enumerate(cards):
    x = 0.6 * IN + i * (cw + 0.167 * IN)
    rect(sh, x, 2.75 * IN, cw, 3.55 * IN, fill=tint(c, 0.9))
    rect(sh, x, 2.75 * IN, cw, 0.5 * IN, fill=c)
    text(sh, x, 2.75 * IN, cw, 0.5 * IN, tag, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
    text(sh, x + 0.2 * IN, 3.4 * IN, cw - 0.4 * IN, 2.1 * IN, qq, size=15)
    rect(sh, x + 0.2 * IN, 5.55 * IN, cw - 0.4 * IN, 0.012 * IN, fill=c)
    text(sh, x + 0.2 * IN, 5.62 * IN, cw - 0.4 * IN, 0.6 * IN, link, size=13, bold=True, color=c)
text(sh, 0.6 * IN, 6.45 * IN, 12.1 * IN, 0.45 * IN,
     [[("Rød tråd: ", {"bold": True, "color": NAVY}),
       ("AI skal ud fra data kende forskel på normalt og afvigende – i billeder af huden og i lys gennem fingeren.", {})]],
     size=16)

# ============================================================================ 3 HUDEN
s, sh, col = new_slide("bio", "Huden og de tre typer hudkræft", """
P1 (0:45): Huden = overhud, læderhud, underhud. Næsten al hudkræft opstår i OVERHUDEN – meget celledeling + UV.
Tre typer: basalcellekarcinom (hyppigst, spreder sig sjældent), planocellulært karcinom (pladeceller), melanom (melanocytter – farligst, spreder sig tidligt).
STIKORD: 3 lag · overhud · UV · basalcelle · planocellulær · melanom = farligst
""")
layers = [("Overhud (epidermis)", "pladeceller · basalceller · melanocytter", RGBColor(0xF6, 0xD9, 0xC8), 1.0),
          ("Læderhud (dermis)", "blodkar · nerver · bindevæv · hårsække", RGBColor(0xEE, 0xB8, 0xA2), 1.5),
          ("Underhud (subcutis)", "fedtvæv", RGBColor(0xF7, 0xE7, 0xB4), 1.1)]
y = 1.6 * IN
for name, desc, fillc, hh in layers:
    rect(sh, 0.6 * IN, y, 5.6 * IN, hh * IN, fill=fillc, line=WHITE)
    text(sh, 0.8 * IN, y + 0.12 * IN, 5.2 * IN, hh * IN - 0.2 * IN,
         [(name, {"bold": True, "size": 18}), (desc, {"size": 14, "color": GREY})], size=16)
    y += hh * IN
sun = rect(sh, 5.35 * IN, 1.35 * IN, 0.7 * IN, 0.7 * IN, fill=RGB_YELLOW, shape=MSO_SHAPE.SUN)
text(sh, 4.05 * IN, 1.48 * IN, 1.3 * IN, 0.4 * IN, "UV-lys", size=14, bold=True, color=RGBColor(0xB5, 0x7A, 0x00),
     align=PP_ALIGN.RIGHT)
text(sh, 0.6 * IN, 5.3 * IN, 5.6 * IN, 1.5 * IN,
     [[("Hvorfor overhuden? ", {"bold": True}),
       ("Basalcellerne deler sig hele tiden, og UV-lyset rammer netop her. Flere delinger = flere chancer for fejl i DNA.", {})]],
     size=15)
types = [("Basalcellekarcinom", "Fra basalcellerne. Den hyppigste. Vokser langsomt og spreder sig næsten aldrig.", 0.82),
         ("Planocellulært karcinom", "Fra pladecellerne (keratinocytter). Kan sprede sig, hvis det ikke behandles.", 0.75),
         ("Modermærkekræft (melanom)", "Fra melanocytterne, der laver pigmentet melanin. Den farligste – kan sprede sig tidligt.", 0.0)]
y = 1.6 * IN
for name, desc, t in types:
    fillc = tint(KEM, 0.88) if t == 0.0 else tint(BIO, t + 0.08)
    accent = KEM if t == 0.0 else BIO
    rect(sh, 6.7 * IN, y, 6.0 * IN, 1.55 * IN, fill=fillc)
    rect(sh, 6.7 * IN, y, 0.1 * IN, 1.55 * IN, fill=accent)
    text(sh, 7.0 * IN, y + 0.15 * IN, 5.6 * IN, 1.3 * IN,
         [(name, {"bold": True, "size": 20, "color": accent}), (desc, {"size": 16})])
    y += 1.75 * IN

# ============================================================================ 4 RASK VS KRÆFT
s, sh, col = new_slide("bio", "Rask hudcelle vs. kræftcelle", """
P1 (1:15): Forskellen er genetisk, morfologisk og biologisk.
GENETISK: mutationer = permanente ændringer i DNA-sekvensen (fx UV-skade).
MORFOLOGISK: stor uregelmæssig kerne = nukleær atypi, forskellig størrelse, mange i deling (mitoser).
BIOLOGISK: raske bliver i vævet – kræftceller invaderer og metastaserer via blod/lymfe.
PEG på tegningen: cellerne der bryder gennem basalmembranen ned mod blodkarret.
""")
cells_diagram(sh, 0.6 * IN, 1.55 * IN, 3.3 * IN, 2.9 * IN, cancer=False)
cells_diagram(sh, 4.1 * IN, 1.55 * IN, 3.3 * IN, 2.9 * IN, cancer=True, seed=11)
text(sh, 0.6 * IN, 4.5 * IN, 3.3 * IN, 0.4 * IN, "Rask hud: ordnede lag", size=15, bold=True, color=BIO,
     align=PP_ALIGN.CENTER)
text(sh, 4.1 * IN, 4.5 * IN, 3.3 * IN, 0.4 * IN, "Kræft: kaos + invasion", size=15, bold=True, color=KEM,
     align=PP_ALIGN.CENTER)
rows = [["", "Rask hudcelle", "Kræftcelle"],
        ["Genetisk", "Intakt DNA og reparation", "Mutationer i proto-onkogener og tumor-suppressorgener"],
        ["Morfologisk", "Ens størrelse, lille rund kerne", "Stor, uregelmæssig kerne (nukleær atypi), mange mitoser"],
        ["Celledød", "Apoptose ved DNA-skade", "Undgår apoptose"],
        ["Væv", "Bliver i sit væv", "Invaderer nabovæv og metastaserer (blod/lymfe)"]]
table(sh, 7.7 * IN, 1.55 * IN, 5.0 * IN, 4.0 * IN, rows, BIO, size=13, col_widths=[1.45, 1.5, 2.15],
      first_col_bold=True)
text(sh, 0.6 * IN, 5.15 * IN, 6.8 * IN, 1.6 * IN,
     [[("Mutation: ", {"bold": True}), ("permanent ændring i arvematerialets sekvens.", {})],
      [("Nukleær atypi: ", {"bold": True}), ("unormal, stor og uregelmæssig cellekerne.", {})],
      [("Metastase: ", {"bold": True}), ("kræftceller spredt til andre organer via blod eller lymfe.", {})]],
     size=15)

# ============================================================================ 5 BILMODELLEN
s, sh, col = new_slide("bio", "Model: Cellen som en bil", """
P1 (1:00): Bilmodellen. Proto-onkogener = speederen. Tumorsuppressorgener (p53) = bremsen. DNA-reparation = mekanikeren. Apoptose = skrotpladsen.
I kræftcellen: speederen sidder fast i bund + bremserne virker ikke + cellen undgår skrotpladsen.
Kræver typisk FLERE fejl på én gang – derfor stiger risikoen med alderen.
BEGRÆNSNING: en celle har mange speedere og bremser – modellen viser heller ikke invasion/metastase.
(Kan springes over hvis I mangler tid – tag den ved spørgsmål.)
""", subtitle="Kræft kræver typisk flere fejl på én gang")
parts = [("Speeder", "Proto-onkogener", "sætter gang i celledeling", "Muteret → onkogen: speederen sidder fast i bund"),
         ("Bremse", "Tumorsuppressorgener (fx p53)", "stopper celledeling ved skader", "Muteret → bremsen virker ikke"),
         ("Mekaniker", "DNA-reparation", "retter fejl i DNA", "Muteret → fejl bliver ikke rettet"),
         ("Skrotplads", "Apoptose", "programmeret celledød", "Kræftcellen undgår skrotpladsen")]
cw = 2.9 * IN
for i, (car, cell, func, bad) in enumerate(parts):
    x = 0.6 * IN + i * (cw + 0.167 * IN)
    rect(sh, x, 1.9 * IN, cw, 2.2 * IN, fill=tint(BIO, 0.88))
    text(sh, x, 2.0 * IN, cw, 0.6 * IN, car.upper(), size=24, bold=True, color=BIO, align=PP_ALIGN.CENTER)
    text(sh, x + 0.15 * IN, 2.65 * IN, cw - 0.3 * IN, 1.4 * IN,
         [(cell, {"bold": True, "size": 17}), (func, {"size": 15, "color": GREY})], align=PP_ALIGN.CENTER)
    arrow(sh, x + cw / 2, 4.15 * IN, x + cw / 2, 4.6 * IN, color=KEM, width=3)
    rect(sh, x, 4.65 * IN, cw, 1.2 * IN, fill=tint(KEM, 0.88))
    text(sh, x + 0.15 * IN, 4.65 * IN, cw - 0.3 * IN, 1.2 * IN, bad, size=15, color=RGBColor(0x8E, 0x1F, 0x1F),
         bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(sh, 0.6 * IN, 6.1 * IN, 12.1 * IN, 0.8 * IN,
     [[("Modellens begrænsning: ", {"bold": True}),
       ("En rigtig celle har mange 'speedere' og 'bremser', og modellen viser ikke invasion og metastasering.", {})]],
     size=15, color=GREY)

# ============================================================================ 6 FRA CELLER TIL BILLEDER
s, sh, col = new_slide("bio", "Fra celler til billeder: ABCDE og AI", """
P1 (1:00): Lægen kan ikke se cellerne med det blotte øje – men forandringerne kan ses på huden: ABCDE-reglen.
AI ser billedet som TAL (pixels: rød/grøn/blå 0–255). Trænes på tusindvis af billeder med kendt svar – lærer selv mønstre der minder om ABCDE.
VIGTIGT: AI ser OVERFLADEN – endelig diagnose = biopsi i mikroskop.
""")
abc = [("A", "Asymmetri", "halvdelene er ikke ens"), ("B", "Border (kant)", "uskarp, takket kant"),
       ("C", "Color (farve)", "flere farver"), ("D", "Diameter", "større end ca. 6 mm"),
       ("E", "Evolution", "ændrer sig over tid")]
y = 1.55 * IN
for letter, name, desc in abc:
    b = rect(sh, 0.6 * IN, y, 0.75 * IN, 0.75 * IN, fill=BIO, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(sh, 0.6 * IN, y, 0.75 * IN, 0.75 * IN, letter, size=30, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
    text(sh, 1.55 * IN, y + 0.02 * IN, 4.2 * IN, 0.75 * IN,
         [(name, {"bold": True, "size": 18}), (desc, {"size": 14, "color": GREY})], line_spacing=0.95)
    y += 0.9 * IN
steps = [("Billede", "pixels = tal\n(R, G, B: 0–255)"), ("Lag 1", "kanter\nog farver"), ("Lag 2", "former:\nrund? takket?"),
         ("Lag 3", "mønstre: asymmetri,\nflere farver"), ("Svar", "87 % ondartet\n13 % godartet")]
x0, y0, bw, bh = 6.1 * IN, 1.6 * IN, 6.6 * IN, 0.62 * IN
for i, (name, desc) in enumerate(steps):
    yy = y0 + i * 0.86 * IN
    shrink = i * 0.35 * IN
    c = NAVY if i in (0, 4) else tint(BIO, 0.25 + 0.15 * (i - 1))
    rr = rect(sh, x0 + shrink, yy, bw - 2 * shrink, bh, fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(sh, x0 + shrink, yy, bw - 2 * shrink, bh,
         [[(name + ":  ", {"bold": True, "color": WHITE}), (desc.replace("\n", " "), {"color": WHITE})]], size=15,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < 4:
        arrow(sh, x0 + bw / 2, yy + bh, x0 + bw / 2, yy + 0.86 * IN, color=GREY, width=2)
note = rect(sh, 6.1 * IN, 6.0 * IN, 6.6 * IN, 0.8 * IN, fill=tint(KEM, 0.88), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 6.3 * IN, 6.0 * IN, 6.3 * IN, 0.8 * IN,
     [[("Husk: ", {"bold": True, "color": KEM}),
       ("AI ser hudens overflade, ikke cellerne. Diagnosen stilles ved biopsi og mikroskopi.", {})]],
     size=14, anchor=MSO_ANCHOR.MIDDLE)

# ============================================================================ 7 LIVEFORSØG
s, sh, col = new_slide("bio", "LIVEFORSØG: AI analyserer hudbilleder", """
P1 (2:00 – DET VIGTIGSTE): Model trænet i Teachable Machine på 160 billeder fra ISIC (80 godartede + 80 melanomer).
Billede 1: godartet – symmetrisk, ensartet farve, skarp kant → AI siger godartet __ %.
Billede 2: melanom – asymmetrisk, flere farver → ondartet __ %.
Billede 3: svært billede → AI usikker (__/__).
Billede 4: AI TAGER FEJL – falsk negativ = farligst (patient sendt hjem).
HVIS TEKNIKKEN SVIGTER: "Vi har optaget demoen i forvejen" → start backup-video.
SKIFT TIL BROWSEREN NU (Alt+Tab).
""", subtitle="Teachable Machine · trænet på 160 billeder fra ISIC Archive (80 godartede, 80 melanomer)")
demo = [("1", "Tydeligt godartet", "symmetrisk · én farve · skarp kant", BIO),
        ("2", "Tydeligt melanom", "asymmetrisk · flere farver · uskarp kant", KEM),
        ("3", "Svært billede", "AI er usikker (fx 55 / 45 %)", GEO),
        ("4", "AI tager fejl", "falsk negativ = farligst", PURPLE)]
cw = 2.9 * IN
for i, (n, name, desc, c) in enumerate(demo):
    x = 0.6 * IN + i * (cw + 0.167 * IN)
    placeholder(sh, x, 1.85 * IN, cw, 2.5 * IN, f"testbillede {n}", color=c)
    text(sh, x, 4.45 * IN, cw, 0.4 * IN, f"{n}. {name}", size=18, bold=True, color=c)
    text(sh, x, 4.85 * IN, cw, 0.4 * IN, desc, size=14, color=GREY)
    rect(sh, x, 5.35 * IN, cw, 0.55 * IN, fill=LIGHT, line=LINE)
    text(sh, x + 0.15 * IN, 5.35 * IN, cw - 0.3 * IN, 0.55 * IN, "AI siger: ________  ___ %", size=15,
         anchor=MSO_ANCHOR.MIDDLE)
live = rect(sh, 0.6 * IN, 6.1 * IN, 12.1 * IN, 0.7 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 0.6 * IN, 6.1 * IN, 12.1 * IN, 0.7 * IN, "▶  Skift til Teachable Machine (Preview → File)   ·   Backup: video af demoen",
     size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ============================================================================ 8 AI-RESULTATER
s, sh, col = new_slide("bio", "Resultat: Hvor god er vores AI?", """
P1 (1:00): Testet på 40 billeder den ALDRIG har set. Træfsikkerhed __ %.
Sensitivitet __ % (fandt __ af 20 melanomer). Specificitet __ % (frikendte __ af 20 godartede).
Forskning: Esteva 2017 + Haenssle 2018 – professionel AI (100.000+ billeder) lige så god som hudlæger.
Fejlkilder: få data, næsten kun lys hud, genveje (pennestreger – Winkler 2019).
SVAR: AI kan i høj grad genkende hudkræft – men KUN SÅ GODT SOM DATA.
OVERGANG: "AI'en i biologi ser på lys, der kastes tilbage fra huden. [P2] viser nu, hvordan lys også kan måle INDE i kroppen."
""", subtitle="Test på 40 billeder, som modellen aldrig havde set (20 melanomer, 20 godartede)")
example_tag(sh, 0.6 * IN, 1.75 * IN)
mx, my, cs = 0.6 * IN, 2.3 * IN, 1.55 * IN
text(sh, mx + 1.7 * IN, my - 0.05 * IN, 2 * cs, 0.35 * IN, "AI siger …", size=13, bold=True, color=GREY,
     align=PP_ALIGN.CENTER)
heads = ["ondartet", "godartet"]
for j, hname in enumerate(heads):
    text(sh, mx + 1.7 * IN + j * cs, my + 0.25 * IN, cs, 0.35 * IN, hname, size=14, bold=True,
         align=PP_ALIGN.CENTER)
for i, rname in enumerate(["Er ondartet", "Er godartet"]):
    text(sh, mx, my + 0.65 * IN + i * cs, 1.65 * IN, cs, rname, size=14, bold=True, anchor=MSO_ANCHOR.MIDDLE)
cellsdata = [[("17", "Sand positiv", BIO), ("3", "Falsk negativ", KEM)],
             [("4", "Falsk positiv", GEO), ("16", "Sand negativ", BIO)]]
for i in range(2):
    for j in range(2):
        n, lbl, c = cellsdata[i][j]
        x, y = mx + 1.7 * IN + j * cs, my + 0.65 * IN + i * cs
        rect(sh, x + 0.04 * IN, y + 0.04 * IN, cs - 0.08 * IN, cs - 0.08 * IN, fill=tint(c, 0.7))
        text(sh, x, y + 0.15 * IN, cs, cs - 0.3 * IN,
             [(n, {"size": 34, "bold": True, "color": INK}), (lbl, {"size": 13, "color": INK})],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=0.9)
stats = [("82,5 %", "Træfsikkerhed", "(17 + 16) / 40"), ("85 %", "Sensitivitet", "17 / 20 melanomer fundet"),
         ("80 %", "Specificitet", "16 / 20 godartede frikendt")]
for i, (v, n, d) in enumerate(stats):
    y = 1.75 * IN + i * 1.05 * IN
    rect(sh, 5.35 * IN, y, 3.4 * IN, 0.92 * IN, fill=tint(BIO, 0.88))
    text(sh, 5.5 * IN, y, 1.6 * IN, 0.92 * IN, v, size=26, bold=True, color=BIO, anchor=MSO_ANCHOR.MIDDLE)
    text(sh, 7.05 * IN, y + 0.08 * IN, 1.7 * IN, 0.8 * IN, [(n, {"bold": True, "size": 15}), (d, {"size": 11, "color": GREY})],
         anchor=MSO_ANCHOR.MIDDLE, line_spacing=0.95)
label_box(sh, 9.0 * IN, 1.75 * IN, 3.7 * IN, 2.05 * IN, "Forskning",
          ["• Esteva 2017: AI lige så god som 21 hudlæger",
           "• Haenssle 2018: AI bedre end de fleste af 58 hudlæger"], BIO, size=13)
label_box(sh, 9.0 * IN, 3.95 * IN, 3.7 * IN, 2.0 * IN, "Fejlkilder",
          ["• Kun 160 træningsbilleder",
           "• Næsten kun lys hud",
           "• Genveje: pen, lineal, hår"], KEM, size=13)
concl = rect(sh, 0.6 * IN, 6.1 * IN, 12.1 * IN, 0.7 * IN, fill=tint(BIO, 0.8), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 0.8 * IN, 6.1 * IN, 11.7 * IN, 0.7 * IN,
     [[("Svar: ", {"bold": True}), ("AI kan i høj grad genkende hudkræft – men den er kun så god som de data, den er trænet på.", {})]],
     size=17, anchor=MSO_ANCHOR.MIDDLE)

# ============================================================================ 9 LYS
s, sh, col = new_slide("fys", "Lys: rødt og infrarødt", """
P2 (0:45): Lys = elektromagnetiske bølger. Pulsoximeter: rødt 660 nm + infrarødt 940 nm (usynligt).
E = h·c/λ → rødt lys ca. 3·10⁻¹⁹ J. UV ca. dobbelt så meget → UV kan skade DNA, rødt lys kan ikke → ufarligt.
DEMO (10 sek): finger over mobil-lommelygten – rødt lys går igennem!
(Kan forkortes hvis I mangler tid.)
""")
spec = [(0.0, "UV", RGBColor(0x6A, 0x3D, 0x9A)), (1.0, "violet", RGBColor(0x8B, 0x3F, 0xD9)),
        (1.6, "blå", RGBColor(0x2F, 0x6F, 0xDE)), (2.4, "grøn", RGBColor(0x2E, 0x9E, 0x6A)),
        (3.2, "gul", RGBColor(0xF2, 0xC2, 0x1A)), (3.8, "orange", RGBColor(0xF0, 0x8A, 0x1A)),
        (4.4, "rød", RGBColor(0xD6, 0x2E, 0x2E)), (5.6, "infrarød", RGBColor(0x6B, 0x1A, 0x2E))]
sx, sy, sw = 0.6 * IN, 1.65 * IN, 12.1 * IN
seg_w = sw / len(spec)
for i, (_, name, c) in enumerate(spec):
    rect(sh, sx + i * seg_w, sy, seg_w, 0.55 * IN, fill=c)
    text(sh, sx + i * seg_w, sy, seg_w, 0.55 * IN, name, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
text(sh, sx, sy + 0.62 * IN, 8.5 * IN, 0.35 * IN,
     "←  kort bølgelængde · høj energi          lang bølgelængde · lav energi  →", size=12, color=GREY)
for idx, lab in ((6, "660 nm"), (7, "940 nm")):
    cx = sx + idx * seg_w + seg_w / 2
    arrow(sh, cx, sy + 1.35 * IN, cx, sy + 0.6 * IN, color=NAVY, width=2.5)
    text(sh, cx - 0.8 * IN, sy + 1.35 * IN, 1.6 * IN, 0.35 * IN, lab, size=15, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER)
formula = rect(sh, 0.6 * IN, 3.65 * IN, 4.6 * IN, 2.2 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
formula.adjustments[0] = 0.08
text(sh, 0.6 * IN, 3.75 * IN, 4.6 * IN, 2.0 * IN,
     [("Fotonenergi", {"size": 16, "color": tint(FYS, 0.5), "bold": True}),
      ("E = h · c / λ", {"size": 40, "bold": True, "color": WHITE}),
      ("h = 6,63·10⁻³⁴ J·s   c = 3,00·10⁸ m/s", {"size": 14, "color": tint(NAVY, 0.7)})],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rows = [["Lys", "λ", "Energi pr. foton", "Effekt"],
        ["UV-B (sol)", "300 nm", "6,6·10⁻¹⁹ J", "Kan skade DNA → hudkræft"],
        ["Rødt", "660 nm", "3,0·10⁻¹⁹ J", "Pulsoximeter – ufarligt"],
        ["Infrarødt", "940 nm", "2,1·10⁻¹⁹ J", "Pulsoximeter – ufarligt"]]
table(sh, 5.5 * IN, 3.65 * IN, 7.2 * IN, 2.2 * IN, rows, FYS, size=15, col_widths=[1.4, 1.0, 1.7, 2.6],
      first_col_bold=True)
text(sh, 0.6 * IN, 6.1 * IN, 12.1 * IN, 0.7 * IN,
     [[("Demo: ", {"bold": True, "color": FYS}),
       ("Hold en finger over mobilens lommelygte i et mørkt rum – fingeren lyser rødt, fordi rødt lys trænger gennem væv og blod.", {})]],
     size=16)

# ============================================================================ 10 PULSOXIMETER
s, sh, col = new_slide("fys", "Sådan virker pulsoximeteret", """
P2 (1:15): To LED'er (rød + IR) – fotodiode på den anden side. Lyset absorberes i fingeren.
Hb UDEN ilt absorberer meget mere RØDT lys end HbO₂.
DC = konstant absorption (hud, knogle, veneblod). AC = pulserende del – arterierne udvider sig ved hvert hjerteslag.
PULS = 60 / T (tid mellem toppe). ILT = forholdet mellem AC for rødt og IR → SpO₂ ≈ 110 − 25·R.
Kun AC bruges → måler ARTERIEBLODET.
""")
oximeter_diagram(sh, 0.9 * IN, 1.7 * IN, 2.6 * IN, 2.6 * IN, size=13)
pts = ppg_points(n=4)
ch = xy_chart(sh, 6.6 * IN, 1.45 * IN, 6.1 * IN, 2.85 * IN, [("Lys gennem fingeren", pts)], [FYS],
              y_min=6.6, y_max=8.2, legend=False, size=11, x_title="tid (s)", y_title="lys ind på sensor",
              x_min=0, x_max=3.2, title="PPG-signal (illustration)")
ch.value_axis.tick_labels.font.size = Pt(1)
ch.value_axis.has_major_gridlines = False
text(sh, 6.6 * IN, 4.25 * IN, 6.1 * IN, 0.4 * IN, "AC = små udsving ved hvert hjerteslag   ·   DC = det konstante niveau",
     size=13, color=GREY, align=PP_ALIGN.CENTER)
rows = [["", "Rødt 660 nm", "Infrarødt 940 nm"],
        ["Hb (uden ilt) – mørkerødt", "absorberer MEGET", "absorberer lidt"],
        ["HbO₂ (med ilt) – lyserødt", "absorberer meget lidt", "absorberer lidt mere"]]
table(sh, 0.6 * IN, 4.75 * IN, 6.0 * IN, 1.4 * IN, rows, FYS, size=13, col_widths=[2.3, 1.8, 1.9],
      first_col_bold=True)
f1 = rect(sh, 6.9 * IN, 4.75 * IN, 2.75 * IN, 1.4 * IN, fill=tint(FYS, 0.85), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 6.9 * IN, 4.75 * IN, 2.75 * IN, 1.4 * IN,
     [("Puls", {"bold": True, "size": 15, "color": FYS}), ("puls = 60 / T", {"bold": True, "size": 22}),
      ("T = 0,80 s → 75 slag/min", {"size": 12, "color": GREY})], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(sh, 9.95 * IN, 4.75 * IN, 2.75 * IN, 1.4 * IN, fill=tint(FYS, 0.85), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 9.95 * IN, 4.75 * IN, 2.75 * IN, 1.4 * IN,
     [("Iltmætning", {"bold": True, "size": 15, "color": FYS}),
      ("R = (AC/DC)rød ÷ (AC/DC)IR", {"bold": True, "size": 13}),
      ("SpO₂ ≈ 110 − 25 · R", {"bold": True, "size": 17})], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(sh, 0.6 * IN, 6.3 * IN, 12.1 * IN, 0.6 * IN,
     [[("Pointe: ", {"bold": True, "color": FYS}),
       ("Kun det pulserende signal bruges, så apparatet måler iltmætningen i arterieblodet (SpO₂).", {})]],
     size=16)

# ============================================================================ 11 METODE
s, sh, col = new_slide("fys", "Ugeforsøg: metode", """
P2 (0:30): Målte på alle fire. Hvile → 3 min trappeløb → målinger hvert 30. sekund i 5 min (restitution).
Fejlkilde-forsøg: bevægelse, kolde fingre, neglelak, lys udefra.
""", subtitle="Uafhængig variabel: aktivitet og tid · Afhængige variable: puls og SpO₂")
steps = [("1", "Hvile", "5 min stille siddende\n3 målinger", BIO),
         ("2", "Arbejde", "3 min trappeløb /\nstep-test", KEM),
         ("3", "Restitution", "måling ved 0, 30, 60, 90,\n120, 180, 240, 300 s", FYS),
         ("4", "Fejlkilder", "bevægelse · kold finger\nneglelak · lys udefra", GEO)]
cw = 2.6 * IN
for i, (n, name, desc, c) in enumerate(steps):
    x = 0.6 * IN + i * (cw + 0.57 * IN)
    circ = rect(sh, x + cw / 2 - 0.45 * IN, 1.9 * IN, 0.9 * IN, 0.9 * IN, fill=c, shape=MSO_SHAPE.OVAL)
    text(sh, x + cw / 2 - 0.45 * IN, 1.9 * IN, 0.9 * IN, 0.9 * IN, n, size=30, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(sh, x, 2.95 * IN, cw, 0.5 * IN, name, size=22, bold=True, color=c, align=PP_ALIGN.CENTER)
    text(sh, x, 3.45 * IN, cw, 1.0 * IN, desc.split("\n"), size=15, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow(sh, x + cw + 0.05 * IN, 2.35 * IN, x + cw + 0.52 * IN, 2.35 * IN, color=GREY, width=3)
placeholder(sh, 0.6 * IN, 4.75 * IN, 3.8 * IN, 2.05 * IN, "foto af jer under forsøget", color=FYS)
label_box(sh, 4.65 * IN, 4.75 * IN, 3.9 * IN, 2.05 * IN, "Kontrolvariable",
          ["• Samme finger og apparat", "• Siddende, hånd i ro", "• Samme arbejde og tid"], FYS, size=14)
label_box(sh, 8.8 * IN, 4.75 * IN, 3.9 * IN, 2.05 * IN, "Sikkerhed",
          ["• Kun så hårdt man selv vil", "• Stop ved svimmelhed", "• Ingen vejrholdning"], KEM, size=14)

# ============================================================================ 12 RESULTATER
s, sh, col = new_slide("fys", "Ugeforsøg: resultater", """
P2 (0:45): Pulsen steg fra gns. __ til __ slag/min – tilbage nær hvile efter ca. __ min.
SpO₂ ændrede sig kun fra __ % til __ %. BEMÆRK: y-aksen starter ved 90 % – ændringen ligger inden for ±2 procentpoint.
Fejlkilder: neglelak/kold finger gav [beskriv].
OVERGANG: "Hvorfor ilten ikke falder mere, forklarer [P3] om lidt."
UDSKIFT GRAFERNE: højreklik på grafen → Rediger data → indsæt jeres tal fra maaleskema.xlsx.
""")
example_tag(sh, 10.1 * IN, 0.4 * IN)
cats = ["hvile", "0 s", "30 s", "60 s", "90 s", "120 s", "180 s", "240 s", "300 s"]
line_chart(sh, 0.5 * IN, 1.4 * IN, 6.2 * IN, 4.2 * IN, cats,
           [("Puls (gns. for gruppen)", (72, 156, 142, 128, 117, 108, 96, 88, 82))], [KEM],
           y_min=50, y_max=180, title="Puls (slag/min)", size=12, legend=False)
line_chart(sh, 6.6 * IN, 1.4 * IN, 6.2 * IN, 4.2 * IN, cats,
           [("SpO₂ (gns. for gruppen)", (98, 97, 97, 98, 98, 98, 98, 98, 98))], [FYS],
           y_min=90, y_max=100, title="Iltmætning SpO₂ (%) – NB: y-akse fra 90", size=12, legend=False)
rows = [["", "Hvile", "Lige efter", "Efter 5 min", "Ændring"],
        ["Puls (slag/min)", "72", "156", "82", "+117 %"],
        ["SpO₂ (%)", "98", "97", "98", "−1 procentpoint"]]
table(sh, 0.6 * IN, 5.75 * IN, 7.6 * IN, 1.1 * IN, rows, FYS, size=13, col_widths=[1.8, 1, 1.2, 1.3, 1.8],
      first_col_bold=True)
rect(sh, 8.45 * IN, 5.75 * IN, 4.25 * IN, 1.1 * IN, fill=tint(GEO, 0.85), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 8.6 * IN, 5.75 * IN, 4.0 * IN, 1.1 * IN,
     [("Fejlkilder", {"bold": True, "color": GEO}),
      ("Neglelak: __ · Kold finger: __ · Bevægelse: __", {"size": 13})], size=15, anchor=MSO_ANCHOR.MIDDLE)

# ============================================================================ 13 AI OG AFVIGELSER
s, sh, col = new_slide("fys", "AI og afvigelser i data", """
P2 (0:45): Simpel afvigelsesmodel i Excel: klassens hvilemålinger → middelværdi og standardafvigelse.
Uden for middel ± 2s = afvigelse (|z| > 2). Fangede neglelak-målingen.
MEN: markerede også puls lige efter trappeløb – som er normal! Mangler KONTEKST.
Rigtig AI (smartwatch): lærer DIN normal + bruger bevægelsessensoren. Apple Heart Study (400.000+): opdager uregelmæssig rytme (atrieflimren).
BIAS: pulsoximetre overser oftere iltmangel ved mørk hud (Sjoding 2020) – melanin absorberer lys.
OVERGANG: "Men hvorfor faldt iltmætningen næsten ikke, selvom vi løb op ad trapperne? Det er kemi."
""")
example_tag(sh, 10.1 * IN, 0.4 * IN)
import random as _r  # noqa: E402
rnd = _r.Random(5)
normal = [round(rnd.gauss(74, 8)) for _ in range(22)]
pts_norm = [(i + 1, v) for i, v in enumerate(normal)]
anom = [(23, 104), (24, 112)]
from pptx.chart.data import XyChartData  # noqa: E402
from pptx.enum.chart import XL_CHART_TYPE, XL_MARKER_STYLE  # noqa: E402
cd = XyChartData()
s1 = cd.add_series("Normale målinger")
for px, py in pts_norm:
    s1.add_data_point(px, py)
s2 = cd.add_series("Afvigelse (|z| > 2)")
for px, py in anom:
    s2.add_data_point(px, py)
s3 = cd.add_series("Øvre grænse (x̄ + 2s)")
for px in (0, 25):
    s3.add_data_point(px, 90)
s4 = cd.add_series("Nedre grænse (x̄ − 2s)")
for px in (0, 25):
    s4.add_data_point(px, 58)
gf = sh.add_chart(XL_CHART_TYPE.XY_SCATTER, Emu(int(0.5 * IN)), Emu(int(1.4 * IN)), Emu(int(6.6 * IN)),
                  Emu(int(4.3 * IN)), cd)
chx = gf.chart
from fffo_design import _style_chart  # noqa: E402
_style_chart(chx, "Hvilepuls i klassen (slag/min)", 12, True)
for i, (c, mk) in enumerate(((FYS, True), (KEM, True), (GREY, False), (GREY, False))):
    ser = chx.series[i]
    if mk:
        ser.format.line.fill.background()
        ser.marker.style = XL_MARKER_STYLE.CIRCLE
        ser.marker.size = 9 if i == 0 else 13
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = c
        ser.marker.format.line.color.rgb = c
    else:
        ser.marker.style = XL_MARKER_STYLE.NONE
        ser.format.line.color.rgb = c
        ser.format.line.width = Pt(2)
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        ser.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
chx.value_axis.minimum_scale = 40
chx.value_axis.maximum_scale = 120
chx.category_axis.minimum_scale = 0
chx.category_axis.maximum_scale = 25
levels = [("1. Regel", "Alarm hvis SpO₂ < 92 %", "simpel – kender ikke personen"),
          ("2. Statistik", "z = (x − x̄) / s   ·   afvigelse hvis |z| > 2", "vores Excel-model"),
          ("3. Maskinlæring", "lærer DIN normal + bevægelse + mønstre i PPG-kurven", "smartwatch, hospital")]
for i, (name, desc, ex) in enumerate(levels):
    y = 1.45 * IN + i * 1.05 * IN
    rect(sh, 7.35 * IN, y, 5.35 * IN, 0.92 * IN, fill=tint(FYS, 0.88 - i * 0.12))
    text(sh, 7.5 * IN, y + 0.06 * IN, 5.1 * IN, 0.85 * IN,
         [[(name + ":  ", {"bold": True, "color": FYS}), (desc, {"bold": True})], (ex, {"size": 12, "color": GREY})],
         size=14)
label_box(sh, 7.35 * IN, 4.65 * IN, 5.35 * IN, 2.15 * IN, "Men pas på",
          ["• Høj puls efter løb er normal – modellen mangler kontekst",
           "• Bias: pulsoximetre overser oftere iltmangel ved mørk hud (Sjoding 2020)"], KEM, size=13)
text(sh, 0.6 * IN, 5.85 * IN, 6.5 * IN, 1.0 * IN,
     [[("Apple Heart Study (2019): ", {"bold": True}),
       ("over 400.000 deltagere – uret kunne advare om uregelmæssig hjerterytme (atrieflimren).", {})]],
     size=14)

# ============================================================================ 14 HÆMOGLOBIN
s, sh, col = new_slide("kem", "Hæmoglobin – blodets iltbærer", """
P3 (1:00): HOLD MODELLEN OP. Hæmoglobin = protein i røde blodlegemer. 4 proteinkæder (2α + 2β).
Hver kæde har en hæmgruppe med jern-ion Fe²⁺ – jernet binder ilten → 4 O₂ pr. Hb.
Bindingen er svag og reversibel – skal fanges i lungerne og afleveres i musklerne. Fe³⁺ kan ikke binde ilt.
""")
hemoglobin_diagram(sh, 0.9 * IN, 1.55 * IN, 4.4 * IN, oxygen=4, size=16)
text(sh, 0.6 * IN, 6.05 * IN, 5.0 * IN, 0.8 * IN, "Hæmoglobin med 4 bundne O₂ (oxyhæmoglobin)", size=14, color=GREY,
     align=PP_ALIGN.CENTER)
facts = [("Protein", "i de røde blodlegemer – ca. 270 mio. pr. blodlegeme"),
         ("4 kæder", "2 α-kæder og 2 β-kæder"),
         ("Hæmgruppe", "porfyrinring med en jern-ion Fe²⁺ i midten"),
         ("4 × O₂", "hvert jern binder ét iltmolekyle"),
         ("Reversibel", "svag binding: fanges i lungerne, slippes i musklerne"),
         ("Fe³⁺", "oxideret jern kan IKKE binde ilt · jernmangel → blodmangel")]
for i, (h, d) in enumerate(facts):
    y = 1.55 * IN + i * 0.83 * IN
    rect(sh, 6.0 * IN, y, 0.1 * IN, 0.68 * IN, fill=KEM)
    text(sh, 6.3 * IN, y, 6.4 * IN, 0.75 * IN, [[(h + "  ", {"bold": True, "color": KEM, "size": 20}), (d, {"size": 16})]],
         anchor=MSO_ANCHOR.MIDDLE)

# ============================================================================ 15 LIGEVÆGT OG KURVE
s, sh, col = new_slide("kem", "Ligevægt og den S-formede bindingskurve", """
P3 (1:15): Kemisk ligevægt: Hb + 4 O₂ ⇌ Hb(O₂)₄. Le Chatelier: forskydes efter hvor meget ilt der er.
LUNGER: meget ilt → mod højre → ca. 97 % mættet. MUSKLER: lidt ilt → mod venstre → ilt afgives.
S-formet fordi bindingen er KOOPERATIV (første O₂ gør det lettere for de næste).
FLAD TOP = sikkerhedsmargin: selvom ilttrykket ændrer sig lidt, forbliver mætningen næsten 100 %.
""")
eq = rect(sh, 0.6 * IN, 1.45 * IN, 5.3 * IN, 1.0 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 0.6 * IN, 1.45 * IN, 5.3 * IN, 1.0 * IN, "Hb + 4 O₂  ⇌  Hb(O₂)₄", size=30, bold=True, color=WHITE,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rows = [["Sted", "pO₂", "Ligevægt", "Mætning"],
        ["Lunger", "13,3 kPa", "→ binder O₂", "ca. 97 %"],
        ["Hvilende væv", "5,3 kPa", "← afgiver lidt", "ca. 75 %"],
        ["Arbejdende muskel", "2,7 kPa", "←← afgiver meget", "ca. 31 %"]]
table(sh, 0.6 * IN, 2.7 * IN, 5.3 * IN, 2.1 * IN, rows, KEM, size=14, col_widths=[1.8, 1.05, 1.55, 1.3],
      first_col_bold=True)
text(sh, 0.6 * IN, 5.0 * IN, 5.3 * IN, 1.9 * IN,
     [[("Le Chateliers princip: ", {"bold": True}), ("ligevægten forskydes, så den modvirker ændringen.", {})],
      [("Kooperativ binding: ", {"bold": True}), ("når første O₂ binder, binder de næste lettere → S-kurve.", {})],
      [("Flad top: ", {"bold": True}), ("sikkerhedsmargin – mætningen holdes høj i lungerne.", {})]], size=15)
curve = [(p / 4, round(hill(p / 4, 3.6), 2)) for p in range(0, 61)]
ch = xy_chart(sh, 6.2 * IN, 1.35 * IN, 6.6 * IN, 5.5 * IN, [("Hæmoglobin (Hill: n = 2,7, P50 = 3,6 kPa)", curve)],
              [KEM], x_min=0, x_max=15, y_min=0, y_max=100, size=12, x_title="iltens partialtryk pO₂ (kPa)",
              y_title="iltmætning (%)", title="Iltbindingskurve")
text(sh, 10.6 * IN, 2.05 * IN, 2.1 * IN, 0.4 * IN, "lunger ≈ 97 %", size=13, bold=True, color=FYS)
text(sh, 9.35 * IN, 3.05 * IN, 2.1 * IN, 0.4 * IN, "hvile ≈ 75 %", size=13, bold=True, color=GEO)
text(sh, 8.15 * IN, 4.5 * IN, 2.1 * IN, 0.4 * IN, "muskel ≈ 31 %", size=13, bold=True, color=KEM)

# ============================================================================ 16 BOHR + FORKLARING
s, sh, col = new_slide("kem", "Bohr-effekten forklarer vores resultater", """
P3 (1:15): Arbejde → mere respiration → mere CO₂ + varme. CO₂ + H₂O → kulsyre → blodet bliver surere.
BTB: efter trappeløb gul på __ s mod __ s i hvile.
BOHR-EFFEKTEN: surt + varmt → Hb slipper ilten lettere → kurven forskydes mod højre → ilten havner hvor musklerne arbejder.
VORES RESULTATER: Puls ↑ fordi blodet skal cirkulere hurtigere. SpO₂ ≈ uændret fordi pulsoximeteret måler ARTERIEBLODET, der lige har været i lungerne (flad top). Faldet sker i VENEBLODET – det måler pulsoximeteret ikke.
OVERGANG: "Teknologien virker på os – men virker den lige godt for alle i verden? Det tager [P4] sig af."
""")
text(sh, 0.6 * IN, 1.4 * IN, 6.2 * IN, 1.2 * IN,
     [("C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + energi", {"bold": True, "size": 19}),
      ("CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻", {"bold": True, "size": 19, "color": KEM})], size=19)
curve_n = [(p / 4, round(hill(p / 4, 3.6), 2)) for p in range(0, 61)]
curve_w = [(p / 4, round(hill(p / 4, 4.4), 2)) for p in range(0, 61)]
xy_chart(sh, 0.5 * IN, 2.55 * IN, 6.3 * IN, 4.35 * IN,
         [("Hvile (normal)", curve_n), ("Arbejdende muskel: mere CO₂, lavere pH, varmere", curve_w)],
         [KEM, PURPLE], x_min=0, x_max=15, y_min=0, y_max=100, size=11, x_title="pO₂ (kPa)",
         y_title="iltmætning (%)", title="Bohr-effekten: kurven forskydes mod højre", dashed=[False, True])
rows = [["Observation", "Forklaring"],
        ["Pulsen steg (72 → 156)", "Musklerne skal have mere O₂ og af med CO₂ → hjertet pumper hurtigere"],
        ["SpO₂ næsten uændret (98 → 97 %)", "Måler arterieblod fra lungerne · flad top på kurven · hurtigere vejrtrækning"],
        ["Iltforbruget ses ikke", "Ilten afgives i musklerne → faldet sker i veneblodet, som ikke måles"],
        ["BTB gul hurtigere efter arbejde", "Mere CO₂ udåndet → mere kulsyre → lavere pH"]]
table(sh, 7.05 * IN, 1.45 * IN, 5.65 * IN, 4.4 * IN, rows, KEM, size=13, col_widths=[2.0, 3.65], first_col_bold=True)
example_tag(sh, 7.05 * IN, 6.05 * IN, w=2.8)
text(sh, 9.95 * IN, 6.0 * IN, 2.8 * IN, 0.8 * IN, "BTB: hvile __ s · arbejde __ s", size=14, bold=True, color=KEM,
     anchor=MSO_ANCHOR.MIDDLE)

# ============================================================================ 17 GEOGRAFI FAKTORER
s, sh, col = new_slide("geo", "Hvem får gavn af AI? Seks faktorer", """
P4 (1:00): Hudkræft mest hvor der er meget UV og mange med lys hud → Australien verdens højeste, Danmark højt (solferier).
Seks faktorer: økonomi, infrastruktur (strøm/internet), sundhedspersonale, lige adgang, data der passer til befolkningen, lovgivning og tillid.
""")
placeholder(sh, 0.6 * IN, 1.45 * IN, 5.0 * IN, 3.3 * IN,
            "verdenskort: forekomst af modermærkekræft (GLOBOCAN / Our World in Data)", color=GEO)
text(sh, 0.6 * IN, 4.9 * IN, 5.0 * IN, 1.9 * IN,
     [[("Behovet: ", {"bold": True, "color": GEO}), ("UV-stråling + lys hud + solvaner.", {})],
      [("Australien ", {"bold": True}), ("har verdens højeste forekomst af modermærkekræft.", {})],
      [("Danmark ", {"bold": True}), ("ligger også højt – lys hud og solferier.", {})]], size=15)
factors = [("Økonomi", "BNP, sundhedsudgifter"), ("Infrastruktur", "strøm, internet, smartphones"),
           ("Sundhedspersonale", "læger og hudlæger pr. indbygger"), ("Lige adgang", "gratis/offentligt eller privat"),
           ("Data og bias", "er AI'en trænet på befolkningens hudtype?"), ("Lovgivning og tillid", "GDPR, EU's AI-forordning")]
for i, (h, d) in enumerate(factors):
    cx = 5.95 * IN + (i % 2) * 3.4 * IN
    cy = 1.45 * IN + (i // 2) * 1.8 * IN
    rect(sh, cx, cy, 3.25 * IN, 1.65 * IN, fill=tint(GEO, 0.86))
    n = rect(sh, cx + 0.15 * IN, cy + 0.2 * IN, 0.55 * IN, 0.55 * IN, fill=GEO, shape=MSO_SHAPE.OVAL)
    text(sh, cx + 0.15 * IN, cy + 0.2 * IN, 0.55 * IN, 0.55 * IN, str(i + 1), size=18, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(sh, cx + 0.85 * IN, cy + 0.18 * IN, 2.3 * IN, 1.4 * IN, [(h, {"bold": True, "size": 16}), (d, {"size": 13, "color": GREY})])

# ============================================================================ 18 AI-PARATHEDSMODEL
s, sh, col = new_slide("geo", "Vores model: AI-parathedsmodellen", """
P4 (1:15): Vores egen model – 5 lande får 1–5 point pr. faktor.
Danmark 30/30: gratis sundhedsvæsen, internet, data. USA kun 22 selvom rigt – ULIGE adgang (sundhedsforsikring).
Indien 14, Nigeria 8: få læger, dårligere infrastruktur, AI ikke trænet på mørk hud.
BEGRÆNSNINGER: subjektive point, alle faktorer vægter ens, stor forskel mellem by og land.
""", subtitle="1–5 point pr. faktor (vores egen vurdering ud fra data fra Verdensbanken, WHO og Gapminder)")
rows = [["Faktor", "DK", "AUS", "USA", "IND", "NGA"],
        ["Økonomi", "5", "5", "5", "2", "1"],
        ["Infrastruktur", "5", "5", "4", "3", "2"],
        ["Sundhedspersonale", "5", "5", "4", "2", "1"],
        ["Lige adgang", "5", "4", "2", "2", "1"],
        ["Data (hudtype)", "5", "5", "3", "2", "1"],
        ["Lovgivning og tillid", "5", "4", "4", "3", "2"],
        ["I alt (ud af 30)", "30", "28", "22", "14", "8"]]
tbl = table(sh, 0.6 * IN, 1.85 * IN, 6.2 * IN, 4.0 * IN, rows, GEO, size=15, col_widths=[2.4, 0.75, 0.75, 0.75, 0.75, 0.75],
            first_col_bold=True)
for c in range(6):
    cell = tbl.cell(7, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = tint(GEO, 0.6)
    cell.text_frame.paragraphs[0].runs[0].font.bold = True
bar_chart(sh, 7.0 * IN, 1.75 * IN, 5.8 * IN, 4.15 * IN, ["Danmark", "Australien", "USA", "Indien", "Nigeria"],
          (30, 28, 22, 14, 8), GEO, title="AI-parathed (point ud af 30)", size=12, y_max=30,
          point_colors=[tint(GEO, 0.0), tint(GEO, 0.15), tint(GEO, 0.35), tint(KEM, 0.2), KEM])
text(sh, 0.6 * IN, 6.05 * IN, 12.1 * IN, 0.8 * IN,
     [[("Begrænsninger: ", {"bold": True, "color": GEO}),
       ("pointene er subjektive · alle faktorer vægter ens · et land er ikke ens overalt (by og land).", {})]],
     size=15)

# ============================================================================ 19 AI-PARADOKSET
s, sh, col = new_slide("geo", "AI-paradokset og kræftdiagnosticering", """
P4 (1:15): AI-PARADOKSET: de lande der har MEST brug for AI (få læger) har DÅRLIGST adgang.
Danmark: AI kan SORTERE (triage) → hudlæger tager alvorlige først → kortere ventetid.
Indien: AI på smartphone i landsbyer uden hudlæge – men kun hvis den virker på MØRK HUD og der er BEHANDLING bagefter.
DTM: når lande udvikler sig og befolkningen bliver ældre → flere kræfttilfælde → behovet vokser.
""")
mx, my, mw, mh = 0.95 * IN, 1.5 * IN, 5.4 * IN, 4.4 * IN
quad = [(0, 0, tint(KEM, 0.82), "Stort behov · lav adgang", "Indien (landområder)\n\"AI kunne hjælpe mest\""),
        (1, 0, tint(BIO, 0.8), "Stort behov · høj adgang", "Australien · Danmark"),
        (0, 1, tint(GEO, 0.85), "Lavt behov · lav adgang", "Nigeria\n(hudkræft sjælden – AI til andre kræftformer)"),
        (1, 1, tint(FYS, 0.85), "Lavere behov · høj adgang", "USA\n(men ulige adgang)")]
for qx, qy, c, h, d in quad:
    x, y = mx + qx * mw / 2, my + qy * mh / 2
    rect(sh, x + 0.03 * IN, y + 0.03 * IN, mw / 2 - 0.06 * IN, mh / 2 - 0.06 * IN, fill=c)
    text(sh, x + 0.12 * IN, y + 0.12 * IN, mw / 2 - 0.24 * IN, mh / 2 - 0.24 * IN,
         [(h, {"bold": True, "size": 14}), *[(ln, {"size": 13}) for ln in d.split("\n")]])
arrow(sh, mx, my + mh + 0.1 * IN, mx + mw, my + mh + 0.1 * IN, color=INK, width=2)
arrow(sh, mx - 0.1 * IN, my + mh, mx - 0.1 * IN, my, color=INK, width=2)
text(sh, mx, my + mh + 0.15 * IN, mw, 0.35 * IN, "adgang til AI →", size=13, bold=True, align=PP_ALIGN.RIGHT)
text(sh, 0.12 * IN, my, 0.66 * IN, 0.8 * IN, ["↑", "behov"], size=12, bold=True, align=PP_ALIGN.CENTER)
label_box(sh, 6.7 * IN, 1.45 * IN, 2.9 * IN, 2.75 * IN, "Danmark",
          ["• AI sorterer (triage)", "• Kortere ventetid hos hudlæge", "• Risiko: flere falske alarmer"], BIO, size=13)
label_box(sh, 9.8 * IN, 1.45 * IN, 2.9 * IN, 2.75 * IN, "Indien / Nigeria",
          ["• AI på smartphone uden hudlæge", "• Kræver data om mørk hud", "• Kræver behandling bagefter"], KEM, size=13)
rows = [["DTM-fase", "Land", "Betydning"],
        ["2–3: ung befolkning", "Nigeria", "færre kræfttilfælde pr. indb."],
        ["3: faldende fødselstal", "Indien", "kræft stiger"],
        ["4–5: aldrende", "DK, AUS", "mange kræfttilfælde"]]
table(sh, 6.7 * IN, 4.4 * IN, 6.0 * IN, 1.75 * IN, rows, GEO, size=13, col_widths=[2.2, 1.3, 2.5], first_col_bold=True)
text(sh, 0.6 * IN, 6.35 * IN, 12.1 * IN, 0.55 * IN,
     [[("AI-paradokset: ", {"bold": True, "color": GEO}),
       ("de lande, der har mest brug for AI, har ofte dårligst adgang til den.", {})]], size=17)

# ============================================================================ 20 KONKLUSION
s, sh, col = new_slide("all", "Konklusion", """
EN SÆTNING PR. FAG – hver person siger sin egen:
P1: AI kan genkende hudkræft næsten lige så godt som hudlæger, fordi kræftceller giver synlige forandringer.
P2: Med lys kan vi måle puls og ilt – og AI kan finde afvigelser i data.
P3: Kemien forklarer, hvorfor iltmætningen er stabil hos raske – derfor er et fald et vigtigt faresignal.
P4: Men AI er kun så god som dens data og det sundhedssystem, den bruges i.
ALLE/P4: AI er et stærkt hjælpeværktøj – ikke en læge. Tak fordi I lyttede – har I spørgsmål?
""")
concl = [("BIOLOGI", BIO, "AI kan genkende hudkræft på billeder næsten lige så godt som hudlæger – fordi kræftceller giver synlige forandringer."),
         ("FYSIK", FYS, "Med rødt og infrarødt lys kan vi måle puls og ilt – og AI kan finde afvigelser i de data."),
         ("KEMI", KEM, "Hæmoglobins bindingskurve holder iltmætningen stabil hos raske – derfor er et fald et vigtigt faresignal."),
         ("GEOGRAFI", GEO, "AI virker kun, hvis der er data om alle hudtyper, sundhedspersonale og behandling – ellers øges uligheden.")]
for i, (tag, c, t) in enumerate(concl):
    y = 1.45 * IN + i * 1.0 * IN
    rect(sh, 0.6 * IN, y, 1.9 * IN, 0.85 * IN, fill=c)
    text(sh, 0.6 * IN, y, 1.9 * IN, 0.85 * IN, tag, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
    rect(sh, 2.5 * IN, y, 10.2 * IN, 0.85 * IN, fill=tint(c, 0.88))
    text(sh, 2.7 * IN, y, 9.9 * IN, 0.85 * IN, t, size=17, anchor=MSO_ANCHOR.MIDDLE)
big = rect(sh, 0.6 * IN, 5.6 * IN, 12.1 * IN, 1.2 * IN, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(sh, 0.6 * IN, 5.6 * IN, 12.1 * IN, 1.2 * IN,
     [("AI er et stærkt hjælpeværktøj – ikke en læge.", {"bold": True, "size": 28, "color": WHITE}),
      ("Den er kun så god som dens data og det sundhedssystem, den bruges i.", {"size": 17, "color": tint(NAVY, 0.75)})],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=0.95)

# ============================================================================ 21 KILDER
s, sh, col = new_slide("all", "Kilder", """
Vises kun – læses ikke op. Sig: "Tak fordi I lyttede – vi er klar til spørgsmål."
""")
left = ["Esteva m.fl. (2017): Dermatologist-level classification of skin cancer with deep neural networks. Nature 542.",
        "Haenssle m.fl. (2018): Man against machine. Annals of Oncology 29.",
        "Tschandl m.fl. (2019): Human readers vs. machine-learning algorithms. Lancet Oncology 20.",
        "Winkler m.fl. (2019): Surgical skin markings and CNN performance. JAMA Dermatology 155.",
        "Daneshjou m.fl. (2022): Disparities in dermatology AI performance. Science Advances 8.",
        "Sjoding m.fl. (2020): Racial bias in pulse oximetry measurement. NEJM 383.",
        "Perez m.fl. (2019): Smartwatch to identify atrial fibrillation (Apple Heart Study). NEJM 381."]
right = ["Kræftens Bekæmpelse – cancer.dk (hudkræft, modermærkekræft)",
         "Sundhed.dk – pulsoximetri, kulilteforgiftning",
         "ISIC Archive – gallery.isic-archive.com (billeder til forsøget)",
         "Teachable Machine – teachablemachine.withgoogle.com",
         "WHO / GLOBOCAN – gco.iarc.fr · Verdensbanken – data.worldbank.org · Gapminder",
         "WHO (2021): Ethics and governance of AI for health · EU's AI-forordning (2024)",
         "Vores fagbøger i biologi, fysik/kemi og geografi"]
bullets(sh, 0.6 * IN, 1.5 * IN, 6.0 * IN, 5.3 * IN, left, size=13, bullet_color=NAVY, gap=0.55)
bullets(sh, 6.9 * IN, 1.5 * IN, 5.8 * IN, 5.3 * IN, right, size=13, bullet_color=NAVY, gap=0.55)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print("Gemt:", OUT, "slides:", len(prs.slides))
