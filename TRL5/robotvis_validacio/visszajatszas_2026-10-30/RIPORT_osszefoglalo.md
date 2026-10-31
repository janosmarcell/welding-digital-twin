# T5-08 – visszajátszásos mérés, 2026-10-30 (valós RobotVis, valós cellás CSV-k)

**Bizonyítékosztály:** mérés a valós RobotVis programmal (2023-06-27-i build, helyi teszt-oldal mód), a valós cellás naplók (`g01_s10`, `g01_s30`, `20_2023-07-12_14-42-8`) visszajátszásával; robot és áramforrás nélkül. A mérés dátuma: 2026-10-30. A számok a nyers naplókból újraszámolva (B).

| Fájl | SHA-256 |
| --- | --- |
| futas1_2026-10-30_20-14-42.csv | 2381207ca4c6f91dd601f4886eecb44627aa3d0a978937da2f4699c9e16378f3 |
| futas2_2026-10-30_20-16-33.csv | 58b92d9693df3b7074846d1b8071ae82e8e319204b259123f870b76643e8fd57 |
| futas3_2026-10-30_20-17-39.csv | b835aafe7a91265662d9718d99634586db2e2410fd2cb4fe8601563106cae1ef |
| kuldesi_naplo.csv | 53ffe139b6335f44739728643b230d5a56017db4071c7499ef085e766b12f196 |

## Eredmény

| Futás | Pozíció P50 / P95 / max [ms] | Áramforrás-érték P50 / P95 / max [ms] | TorchSignal-váltás késése [ms] (6 váltás) | Megállás > 2 s |
| --- | --- | --- | --- | --- |
| futas1 (g01_s10) | 37 / 85 / 295 | 185 / 351 / 831 | 550, 130, 147, 114, 620, 267 | 0 |
| futas2 (g01_s30) | 31 / 73 / 532 | 133 / 294 / 796 | 342, **kimaradt**, 132, 155, 152, 110 | 0 |
| futas3 (20, 2023-07-12) | 32 / 69 / 120 | 249 / 465 / 483 | 933, 270, 973, 466, 979, 463 | 0 |

- **Pozíció (RobotComm-út):** mind a 3602 elküldött pozíció megjelent a naplóban; P95 ≤ 85 ms.
- **Áramforrás-értékek (Selenium-olvasás):** P95 ≤ 465 ms, de a naplóban az értékváltások közötti idő mediánja 245–1014 ms, miközben a forrásban kb. 230 ms: a Selenium-út effektíven ritkábban frissít a forrásnál, és a forrásértékek 36–76%-a nem kerül a naplóba.
- **TorchSignal:** 18 váltásból 17 megjelent, legfeljebb kb. 0,98 s késéssel. **Egy rövid kikapcsolás (futas2, az 1. és 2. varrat közötti kb. 0,45 s) egyáltalán nem jelent meg**, így a naplóban a két varrat egy szakasznak látszik. Ugyanez a jelenség, mint a cellás `g02_s33` naplóban.
- **Megállás:** nincs 2 s-nál hosszabb naplórés; a leghosszabb rés (0,60–0,75 s) a forrás saját szünete (varratok közötti mozgás).

## Értékelés a T5-08 kapuhoz

- **A késleltetési feltétel (P95 ≤ 2 s minden futásban) teljesül** a pozícióra és az áramforrás-értékekre is.
- **Az adatteljesség nem hibamentes:** az áramforrás-értékek olvasása lassabb a forrás változásánál, és egy rövid TorchSignal-szünet elveszett. Ez a szakaszfelismerést (T5-01) is érinti. Javaslat: a TorchSignal a robotvezérlőből (I/O) vagy az áramforrás WebSocket-kapcsolatából (a RobotVis-ben előkészített `WeldUnitConnector`) jöjjön a Selenium-olvasás helyett; addig a 0,5 s-nál rövidebb szünetek „ELLENŐRIZENDŐ” státuszt kapnak.
- **Nem méri:** a valós robotvezérlő és áramforrás belső késését (ezt a cellás videók becslik: ≤ kb. 0,62–0,86 s), a cellabeli hálózati hibákat.
- A kezelő nevét, a próba körülményeit és az ellenőrzőlistát a jegyzőkönyv rögzíti.
