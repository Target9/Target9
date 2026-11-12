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
    "1. Mobil-PPG – delforsøg 1: puls og lys (DC, AC/DC) fra mobilkameraet sammenlignet med pulsoximeteret.",
    "2. Måledagbog – delforsøg 2: 5 dage × 4 situationer + bevidste fejlmålinger. To AI-modeller markerer afvigelser.",
    "3. Dagbog-resultater – gennemsnit pr. situation og AI-blindtest (sensitivitet/specificitet for model A og B).",
    "4. Blå flaske – kemiforsøget: tid til farveløs ved 20, 30 og 40 °C.",
    "5. AI-test hudkræft – testskema til liveforsøget i biologi. Beregner sensitivitet, specificitet og træfsikkerhed.",
    "6. BTB – valgfrit kemiforsøg med CO₂ i udåndingsluft.",
    "7. Hb-bindingskurve – model af hæmoglobins iltbinding (Hill-ligningen) med Bohr-effekt. Prøv at ændre P50!",
    "8. Geografi-model – AI-parathedsmodellen (1–5 point pr. faktor) og landedata.",
    "",
    "Grafer til PowerPoint: Kopiér grafen (Ctrl+C) og indsæt i PowerPoint (Ctrl+V), eller højreklik på grafen i PowerPoint → Rediger data.",
    "Fanerne Mobil-PPG, Måledagbog og Blå flaske indeholder EKSEMPELDATA – overskriv dem med jeres egne.",
    "Skjulte kolonner i Måledagbog (K–M, O–P) er hjælpeberegninger til model B – dem skal I ikke røre.",
]
for i, t in enumerate(lines, start=3):
    ws.cell(row=i, column=1, value=t)
ws["A3"].font = BOLD
ws.column_dimensions["A"].width = 120

# ============================================================================ MOBIL-PPG
ws = wb.create_sheet("Mobil-PPG")
ws["A1"] = "Delforsøg 1 – Pulsmåler med mobilkameraet (resultater fra ppg-analyse/index.html)"
ws["A1"].font = TITLE
ws["A2"] = "EKSEMPELDATA i de gule felter – overskriv med jeres egne. Pulsoximeter-puls = gennemsnit af 3 aflæsninger under optagelsen."
ws["A2"].font = NOTE
header_row(ws, 4, ["Person / variant", "Puls mobil", "Puls oximeter", "Forskel", "Uregelm. slag",
                   "DC rød", "DC grøn", "DC blå", "AC/DC rød (%)", "AC/DC grøn (%)", "AC/DC blå (%)", "Kvalitet", "Note"])
ppg_rows = [
    ("Person 1", 64, 63, 0, 238, 41, 5, 0.8, 2.1, 0.4, "god", ""),
    ("Person 2", 73, 74, 1, 231, 37, 4, 0.7, 1.8, 0.3, "god", ""),
    ("Person 3", 79, 78, 0, 244, 46, 6, 0.6, 2.4, 0.5, "god", ""),
    ("Person 4", 68, 69, 0, 226, 35, 4, 0.9, 1.9, 0.4, "god", ""),
    ("a. Tryk hårdt (P1)", 63, 64, 0, 247, 58, 8, 0.3, 0.6, 0.2, "usikker", "blodet presses ud → lille AC"),
    ("b. Kold finger (P1)", 61, 62, 1, 236, 40, 5, 0.4, 0.9, 0.3, "god", "svagere signal"),
    ("c. Bevægelse (P1)", 88, 64, 6, 229, 39, 5, 1.9, 3.6, 1.1, "usikker", "falske slag"),
    ("d. Efter aktivitet (P1)", 112, 114, 0, 235, 40, 5, 0.9, 2.5, 0.4, "god", ""),
]
for i, row in enumerate(ppg_rows):
    r = 5 + i
    name, pm, po, irr, dr, dg, db, ar, ag, ab, q, note = row
    cell(ws, f"A{r}", name, None, BOLD, align=WRAP)
    for col, v in zip("BCEFGHIJKLM", (pm, po, irr, dr, dg, db, ar, ag, ab, q, note)):
        cell(ws, f"{col}{r}", v, INPUT, align=WRAP if col == "M" else None)
    cell(ws, f"D{r}", f'=IF(OR(B{r}="",C{r}=""),"",B{r}-C{r})', CALC, BOLD)
