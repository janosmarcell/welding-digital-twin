# T5-08 kiegészítő mérés – cellás videó, 140. darab (g05_s140)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-12); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), a felhasznált átmenetek képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `140_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 20,0 s) |
| SHA-256 | `d5360fc3f9a635c0edd7db9170cce6a993cabcb05c9a657d1a77121a5087cd73` |
| Felvétel ideje | 2023-07-12, kb. 13:16 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g05_70/g05_s140.csv` (első sor 13:16:11,395 helyi idő) |
| A képernyőn | RobotVis; 70 cm/min-es csoport; kb. 20,6 V, 158 A |

Mind a hat átmenet látszik, a két varratközi ívszünet (409 ms és 363 ms a naplóban) a kijelzőn is megjelenik (433 ms, illetve 333 ms).

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 42 | 1,136 | 3,378 | 2,242 |
| 1. varrat: TorchSignal 1→0 | 202 | 5,260 | 7,510 | 2,250 |
| 2. varrat: TorchSignal 0→1 | 217 | 5,669 | 7,943 | 2,274 |
| 2. varrat: TorchSignal 1→0 | 380 | 9,871 | 12,141 | 2,270 |
| 3. varrat: TorchSignal 0→1 | 391 | 10,234 | 12,474 | 2,240 |
| 3. varrat: TorchSignal 1→0 | 549 | 14,331 | 16,606 | 2,275 |

- **Stabilitás:** az eltolás 2,240–2,275 s (terjedelem 35 ms, kb. egy-másfél képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl neve a felvétel közben váltott (`139_2023-07-12_13-11-17.csv` → `140_2023-07-12_13-16-10.csv`, 1,545 s-nál; 1,512 s-nál még a régi); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,37 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
