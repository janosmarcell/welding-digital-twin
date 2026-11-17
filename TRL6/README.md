# TRL 6 – Rendszermodell demonstrálása releváns környezetben

**Állapot:** nem teljesült – terv (egyszerűsítve 2026-11-17; lásd `Hegesztesi_DT_TRL6_Leiras.docx` a beadási anyagban).

**A TRL 5-ből (teljesült, 2026-11-13; aláírva 2026-11-17):**
- a T5-02 jelanomália-detektor ide került (jóváhagyva 2026-11-10);
- **a cellanap előtt kötelező az ívjel-javítás** (`../TRL5/robotvis_validacio/ivjel_javitas_v1/`). A T5-01 1. köre szerint a weboldalról jövő TorchSignal a varratvégeknél kb. 0,5 s-ot késik, a kezelői próba szerint pedig a böngészőablak láthatósága is rontja az adatteljességet;
- a varratvégeket a `szakaszolo_v2.py` a robot elindulásából veszi; az 5/449 túl korai zárás miatt a cellanap előtt időalapú küszöb kell.

**Szerepek (döntés, 2026-11-16; a nevek a beadási csomagban):**
- **Független hegesztési szakértő:** hegesztőmérnök, nem fejlesztő; a T5-07 vak minősítését végzi (keresztmetszetek, darabok). A darabokat véletlen kóddal kapja, sorszám és paraméterek nélkül.
- **Minőségügyi szakértő:** ugyanaz, mint a TRL 5-ben; a kapukat a mérés előtt jóváhagyja, a jegyzőkönyvet ellenjegyzi.
- A két szerepet nem töltheti be ugyanaz a személy. A 2D réteg nem épít YOLO-módszerre.

## A terv (egyszerűsítve, 2026-11-17)

A demonstráció három része:

| Rész | Mit mutat be |
| --- | --- |
| **A. Cellanap (élő)** | a TRL 5 javításaival (ívjel a robot I/O-jából, szakaszoló v2 időalapú küszöbbel) egy nem fejlesztő kezelő élőben futtatja a rendszert; kb. 6 hibátlan + 4 szándékosan zavart darab |
| **B. Cella nélkül** | a 2023-as, a varratok közepén elvágott darabokon a vágási felület (valós keresztmetszet) a referencia a 2D- és 3D-mérésnek; a független szakértő vakon minősít; 15 darabos rács (5 sebesség × 3 áram) |
| **C. Integrált bemutató** | napló → 2D → 3D → riport egy darabazonosítóval; hiányos adatnál „ELLENŐRIZENDŐ”, automatikus OK nélkül |

Javasolt kapuk (jóváhagyandó, a mérések előtt):

| Kapu | Feltétel (javaslat) |
| --- | --- |
| G6-01 élő adatrögzítés | minden ívjel-váltás a naplóban; P95 ≤ 2 s; nincs > 2 s megállás |
| G6-02 varrathatárok | ±1 sor, pontbecslés ≥ 99% független vak annotációval |
| G6-03 zavar jelzése | mind a 4 zavart darab „ELLENŐRIZENDŐ”; legfeljebb 1 téves jelzés |
| G6-04 2D/3D a keresztmetszethez | varratszélesség-eltérés a vágási felülettől a rögzített határon belül (javaslat: medián ≤ 0,5 mm) |
| G6-05 nincs hamis OK | a szakértő által hibásnak minősített darab nem kap automatikus OK-t |

Kikerült (TRL 7-re vagy későbbre): a 15 + 15 darabos sorozat, a küszöb-érzékenységi görbe független teszten, az ismételt szkennelés szórása, az új geometria, az IEC 62264-1 interfész.

## Mappák (a demonstráció bizonyítékai)

- `cellanap/` – az A rész: naplók (ívjel robot és web), zavarnapló, annotáció, kezelői lap.
- `szetvagott_darabok/` – a B rész: darabonként a vágási felület és a felülnézet fotója méretreferenciával, a szkenek, a szakértő vak minősítése (kóddal).
- `integralt_bemutato/` – a C rész riportjai.
- `kiertekeles/` – a G6-01 … G6-05 kiértékelése és a jegyzőkönyv szövege.

A szintetikus bemutató csomag (D) nem kerül ide valós adatként.
