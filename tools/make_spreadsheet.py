"""Genererer skabeloner/maaleskema.xlsx.

Kør:  python3 tools/make_spreadsheet.py
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference, ScatterChart, Series
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parent.parent / "skabeloner" / "maaleskema.xlsx"

INPUT = PatternFill("solid", fgColor="FFF4C2")
HEAD = PatternFill("solid", fgColor="1B2A41")
CALC = PatternFill("solid", fgColor="E8EEF8")
GOOD = PatternFill("solid", fgColor="CDEFD9")
BAD = PatternFill("solid", fgColor="F8CFCF")
WHITE_B = Font(bold=True, color="FFFFFF")
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=16, color="1B2A41")
NOTE = Font(italic=True, color="6B7585")
thin = Side(style="thin", color="D5DBE5")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()


def header_row(ws, row, values, col=1):
    for i, v in enumerate(values):
        c = ws.cell(row=row, column=col + i, value=v)
        c.fill = HEAD
        c.font = WHITE_B
        c.alignment = CENTER
        c.border = BOX


def cell(ws, ref, value=None, fill=None, font=None, fmt=None, align=None):
    c = ws[ref]
    if value is not None:
        c.value = value
    if fill:
        c.fill = fill
    if font:
        c.font = font
    if fmt:
        c.number_format = fmt
    c.border = BOX
    c.alignment = align or CENTER
    return c


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


# ============================================================================ VEJLEDNING
ws = wb.active
ws.title = "Vejledning"
ws["A1"] = "FFFO – AI i sundhed · måleskema og modeller"
ws["A1"].font = TITLE
lines = [
    "Gule felter = I skal selv skrive. Blå felter = beregnes automatisk. Graferne opdateres af sig selv.",
    "",
    "Faneblade:",
    "1. Hvile – 3 målinger pr. person i hvile (fysik-ugeforsøg 1).",
    "2. Arbejde og restitution – målinger efter 3 min arbejde (ugeforsøg 2). Grønne felter = pulsen er under hvile + 10.",
    "3. Fejlkilder – bevægelse, kold finger, neglelak, lys udefra, tryk (ugeforsøg 3).",
    "4. Klassedata og afvigelser – AI-afvigelsesmodel: middelværdi ± 2 standardafvigelser og z-værdier (ugeforsøg 5).",
    "5. AI-test hudkræft – testskema til liveforsøget i biologi. Beregner sensitivitet, specificitet og træfsikkerhed.",
    "6. BTB – kemiforsøget med CO₂ i udåndingsluft.",
    "7. Hb-bindingskurve – model af hæmoglobins iltbinding (Hill-ligningen) med Bohr-effekt. Prøv at ændre P50!",
    "8. Geografi-model – AI-parathedsmodellen (1–5 point pr. faktor) og landedata.",
    "",
    "Grafer til PowerPoint: Kopiér grafen (Ctrl+C) og indsæt i PowerPoint (Ctrl+V), eller højreklik på grafen i PowerPoint → Rediger data.",
    "Fanen 'Klassedata og afvigelser' indeholder EKSEMPELDATA – slet dem og indsæt jeres egne.",
]
for i, t in enumerate(lines, start=3):
    ws.cell(row=i, column=1, value=t)
ws["A3"].font = BOLD
ws.column_dimensions["A"].width = 120

# ============================================================================ HVILE
ws = wb.create_sheet("Hvile")
ws["A1"] = "Forsøg 1 – Hvile (sid stille 5 min, mål 3 gange med 30 s mellemrum)"
ws["A1"].font = TITLE
header_row(ws, 3, ["Person", "Puls 1", "Puls 2", "Puls 3", "Gns. puls", "SpO₂ 1 (%)", "SpO₂ 2 (%)", "SpO₂ 3 (%)", "Gns. SpO₂ (%)"])
for r in range(4, 8):
    cell(ws, f"A{r}", f"Person {r - 3}", INPUT)
    for col in "BCDFGH":
        cell(ws, f"{col}{r}", None, INPUT)
    cell(ws, f"E{r}", f'=IF(COUNT(B{r}:D{r})=0,"",AVERAGE(B{r}:D{r}))', CALC, fmt="0.0")
    cell(ws, f"I{r}", f'=IF(COUNT(F{r}:H{r})=0,"",AVERAGE(F{r}:H{r}))', CALC, fmt="0.0")
cell(ws, "A8", "Gruppens gns.", CALC, BOLD)
cell(ws, "E8", '=IF(COUNT(E4:E7)=0,"",AVERAGE(E4:E7))', CALC, BOLD, "0.0")
cell(ws, "I8", '=IF(COUNT(I4:I7)=0,"",AVERAGE(I4:I7))', CALC, BOLD, "0.0")
widths(ws, {c: 13 for c in "ABCDEFGHI"})

# ============================================================================ ARBEJDE OG RESTITUTION
ws = wb.create_sheet("Arbejde og restitution")
ws["A1"] = "Forsøg 2 – 3 min arbejde, derefter målinger mens I sidder stille"
ws["A1"].font = TITLE
ws["A2"] = "Hvile-rækken hentes automatisk fra fanen 'Hvile'. Grønt = pulsen er tilbage under hvilepuls + 10. (#I/T eller #N/A forsvinder, når I skriver tal ind.)"
ws["A2"].font = NOTE
cols = ["Tid", "Puls P1", "Puls P2", "Puls P3", "Puls P4", "Gns. puls", "SpO₂ P1", "SpO₂ P2", "SpO₂ P3", "SpO₂ P4", "Gns. SpO₂"]
header_row(ws, 4, cols)
times = ["hvile", "0 s", "30 s", "60 s", "90 s", "120 s", "180 s", "240 s", "300 s"]
for i, t in enumerate(times):
    r = 5 + i
    cell(ws, f"A{r}", t, CALC if i == 0 else None, BOLD)
    for j, col in enumerate("BCDE"):
        if i == 0:
            cell(ws, f"{col}{r}", f"=Hvile!E{4 + j}", CALC, fmt="0")
        else:
            cell(ws, f"{col}{r}", None, INPUT)
    for j, col in enumerate("GHIJ"):
        if i == 0:
            cell(ws, f"{col}{r}", f"=Hvile!I{4 + j}", CALC, fmt="0")
        else:
            cell(ws, f"{col}{r}", None, INPUT)
    cell(ws, f"F{r}", f'=IF(COUNT(B{r}:E{r})=0,NA(),AVERAGE(B{r}:E{r}))', CALC, BOLD, "0")
    cell(ws, f"K{r}", f'=IF(COUNT(G{r}:J{r})=0,NA(),AVERAGE(G{r}:J{r}))', CALC, BOLD, "0.0")
for col in "BCDE":
    ws.conditional_formatting.add(
        f"{col}6:{col}13",
        FormulaRule(formula=[f'AND(ISNUMBER({col}6),ISNUMBER({col}$5),{col}6<={col}$5+10)'], fill=GOOD),
    )
cell(ws, "A15", "Restitutionstid (s)", INPUT, BOLD)
for col in "BCDE":
    cell(ws, f"{col}15", None, INPUT)
ws["F15"] = "← skriv første tid, hvor feltet bliver grønt"
ws["F15"].font = NOTE
cell(ws, "A16", "Ændring i puls (%)", CALC, BOLD)
cell(ws, "F16", '=IFERROR((F6-F5)/F5*100,"")', CALC, BOLD, "0")
cell(ws, "A17", "Ændring SpO₂ (pp)", CALC, BOLD)
cell(ws, "K17", '=IFERROR(K6-K5,"")', CALC, BOLD, "0.0")
widths(ws, {c: 11 for c in "ABCDEFGHIJK"})
ws.column_dimensions["A"].width = 20

lc = LineChart()
lc.title = "Puls efter arbejde"
lc.y_axis.title = "slag/min"
lc.x_axis.title = "tid"
lc.height, lc.width = 8, 16
lc.add_data(Reference(ws, min_col=2, max_col=6, min_row=4, max_row=13), titles_from_data=True)
lc.set_categories(Reference(ws, min_col=1, min_row=5, max_row=13))
ws.add_chart(lc, "M4")
lc2 = LineChart()
lc2.title = "Iltmætning SpO₂ efter arbejde"
lc2.y_axis.title = "%"
lc2.y_axis.scaling.min = 90
lc2.y_axis.scaling.max = 100
lc2.height, lc2.width = 8, 16
lc2.add_data(Reference(ws, min_col=7, max_col=11, min_row=4, max_row=13), titles_from_data=True)
lc2.set_categories(Reference(ws, min_col=1, min_row=5, max_row=13))
ws.add_chart(lc2, "M21")

# ============================================================================ FEJLKILDER
ws = wb.create_sheet("Fejlkilder")
ws["A1"] = "Forsøg 3 – Fejlkilder (én ændring ad gangen, samme person i hvile)"
ws["A1"].font = TITLE
header_row(ws, 3, ["Delforsøg", "Fremgangsmåde", "Puls", "SpO₂ (%)", "Tid til signal (s)", "Observation", "Fysisk forklaring"])
rows = [
    ("Normal (reference)", "Hånd i ro på bordet", "", "Referencemåling"),
    ("a. Bevægelse", "Ryst hånden let", "", "Bevægelse ændrer lysvejen → falsk AC-signal"),
    ("b. Kold finger", "1 min i koldt vand, tør", "", "Blodkar trækker sig sammen → svagt AC-signal"),
    ("c. Neglelak", "Mørk neglelak, tør", "", "Lakken absorberer lyset"),
    ("d. Lys udefra", "Lommelygte på klemmen", "", "Fremmed rødt/IR-lys forstyrrer sensoren"),
    ("e. Tryk", "Pres fingeren mod bordet", "", "Mindre blodgennemstrømning → svagt signal"),
]
for i, (a, b, _, f) in enumerate(rows):
    r = 4 + i
    cell(ws, f"A{r}", a, None, BOLD, align=WRAP)
    cell(ws, f"B{r}", b, align=WRAP)
    for col in "CDEF":
        cell(ws, f"{col}{r}", None, INPUT, align=WRAP)
    cell(ws, f"G{r}", f, align=WRAP)
widths(ws, {"A": 20, "B": 26, "C": 9, "D": 10, "E": 14, "F": 34, "G": 44})

# ============================================================================ KLASSEDATA OG AFVIGELSER
ws = wb.create_sheet("Klassedata og afvigelser")
ws["A1"] = "Forsøg 5 – AI-afvigelsesmodel: hvilke målinger er unormale?"
ws["A1"].font = TITLE
ws["A2"] = "EKSEMPELDATA i de gule felter – slet og indsæt hele klassens hvilemålinger. Rækker 26–27 er bevidst 'afvigende' (neglelak / høj puls)."
ws["A2"].font = NOTE
header_row(ws, 4, ["Person/gruppe", "Hvilepuls", "SpO₂ (%)", "z (puls)", "z (SpO₂)", "Status"])
example = [72, 65, 80, 77, 69, 84, 74, 70, 63, 79, 88, 71, 66, 75, 82, 68, 73, 78, 61, 76, 70]
example_spo2 = [98, 99, 97, 98, 98, 97, 99, 98, 98, 97, 98, 99, 98, 97, 98, 98, 99, 97, 98, 98, 99]
for i in range(45):
    r = 5 + i
    cell(ws, f"A{r}", f"Elev {i + 1}" if i < 23 else None, INPUT)
    if i < len(example):
        p, o = example[i], example_spo2[i]
    elif i == 21:
        p, o = 106, 98
    elif i == 22:
        p, o = 74, 89
    else:
        p, o = None, None
    cell(ws, f"B{r}", p, INPUT)
    cell(ws, f"C{r}", o, INPUT)
    cell(ws, f"D{r}", f'=IF(B{r}="","",(B{r}-$I$5)/$I$6)', CALC, fmt="0.00")
    cell(ws, f"E{r}", f'=IF(C{r}="","",(C{r}-$J$5)/$J$6)', CALC, fmt="0.00")
    cell(ws, f"F{r}", f'=IF(AND(B{r}="",C{r}=""),"",IF(OR(ABS(N(D{r}))>2,ABS(N(E{r}))>2),"AFVIGELSE","normal"))', CALC, BOLD)
ws.conditional_formatting.add("F5:F49", CellIsRule(operator="equal", formula=['"AFVIGELSE"'], fill=BAD))
ws.conditional_formatting.add("F5:F49", CellIsRule(operator="equal", formula=['"normal"'], fill=GOOD))
header_row(ws, 4, ["Statistik", "Puls", "SpO₂"], col=8)
stats = [("Middelværdi x̄", "AVERAGE"), ("Standardafvigelse s", "STDEV"), ("Nedre grænse x̄ − 2s", None),
         ("Øvre grænse x̄ + 2s", None), ("Antal målinger", "COUNT")]
for i, (name, fn) in enumerate(stats):
    r = 5 + i
    cell(ws, f"H{r}", name, None, BOLD)
    for col, src in (("I", "B"), ("J", "C")):
        if fn:
            f = f"={fn}({src}5:{src}49)"
        elif "Nedre" in name:
            f = f"={col}5-2*{col}6"
        else:
            f = f"={col}5+2*{col}6"
        cell(ws, f"{col}{r}", f, CALC, fmt="0" if fn == "COUNT" else "0.0")
ws["H11"] = "Regel: en måling er en AFVIGELSE, hvis |z| > 2, dvs. den ligger uden for x̄ ± 2s."
ws["H12"] = "Diskutér: Ville en høj puls lige efter løb også blive markeret? Hvad mangler modellen?"
ws["H11"].font = NOTE
ws["H12"].font = NOTE
widths(ws, {"A": 15, "B": 11, "C": 11, "D": 10, "E": 10, "F": 13, "G": 3, "H": 24, "I": 11, "J": 11})
sc = ScatterChart()
sc.title = "Hvilepuls – hver prik er én person"
sc.style = 13
sc.x_axis.title = "person nr."
sc.y_axis.title = "slag/min"
sc.height, sc.width = 9, 16
ws["L4"] = "Nr."
for i in range(45):
    ws[f"L{5 + i}"] = i + 1
ser = Series(Reference(ws, min_col=2, min_row=5, max_row=49), Reference(ws, min_col=12, min_row=5, max_row=49),
             title="Hvilepuls")
ser.marker.symbol = "circle"
ser.marker.size = 7
ser.graphicalProperties.line.noFill = True
sc.series.append(ser)
ws.column_dimensions["L"].hidden = True
ws.add_chart(sc, "H15")

# ============================================================================ AI-TEST HUDKRÆFT
ws = wb.create_sheet("AI-test hudkræft")
ws["A1"] = "Biologi – liveforsøg: test af AI-modellen på 40 billeder, den ikke har set før"
ws["A1"].font = TITLE
ws["A2"] = "Vælg 'Ondartet' eller 'Godartet' i kolonne B og C. 'Positiv' = AI siger ondartet."
ws["A2"].font = NOTE
header_row(ws, 4, ["Billede nr.", "Rigtigt svar", "AI's gæt", "AI-sikkerhed (%)", "Særligt ved billedet", "Resultat"])
dv = DataValidation(type="list", formula1='"Ondartet,Godartet"', allow_blank=True)
ws.add_data_validation(dv)
for i in range(40):
    r = 5 + i
    cell(ws, f"A{r}", i + 1)
    cell(ws, f"B{r}", "Ondartet" if i < 20 else "Godartet", INPUT)
    cell(ws, f"C{r}", None, INPUT)
    cell(ws, f"D{r}", None, INPUT)
    cell(ws, f"E{r}", None, INPUT, align=WRAP)
    dv.add(f"B{r}")
    dv.add(f"C{r}")
    cell(ws, f"F{r}", f'=IF(C{r}="","",IF(B{r}="Ondartet",IF(C{r}="Ondartet","Sand positiv","FALSK NEGATIV"),'
                      f'IF(C{r}="Godartet","Sand negativ","Falsk positiv")))', CALC, BOLD)
ws.conditional_formatting.add("F5:F44", FormulaRule(formula=['LEFT(F5,4)="Sand"'], fill=GOOD))
ws.conditional_formatting.add("F5:F44", FormulaRule(formula=['OR(F5="FALSK NEGATIV",F5="Falsk positiv")'], fill=BAD))
header_row(ws, 4, ["", "AI: ondartet", "AI: godartet"], col=8)
cell(ws, "H5", "Er ondartet", None, BOLD)
cell(ws, "H6", "Er godartet", None, BOLD)
cell(ws, "I5", '=COUNTIF(F5:F44,"Sand positiv")', GOOD, BOLD)
cell(ws, "J5", '=COUNTIF(F5:F44,"FALSK NEGATIV")', BAD, BOLD)
cell(ws, "I6", '=COUNTIF(F5:F44,"Falsk positiv")', BAD, BOLD)
cell(ws, "J6", '=COUNTIF(F5:F44,"Sand negativ")', GOOD, BOLD)
res = [("Træfsikkerhed", "=IFERROR((I5+J6)/(I5+J5+I6+J6),\"\")", "(SP + SN) / alle"),
       ("Sensitivitet", "=IFERROR(I5/(I5+J5),\"\")", "SP / (SP + FN) – andel af kræft fundet"),
       ("Specificitet", "=IFERROR(J6/(J6+I6),\"\")", "SN / (SN + FP) – andel af raske frikendt"),
       ("Gns. AI-sikkerhed", "=IFERROR(AVERAGE(D5:D44)/100,\"\")", "hvor sikker var modellen i gennemsnit")]
for i, (n, f, d) in enumerate(res):
    r = 9 + i
    cell(ws, f"H{r}", n, None, BOLD)
    cell(ws, f"I{r}", f, CALC, BOLD, "0.0%")
    ws[f"J{r}"] = d
    ws[f"J{r}"].font = NOTE
widths(ws, {"A": 11, "B": 13, "C": 13, "D": 15, "E": 30, "F": 16, "G": 3, "H": 20, "I": 14, "J": 40})

# ============================================================================ BTB
ws = wb.create_sheet("BTB")
ws["A1"] = "Kemi – CO₂ i udåndingsluft (BTB): tid til farveskift til gul"
ws["A1"].font = TITLE
header_row(ws, 3, ["Person", "Hvile (s)", "Efter arbejde (s)", "Forskel (s)"])
for i in range(3):
    r = 4 + i
    cell(ws, f"A{r}", f"Person {i + 1}", INPUT)
    cell(ws, f"B{r}", None, INPUT)
    cell(ws, f"C{r}", None, INPUT)
    cell(ws, f"D{r}", f'=IF(OR(B{r}="",C{r}=""),"",B{r}-C{r})', CALC)
cell(ws, "A7", "Gennemsnit", CALC, BOLD)
for col in "BCD":
    cell(ws, f"{col}7", f'=IFERROR(AVERAGE({col}4:{col}6),"")', CALC, BOLD, "0.0")
ws["A9"] = "Forventning: kortere tid efter arbejde, fordi der udåndes mere CO₂ → CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻"
ws["A9"].font = NOTE
widths(ws, {"A": 14, "B": 12, "C": 18, "D": 12})
bc = BarChart()
bc.title = "Tid til BTB bliver gul"
bc.y_axis.title = "sekunder"
bc.add_data(Reference(ws, min_col=2, max_col=3, min_row=3, max_row=6), titles_from_data=True)
bc.set_categories(Reference(ws, min_col=1, min_row=4, max_row=6))
bc.height, bc.width = 8, 14
ws.add_chart(bc, "F3")

# ============================================================================ HB-BINDINGSKURVE
ws = wb.create_sheet("Hb-bindingskurve")
ws["A1"] = "Kemi – model: hæmoglobins iltbindingskurve (Hill-ligningen)  S = pO₂ⁿ / (P50ⁿ + pO₂ⁿ)"
ws["A1"].font = TITLE
cell(ws, "A3", "n (samarbejde)", None, BOLD)
cell(ws, "B3", 2.7, INPUT)
cell(ws, "A4", "P50 hvile (kPa)", None, BOLD)
cell(ws, "B4", 3.6, INPUT)
cell(ws, "A5", "P50 arbejde (kPa)", None, BOLD)
cell(ws, "B5", 4.4, INPUT)
ws["C4"] = "normal (pH 7,4, 37 °C)"
ws["C5"] = "mere CO₂, lavere pH, varmere → kurven forskydes mod højre (Bohr-effekt)"
ws["C4"].font = NOTE
ws["C5"].font = NOTE
header_row(ws, 7, ["Sted", "pO₂ (kPa)", "Mætning hvile (%)", "Mætning arbejde (%)"])
places = [("Lunger", 13.3), ("Hvilende væv", 5.3), ("Arbejdende muskel", 2.7)]
for i, (n, p) in enumerate(places):
    r = 8 + i
    cell(ws, f"A{r}", n, None, BOLD)
    cell(ws, f"B{r}", p, INPUT)
    cell(ws, f"C{r}", f"=100*B{r}^$B$3/($B$4^$B$3+B{r}^$B$3)", CALC, BOLD, "0.0")
    cell(ws, f"D{r}", f"=100*B{r}^$B$3/($B$5^$B$3+B{r}^$B$3)", CALC, BOLD, "0.0")
ws["A12"] = "Ilt afgivet i musklen pr. 100 Hb-pladser (lunge − muskel):"
cell(ws, "C12", "=C8-C10", CALC, BOLD, "0.0")
cell(ws, "D12", "=D8-D10", CALC, BOLD, "0.0")
header_row(ws, 14, ["pO₂ (kPa)", "Hvile (%)", "Arbejde (%)"])
for i in range(61):
    r = 15 + i
    ws[f"A{r}"] = i * 0.25
    ws[f"B{r}"] = f"=100*A{r}^$B$3/($B$4^$B$3+A{r}^$B$3)"
    ws[f"C{r}"] = f"=100*A{r}^$B$3/($B$5^$B$3+A{r}^$B$3)"
    ws[f"B{r}"].number_format = ws[f"C{r}"].number_format = "0.0"
widths(ws, {"A": 22, "B": 12, "C": 18, "D": 20})
sc = ScatterChart()
sc.title = "Iltbindingskurve – hvile vs. arbejde"
sc.style = 13
sc.x_axis.title = "pO₂ (kPa)"
sc.y_axis.title = "iltmætning (%)"
sc.y_axis.scaling.min, sc.y_axis.scaling.max = 0, 100
sc.x_axis.scaling.min, sc.x_axis.scaling.max = 0, 15
sc.height, sc.width = 10, 18
xs = Reference(ws, min_col=1, min_row=15, max_row=75)
for col, title in ((2, "Hvile"), (3, "Arbejde (Bohr)")):
    s = Series(Reference(ws, min_col=col, min_row=15, max_row=75), xs, title=title)
    s.marker.symbol = "none"
    s.smooth = True
    sc.series.append(s)
ws.add_chart(sc, "F3")

# ============================================================================ GEOGRAFI-MODEL
ws = wb.create_sheet("Geografi-model")
ws["A1"] = "Geografi – AI-parathedsmodellen (1–5 point pr. faktor, 5 = bedst)"
ws["A1"].font = TITLE
countries = ["Danmark", "Australien", "USA", "Indien", "Nigeria"]
header_row(ws, 3, ["Faktor"] + countries + ["Begrundelse (skriv selv)"])
factors = [("Økonomi", [5, 5, 5, 2, 1]), ("Infrastruktur (strøm/internet)", [5, 5, 4, 3, 2]),
           ("Sundhedspersonale", [5, 5, 4, 2, 1]), ("Lige adgang til sundhed", [5, 4, 2, 2, 1]),
           ("Data der passer til befolkningen", [5, 5, 3, 2, 1]), ("Lovgivning og tillid", [5, 4, 4, 3, 2])]
for i, (f, vals) in enumerate(factors):
    r = 4 + i
    cell(ws, f"A{r}", f, None, BOLD, align=WRAP)
    for j, v in enumerate(vals):
        cell(ws, f"{'BCDEF'[j]}{r}", v, INPUT)
    cell(ws, f"G{r}", None, INPUT, align=WRAP)
pv = DataValidation(type="whole", operator="between", formula1="1", formula2="5")
ws.add_data_validation(pv)
pv.add("B4:F9")
cell(ws, "A10", "AI-parathed i alt (ud af 30)", CALC, BOLD)
for col in "BCDEF":
    cell(ws, f"{col}10", f"=SUM({col}4:{col}9)", CALC, BOLD)
header_row(ws, 13, ["Land", "BNP pr. indb. (USD)", "Internetbrugere (%)", "Læger pr. 1.000", "Middellevetid (år)",
                    "Medianalder (år)", "Melanom pr. 100.000", "Kilde + årstal"])
landedata = [("Danmark", 68000, 98, 4.2, 81, 42, "25–30"), ("Australien", 65000, 96, 4.0, 83, 38, "35–40"),
             ("USA", 80000, 92, 2.7, 77, 38, "15–20"), ("Indien", 2500, 50, 0.7, 70, 28, "under 1"),
             ("Nigeria", 1500, 45, 0.4, 54, 18, "under 1")]
for i, row in enumerate(landedata):
    r = 14 + i
    for j, v in enumerate(row):
        cell(ws, f"{'ABCDEFG'[j]}{r}", v, INPUT if j else None, BOLD if j == 0 else None)
    cell(ws, f"H{r}", "TJEK: Verdensbanken / Gapminder / GLOBOCAN", INPUT, align=WRAP)
ws["A20"] = "Tallene er afrundede ca.-tal (ca. 2021–2023) – tjek og opdater dem selv, og skriv kilde og årstal."
ws["A20"].font = NOTE
widths(ws, {"A": 32, "B": 14, "C": 14, "D": 14, "E": 14, "F": 14, "G": 16, "H": 36})
bc = BarChart()
bc.title = "AI-parathed (point ud af 30)"
bc.add_data(Reference(ws, min_col=2, max_col=6, min_row=10, max_row=10), from_rows=True, titles_from_data=False)
bc.set_categories(Reference(ws, min_col=2, max_col=6, min_row=3, max_row=3))
bc.legend = None
bc.y_axis.scaling.min, bc.y_axis.scaling.max = 0, 30
bc.height, bc.width = 8, 16
ws.add_chart(bc, "J3")

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print("Gemt:", OUT)
