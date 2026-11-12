# 2. Fysik – Pulsoximeteret: lys, puls, iltmætning og AI

> **Underspørgsmål:** Hvordan måler en pulsoximeter puls og iltmætning ved hjælp af lys, og hvordan kan AI bruge den slags data til at opdage afvigelser?
> **Forsøg:** Ugeforsøg om puls og iltmætning (hvile → arbejde → restitution) + delforsøg om fejlkilder.

---

## Del A – Teori

### A1. Lys er elektromagnetisk stråling

- Lys er bølger med en **bølgelængde** \(\lambda\) (lambda), som måles i nanometer (nm).
- Synligt lys går fra ca. 400 nm (violet) til 700 nm (rødt). Lige over 700 nm kommer **infrarødt lys (IR)**, som vi ikke kan se.
- Lys består af små energipakker kaldet **fotoner**. Energien af én foton er

\[ E = \frac{h \cdot c}{\lambda} \]

hvor \(h = 6{,}63 \cdot 10^{-34}\ \text{J·s}\) (Plancks konstant) og \(c = 3{,}00 \cdot 10^{8}\ \text{m/s}\) (lysets fart).

| Lys | Bølgelængde | Fotonenergi | Bruges til |
|---|---|---|---|
| UV-B (sol) | 300 nm | \(6{,}6 \cdot 10^{-19}\) J | Kan skade DNA (hudkræft) |
| Rødt | **660 nm** | \(3{,}0 \cdot 10^{-19}\) J | Pulsoximeter |
| Infrarødt | **940 nm** | \(2{,}1 \cdot 10^{-19}\) J | Pulsoximeter |

**Regneeksempel (rødt lys):**
\[ E = \frac{6{,}63 \cdot 10^{-34} \cdot 3{,}00 \cdot 10^{8}}{660 \cdot 10^{-9}} = 3{,}0 \cdot 10^{-19}\ \text{J} \]

**Pointe:** Rødt og infrarødt lys har **for lidt energi til at skade DNA**, så pulsoximeteret er helt ufarligt. UV-lys har dobbelt så meget energi pr. foton og kan skade DNA. Her kobler fysik og biologi sig sammen.

### A2. Når lys møder stof: refleksion, transmission og absorption

Lys, der rammer fingeren, kan blive:
- **reflekteret** (kastet tilbage)
- **transmitteret** (sendt igennem)
- **absorberet** (opsuget, og energien bliver til varme)

Jo **mere stof** lyset skal igennem, og jo **mere farvestof** der er, jo mere bliver absorberet. Det beskrives med **Lambert-Beers lov** (ekstra niveau):

\[ I = I_0 \cdot 10^{-\varepsilon \cdot c \cdot l} \]

\(I_0\) er lyset, der sendes ind, \(I\) er lyset, der kommer ud, \(\varepsilon\) er hvor godt stoffet absorberer, \(c\) er koncentrationen, og \(l\) er længden, lyset skal igennem.

### A3. Hvorfor netop rødt og infrarødt lys?

Blodets farvestof, **hæmoglobin**, findes i to former (se kemiguiden):
- **Oxyhæmoglobin (HbO₂)** med ilt bundet er **lyserødt**. Det absorberer **meget lidt rødt lys** og **lidt mere infrarødt**.
- **Deoxyhæmoglobin (Hb)** uden ilt er **mørkerødt**. Det absorberer **meget rødt lys** (ca. 10 gange mere end HbO₂ ved 660 nm).

| | Rødt lys (660 nm) | Infrarødt lys (940 nm) |
|---|---|---|
| **Hb** (uden ilt, mørkerødt) | Absorberer **meget** | Absorberer lidt |
| **HbO₂** (med ilt, lyserødt) | Absorberer **meget lidt** | Absorberer lidt mere end Hb |

Tegn det på planchen som to søjlepar (rødt og IR) eller som de to absorptionskurver. Søg på "hemoglobin absorption spectrum", eller tegn det selv ud fra tabellen.

Ved at sammenligne, hvor meget **rødt** og hvor meget **infrarødt** lys der kommer igennem, kan apparatet regne ud, hvor stor en del af hæmoglobinet der bærer ilt.

### A4. Sådan virker pulsoximeteret (trin for trin)

1. På den ene side af klemmen sidder **to lysdioder (LED)**: én rød (660 nm) og én infrarød (940 nm). De blinker på skift hundredvis af gange i sekundet.
2. På den anden side sidder en **fotodiode** (lyssensor), som måler, hvor meget lys der kommer igennem fingeren (**transmission**). Smartwatches måler i stedet det lys, der kastes tilbage (**refleksion**), fordi sensoren sidder på samme side.
3. Det meste lys absorberes af hud, knogle, væv og blod i venerne. Den del er **konstant**, og den kaldes **DC-delen**.
4. Hver gang hjertet slår, udvider **arterierne** sig med lidt mere iltrigt blod. Så absorberes der lidt mere lys. Det giver et lille **pulserende signal**, som kaldes **AC-delen**. Kurven kaldes et **PPG-signal** (fotopletysmografi).

