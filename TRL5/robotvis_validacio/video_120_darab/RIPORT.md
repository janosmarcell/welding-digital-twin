# T5-08 kiegészítő mérés – cellás videó, 120. darab (g04_s120)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-12); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), minden felhasznált átmenet képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `120_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 20,9 s) |
| SHA-256 | `1718f2be7b673817fbebc3ff7ccb217f7f690987b1a472db3f99ae525a4f8f44` |
| Felvétel ideje | 2023-07-12, kb. 11:14 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g04_60/g04_s120.csv` (első sor 11:13:45,088 helyi idő) |
| A képernyőn | RobotVis; 60 cm/min-es csoport; 23,8 V, 200 A, 7 m/min |

A kamera a 2. varrat végén és a 3. elején a cellát mutatja.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,090 | 3,262 | 2,172 |
| 1. varrat: TorchSignal 1→0 | 229 | 6,027 | 8,227 | 2,200 |
| 2. varrat: TorchSignal 0→1 | 240 | 6,388 | 8,560 | 2,172 |
| 3. varrat: TorchSignal 1→0 | 623 | 16,171 | 18,356 | 2,185 |

- **Stabilitás:** az eltolás 2,172–2,200 s (terjedelem 28 ms, kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl neve a felvétel közben váltott (`119_2023-07-12_11-2-11.csv` → `120_2023-07-12_11-13-44.csv`, 1,263 s-nál; 1,229 s-nál még a régi); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,88 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
