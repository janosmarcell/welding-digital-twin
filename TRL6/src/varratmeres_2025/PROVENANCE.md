# Provenance: 2D varratmérés és hibacsoportok (2025)

**Állapot:** a projektcsapat közös munkája a 2023-as kísérletsorozat képein, a varratél-detektálás témájában. Feltáró és fejlesztési anyag, **nem validált mérés**. A fájlok byte-ra azonosak a kapott állományokkal (érkezett 2026-11-21), kivéve a `hibacsoportok_2025-06.csv`-t, amely egy belső dokumentumból készült kivonat (lásd lent).

| Forrás | SHA-256 |
|---|---|
| `weld-seam-analysis_1.zip` | `4b00d8fc0c6b634ed29a7b8d4a00370586da8c1c6cf74b5cea4dbfc3d8987b5d` |
| `linreq_excel.zip` | `edadc75bc2fb160e5112713c7b07c3fd4722ca02c4a51c1885781d705307e9de` |
| `hibacsoport_1.docx` (nem közölt; a kivonat forrása) | `c4f819b9048f33da8165d6b20fc8a07894d7bca1ca2f7593769374b913593e10` |

## weld-seam-analysis/ (2025. március–április)

Asztali alkalmazás (Python, PyQt5, OpenCV). A lánc: szürkeárnyalat → CLAHE → Gauss-elmosás → Canny adaptív küszöbbel (a medián ± 33%) → élek tágítása → kontúrok terület szerinti szűrése, egyesítése, morfológiai zárás → a legnagyobb kontúr. A varrat befoglaló mérete mellett a varrat középső 80%-án 100 oszlopban méri a varrat szélességét, a kiugró értékeket mediánnal (±2,5 MAD) szűri, és átlagol. Az alkalmazás a kép mappájában lévő `archive_info.json`-ből a hegesztési paramétereket is kiírja.

**Korlát:** az eredmény pixelben van; a mm-re váltás fix szorzó (`× 16,67 / 2000`, azaz kb. 120 px/mm), kalibráció és referencia nélkül. A `__pycache__` mappát nem vettük át.

## linreq/ (2025. április)

- `json_data_export.xlsx`: 429 varrat (ID, áram, feszültség, sebesség, mappa); **60 varratnál** (58 darab, mind az 5 sebesség) van mért „Height” érték mm-ben, a fenti fix szorzóval.
- `lin_req.ipynb`: lineáris regresszió a 60 mért értékre: Height ≈ −4,778 + 0,00777·I + 0,6715·U − 0,0520·v (I: A, U: V, v: cm/perc); R² = 0,73 egy 12 pontos teszthalmazon (80/20-as felosztás, random_state = 42).

**Fontos:**
- A „Height” a felülnézeti képen a varrat hossztengelyére merőleges méret, vagyis **varratszélesség**, nem a varratmagasság (dudor).
- A notebook a hiányzó 369 varratra **modellből becsült** értékeket is kiszámol (`complete_data_with_predictions.xlsx`, a tárolóban nincs meg). Ezek nem mérések, valós adatként nem használhatók.
- Az eredeti fájlnév `lin_req.IPYNB`, itt kisbetűs kiterjesztéssel. A notebook egy másik gépen futott (a mentési útvonalban egy helyi felhasználónév látszik); a fájl változatlan.

## hibacsoportok_2025-06.csv (2025. június)

Egy belső dokumentum kivonata, név és képernyőképek nélkül: 22 varratkép öt hibacsoportba sorolva, a csoport okával és javaslatával (a dokumentumban még egy kép szerepel felirat nélkül). Az áram, a feszültség és a sebesség a kísérleti tervből (`datasets/kiserleti_terv_2023/`) van hozzárendelve. A 202-es darab az előkísérletek közül, az 500-as tesztkép.

| Csoport | Javaslat |
|---|---|
| 1. a kép lelóg | nagy paramétereknél a laposvasra nem fér ki 3 varrat – újratervezés |
| 2. nem egységes textúra | egyenletes megvilágítás fotózás előtt |
| 3. dudorok + kontraszthiba | csak a varrat közepét vizsgálni |
| 4. nem folytonos varrat | túl nagy sebesség – a sebesség újratervezése |
| 5. egyéb | több hiba egyszerre; a 4_2 javíthatatlan selejt |

Ez szemrevételezéses csoportosítás, **nem független szakértői minősítés**. A TRL 6 fotózási szabályaihoz (megvilágítás, látómező, a varrat középső szakasza) és a zavart darabok tervezéséhez ad bemenetet.

## Szerepe a TRL-ben

2024: feltáró éldetektálás (`../eldetektalas_2024/`) → **2025: 2D mérőalkalmazás és az első paraméter–geometria modell (ez a mappa)** → TRL 6: a G6-04 2D-oldala dokumentált mm-skálával, a vágási felülethez mérve.

## Fájlok

| Fájl | Módosítva (a forrásban tárolt idő) | Bájt | SHA-256 |
|---|---|---:|---|
| `weld-seam-analysis/README.md` | 2025-03-20 12:51 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weld-seam-analysis/requirements.txt` | 2025-03-20 13:43 | 46 | `928dcd20c64f9f56ed1f6ba91fd3a1a88e97c1c61bc75b45580dde62871f3ed9` |
| `weld-seam-analysis/src/analyzer.py` | 2025-04-01 16:17 | 13506 | `9383f4ad415df6e47540a61fb0623af2bc10a9ab91f86757c9c88353542d7220` |
| `weld-seam-analysis/src/gui.py` | 2025-04-08 15:06 | 13672 | `847b44b90b368e10054084f93d76fcb1eba72bee56df0a85fe69cd70dce040cd` |
| `weld-seam-analysis/src/main.py` | 2025-03-17 19:52 | 227 | `240dba9ee73b37f95fc9635bf6503381bf448276301f39e9c393aecc834625d1` |
| `linreq/json_data_export.xlsx` | 2025-04-08 15:45 | 25540 | `3158331ca2924f49fb759c46c1875eaa2abe43a1529237c7a63160a4a16ed79e` |
| `linreq/lin_req.ipynb` | 2025-04-08 15:44 | 306654 | `6db12fbcfad9218a37aeb96af7ef833df896987c3f29dc46de33f4db49c1062b` |
| `hibacsoportok_2025-06.csv` | a forrásdokumentum: 2025-06-24 | 1311 | `130258e9b2fc92a75e7f091e1a9ee5b3e42f26ed167adc07f16e6c1a6cd6a94f` |
