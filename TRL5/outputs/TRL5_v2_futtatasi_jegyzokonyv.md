# TRL5 – valós adatos validációs jegyzőkönyv (v2)

Futtatás: 2026-10-15T11:39:51.087886+00:00
Bemeneti ZIP SHA-256: `bfd05bc7bb5e82f74bba5a7ecac556790a993a53add47f30a7bab77648e298bf`

**Szintzárás: NEM TELJESÍTETT.** A valós adatok strukturális ellenőrzése és valós adatokból generált szintetikus stressztesztek készültek, nem hegesztési megfelelőségi minősítés.

## Tényadatok
- CSV: **150**; JPG: **20**; PLY: **18**.
- Három várható aktív szakasz: **149/150 CSV**; kivétel: g02_s33.
- Fájlnév szerinti párosítás: **20 CSV+JPG**, **18 CSV+PLY**, **17 mindhárom**; a közös fájlnév technikai egyezés, nem kézzel hitelesített munkadarab-azonosítás.
- Időbélyeg-ismeret: 150 CSV-ben legalább egy ismétlődő időbélyeg-átmenet; ez a nyers időfelbontás értelmezését igényli. Nem csökkenő sorrend: True.
- PLY vertexek beolvasása **18/18**, JPG dekódolás **20/20**.

## Nyolc teszt – megfigyelés
| Azonosító | Megtörtént | Hiányzó rész |
|---|---|---|
| T5-01 | 150 valós CSV TorchSignal szerkezeti ellenőrzése | Kézzel annotált kezdő/vég ellenőrzés |
| T5-02 | Valós CSV-ből származtatott kontrollált jelkiugrás | Függetlenül címkézett valós anomáliák, valódi detektor pontossága |
| T5-03 | 20 valós JPG leolvasás, feltáró QC és képtorzítás | Kézi referenciakontúr/skála |
| T5-04 | 18 PLY leolvasása és ismert eltolású szintetikus pontfelhő | FGR + ICP valós referenciapárokon és szakértői hibatérkép |
| T5-05 | 91–99% vizsgálat valósból származtatott ismert eltérésen | Független valós adatokon választott küszöb igazolása |
| T5-06 | Fájlnév szerinti párosítás és teljes lefedettségi mátrix | Fizikai munkadarab-azonosító ellenőrzés |
| T5-07 | Biztonságos alpha előminősítés logika szintetikus adatokon | Független valós OK/NOK címkék; fals OK statisztika |
| T5-08 | Offline szintetikus stream logika | End-to-end robotcellás késleltetés és kezelői próba |

## Kapcsolódó fájlok

- `real_csv_inventory.csv` (150 munkadarab sor)
- `real_seam_features.csv` (aktív varratszakaszok)
- `real_modalities_mapping.csv` (CSV/JPG/PLY fájlnév-egyezés)
- `real_image_qc_exploratory.csv` (20 JPG, feltáró mutatók)
- `real_ply_geometry_inventory.csv` (18 PLY metadata és alakjellemző)
- `real_anchored_ply_threshold_sweep.csv` (szintetikus ismert eltolás: 91–99%)
- `real_data_results.json` (gépileg feldolgozható összesítő)

## Megkötések
A 97-es érték itt távolságpercentilis, nem az ISO 5817 szerinti megfelelőségi határ. Valós felületi referencia és független hegesztési minősítés nélkül OK/NOK pontosság nem becsülhető. A fájlnév szerinti összerendelés nem bizonyítja, hogy minden kép és PLY ugyanazon varratot ábrázolja.
