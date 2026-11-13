# Derived tables

## `seam_segments_v2.csv` – seam boundaries for all 150 cell logs (449 seams)

One row per arc-on segment. Seams are identified by TorchSignal; the start is the TorchSignal 0→1 row, the end is taken from the robot pose by `TRL5/robotvis_validacio/eszkozok/szakaszolo_v2.py`: the last row before the tool moves ≥ 0.5 mm in two consecutive rows, never later than the TorchSignal end.

| Column | Meaning |
| --- | --- |
| `log`, `group`, `seam_in_log` | log name (e.g. `g02_s45`), speed group, segment number in the log |
| `start_row`, `end_row` | 0-based row index in the log CSV (v2) |
| `end_row_torch` | the TorchSignal 1→0 row (v1); it lags the pose-based end by a median of 1 row (P95 ≈ 0.66 s) because the power-source values are read from a web page |
| `start_ms`, `end_ms`, `end_torch_ms` | SysTimeMsecs at those rows |
| `n_segments_in_log` | 3, except g02_s33 (2: a 2.5 s logging gap merges seams 1 and 2) |
| `qc_flag` | `check_end`: the v2 end lies more than 8 rows before the TorchSignal end (5 of 449 seams: a logging gap or a pose step ≥ 0.5 mm/row during welding at high speed); use `end_row_torch` or inspect |

Validation: in a blind annotation of 20 logs not used in the rule's design (60 seams, 120 events), the v2 boundaries agreed within ±1 row for 120/120 events (`TRL5/robotvis_validacio/annotacio_T5-01/`). The flagged seams were not in that sample.
