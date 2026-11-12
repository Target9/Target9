# 3. Kemi – Hæmoglobin, ilt og fysisk aktivitet

> **Underspørgsmål:** Hvordan binder hæmoglobin ilt i blodet, og hvorfor ændrer iltmætningen sig ved fysisk aktivitet?
> **Kobling til forsøg:** Kemien **forklarer resultaterne** fra ugeforsøgets måledagbog (fysik). Kemiens egen del af ugeforsøget er **den blå flaske**, en model af iltoptag og iltforbrug. Dertil kommer en **model af bindingskurven** i regnearket.

---

## Del A – Teori

### A1. Hvad er hæmoglobin?

- **Hæmoglobin (Hb)** er et **protein** i de **røde blodlegemer**. Hvert rødt blodlegeme indeholder ca. 270 millioner hæmoglobinmolekyler.
- Ét hæmoglobinmolekyle består af **4 proteinkæder** (2 α-kæder og 2 β-kæder).
- Hver kæde har en **hæmgruppe**: en ringformet organisk struktur (en *porfyrinring*) med en **jern-ion, Fe²⁺**, i midten.
- Det er **jernionen**, der binder iltmolekylet (O₂).
- Derfor kan **ét hæmoglobin binde op til 4 O₂-molekyler**.

```
          α-kæde           β-kæde
        [ hæm Fe²⁺ ]     [ hæm Fe²⁺ ]
             ↑ O₂             ↑ O₂
        [ hæm Fe²⁺ ]     [ hæm Fe²⁺ ]
          β-kæde           α-kæde
       = 4 pladser til ilt pr. hæmoglobin
```

**Hvorfor jern?** Jern er et overgangsmetal, som kan danne en **svag, reversibel binding** (kompleksbinding) til ilt. Bindingen skal være stærk nok til at fange ilten i lungerne, men svag nok til at slippe den i musklerne. Hvis jernet bliver oxideret til **Fe³⁺** (methæmoglobin), kan det **ikke** binde ilt. Det er også derfor, vi har brug for jern i kosten: mangler man jern, laver kroppen for lidt hæmoglobin (**blodmangel/anæmi**).

### A2. Bindingen er en kemisk ligevægt

\[ \text{Hb} + 4\,\text{O}_2 \;\rightleftharpoons\; \text{Hb(O}_2\text{)}_4 \]

Dobbeltpilen betyder, at reaktionen kan gå begge veje. Hvilken vej den går, afhænger af, **hvor meget ilt der er** (iltens partialtryk, pO₂). Det er **Le Chateliers princip**: Ligevægten forskydes, så den modvirker ændringen.

| Sted | pO₂ | Ligevægten forskydes mod | Resultat |
|---|---|---|---|
| **Lungerne** | Højt (ca. 13 kPa / 100 mmHg) | **Højre** → | Hb binder ilt (bliver *mættet*) |
| **Musklerne i hvile** | Middel (ca. 5 kPa / 40 mmHg) | ← Venstre | Hb afgiver en del af ilten |
| **Arbejdende muskler** | Lavt (ca. 2–3 kPa / 15–20 mmHg) | ←← Mere til venstre | Hb afgiver **meget** ilt |

### A3. Iltmætning

**Iltmætning** er den procentdel af hæmoglobinets ilt-pladser, der er optaget:

\[ \text{iltmætning} = \frac{\text{HbO}_2}{\text{Hb} + \text{HbO}_2} \cdot 100\ \% \]

- **SaO₂/SpO₂** er mætningen i **arterieblodet**, som lige har været i lungerne. Normalt er den 95–100 %. Det er den, pulsoximeteret måler (fysik).
- **SvO₂** er mætningen i **veneblodet**, som kommer tilbage fra kroppen. Normalt er den ca. 75 % i hvile, og den kan falde til 20–40 % i musklernes vener under hårdt arbejde.

### A4. Den S-formede bindingskurve (samarbejde mellem pladserne)

