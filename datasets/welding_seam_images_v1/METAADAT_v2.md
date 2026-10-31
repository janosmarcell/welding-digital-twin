# Varratképek metaadatai – teljes JSON-készlet (2026-10-31)

**Forrás:** a `heg\Heg_varratkepek_0…3` mappák (a felhasználó gépén; módosítás dátuma 2025-03-20), a `seam_json.csv` és a `fajllista.csv` alapján (PowerShell-lista, 2026-10-31). A panorámák azonosak a repóban lévőkkel (`seam147_1` ellenőrizve, r = 0,9996).

## Mi változott

- `manifest_v2.csv`: a `welding_seam_images_v1/manifest.csv` bővítése; **mind a 462 varratképhez** kitöltve a beállított áram, feszültség és sebesség az `archive_info.json`-ból (korábban 128-hoz). A korábbi 128 érték változatlan (128/128 egyezik).
- `archive_info_osszes.csv`: a 462 JSON tartalma mappanévvel.

## Ellenőrzés

- A JSON-ban lévő ID minden mappánál egyezik a mappa darabszámával (462/462).
- A sorozat 450 varratképéből (1–150) 447 egyezik a 150 darabos tervvel; a kivétel a **22. darab** 3 képe: a JSON 174 A / 21,7 V, a terv és a CSV (`g01_s22`: 170,8 A / 21,92 V) 171 A / 21,9 V → a JSON-ban elírás; a CSV és a terv a mérvadó.
- **201–207:** a 2023-07-07-i előkísérletek (a szélső beállítások: 40 A / 18 V és 200 A / 23,8 V, 20, 30, 60 és 90 cm/min), nem a 150 darabos sorozat része. Megegyezik a hátoldali feliratos fotókkal (IMG_20230707_105*).
- **500–503:** helyőrző metaadat (500/500/500), tesztképek; nem mérési adat.
- **76. darab:** 6 varratmappa (76_1…76_6), azonos paraméterrel – valószínűleg ismételt fotózás; tisztázandó.
- **Hiányzó darabok:** 44, 121, 125, 130, 135, 140, 145, 150 a teljes exportban sincs meg → a 2023-as fotózáskor nem készült róluk kép.
- **Nyers felvételek:** 752 mappa (a 462 varrat egy része több részmappában), ebből 409-ben 6 nyers kép (`saved_image_1…6`); a TRL6 varratszélesség-validációhoz.
- **`models` mappák:** 2024 novemberi gépi tanulásos modellek (CNN és kNN „intensity” modellek, `welding_model*.keras`); eredetük és a hozzájuk tartozó munka tisztázandó (TRL3–4 előzmény?).

## Hatás az 1. cikkre

- 7. ábra (kép–CSV hozzárendelés): **n = 425 varrat, r = 0,993** (korábban n = 113, r = 0,994); ±5 darab eltolásnál r = 0,26.