cell(ws, "A14", "Gns. personer 1–4", CALC, BOLD)
for col in "BCFGHIJK":
    cell(ws, f"{col}14", f'=IFERROR(AVERAGE({col}5:{col}8),"")', CALC, BOLD, "0.0")
cell(ws, "A15", "Gns. afvigelse mobil vs. oximeter (slag/min)", CALC, BOLD, align=WRAP)
cell(ws, "D15", '=IFERROR(SUMPRODUCT(ABS(B5:B8-C5:C8))/COUNT(B5:B8),"")', CALC, BOLD, "0.0")
ws["A17"] = "Blåt lys absorberes næsten helt (lav DC), rødt slipper bedst igennem (høj DC). Pulsoximeteret bruger rødt + infrarødt."
ws["A17"].font = NOTE
widths(ws, {"A": 26, "B": 11, "C": 13, "D": 9, "E": 12, "F": 9, "G": 9, "H": 9, "I": 13, "J": 14, "K": 13, "L": 10, "M": 28})
bc = BarChart()
bc.title = "Hvor meget lys slipper gennem fingeren? (DC, gns.)"
bc.y_axis.title = "lysstyrke (0–255)"
bc.add_data(Reference(ws, min_col=6, max_col=8, min_row=14, max_row=14), from_rows=True, titles_from_data=False)
bc.set_categories(Reference(ws, min_col=6, max_col=8, min_row=4, max_row=4))
bc.legend = None
bc.height, bc.width = 8, 14
ws.add_chart(bc, "O4")

# ============================================================================ MÅLEDAGBOG
ws = wb.create_sheet("Måledagbog")
ws["A1"] = "Delforsøg 2 – Måledagbog (5 dage × 4 situationer) med AI-blindtest"
ws["A1"].font = TITLE
ws["A2"] = ("EKSEMPELDATA – overskriv. Kolonne G (facit) udfyldes af en ANDEN person: 'Ja' for de bevidste fejlmålinger. "
            "Model A = hele gruppens normal. Model B = personens egen normal i samme situation (målingen selv tæller ikke med).")
ws["A2"].font = NOTE
ws["A2"].alignment = WRAP
ws.merge_cells("A2:N2")
ws.row_dimensions[2].height = 32
cell(ws, "P1", "Grænse for |z|", None, BOLD)
cell(ws, "Q1", 2, INPUT)
cell(ws, "P2", "Mindste spredning puls", None, BOLD)
cell(ws, "Q2", 4, INPUT)
cell(ws, "P3", "Mindste spredning SpO₂", None, BOLD)
cell(ws, "Q3", 1, INPUT)
ws["R2"] = "(apparatets usikkerhed – undgår deling med 0)"
ws["R2"].font = NOTE
header_row(ws, 5, ["Person", "Dag", "Situation", "Puls", "SpO₂ (%)", "Note", "Fejlmåling? (facit)",
                   "z puls (A)", "z SpO₂ (A)", "Model A", "n", "gns puls", "s puls", "z puls (B)",
                   "gns SpO₂", "s SpO₂", "z SpO₂ (B)", "Model B"])
SITS = ["Morgen – hvile", "Skole – siddende", "Efter aktivitet", "Aften – hvile"]
dv_sit = DataValidation(type="list", formula1='"' + ",".join(SITS) + '"', allow_blank=True)
dv_yn = DataValidation(type="list", formula1='"Ja,Nej"', allow_blank=True)
ws.add_data_validation(dv_sit)
ws.add_data_validation(dv_yn)

import random as _random
rnd = _random.Random(42)
base = {"Person 1": ([58, 66, 118, 62], 98), "Person 2": ([68, 76, 136, 72], 97),
        "Person 3": ([74, 82, 145, 78], 98), "Person 4": ([63, 70, 125, 66], 99)}
faults = {("Person 1", 2, 1): ("neglelak", 0, -8), ("Person 1", 4, 3): ("bevægelse", 30, -1),
          ("Person 2", 1, 0): ("kold finger", -2, -4), ("Person 2", 3, 1): ("lys udefra", 24, 0),
          ("Person 3", 2, 3): ("neglelak", 2, -7), ("Person 3", 5, 0): ("bevægelse", 28, 0),
          ("Person 4", 3, 1): ("kold finger", -3, -5), ("Person 4", 4, 0): ("lys udefra", 26, -1)}
