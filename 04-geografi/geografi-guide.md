# 4. Geografi – Hvem får gavn af AI i sundhedsvæsenet?

> **Underspørgsmål:** Hvilke faktorer afgør, om et lands befolkning får gavn af AI i sundhedsvæsenet, og hvad betyder det for kræftdiagnosticering?
> **Kobling:** Model (AI-parathedsmodel + behov/adgang-diagram + den demografiske transitionsmodel) og perspektivering.

---

## Del A – Teori

### A1. Hvor i verden er der mest hudkræft? (behovet)

Hudkræft (især modermærkekræft) afhænger af tre ting:

1. **UV-stråling.** Den er stærkest nær **ækvator** og i **højder**, og hvor ozonlaget er tyndt (fx over Australien og New Zealand).
2. **Hudtype.** Lys hud har lidt **melanin** og derfor lidt beskyttelse (se biologi). Hudtyper beskrives med **Fitzpatrick-skalaen** fra I (meget lys) til VI (meget mørk).
3. **Livsstil og kultur.** Solferier, solarium og et udendørsliv. Danskere rejser fx meget sydpå på ferie.

Derfor har **Australien og New Zealand** verdens højeste forekomst af modermærkekræft: mange lyshudede indbyggere (efterkommere af europæiske indvandrere) bor med høj UV-stråling. **Danmark** ligger også meget højt, selvom solen er svagere, fordi befolkningen har lys hud og tager på solferier. I **Afrika og Asien** er modermærkekræft sjælden. Når det opstår hos mørkhudede, sidder det tit på **håndflader, fodsåler eller under neglene** og bliver ofte opdaget sent. Reggaemusikeren Bob Marley døde af netop denne type, som startede under en tånegl.

### A2. Faktorer, der afgør, om befolkningen får gavn af AI

| Faktor | Hvorfor betyder den noget? | Eksempel |
|---|---|---|
| **1. Økonomi** (BNP pr. indbygger, sundhedsudgifter) | AI-systemer, computere, kameraer og licenser koster penge | Rige lande kan købe og afprøve AI først |
| **2. Infrastruktur** (strøm, internet, mobiltelefoner) | AI kræver stabil strøm, internet og ofte en smartphone | Landområder i Afrika syd for Sahara har ofte ustabil strøm og dårligt internet |
| **3. Sundhedsvæsenet** (antal læger, afstand til hospital, offentligt/privat) | AI skal bruges *af* nogen. Hvis AI siger "mistanke om kræft", skal der være en læge, en biopsi og behandling bagefter | I Danmark er der gratis adgang til læge. I lande uden offentligt sundhedsvæsen afhænger det af, om man har råd. |
| **4. Uddannelse og digitale kompetencer** | Personale og patienter skal kunne bruge og stole på teknologien | Læse- og it-færdigheder |
| **5. Data og repræsentation** (bias) | AI er trænet på billeder, som især stammer fra Europa, USA og Australien med **lys hud**. Den virker dårligere på mørk hud. | Daneshjou m.fl. 2022: dårligere præcision på mørk hud |
| **6. Lovgivning, etik og tillid** | Regler om persondata og godkendelse af medicinsk udstyr | EU's AI-forordning (AI Act) klassificerer medicinsk AI som **højrisiko**. Det giver sikkerhed, men også langsommere indførelse. |
| **7. Befolkningens sammensætning** | Gamle befolkninger får mere kræft. Hudtype og UV påvirker behovet. | Danmark har en aldrende befolkning, Nigeria en meget ung |
| **8. By og land** | Specialister bor i byerne, og AI og telemedicin kan nå ud på landet | Indien: få hudlæger i landområderne, men mange har en smartphone |

### A3. "AI-paradokset"

> **De lande, der har *mest brug* for AI (få læger, lange afstande), har ofte *dårligst adgang* til den (dårligt internet, få penge, ingen data om egen befolkning). Og de lande, der har *bedst adgang* (Danmark, Australien), har allerede mange læger.**

AI kan altså enten **mindske** eller **øge** uligheden i sundhed. Det afhænger af, hvordan den bliver udviklet og indført. Det svarer til ideen i **center–periferi-modellen**: Teknologien udvikles i centrum (rige lande), og periferien får den senere eller i en form, der ikke passer til befolkningen.

### A4. Hvad betyder det for kræftdiagnosticering?

