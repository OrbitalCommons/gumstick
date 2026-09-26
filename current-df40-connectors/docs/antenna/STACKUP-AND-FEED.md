# RF stackup and feed design — 2026-09-25

Selected ordering stackup: **JLC04101H-7628**, nominal **1.0 mm**, four layers, 1 oz outer / 0.5 oz inner. Specify this stackup explicitly and 50-ohm single-ended controlled impedance when ordering; do not allow an arbitrary stack substitution.

Published layer construction: F.Cu 0.035 mm; 7628 prepreg 0.2104 mm, Er 4.4; In1 0.0152 mm; core 0.5 mm, Er 4.48; In2 0.0152 mm; prepreg 0.2104 mm, Er 4.4; B.Cu 0.035 mm. Nominal ordering thickness and the summed 1.0212 mm copper/dielectric construction differ; confirm fabrication tolerance. KiCad now records this construction. Dielectric loss tangent 0.02 is an unverified CAD placeholder, not a measured loss model.

JLCPCB coated grounded-coplanar calculator result: **0.260 mm base trace width, 0.150 mm ground gap → 50.1544 ohms**. Uniform RF sections use that width; the short QFN escape stays 0.15 mm. This calculation does not model discrete parts, their pads, selector gaps, launch discontinuities, finite board edges or the antenna transition.

Calculator model: CoatedCoplanarWaveguideWithLowerGnd1B. H1=0.2104 mm, Er1=4.4; manufacturer calculator process defaults T1=1.6 mil finished copper, top width 0.5 mil narrower than base, substrate coating 1.0 mil, trace coating 0.6 mil, coating Er=3.8. The published stackup nominal copper is 0.035 mm; the calculator uses its process-specific finished thickness. These are manufacturer calculator assumptions, not lot measurements. Request final fabrication confirmation/tolerance (target ±10%). Raw requests/results and material data are in calculations/.

A custom RF-to-ground-zone clearance rule enforces the 0.15 mm gap. The obsolete selector and chip-antenna exclusions have been removed. Ground stitching and filled planes support the direct U.FL feed. All 52 sampled RF track points have In1 GND beneath them; this is not full electromagnetic validation.

Sources: https://jlcpcb.com/impedance and https://jlcpcb.com/pcb-impedance-calculator. Data retrieved from their public page APIs: /api/overseas-core-platform/shoppingCart/getImpedanceTemplateSettings and /api/jlcTools/impedance/selectPageImpedanceDefaultTemplate, with 4 layers, 1.0 mm, 1/0.5 oz selection; calculator requests and results captured directly.

## Current external-only revision

No chip antenna, selector or ungrounded antenna artwork remains. J3 is aligned with the RF matching network and fed directly by the original matching network. Confirm connector-launch and complete cable/antenna RF performance; the nominal transmission-line calculation is not a measured qualification.

## Live stackup recheck — 2026-09-26

Queried JLCPCB's current selectPageImpedanceDefaultTemplate endpoint (4 layers, 1.0 mm, 1 oz outer, 0.5 oz inner). JLC04101H-7628 remains listed. Copper/dielectric thicknesses and dielectric constants match the KiCad stackup: 0.035 / 0.2104 / 0.0152 / 0.5000 / 0.0152 / 0.2104 / 0.035 mm; prepreg Er 4.4, core Er 4.48. Snapshot: calculations/selected-stackup-20260926.json. Explicitly select this stackup with controlled impedance when ordering.

The public impedance page currently lists substrate soldermask coating 1.2 mil, whereas the saved calculator request used 1.0 mil (trace coating is 0.6 mil in both). Thus the previous 50.1544-ohm result remains a nominal calculation under its recorded assumptions, not exact confirmation for the current mask process. Have JLC confirm the coated CPWG width/gap and tolerance before release. CAD dielectric loss tangent remains an unverified placeholder.
