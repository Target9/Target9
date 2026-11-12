# 3. Kemi – Hæmoglobin, ilt og fysisk aktivitet

> **Underspørgsmål:** Hvordan binder hæmoglobin ilt i blodet, og hvorfor ændrer iltmætningen sig ved fysisk aktivitet?
> **Kobling til forsøg:** Kemien **forklarer resultaterne** fra ugeforsøget (fysik). Hertil kommer et lille kemiforsøg med **BTB og CO₂** og en **model af bindingskurven** i regnearket.

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

Brug denne tabel, når I præsenterer data. Sæt jeres egne tal ind.

| Observation i forsøget | Kemisk/biologisk forklaring |
|---|---|
| **Pulsen steg** fra __ til __ slag/min | Musklerne bruger mere O₂ og laver mere CO₂. Hjertet pumper hurtigere for at transportere mere ilt til musklerne og fjerne CO₂. |
| **Iltmætningen (SpO₂) ændrede sig næsten ikke** (fx 98 % → 97 %) | Pulsoximeteret måler **arterieblodet**, der lige har været i lungerne. Højere vejrtrækning og den **flade top** på bindingskurven sørger for, at Hb næsten bliver fuldt mættet i lungerne igen. Det ekstra iltforbrug ses i **veneblodet** (SvO₂), som pulsoximeteret ikke måler. |
| **Lille fald i SpO₂** lige efter arbejde (hvis I så det) | (1) **Bohr-effekten**: højere temperatur og lavere pH forskyder kurven en smule til højre, også i arterieblodet. (2) Blodet passerer lungerne hurtigere, så der er lidt mindre tid til at binde ilt. (3) **Fejlmåling**: bevægelse og kolde fingre (se fysikguiden). Et fald på 1–2 procentpoint ligger inden for apparatets usikkerhed. |
| **Pulsen faldt igen** i restitutionen | CO₂-niveauet og pH normaliseres, og iltgælden betales tilbage. Hjertet behøver ikke pumpe så hurtigt længere. |
| **Forskel mellem personer** | Trænede personer har et større hjerte (slagvolumen) og flere røde blodlegemer, så de har lavere hvilepuls og hurtigere restitution. |
| **Hvornår ville SpO₂ falde rigtigt?** | Ved lungesygdom (fx lungebetændelse, COVID-19), i stor højde, ved hjertefejl, og nogle gange hos eliteatleter ved maksimalt arbejde. Det er netop dét, en AI-afvigelsesmodel skal opdage. |

---

## Del C – Ekstra kemiforsøg: CO₂ i udåndingsluft før og efter arbejde (BTB)

### Formål

At vise, at kroppen laver og udånder **mere CO₂** ved fysisk aktivitet, og at CO₂ danner **syre** i vand. Det er det samme, der sker i blodet (Bohr-effekten).

### Teori

**BTB (bromthymolblåt)** er en syre-base-indikator:
- **Blå** = basisk (pH > ca. 7,6)
- **Grøn** = neutral (ca. pH 7)
- **Gul** = sur (pH < ca. 6)

CO₂ fra udåndingsluften reagerer med vandet: CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻. De ekstra H⁺-ioner farver BTB gul.

### Materialer

3 bægerglas (100 mL), 50 mL vand i hvert, BTB-opløsning, **ét nyt sugerør pr. person**, stopur, hvidt papir som baggrund, sikkerhedsbriller.

### Fremgangsmåde

1. Hæld **50 mL vand** og **10 dråber BTB** i hvert af de tre glas. Opløsningen skal være **blå**. Hvis den er grøn, kan læreren tilsætte en lille dråbe fortyndet NaOH.
2. **Glas 1 = kontrol.** Det skal I ikke røre.
3. **Glas 2 = hvile.** Forsøgspersonen har siddet stille i 5 min og **puster roligt ud** gennem sugerøret ned i vandet, i sit normale vejrtrækningstempo. Start stopuret. Stop, når farven er **gul** (sammenlign med kontrollen). Notér tiden.
4. Forsøgspersonen laver **3 minutters arbejde** (samme som i ugeforsøget).
5. **Glas 3 = efter arbejde.** Samme person puster lige med det samme ud i et nyt glas, i det tempo kroppen selv vil (hurtigere vejrtrækning). Notér tiden til gul.
6. Gentag gerne med 2–3 personer.

> **Sikkerhed:** Pust kun **ud**, og sug aldrig. Ét sugerør pr. person. Brug briller. BTB kan farve tøj.

### Resultatskema

| Person | Tid til gul – hvile (s) | Tid til gul – efter arbejde (s) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| Gennemsnit | | |

### Forventet resultat og forklaring

Efter arbejde skifter farven **hurtigere**, fordi:
- musklerne har lavet mere CO₂ ved respiration
- man trækker vejret hurtigere og dybere, så der kommer mere CO₂ ud pr. minut

**Kobling:** Det samme CO₂ gør **blodet** lidt surere i de arbejdende muskler. Det får hæmoglobin til at **afgive mere ilt** (Bohr-effekten). Det er derfor, ilten havner præcis dér, hvor der er brug for den.

**Fejlkilder:** Det er svært at puste præcis lige meget hver gang. Det er subjektivt at bedømme, hvornår farven er "gul". Personerne har også forskellig lungekapacitet. Forbedring: Brug en pH-måler i stedet for at bedømme farven med øjet.

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
