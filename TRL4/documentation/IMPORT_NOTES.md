# TRL4 archive import notes

Sources: `TRL4_laborvalidacio_vscode.zip` and `adat_csomag_trl4.zip`, supplied by the project owner.

- `src/lab_validation/`: two supplied Python modules for dataset coverage; `common_io.py` was modified only to remove machine-specific hardcoded paths.
- `validation/results/legacy/`: previously saved JSON coverage output.
- `documentation/legacy/`: previously saved markdown summary.
- `data/processed/`: 13 legacy result tables and supporting notes, copied without changing their content.
- The raw 147 MB `csv_light2.zip` and `alátámasztás_pdf_trl4.zip` are **not** bundled or tracked here. Retain them in controlled storage.

These are historical results, not all freshly re-computed outputs. The documented 449 active welding segments and the g02_s33 exception must be independently reproduced before a formal TRL4 acceptance claim. The coverage script alone does not regenerate `segment_features.csv`, other tables, or FGR/ICP/DBSCAN results.

Before uploading confirm institutional permission to store processed research data on GitHub, even in a private repository.
