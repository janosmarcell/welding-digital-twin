# TRL 6 – Rendszermodell demonstrálása releváns környezetben

**Állapot:** nem teljesült – terv (lásd `Hegesztesi_DT_TRL6_Leiras.docx`).

**A TRL 5-ből (teljesült, 2026-11-13):**
- a T5-02 jelanomália-detektor ide került (jóváhagyva 2026-11-10);
- **a cellanap előtt kötelező az ívjel-javítás** (`../TRL5/robotvis_validacio/ivjel_javitas_v1/`). A T5-01 1. köre szerint a weboldalról jövő TorchSignal a varratvégeknél kb. 0,5 s-ot késik, a kezelői próba szerint pedig a böngészőablak láthatósága is rontja az adatteljességet;
- a varratvégeket a `szakaszolo_v2.py` a robot megállásából veszi.

**Szerepek (döntés, 2026-11-16; a nevek a beadási csomagban):**
- **Független hegesztési szakértő:** hegesztőmérnök, nem fejlesztő; a T5-07 vak minősítését végzi (keresztmetszetek, darabok). A darabokat véletlen kóddal kapja, sorszám és paraméterek nélkül.
- **Minőségügyi szakértő:** ugyanaz, mint a TRL 5-ben; a kapukat a mérés előtt jóváhagyja, a jegyzőkönyvet ellenjegyzi.
- A két szerepet nem töltheti be ugyanaz a személy. A 2D réteg nem épít YOLO-módszerre.

Ide kerülnek a demonstráció bizonyítékai:

- `validacios_sorozat/` – a 15 hibátlan + 15 zavart darabos valós sorozat: CSV, panorámák (és a 6 nyers felvétel), PLY, gyártási és zavarnapló, szakértői vak minősítés (aláírt).
- `varratszelesseg/` – a T5-03 varratszélesség-validáció (nyers felvétel ↔ panoráma ↔ kézi referencia, mm/px skála).
- `ivjel_javitas_meres/` – az ívjel-javítás előtte–utána mérése (visszajátszás, majd cellanap).
- `kiertekeles/` – a T5-04 … T5-07 és G6-01 … G6-05 kapuk kiértékelése.

A szintetikus bemutató csomag (D) nem kerül ide valós adatként.
