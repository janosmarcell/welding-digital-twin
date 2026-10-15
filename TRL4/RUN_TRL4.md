# TRL4 laboratory coverage reproducibility

This folder is an additive import into an existing `TRL4/` GitHub directory. Keep the existing `TRL4/README.md`, `TRL4/data/README.md`, `TRL4/src/csv_processing/audit_dataset.py`, and the existing audit JSON.

## Run on Windows (from the TRL4 directory)

1. Install Python 3.10 or later. No third-party modules are needed for the coverage script.
2. Keep the raw `csv_light2.zip` file outside the repository or put it in `TRL4/data/raw/` (excluded via the supplied `.gitignore` suggestions).
3. Run:

```powershell
python src/lab_validation/trl4_lab_validation_matrix.py --zip "C:\\path\\to\\csv_light2.zip"
```

The script creates `outputs/trl4_lab_validation_matrix.json` and `reports/trl4_lab_validation_report.md` relative to the current directory. Compare the resulting JSON `coverage` and `matrix` sections with `validation/results/legacy/trl4_lab_validation_matrix.json`.

**Scope:** coverage of CSV/JPG/PLY names. This is not geometric defect validation or full TRL4 sign-off. Legacy result tables in `data/processed/` are archived outputs; the complete original generation pipeline was not present in the supplied VS Code ZIP.
