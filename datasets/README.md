# Robotic GMAW welding dataset (2023) – data description

Multimodal data from 150 bead-on-plate welds made with a robotic GMAW cell at ELTE Faculty of Informatics, Savaria Institute of Technology (Szombathely, Hungary), July 2023: process logs recorded during welding, top-view seam images and 3D surface scans, plus the experimental plan and derived seam boundaries.

- **Licence:** CC BY 4.0 (`../LICENSE-DATA.md`). Code in this repository: MIT (`../LICENSE`).
- **Cite as:** Hegedűs-Kuti, J. (2026). *Robotic GMAW welding digital twin: process data, seam images, 3D scans and TRL 1-7 validation* (v1.0). Zenodo. DOI: [to be added]
- **Evidence classes** used in this repository: A published, B recomputed from raw data, C secondary, D synthetic. Everything in `datasets/` is real (A/B) except `cad_pointclouds_v1/`, which is CAD geometry, not measured data. Synthetic files elsewhere in the repository are labelled and are not measurements (`../EVIDENCE_POLICY.md`).

## Experimental design

| Item | Value |
| --- | --- |
| Pieces | 150 plates, three parallel seams each (450 seams) |
| Travel speed | 5 groups: 30, 40, 50, 60, 70 cm/min (`g01` … `g05`) |
| Current / voltage / wire feed | a 30-step synergic ramp within each group, from about 40 A / 18.0 V / 1.2 m/min to 200 A / 23.8 V / 7.0 m/min; the set values per piece are in `kiserleti_terv_2023/` |
| Shielding gas | 16 l/min (column `gas`) |
| Piece numbering | `gNN_sMM`: group `NN`, piece `MM` = 1 … 150 across all groups (e.g. `g03_s75` = piece 75, 50 cm/min) |

## Folders

| Folder | Content | Size |
| --- | --- | ---: |
| `welding_experiments_v1/` | 150 process logs (CSV), 20 full-resolution seam panoramas (JPG) and 18 3D surface scans (PLY), in one subfolder per speed group | 214 MB |
| `welding_seam_images_v1/` | 462 per-seam panoramas (JPG) with a manifest and the original per-seam metadata | 68 MB |
| `kiserleti_terv_2023/` | experimental plan of 10 July 2023 (CSV and the original XLSX) | 60 kB |
| `derived/` | seam boundaries for all 150 logs (`seam_segments_v2.csv`, 449 seams), see `derived/README.md` | 40 kB |
| `cad_pointclouds_v1/` | 7 CAD meshes of an ideal and six defective fillet welds (a5 series, 2021); **CAD geometry, not measurements**, see its README | 44 kB |

### Process logs: `welding_experiments_v1/gNN_VV/gNN_sMM.csv`

One file per piece, recorded by the RobotVis application during welding. One row per update (median interval 114 ms).

| Column | Unit | Meaning |
| --- | --- | --- |
| `SysTimeMsecs` | ms | acquisition PC clock, Unix epoch; consecutive rows can share a value |
| `X`, `Y`, `Z` | mm | tool centre point position, robot base frame |
| `Rx`, `Ry`, `Rz` | degree | tool orientation |
| `TorchSignal` | 0/1 | arc on (1) / off (0), read from the power source |
| `Voltage` | V | arc voltage reported by the power source |
| `Current` | A | welding current reported by the power source |
| `WireFeedSpeed` | m/min | wire feed speed reported by the power source |

**Timing.** The robot pose arrives over a local socket; the power-source values (`TorchSignal`, `Voltage`, `Current`, `WireFeedSpeed`) are read from the power source's web page and lag the pose by up to about 0.5 s (95th percentile 0.29–0.47 s in replay tests, `../TRL5/robotvis_validacio/`). For seam boundaries, use `derived/seam_segments_v2.csv`, whose ends are taken from the robot motion.

**Known issues.** 7 of the 150 logs contain a logging gap longer than 1 s (longest 2.5 s, `g02_s33`, where seams 1 and 2 merge into one arc-on segment). The set values of `g01_s15` differ from the plan (logged 130.5 A, 18.72 V, 3.8 m/min; planned 127 A, 20.9 V, 4.0 m/min).

### Full-resolution panoramas and 3D scans: `welding_experiments_v1/`

- `gNN_sMM.jpg`: full-resolution panorama (about 6000 × 2100 px) of one seam of the piece, 20 pieces; the down-scaled panoramas of all seams are in `welding_seam_images_v1/`.
- `gNN_sMM.ply`: 3D surface scan, 18 pieces (01, 15, 19, 22, 23, 30, 60, 61, 75, 79, 85, 90, 99, 110, 118, 121, 135, 150). Two resolutions are present (about 30–50 thousand and 400–670 thousand points), reflecting two scanner set-ups.

### Seam panoramas: `welding_seam_images_v1/`

- `jpg/seamN_k.jpg`: panorama of seam `k` (1–3) of piece `N`, stitched from six overlapping microscope-camera frames and down-scaled to 1600 px width (originals about 6000 × 2100 px).
- `manifest.csv`: one row per image. Columns (Hungarian names): `kep_fajl` file, `darab_id` piece, `json_id` ID in the original metadata, `varrat_sorszam` seam number, `aram_A` current (A), `feszultseg_V` voltage (V), `sebesseg_cm_perc` travel speed (cm/min), `eredeti_px` original size, `forras` / `json_forras` source archive.
- `archive_info_osszes.csv`: the original per-seam metadata (`archive_info.json`) of all 462 images.
- `METAADAT_v2.md`: provenance and checks (in Hungarian).

**Coverage and exceptions.**
- Panoramas exist for 142 of the 150 pieces; none were taken of pieces 44, 121, 125, 130, 135, 140, 145 and 150.
- Piece 76 has six images with identical settings (probably photographed twice).
- IDs 201–207 are preliminary trials of 7 July 2023 (extreme settings at 20–90 cm/min) and 500–503 are test images with placeholder metadata; neither belongs to the 150-piece series.
- For piece 22 the image metadata state 174 A / 21.7 V; the plan and the log (171 A / 21.9 V) are authoritative.
- The image-to-log mapping was checked by correlating seam appearance with the logged settings (r = 0.993, n = 425 seams).

### Experimental plan: `kiserleti_terv_2023/`

`kiserleti_terv_2023-07-10.csv`: `ref` piece number, `I` current (A), `U` voltage (V), `v` travel speed (cm/min), `wfs` wire feed speed (m/min), `gas` shielding gas flow (l/min). The logged set values match the plan within 0.5 A, 0.04 V and 0 m/min for all pieces except `g01_s15`.

## Related material in the repository

- Validation of the process-data layer (latency, blind annotation of seam boundaries, operator trial): `../TRL5/`.
- 2D seam measurement and 3D comparison prototypes (2024–2025): `../TRL6/src/`.

## Language

This file and `derived/README.md` are in English. Some provenance notes (`METAADAT_v2.md`) and column names are in Hungarian; their meaning is given above.
