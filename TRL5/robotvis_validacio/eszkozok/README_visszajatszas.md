# T5-08 visszajátszásos mérés – útmutató

A mérés a **valós RobotVis programot** futtatja a **valós cellás CSV-kkel**, robot és áramforrás nélkül. A RobotComm helyére a `04_visszajatszo.py` ül (127.0.0.1:9999), az áramforrás webfelülete helyett pedig ugyanez a program szolgál ki egy helyi teszt-oldalt (127.0.0.1:8000). A RobotVis ezt a beépített `open_local_test_site` módjával olvassa.

Mérőszámok: késés a forrástól a RobotVis-naplóig (pozíció és áramforrás-érték, P50/P95/max), kimaradt értékek, megállás. A naplóidő és a küldési idő ugyanannak a PC-nek az órájából jön.

**Mit nem mér:** a valós robotvezérlő és áramforrás belső késését (ezt a cellás videók becslik), a cellabeli hálózati hibákat.

## Előkészítés (egyszer)

1. Másold le a teljes `RobotVis` mappát (például `RobotVis_teszt` néven). A mérés a másolaton fut, az eredeti érintetlen marad.
2. A másolatban nyisd meg Jegyzettömbbel a `Main.tscn` fájlt. A 10. sor után (`[node name="WeldUnitConnectorBrowser" parent="." instance=ExtResource( 4 )]`) szúrd be ezt a sort, és mentsd:
   ```
   open_local_test_site = true
   ```
3. Tedd egy mappába a `04_visszajatszo.py`, `05_visszajatszas_kiertekelo.py` fájlt és a három visszajátszandó CSV-t (javaslat: `g01_s10.csv`, `g01_s30.csv`, `20_2023-07-12_14-42-8.csv`; ugyanazok, mint a videós mérésnél).
4. Python: a RobotVis-be csomagolt is jó: `RobotVis_teszt\addons\pythonscript\windows-64\python.exe`.

## A mérés (kb. 15 perc; a kezelő NEM a RobotVis fejlesztője)

1. **A RobotComm ne fusson.** Indítsd a visszajátszót (parancssorban, a 3. pont mappájában):
   ```
   <python.exe> 04_visszajatszo.py --csv g01_s10.csv g01_s30.csv 20_2023-07-12_14-42-8.csv
   ```
   Kiírja: „Várom a RobotVis csatlakozását…”.
2. Indítsd el a `RobotVis_teszt\RobotVis.exe`-t. Magától csatlakozik; a visszajátszó kiírja: „RobotVis csatlakozott”.
3. A kezelő a RobotVis-ben bekapcsolja a böngésző-kapcsolatot (Firefox). Megnyílik a „T5-08 visszajátszó – helyi teszt-oldal” lap.
4. **Futásonként:** a kezelő a *Log File Prefix* mezőbe beírja: `futas1` (majd `futas2`, `futas3`), bekapcsolja a *Recording*-ot, a visszajátszó ablakában Entert nyom. A futás kb. 30 s. Ha a visszajátszó kiírja, hogy „kész”, a kezelő kikapcsolja a *Recording*-ot.
5. Közben a kezelő kitölti a jegyzőkönyv 5. pontját (ellenőrzőlista), és lehetőleg képernyővideó is készül.
6. A végén a RobotVis-ben az *Open Logs Folder* gombbal megnyílik a naplómappa: a `futas1_…`, `futas2_…`, `futas3_…` CSV-ket másold a mérés mappájába.

## Kiértékelés

```
<python.exe> 05_visszajatszas_kiertekelo.py --kuldes visszajatszas_naplo\kuldesi_naplo.csv --robotvis "futas*_*.csv" --out T5-08_visszajatszas
```
Kimenet: `T5-08_visszajatszas_riport.md`, futásonkénti és eseményenkénti táblázat. A riport, a `kuldesi_naplo.csv`, a három RobotVis-napló és a jegyzőkönyv kerül a tárolóba (`TRL5/robotvis_validacio/visszajatszas/`).

## Megjegyzések

- A RobotVis képkockánként naplóz; egy képkockán belül érkezett több pozícióból csak az utolsó kerül a naplóba („összevont”, nem adatvesztés).
- Az áramforrás-értékeket a RobotVis a weboldalról olvassa (Selenium). Ha két érték között nem olvas, az érték „kimarad” – ezt külön kell értékelni (a cellás naplókban ugyanez kb. 2 s-os kiesésként látszott, `../naplo_folytonossag/`).
- A programok működését egy szimulált RobotVis-klienssel kipróbáltuk (gyorsított visszajátszás); ez nem mérési eredmény.
