# TRL3 experimental PoC matrix

| ID | Technical test | Expected artifacts | Evidence classification | Follow-up |
|---|---|---|---|---|
| T3-01 | CAD/reference-to-test PLY registration | FGR+ICP settings, transformation, RMSE, image | Published method in P02 | Find runnable original script, inputs and exact output |
| T3-02 | Significant deviation region clustering | DBSCAN labels, cluster coordinates and summary | Published method in P02 | Re-run and store reproducible run log |
| T3-03 | Robot/welding data extraction | Sample CSV, interface logs, acquisition description | Cell experiment published in P03 | Locate original source and device configurations |
| T3-04 | TorchSignal replay segmentation | Segment boundaries, counts, anomalies | Later processing artifacts held in TRL4 | Re-run in TRL4; do not backdate code as TRL3 |

Publication-based method evidence is not equivalent to a verified executable GitHub pipeline.
