# T5-08 – a cellás naplók folytonossága (adatvesztés, megállás)

**Bizonyítékosztály:** valós cellás naplók (2023-07-10…12), újraszámolva (B). Kiértékelés: 2026-10-30.
**Adat:** a 150 darab CSV (`datasets/welding_experiments_v1`) és a 2023-07-12-i `20_2023-07-12_14-42-8.csv`, összesen 151 futás.

## Módszer

A RobotVis a `SysTimeMsecs` időbélyeget csomagokban írja (több sor azonos időbélyeggel). A folytonosságot a különböző időbélyegek közötti lépésből mérjük; az 1 s-nál nagyobb lépés kiesésnek (adatvesztés vagy megállás) számít.

## Eredmény

- **Szokásos frissítés:** a lépés mediánja futásonként 109–118 ms (összesítve 114 ms), a 95. percentilis mediánja 144 ms.
- **Kiesések:** 151 futásból 7-ben (4,6%) van 1 s-nál hosszabb rés, összesen 8; ebből 3 futásban 2 s felett (leghosszabb 2,50 s). Mindegyik hegesztés közben (TorchSignal = 1) történt, és szinte mind kb. 2,0 s hosszú, ami időtúllépésre vagy újracsatlakozásra utal.
- **Következmény:** a `g02_s33` fájlban a 2,50 s-os rés éppen az 1. és 2. varrat közötti váltásra esett, ezért a naplóban csak 2 aktív szakasz van a 3 helyett. A `g01_s24` és a `g03_s61` fájlban a rés a varrat végére esett, így a váltás késve rögzült.

| Fájl | Sor | Rés [ms] | TorchSignal előtte → utána | Idő a futás elejétől [s] |
| --- | --- | --- | --- | --- |
| g01_s03 | 503 | 1895 | 1 → 1 | 12,96 |
| g01_s24 | 341 | 2099 | 1 → 0 | 8,08 |
| g02_s33 | 311 | 2502 | 1 → 1 | 7,21 |
| g03_s61 | 600 | 2008 | 1 → 1 | 15,62 |
| g03_s61 | 601 | 1982 | 1 → 0 | 17,63 |
| g03_s78 | 170 | 1975 | 1 → 1 | 4,34 |
| g05_s129 | 243 | 1997 | 1 → 1 | 6,60 |
| g05_s136 | 265 | 1997 | 1 → 1 | 7,38 |

## Értékelés a T5-08 kapuhoz

- A rendes frissítés (kb. 114 ms) és a videókból becsült kijelzési késés (≤ kb. 0,86 s) a 2 s-os célon belül van.
- **Az adatfolyam azonban nem hibamentes:** a futások kb. 5%-ában kb. 2 s-os kiesés van, ami egy esetben szakaszhatárt is elnyelt. A jegyzőkönyvben ezt a kapun kívül, külön kell értékelni (a 03-as kiértékelő is külön jelzi az adatvesztést és a megállást).
- **Javaslat:** a kiesés okának feltárása (RobotComm-socket, Selenium-olvasás vagy a webfelület frissítése); a TorchSignal-váltást a T5-01 annotációban és a T5-02 detektorban ilyen résnél „ELLENŐRIZENDŐ” státusszal kell kezelni.

Fájlok: `fajlonkent.csv` (futásonként), `resek_1s_felett.csv`.
