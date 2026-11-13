# TRL 5 – Folyamatadat-réteg validációja releváns környezetben

**Állapot (2026-11-13):** mindhárom zárókapu teljesül, a jegyzőkönyv aláírva (végrehajtó, kezelő, minőségügyi szakértő). Hátra van: a TRL 5 leírás aláírása (projektvezető, rektor). Részletek: `Hegesztesi_DT_TRL5_Leiras.docx`.

**Hatókör:** a RobotComm–RobotVis folyamatadat-réteg (robotpozíció, áramforrás-adatok gyűjtése, kijelzése, naplózása a valós robotcellában). A képi és 3D réteg kapui (T5-03 … T5-07) és a jelanomália-detektor (T5-02) a TRL 6-ba kerültek; lásd [`SZINTZARASI_KRITERIUMOK.md`](SZINTZARASI_KRITERIUMOK.md).

## Kapuk és bizonyítékok

| Kapu | Állapot | Hol |
| --- | --- | --- |
| T5-01 eseményfelismerés (vak annotáció, 2 kör) | **teljesül (B)** – 2. kör (szakaszoló v2): 120/120; 1. kör (v1): 73,1%, ok: a TorchSignal késése | `robotvis_validacio/annotacio_T5-01/` |
| T5-08 streaming késleltetés | **teljesül (B)** – visszajátszás 3 futás (P95 ≤ 85 ms / ≤ 465 ms), 15 cellás videó (≤ kb. 0,88 s) | `robotvis_validacio/visszajatszas_2026-10-30/`, `robotvis_validacio/video_*_darab/`, `robotvis_validacio/T5-08_video_osszesites.md` |
| Kezelői próba | **teljesül, dokumentált korláttal** (2026-11-12; a minőségügyi szakértő elfogadta 2026-11-13) | `robotvis_validacio/kezeloi_proba_2026-11-12/` |
| Adatteljesség (korlát) | dokumentált; javítás előkészítve | `robotvis_validacio/naplo_folytonossag/`, `robotvis_validacio/ivjel_javitas_v1/` |

A lezárásig hátralévő lépések: [`NYITOTT_ADATIGENY.md`](NYITOTT_ADATIGENY.md). A záró kiértékelés egy paranccsal: `robotvis_validacio/eszkozok/06_trl5_zaras.py` (leírás: `robotvis_validacio/eszkozok/README.md`).

## Mappák

| Mappa | Tartalom |
| --- | --- |
| `robotvis_validacio/` | A TRL 5 tényleges bizonyítékai: eszközök, visszajátszásos mérés, 15 cellás videó kiértékelése, naplófolytonosság (151 futás), ívjel-javítás és forráskód-elemzés |
| `src/`, `outputs/`, `run_windows.bat`, `requirements.txt` | A 2026-10-15-i v2 előzetes validáció (valós adatleltár + szintetikus stressztesztek). **Előzmény**, nem zárókapu-bizonyíték; az `outputs/synthetic*` mappák D osztályú, szintetikus adatok |
| `documentation/` | Csomag-eredet (SHA-256) és GitHub-integrációs jegyzet |

### A v2 előzetes validáció futtatása (előzmény)

- Python 3.10+; `python -m pip install -r requirements.txt`
- `python src/run_real_validation.py --real-zip "C:\\adatok\\csv_light2.zip"` vagy `run_windows.bat "C:\\adatok\\csv_light2.zip"`
- tesztek: `python -m pytest src/test_validation.py -q`

A v2 eredményei (150 CSV, 20 JPG, 18 PLY beolvasva; szintetikus, valós bázisra injektált eltérések) a TRL 4 és a TRL 6 tervezéséhez adtak bemenetet. A `synthetic_real_anchored` állományok **nem valós hibás hegesztések**.

## Bizonyítékosztályok

A – publikált; B – a nyers adatból újraszámolt; C – másodlagos; D – szintetikus (csak módszer-bemutatás).
