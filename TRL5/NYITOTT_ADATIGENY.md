# TRL 5 – ami a lezárásig hiányzik (2026-10-31)

A hatókör és a kapuk: [`SZINTZARASI_KRITERIUMOK.md`](SZINTZARASI_KRITERIUMOK.md) (v3). A mérésekből már nem hiányzik semmi; a hátralévő lépések emberi lépések.

| # | Lépés | Ki | Bemenet | Kimenet |
| --- | --- | --- | --- | --- |
| 1 | ✅ **Kész (2026-11-10).** A jóváhagyási lap kitöltése és aláírása (hatókör, T5-02 áthelyezése, a T5-01 feltétele, az adatteljesség mint korlát, szereplők) | projektvezető, minőségügyi szakértő | a TRL 5 dokumentáció melléklete | aláírt lap, a 2–3. lépés előtti dátummal |
| 2 | ✅ **Kész (2026-11-11), teljesül: 2. kör 120/120.** T5-01 vak annotáció: 21 napló, 63 varrat kezdő- és zárósora | annotátor (nem fejlesztő) | `T5-01_ANNOTATORNAK` csomag (a kulcs nélkül) | kitöltött annotációs lap |
| 3 | ✅ **Kész (2026-11-12), teljesül, dokumentált korláttal.** Kezelői próba visszajátszásos módban (kb. 30 perc, robot nélkül) | kezelő (nem fejlesztő, nem az annotátor), végrehajtó figyel | a kezelői próba forgatókönyve | 3 futás naplója, kitöltött ellenőrzőlista |
| 4 | ✅ **Kész.** Záró kiértékelés: `python robotvis_validacio/eszkozok/06_trl5_zaras.py …` | végrehajtó | a 2–3. lépés kimenete | `TRL5_ZARO_RIPORT.md`, kapunkénti döntés |
| 5 | ✅ **Kész (2026-11-13).** A jegyzőkönyv kitöltése és aláírása | végrehajtó, kezelő, minőségügyi szakértő | a 4. lépés riportja | aláírt jegyzőkönyv |
| 6 | Feltöltés: annotáció, kulcs, riportok a tárolóba; a TRL 5 leírás és az Excel frissítése | végrehajtó | | |

## Már nem TRL 5-feladat

A v2 (2026-10-16) adatigényei közül a következők a TRL 6-ba kerültek: valós varratminősítés munkadarab-azonosítóval (T5-07), referencia- és hibás 3D pontfelhő-pár (T5-04, T5-05), a 2D képek mm/px referenciája (T5-03), a jelanomália-detektor valós zavart darabokon (T5-02). Lásd `TRL6/`.

## Ismert, dokumentált tételek

- A `g02_s33` naplóban két aktív szakasz van: az ok egy kb. 2 s-os naplókiesés (`robotvis_validacio/naplo_folytonossag/`), nem gyártási hiba. A T5-01 mintában tudatos kivételként szerepel.
- Az ismétlődő időbélyegek és az áramforrás-értékek ritka frissülése a RobotVis felépítéséből adódik (forráskód-elemzés: `robotvis_validacio/ivjel_javitas_v1/`); TRL 5-ben dokumentált korlát.
