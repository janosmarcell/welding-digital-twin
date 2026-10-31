# T5-08 kiegészítő mérés – cellás videó, 60. darab (g02_s60)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-10); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. A módszer azonos a 10/20/30. darab riportjáéval; a „Torch Signal” sort a képkockákon sablonillesztés követi (`track_torch.py`), minden átmenetet képsorral vizuálisan ellenőriztem (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `60_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 30,4 s) |
| SHA-256 | `5f6aea19768b9a55e94a3646bad4be7da101195bfac2c5a83b60964e1427697a` |
| Felvétel ideje | 2023-07-10, kb. 16:12 helyi idő (fájl-metaadat, a felvétel vége; a képernyő órája egyezik) |
| Párosított CSV | `datasets/welding_experiments_v1/g02_40/g02_s60.csv` (első sor 16:12:03,075 helyi idő) |
| A képernyőn | RobotVis; a naplófájl neve `59_2023-07-10_16-9-21.csv` → `60_2023-07-10_16-12-2.csv` (3,607 s-nál; 3,573 s-nál még a régi); 40 cm/min-es csoport; 23,8 V, 200 A, 7 m/min |

A kamera a 2. varrat végén és a 3. elején a cellát mutatja.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,136 | 5,473 | 4,337 |
| 1. varrat: TorchSignal 1→0 | 316 | 7,924 | 12,270 | 4,346 |
| 2. varrat: TorchSignal 0→1 | 329 | 8,334 | 12,703 | 4,369 |
| 3. varrat: TorchSignal 1→0 | 892 | 22,222 | 26,564 | 4,342 |

- **Stabilitás:** az eltolás 4,337–4,369 s (terjedelem 32 ms, legfeljebb kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl 16:12:02-kor jött létre (másodperc pontossággal), a neve 3,573–3,607 s között jelent meg a képernyőn; ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb, 0,72 s.
- **Feltétel:** a CSV `SysTimeMsecs` és a naplófájl neve ugyanabból a PC-órából származik (a RobotVis-forrás szerint igen: `OS.get_system_time_msecs`, illetve `OS.get_datetime`).

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó; a felső becslés a 2 s-os kapu alatt.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