diary = []
for day in range(1, 6):
    for si, sit in enumerate(SITS):
        for person, (pulses, sp) in base.items():
            sd = 8 if si == 2 else 3
            p = round(pulses[si] + rnd.gauss(0, sd))
            o = min(100, max(95, round(sp + rnd.gauss(0, 0.55) - (0.4 if si == 2 else 0))))
            diary.append((person, day, sit, p, o, "", "Nej"))
            key = (person, day, si)
            if key in faults:
                kind, dp, do = faults[key]
                fp = round(pulses[si] + dp + rnd.gauss(0, 2))
                diary.append((person, day, sit, fp, min(100, sp + do), "", "Ja"))
ROWS = 140
LAST = 5 + ROWS
rng = lambda c: f"${c}$6:${c}${LAST}"
for i in range(ROWS):
    r = 6 + i
    vals = diary[i] if i < len(diary) else (None,) * 7
    for col, v in zip("ABCDEFG", vals):
        cell(ws, f"{col}{r}", v, INPUT)
    dv_sit.add(f"C{r}")
    dv_yn.add(f"G{r}")
    empty = f'OR(D{r}="",E{r}="")'
    cell(ws, f"H{r}", f'=IF({empty},"",(D{r}-AVERAGE({rng("D")}))/STDEV({rng("D")}))', CALC, fmt="0.0")
    cell(ws, f"I{r}", f'=IF({empty},"",(E{r}-AVERAGE({rng("E")}))/MAX($Q$3,STDEV({rng("E")})))', CALC, fmt="0.0")
    cell(ws, f"J{r}", f'=IF({empty},"",IF(OR(ABS(H{r})>$Q$1,ABS(I{r})>$Q$1),"AFVIGELSE","normal"))', CALC, BOLD)
    cell(ws, f"K{r}", f'=IF({empty},"",COUNTIFS({rng("A")},A{r},{rng("C")},C{r}))', CALC)
    mask = f'({rng("A")}=A{r})*({rng("C")}=C{r})'
    cell(ws, f"L{r}", f'=IF(OR({empty},N(K{r})<3),"",(SUMIFS({rng("D")},{rng("A")},A{r},{rng("C")},C{r})-D{r})/(K{r}-1))', CALC, fmt="0.0")
    cell(ws, f"M{r}", f'=IF(L{r}="","",SQRT(MAX(0,(SUMPRODUCT({mask}*({rng("D")}-L{r})^2)-(D{r}-L{r})^2)/(K{r}-2))))', CALC, fmt="0.0")
    cell(ws, f"N{r}", f'=IF(L{r}="","",(D{r}-L{r})/MAX($Q$2,M{r}))', CALC, fmt="0.0")
    cell(ws, f"O{r}", f'=IF(OR({empty},N(K{r})<3),"",(SUMIFS({rng("E")},{rng("A")},A{r},{rng("C")},C{r})-E{r})/(K{r}-1))', CALC, fmt="0.0")
    cell(ws, f"P{r}", f'=IF(O{r}="","",SQRT(MAX(0,(SUMPRODUCT({mask}*({rng("E")}-O{r})^2)-(E{r}-O{r})^2)/(K{r}-2))))', CALC, fmt="0.0")
    cell(ws, f"Q{r}", f'=IF(O{r}="","",(E{r}-O{r})/MAX($Q$3,P{r}))', CALC, fmt="0.0")
    cell(ws, f"R{r}", f'=IF({empty},"",IF(L{r}="","for få data",IF(OR(ABS(N{r})>$Q$1,ABS(Q{r})>$Q$1),"AFVIGELSE","normal")))', CALC, BOLD)
for col in "JR":
    ws.conditional_formatting.add(f"{col}6:{col}{LAST}", CellIsRule(operator="equal", formula=['"AFVIGELSE"'], fill=BAD))
    ws.conditional_formatting.add(f"{col}6:{col}{LAST}", CellIsRule(operator="equal", formula=['"normal"'], fill=GOOD))
