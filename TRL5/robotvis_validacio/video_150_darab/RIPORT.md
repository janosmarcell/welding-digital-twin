# T5-08 kiegészítő mérés – cellás videó, 150. darab (g05_s150)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-12); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), a felhasznált átmenetek képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `150_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 19,3 s) |
| SHA-256 | `6e179e68b9ed8634e1f3dc275c166740e4be72bf62eca818611a63eefdc6c91c` |
| Felvétel ideje | 2023-07-12, kb. 14:38 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g05_70/g05_s150.csv` (első sor 14:37:36,099 helyi idő) |
| A képernyőn | RobotVis; 70 cm/min-es csoport; 23,8 V, 200 A, 7 m/min |

Mind a hat átmenet látszik, a két varratközi ívszünet a kijelzőn is megjelenik.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 44 | 1,116 | 3,249 | 2,133 |
| 1. varrat: TorchSignal 1→0 | 201 | 5,310 | 7,447 | 2,137 |
| 2. varrat: TorchSignal 0→1 | 213 | 5,664 | 7,814 | 2,150 |
| 2. varrat: TorchSignal 1→0 | 375 | 9,919 | 12,045 | 2,126 |
| 3. varrat: TorchSignal 0→1 | 386 | 10,265 | 12,412 | 2,147 |
| 3. varrat: TorchSignal 1→0 | 545 | 14,504 | 16,644 | 2,140 |

- **Stabilitás:** az eltolás 2,126–2,150 s (terjedelem 24 ms, kb. egy-másfél képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl neve a felvétel közben váltott (`149_2023-07-12_14-0-50.csv` → `150_2023-07-12_14-37-35.csv`, 1,349 s-nál; 1,316 s-nál még a régi); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,73 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
