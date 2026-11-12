# 7. Manuskript – guideline til fremlæggelsen

> **Sådan bruger I manuskriptet:** Det er en **guideline**, ikke noget, I skal læse op. Øv jer med det, til I kan sige det med jeres egne ord. Til prøven har I kun **stikordene** (de fede ord) med på et kort eller i talenoterne.
> **Samlet tid:** ca. 17 minutter + spørgsmål. Tiderne i parentes er vejledende.
> **P1** = biologi, **P2** = fysik, **P3** = kemi, **P4** = geografi. Slide-numrene passer til `05-powerpoint/FFFO-praesentation.pptx`.

---

## INTRO (ca. 1:30)

### Slide 1 – Titel · P1

> "Hej, og velkommen. Vi er [navne], og vores emne er **AI i sundhed – fra hudkræft til iltmætning**.
> Kunstig intelligens bliver brugt mere og mere på hospitaler, og vi ville finde ud af, hvordan det egentlig virker, og om det virker lige godt for alle."

**Stikord:** navne · AI i sundhed · virker det for alle?

### Slide 2 – Problemformulering · P1

> "Vores overordnede problemformulering er: **Hvordan kan kunstig intelligens hjælpe med at opdage sygdom og afvigelser i kroppen, og hvem får gavn af det?**
> Vi har delt den op i fire underspørgsmål, ét for hvert fag.
> I **biologi** ser vi på, hvordan kræftceller i huden adskiller sig fra raske celler, og hvor godt AI kan genkende hudkræft på billeder. Her har vi lavet et **liveforsøg**.
> I **fysik** ser vi på, hvordan et pulsoximeter måler puls og ilt **med lys**, og hvordan AI kan finde afvigelser i data.
> I **kemi** forklarer vi, hvordan **hæmoglobin binder ilt**, og bruger det til at forklare resultaterne fra vores **ugeforsøg**.
> Og i **geografi** ser vi på, **hvilke lande** der får gavn af AI, og hvad det betyder for kræftdiagnoser.
> Den røde tråd er, at AI'en i alle tilfælde skal kunne kende forskel på **normalt og afvigende** ud fra **data**."

**Stikord:** problemformulering · 4 fag · normalt vs. afvigende · data
**Overgang:** "Vi starter med biologien – hvad er det egentlig, AI'en skal finde?"

---

## BIOLOGI (ca. 5:00) · P1

### Slide 3 – Huden og hudkræft (0:45)

> "Huden består af overhud, læderhud og underhud. Næsten al hudkræft opstår i **overhuden**, fordi cellerne dér deler sig hele tiden, og fordi de bliver ramt af **UV-stråling**.
> Der er tre hovedtyper: **basalcellekarcinom**, som er den hyppigste og sjældent spreder sig, **planocellulært karcinom** fra pladecellerne, og **modermærkekræft**, altså melanom, fra de pigmentproducerende **melanocytter**. Melanom er den farligste, fordi den kan sprede sig tidligt."

**Stikord:** 3 lag · overhud · UV · basalcelle · planocellulær · melanom = farligst

### Slide 4 – Rask celle vs. kræftcelle (1:15)

> "Forskellen på en rask celle og en kræftcelle er både **genetisk, morfologisk og biologisk**.
> Genetisk: Kræft starter med **mutationer** i DNA'et, altså permanente ændringer i den genetiske sekvens. UV-lys kan fx skade DNA direkte.
> Morfologisk: Kræftceller har en **stor, uregelmæssig kerne**, det kaldes **nukleær atypi**. Cellerne har forskellig størrelse, og flere er i gang med at dele sig.
> Biologisk: Raske celler bliver i deres væv. Kræftceller kan **invadere** nabovævet og **metastasere**, altså sprede sig via blodet eller lymfen."

**Stikord:** genetisk (mutation) · morfologisk (nukleær atypi, mitoser) · biologisk (invasion, metastase)

### Slide 5 – Bilmodellen (1:00)

