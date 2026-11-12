# 2. Fysik – Pulsoximeteret: lys, puls, iltmætning og AI

> **Underspørgsmål:** Hvordan måler en pulsoximeter puls og iltmætning ved hjælp af lys, og hvordan kan AI bruge den slags data til at opdage afvigelser?
> **Forsøg:** Ugeforsøg "Find din egen normal": (1) byg en pulsmåler med mobilkameraet og (2) en 5-dages måledagbog med AI-blindtest.

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

**Trin 2: Statistisk model** (det laver regnearket på jeres måledagbog). Ud fra mange målinger på raske personer findes:
- **middelværdien** \(\bar{x}\)
- **standardafvigelsen** \(s\), som viser, hvor meget målingerne normalt spreder sig

Ca. 95 % af normale målinger ligger inden for \(\bar{x} \pm 2s\). En måling udenfor er **mistænkelig**. Man kan regne en **z-værdi** ud:
\[ z = \frac{x - \bar{x}}{s} \]
Hvis \(|z| > 2\), markeres målingen som en afvigelse.

*Eksempel:* Gruppens puls har \(\bar{x} = 74\) og \(s = 9\). En elev har 102. \(z = (102 - 74)/9 = 3{,}1\), så det er en afvigelse.

**Trin 3: Maskinlæring (rigtig AI).** I smartwatches og på hospitaler trænes modeller på **millioner** af målinger. De lærer:
- **den enkelte persons normal** (din hvilepuls er måske 58 og ikke 74)
- **sammenhæng** (høj puls er normal, når accelerometeret viser, at du løber, men unormal, når du sover)
- **mønstre i selve PPG-kurven**: uregelmæssig afstand mellem slagene kan være **atrieflimren** (hjerterytmeforstyrrelse)

Eksempel: I *Apple Heart Study* (Perez m.fl., *NEJM* 2019) deltog over 400.000 personer. Uret advarede om uregelmæssig puls, og hos ca. en tredjedel af dem, der fik en advarsel og blev undersøgt nærmere, fandt man faktisk atrieflimren.

På hospitaler bruges AI til **tidlig varsling**: Den kombinerer puls, SpO₂, vejrtrækning, blodtryk og temperatur og advarer personalet, *før* patienten bliver kritisk syg.

**Kobling til biologi:** Det er præcis samme princip som hudkræft-AI'en. Den lærer, hvad "normalt" ser ud som, og markerer det, der afviger. Og samme svagheder gælder: skæve data, fejlmålinger og falske alarmer.

---

## Del B – Ugeforsøg: "Find din egen normal" (trin for trin)

### Hvorfor er forsøget bygget sådan?

Hos raske personer ændrer **iltmætningen sig næsten ikke**, heller ikke ved hårdt arbejde (det forklarer kemien). Et forsøg, der kun måler "før og efter løb", giver derfor kedelige SpO₂-data. I stedet undersøger I de tre ting, jeres problemformulering faktisk spørger om:

| Delforsøg | Hvad undersøger I? | Svarer på |
|---|---|---|
| **1. Byg en pulsmåler med mobilen** (dag 1) | Hvordan lys gennem fingeren afslører pulsen, og hvorfor forskellige farver lys opfører sig forskelligt | *Hvordan måler en pulsoximeter puls ved hjælp af lys?* |
| **2. Måledagbog med AI-blindtest** (dag 1–5) | Hvad der er "normalt" for hver af jer, og om en AI-model kan finde de målinger, der er forkerte | *Hvordan kan AI bruge data til at opdage afvigelser?* |
| **3. Den blå flaske** (dag 2, se kemiguiden) | En model af, hvordan ilt bindes og forbruges | *Kemi: hvorfor ændrer iltmætningen sig (ikke)?* |

### Hypoteser (skriv jeres egne, *før* I måler)

1. Mobilkameraet kan måle den samme puls som pulsoximeteret (±5 slag/min), fordi blodet absorberer lys i takt med hjerteslagene.
2. Rødt lys slipper bedst gennem fingeren, mens blåt lys næsten bliver helt absorberet.
3. Pulsen varierer meget mellem situationer (hvile/aktivitet), men iltmætningen ligger stabilt på 95–100 %.
4. En AI-model, der kender **personen og situationen**, finder flere fejlmålinger og giver færre falske alarmer end en model, der bare bruger hele gruppens gennemsnit.

### Materialer

