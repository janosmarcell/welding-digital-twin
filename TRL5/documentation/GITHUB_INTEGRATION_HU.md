# TRL5 v2 GitHub-integráció

## Eredet

Az állományok a `TRL5_valos_adatos_validacio_v2.zip` csomagból származnak. A meglévő mappaszerkezetet megtartottuk, mert a Python-futtatás és a Windows-batch ezen alapul.

## Futtatás

1. Python 3.10+ telepítése.
2. A `TRL5` mappában: `python -m pip install -r requirements.txt`.
3. Valós mérési adatokkal: `python src/run_real_validation.py --real-zip "C:\\adatok\\csv_light2.zip"`.
4. Tesztparancs: `python -m pytest src/test_validation.py -q` (a `pytest` külön telepítendő).

A `csv_light2.zip` nyers mérési archívum nincs a GitHub-feltöltőcsomagban.

## Státusz

A csomag korábbi teszteredményeket is tartalmaz. Ezek a régi futások dokumentált eredményei, nem a GitHubba áthelyezés során újrafuttatott vizsgálatok. A forrásfájlok szintaktikai ellenőrzése sikeres. Az FGR/ICP/DBSCAN valós referenciapárokon és a teljes robotcellás validáció még nyitott. A TRL5 nem lezárt.

## Fontos fájlok

- `README.md`: eredeti futtatási útmutató.
- `SZINTZARASI_KRITERIUMOK.md`: tervezett, jóváhagyandó tesztkapuk.
- `NYITOTT_ADATIGENY.md`: további szükséges adatok.
- `outputs/TRL5_v2_futtatasi_jegyzokonyv.md`: eredeti futtatási jegyzőkönyv.
- `outputs/TRL5_v2_test_results.json`: tesztkimenetek.
- `outputs/reports/`: részletes valósadat-feldolgozási jelentések.
- `outputs/synthetic/` és `outputs/synthetic_real_anchored/`: szintetikus próbák.

## GitHub-feltöltés

A repository főkönyvtárában (ahol `TRL1`–`TRL4` látható) kell feltölteni a ZIP-ből kibontott `TRL5` mappát. Feltöltés előtt ellenőrizd a kutatási eredményállományok megosztási jogosultságát.
