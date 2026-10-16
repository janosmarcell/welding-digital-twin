# TRL5 – valós + szintetikus validáció (v2)

## Elkészült eredmények

A 2026.10.15-i futás a felhasználó `csv_light2.zip` csomagjából dolgozik. A bemeneti SHA-256 hash a jegyzőkönyvben van. Az alapcsomagban 150 CSV, 20 JPG, 18 PLY szerepel. Az összes CSV, JPG és PLY beolvasható. A 150 CSV közül 149 három aktív TorchSignal-szakaszt, a `g02_s33` fájl kettőt tartalmaz. 17 munkadarabhoz áll rendelkezésre mindhárom fájltípus azonos fájltővel; **ez nem jelenti a kézi mintaszintű azonosság igazolását**.

A szintetikus stresszteszteket a v1 hat általános forgatókönyve és az eredeti valós adatokból generált kiegészítő szcenáriók adják. A `synthetic_real_anchored` állományok **nem valós hibás hegesztések**, hanem ismert injektált eltérések a valós bázismintában.

### Futtatás VS Code-ban

- Python 3.10+; `python -m pip install -r requirements.txt`
- `python src/run_real_validation.py --real-zip "C:\\adatok\\csv_light2.zip"`
- vagy Windowsban: `run_windows.bat "C:\\adatok\\csv_light2.zip"`
- tesztek: `python -m pytest src/test_validation.py -q` (pytest telepítése szükséges)

A CSV/JPG/PLY **nincs duplikálva a ZIP-ben**; a felhasználó eredeti `csv_light2.zip` mellé kell tenni és `--real-zip` útvonallal megadni. A program az eredeti ZIP-et nem módosítja.

A gépi kimenetek a `outputs/` mappába kerülnek. A `outputs/TRL5_valos_adatos_osszefoglalo.xlsx` áttekintés; a `outputs/TRL5_v2_futtatasi_jegyzokonyv.md` a tudományosan védhető megállapítások és korlátok listája.

## Nyolc teszt – értelmezés

- T5-01: valós CSV szerkezet átvizsgálva; kézzel annotált események pontosságvizsgálata nyitott.
- T5-02: valódi mintából képzett jelkiugrás, ugyanazon minta alapján beállított egyszerű tesztdetektor; független valódi hiba nélkül nem minősül végleges anomáliadetektornak.
- T5-03: minden JPG leolvasva, feltáró QC + kontrollált képtorzítás; a v1 élesség/kontraszt döntési függvénye nem fogott meg minden takarást, ezért finomítandó.
- T5-04: minden PLY vertexrésze beolvasva; valós PLY-ből mesterségesen eltolt pontokkal próba. Az **FGR/ICP igazolása nincs elvégezve**, a teljes modell nem futott.
- T5-05: 91–99% rangpercentilis sweep az ismert szintetikus eltérésen. A 98% eredmény az *adott próba sajátossága*, nem állandó minőségi határ.
- T5-06: fájlnév-megfeleltetés és hiánylista kész, fizikai azonosító hitelesítése szükséges.
- T5-07: hiányzik a független valós OK/NOK címke és a megfelelő konfúziós mátrix.
- T5-08: szükséges a tényleges robotcellás hálózati késleltetés és kezelői próba.

## Szintzárási státusz

**A TRL5 nem lezárt.** Reprodukálható adatinventár, valós adatokra épülő első stressztesztek, és validációs hiánylista készült. A valós hibák detektálási pontossága, az ISO 5817 szerinti minőségmegfelelőség, a fizikai mérőrendszer felbontása és egy digitális iker üzemi működése a mostani fájlok alapján nem igazolt.