```
Lys der kommer igennem
   ↑    /\      /\      /\      /\        ← AC: pulserer med hjerteslag
   |   /  \    /  \    /  \    /  \
   |__/    \__/    \__/    \__/    \__
   |                                       ← DC: konstant (væv, knogle, veneblod)
   |
   +----------------------------------→ tid
       |<- T ->|   T = periodetid (tid mellem to slag)
```

5. **Puls** findes ud fra tiden mellem toppene:
\[ \text{puls} = \frac{60}{T} \quad (\text{slag pr. minut, når } T \text{ er i sekunder}) \]
*Eksempel:* \(T = 0{,}80\) s giver \(\text{puls} = 60 / 0{,}80 = 75\) slag/min.

6. **Iltmætning (SpO₂)** findes ud fra forholdet mellem det pulserende signal for rødt og for infrarødt lys:
\[ R = \frac{AC_{\text{rød}} / DC_{\text{rød}}}{AC_{\text{IR}} / DC_{\text{IR}}} \]
Producenten har målt sammenhængen på raske forsøgspersoner (kalibrering). En typisk tilnærmelse er
\[ \text{SpO}_2 \approx 110 - 25 \cdot R \]
*Eksempel:* \(R = 0{,}5\) giver \(\text{SpO}_2 \approx 110 - 12{,}5 = 97{,}5\ \%\). Jo **mindre** R, jo **mere** ilt.

7. Det smarte er, at apparatet **kun bruger AC-delen**, altså det pulserende arterieblod. Derfor måler det iltmætningen i **arterierne**, og ikke i hele fingeren.

**Normalværdier**

| Måling | Normal (rask ung i hvile) | Bemærk |
|---|---|---|
| Puls | 60–100 slag/min (trænede kan ligge lavere) | Stiger ved arbejde, nervøsitet, feber |
| SpO₂ | 95–100 % | Under ca. 92 % bør man kontakte en læge. Apparatet har en usikkerhed på ca. ±2 procentpoint. |

### A5. Begrænsninger ved pulsoximeteret (fysikken bag fejlkilderne)

| Problem | Fysisk forklaring |
|---|---|
| **Bevægelse** | Bevægelse ændrer, hvor langt lyset skal igennem (l i Lambert-Beer). Det giver et falsk AC-signal. |
| **Kolde fingre** | Blodkarrene trækker sig sammen, så AC-signalet bliver for svagt |
| **Neglelak (mørk)** | Neglelakken absorberer lys, så der kommer for lidt lys til sensoren |
| **Stærkt lys udefra** | Sollys og lamper indeholder både rødt og IR-lys, som forstyrrer sensoren |
| **Kulilteforgiftning** | Hæmoglobin med CO (HbCO) er også lyserødt, så apparatet tror, det er ilt, og viser en **falsk høj** værdi (se kemi) |
| **Mørk hud** | Melanin absorberer også lys. Apparaterne er især kalibreret på lys hud. Et stort amerikansk studie (Sjoding m.fl., *NEJM* 2020) viste, at skjult iltmangel blev overset næsten **3 gange så ofte** hos sorte patienter. Det kobler til geografi og bias. |

### A6. Hvordan kan AI bruge data til at opdage afvigelser?

En **afvigelse** (anomali) er en måling, der ikke passer til det normale mønster.

**Trin 1: Regelbaseret.** Det gør et almindeligt apparat: "Alarm, hvis SpO₂ < 92 % eller puls > 120 i hvile". Det er simpelt, men det kender ikke personen eller situationen.

**Trin 2: Statistisk model** (det laver I selv i regnearket). Ud fra mange målinger på raske personer findes:
- **middelværdien** \(\bar{x}\)
- **standardafvigelsen** \(s\), som viser, hvor meget målingerne normalt spreder sig

Ca. 95 % af normale målinger ligger inden for \(\bar{x} \pm 2s\). En måling udenfor er **mistænkelig**. Man kan regne en **z-værdi** ud:
\[ z = \frac{x - \bar{x}}{s} \]
Hvis \(|z| > 2\), markeres målingen som en afvigelse.

*Eksempel:* Klassens hvilepuls har \(\bar{x} = 74\) og \(s = 9\). En elev har 102. \(z = (102 - 74)/9 = 3{,}1\), så det er en afvigelse.

