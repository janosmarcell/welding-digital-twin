# TRL3 — Experimental proof of concept

**Evidence status:** published subsystem-level PoC; not a complete integrated Digital Twin.

## PoC stream A — Geometry
P02 (Sensors 2023) investigates registration of nominal/reference and welded point-cloud geometry using FGR + ICP and subsequent DBSCAN localization of significant deviations. Limitations include small defects and cracks.

## PoC stream B — Process data
P03 (Scientific Reports 2024) describes RobotComm/RobotVis data reading and visualization for a Yaskawa/Fronius experimental welding cell. It does not show that 3D defect decisions were already made in real time in that system.

## Supporting later methodology
P05 and P06 (GÉP 2026) inform refinement of threshold sensitivity and point-cloud feature interpretation. They are **later publications** and must not be used to backdate 2023–2024 accomplishments.

## Content
- `experiments/poc_test_matrix.md`: T3-01–T3-04 and evidence requirements
- `src/README.md`: strict code provenance policy
- `validation/status_and_gaps.md`: reproducibility gaps
- `documentation/prototype_boundaries.md`: subsystem boundaries and limitations
- `evidence/evidence_register.csv`: bibliographic evidence and dates

## Transition criterion
Demonstrated component-level algorithms and robot data access with stated limits; integrated TRL4 evidence remains separate.
