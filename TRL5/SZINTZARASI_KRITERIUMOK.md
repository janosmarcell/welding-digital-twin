# TRL 5 szintzárási kritériumok – v3 (2026-10-31, jóváhagyandó)

**Ez a változat felváltja a 2026-10-16-i v1-et.** A kapuk javaslatok: a projektvezető és a minőségügyi szakértő a jóváhagyási lapon (a TRL 5 dokumentáció melléklete) rögzíti őket, **a T5-01 kiértékelése és a kezelői próba előtt**. Az értékek nem az ISO 5817 követelményei.

## Hatókör

A TRL 5 a **folyamatadat-rétegre** vonatkozik (RobotComm, RobotVis: robotpozíció és áramforrás-adatok gyűjtése, kijelzése, naplózása a valós robotcellában).

| Réteg | Kapu | Hová tartozik |
| --- | --- | --- |
| Folyamatadat (RobotComm, RobotVis) | T5-01, T5-08, kezelői próba | **TRL 5** |
| Jelanomália-detektor | T5-02 | TRL 6 (javasolt áthelyezés: csak valós zavart darabokon igazolható, ezek a TRL 6 cellanapján készülnek) |
| 2D varratkép | T5-03 | TRL 6 |
| 3D pontfelhő (FGR–ICP–DBSCAN) | T5-04, T5-05, T5-07 | TRL 6 |
| CSV–2D–3D hozzárendelés | T5-06 | TRL 6 |

A képi és a 3D réteg a TRL 4 szinten marad, amíg a TRL 6 kapui nem teljesülnek. A T5-02 … T5-07 kapuk megfogalmazása a `TRL6/` dokumentációban szerepel; az itteni v1-táblázat ezekre már nem érvényes.

## Zárókapuk

| Kapu | Mérőszám | Feltétel (javaslat) | Állapot (2026-10-31) | Bizonyíték |
| --- | --- | --- | --- | --- |
| **T5-01** eseményfelismerés | A vakon, kézzel annotált kezdő- és záróesemények aránya, amelyeket az automatikus szakaszolás legfeljebb 1 sor eltéréssel talál meg | Annotálva 21 napló, 63 varrat; **a kapu a 20 véletlen naplón** (60 varrat, 120 esemény) számolódik, a g02_s33 (ismert, 2,5 s-os naplókiesés: az automata az 1–2. varratot egy szakasznak látja) tájékoztató jelleggel, külön; a jóváhagyási lapon választandó: (a) pontbecslés ≥ 99% **vagy** (b) Wilson 95% CI alsó határa ≥ 95%; minden kivétel listázva | **Nyitott:** az annotációs csomag kész, az annotáció hiányzik. A szerkezeti ellenőrzés kész (151 napló, B) | `robotvis_validacio/eszkozok/01–02_*`, később `robotvis_validacio/annotacio_T5-01/` |
| **T5-08** streaming késleltetés | A forrástól a naplóig, illetve a CSV-időbélyegtől a kijelzésig tartó késés; adatvesztés; megállás | P95 ≤ 2 s minden futásban; ≥ 3 ismételt futás; az adatvesztés és a megállások megadva | **Teljesül (B):** visszajátszás 3 futás: pozíció P95 ≤ 85 ms, áramforrás-érték P95 ≤ 465 ms, megállás 0; 15 cellás videó (5 sebességcsoport, 57 esemény): felső becslés ≤ kb. 0,88 s | `robotvis_validacio/visszajatszas_2026-10-30/`, `robotvis_validacio/video_*_darab/`, `T5-08_video_osszesites.md` |
| **Kezelői próba** | Egy nem fejlesztő kezelő a forgatókönyv szerint, segítség nélkül végigviszi a visszajátszásos futást | Az ellenőrzőlista 1–4. pontja „igen”, a 7. pont (érthetőség, 1–5) legalább 3; a futások naplója megvan | **Nyitott:** a forgatókönyv kész, a próba hiányzik | később `robotvis_validacio/kezeloi_proba_<dátum>/` |

### Dokumentált korlát (nem kapu)

**Adatteljesség:** a RobotVis az áramforrás-értékeket a weboldalról olvassa, ezért a naplóban kb. 0,25–1 s-onként változnak (a forrás kb. 0,23 s-onként); a visszajátszásban 18 TorchSignal-váltásból 1 (egy kb. 0,45 s-os ívszünet) nem került a naplóba. Az ok a forráskódból azonosítva; a javítás (ívjel a robot I/O-ból, `robotvis_validacio/ivjel_javitas_v1/`) a TRL 6 előtt kerül be, és ott mérendő. A jóváhagyási lapon elfogadandó korlátként.

## Szerepek

| Szerep | Feltétel |
| --- | --- |
| Végrehajtó (próbavezető) | kezeli a T5-01 kulcsát, futtatja a kiértékelést, kitölti a jegyzőkönyv mért részeit |
| Annotátor | nem fejlesztő; nem látta a TorchSignalt, a kulcsot, a visszajátszott és a videón szereplő naplókat |
| Kezelő | nem a RobotVis fejlesztője; nem az annotátor |
| Projektvezető | jóváhagyja a hatókört és a kapukat |
| Minőségügyi szakértő | független a végrehajtótól; jóváhagyja a kapukat, ellenjegyzi a jegyzőkönyvet |

## A szint lezárása

A TRL 5 akkor jelölhető lezártnak, ha:

1. a jóváhagyási lap aláírva, a kiértékelések előtti dátummal;
2. a T5-01, a T5-08 és a kezelői próba a jóváhagyott feltétel szerint teljesül (a `robotvis_validacio/eszkozok/06_trl5_zaras.py` riportja szerint);
3. a jegyzőkönyv kitöltve és aláírva (végrehajtó, kezelő, minőségügyi szakértő);
4. a nyers naplók, a riportok és az ellenőrzőösszegek a tárolóban vannak (az aláírt példányok a beadási csomagban, nem a nyilvános tárolóban).

## Változatok

- v1 (2026-10-16): mind a nyolc kapu (T5-01 … T5-08) a TRL 5-ben.
- v3 (2026-10-31): a hatókör a folyamatadat-rétegre szűkítve; T5-02 … T5-07 a TRL 6-ba; a T5-01 feltétele választható; kezelői próba külön kapuként; T5-08 mérve.