**Trin 3: Maskinlæring (rigtig AI).** I smartwatches og på hospitaler trænes modeller på **millioner** af målinger. De lærer:
- **den enkelte persons normal** (din hvilepuls er måske 58 og ikke 74)
- **sammenhæng** (høj puls er normal, når accelerometeret viser, at du løber, men unormal, når du sover)
- **mønstre i selve PPG-kurven**: uregelmæssig afstand mellem slagene kan være **atrieflimren** (hjerterytmeforstyrrelse)

Eksempel: I *Apple Heart Study* (Perez m.fl., *NEJM* 2019) deltog over 400.000 personer. Uret advarede om uregelmæssig puls, og hos ca. en tredjedel af dem, der fik en advarsel og blev undersøgt nærmere, fandt man faktisk atrieflimren.

På hospitaler bruges AI til **tidlig varsling**: Den kombinerer puls, SpO₂, vejrtrækning, blodtryk og temperatur og advarer personalet, *før* patienten bliver kritisk syg.

**Kobling til biologi:** Det er præcis samme princip som hudkræft-AI'en. Den lærer, hvad "normalt" ser ud som, og markerer det, der afviger. Og samme svagheder gælder: skæve data, fejlmålinger og falske alarmer.

---

## Del B – Ugeforsøg: Puls og iltmætning (trin for trin)

### Formål

At undersøge, hvordan **puls** og **iltmætning** ændrer sig fra **hvile → fysisk arbejde → restitution**. Derudover at undersøge, hvilke faktorer der giver **fejlmålinger**, og at bygge en simpel **afvigelsesmodel**.

### Hypoteser (eksempler; skriv jeres egne, *før* I måler)

1. Pulsen stiger kraftigt ved arbejde og falder igen i restitutionsperioden.
2. Iltmætningen ændrer sig **kun lidt** (forbliver over 95 %), fordi lungerne kan nå at mætte blodet med ilt. *Kemien forklarer hvorfor.*
3. Kolde fingre, neglelak og bevægelse giver dårligere eller forkerte målinger.

### Variable

| Type | I dette forsøg |
|---|---|
| Uafhængig variabel (det, I ændrer) | Aktivitetsniveau (hvile/arbejde) og tid efter arbejde |
| Afhængige variable (det, I måler) | Puls (slag/min) og SpO₂ (%) |
| Kontrolvariable (holdes ens) | Samme finger, samme apparat, siddende stilling ved målingen, rolig hånd, samme type arbejde og varighed |

### Materialer

Pulsoximeter, stopur, trappe/step-bænk/sjippetov, lommelygte, mørk neglelak, skål med koldt vand, regnearket `skabeloner/maaleskema.xlsx`.

### Forsøg 1 – Hvile (alle personer)

1. Forsøgspersonen sidder stille i **5 minutter**.
2. Sæt pulsoximeteret på **pegefingeren** og hold hånden i ro på bordet i hjertehøjde.
3. Vent, til tallet er stabilt (ca. 10–15 sekunder).
4. Aflæs **puls og SpO₂ 3 gange** med 30 sekunders mellemrum, og skriv dem i fanen **"Hvile"**.
5. Regnearket finder gennemsnittet.

### Forsøg 2 – Arbejde og restitution (alle personer)

1. Forsøgspersonen laver **3 minutters arbejde**: trappeløb, step-test (op/ned ad en bænk i fast tempo, fx 30 gange pr. minut) eller sjip. **Alle i gruppen skal lave det samme.**
2. **Lige efter** (t = 0) sætter forsøgspersonen sig ned, og I sætter oximeteret på med det samme.
3. Aflæs puls og SpO₂ ved **0, 30, 60, 90, 120, 180, 240 og 300 sekunder**.
4. Skriv det i fanen **"Arbejde og restitution"**. Grafen tegnes automatisk.
5. **Restitutionstid:** Notér, hvor lang tid der går, før pulsen er under *hvilepuls + 10*.

> Tip: Én person er forsøgsperson, én aflæser, én styrer stopuret, og én skriver. Byt roller.

### Forsøg 3 – Fejlkilder (fysikken i praksis)

Mål på én person i hvile. Først en normal måling, derefter én ændring ad gangen:

| Delforsøg | Fremgangsmåde | Hvad forventer I? |
|---|---|---|
| a. Bevægelse | Ryst hånden let under målingen | Svingende eller forkert puls |
| b. Kold finger | Hånden i koldt vand i 1 min, tør, og mål | Langsommere og svagere signal |
| c. Neglelak | Mørk neglelak på neglen, lad tørre, og mål | Lavere eller ingen måling |
| d. Lys udefra | Lys med lommelygten direkte på klemmen | Forstyrret måling |
| e. Klem/tryk | Tryk fingeren hårdt mod bordet | Svagere AC-signal (mindre blodgennemstrømning) |