Når det første O₂ binder sig, ændrer hæmoglobinmolekylet form en smule. Så bliver det **lettere for de næste** O₂ at binde sig. Det kaldes **kooperativ binding**. Det giver en **S-formet (sigmoid) kurve**:

```
Iltmætning (%)
100 |                    ____________  ← lungerne (flad top = sikkerhedsmargin)
 90 |                 _/
 75 |              _/ ← hvilende væv
 50 |            /  ← P50 ≈ 3,6 kPa
 30 |          / ← arbejdende muskel
 10 |       _/
  0 |_____/________________________________
     0    2    4    6    8    10   12   14   pO₂ (kPa)
```

Kurven kan beskrives med **Hill-ligningen** (dette bruges i regnearket):

\[ S = \frac{(pO_2)^n}{(P_{50})^n + (pO_2)^n} \]

hvor \(n \approx 2{,}7\) (graden af samarbejde) og \(P_{50} \approx 3{,}6\ \text{kPa}\) (det tryk, hvor Hb er 50 % mættet).

| pO₂ | Beregnet mætning |
|---|---|
| 13,3 kPa (lunger) | ca. **97 %** |
| 5,3 kPa (hvilende væv) | ca. **75 %** |
| 2,7 kPa (arbejdende muskel) | ca. **31 %** |

**To vigtige pointer fra kurven:**
1. **Den flade top:** Selvom iltrykket i lungerne falder lidt (fx ved hårdt arbejde eller lidt oppe i bjergene), er mætningen næsten uændret. Det er en *sikkerhedsmargin*.
2. **Den stejle midte:** Et lille fald i pO₂ i musklerne får Hb til at afgive **meget** ilt. Det er perfekt til at levere ilt, præcis hvor der er brug for det.

### A5. Hvad sker der ved fysisk aktivitet? (Bohr-effekten)

Musklerne laver energi ved **respiration**:

\[ \text{C}_6\text{H}_{12}\text{O}_6 + 6\,\text{O}_2 \rightarrow 6\,\text{CO}_2 + 6\,\text{H}_2\text{O} + \text{energi} \]

Ved arbejde bruger musklerne **mere O₂** og laver **mere CO₂ og varme**. CO₂ reagerer med vand i blodet og danner kulsyre, som gør blodet surere:

\[ \text{CO}_2 + \text{H}_2\text{O} \;\rightleftharpoons\; \text{H}_2\text{CO}_3 \;\rightleftharpoons\; \text{H}^+ + \text{HCO}_3^- \]

Ved meget hårdt arbejde laver musklerne også **mælkesyre (laktat)**, som giver endnu flere H⁺-ioner.

**Bohr-effekten:** H⁺-ioner og CO₂ binder sig til hæmoglobinet og ændrer dets form, så det **slipper ilten lettere**. Det samme gør en højere temperatur. Bindingskurven **forskydes mod højre**:

| Faktor ved arbejde | Ændring | Effekt på Hb |
|---|---|---|
| Mere CO₂ | ↑ | Afgiver mere O₂ |
| Lavere pH (flere H⁺) | ↓ pH | Afgiver mere O₂ |
| Højere temperatur | ↑ | Afgiver mere O₂ |
| Lavere pO₂ i musklen | ↓ | Afgiver mere O₂ |

**Smart:** Kroppen afleverer automatisk **mere ilt til de muskler, der arbejder mest**, fordi det er dér, det er surest og varmest.

### A6. Kroppens svar: mere ilt ind og mere CO₂ ud

- **Vejrtrækningen** bliver hurtigere og dybere. Hjernen reagerer især på stigende CO₂ og faldende pH.
- **Pulsen** stiger, så blodet cirkulerer hurtigere. Det kunne I måle i forsøget.
- Derfor kan lungerne **blive ved med at mætte arterieblodet**, selvom musklerne bruger meget mere ilt.

### A7. Kulilte (CO) – når kemien snyder fysikken

