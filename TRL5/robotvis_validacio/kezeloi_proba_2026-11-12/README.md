# Kezelői próba – 2026-11-12, 19:52–20:03

**Eredmény: teljesül, dokumentált korláttal.** A minőségügyi szakértő 2026-11-13-án elfogadta (jegyzőkönyv 7. pont).

- **Kezelő:** nem a RobotVis fejlesztője, és nem az annotátor. **Végrehajtó:** figyelt, nem segített. A nevek és az aláírt kezelői lap (AVDH, 2026-11-12 21:02) a beadási csomagban vannak.
- **Mód:** visszajátszás robot és áramforrás nélkül. Három cellás napló: g02_s45, g03_s65, g05_s125 (futas1–3). RobotVis 2023-06-27-i build, `open_local_test_site = true`. Gép: i5-1235U, 16 GB, Windows 64 bit, Firefox 153.0.3.
- **Ellenőrzőlista:**
  - 1., 2., 4. pont: igen;
  - 3. pont: igen/részben – „a pipa nem minden varratnál váltott”;
  - 5–6. pont: nem tesztelt;
  - 7. pont (érthetőség): 5/5;
  - 8. pont: igen.
- **T5-08 (`05_visszajatszas_kiertekelo.py`):** a pozíciónapló minden futásban teljes (927/774/584 sor). A pozíció P95-öse 71–117 ms, az áramforrás-értékeké 434–802 ms, megállás nem volt. A kapu (P95 ≤ 2 s) teljesül.
- **Adatteljesség (korlát):** a TorchSignal-váltások közül a naplóba 1/6, 2/6, illetve 4/6 került; az áramforrás-értékek 66/89, 52/71, illetve 38/54 arányban maradtak ki. Ok: a Firefox-ablak (áramforrás-oldal) a háttérben volt, ezért az oldal olvasása lassabb volt, mint a 2026-10-30-i mérésen. Ez ugyanaz az elfogadott korlát; a javítás (ívjel a robot I/O-ból) a TRL 6 előtt kerül be. Tanulság: a RobotVis jelenlegi felépítése érzékeny arra, hogy a böngészőablak látható-e.

Fájlok: a három RobotVis-napló, a küldési napló, a `meta.json`, valamint a kiértékelő kimenete (`T5-08_visszajatszas_*`).
