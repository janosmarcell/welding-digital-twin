# Experimental dataset inventory

The separately stored `csv_light2.zip` contains **150 CSV time-series**, **20 JPG images** and **18 PLY point clouds** (188 files total). The five nominal welding speeds are 30, 40, 50, 60 and 70 cm/min, with 30 CSV files per group.

- `g01_30`: `g01_s01.csv`–`g01_s30.csv`
- `g02_40`: `g02_s31.csv`–`g02_s60.csv`
- `g03_50`: `g03_s61.csv`–`g03_s90.csv`
- `g04_60`: `g04_s91.csv`–`g04_s120.csv`
- `g05_70`: `g05_s121.csv`–`g05_s150.csv`

The raw data archive is **not included** in this GitHub upload. Keep it in an approved controlled-access data store. The audit tool reads the archive in place and does not extract or modify it.

CSV columns: `SysTimeMsecs`, `X`, `Y`, `Z`, `Rx`, `Ry`, `Rz`, `TorchSignal`, `Voltage`, `Current`, `WireFeedSpeed`.

For the per-file row counts and on-state record counts, see `../validation/results/csv_light2_audit.json`. Audit counts are **structural checks, not physical process validation**. Sampling rates, signal semantics, correct number of weld segments, sensor calibration, and ground truth must be validated separately.
