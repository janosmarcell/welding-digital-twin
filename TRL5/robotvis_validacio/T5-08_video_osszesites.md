# T5-08 – cellás videók összesítése (3 valós futás)

A kijelzett „Torch Signal” váltások és értékváltások képkockánkénti illesztése a RobotVis CSV-naplójához. Felvételek: 2023-07-10 és 2023-07-12 (valós, cellában); kiértékelés: 2026-10-30 (B).

| Futás | Napló | Mért események | Eltolás terjedelme | A késés felső becslése |
| --- | --- | --- | --- | --- |
| 10. darab, 2023-07-10 | g01_s10.csv | 4 | 41 ms | ≤ kb. 0,62 s |
| 20. beállítás, 2023-07-12 | 20_2023-07-12_14-42-8.csv | 3 | 10 ms | ≤ kb. 0,86 s |
| 30. darab, 2023-07-10 | g01_s30.csv | 4 | 31 ms | ≤ kb. 0,84 s |

**Következtetés:** mindhárom valós cellás futásban a RobotVis folyamatosan és a naplóval egyezően jelenített meg; a CSV-időbélyegtől a kijelzésig tartó késés felső becslése legfeljebb kb. 0,86 s (a javasolt kapu: P95 ≤ 2 s), és egy futáson belül állandó (terjedelem ≤ 41 ms, kb. egy képkocka). A látható szakaszokban megállás nem volt.

**Korlátok:** eseményenkénti felső becslés, nem P50/P95-eloszlás; a robotvezérlő és az áramforrás felőli késés nem mérhető (a robot és a kijelző nem látszik egyszerre); adatvesztés nem számolható; a kezelői próba (nem fejlesztő kezelő) nem része a felvételeknek. Feltétel: a CSV-időbélyeg és a naplófájl neve ugyanabból az órából származik.
