# T5-08 – visszajátszásos mérés (valós cellás CSV-k, valós RobotVis, robot és áramforrás nélkül)

- Futások: 3 (követelmény: ≥ 3); cél: P95 ≤ 2000 ms a pozícióra és az áramforrás-értékekre minden futásban (jóváhagyandó).
- A mérés a forrás (visszajátszó) és a RobotVis-napló között méri a késést; a kijelzés ugyanabban a képkockában frissül, mint a naplózás.
- Nem méri: a valós robotvezérlő és áramforrás belső késését (ezt a cellás videók becslik), a hálózati kapcsolat hibáit a cellában.

| Futás | Pozíció P50 / P95 / max [ms] | Összevont pozíció | Áramforrás P50 / P95 / max [ms] | Kimaradt érték | TorchSignal-váltás max [ms] | Leghosszabb naplórés [ms] | Megállás > 2 s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| futas1 | 36.9 / 85.4 / 295.3 | 0 / 1199 | 185.1 / 351.3 / 830.8 | 83 / 115 | 266.9 (3 db) | 604 | 0 |
| futas2 | 31.1 / 73.1 / 532.0 | 0 / 1197 | 133.0 / 294.0 / 796.2 | 41 / 111 | 154.7 (3 db) | 753 | 0 |
| futas3 | 32.4 / 69.3 / 119.5 | 0 / 1206 | 249.0 / 464.9 / 482.7 | 91 / 119 | 466.1 (3 db) | 737 | 0 |

**A KÉSLELTETÉSI FELTÉTEL TELJESÜL** (a kimaradt értékeket és a megállásokat a jegyzőkönyvben külön kell értékelni).
