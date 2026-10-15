# Proposed data model and identification rules

| Entity | Key | Attributes / references |
|---|---|---|
| Experiment group | `group_id` | Nominal travel speed (30, 40, 50, 60, 70 cm/min) |
| Workpiece/sample | `sample_id` | Unique sample identifier and group |
| Weld segment | `sample_id + weld_index` | Torch on/off interval, time bounds |
| Process recording | `csv_file_id` | Timestamp, motion/process channels, source checksum |
| 2D acquisition | `image_id` | Image file, imaging conditions, optional sample match |
| 3D acquisition | `pointcloud_id` | PLY file, scan settings, optional sample match |
| Derived result | `run_id` | Script revision, parameters, dataset reference and output |

## Matching policy
- Do not infer a one-to-one weld-image or weld-pointcloud link from numeric naming alone.
- Match only after inspecting source identifiers and acquisition metadata.
- Track `unknown`, `sample-level`, and `weld-level verified` as distinct confidence states.
- All dates, IDs and schema field names should be checked against original source files before implementation.
