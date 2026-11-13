# T5-08 – visszajátszásos mérés (valós cellás CSV-k, valós RobotVis, robot és áramforrás nélkül)

- Futások: 3 (követelmény: ≥ 3); cél: P95 ≤ 2000 ms a pozícióra és az áramforrás-értékekre minden futásban (jóváhagyandó).
- A mérés a forrás (visszajátszó) és a RobotVis-napló között méri a késést; a kijelzés ugyanabban a képkockában frissül, mint a naplózás.
- Nem méri: a valós robotvezérlő és áramforrás belső késését (ezt a cellás videók becslik), a hálózati kapcsolat hibáit a cellában.

| Futás | Pozíció P50 / P95 / max [ms] | Összevont pozíció | Áramforrás P50 / P95 / max [ms] | Kimaradt érték | TorchSignal-váltás max [ms] | Leghosszabb naplórés [ms] | Megállás > 2 s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| futas1 | 33.5 / 70.6 / 95.8 | 0 / 927 | 275.3 / 746.7 / 894.9 | 66 / 89 | 137.1 (1 db) | 582 | 0 |
| futas2 | 32.2 / 117.0 / 493.3 | 0 / 774 | 278.7 / 802.4 / 808.1 | 52 / 71 | 720.1 (3 db) | 546 | 0 |
| futas3 | 32.1 / 75.8 / 140.8 | 0 / 584 | 226.1 / 433.6 / 518.4 | 38 / 54 | 405.4 (3 db) | 643 | 0 |

**A KÉSLELTETÉSI FELTÉTEL TELJESÜL** (a kimaradt értékeket és a megállásokat a jegyzőkönyvben külön kell értékelni).
