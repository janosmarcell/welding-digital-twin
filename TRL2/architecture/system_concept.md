# TRL2 conceptual system architecture

**Status:** retrospective architecture of proposed subsystems; **not** a verified integrated deployment.

```mermaid
flowchart TD
 A[Yaskawa robot] --> C[Process recording]
 B[Fronius welding source] --> C
 C --> D[Timestamped CSV]
 D --> G[Sample and weld ID mapping]
 E[2D camera images] --> G
 F[3D scans / PLY] --> G
 G --> H[Offline analytics: segmentation and geometry]
 H --> I[Evidence report / engineer review]
```

## Boundaries
- Physical cell and process recorder are separate from offline analytics and image/scanner acquisition.
- Joined records must preserve sample ID, weld number, process configuration, and timestamp where available.
- Existing images/PLYs may not be weld-specific; sample-level matching **must not** be presented as weld-level pairing.
- No closed-loop optimization, production approval, or real-time geometry decision is demonstrated by this architecture.