- Kulilte (CO, fra brand, udstødning og dårlige brændeovne) binder sig til jernet **ca. 200–250 gange stærkere** end ilt.
- CO "stjæler" pladserne, så blodet ikke kan transportere ilt. Det er livsfarligt.
- HbCO er **lyserødt** ligesom HbO₂, så et almindeligt pulsoximeter tror, det er ilt, og viser en **falsk normal værdi**. Det er et godt eksempel på, at data og AI kun er så gode som målingen bag dem.

---

## Del B – Forklaring af jeres resultater fra ugeforsøget

Brug denne tabel, når I præsenterer data fra **måledagbogen** (fysik) og **den blå flaske** (kemi). Sæt jeres egne tal ind.

| Observation i forsøget | Kemisk/biologisk forklaring |
|---|---|
| **Pulsen var højest "efter aktivitet"** (__ slag/min mod __ om morgenen) | Musklerne bruger mere O₂ og laver mere CO₂ ved respiration. Hjertet pumper hurtigere for at levere ilt og fjerne CO₂. |
| **SpO₂ lå stabilt (96–99 %) i alle situationer** | Pulsoximeteret måler **arterieblodet**, der lige har været i lungerne. Når musklerne bruger mere ilt, trækker vi vejret hurtigere, og den **flade top** på bindingskurven sørger for, at Hb bliver næsten fuldt mættet igen. Det ekstra iltforbrug ses i **veneblodet**, som pulsoximeteret ikke måler. Det er det samme, I så i den blå flaske: Så længe "vejrtrækningen" (rystningen) følger med forbruget, forbliver opløsningen blå. |
| **Lavest puls om morgenen** | Kroppen er i hvile, og stofskiftet og iltbehovet er lavt. |
| **Fejlmålingerne gav lav SpO₂** (fx neglelak: __ %) | Det er *ikke* kemi, men fysik: Neglelakken absorberer lyset, så apparatet regner forkert. Kemisk er ilten i blodet uændret. |
| **Forskel mellem personer** | Trænede personer har et større hjerte (slagvolumen) og flere røde blodlegemer, så de har lavere hvilepuls. Derfor er en **personlig** normal bedre end gruppens gennemsnit. |
| **Den blå flaske affarvedes hurtigere i varmt vand** | Kemiske reaktioner går hurtigere ved højere temperatur, så ilten blev brugt hurtigere. På samme måde bruger varme, arbejdende muskler ilten hurtigere, og Bohr-effekten får hæmoglobinet til at afgive mere. |
| **Hvornår ville SpO₂ falde rigtigt?** | Ved lungesygdom (fx lungebetændelse, COVID-19), i stor højde, ved hjertefejl og nogle gange hos eliteatleter ved maksimalt arbejde. Fordi SpO₂ normalt er så stabil, er selv et fald på få procentpoint et vigtigt **faresignal**, og det er præcis dét, en AI-afvigelsesmodel skal opdage. |

---

## Del C – Kemiforsøg: Den blå flaske (model af iltoptag og iltforbrug)

### Formål

At undersøge en reaktion, hvor **farven viser, om der er ilt til stede**, og hvordan **temperaturen** påvirker, hvor hurtigt ilten bliver brugt. Forsøget er en model af blodets balance mellem **iltoptag i lungerne** og **iltforbrug i musklerne**.

### Teori (forenklet)

I flasken er der vand, en base (KOH eller NaOH), **glukose** og farvestoffet **methylenblåt**.

1. **Glukose** reagerer med methylenblåt, så det bliver **farveløst**. Glukosen "bruger" farvestoffets evne til at reagere med ilt.
2. Når I **ryster** flasken, opløses **ilt (O₂)** fra luften i væsken. Ilten reagerer med det farveløse stof, så det bliver **blåt** igen.
3. Når ilten er **brugt op**, bliver væsken farveløs igen. Det kan gentages mange gange.

\[ \text{blå (ilt til stede)} \;\xrightarrow{\text{glukose bruger ilten}}\; \text{farveløs (ingen ilt)} \;\xrightarrow{\text{ryst: O}_2\text{ fra luften}}\; \text{blå} \]

