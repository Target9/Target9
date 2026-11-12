# 8. Eksamensforberedelse – spørgsmål, svar og øveplan

Efter fremlæggelsen stiller lærer og censor spørgsmål, både i jeres eget fag og **på tværs af fagene**. Øv spørgsmålene i par: Én spørger, og én svarer uden at kigge.

## Øveplan

| Runde | Hvad | Hvordan |
|---|---|---|
| 1 | Læs manuskriptet højt for dig selv | Med papir. Tag tid. |
| 2 | Fortæl dit fag til en anden i gruppen | Kun med stikord |
| 3 | Generalprøve 1 med slides | Hele gruppen. Tag tid. Øv overgange. |
| 4 | Spørgsmålsrunde | Brug listen nedenfor. Byt fag! |
| 5 | Generalprøve 2 for en "censor" (forælder/ven) | Bed dem stille 3 spørgsmål bagefter |

---

## Biologi

**1. Hvad er forskellen på et proto-onkogen og et tumorsuppressorgen?**
Proto-onkogener stimulerer celledeling (speederen). Bliver de overaktive ved en mutation, kaldes de onkogener. Tumorsuppressorgener bremser celledelingen og kan sætte apoptose i gang (bremsen), fx p53. Ved kræft er speederen typisk i bund, og bremsen virker ikke.

**2. Hvad er apoptose, og hvorfor er det vigtigt?**
Programmeret celledød. Kroppen fjerner selv celler med alvorlige DNA-skader. Kræftceller kan undgå apoptose og overlever derfor trods skaderne.

**3. Hvad er metastaser?**
Kræftceller, der har spredt sig fra den oprindelige tumor via blod eller lymfe og danner nye svulster i andre organer.

**4. Hvorfor er melanom farligere end basalcellekarcinom?**
Melanom udgår fra melanocytterne og kan sprede sig tidligt. Basalcellekarcinom vokser langsomt og spreder sig næsten aldrig.

**5. Hvordan skader UV-lys DNA?**
UV-fotoner har høj energi og kan få to nabo-thyminbaser til at binde sammen (thymin-dimerer). Repareres det ikke, kan det blive til en mutation.

**6. Hvad er sensitivitet og specificitet?**
Sensitivitet er andelen af syge, testen finder (SP/(SP+FN)). Specificitet er andelen af raske, testen frikender (SN/(SN+FP)).

**7. Hvad er værst: en falsk positiv eller en falsk negativ?**
Ved kræft er falsk negativ værst, fordi patienten bliver sendt hjem med kræft. Derfor prioriterer man høj sensitivitet og accepterer flere falske alarmer.

**8. Kan AI'en se kræftcellerne?**
Nej. Vores AI ser billeder af hudens overflade og reagerer på træk som asymmetri og farver, der skyldes forandringerne i cellerne. Diagnosen stilles ved biopsi og mikroskopi. Der findes dog også AI, der analyserer mikroskopibilleder.

**9. Hvorfor tog jeres model fejl?**
Få træningsbilleder (160 mod 100.000+), billeder med hår/lineal/pen, kun to klasser, og næsten kun lys hud. Modellen kan lære forkerte genveje.

**10. Hvordan kunne I forbedre forsøget?**
Flere og mere varierede billeder, flere hudtyper, flere klasser, gentage træningen 3 gange og tage gennemsnit, og sammenligne med en hudlæges vurdering.

## Fysik

**1. Hvorfor bruger pulsoximeteret to bølgelængder?**
Fordi Hb og HbO₂ absorberer rødt og infrarødt lys forskelligt. Forholdet mellem de to signaler fortæller, hvor stor en andel der er iltet.

**2. Hvad er forskellen på AC- og DC-signalet?**
DC er den konstante absorption i væv, knogle og veneblod. AC er den lille pulserende del, der skyldes, at arterierne udvider sig ved hvert hjerteslag. Apparatet bruger AC-delen, så det måler arterieblodet.

**3. Hvordan regner man pulsen ud fra signalet?**
Puls = 60 / T, hvor T er tiden mellem to toppe i sekunder. Ved T = 0,8 s er pulsen 75 slag/min.

**4. Regn fotonenergien ud for 940 nm.**
E = hc/λ = (6,63·10⁻³⁴ · 3,00·10⁸) / (940·10⁻⁹) ≈ 2,1·10⁻¹⁹ J.

