# TRL5 mérhető szintzárási követelmények — jóváhagyandó v1

**Fontos:** alábbi értékek tervezett mérési kapuk, **nem teljesített eredmények** és nem az ISO 5817 követelményértékei. A mintaméretet, hibakategóriákat és számszerű határokat **a valós vizsgálat kezdete előtt** projektvezető/minőségügyi szakértő rögzíti.

| Teszt | Mérőszám / képlet | Kiinduló javasolt tesztkapu | Bizonyíték, amit létre kell hozni |
|---|---|---|---|
| T5-01 | Pontosan felismert, manuálisan annotált kezdő- és záróesemények aránya; külön struktúrahiba-visszautasítás | Valós mintákon cél >= 99% eseményegyezés, max. 1 rögzített mintavételi periódus időkülönbséggel; minden kivétel listázva | Annotált valós CSV + automatikus vs. manuális összevetés |
| T5-02 | Pontosság, recall, TP/FP/FN injektált jelanomáliákon | Szintetikus validáción recall >= 95%; valós hibadetektálási limit csak szakértői címkékkel | Injektálási napló + elkülönített FP/FN riport |
| T5-03 | Nem értékelhető képek felismerése; kontúr/szélesség eltérés manuális referenciához | Kontraszt, elmosódás és takarás esetén nincs automatikus OK; a mérési eltérés mm-ben csak ismert képi skála mellett értékelhető | Valós JPG + képminőség-jegyzőkönyv + mérési referencia |
| T5-04 | FGR/ICP fitness és RMSE, DBSCAN lokalizáció IoU / pozíciós hiba | Szintetikus ismert hibákon javasolt IoU >= 0.70; valós mintákra hibatípusonként és ismételt szkennelés alapján külön határ | Valós és szintetikus PLY + ismert hibahely + vizuális ellenőrzés |
| T5-05 | 91..99%-os szenzitivitási görbe; hibatípusonként precision, recall, IoU | Kilenc pont értékelve; választott paraméter elkülönített, független teszten rögzítve; a 97% nem alapértelmezett minőségi határ | Görbék, kiválasztási jegyzőkönyv, rögzített paraméterkonfiguráció |
| T5-06 | Helyes CSV–2D–3D hozzárendelési arány; hiányadat visszautasítás | 100% bizonyítható azonosító egyezés a hitelesített mintatérképen; hiányos/ellentmondásos darab nem kap automatikus OK-t | Mapping CSV, lefedettségi riport, ellenpéldák |
| T5-07 | Független minősítési ground truth alapján TP/FP/TN/FN, külön false-OK | Előzetes javaslat: **0 hamis OK** a vizsgált hibás minták között; kétoldali 95% CI és mintaméret feltüntetése, 0 eset sem bizonyít zéró valós kockázatot | Független minősítés, összezárt confusion matrix, CI |
| T5-08 | Releváns környezeti streaming P50/P95 késleltetés, adatvesztés, kezelői helyes használat | Streaming kijelzés P95 <= 2 s mint vizsgálati cél; képfeldolgozás és 3D riport külön folyamatidővel; 3 ismételt kontrollált futás | Időbélyegzett log + kezelői aláírt jegyzőkönyv |

## Elengedhetetlen TRL5 zárófeltételek

- **Adatok eredete:** `real` / `synthetic` végig elkülönül, készletválasztás forrásmunkadarab alapján (származtatott minta nem kerülhet a végső független valós tesztbe ugyanannak a darabnak tanítóváltozataként).
- **Releváns környezet:** legalább egy dokumentált robotcellás, üzemszerű munkafolyamat, mérési feltételekkel, technológiai változtatással, környezeti paraméterekkel és kezelői beavatkozási menettel.
- **Műszaki korlát:** repedés, belső hiba és térfogati hibák automatikus OK-ja 3D felületi letapogatásból nem adható.
- **Rendszervédelem:** hiányzó 2D/3D, sikertelen illesztés vagy adatkapcsolási ellentmondás esetén `ELLENŐRIZENDŐ` / `NEM ÉRTÉKELHETŐ` státusz.
- **Kimenet:** futtatható, reprodukálható szoftververzió, gépi mérési riportok, emberi validációs jegyzőkönyv, verzió/futtatási azonosító, vállalt küszöbértékek és nyitott hibák listája.

A teljes TRL5-t csak a **valós, releváns környezeti teszt eredményével** és a jóváhagyott szintzárási dokumentum alapján szabad lezártnak jelölni.