ws.conditional_formatting.add(f"G6:G{LAST}", CellIsRule(operator="equal", formula=['"Ja"'], fill=PatternFill("solid", fgColor="FFD64A")))
for col in "KLMOP":
    ws.column_dimensions[col].hidden = True
widths(ws, {"A": 11, "B": 6, "C": 17, "D": 8, "E": 9, "F": 14, "G": 12, "H": 10, "I": 10, "J": 12,
            "N": 10, "Q": 10, "R": 12})
ws.freeze_panes = "A6"

# ============================================================================ DAGBOG-RESULTATER
ws = wb.create_sheet("Dagbog-resultater")
ws["A1"] = "Resultater fra måledagbogen (beregnes automatisk – fejlmålinger er trukket fra gennemsnittene)"
ws["A1"].font = TITLE
D = "'Måledagbog'!"
dr = lambda c: f"{D}${c}$6:${c}${LAST}"
header_row(ws, 3, ["Situation", "Gns. puls", "Laveste puls", "Højeste puls", "Gns. SpO₂ (%)", "Laveste SpO₂", "Højeste SpO₂"])
for i, sit in enumerate(SITS):
    r = 4 + i
    cell(ws, f"A{r}", sit, None, BOLD)
    crit = f'{dr("C")},A{r},{dr("G")},"Nej"'
    cell(ws, f"B{r}", f'=IFERROR(AVERAGEIFS({dr("D")},{crit}),"")', CALC, BOLD, "0")
    cell(ws, f"C{r}", f'=IFERROR(_xlfn.MINIFS({dr("D")},{crit}),"")', CALC, None, "0")
    cell(ws, f"D{r}", f'=IFERROR(_xlfn.MAXIFS({dr("D")},{crit}),"")', CALC, None, "0")
    cell(ws, f"E{r}", f'=IFERROR(AVERAGEIFS({dr("E")},{crit}),"")', CALC, BOLD, "0.0")
    cell(ws, f"F{r}", f'=IFERROR(_xlfn.MINIFS({dr("E")},{crit}),"")', CALC, None, "0")
    cell(ws, f"G{r}", f'=IFERROR(_xlfn.MAXIFS({dr("E")},{crit}),"")', CALC, None, "0")

header_row(ws, 10, ["AI-blindtest", "Model A (gruppe)", "Model B (personlig)", "Forklaring"])
def cnt(model_col, facit, flag, extra=""):
    return f'=COUNTIFS({dr("G")},"{facit}",{dr(model_col)},"{flag}"{extra})'
rows = [
    ("Fejlmålinger fundet (sand positiv)", cnt("J", "Ja", "AFVIGELSE"), cnt("R", "Ja", "AFVIGELSE"), "fejlmåling markeret som afvigelse"),
    ("Fejlmålinger overset (falsk negativ)", cnt("J", "Ja", "normal"), cnt("R", "Ja", "normal"), "fejlmåling markeret som normal"),
    ("Falske alarmer (falsk positiv)", cnt("J", "Nej", "AFVIGELSE"), cnt("R", "Nej", "AFVIGELSE"), "normal måling markeret som afvigelse"),
    ("Korrekt normal (sand negativ)", cnt("J", "Nej", "normal"), cnt("R", "Nej", "normal"), ""),
    ("Sensitivitet", "=IFERROR(B11/(B11+B12),\"\")", "=IFERROR(C11/(C11+C12),\"\")", "andel af fejlmålinger fundet"),
    ("Specificitet", "=IFERROR(B14/(B14+B13),\"\")", "=IFERROR(C14/(C14+C13),\"\")", "andel af normale målinger, der ikke gav alarm"),
    ("Falske alarmer 'Efter aktivitet'", cnt("J", "Nej", "AFVIGELSE", f',{dr("C")},"Efter aktivitet"'),
     cnt("R", "Nej", "AFVIGELSE", f',{dr("C")},"Efter aktivitet"'), "høj puls efter løb er normal – men ligner en afvigelse"),
]
for i, (n, fa, fb, d) in enumerate(rows):
    r = 11 + i
    fmt = "0%" if n in ("Sensitivitet", "Specificitet") else "0"
    cell(ws, f"A{r}", n, None, BOLD, align=WRAP)
    cell(ws, f"B{r}", fa, CALC, BOLD, fmt)
    cell(ws, f"C{r}", fb, CALC, BOLD, fmt)
    ws[f"D{r}"] = d
    ws[f"D{r}"].font = NOTE