**5. Hvorfor giver neglelak og kolde fingre fejlmålinger?**
Neglelakken absorberer lyset, så der kommer for lidt lys til sensoren. Ved kolde fingre trækker blodkarrene sig sammen, og så bliver det pulserende signal for svagt.

**6. Hvad er forskellen på transmission og refleksion i måling?**
Fingerclipsen måler det lys, der går igennem fingeren (transmission). Et smartwatch måler det lys, der kastes tilbage fra huden (refleksion), fordi LED og sensor sidder på samme side.

**7. Hvordan virker jeres afvigelsesmodel?**
Vi beregner middelværdi og standardafvigelse og markerer en måling, hvis |z| > 2, altså hvis den ligger mere end 2 standardafvigelser fra middel (ca. 95 % af normale målinger ligger indenfor). Model A sammenligner med hele gruppens målinger. Model B sammenligner kun med personens egne målinger i samme situation, men uden selve målingen.

**8. Hvorfor er det svært for en AI at vide, om en høj puls er farlig?**
Den mangler kontekst. Høj puls er normal ved løb, men unormal i søvn. Derfor kombinerer smartwatches pulsen med bevægelsessensoren og lærer personens egen normal.

**9. Hvorfor kan pulsoximetre være upræcise på mørk hud?**
Melanin absorberer også lys, og apparaterne er især kalibreret på personer med lys hud. Studier viser, at skjult iltmangel overses oftere.

**10. Hvordan kunne mobilkameraet måle pulsen?**
Lommelygten sender lys ind i fingeren, og kameraet måler, hvor meget der slipper igennem. Ved hvert hjerteslag kommer der mere blod i fingeren, som absorberer mere lys, så billedet bliver en anelse mørkere. Tiden mellem de mørke "dyk" giver pulsen (puls = 60/T).

**11. Hvorfor var blåt lys næsten 0, mens rødt var højt?**
Blod og væv absorberer blåt og grønt lys meget kraftigt, mens rødt lys trænger bedre igennem. Absorptionen afhænger af bølgelængden, og det er derfor, pulsoximeteret bruger to bestemte bølgelængder.

**12. Hvorfor kan mobilen ikke måle iltmætning?**
Den har ikke infrarødt lys, og den er ikke kalibreret. Iltmætning kræver, at man sammenligner absorptionen ved to bølgelængder, hvor Hb og HbO₂ opfører sig forskelligt.

**13. Hvorfor fandt den personlige model flere fejlmålinger end gruppemodellen?**
Gruppemodellen sammenligner med alles gennemsnit, så en høj puls efter aktivitet ligner en afvigelse (falsk alarm), mens en fejlmåling hos en person med lav puls kan gemme sig. Den personlige model sammenligner med personens egne målinger i samme situation, altså med kontekst, ligesom et smartwatch.

**14. Hvorfor lavede I en blindtest?**
Så modellen (og vi) ikke kendte svaret på forhånd. Det svarer til testbillederne i biologi: Man kan kun måle, hvor god en model er, på data, den ikke har "set" facit for.

## Kemi

**1. Hvor binder ilten på hæmoglobin?**
På jern-ionen (Fe²⁺) i midten af hæmgruppen. Der er 4 hæmgrupper, altså op til 4 O₂ pr. hæmoglobin.

**2. Skriv reaktionen og forklar ligevægten.**
Hb + 4 O₂ ⇌ Hb(O₂)₄. Højt O₂ i lungerne forskyder mod højre (binding), og lavt O₂ i musklerne mod venstre (afgivelse). Det er Le Chateliers princip.

**3. Hvorfor er bindingskurven S-formet?**
Kooperativ binding: Når én O₂ binder, ændrer molekylet form, så de næste binder lettere.

**4. Hvad er Bohr-effekten?**
Mere CO₂, flere H⁺ (lavere pH) og højere temperatur får hæmoglobin til at afgive ilt lettere. Kurven forskydes mod højre. Det sker i arbejdende muskler.

**5. Hvorfor var jeres iltmætning stabil i alle situationer i måledagbogen?**
Pulsoximeteret måler arterieblodet, der lige er blevet iltet i lungerne. Hurtigere vejrtrækning og den flade top af bindingskurven sikrer næsten fuld mætning. Iltforbruget ses i veneblodet.

