# T5-08 kiegészítő mérés – cellás videó, 50. darab (g02_s50)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-10); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. A módszer azonos a 10/20/30. darab riportjáéval; a „Torch Signal” sort a képkockákon sablonillesztés követi (`track_torch.py`), minden átmenetet képsorral vizuálisan ellenőriztem (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `50_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 31,7 s) |
| SHA-256 | `9d1dbfeb2b53c2aaccb990b9f0e9231a482214cd8dd3ca5f8fb7a47cc5a67795` |
| Felvétel ideje | 2023-07-10, kb. 15:22 helyi idő (fájl-metaadat, a felvétel vége; a képernyő órája egyezik) |
| Párosított CSV | `datasets/welding_experiments_v1/g02_40/g02_s50.csv` (első sor 15:22:14,292 helyi idő) |
| A képernyőn | RobotVis; a naplófájl neve `49_2023-07-10_15-18-14.csv` → `50_2023-07-10_15-22-13.csv` (5,046 s-nál; 5,013 s-nál még a régi); 40 cm/min-es csoport; 21,4 V, 160 A, 5 m/min |

A kamera kb. 16,2–24,6 s között a cellát mutatja; a 2. varrat vége és a 3. eleje ezért nem látszik. A 6,012 s-nál jelzett egykockás „pipa” vizuálisan ellenőrizve műtermék (a képen nincs pipa), kihagyva.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,232 | 7,145 | 5,913 |
| 1. varrat: TorchSignal 1→0 | 318 | 7,918 | 13,843 | 5,925 |
| 2. varrat: TorchSignal 0→1 | 330 | 8,252 | 14,176 | 5,924 |
| 3. varrat: TorchSignal 1→0 | 891 | 22,245 | 28,170 | 5,925 |

- **Stabilitás:** az eltolás 5,913–5,925 s (terjedelem 12 ms, legfeljebb kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl 15:22:13-kor jött létre (másodperc pontossággal), a neve 5,013–5,046 s között jelent meg a képernyőn; ebből a CSV-időbélyegtől a kijelzésig tartó késés legfeljebb kb, 0,62 s.
- **Feltétel:** a CSV `SysTimeMsecs` és a naplófájl neve ugyanabból a PC-órából származik (a RobotVis-forrás szerint igen: `OS.get_system_time_msecs`, illetve `OS.get_datetime`).

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó; a felső becslés a 2 s-os kapu alatt.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
