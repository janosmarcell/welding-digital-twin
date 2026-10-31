# T5-08 kiegészítő mérés – cellás videó, 90. darab (g03_s90)

**Bizonyítékosztály:** a felvétel valós, cellában készült (2023-07-11); a kiértékelés a nyers videóból és a nyers CSV-ből újraszámolt (B). A kiértékelés dátuma: 2026-10-31. A módszer azonos a 10/20/30. darab riportjáéval; a „Torch Signal” sort a képkockákon sablonillesztés követi (`track_torch.py`), minden átmenetet képsorral vizuálisan ellenőriztem (`row_sheet.py`, `fname_sheet.py`).

## Forrás

| Tétel | Érték |
| --- | --- |
| Videó | `90_darab.mp4` (telefonfelvétel, 1920×1080, kb. 30 fps, 25,8 s) |
| SHA-256 | `284cebe3ac287cdaff54e800d95f9be729ec6c090db50a9efcc8aca9ef374d1d` |
| Felvétel ideje | 2023-07-11, kb. 11:21 helyi idő (fájl-metaadat, a felvétel vége; a képernyő órája egyezik) |
| Párosított CSV | `datasets/welding_experiments_v1/g03_50/g03_s90.csv` (első sor 11:20:56,728 helyi idő) |
| A képernyőn | RobotVis; a naplófájl neve `89_2023-07-11_11-18-17.csv` → `90_2023-07-11_11-20-55.csv` (2,445 s-nál; 2,411 s-nál még a régi); 50 cm/min-es csoport; 23,8 V, 200 A, 7 m/min |

A kamera kb. 10,0–18,2 s között a cellát mutatja. A 7,2–7,9 s és a 18,5–19,4 s közötti automatikus „kikapcsolások” tükröződés és kameramozgás miatti műtermékek; a képsorokon a pipa végig látszik, ezért vizuális ellenőrzés alapján kihagyva.

## Eredmény

| Esemény | CSV-sor | CSV-idő [s] | Videó, első képkocka [s] | Eltolás [s] |
| --- | --- | --- | --- | --- |
| 1. varrat: TorchSignal 0→1 | 43 | 1,166 | 4,277 | 3,111 |
| 1. varrat: TorchSignal 1→0 | 268 | 6,857 | 9,975 | 3,118 |
| 3. varrat: TorchSignal 1→0 | 744 | 18,916 | 22,037 | 3,121 |

- **Stabilitás:** az eltolás 3,111–3,121 s (terjedelem 10 ms, legfeljebb kb. egy képkocka). Késés-felhalmozódás vagy kijelzési megállás a látható szakaszokban nincs.
- **A késés felső becslése:** a naplófájl 11:20:55-kor jött létre (másodperc pontossággal), a neve 2,411–2,445 s között jelent meg a képernyőn; ebből a CSV-időbélyegtől a kijelzésig tartó késés kb. 0 (egy képkockán, 0,03 s-on belül; a számított érték −0,02 s, ami a képkocka- és másodperc-kerekítésen belül van).
- **Feltétel:** a CSV `SysTimeMsecs` és a naplófájl neve ugyanabból a PC-órából származik (a RobotVis-forrás szerint igen: `OS.get_system_time_msecs`, illetve `OS.get_datetime`).

## Mit igazol és mit nem

- **Igazol:** folyamatos, a naplóval egyező megjelenítés valós hegesztés közben; a késés a futás alatt állandó; a felső becslés a 2 s-os kapu alatt.
- **Nem igazol:** P50/P95-eloszlást, adatvesztést, a robotvezérlő és az áramforrás felőli késést, a nem fejlesztő kezelő önálló használatát.
