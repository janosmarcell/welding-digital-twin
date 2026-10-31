# T5-08 kiegészítő mérés – cellás videó, 70. darab (g03_s70)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-11); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), minden felhasznált átmenet képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `70_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 26,7 s) |
| SHA-256 | `3030f358731663c65d223185335b17ce754a5904e7ef0043aae7d82855c87c9c` |
| Felvétel ideje | 2023-07-11, kb. 9:14 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g03_50/g03_s70.csv` (első sor 09:13:48,522 helyi idő) |
| A képernyőn | RobotVis; 50 cm/min-es csoport; 18,11 V, kb. 107 A |

A kamera kb. 20,3–26,5 s között a cellát mutatja, a 3. varrat vége nem látszik. A 9,0–11,3 s közötti automatikus „kikapcsolás” a kamera közelítése miatti műtermék; a képsoron a pipa 11,324 s-ig látszik, ezért kihagyva.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 42 | 1,226 | 5,759 | 4,533 |
| 1. varrat: TorchSignal 1→0 | 267 | 6,799 | 11,357 | 4,558 |
| 2. varrat: TorchSignal 0→1 | 277 | 7,142 | 11,657 | 4,515 |

- **Stabilitás:** az eltolás 4,515–4,558 s (terjedelem 43 ms, kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl a felvétel közben jött létre (a naplófájl neve `69_2023-07-11_9-11-29.csv` → `70_2023-07-11_9-13-46.csv` (3,060 s-nál; 3,027 s-nál még a régi)); ebből a CSV-időbélyegtől a kijelzésig tartó késés kb. 0 (egy képkockán belül; számított érték +0,01 s).

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