| I rige lande (fx Danmark) | I fattigere lande (fx Nigeria, landområder i Indien) |
|---|---|
| AI kan **sortere** (triage), så hudlæger bruger tid på de alvorlige tilfælde, og ventetiderne bliver kortere | AI på en smartphone kan bruges af en sygeplejerske i en landsby, **hvor der ingen hudlæge er** |
| **Teledermatologi:** Egen læge tager billeder og sender dem til en hudlæge, og AI kan hjælpe med vurderingen | Men: Hvis AI'en er trænet på lys hud, kan den **overse** kræft på mørk hud |
| Risiko for **overdiagnosticering**: flere falske alarmer, flere unødige biopsier og mere bekymring | Hvis der findes kræft, skal der også være **kirurg, patolog og behandling**, ellers hjælper diagnosen ikke |
| Data findes allerede (journaler, billeder), og der er stærk databeskyttelse (GDPR) | Der mangler lokale data og lokale forskere til at træne modellen på befolkningen |
| | Andre kræftformer er større problemer (fx livmoderhals- og brystkræft), og her afprøves AI også til screening |

**Pointe:** AI er ikke en løsning i sig selv. Den virker kun, hvis den er **en del af et sundhedssystem**: data, personale, økonomi og behandling.

---

## Del B – Landedata (sammenligning af 5 lande)

> Tallene nedenfor er **afrundede ca.-tal** (ca. 2021–2023) til at komme i gang. **Tjek og opdater dem selv** på kilderne nedenfor, og skriv årstal på, når I bruger dem. Det giver point for kildekritik.

| Land | BNP pr. indb. (USD) | Internetbrugere (%) | Læger pr. 1.000 indb. | Middellevetid (år) | Medianalder (år) | Modermærkekræft (nye tilfælde pr. 100.000, aldersstandardiseret) |
|---|---|---|---|---|---|---|
| **Danmark** | ca. 68.000 | ca. 98 | ca. 4,2 | ca. 81 | ca. 42 | ca. 25–30 (meget højt) |
| **Australien** | ca. 65.000 | ca. 96 | ca. 4,0 | ca. 83 | ca. 38 | ca. 35–40 (verdens højeste) |
| **USA** | ca. 80.000 | ca. 92 | ca. 2,7 | ca. 77 | ca. 38 | ca. 15–20 (højt) |
| **Indien** | ca. 2.500 | ca. 45–55 | ca. 0,7 | ca. 70 | ca. 28 | under 1 (meget lavt) |
| **Nigeria** | ca. 1.000–2.000 | ca. 35–55 | ca. 0,4 | ca. 54 | ca. 18 | under 1 (meget lavt) |