| I flasken | I kroppen |
|---|---|
| Rystning = ilt opløses fra luften | **Lungerne**: ilt optages i blodet |
| Glukose bruger ilten | **Respiration** i musklerne: C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O |
| Blå farve = der er ilt | **Lyserødt HbO₂** = iltet blod |
| Farveløs = ilten er brugt | **Mørkerødt Hb** = blod uden ilt |
| Varmere vand = hurtigere forbrug | **Arbejdende muskler** er varmere og bruger ilten hurtigere |
| Farven aflæses med øjet | **Pulsoximeteret** "aflæser farven" med lys |

### Materialer

- 1 L konisk kolbe med gummiprop. Kun halvt fyldt, så der er luft (ilt) over væsken.
- 300 mL vand, ca. 8 g KOH (eller ca. 6 g NaOH), ca. 10 g glukose (druesukker), 5 dråber methylenblåt (1 %). **Læreren afvejer basen.**
- 3 vandbade/baljer: ca. 20 °C (stuetemperatur), ca. 30 °C og ca. 40 °C (varmt vand fra hanen) + termometer
- Stopur, hvidt papir som baggrund
- Sikkerhedsbriller og handsker

### Fremgangsmåde

1. Læreren opløser basen i vandet i kolben. Tilsæt glukose og methylenblåt, og sæt proppen i.
2. Lad kolben stå, til væsken er **farveløs** (1–3 min).
3. **Ryst kolben kraftigt 10 gange** (tæl højt, så det er ens hver gang). Væsken bliver blå.
4. Stil kolben på bordet, og **start stopuret**. Stop, når væsken er **farveløs** (sammenlign med det hvide papir). Notér tiden.
5. Gentag 3 gange ved **stuetemperatur**.
6. Stil kolben i vandbadet ved **30 °C** i 5 minutter, og gentag trin 3–4 tre gange. Mål væskens temperatur.
7. Gentag ved **40 °C**.
8. **Variant (valgfri):** Ryst 5 gange og 20 gange (i stedet for 10) ved samme temperatur. Mere rystning giver mere opløst ilt og en længere blå periode.
9. **Variant: "Hold den blå"** (valgfri, men god til fremlæggelsen): Ved 20 °C og ved 40 °C prøver I at holde væsken blå i 1 minut ved at ryste kort, hver gang den begynder at blive lys. Tæl, hvor mange gange I skal ryste. Ved 40 °C skal I ryste oftere, ligesom man trækker vejret hurtigere under arbejde for at holde blodet iltet.

> **Sikkerhed:** KOH og NaOH er **ætsende**. Brug briller og handsker. Proppen skal sidde fast, når I ryster. Methylenblåt farver hud og tøj. Følg lærerens anvisning til bortskaffelse (normalt i vasken med rigeligt vand).

### Resultatskema (fanen **Blå flaske** i regnearket)

| Temperatur (°C) | Forsøg 1 (s) | Forsøg 2 (s) | Forsøg 3 (s) | Gennemsnit (s) |
|---|---|---|---|---|
| ca. 20 | | | | |
| ca. 30 | | | | |
| ca. 40 | | | | |

### Forventet resultat og forklaring

- Tiden til farveløs bliver **kortere**, jo varmere det er. Ofte halveres tiden for hver ca. 10 °C. Det skyldes, at molekylerne bevæger sig hurtigere og støder oftere sammen, så reaktionen går hurtigere.
- **Kobling til kroppen:** Arbejdende muskler er varmere og har et højere stofskifte, så de bruger ilten hurtigere. Derfor stiger **pulsen og vejrtrækningen**, og det er præcis, hvad I målte i måledagbogen. Så længe tilførslen følger med forbruget, forbliver blodet i arterierne iltmættet, og det er derfor, SpO₂ var stabil.
- Efter mange gentagelser bliver væsken gullig, og den blå periode bliver kortere, fordi glukosen og ilten i flasken bruges op.

### Modellens begrænsninger (skal med!)

