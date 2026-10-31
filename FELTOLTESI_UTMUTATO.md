# GitHub-feltöltés – 2026-10-31

**Tároló:** https://github.com/janosmarcell/welding-digital-twin (ellenőrizve az `origin/main` 0a40100 commitján, 805 fájl).

A csomag mappaszerkezete a tárolóét követi: a tartalmát a tároló gyökerébe kell másolni (a meglévő mappákba olvad), majd GitHub Desktopban commitolni.

## 1. Új fájlok (ebből a csomagból)

| Hova | Mi | Miért |
| --- | --- | --- |
| `TRL5/robotvis_validacio/video_40_darab … video_150_darab/` | 12 cellás videó riportja és eseménytáblája | T5-08: 15 videó, 5 sebességcsoport |
| `TRL5/robotvis_validacio/T5-08_video_osszesites.md` | Frissített összesítés (15 futás) | **felülírja** a régit |
| `TRL5/robotvis_validacio/eszkozok/` | A mérőeszközök (annotáció, késés, visszajátszó `--ivjel` kapcsolóval, kiértékelő) | a dokumentumok erre hivatkoznak, a tárolóból eddig hiányzott |
| `TRL5/robotvis_validacio/eszkozok_video/` | A videós kiértékelés szkriptjei | reprodukálhatóság |
| `TRL5/robotvis_validacio/ivjel_javitas_v1/` | Ívjel-javítás (RobotComm, RobotVis), eltérések, forráskód-elemzés | TRL5/TRL6, 2. cikk |
| `TRL5/robotvis_validacio/visszajatszas_2026-10-30/` | A visszajátszás 8 fájlja almappában | a dokumentumok ezt az elérési utat idézik |
| `datasets/welding_seam_images_v1/manifest.csv` | Bővített manifest: mind a 462 képhez paraméter | **felülírja** a régit (a régi 128 érték változatlan) |
| `datasets/welding_seam_images_v1/archive_info_osszes.csv`, `METAADAT_v2.md` | A 462 JSON és a leírás | forrás és ellenőrzés |
| `datasets/welding_experiments_v1/docs/` | Kísérleti terv (CSV) és az eredeti `Hegesztesi_adatok_20230710.xlsx` | az 1. cikk Methods része, 150/150 egyezés |
| `tools/trl_recompute/` | A B osztályú számok újraszámolója | az xlsx erre hivatkozik, eddig hiányzott |
| `TRL6/README.md`, `TRL7/README.md` | A szintmappák | az xlsx TRL6/TRL7 linkje csak így működik |

## 2. Áthelyezendő (GitHub Desktopban kézzel)

A `TRL5/robotvis_validacio/` **gyökeréből törlendő** ez a 8 fájl, mert a `visszajatszas_2026-10-30/` almappába kerültek (tartalmuk azonos):
`RIPORT_osszefoglalo.md`, `T5-08_visszajatszas_esemenyek.csv`, `T5-08_visszajatszas_futasok.csv`, `T5-08_visszajatszas_riport.md`, `futas1_…csv`, `futas2_…csv`, `futas3_…csv`, `kuldesi_naplo.csv`.
A GitHub Desktop a törlést és az új helyet együtt „átnevezésként” mutatja.

## 3. Nem kerül a tárolóba

- **A videók (mp4):** a `.gitignore` kizárja őket (`*.mp4`), és a `Paraméterek_Fronius.mp4` 230 MB-os (a GitHub-korlát 100 MB). A riportokban az SHA-256 szerepel; az mp4-ek helye: OneDrive / Zenodo (az 1–2. cikk adattárával együtt).
- **A fejlesztői forrás (`Source.zip`, `Windows*.zip`):** harmadik fél kódja, 100 MB körül; csak a két módosított fájl és az eltérések kerülnek be.
- **A beállítás-fotók (`Képek_beállítás.zip`, 23 kép, 78 MB):** javaslat: `TRL4/evidence/beallitas_fotok/` – opcionális, külön commitban.
- **A nyers képexport (`Heg_varratkepek_0…3`, 6 nyers felvétel varratonként, `models`):** a TRL6 varratszélesség-validációnál kerül sorra.
- **A szintetikus bemutató csomag** (`WDT_validacios_sorozat_SZINTETIKUS_v0`): D osztály, nem kerül valós adatként a tárolóba.

## 4. Párhuzamosság-ellenőrzés (dokumentumok ↔ tároló)

| Ellenőrzés | Eredmény |
| --- | --- |
| Az xlsx összefoglaló lap linkjei (9) | az 1. pont után mind él |
| A TRL1–TRL5 lapok GitHub-linkje | él |
| A TRL6/TRL7 lapok GitHub-linkje | a `TRL6/`, `TRL7/` mappa létrehozása után él |
| A melléklet `TRL5_robotvis_validacio/` 79 fájlja | 71 már a tárolóban vagy ebben a csomagban; az `eszkozok/` 8 fájlja eddig hiányzott → most a csomagban |
| `tools/trl_recompute/` | eddig hiányzott → most a csomagban |
| `TRL5/outputs/synthetic*` | a tárolóban van; D osztály, a dokumentumok így is jelölik |

## Javasolt commit-üzenetek

1. `T5-08: 12 további cellás videó (40–150) és összesítés`
2. `TRL5: mérőeszközök, videós szkriptek; visszajátszás almappába`
3. `TRL5: ívjel-javítás v1 és forráskód-elemzés`
4. `datasets: teljes képmetaadat (462 JSON) és kísérleti terv`
5. `tools: trl_recompute; TRL6, TRL7 mappák`
