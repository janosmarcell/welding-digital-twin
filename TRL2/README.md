# TRL2 — Technology concept and data architecture

**Evidence status:** retrospectively supported concept; architecture is documented here as a reconstruction, not evidence that the whole system had been integrated at TRL2.

## Objective
Specify a modular approach connecting robot/welding process data with 2D weld imagery and 3D surface geometry assessment.

## Modules
1. Yaskawa robot / Fronius welding source process acquisition (historical PoC evidence: P03).
2. CSV time series with coordinates, torch state and relevant process signals.
3. Optional 2D images and 3D point-cloud files tied to sample IDs.
4. Segmentation, feature extraction, registration and anomaly assessment.
5. Traceable assessment and reporting; no claimed automated process control.

## Documents
- `architecture/system_concept.md`: Mermaid data-flow design
- `architecture/data_model.md`: linking rules and fields
- `documentation/functional_requirements.md`: requirements and risks
- `evidence/evidence_register.csv`: publications and status
- `validation/trl2_design_review.md`: planned vs verified checks

## Sources
P01 [HJIC 2021](https://doi.org/10.33927/hjic-2021-13); P02 [Sensors 2023](https://doi.org/10.3390/s23052503); P03 [Scientific Reports 2024](https://doi.org/10.1038/s41598-024-59146-9).

## Transition criterion
Testable PoC tasks, data interfaces, key identifiers and non-automated review boundaries are explicitly specified. A historical formal acceptance record has not been verified.