> "For at forklare, hvorfor cellen går amok, bruger vi en **bilmodel**.
> **Proto-onkogenerne** er speederen: De sætter gang i celledelingen. **Tumorsuppressorgenerne**, fx p53, er bremsen. **DNA-reparation** er mekanikeren, og **apoptose**, altså programmeret celledød, er skrotpladsen for ødelagte celler.
> I en kræftcelle sidder speederen fast i bund, bremserne virker ikke, og cellen undgår skrotpladsen. Det kræver typisk **flere** fejl på én gang, og derfor stiger risikoen med alderen.
> Modellens begrænsning er, at en celle har mange speedere og bremser, ikke bare én."

**Stikord:** speeder = proto-onkogen · bremse = tumorsuppressor/p53 · mekaniker = DNA-reparation · skrotplads = apoptose · begrænsning

### Slide 6 – Fra celler til billeder (1:00)

> "Lægen kan ikke se cellerne med det blotte øje, men forandringerne kan ses **på huden**. Derfor bruger man **ABCDE-reglen**: **A**symmetri, uregelmæssig kant (**B**order), flere farver (**C**olor), **D**iameter over 6 mm og **E**volution, altså forandring over tid.
> En AI ser billedet som **tal**: hver pixel har en værdi for rød, grøn og blå. Den bliver trænet på tusindvis af billeder, hvor svaret er kendt, og lærer selv mønstre, der minder om ABCDE.
> Men det er vigtigt at sige: AI'en ser hudens **overflade**. Den endelige diagnose stilles stadig ved en **biopsi** i mikroskop."

**Stikord:** ABCDE · pixels = tal · træning · overflade ≠ celler · biopsi

### Slide 7 – LIVEFORSØG (ca. 2:00 – det vigtigste!)

> "Nu vil vi vise vores liveforsøg. Vi har trænet en AI-model i **Teachable Machine** på **160 billeder** fra ISIC-databasen: 80 godartede modermærker og 80 melanomer.
> [Billede 1] Her er et godartet modermærke: symmetrisk, ensartet farve, skarp kant. AI'en siger godartet med __ %.
> [Billede 2] Her er et melanom: asymmetrisk og flere farver. AI'en siger ondartet med __ %.
> [Billede 3] Det her er et svært billede, og man kan se, at AI'en er **usikker**: __ mod __ %.
> [Billede 4] Og her **tager den fejl**. Det er et melanom, men den siger godartet. Det er en **falsk negativ**, og det er den farligste fejl, fordi patienten ville blive sendt hjem."

**Stikord:** Teachable Machine · 160 billeder · godartet · ondartet · usikker · fejl = falsk negativ
**Hvis teknikken svigter:** "Vi har heldigvis optaget demoen i forvejen" → start backup-videoen.

### Slide 8 – Resultater af AI-testen (1:00)

> "Vi testede modellen på **40 billeder**, den aldrig havde set før. Den gættede rigtigt i __ %.
> **Sensitiviteten** var __ %: Den fandt __ ud af 20 melanomer. **Specificiteten** var __ %: Den frikendte __ ud af 20 godartede.
> Til sammenligning viser forskning, fx **Esteva 2017 og Haenssle 2018**, at professionelle AI-modeller trænet på over 100.000 billeder er **lige så gode som hudlæger**.
> Men vores egne fejlkilder viser svaghederne: få data, og næsten kun **lys hud** i billederne. Forskning viser også, at AI kan lære **forkerte genveje**, fx pennestreger på huden.
> Så vores svar på biologi-spørgsmålet er: AI kan i høj grad genkende hudkræft, men **kun så godt som de data, den er trænet på**."

**Stikord:** 40 testbilleder · træfsikkerhed · sensitivitet · specificitet · Esteva/Haenssle · lys hud · genveje · kun så god som data
**Overgang til P2:** "AI'en i biologi ser på lys, der bliver kastet tilbage fra huden. [Navn] vil nu vise, hvordan man også kan bruge lys til at måle **inde i** kroppen."

---

## FYSIK (ca. 4:00) · P2

### Slide 9 – Lys: rødt og infrarødt (0:45)