**6. Hvad viste den blå flaske, og hvorfor er den en model?**
Glukose gør methylenblåt farveløst, og ilt fra luften (rystning) gør det blåt igen. Rystning svarer til lungerne, og glukosens iltforbrug svarer til respirationen. Ved højere temperatur blev ilten brugt hurtigere, og vi skulle ryste oftere for at holde den blå, ligesom man trækker vejret hurtigere under arbejde. Begrænsning: Methylenblåt reagerer kemisk med ilten (oxideres), mens hæmoglobin binder den løst og har en S-formet kurve.

**7. Hvorfor går reaktionen i den blå flaske hurtigere, når det er varmt?**
Molekylerne bevæger sig hurtigere og støder oftere og hårdere sammen, så flere stød fører til reaktion.

**8. Hvorfor er kulilte farligt, og hvorfor opdager pulsoximeteret det ikke?**
CO binder ca. 200–250 gange stærkere til jernet end O₂ og blokerer pladserne. HbCO er lyserødt ligesom HbO₂, så apparatet viser en falsk høj iltmætning.

**9. Skriv respirationsligningen.**
C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + energi

## Geografi

**1. Hvorfor har Australien og Danmark meget hudkræft?**
Mange med lys hud (lidt melanin). I Australien er UV-strålingen høj. I Danmark tager mange på solferier og har tidligere brugt solarier meget.

**2. Hvad er AI-paradokset?**
De lande, der har størst behov for AI (få læger), har ofte dårligst adgang til den (økonomi, infrastruktur, data).

**3. Hvorfor får USA ikke fuldt point, selvom det er rigt?**
Ulige adgang til sundhed: Mange har ingen eller dårlig sundhedsforsikring, og AI-modellerne virker dårligere på sorte og latinamerikanske patienter (bias).

**4. Hvad er styrker og svagheder ved jeres model?**
Styrker: overskuelig, sammenlignelig, viser hvorfor et land scorer lavt. Svagheder: subjektive point, lige vægtning af faktorer, ingen forskel mellem by og land.

**5. Hvordan hænger DTM sammen med kræft?**
I de sene faser er befolkningen ældre, og kræft stiger med alderen. Lande på vej gennem DTM'en vil få flere kræfttilfælde og et større behov for diagnostik.

**6. Hvordan kan man gøre AI mere retfærdig globalt?**
Træne på billeder af alle hudtyper, afprøve lokalt, billig AI på smartphones, og samtidig uddanne sundhedspersonale og sikre adgang til behandling.

## Spørgsmål på tværs (dem bliver alle spurgt om!)

**Hvad har jeres fire fag med hinanden at gøre?**
Alle handler om at opdage afvigelser i kroppen med data. Biologien forklarer sygdommen, fysikken hvordan vi måler med lys, kemien hvorfor målingerne ser ud, som de gør, og geografien hvem der får gavn af det.

**Hvad har lys med både hudkræft og pulsoximetre at gøre?**
UV-lys skader DNA og giver hudkræft. AI'en analyserer billeder, altså reflekteret lys fra huden. Pulsoximeteret sender rødt og IR-lys gennem fingeren. Melanin absorberer lys, og det giver både beskyttelse mod UV og målefejl i pulsoximetre og bias i AI. Det er det, der binder det hele sammen.

**Ville I stole på en AI-diagnose?**
Som hjælp, ja, men ikke alene. Den skal bruges sammen med en læge, fordi den kan lave fejl, især på billeder, der ligner noget, den ikke er trænet på.

**Hvem har ansvaret, hvis AI'en tager fejl?**
Det er et etisk dilemma. I dag har lægen ansvaret, og AI er et hjælpemiddel. EU's AI-forordning stiller krav til højrisiko-AI som medicinsk AI.

**Hvad er en model, og hvad er begrænsningen ved jeres modeller?**
En model er en forenklet gengivelse af virkeligheden, der hjælper med at forklare eller forudsige. Alle vores modeller forenkler: bilmodellen (kun én speeder/bremse), Hill-kurven (gennemsnitsværdier), afvigelsesmodellen (ingen kontekst) og AI-parathedsmodellen (subjektive point).

**Hvad ville I undersøge, hvis I havde mere tid?**
Teste AI'en på flere hudtyper, måle med et medicinsk pulsoximeter, sammenligne mobil-pulsmåleren med et smartwatch, føre måledagbog i længere tid og med flere personer, og måle den blå flaskes farve med en lysmåler i stedet for med øjet.
