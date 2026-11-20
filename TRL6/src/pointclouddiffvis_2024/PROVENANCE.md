# Provenance: PointCloudDiffVis (2024)

**Status:** source files as supplied by the author in `PointCloudDiffVisWindows.zip` (received 2026-11-20; SHA-256 `beb383df1ba1c181a313b11ad40e508332dc274ff2df63e89f7fea61bda342f6`). Not modified here. The Windows executable (`PointCloudDiffVis.exe`), the bundled Python runtime and packages (`addons/pythonscript/`, incl. Open3D, NumPy, Matplotlib) and the cache folders are **not included**: they are third-party software under their own licences and are rebuilt by the setup in `README.md`.

## What it is

A desktop application (Pandemonium/Godot engine with the pythonscript extension and Open3D) that compares a reference mesh with a scanned test mesh and shows each step in a 3D viewer. `processor/point_cloud_processor.py` runs the same pipeline as the 2022 notebook `TRL3/src/original_2021-2022/hegesztes_12.py`, with the same parameters:

1. read both meshes (`.ply`), compute normals; sample 250,000 points uniformly from each;
2. FPFH features (radius 10 × pcr, max_nn 1000) and Fast Global Registration (500 iterations, max tuple count 2500); pcr = mean nearest-neighbour distance;
3. ICP point-to-plane refinement (threshold 10 × pcr, max 2000 iterations);
4. point distances, histogram, colour map;
5. points above the 90th percentile of the distances are marked;
6. DBSCAN on the marked points (eps 15 × pcr, min 100 points); clusters with more than 400 points are selected.

The step that converts distances to millimetres multiplies by a fixed factor of 25 (as in the 2022 notebook); the scale is not taken from the scanner or the CAD model. The worst-cluster RMSE step of the notebook is present but commented out.

## Role in the TRL documentation

- TRL 3 (2021–2022): scripts and notebook (`TRL3/src/original_2021-2022/`).
- **2024: the same method as a standalone application with a user interface** (this folder) – the 3D step of the integrated demonstration planned for TRL 6 (part C) builds on it.
- Before use in a TRL 6 gate (G6-04), the fixed ×25 scale must be replaced by a documented scale.

## Files

Timestamps are the file-system modification times stored in the ZIP (local time of the author's computer). They are **not independently authenticated** and are not a TRL acceptance date.

| File | Modified (as stored in the ZIP) | Bytes | SHA-256 |
|---|---|---:|---|
| `.gitignore` | 2024-09-15 22:46 | 74 | `0c4f4386028248152040d736553b4f2a5af46570dd3d47a59a44605c3aa966f5` |
| `Main.gd` | 2024-09-15 22:30 | 1978 | `ff5511c9f306eeb06603a2e754b3d7ee07529700aff70d9a0e4ef708070f59ac` |
| `Main.tscn` | 2024-09-15 23:02 | 1766 | `b18a582b79683ab0c04058da4ca9849a000fc9156c18110c0e1afba465369dcd` |
| `README.md` | 2024-09-15 11:17 | 446 | `9fe44bf6106e22144e879713d2565dda3e770cc036f7558e48d09a7b3451ed7d` |
| `control_bar/ControlBar.gd` | 2024-09-15 22:39 | 2295 | `04b020b3971d7bd4e90d0b9fbac8e4adbc7a7613a5c146fda5f9cca89d138a79` |
| `control_bar/ControlBar.tscn` | 2024-09-15 23:02 | 6486 | `7bb10a82f2d1f2291e7ff810d53fcd01c23ccd6aefbee0fc9473550942d85a57` |
| `data_viewer/FreeLookCamera.gd` | 2024-09-15 22:41 | 2907 | `c0bee5710651a9980f43364b7bc4836a3763bfeb8fbe556c118c68570f20eb5c` |
| `data_viewer/Grid.gd` | 2024-09-15 21:42 | 958 | `c110ec273a8d5b45aecc7f81c08cde32b68729915557261b4b827b5f22a0e7bd` |
| `data_viewer/ResultDataViewer.gd` | 2024-09-15 22:40 | 2661 | `a5a74a4ba1480b7d87405e7ffa7be556870e15d60ed0b3f67a76e2fc0cf12824` |
| `data_viewer/ResultDataViewer.tscn` | 2024-09-15 23:02 | 2170 | `f9a4104e932647d9d6385a7f4de0822cf98f8270cbfaa0c47176d7ff0e14831c` |
| `data_viewer/new_spatialmaterial.tres` | 2024-09-15 20:21 | 92 | `be33b6b6844862b37718fa6be3483cc866200768087d31de6926264f4be4c6f1` |
| `default_env.tres` | 2024-09-15 23:02 | 165 | `42462735f8951805f33c53d0db7e89d7254239bda6fe9f1c3036557189401379` |
| `edit.bat` | 2024-09-16 15:36 | 35 | `e68418066f151d799e5758582a6546f7b2c4ef173f2351994208d19399e6d0ae` |
| `edit.sh` | 2024-09-15 22:46 | 34 | `425b0a64a12e0860f42d348fe458fe165c010ab8a38f7e0de03c84e671d41805` |
| `export_presets.cfg` | 2024-09-15 11:17 | 1738 | `5568e498459c343c7a14a8ada6e136fcf0cefdf1e3d3bad00d00463db752015d` |
| `file_opener/FileOpener.gd` | 2024-09-15 22:28 | 1695 | `b1c1a5a4437f90f3d93ff80c566e49145601cfa676a31c91fdc01f3d424db007` |
| `file_opener/FileOpener.tscn` | 2024-09-15 23:02 | 5533 | `9647ee1b5731fe26d2c326fc36d87408edbed12855b33a5dd3b98cf091f08219` |
| `icon.png` | 2024-09-15 11:17 | 7487 | `fa927eaae4d4bed5c96c4660af497b7d3c5718fff52952e4a4535bb3ee040a6e` |
| `icon.png.import` | 2024-09-15 11:17 | 674 | `283616abf50595d9a6015e25f558986730ea17fc230ab4fba1efe6890c459a6e` |
| `processor/Processor.gd` | 2024-09-15 22:55 | 2060 | `1388a7398063285e29fce9dca6f611fbd756c6cbb650ca223294dd8d1d848962` |
| `processor/Processor.tscn` | 2024-09-15 23:02 | 333 | `26fd7446ce323858ed11932d9ae8cc50c029f8fcd7547c815d7d3a733887b1c3` |
| `processor/point_cloud_processor.py` | 2024-09-15 23:02 | 19896 | `bafa886d455496fa09f49007938169779980f1e6821519755709a2f5c6724f83` |
| `project.pandemonium` | 2024-09-15 22:59 | 1479 | `adae747b7273da3e02d62ec4095733d32541cf3ee661edc0b5ba4fcbab5a419a` |
| `pythonscript.gdnlib` | 2024-09-15 11:17 | 552 | `fee0a450cc0040da81efc97150eaae9b2e4ea6b59ec9038543b09249b494d507` |
