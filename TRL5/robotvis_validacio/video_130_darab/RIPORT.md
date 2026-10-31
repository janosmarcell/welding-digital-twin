# T5-08 kiegészítő mérés – cellás videó, 130. darab (g05_s130)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-12); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), a felhasznált átmenetek képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `130_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 21,5 s) |
| SHA-256 | `3fa0f44c06d7e5f87d87e8ccb7b9292e2ade60da6412316e9ff9e3a331a62e20` |
| Felvétel ideje | 2023-07-12, kb. 12:19 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g05_70/g05_s130.csv` (első sor 12:19:03,277 helyi idő) |
| A képernyőn | RobotVis; 70 cm/min-es csoport; 19,8 V, 95,5 A, 3 m/min |

A kamera a 2. varrat végén és a 3. elején a cellát mutatja.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 42 | 1,030 | 3,400 | 2,370 |
| 1. varrat: TorchSignal 1→0 | 202 | 5,280 | 7,665 | 2,385 |
| 2. varrat: TorchSignal 0→1 | 215 | 5,625 | 7,965 | 2,340 |
| 3. varrat: TorchSignal 1→0 | 547 | 14,390 | 16,762 | 2,372 |

- **Stabilitás:** az eltolás 2,340–2,385 s (terjedelem 45 ms, kb. egy-másfél képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl neve a felvétel közben váltott (`129_2023-07-12_12-8-17.csv` → `130_2023-07-12_12-19-2.csv`, 1,467 s-nál; 1,434 s-nál még a régi); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,67 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
