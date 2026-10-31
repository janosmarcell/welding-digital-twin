# T5-08 kiegészítő mérés – cellás videó, 40. darab (g02_s40)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-10); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), minden felhasznált átmenet képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `40_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 32,7 s) |
| SHA-256 | `c70dc4dc6f72147a315988fc6ca9e70bf59f0a2c273971f169b8ada2517c1a9e` |
| Felvétel ideje | 2023-07-10, kb. 13:20 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g02_40/g02_s40.csv` (első sor 13:19:39,759 helyi idő) |
| A képernyőn | RobotVis; 40 cm/min-es csoport; 19,8 V, 95,5 A, 3 m/min |

A kamera a 2. varrat végén és a 3. elején a cellát mutatja.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,115 | 6,512 | 5,397 |
| 1. varrat: TorchSignal 1→0 | 320 | 7,975 | 13,376 | 5,401 |
| 2. varrat: TorchSignal 0→1 | 332 | 8,312 | 13,709 | 5,397 |
| 3. varrat: TorchSignal 1→0 | 892 | 21,992 | 27,404 | 5,412 |

- **Stabilitás:** az eltolás 5,397–5,412 s (terjedelem 15 ms, kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** nem határozható meg, mert a naplófájl neve (`40_2023-07-10_13-19-12.csv`) már a felvétel indulásakor látszik, ezért a fájl létrehozása nem esik a felvételbe.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