> "Lys er elektromagnetiske bølger, og hver bølgelængde har sin farve. Et pulsoximeter bruger **rødt lys på 660 nanometer** og **infrarødt lys på 940 nanometer**, som vi ikke kan se.
> Energien i én foton er **E = h · c / λ**. For rødt lys giver det ca. **3 · 10⁻¹⁹ joule**. Det er under halvdelen af UV-lysets energi, og derfor er pulsoximeteret helt ufarligt. UV kan skade DNA, rødt lys kan ikke."

**Stikord:** 660 nm rødt · 940 nm IR · E = hc/λ · 3·10⁻¹⁹ J · ufarligt vs. UV
**Demo (10 sek.):** Hold fingeren over mobil-lommelygten: "Se, rødt lys går lige igennem fingeren."

### Slide 10 – Sådan virker pulsoximeteret (1:15)

> "I klemmen sidder to **lysdioder** på den ene side og en **fotodiode**, altså en lyssensor, på den anden. Lyset bliver sendt gennem fingeren, og noget bliver **absorberet**.
> Det smarte er, at **hæmoglobin med ilt** og **hæmoglobin uden ilt** absorberer lyset forskelligt. Hæmoglobin uden ilt absorberer meget mere rødt lys.
> Det meste lys absorberes konstant af hud, knogle og veneblod. Det er **DC-delen**. Men hver gang hjertet slår, udvider arterierne sig, og der absorberes lidt mere. Det er det pulserende **AC-signal**.
> **Pulsen** findes ud fra tiden mellem toppene: puls = 60 divideret med periodetiden. **Iltmætningen** findes ved at sammenligne AC-signalet for rødt og infrarødt lys. Fordi apparatet kun bruger det pulserende signal, måler det ilten i **arterieblodet**."

**Stikord:** LED + fotodiode · absorption · Hb vs. HbO₂ · DC konstant · AC pulserer · puls = 60/T · rødt/IR-forhold · arterieblod

### Slide 11 – Ugeforsøget: metode (0:30)

> "I vores ugeforsøg målte vi puls og iltmætning på alle fire i gruppen: først i **hvile**, så efter **3 minutters trappeløb**, og derefter hvert halve minut i **5 minutter**, mens vi restituerede. Vi testede også fejlkilder: **bevægelse, kolde fingre, neglelak og lys udefra**."

**Stikord:** hvile · 3 min arbejde · restitution 5 min · fejlkilder

### Slide 12 – Resultater (0:45)

> "Her ser I resultaterne. Pulsen steg fra i gennemsnit **__ til __** slag i minuttet og var tilbage nær hvile efter ca. **__ minutter**.
> Iltmætningen ændrede sig kun fra **__ % til __ %**. Bemærk, at y-aksen starter ved 90 %, så den lille ændring ser større ud, end den er. Ændringen ligger inden for apparatets usikkerhed på **±2 procentpoint**.
> Ved neglelak og kolde fingre fik vi [beskriv]. Hvorfor ilten ikke falder mere, forklarer [P3] om lidt."

**Stikord:** puls __ → __ · restitution __ min · SpO₂ __ → __ · y-akse fra 90 · ±2 · fejlkilder

### Slide 13 – AI og afvigelser (0:45)

> "Hvordan kan AI bruge sådanne data? Vi lavede en simpel **afvigelsesmodel** i Excel: Ud fra klassens hvilemålinger fandt vi **middelværdien og standardafvigelsen**. Målinger uden for **middel ± 2 standardafvigelser** bliver markeret som afvigelser. Den fangede fx vores neglelak-måling.
> Men den markerede også pulsen lige efter trappeløb, som jo er helt normal. Rigtig AI, fx i et **smartwatch**, lærer **din personlige normal** og kombinerer med **bevægelsessensoren**. I Apple Heart Study med over 400.000 deltagere kunne uret opdage **uregelmæssig hjerterytme**.
> Men også her er der **bias**: Et stort studie viste, at pulsoximetre oftere overser iltmangel hos personer med **mørk hud**, fordi melanin også absorberer lys."

**Stikord:** middel ± 2s · z-værdi · fanger neglelak · men ikke kontekst · smartwatch · personlig normal · atrieflimren · bias mørk hud
**Overgang til P3:** "Men hvorfor faldt iltmætningen næsten ikke, selvom vi løb op ad trapperne? Det er kemi."