**Kilder til at slå op:**
- [Gapminder](https://www.gapminder.org/tools) – BNP, middellevetid, læger (lav også en boblegraf!)
- [Verdensbanken – data.worldbank.org](https://data.worldbank.org) – internetbrugere, læger pr. 1.000, sundhedsudgifter
- [WHO Global Cancer Observatory (GLOBOCAN) – gco.iarc.fr](https://gco.iarc.fr) – kræftforekomst pr. land (vælg "Melanoma of skin")
- [Our World in Data](https://ourworldindata.org) – grafer om sundhed og teknologi
- Danmarks Statistik / Sundhedsdatastyrelsen – danske tal

---

## Del C – Modeller

### Model 1: AI-parathedsmodellen (jeres egen model, og den vigtigste)

Giv hvert land **1–5 point** for hver faktor (5 = rigtig godt). Fanen **"Geografi-model"** i regnearket lægger automatisk sammen og laver et søjlediagram.

| Faktor | Danmark | Australien | USA | Indien | Nigeria |
|---|---|---|---|---|---|
| Økonomi | 5 | 5 | 5 | 2 | 1 |
| Infrastruktur (strøm/internet) | 5 | 5 | 4 | 3 | 2 |
| Sundhedspersonale | 5 | 5 | 4 | 2 | 1 |
| Lige adgang til sundhed | 5 | 4 | 2 | 2 | 1 |
| Data der passer til befolkningen (hudtype) | 5 | 5 | 3 | 2 | 1 |
| Lovgivning og tillid | 5 | 4 | 4 | 3 | 2 |
| **AI-parathed i alt (ud af 30)** | **30** | **28** | **22** | **14** | **8** |

> Pointene er **jeres egen vurdering**. Begrund mindst ét point pr. land i præsentationen. USA får fx kun 2 for "lige adgang", fordi mange ikke har en sundhedsforsikring.

**Styrker ved modellen:** Den gør mange faktorer overskuelige og sammenlignelige, og man kan se *hvorfor* et land scorer lavt.
**Begrænsninger:** Pointene er subjektive. Alle faktorer vægter lige meget, selvom de måske ikke burde. Et land er ikke ens overalt: Der er stor forskel på by og land i både Indien og USA.

### Model 2: Behov og adgang (2×2-diagram)

Tegn et koordinatsystem på planchen:
- **x-akse:** Adgang til AI (AI-parathed fra model 1)
- **y-akse:** Behov for hjælp til hudkræftdiagnose (forekomst af hudkræft *og* mangel på hudlæger)

```
 Behov ↑
  højt |  [Mangel på læger]          [Australien]
       |  Indien (landområder)       Danmark
       |  "AI kunne hjælpe mest,      "Har råd og høj forekomst"
       |   men adgangen er lav"
       |-----------------------------------------------
       |  Nigeria                     USA (ulige adgang)
  lavt |  "Hudkræft sjælden, men
       |   AI til andre kræftformer"
       +----------------------------------------------→ Adgang til AI
          lav                                    høj
```

Øverst til venstre er der, hvor AI kunne gøre **mest gavn**, men hvor den kommer **sidst**. Det er AI-paradokset.

### Model 3: Den demografiske transitionsmodel (DTM) – kobling til kræft

| Fase | Kendetegn | Land (eksempel) | Betydning for kræft og AI |
|---|---|---|---|
| 2–3 | Mange fødsler, faldende dødelighed, **ung befolkning** | Nigeria | Færre kræfttilfælde pr. indbygger. Infektionssygdomme fylder mest. |
| 3 | Faldende fødselstal | Indien | Kræft bliver et voksende problem, efterhånden som folk lever længere |
| 4–5 | Få fødsler, lang levetid, **aldrende befolkning** | Danmark, Australien | Flere kræfttilfælde (kræft stiger med alderen), og der er brug for effektiv diagnose. AI kan aflaste. |

**Pointe:** Efterhånden som lande bevæger sig gennem DTM'en, stiger antallet af kræfttilfælde, og dermed også behovet for AI i kræftdiagnosticering.

---

## Del D – Perspektivering (vælg 2–3 til præsentationen)

1. **Bias og retfærdighed.** Hvis AI kun trænes på lys hud, forstærker den uligheden. Løsning: datasæt med alle hudtyper (fx *Diverse Dermatology Images*) og lokal afprøvning. Den samme bias findes i pulsoximetre (se fysik).
2. **Smartphones som springbræt.** Mange lande sprang fastnettelefoner over og gik direkte til mobiltelefoner. På samme måde kan AI på mobilen måske springe manglen på hudlæger over, hvis den virker for befolkningen.
3. **Danmark.** Gratis sundhedsvæsen, digital infrastruktur (MitID, sundhed.dk) og mange sundhedsdata gør Danmark velegnet til at indføre AI. Men: Hvem har ansvaret, hvis AI'en tager fejl? Lægen, firmaet eller regionen?
4. **Forebyggelse er stadig billigst.** Solcreme, skygge, tøj og ingen solarier. AI finder kræften, men forebyggelse undgår den.
5. **Klima og ozonlag.** Ozonlaget er ved at hele (Montreal-protokollen fra 1987 forbød de stoffer, der nedbrød det), men mere solskin og varme somre kan ændre vores solvaner.
6. **Etik.** Er det okay, at private firmaer ejer AI'en, der er trænet på patienters billeder? Skal patienten give samtykke?

### Konklusion (skabelon)

> "Om et lands befolkning får gavn af AI i sundhedsvæsenet, afhænger især af økonomi, infrastruktur, antallet af sundhedspersonale, lige adgang og om AI'en er trænet på data, der passer til befolkningen. Vores AI-parathedsmodel viser, at Danmark og Australien scorer højest, mens Nigeria og Indien scorer lavest, selvom manglen på læger dér gør, at AI potentielt kunne hjælpe mest. For kræftdiagnosticering betyder det, at AI kan forkorte ventetider og opdage kræft tidligere i rige lande, men at den risikerer at øge uligheden globalt, hvis den ikke udvikles til alle hudtyper og indføres sammen med behandlingsmuligheder."

---

## Kilder (geografi)

- Geografibogen (befolkningsgeografi, den demografiske transitionsmodel, center–periferi)
- Gapminder, Verdensbanken, WHO/GLOBOCAN, Our World in Data (links ovenfor)
- Daneshjou, R. m.fl. (2022): *Disparities in dermatology AI performance on a diverse, curated clinical image set*. Science Advances 8.
- Adamson, A.S. & Smith, A. (2018): *Machine learning and health care disparities in dermatology*. JAMA Dermatology 154.
- WHO (2021): *Ethics and governance of artificial intelligence for health*.
- EU's AI-forordning (AI Act), 2024 – digst.dk / europa.eu
