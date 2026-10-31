# Ívjel-javítás v1 – RobotComm + RobotVis (tervezet, cellában még nem próbált)

**Kiinduló forrás:** `DigitalTwin1.5/Source` (RobotComm 2023-06-26, RobotVis 2023-06-27). A lefordított változat ezzel azonos; a `.gdc` visszafejtésével és bájtszintű összevetéssel ellenőrizve.

## A hiba oka (a forrásból)

- A **RobotComm** (`Program.cs`) végtelen ciklusban kérdezi a Yaskawa robot pozícióját HSE-n, és minden választ továbbküld a RobotVis-nek (`X,Y,Z,Rx,Ry,Rz;`). Ívjelet nem küld.
- A **RobotVis** (`Connector.gd`) minden beérkező pozícióhoz hozzáfűzi az áramforrás-weboldalról utoljára olvasott TorchSignal, U, I és huzalsebesség értéket. A sort csak akkor írja ki, ha eltér az előzőtől (`last_stored_line`): ez szüntette meg a régi, álló robotnál keletkező tömeges sorokat.
- Az áramforrás-oldalt a `WeldUnitConnectorBrowser.py` olvassa Seleniummal, minden képkockában négy külön lekérdezéssel. Ha egy olvasás tovább tart, mint az ívszünet (medián 415 ms), a szünet nem kerül a naplóba.
- **Mellékelt lelet:** a forrásban van egy félbehagyott, közvetlen **WebSocket**-kapcsolat az áramforráshoz (`weld_unit_connector/WeldUnitConnector.gd`, `wss://10.192.70.129/WSspeedNet`, bejelentkezéssel). Nincs bekötve a `Main.tscn`-be, és csak kiírja a kapott adatot. Később ebből lehet a feszültség, az áram és a huzalsebesség gyors útja.

## A javítás

1. **RobotComm** (`RobotComm/Program.cs`):
   - Két új, nem kötelező kapcsoló: `--arc-io <logikai szám>` és `--arc-bit <0..7>`. Ha meg vannak adva, minden pozíció után a már meglévő `HSEClient.IORead`-del kiolvassa a robot ívjel-bemenetét, és 7. mezőként küldi (`1` = ív, `0` = nincs ív, `-1` = olvasási hiba).
   - Kapcsolók nélkül pontosan a régi 6 mezős üzenet megy, tehát visszafelé kompatibilis.
2. **RobotVis** (`RobotVis/connector/Connector.gd`):
   - A 6 és a 7 mezős üzenetet is elfogadja. Ha van robot-ívjel, a `TorchSignal` abból jön, különben a weboldalról, mint eddig.
   - Két új oszlopot naplóz:
     - `TorchSignalWeb`: a weboldal jele, hogy egy futáson belül összevethető legyen a két út;
     - `TorchSource`: `robot`, `web` vagy `manual`.
   - **Életjel:** azonos sort is kiír 1 s-onként, így a naplókiesések (mint a `g02_s33`-ban) közvetlenül látszanak. Változáskor azonnal ír, ezért a fájl nem lesz nagy.
3. **Visszajátszó** (`04_visszajatszo.py`): új `--ivjel` kapcsoló, amely a javított RobotComm üzenetét szimulálja (7. mező). Tesztelve: a `g01_s05` visszajátszásakor mind az 1208 üzenet 7 mezős, a 3 varrat 6 ívváltása mind megvan.

A `*.diff` fájlok soronként mutatják a változást; az eredeti fájlok az `eredeti/` mappában vannak.

## Ami még kell

- [ ] **A cellából:** melyik robotbemenetre érkezik az ívjel (Fronius „Current flow” vagy „Arc stable” a RI FB INSIDE/i interfészen). Ez a Yaskawa I/O-logikai szám és bit, az integrátor vagy a tanítópanel I/O-monitora megmondja.
- [ ] A RobotComm lefordítása (.NET 7, `dotnet build`). Itt nem fordítottam le, mert nincs fordító a környezetben; a módosítás csak a már meglévő `IORead` hívást használja.
- [ ] A RobotVis exportja a módosított `Connector.gd`-vel (Pandemonium-szerkesztőben).
- [ ] Mérés: visszajátszás a régi és a javított változattal (≥ 10–10 futás, `--ivjel` nélkül és vele). Ehhez a kiértékelőt (`05_…`) bővítem, hogy a pisztolyjelet és a feszültség/áram értékeket külön párosítsa.
- [ ] Cellában: a zavart sorozat gyártásakor a javított változat fusson; az `IORead` többletidejét (pozíciónként egy plusz HSE-kérés) a napló sűrűségén ellenőrizni kell.