widths(ws, {"A": 34, "B": 17, "C": 19, "D": 14, "E": 14, "F": 13, "G": 13})
ch = BarChart()
ch.title = "Gennemsnitlig puls pr. situation"
ch.y_axis.title = "slag/min"
ch.add_data(Reference(ws, min_col=2, min_row=3, max_row=7), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=4, max_row=7))
ch.legend = None
ch.height, ch.width = 7.5, 14
ws.add_chart(ch, "I3")
ch2 = BarChart()
ch2.title = "Gennemsnitlig SpO₂ pr. situation"
ch2.y_axis.title = "%"
ch2.y_axis.scaling.min, ch2.y_axis.scaling.max = 90, 100
ch2.add_data(Reference(ws, min_col=5, min_row=3, max_row=7), titles_from_data=True)
ch2.set_categories(Reference(ws, min_col=1, min_row=4, max_row=7))
ch2.legend = None
ch2.height, ch2.width = 7.5, 14
ws.add_chart(ch2, "I19")
ch3 = BarChart()
ch3.title = "AI-blindtest: model A vs. model B"
ch3.add_data(Reference(ws, min_col=2, max_col=3, min_row=10, max_row=10), titles_from_data=True)
ch3.series = []
from openpyxl.chart import Series as _S
for col in (2, 3):
    s = _S(Reference(ws, min_col=col, min_row=15, max_row=16), title_from_data=False,
           title=ws.cell(row=10, column=col).value)
    ch3.series.append(s)
ch3.set_categories(Reference(ws, min_col=1, min_row=15, max_row=16))
ch3.y_axis.scaling.min, ch3.y_axis.scaling.max = 0, 1
ch3.y_axis.number_format = "0%"
ch3.height, ch3.width = 7.5, 14
ws.add_chart(ch3, "A20")

# ============================================================================ BLÅ FLASKE
ws = wb.create_sheet("Blå flaske")
ws["A1"] = "Kemi – Den blå flaske: tid fra rystning (10 gange) til væsken er farveløs"
ws["A1"].font = TITLE
ws["A2"] = "EKSEMPELDATA – overskriv med jeres egne målinger."
ws["A2"].font = NOTE
header_row(ws, 4, ["Temperatur (°C)", "Forsøg 1 (s)", "Forsøg 2 (s)", "Forsøg 3 (s)", "Gennemsnit (s)"])
for i, (t, a, b, c) in enumerate(((20, 62, 58, 65), (30, 33, 30, 35), (40, 17, 15, 18))):
    r = 5 + i
    cell(ws, f"A{r}", t, INPUT, BOLD)
    for col, v in zip("BCD", (a, b, c)):
        cell(ws, f"{col}{r}", v, INPUT)
    cell(ws, f"E{r}", f'=IFERROR(AVERAGE(B{r}:D{r}),"")', CALC, BOLD, "0.0")
header_row(ws, 10, ["'Hold den blå' i 1 min", "Antal rystninger"])
cell(ws, "A11", "ca. 20 °C", None, BOLD)
cell(ws, "B11", 2, INPUT)
cell(ws, "A12", "ca. 40 °C", None, BOLD)
cell(ws, "B12", 5, INPUT)
ws["A14"] = "Varmere → ilten bruges hurtigere → man skal 'trække vejret' (ryste) oftere for at holde væsken blå (iltet)."
ws["A14"].font = NOTE
widths(ws, {"A": 22, "B": 16, "C": 13, "D": 13, "E": 15})
sc = ScatterChart()
sc.title = "Tid til farveløs vs. temperatur"
sc.style = 13
sc.x_axis.title = "temperatur (°C)"
sc.y_axis.title = "tid (s)"
sc.height, sc.width = 8, 14
s = Series(Reference(ws, min_col=5, min_row=5, max_row=7), Reference(ws, min_col=1, min_row=5, max_row=7), title="Gennemsnit")
s.marker.symbol = "circle"
s.marker.size = 8
sc.series.append(s)
sc.legend = None
ws.add_chart(sc, "G4")

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
ws["A1"] = "Kemi (valgfrit) – CO₂ i udåndingsluft (BTB): tid til farveskift til gul"
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