- Methylenblåt **reagerer kemisk** med ilten (det oxideres). Hæmoglobin **binder** ilten løst, uden at jernet ændres (Fe²⁺ forbliver Fe²⁺).
- Modellen viser **ikke** den S-formede kurve (kooperativ binding) eller Bohr-effektens pH-afhængighed.
- Den viser kun balancen mellem **tilførsel og forbrug** af ilt, og hvordan temperatur påvirker forbruget.

**Fejlkilder:** Det er svært at ryste præcis lige hårdt. Det er subjektivt, hvornår væsken er "farveløs". Temperaturen falder, mens kolben står på bordet. Forbedring: Brug et lysmåler-app (mobilens lyssensor) eller et kolorimeter for at måle farven objektivt.

### Valgfrit ekstra: BTB og CO₂ i udåndingsluft

Hvis I har tid, kan I vise, at CO₂ gør vand surt (og dermed blodet, jf. Bohr-effekten): Pust med et sugerør ud i 50 mL vand med 10 dråber **BTB** (blå → gul ved syre), først i hvile og så efter 2 min trappeløb, og tag tid til farveskiftet. Efter aktivitet skifter farven hurtigere, fordi der udåndes mere CO₂: CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻. *Sikkerhed: Pust kun ud, og brug ét sugerør pr. person.* Fanen **BTB** i regnearket kan bruges til resultaterne.

---

## Del D – Modeller

### Model 1: Bindingskurven i regnearket

Fanen **"Hb-bindingskurve"** i `skabeloner/maaleskema.xlsx` tegner to kurver med Hill-ligningen:
- **Normal** (hvile): \(P_{50} = 3{,}6\) kPa
- **Arbejdende muskel** (mere CO₂, lavere pH, varmere): \(P_{50} = 4{,}4\) kPa (kurven forskudt mod højre)

Brug modellen til at vise:
1. Mætningen i lungerne (13,3 kPa) er **næsten ens** for begge kurver. Derfor ændrer jeres SpO₂ sig næsten ikke.
2. Ved musklen (2,7 kPa) afgiver hæmoglobinet **ekstra ilt**, når kurven er forskudt.

**Begrænsning:** Hill-ligningen er en forenkling. Den rigtige kurve afhænger også af fx 2,3-BPG (et stof i de røde blodlegemer), og tallene er gennemsnit.

### Model 2: Fysisk hæmoglobinmodel (til at holde op til prøven)

Byg et hæmoglobin af LEGO, perler eller molekylebyggesæt:
- 4 store klodser = 4 proteinkæder
- 4 røde "plader" med et **gult** jern i midten = hæmgrupper med Fe²⁺
- 4 blå kugler (O=O) = iltmolekyler, der kan sættes på og tages af
- Vis: I **lungerne** sætter I alle 4 O₂ på. I **musklen** tager I 2–3 af, og de bliver lettere at tage af, når I lægger nogle "H⁺/CO₂-klodser" på modellen (Bohr-effekten).

**Begrænsning:** Den rigtige struktur er tredimensionel og foldet, og formændringen ved kooperativ binding kan modellen ikke vise.

### Model 3: Ligevægts-vippen (Le Chatelier)

Tegn en vippe på tavlen: **Hb + 4 O₂** på venstre side, **Hb(O₂)₄** på højre side.
- Lungerne: Læg "meget O₂" på venstre side, så vippen tipper mod højre, og Hb binder ilt.
- Musklen: Lidt O₂ og meget CO₂/H⁺, så vippen tipper mod venstre, og Hb afgiver ilt.

---

## Kilder (kemi)

- Fysik/kemi-bogen (kapitler om kemiske reaktioner, syre/base og ligevægt)
- Biologibogen (kredsløb, respiration og blodet)
- Sundhed.dk: *Kulilteforgiftning* og *Blodmangel*
- Hill-konstanter: standardværdier fra lærebøger i fysiologi (\(n \approx 2{,}7\), \(P_{50} \approx 26{,}8\) mmHg ≈ 3,6 kPa)
