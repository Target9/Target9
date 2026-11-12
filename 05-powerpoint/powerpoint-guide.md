# 5. PowerPoint – guide

Filen **`FFFO-praesentation.pptx`** er en færdig skabelon med 21 slides, diagrammer, grafer der kan redigeres, og **talenoter** (stikord og manus) under hver slide. Den følger manuskriptet i `07-manuskript/manuskript.md` slide for slide.

## Det skal I selv gøre

| # | Opgave | Hvor |
|---|---|---|
| 1 | Skriv jeres **navne, klasse og skole** | Slide 1 |
| 2 | Indsæt **4 testbilleder** fra jeres AI-forsøg | Slide 7 (stiplede felter) |
| 3 | Ret **konfusionsmatrix og procenter** til jeres egne tal | Slide 8 (gul mærkat = eksempeldata) |
| 4 | Indsæt **foto** af jer under ugeforsøget | Slide 11 |
| 5 | Udskift **graferne** med jeres målinger: højreklik på grafen → *Rediger data* → indsæt tal fra `maaleskema.xlsx` | Slide 12, 13 |
| 6 | Skriv **BTB-resultatet** | Slide 16 |
| 7 | Indsæt et **verdenskort** over modermærkekræft (GLOBOCAN eller Our World in Data) | Slide 17 |
| 8 | Ret **pointene** i AI-parathedsmodellen, hvis I vurderer anderledes | Slide 18 |
| 9 | Fjern alle gule **"EKSEMPELDATA"**-mærkater, når tallene er jeres egne | Slide 8, 12, 13, 16 |

## Slideoversigt

| Slide | Titel | Person | Indhold |
|---|---|---|---|
| 1 | Titel | P1 | Emne, navne |
| 2 | Problemformulering | P1 | Overordnet spørgsmål + 4 underspørgsmål + rød tråd |
| 3 | Huden og de tre typer hudkræft | P1 | Hudens lag, UV, basalcelle / planocellulær / melanom |
| 4 | Rask hudcelle vs. kræftcelle | P1 | Tegning af celler + tabel (genetisk, morfologisk, celledød, væv) |
| 5 | Model: Cellen som en bil | P1 | Speeder, bremse, mekaniker, skrotplads + begrænsning |
| 6 | Fra celler til billeder: ABCDE og AI | P1 | ABCDE-reglen + hvordan et neuralt netværk "ser" |
| 7 | **LIVEFORSØG** | P1 | 4 testbilleder → skift til Teachable Machine |
| 8 | Resultat: Hvor god er vores AI? | P1 | Konfusionsmatrix, sensitivitet, specificitet, forskning, fejlkilder |
| 9 | Lys: rødt og infrarødt | P2 | Spektrum, \(E = hc/\lambda\), UV vs. rødt + lommelygte-demo |
| 10 | Sådan virker pulsoximeteret | P2 | Skitse, PPG-signal, AC/DC, puls = 60/T, R og SpO₂ |
| 11 | Ugeforsøg: metode | P2 | 4 trin, kontrolvariable, sikkerhed |
| 12 | Ugeforsøg: resultater | P2 | Grafer over puls og SpO₂ + tabel |
| 13 | AI og afvigelser i data | P2 | Punktdiagram med normalområde, 3 niveauer af AI, bias |
| 14 | Hæmoglobin – blodets iltbærer | P3 | Model af Hb (4 kæder, Fe²⁺, O₂) + fakta |
| 15 | Ligevægt og den S-formede bindingskurve | P3 | Reaktion, Le Chatelier, tabel, bindingskurve |
| 16 | Bohr-effekten forklarer vores resultater | P3 | Respiration, kulsyre, forskudt kurve, forklaringstabel |
| 17 | Hvem får gavn af AI? Seks faktorer | P4 | Verdenskort + 6 faktorer |
| 18 | Vores model: AI-parathedsmodellen | P4 | Pointtabel + søjlediagram + begrænsninger |
| 19 | AI-paradokset og kræftdiagnosticering | P4 | Behov/adgang-diagram, DK vs. Indien/Nigeria, DTM |
| 20 | Konklusion | Alle | Én sætning pr. fag + hovedbudskab |
| 21 | Kilder | – | Vises kun |

## Designregler (hvis I laver flere slides)

- **Farvekode pr. fag:** biologi = grøn, fysik = blå, kemi = rød, geografi = orange, fælles = mørkeblå. Det hjælper censor med at følge med i, hvilket fag I er i.
- **Maks. 6 linjer tekst pr. slide.** Resten siger I, og det står i talenoterne.
- **Én pointe pr. slide.** Titlen skal kunne læses som en sætning.
- **Grafer skal have akser med enhed** (slag/min, %, kPa). Sig det højt, når y-aksen ikke starter ved 0 (SpO₂-grafen).
- **Skriftstørrelse mindst 14**, så det kan læses bagerst i lokalet.
- **Billeder:** Brug egne fotos fra forsøgene. Billeder fra nettet skal have kilde.

## Sådan bruger I talenoterne

- PowerPoint: *Diasshow* → *Brug præsentationsvisning*. Så ser I noterne på jeres skærm, mens censor ser slides.
- Google Slides: *Præsenter* → *Præsentationsvisning*.
- Print noterne som støttekort: *Filer* → *Udskriv* → *Noteside*.

## Live-demoen (slide 7) – teknisk tjekliste

1. Åbn Teachable Machine-projektet i en **separat browserfane**, før prøven starter.
2. Sæt *Preview* til **File** (ikke webcam, for det er mere stabilt).
3. Læg de 4 testbilleder i en mappe på skrivebordet med navnene `1_godartet.jpg`, `2_melanom.jpg`, `3_svaer.jpg` og `4_fejl.jpg`.
4. Skift mellem PowerPoint og browser med **Alt + Tab** (Mac: **Cmd + Tab**).
5. **Backup-video** ligger på skrivebordet. Hvis noget går galt, så sig det roligt og afspil videoen.

## Hvis I vil lave filen om

Filen er genereret med `tools/make_presentation.py` (Python + `python-pptx`). I kan bare redigere `.pptx`-filen direkte i PowerPoint. Scriptet behøver I ikke røre.
