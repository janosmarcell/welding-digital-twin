# T5-08 kiegészítő mérés – cellás videó, 80. darab (g03_s80)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-11); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. Módszer: a „Torch Signal” sor sablonillesztéses követése (`track_torch.py`), minden felhasznált átmenet képsoros vizuális ellenőrzésével (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `80_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 25,7 s) |
| SHA-256 | `bc2ff75ac59222a41bda13f2cc22fe6b6df3cd28bae0c2f4a2c040a4e2a193e1` |
| Felvétel ideje | 2023-07-11, kb. 9:34 helyi idő (fájl-metaadat, a felvétel vége) |
| Párosított CSV | `datasets/welding_experiments_v1/g03_50/g03_s80.csv` (első sor 09:33:57,093 helyi idő) |
| A képernyőn | RobotVis; 50 cm/min-es csoport; 21,4 V, 160 A, 5 m/min |

A kamera kb. 9–20 s között a cellát mutatja, a köztes ívszünetek nem látszanak.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,131 | 4,294 | 3,163 |
| 3. varrat: TorchSignal 1→0 | 738 | 18,783 | 21,954 | 3,171 |

- **Stabilitás:** az eltolás 3,163–3,171 s (terjedelem 8 ms, kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl a felvétel közben jött létre (a naplófájl neve `79_2023-07-11_9-31-57.csv` → `80_2023-07-11_9-33-56.csv` (2,328 s-nál; 2,295 s-nál még a régi)); ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb. 0,78 s.

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