Notér både tal og **hvor lang tid** apparatet var om at finde et signal.

### Forsøg 4 – Demo: Se lyset gå gennem fingeren (godt til prøven!)

1. Gør rummet mørkt.
2. Hold en finger over mobilens lommelygte.
3. Fingeren lyser **rødt**, fordi rødt lys trænger meget bedre gennem væv og blod end blåt og grønt lys. Blod absorberer de andre farver.
4. **Bonus:** Læg fingeren over både kamera og blitz på en mobil og åbn kameraet (eller en pulsmåler-app). Billedet flimrer svagt i takt med pulsen. Det er præcis PPG-princippet!

### Forsøg 5 (valgfrit) – Klassedata og AI-afvigelsesmodel

1. Saml alle gruppers **hvilepuls og hvile-SpO₂** i fanen **"Klassedata og afvigelser"** (jo flere, jo bedre).
2. Regnearket beregner middelværdi, standardafvigelse og **normalområdet** \(\bar{x} \pm 2s\).
3. Hver måling får en **z-værdi** og bliver markeret "AFVIGELSE", hvis \(|z| > 2\).
4. Indsæt bevidst en "syg" eller fejlmålt værdi (fx SpO₂ = 88 % fra neglelak-forsøget), og vis, at modellen fanger den.
5. Diskutér: Er pulsen *lige efter arbejde* en afvigelse? Modellen siger ja, men det er jo normalt! Pointen er, at **AI'en skal kende sammenhængen**. Det er derfor, smartwatches også bruger bevægelsessensoren.

> **Sikkerhed:** Hold aldrig vejret for at få iltmætningen ned. Det er ikke nødvendigt for forsøget, og hos raske personer falder SpO₂ alligevel næsten ikke ved kort vejrholdning.

### Databehandling

1. **Graf 1:** Puls (y) mod tid efter arbejde (x) for alle i gruppen.
2. **Graf 2:** SpO₂ (y) mod tid efter arbejde (x). Sæt y-aksen fra 90 til 100 %, så I kan se de små ændringer, men sig det højt, når I viser den.
3. **Tabel:** Hvile vs. lige efter arbejde (gennemsnit for gruppen).
4. **Udregn** ændringen i puls i % og ændringen i SpO₂ i procentpoint.

### Typiske resultater (så I ved, hvad I kan forvente)

| | Hvile | Lige efter arbejde | Efter 5 min |
|---|---|---|---|
| Puls | 65–85 | 130–180 | tæt på hvile + 10–20 |
| SpO₂ | 96–99 % | 94–99 % (ofte uændret eller **lidt** lavere) | 96–99 % |

> Hvis SpO₂ falder til fx 93 % lige efter arbejde, så tjek, om hånden var i ro. Bevægelse og kolde, sammentrukne blodkar er de hyppigste årsager til et "fald" lige efter arbejde. Det er en vigtig fejlkildediskussion.

### Fejlkilder (sammenfatning)

- Måleusikkerhed på ca. ±2 procentpoint for SpO₂ og ±1–2 slag for puls
- Bevægelse og nervøsitet lige efter arbejdet
- Forskellig tid fra stop til første måling
- Forsøgspersonerne arbejdede ikke lige hårdt
- Få forsøgspersoner (4), så der er stor tilfældighed
- Billigt apparat, der ikke er medicinsk kalibreret

### Konklusion (skabelon)

> "Pulsen steg fra gennemsnitligt __ til __ slag/min (__ %) og var tilbage nær hvileniveau efter ca. __ minutter. Iltmætningen ændrede sig kun fra __ % til __ %, altså inden for apparatets usikkerhed. Pulsoximeteret måler dette ved at sende rødt (660 nm) og infrarødt (940 nm) lys gennem fingeren og sammenligne, hvor meget der absorberes af iltet og ikke-iltet hæmoglobin i det pulserende arterieblod. Vores afvigelsesmodel kunne finde unormale målinger, men den kunne ikke skelne mellem sygdom, fejlmåling og normal høj puls efter arbejde. Det kræver mere data og information om sammenhængen, og det er netop dét, rigtig AI kan."

---

## Kilder (fysik)

- Fysik/kemi-bogen (kapitler om lys, bølger og energi)
- Sundhed.dk: *Iltmætning / pulsoximetri*
- Sjoding, M.W. m.fl. (2020): *Racial bias in pulse oximetry measurement*. New England Journal of Medicine 383.
- Perez, M.V. m.fl. (2019): *Large-scale assessment of a smartwatch to identify atrial fibrillation*. New England Journal of Medicine 381.
- Producentens brugsanvisning til jeres pulsoximeter (nøjagtighed og bølgelængder)
