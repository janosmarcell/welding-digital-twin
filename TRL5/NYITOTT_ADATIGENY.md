# A TRL5 végleges igazolásához még szükséges

1. **Valós varratminősítés munkadarabazonosítóval**: jó/hibrid/hibás szakértői címke a releváns szabványértékek, vizuális/NDT vizsgálatok és hibatípusok rögzítésével; kézzel jóváhagyott hozzákapcsolás a CSV / JPG / PLY állományokhoz.
2. **Legalább egy hiteles referencia 3D pontfelhő + hibás darab pár** ugyanazzal a geometriai koordinátarendszerrel vagy dokumentált illesztési lehetőséggel, FGR + ICP ellenőrzéshez. Ismételt szkennelés mérési szórással.
3. **2D képek referenciaadata**: mm/px, kézi kontúr vagy más mért varratszélesség, kamerabeállítás és világítás.
4. **Releváns robotcellás demonstráció**: időbélyegzett robotkommunikációs log, feldolgozási és kijelzési késleltetés, kezelői visszajelzés.
5. **Előre jóváhagyott mérési kapuk**: hibatípusonkénti követelmény és mintaméret; a statisztikai hibahatárt is dokumentálni kell.

A `g02_s33` két aktív TorchSignal-szakaszát külön vizsgálni szükséges (nem automatikusan gyártási minőségi hiba). A sok ismétlődő időbélyeg miatt a mérés időfelbontását a vezérlő és loggoló oldalon tisztázni kell.
