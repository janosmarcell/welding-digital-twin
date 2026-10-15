# Upload this overlay to the existing GitHub repository

This bundle is an **overlay**, not a new repository and not a replacement for existing README files. Preserve the existing TRL4/README.md and folder structure.

1. Extract this ZIP locally.
2. Open your private GitHub repository and choose **Add file → Upload files** at the repository root.
3. Drag the **TRL4 folder contents preserving their relative paths** from the extracted bundle into the upload area. If the web interface does not retain folder paths, use GitHub Desktop and copy the extracted TRL4 directory into the local clone, then commit and push.
4. Check that the paths start with `TRL4/` (do not create `TRL4/TRL4/`).
5. Commit with message `Add TRL4 dataset inventory and structural audit`.
6. Keep `csv_light2.zip` and raw JPG/PLY/CSV datasets OUT of this commit until institutional data policies are checked.

## Re-run audit locally

```bash
python TRL4/src/csv_processing/audit_dataset.py /path/to/csv_light2.zip --out TRL4/validation/results/csv_light2_audit.json
```

The present audit only checks inventory, filenames, headers, rows and TorchSignal counts. TRL4 quality and performance validation still requires dedicated tests and evidence.
