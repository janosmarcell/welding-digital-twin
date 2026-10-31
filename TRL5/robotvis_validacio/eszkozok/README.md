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
