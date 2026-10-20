# Provenance: FGR + ICP + DBSCAN scripts (supplied 2026-10-20)

**Status:** original files, byte-for-byte as supplied by the author in `holtpont1.zip` (ZIP created 2026-10-20). They are **not modified** here. Do not edit them; put any modern reproduction script in a separate file.

## Files

| File | Modified (as stored in the ZIP) | Bytes | SHA-256 | Note |
|---|---|---:|---|---|
| `figure1208.py` | 2021-12-08 16:54 | 5874 | `ca662d7202196b40b75170f2cb5c301a314f419c77c5fdad1021a2f33c5abb29` | Plots the percentile-sensitivity table `sens.csv` (cluster size vs. threshold, per ISO 5817 defect group). |
| `hegesztes1208.py` | 2021-12-08 16:54 | 8825 | `b0ab54daed1bfc31308418129ccb91304fb3fdd6db691bc20e1734723f9fc78d` | Earliest supplied pipeline version (Jupyter export; mesh paths `d:/actualW/sens/`). |
| `hegesztes1208_v2.py` | 2021-12-21 14:52 | 8929 | `7f2b7949b3fd4ebb38376fc2bd5cd5584de93009d3e44e1cab2db79dd2c628f4` | Same pipeline; mesh paths point to `C:/Users/ruppert/Dropbox/HKJ_RT/holt-pont/meshfelhok/`. |
| `hegesztes_v3.py` | 2021-12-21 14:53 | 8367 | `180bfa4400cddb3193dfa1bbe25da8aa1d9255909cbf65b5e6d632c6408c7979` | Adds library-version comments (Open3D 0.12, NumPy 1.15, Matplotlib 3.3). Calls `registration_fast_based_on_feature_matching`. |
| `hegesztes_v4.py` | 2021-12-28 05:30 | 8366 | `cc4d9800bb8d0acdd2825a32223ccc2c2a473d60c801cff9a378c72805f8b1c1` | Differs from v3 in one line: `registration_fast_based_on_feature_matching` -> `registration_fgr_based_on_feature_matching`. |
| `hegesztes_12.py` | 2022-11-04 13:20 | 9107 | `5bccddd5e44503715d35aa3360008abe1365de16e1cd9d34a478a96f268d9a95` | Latest supplied version (Jupyter export of the notebook below). Uses the a3 CAD series, mesh paths `x:/12/`. |
| `hegesztes_12.ipynb` | 2022-11-04 12:57 | 23562 | `bb04467120927a4fd2558dc4df4ac87249332da579ebb5189a2d9383031d36bf` | Notebook of the latest version. |
| `sens.csv` | 2021-12-08 16:54 | 532 | `4647ec3b1ee3e6c5238e02d08253100783ad19be328a1daaf397dfee87ef4b72` | Percentile-sensitivity table: cluster sizes for percentile 90-99 per defect group (input of `figure1208.py`). |

Timestamps are the file-system modification times stored in the ZIP (local time of the author's computer; time zone not recorded). They are **not independently authenticated** and are not a TRL acceptance date.

## What the code does (verified by reading `hegesztes_12.py`)

1. Read reference and test triangle meshes (`.ply`), compute vertex normals.
2. Sample 250,000 points uniformly from each mesh.
3. `pcr` = mean nearest-neighbour distance (average of both clouds).
4. FPFH features (radius = 10 x pcr, max_nn = 1000), then Fast Global Registration (max correspondence distance 10 x pcr, 500 iterations, max tuple count 2500).
5. ICP refinement, point-to-plane, threshold 10 x pcr, max 2000 iterations.
6. Point-to-point distances; points above the 90th percentile of the distances are kept.
7. DBSCAN on those points (eps = 15 x pcr, min points = 100); clusters with more than 400 points are selected.
8. RMSE of the worst cluster against the reference, and its centroid.

These values agree with the parameters reported in Hegedus-Kuti et al., Sensors 2023, 23, 2503 (250,000 points; eps = 15 x pcr; minimum 100 points per cluster; threshold sweep 90-99%; Python 3.7.7). Agreement of parameters is not a reproduction of the results.

## Open items

- [ ] **Independent timestamp.** The file dates (2021-12-08 ... 2022-11-04) precede the Sensors 2023 submission date (received 2022-12-29). Confirm with an independent record, e.g. Dropbox version history of the `HKJ_RT/holt-pont` folder or e-mail attachments.
- [ ] **Authorship per version.** `hegesztes1208_v2.py` refers to a `ruppert` user directory; record who wrote and ran each version.
- [ ] **Original environment.** v3 comments: Open3D 0.12, NumPy 1.15, Matplotlib 3.3. Sensors 2023 states Python 3.7.7 and "Open3D (vers.: 21.1.3)", which does not match the Open3D 0.12 comment. Provide `pip freeze` of the original environment if it still exists.
- [ ] **Unit scale.** The three CAD meshes' bounding box is 1.969 x 1.969 x 1.181 (= 50 x 50 x 30 mm if the unit is inch). `hegesztes_12.py` converts distances to mm with a factor of 25 (not 25.4). Confirm the unit before quoting mm values from this code.
- [ ] **Reproduction.** Not run yet. Reproduce under a declared Python/Open3D environment and record transformation, fitness, RMSE and DBSCAN labels (see `TRL3/validation/status_and_gaps.md`).
- [ ] Scripts contain absolute paths (`x:/12/`, `d:/actualW/`, `C:/Users/ruppert/...`) and `get_ipython()` calls, so they do not run unchanged on another machine.
