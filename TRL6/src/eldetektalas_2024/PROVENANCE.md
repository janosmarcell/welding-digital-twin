# Provenance: 2D éldetektálási kísérletek (2024)

**Állapot:** feltáró munka, nem validált mérés. A fájlok byte-ra azonosak a szerző által küldött `Downloads.zip` tartalmával (érkezett 2026-11-20; SHA-256 `ef2a9fabf72cedd40d2d3b805f16504f03452e0d76a4fada65899c75c7b4c371`). Ezek Jupyter-ellenőrzőpont (`-checkpoint`) fájlok; az eredeti notebookok nincsenek meg.

## Mit csinálnak

A varratpanorámákon (OpenCV, SciPy):
- Gauss-elmosás, **Canny**-éldetektálás (50/150, illetve 100/150), **Roberts**-operátor;
- küszöbölés, morfológiai nyitás, kontúrkeresés terület- és arányszűréssel; a kontúrok befoglaló téglalapjának mérete **pixelben** (`pixelben2`, `Untitled2`);
- távolság-transzformáció az éltérképen (`eltavolsag`), kontúr-középpontok távolsága (`panorama1`);
- Hough-vonalkeresés.

**Korlát:** a szélesség csak pixelben van, mm/px skála és kézi referencia nélkül; értékelés nincs. A T5-03 / G6-04 (2D varratszélesség a keresztmetszethez mérve) kiindulópontja lehet, de bizonyítéknak nem az.

## Megjegyzések

- A ZIP-ben a `panorama_30_as alkatrész.jpg` byte-ra azonos a tárolóban már meglévő `datasets/welding_experiments_v1/g01_30/g01_s15.jpg` képpel (a 30 cm/perces csoport 15. darabja), ezért nem másoltuk újra.
- A `panorama.jpg` (6020 × 2113) és az `image_4.jpg` (3840 × 2160) a `kepek/` mappában van; hogy melyik darabról készült, nincs rögzítve.
- Az `éltavolság-checkpoint.ipynb` fájlnév ékezet nélkül, `eltavolsag-checkpoint.ipynb` néven szerepel. A `panorama1` és az `Untitled1` tartalma azonos. Négy üres (72 bájtos) `Untitled*-checkpoint` fájlt nem vettünk át.
- A notebookok a szerző gépén lévő `c:/users/hj/downloads/eszes2/1/` mappából olvasnak.

## Fájlok

A dátum a ZIP-ben tárolt módosítási idő (2024-10-01, a szerző gépének helyi ideje); nem hitelesített, és nem TRL-elfogadási dátum.

| Fájl | Bájt | SHA-256 |
|---|---:|---|
| `notebooks/Untitled1-checkpoint.ipynb` | 3112 | `e258ab91b21c7723d7223da9fc1cb819584541eea249566eae74913d55b8217f` |
| `notebooks/Untitled2-checkpoint.ipynb` | 3772 | `c3f1191da82460743d674143787c75873f8485c0e0cb5b4e86fd7bc7a88fe441` |
| `notebooks/Untitled3-checkpoint.ipynb` | 626598 | `249816319df2e76111020703313f706b4dc8ff337c7e92c9059e14932c63be02` |
| `notebooks/eltavolsag-checkpoint.ipynb` | 872168 | `567626c649f6a64f0a2fee943a19429da22560c8963f76e3a3467f3b85d9c1d7` |
| `notebooks/panorama1-checkpoint.ipynb` | 3112 | `e258ab91b21c7723d7223da9fc1cb819584541eea249566eae74913d55b8217f` |
| `notebooks/pixelben2-checkpoint.ipynb` | 2905 | `3f33114b2aa86a76041924fe86a6513896e71262a4c0be54f51de3904d139b9c` |
| `kepek/image_4.jpg` | 1044624 | `c53a77289a1b6b08fc4e37ee2befbbcacd603f9b1d3c552060ce35c63d89d05a` |
| `kepek/panorama.jpg` | 2164784 | `e0ae1d4bbbd3ac3c27bf19d9fb2cc90a7cb48070aa7ee92887d267fbb7febdaa` |