---

## KEMI (ca. 3:30) · P3

### Slide 14 – Hæmoglobin (1:00)

> "Ilten bliver transporteret af **hæmoglobin**, et protein i de røde blodlegemer. [Hold modellen op] Hæmoglobin består af **fire proteinkæder**, og hver kæde har en **hæmgruppe** med en **jern-ion, Fe²⁺**, i midten. Det er jernet, der binder ilten. Ét hæmoglobin kan altså binde **fire O₂**.
> Bindingen er svag og kan gå begge veje. Det er vigtigt, fordi ilten både skal fanges i lungerne og afleveres i musklerne. Hvis jernet bliver til Fe³⁺, kan det ikke binde ilt."

**Stikord:** protein · 4 kæder · hæm · Fe²⁺ · 4 O₂ · reversibel binding
**Rekvisit:** hæmoglobinmodellen

### Slide 15 – Ligevægt og bindingskurve (1:15)

> "Bindingen er en **kemisk ligevægt**: Hb plus 4 O₂ ⇌ HbO₂. Ifølge **Le Chateliers princip** forskydes ligevægten efter, hvor meget ilt der er.
> I **lungerne** er der meget ilt, så ligevægten går mod højre, og hæmoglobinet bliver ca. **97 % mættet**. I **musklerne** er der lidt ilt, så den går mod venstre, og ilten bliver afgivet.
> Kurven er **S-formet**, fordi bindingen er **kooperativ**: Når den første ilt sidder fast, bliver det lettere for de næste. Det vigtige er den **flade top**: Selvom ilttrykket i lungerne ændrer sig lidt, forbliver mætningen næsten 100 %."

**Stikord:** Hb + 4O₂ ⇌ Hb(O₂)₄ · Le Chatelier · lunger → højre (97 %) · muskler → venstre · S-kurve · kooperativ · flad top

### Slide 16 – Fysisk aktivitet og vores resultater (1:15)

> "Når vi arbejder, laver musklerne mere energi ved **respiration**, og det giver mere **CO₂** og varme. CO₂ reagerer med vand og danner **kulsyre**, så blodet bliver **surere**. Det viste vi med **BTB**: Efter trappeløb blev BTB'en gul på __ sekunder mod __ sekunder i hvile.
> Det sure miljø og varmen får hæmoglobinet til at **slippe ilten lettere**. Det hedder **Bohr-effekten**, og kurven bliver forskudt mod højre. Så ilten havner præcis dér, hvor musklerne arbejder.
> Og nu kan vi forklare vores resultater: **Pulsen steg**, fordi blodet skulle cirkulere hurtigere. Men **iltmætningen** faldt næsten ikke, fordi pulsoximeteret måler **arterieblodet**, som lige har været i lungerne. Takket være den flade top bliver det mættet igen. Faldet i ilt sker i **veneblodet**, og det måler pulsoximeteret ikke."

**Stikord:** respiration → CO₂ · kulsyre · surere · BTB-resultat · Bohr-effekt · højreforskydning · puls ↑ · SpO₂ ≈ uændret · arterie vs. vene
**Overgang til P4:** "Vi har nu set, at teknologien virker på os. Men virker den lige godt for alle i verden? Det tager [Navn] sig af."

---

## GEOGRAFI (ca. 3:30) · P4

### Slide 17 – Faktorer (1:00)

> "Hudkræft er mest udbredt, hvor der er meget **UV-stråling** og mange med **lys hud**. Derfor har **Australien** verdens højeste forekomst, og **Danmark** ligger også højt, blandt andet på grund af solferier.
> Om et land får gavn af AI, afhænger af flere faktorer. Vi har fundet seks vigtige: **økonomi, infrastruktur** som strøm og internet, **sundhedspersonale**, **lige adgang** til sundhed, om der findes **data, der passer til befolkningen**, og **lovgivning og tillid**."

**Stikord:** UV + lys hud · Australien · Danmark · 6 faktorer

### Slide 18 – AI-parathedsmodellen (1:15)

