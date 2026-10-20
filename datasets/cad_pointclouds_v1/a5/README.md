# CAD point clouds v1 - series a5

**Evidence class:** CAD-derived geometry. These are **not scans** and not measured data. They are neither raw measurements nor reprocessed measurements (see `EVIDENCE_POLICY.md`, rule 3). Keep them separate from `datasets/welding_experiments_v1/` (real scans).

Supplied by the author on 2026-10-20 (`holtpont1.zip`); file modification times in the ZIP: 2021-12-08 16:58. Files are unmodified.

## Files

| File | Content (from file name) | Vertices | Faces | Bounding box | SHA-256 |
|---|---|---:|---:|---|---|
| `ideal_a5.ply` | Reference (ideal) weld model | 20 | 36 | 1.969 x 1.969 x 1.181 | `65eca400dfc2e11934835237869ea1536deeaadb2bfc40a47ab114dbb4c3f5f6` |
| `crack_repedes_a5du.ply` | Crack (ISO 5817 no. 100) | 28 | 52 | 1.969 x 1.969 x 1.181 | `0358297d77ea3b3d66db85e80b0c2df0d9c025b3898a9b7e6b4ffa20ac2b1f81` |
| `end_crater_pipe_vegkrater_a5D.ply` | End crater pipe | 73 | 142 | 1.969 x 1.969 x 1.181 | `7ccdb6ef2fe5acef7dbe5df7e18a9e4e095cc0b9e3c819c7b9d9535b1d6b9e10` |
| `exc_throat_amn_a5_D.ply` | Excessive throat thickness | 20 | 36 | 1.969 x 1.969 x 1.181 | `e90310c4fc663256fbe7364e2e98c1f576ca3bd4475da41cc231e1a54872e79a` |
| `excessive_assim_aszim_a5D.ply` | Excessive asymmetry of fillet weld | 20 | 36 | 1.969 x 1.969 x 1.181 | `ae7912e8dda276c53a779c7fee1f8ee5420b7cd04dddb5e19d098e7c9b78d6a3` |
| `excessive_conv_vdudor_a5D.ply` | Excessive convexity | 32 | 60 | 1.969 x 1.969 x 1.181 | `02f7e3fdec0337d3829cbbc0bd1df99c7d2815fe0d177190e487ef4aa9ba2a9f` |
| `solid_intermittend_u_szel_a5_D.ply` | Intermittent undercut | 30 | 56 | 1.969 x 1.969 x 1.181 | `fbd8b8a6ce7394b8d4354eef931cb1d0ff20a475f9a89397e47442b5c4e5e9fe` |

- Binary little-endian PLY triangle meshes (VCGLIB), 20-73 vertices each. Point clouds with 250,000 points are produced by sampling the meshes in the scripts (`TRL3/src/original_2021-2022/`).
- All seven meshes share the same bounding box, i.e. the same coordinate frame as the reference.
- The bounding box 1.969 x 1.969 x 1.181 corresponds to 50 x 50 x 30 mm **if the unit is inch** (to be confirmed).
- "a5" is read as the A5 fillet-weld size used for the ISO 5817 limit values in Sensors 2023, 23, 2503 (to be confirmed). The defect names correspond to the ISO 5817 deviations evaluated in that paper; the mapping is by file name only.
- The a3 series (`idealis_a3`, `amn_a3B/C/D`, `amk_a3C/D`, `aszim_a3B/C/D`) belongs in the same dataset as a separate `a3/` subfolder.

## Use

Reference/test pairs for FGR + ICP + DBSCAN registration (TRL3 test T3-01 in `TRL3/experiments/poc_test_matrix.md`; TRL5 test T5-04). Results from CAD pairs must be reported separately from results on real scans.
