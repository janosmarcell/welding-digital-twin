# T5-01 – az eseményfelismerés vak annotációja

**Kapu (jóváhagyási lap, 2026-11-10):** 20 véletlen naplón (60 varrat, 120 esemény) egy esemény egyezik, ha az annotált és az automata sor legfeljebb **±1 sorral** tér el; feltétel: **pontbecslés ≥ 99%**. Annotátor: A1 (nem fejlesztő; a név a beadási csomagban). Az automata a varratok kezdetét és végét jelöli.

## Eredmény: a T5-01 a 2. körben teljesül

| Kör | Dátum | Automata | Minta | Eredmény (±1 sor) | Státusz |
| --- | --- | --- | --- | --- | --- |
| 1. | 2026-11-11, 14:08–15:20 | **v1** (vég = TorchSignal 1→0) | seed 2026; 20 napló + g02_s33 (tájékoztató) | 87/119 = **73,1%** (Wilson 0,645–0,803) | **nem teljesült** – hivatalos |
| 1. (utólag) | – | v2 | ugyanaz | 116/119 = 97,5% | csak tájékoztató: a v2 az 1. kör adatainak ismeretében készült |
| 2. | 2026-11-11, 18:28–19:06 | **v2** (vég = a robot elindulása előtti sor) | seed 2027; 20 új napló (kizárva: az 1. kör, a videós, a visszajátszott és a kezelői próba naplói) | 120/120 = **100%** (Wilson 0,969–1,000) | **teljesül** – hivatalos |

## Mit talált az 1. kör, és mi lett a javítás

- A kezdetek jól egyeztek (60/60 ±2 soron belül). A varratvégeknél az annotátor rendszeresen 2–6 sorral korábbra jelölt, mint a v1 (medián −2).
- Az ok: a v1 a véget a TorchSignal 1→0 váltásához tette. A TorchSignal az áramforrás weboldaláról jön, és kb. 0,5 s-ot késik; ezt a T5-08 mérés is mutatja (az áramforrás-érték P95 késése ≤ 465 ms, ez kb. 4–5 sor). Az annotátor a robot megállását, vagyis a valós ívoltást jelölte.
- A javítás: a **v2** (`../eszkozok/szakaszolo_v2.py`) a véget a robot elindulása előtti sorhoz teszi. Elindulásnak az számít, ha a lépésköz két egymást követő sorban legalább 0,5 mm. A kezdet változatlan.
- A v2-t **lefagyasztottuk, mielőtt kiértékeltük volna** (commit `08c5c4a`, 2026-11-11 17:09). A 2. kör kulcsának SHA-256-ját a 2. annotáció előtt feltöltöttük (`kor2_KULCS_SHA256_lefagyasztva.txt`, commit `3a387a8`, 17:10). A kiértékeléskor a kulcs egyezett vele.
- A 2. körben az annotátor ugyanazt az útmutatót és sablont kapta; az 1. kör eredményéről nem tájékoztattuk.

## A v2 a teljes adatsoron (2026-11-13)

A v2-t mind a 150 naplóra lefuttattuk (`datasets/derived/seam_segments_v2.csv`, 449 szakasz). 444 szakasznál a v2-vég legfeljebb 8 sorral korábbi a TorchSignal-végnél (medián 1 sor). **5 szakasznál a v2 túl korán zár** (g02_s33 1., g03_s61 3., g03_s66 2., g05_s124 1., g05_s136 2.). Az ok vagy egy naplókiesés, vagy az, hogy nagy sebességnél egy-egy sorközben a lépésköz ≥ 0,5 mm. Ezek a szakaszok nem voltak a 2. kör mintájában, ezért a T5-01 eredményét nem érintik. A táblában `qc_flag` jelöli őket, a szabályt (például időalapú küszöbbel) a TRL 6-ban kell javítani.

## Ismert adatok

- **g02_s33** (1. kör, tájékoztató): 2,5 s-os naplókiesés az 1. és 2. varrat között; az annotátor is 2 szakaszt látott, és egyezett az automatával.
- **g05_s136** (1. kör): a naplókiesés a 2. varrat végére esik; az annotátor „nem egyértelmű”-nek jelölte.
- **g01_s03** (2. kör): 1,9 s-os naplókiesés az 504. sornál; nem okozott eltérést.

## Fájlok

- `kor1_2026-11-11_v1/`: az annotáció (A1), a v1 kulcs és riport (hivatalos), a v2 kulcs és riport (TÁJÉKOZTATÓ).
- `kor2_2026-11-11_v2/`: az annotáció (A1), a v2 kulcs, a riport és az eredménytábla.
- A naplók: `datasets/welding_experiments_v1/`. Az ábrák és a vak CSV-k az `01_annotacios_lap_keszito.py`-vel újra előállíthatók:
  - 1. kör: `--seed 2026 --szakaszolo v1`;
  - 2. kör: `--seed 2027 --szakaszolo v2 --g02s33 nem` és a kizárási lista; lásd a végrehajtói teendőlistát a beadási csomagban.