- 1–2 pulsoximetre (fingerclips)
- Mobiltelefoner med kamera og lommelygte
- Computer med Chrome eller Edge og analyseværktøjet **`02-fysik/ppg-analyse/index.html`** (åbn filen ved at dobbeltklikke, og det virker uden internet)
- Regnearket `skabeloner/maaleskema.xlsx` (fanerne **Mobil-PPG** og **Måledagbog**)
- Mørk neglelak + neglelakfjerner, skål med koldt vand (til fejlmålingerne)

---

### Delforsøg 1 – Byg en pulsmåler med mobilen (ca. 45 min)

**Ideen:** Mobilens lommelygte sender hvidt lys (alle farver) ind i fingeren, og kameraet måler, hvor meget der slipper igennem. Hver gang hjertet slår, kommer der mere blod i fingeren, og det absorberer lidt mere lys, så billedet bliver en anelse mørkere. Det er præcis det, et pulsoximeter gør, bare med rødt og infrarødt lys.

**Fremgangsmåde**

1. Forsøgspersonen sidder ned og har siddet stille i 3 minutter.
2. Sæt pulsoximeteret på **venstre** pegefinger.
3. Tænd mobilens **lommelygte**, og start **videooptagelse** med bagkameraet.
4. Læg **højre** pegefinger **let** over både kamera og lommelygte. Skærmen bliver rød.
5. Optag i **30 sekunder**, og hold hånden **helt stille** på bordet. En anden aflæser pulsoximeterets puls 3 gange undervejs.
6. Overfør videoen til computeren (AirDrop, mail, Google Drev eller kabel).
7. Åbn `ppg-analyse/index.html`, klik **Vælg video**, og vent, mens videoen afspilles.
8. Skriv resultaterne i fanen **Mobil-PPG**: pulsen fra mobilen og fra oximeteret, samt **DC** og **AC/DC** for rød, grøn og blå.
9. Gentag for alle i gruppen.

**Varianter** (ét forsøg pr. variant, på samme person):

| Variant | Gør sådan | Hvad forventer I? |
|---|---|---|
| a. Tryk hårdt | Pres fingeren hårdt mod kameraet | Blodet presses ud, så AC-signalet bliver mindre |
| b. Kold finger | Fingeren i koldt vand i 1 min, tør, og optag | Sammentrukne blodkar giver et svagere signal |
| c. Bevægelse | Bevæg hånden lidt under optagelsen | Falske "slag", som værktøjet markerer som uregelmæssige |
| d. Efter aktivitet | Optag lige efter 1 min trappeløb | Højere puls, som mobilen også bør kunne se |

**Det skal I lægge mærke til (fysikken):**
- **DC for blå** er næsten 0, fordi blåt lys absorberes næsten fuldstændigt af blod og væv. **Rød** har høj DC, fordi rødt lys slipper bedst igennem. Det er derfor, fingeren lyser rødt.
- **Absorptionen afhænger af bølgelængden.** Det er hele grundideen bag pulsoximeteret: Det bruger to bølgelængder (660 og 940 nm), fordi Hb og HbO₂ absorberer dem forskelligt.
- **Mobilen kan ikke måle iltmætning**, fordi den mangler infrarødt lys og er ikke kalibreret. Det er en vigtig pointe om, hvorfor et rigtigt apparat har netop de to LED'er.

**Fejlkilder:** Kameraets automatiske justering af lys og farve, bevægelse, for hårdt tryk, og at videoen kan være komprimeret.

---

### Delforsøg 2 – Måledagbog med AI-blindtest (dag 1–5, ca. 5 min om dagen)

**Ideen:** Rigtig AI i et smartwatch kender **din** normal og **situationen** (sover du, eller løber du?). I samler jeres egne data i 5 dage og tester, om en model kan skelne mellem *normal variation* og *forkerte målinger*.

**Fremgangsmåde**

1. Hver person måler **puls og SpO₂ 4 gange om dagen** i 5 dage, altid siddende og med hånden i ro i 30 sekunder, før I aflæser:

| Situation | Hvornår |
|---|---|
| **Morgen – hvile** | Lige efter I er stået op, inden morgenmad |
| **Skole – siddende** | I en time, efter I har siddet i 10 min |
| **Efter aktivitet** | Lige efter idræt, cykling til skole eller 2 min trappeløb |
| **Aften – hvile** | Inden sengetid |

