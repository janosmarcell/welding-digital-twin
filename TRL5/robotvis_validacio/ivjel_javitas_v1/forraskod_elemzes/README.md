# Forráskód-elemzés (2026-10-31)

- `gdc_decode.py`: a RobotVis lefordított GDScript-fájljainak (`.gdc`, GDSC v13, Pandemonium-tokenkészlet) visszafejtője. Csak olvasásra, a változatok összevetéséhez.
- `build_2023-06-27_Windows_*.gd`: a 2023-06-27-i Windows-build (a felhasználó „félévvel korábbi” csomagja) visszafejtve.
- `build_RobotComm-zip_*.gd`: a visszajátszásos méréshez használt build visszafejtve.

**Eredmény:** a két build bájtra azonos (Connector, GUI, WeldUnitConnector, RobotIK `.gdc`, `Main.tscn`, `project.binary`, `WeldUnitConnectorBrowser.py`; a RobotComm.dll is). A fejlesztői forrás (DigitalTwin1.5/Source: RobotComm 2023-06-26, RobotVis 2023-06-27) ezzel egyezik; a `project.pandemonium` szerint `low_processor_mode = true`.

**A 2023-06-26-i és korábbi naplók** (a felhasználótól, 2026-10-31): a június 6–16-i naplók csak pozíciót tartalmaznak, kb. 17 ms-onként (képkockánként); a 2023-06-26-iak már hegesztési adatot is (`WeldSpeed` oszlopnév), kb. 57 ms-onként; a júliusi sorozat kb. 112 ms-onként. A „nagy CSV” változat forrása nem áll rendelkezésre.

A fejlesztői forrás (Source.zip) harmadik fél kódja; a tárolóba csak a módosított két fájl és az eltérések kerülnek (`../RobotComm`, `../RobotVis`, `../*.diff`).
