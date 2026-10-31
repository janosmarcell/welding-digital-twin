# T5-08 kiegészítő mérés – cellás videó, 110. darab (g04_s110)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-12); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), minden felhasznált átmenet képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `110_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 20,5 s) |
| SHA-256 | `b31d73fe6897b6fb9b3ad2455525a3932852698b9cf27aec5d2c8a34349f4e77` |
| Felvétel ideje | 2023-07-12, kb. 9:37 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g04_60/g04_s110.csv` (első sor 09:36:48,902 helyi idő) |
| A képernyőn | RobotVis; 60 cm/min-es csoport; 21,4 V, 160 A |

A kamera kb. 4–17 s között a cellát mutatja, a köztes ívszünetek nem látszanak.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 44 | 1,149 | 3,142 | 1,993 |
| 3. varrat: TorchSignal 1→0 | 622 | 16,202 | 18,203 | 2,001 |

- **Stabilitás:** az eltolás 1,993–2,001 s (terjedelem 8 ms, kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl neve a felvétel közben váltott (`109_2023-07-12_9-31-54.csv` → `110_2023-07-12_9-36-47.csv`, 1,043 s-nál; 1,010 s-nál még a régi); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,09 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