> "Vi har lavet vores egen model, som vi kalder **AI-parathedsmodellen**. Vi har givet fem lande 1–5 point for hver faktor.
> **Danmark** får 30 af 30, fordi vi har gratis sundhedsvæsen, internet og data. **USA** får kun 22, selvom de er rige, fordi der er **ulige adgang**: Mange har ikke en sundhedsforsikring. **Indien** får 14 og **Nigeria** 8, fordi der er få læger, dårligere infrastruktur, og fordi AI'en ikke er trænet på mørk hud.
> Modellens **begrænsning** er, at pointene er vores egen vurdering, at alle faktorer vægter ens, og at der er stor forskel mellem by og land inden for et land."

**Stikord:** egen model · 5 lande · DK 30 · USA 22 (ulige) · Indien 14 · Nigeria 8 · begrænsninger

### Slide 19 – AI-paradokset og kræftdiagnose (1:15)

> "Det giver det, vi kalder **AI-paradokset**: De lande, der har **mest brug** for AI, fordi der er få læger, har **dårligst adgang** til den.
> For **kræftdiagnosticering** betyder det, at AI i Danmark kan bruges til at **sortere**, så hudlægerne tager de alvorlige tilfælde først, og ventetiderne bliver kortere. I fx Indien kan AI på en smartphone hjælpe i landsbyer **uden hudlæge**, men kun hvis den virker på **mørk hud**, og hvis der også er **behandling** bagefter.
> Den **demografiske transitionsmodel** viser også, at når lande udvikler sig, og befolkningen bliver ældre, får de flere kræfttilfælde, så behovet vil vokse."

**Stikord:** AI-paradoks · DK: triage, ventetid · Indien: smartphone, ingen hudlæge · mørk hud · behandling · DTM

---

## FÆLLES KONKLUSION (ca. 1:00) · P4 (eller alle på skift)

### Slide 20 – Konklusion

> "Så for at svare på vores problemformulering:
> **[P1]** AI kan genkende hudkræft på billeder næsten lige så godt som hudlæger, fordi kræftceller giver synlige forandringer.
> **[P2]** Med lys kan vi måle puls og ilt, og AI kan finde afvigelser i de data.
> **[P3]** Kemien forklarer, hvorfor iltmætningen er stabil hos raske, og det betyder, at et fald faktisk er et vigtigt faresignal.
> **[P4]** Men AI er **kun så god som dens data og det sundhedssystem, den bruges i**. Uden data om alle hudtyper og uden læger og behandling risikerer AI at øge uligheden.
> **[Alle/P4]** AI er et **stærkt hjælpeværktøj, ikke en læge**. Tak fordi I lyttede. Har I nogle spørgsmål?"

**Stikord:** én sætning pr. fag · kun så god som data og system · hjælpeværktøj, ikke læge · spørgsmål?

### Slide 21 – Kilder (vises kun, læses ikke op)

---

## Tidsoversigt

| Del | Person | Slides | Tid |
|---|---|---|---|
| Intro | P1 | 1–2 | 1:30 |
| Biologi + liveforsøg | P1 | 3–8 | 5:00 |
| Fysik + ugeforsøg | P2 | 9–13 | 4:00 |
| Kemi | P3 | 14–16 | 3:30 |
| Geografi | P4 | 17–19 | 3:30 |
| Konklusion | P4/alle | 20 | 1:00 |
| **I alt** | | | **ca. 18:30** |

**Skal I ned i tid?** Spring slide 5 (bilmodellen) og slide 9 (fotonenergi) over, og tag dem i stedet ved spørgsmålene, hvis censor spørger.
**Har I mere tid?** Tag pennestreg-testen med i live-demoen, og vis BTB-glassene frem.

## Gode vaner, når I fremlægger

- **Peg** på grafen/planchen, når I siger noget om den.
- **Brug fagordet, og forklar det med det samme** ("apoptose, altså programmeret celledød").
- **Overgange** binder fagene sammen. Øv dem særligt, for det er dér, censor ser, at det er *fællesfagligt*.
- **Kig på censor**, ikke på skærmen.
- Det er helt okay at sige: "Det ved jeg ikke præcist, men jeg tror, det hænger sammen med ..."
