# T5-08 kiegészítő mérés – cellás videó, 100. darab (g04_s100)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-11); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), minden felhasznált átmenet képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `100_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 23,3 s) |
| SHA-256 | `a673fc087a473c319a80f2a6f8ebadf7951afd276f20bfff1a504984f0e48d21` |
| Felvétel ideje | 2023-07-11, kb. 15:23 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g04_60/g04_s100.csv` (első sor 15:23:00,670 helyi idő) |
| A képernyőn | RobotVis; 60 cm/min-es csoport; 19,8 V, 95,5 A, 3 m/min |

A kamera a 2. varrat végén és a 3. elején a cellát mutatja.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,121 | 3,906 | 2,785 |
| 1. varrat: TorchSignal 1→0 | 228 | 5,917 | 8,705 | 2,788 |
| 2. varrat: TorchSignal 0→1 | 238 | 6,281 | 9,038 | 2,757 |
| 3. varrat: TorchSignal 1→0 | 625 | 16,242 | 19,001 | 2,759 |

- **Stabilitás:** az eltolás 2,757–2,788 s (terjedelem 31 ms, kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl neve a felvétel közben váltott (`99_2023-07-11_15-20-46.csv` → `100_2023-07-11_15-22-59.csv`, 2,074 s-nál; 2,041 s-nál még a régi); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,08 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
