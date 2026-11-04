# TRL 5 – RobotVis (folyamatadat-réteg) validációs eszközök

Ez a mappa a TRL 5 hatókör-javaslat (folyamatadat-réteg: RobotComm, RobotVis) két mérési kapujához tartozó eszközöket tartalmazza:

| Kapu | Mit mér | Eszközök |
|---|---|---|
| T5-01 | A hegesztési szakaszok (TorchSignal 0→1 és 1→0) automatikus felismerése a vak kézi annotációhoz képest | `01_annotacios_lap_keszito.py`, `02_annotacio_kiertekelo.py` |
| T5-08 | A RobotVis megjelenítési késleltetése (P50, P95), adatvesztés, kijelzési megállás | `robotvis_latency_logger.py`, `03_keses_kiertekelo.py` |

**Állapot.** Az eszközök működésüket tekintve ki lettek próbálva a valós CSV-szerkezeten, szimulált annotáción és szintetikus késleltetés-naplón. Ez nem mérési eredmény: a kapuk teljesüléséhez a vak annotáció és a robotcellás mérés szükséges, és a kapuk számszerű értékei jóváhagyandók (TRL5/SZINTZARASI_KRITERIUMOK.md).

Követelmények: Python 3, `numpy`, `pandas`, `matplotlib`. A szkriptek `python3 -I` móddal futtathatók.

## T5-01: hegesztési szakaszok felismerése

1. Annotációs lap készítése (csoportonként 4 CSV, a g02_s33 mindig bekerül; `--seed` rögzíti a mintavételt):

   ```
   python3 -I 01_annotacios_lap_keszito.py --dataset <repo>/datasets/welding_experiments_v1 --out T5-01_annotacio --per-group 4 --seed 1
   ```

   Kimenet: `annotacio_sablon.csv` (üres lap), `abrak/*.png` (feszültség, áram, huzalsebesség, a szerszám soronkénti lépésköze; a TorchSignal nélkül), `automata_kulcs.csv` (az automatikus határok; az annotátornak nem adható oda), `ANNOTACIO_UTMUTATO.md`.
2. Az annotátor (aki a TorchSignal oszlopot és a kulcsot nem látta) a sablonba beírja minden varrat `kezdet_sor` és `veg_sor` értékét, valamint a nevét és a dátumot. Ha egy esemény nem egyértelmű, üresen hagyja, és a megjegyzésben indokolja.
3. Kiértékelés:

   ```
   python3 -I 02_annotacio_kiertekelo.py --kulcs T5-01_annotacio/automata_kulcs.csv --kitoltott annotacio_sablon_kitoltve.csv --out T5-01_eredmeny --tol-sor 1 --kapu 0.99
   ```

   Kimenet: `T5-01_eredmeny.csv` (eseményenként), `T5-01_riport.md` (egyezési arány, Wilson 95%-os konfidenciaintervallum, kivételek, a kapuhoz mért állapot).

Megjegyzés: kb. 120 eseménynél hibátlan egyezés esetén is csak kb. 96,9% a Wilson-alsó határ; a kapu megfogalmazását (pontbecslés vagy alsó határ) és a mintaméretet a projektvezetés rögzítse.

## T5-08: késleltetés és adatvesztés

1. A RobotVis Python-oldalán a hívási pontokat a szerző illeszti be (három külön `run_id`-vel, három ismételt futásra):

   ```python
   from robotvis_latency_logger import LatencyLog
   log = LatencyLog("robotvis_latency.csv", run_id="futas1")
   # az adatcsomag megérkezésekor / feldolgozásának elején:   log.on_receive(seq)
   # a kirajzolás (kijelző-frissítés) után:                  log.on_display(seq)
   # a futás végén:                                          log.close()
   ```

   Mindkét időbélyeg ugyanazon a monotonikus órán készül (`time.perf_counter`). A `seq` a csomag futáson belüli sorszáma. A kirajzolatlan csomag nem kerül a naplóba; a hiányzó sorszámokat a kiértékelő veszteségként számolja.
2. Kiértékelés:

   ```
   python3 -I 03_keses_kiertekelo.py --log robotvis_latency.csv --out T5-08_eredmeny --cel-ms 2000 --min-futas 3 --megallas-ms 2000
   ```

   Kimenet: `T5-08_futasok.csv` (futásonként P50, P95, P99, maximum, elveszett csomag, megállás, negatív késleltetés), `T5-08_riport.md`.
3. A napló csak a számítógépen belüli (megérkezéstől a kirajzolásig tartó) késleltetést méri. A robotvezérlő és az áramforrás oldali késleltetést külön kell mérni (például a képernyő és a robot egyidejű videófelvételével), és a jegyzőkönyvben feltüntetni.

## Kezelői jegyzőkönyv

A kezelői próbához és a két kapu eredményének rögzítéséhez a `TRL5_RobotVis_kezeloi_jegyzokonyv_sablon.docx` üres sablon szolgál (aláírás: végrehajtó, kezelő, minőségügyi szakértő).

## A TRL 5 záró kiértékelése (`06_trl5_zaras.py`)

A jóváhagyási lap aláírása, a vak annotáció és a kezelői próba után egy paranccsal kapunkénti döntést ad a T5-01, a T5-08 és a kezelői próba kapujára.

1. A kezelő a próba végén kitölti a `kezeloi_ellenorzolista_sablon.csv` másolatát. Az 1–4. és a 8. pontra `igen` vagy `nem` a válasz, az 5–6. pontra `igen`, `nem` vagy `nem tesztelt`, a 7. pontra 1–5. A kitöltött lapot a végrehajtó menti el.
2. A kezelői próba visszajátszott futásait a `05_visszajatszas_kiertekelo.py` értékeli ki (lásd a forgatókönyvet).
3. Záró kiértékelés. A `--t501-feltetel` értéke `pont` vagy `wilson`, a jóváhagyási lapon választott feltétel szerint:

   ```
   python3 -I 06_trl5_zaras.py --t501-kulcs automata_kulcs.csv --t501-kitoltott annotacio_kitoltott.csv --t501-feltetel pont --t508-futasok ../visszajatszas_2026-10-30/T5-08_visszajatszas_futasok.csv T5-08_kezeloi_proba/T5-08_visszajatszas_futasok.csv --t508-video ../T5-08_video_osszesites.md --kezeloi-lista kezeloi_ellenorzolista_kitoltott.csv --out TRL5_zaras
   ```

   Kimenet: `TRL5_ZARO_RIPORT.md` és `trl5_zaras.json`, amelyek a kapunkénti döntést, a kivételeket és a bemenetek SHA-256-ját tartalmazzák. A kilépési kód 0, ha mindhárom kapu teljesül.

A g02_s33 napló alapértelmezésként tájékoztató jelleggel, a kapun kívül szerepel (`--t501-tajekoztato`, a 02-esnél `--tajekoztato`): egy ismert, 2,5 s-os naplókiesés miatt az automata ott az 1. és 2. varratot egy szakasznak látja, így a sorszám szerinti párosítás nem értelmezhető. A kiértékelőt szimulált bemenettel (`--szimulalt`) próbáltuk ki: valószerű kitöltéssel (a g02_s33-ban 3 varrat, máshol 1 eltérés) 119/120 = 99,2% (Wilson 0,954–0,999), ugyanazt adja, mint a `02_annotacio_kiertekelo.py`; a g02_s33 nélküli kezelés előtt ugyanez 120/126 = 95,2% lett volna. Ha a kezelői ellenőrzőlista 3. pontja „nem”, a kiértékelő a kezelői próbát „nem teljesül” eredménnyel zárja. A próbafuttatás nem mérési eredmény.
