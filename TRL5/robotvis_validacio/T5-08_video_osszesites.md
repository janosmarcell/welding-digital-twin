# T5-08 – cellás videók összesítése (15 valós futás)

A kijelzett „Torch Signal” váltások képkockánkénti illesztése a RobotVis CSV-naplójához. Felvételek: 2023-07-10, -11 és -12 (valós, cellában); kiértékelés: 2026-10-30 és 2026-10-31 (B). A 2026-10-31-i futásoknál a „Torch Signal” sort sablonillesztés követte, és minden felhasznált átmenetet képsorral vizuálisan ellenőriztem.

| Futás | Csoport | Napló | Mért események | Eltolás terjedelme | A késés felső becslése |
| --- | --- | --- | --- | --- | --- |
| 10. darab, 2023-07-10 | 30 cm/min | g01_s10.csv | 4 | 41 ms | ≤ kb. 0,62 s |
| 20. beállítás, 2023-07-12 | 30 cm/min | 20_2023-07-12_14-42-8.csv | 3 | 10 ms | ≤ kb. 0,86 s |
| 30. darab, 2023-07-10 | 30 cm/min | g01_s30.csv | 4 | 31 ms | ≤ kb. 0,84 s |
| 40. darab, 2023-07-10 | 40 cm/min | g02_s40.csv | 4 | 15 ms | nem mérhető (a naplófájl a felvétel előtt jött létre) |
| 50. darab, 2023-07-10 | 40 cm/min | g02_s50.csv | 4 | 12 ms | ≤ kb. 0,62 s |
| 60. darab, 2023-07-10 | 40 cm/min | g02_s60.csv | 4 | 32 ms | ≤ kb. 0,72 s |
| 70. darab, 2023-07-11 | 50 cm/min | g03_s70.csv | 3 | 43 ms | kb. 0 (egy képkockán belül) |
| 80. darab, 2023-07-11 | 50 cm/min | g03_s80.csv | 2 | 8 ms | ≤ kb. 0,78 s |
| 90. darab, 2023-07-11 | 50 cm/min | g03_s90.csv | 3 | 10 ms | kb. 0 (egy képkockán belül) |
| 100. darab, 2023-07-11 | 60 cm/min | g04_s100.csv | 4 | 31 ms | ≤ kb. 0,08 s |
| 110. darab, 2023-07-12 | 60 cm/min | g04_s110.csv | 2 | 8 ms | ≤ kb. 0,09 s |
| 120. darab, 2023-07-12 | 60 cm/min | g04_s120.csv | 4 | 28 ms | ≤ kb. 0,88 s |
| 130. darab, 2023-07-12 | 70 cm/min | g05_s130.csv | 4 | 45 ms | ≤ kb. 0,67 s |
| 140. darab, 2023-07-12 | 70 cm/min | g05_s140.csv | 6 | 35 ms | ≤ kb. 0,37 s |
| 150. darab, 2023-07-12 | 70 cm/min | g05_s150.csv | 6 | 24 ms | ≤ kb. 0,73 s |

**Következtetés:** mind a tizenöt valós cellás futásban (mind az 5 sebességcsoport, 3 nap, 57 esemény) a RobotVis folyamatosan és a naplóval egyezően jelenített meg; a CSV-időbélyegtől a kijelzésig tartó késés felső becslése (14 futásból) legfeljebb kb. 0,88 s (a javasolt kapu: P95 ≤ 2 s), és egy futáson belül állandó (terjedelem ≤ 45 ms, kb. egy-másfél képkocka). A látható szakaszokban megállás nem volt.

**Korlátok:** eseményenkénti felső becslés, nem P50/P95-eloszlás; a robotvezérlő és az áramforrás felőli késés nem mérhető (a robot és a kijelző nem látszik egyszerre); adatvesztés nem számolható; a kezelői próba (nem fejlesztő kezelő) nem része a felvételeknek. Feltétel: a CSV-időbélyeg és a naplófájl neve ugyanabból a PC-órából származik (a forrás szerint igen). A 140. és 150. darab felvételén mind a két varratközi ívszünet (kb. 0,35–0,41 s) a kijelzőn is megjelenik.