2. Skriv hver måling ind i fanen **Måledagbog**: person, dag, situation, puls og SpO₂.
3. **Blindtesten:** Hver person laver i løbet af ugen **2 bevidste fejlmålinger**, fx med neglelak, kold finger, en finger der bevæger sig, eller lommelygtelys på klemmen. Skriv dem ind som almindelige målinger. **En anden i gruppen** noterer i kolonnen **"Fejlmåling? (facit)"**, hvilke det var. Det er ligesom testbillederne i biologi: Modellen må ikke kende svaret.
4. Efter 5 dage har hver person ca. 20 målinger, og gruppen har ca. 80.

**Analyse (regnearket gør det automatisk)**

Regnearket kører **to AI-modeller** på jeres data og sammenligner dem med facit:

| | **Model A: Gruppemodel** | **Model B: Personlig model** |
|---|---|---|
| Hvad er "normalt"? | Hele gruppens gennemsnit og spredning | Personens **egne** målinger i **samme situation** |
| Afvigelse når | \|z\| > 2 for puls eller SpO₂ | \|z\| > 2 for puls eller SpO₂ |
| Ligner | Et simpelt apparat med fast alarmgrænse | Et smartwatch, der lærer dig at kende |

For hver model beregner regnearket **sensitivitet** (hvor mange af fejlmålingerne den fandt) og **specificitet** (hvor mange normale målinger den lod være). Det er præcis de samme mål som i jeres AI-forsøg med hudbilleder i biologi.

**Typiske resultater (så I ved, hvad I kan forvente)**

| | Morgen | Skole | Efter aktivitet | Aften |
|---|---|---|---|---|
| Puls | 55–75 | 65–85 | 100–150 | 60–80 |
| SpO₂ | 96–99 % | 96–99 % | 95–99 % | 96–99 % |

- **Gruppemodellen** giver typisk **falske alarmer** ved "efter aktivitet", fordi en høj puls ser unormal ud i forhold til gruppens gennemsnit. Den overser også fejlmålinger hos en person, der normalt har lav puls.
- **Den personlige model** finder typisk **flere** fejlmålinger og giver **færre** falske alarmer, fordi den kender personen og situationen.
- **SpO₂ ændrer sig næsten ikke** mellem situationerne. Derfor er selv et lille fald (fx 99 → 94 %) mistænkeligt, og det er netop derfor, iltmætning er et godt faresignal (se kemi).

### Sikkerhed

- Fysisk aktivitet kun så hårdt, som man selv har det godt med.
- Hold **aldrig** vejret for at få iltmætningen ned. Det er ikke en del af forsøget.
- Neglelakfjerner bruges i et udluftet lokale.

### Databehandling – det skal med i præsentationen

1. **Mobil-PPG:** Puls fra mobilen sammenlignet med pulsoximeteret (tabel), plus et skærmbillede af kurven fra analyseværktøjet.
2. **Søjlediagram:** gennemsnitlig puls og SpO₂ i hver situation (laves automatisk i regnearket).
3. **AI-sammenligning:** sensitivitet og specificitet for model A og model B.

### Konklusion (skabelon)

> "Med mobilkameraet kunne vi se pulsen som små udsving i lysstyrken: __ slag/min mod __ slag/min på pulsoximeteret. Blåt lys blev næsten helt absorberet (DC ≈ __), mens rødt lys slap bedst igennem. Det viser, at absorptionen afhænger af bølgelængden, og det er derfor, pulsoximeteret bruger rødt og infrarødt lys.
> I måledagbogen varierede pulsen fra ca. __ (morgen) til __ (efter aktivitet), mens SpO₂ lå stabilt mellem __ og __ %.
> Gruppemodellen fandt __ af __ fejlmålinger og gav __ falske alarmer. Den personlige model fandt __ af __ og gav __ falske alarmer. Det viser, at AI bliver bedre til at opdage afvigelser, når den kender personens egen normal og situationen. Det er præcis det, smartwatches og hospitalernes overvågningssystemer gør."

---

## Kilder (fysik)

- Fysik/kemi-bogen (kapitler om lys, bølger og energi)
- Sundhed.dk: *Iltmætning / pulsoximetri*
- Sjoding, M.W. m.fl. (2020): *Racial bias in pulse oximetry measurement*. New England Journal of Medicine 383.
- Perez, M.V. m.fl. (2019): *Large-scale assessment of a smartwatch to identify atrial fibrillation*. New England Journal of Medicine 381.
- Producentens brugsanvisning til jeres pulsoximeter (nøjagtighed og bølgelængder)
