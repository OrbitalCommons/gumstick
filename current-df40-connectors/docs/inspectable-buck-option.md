# Inspectable buck replacement — implemented 2026-09-26

U3 is now Texas Instruments **TPS62160DGKR**, LCSC **C60726**, replacing TPS62162DSGR. Its DGK VSSOP-8 package has a 3 × 3 mm body, 0.65 mm-pitch gull-wing leads and no underside thermal pad. All eight leads are exposed for inspection/probing/rework. The project-local footprint and STEP are copied from KiCad's VSSOP-8 3 × 3 mm library; pin numbering was checked against TI's DGK drawing. No ninth pad remains.

## Circuit

Pins 1/4 are PGND/AGND; 2 VIN and 3 EN use VIN_5V; 5 is BUCK_FB; 6 VOS senses the output capacitor; 7 SW feeds L4; 8 PG retains R62's pull-up. R64 is 75 kΩ from 3.3 V to FB and R65 is 24 kΩ from FB to AGND. Both are 0402, 1%, 62.5 mW:

- R64: UNI-ROYAL 0402WGF7502TCE, C25798.
- R65: UNI-ROYAL 0402WGF2402TCE, C25769.

Nominal output is 0.8 × (1 + 75/24) = **3.300 V**. Divider current is 33.3 µA, exceeding TI's 2 µA minimum recommendation. Worst-case resistor ratio alone gives about 3.250–3.351 V; IC reference tolerance and temperature add to that. Dissipation is approximately 83 µW / 27 µW in R64/R65.

L4 remains 2.2 µH, C60 10 µF, and C61/C67 22 µF each. TI's shared TPS6216x LC table supports this nominal combination; the existing output-capacitor DC-bias review applies. Prototype transient/stability testing remains required.

## Placement and routing

U3 moved up 1.2 mm to absolute (116,122.8), rotation −90°. C60 is beside the VIN/PGND lead bank, with direct copper to both. R64/R65 sit beside AGND and FB, separated from SW. L4 was rotated 180° to receive SW directly on the right pad; the output capacitors were rotated to put their positive pads on the left output rail. The VOS trace uses a separate bottom-layer sense route from the C61 positive terminal's via. The feedback divider references the 3.3 V plane. Vias are outside regulator/passive pads and outside the regulator body; no switching-node vias were added. New passives have no orientation dots or visible reference labels.

## Thermal and sourcing limits

The DGK thermal resistance is materially higher than DSG: TI lists 184.3 versus 61.8 °C/W on its test board. These are not predictions for this PCB. At an illustrative 90–95% efficiency, 5 V → 3.3 V / 1 A implies roughly 0.17–0.37 W total conversion loss, not all inside U3. Measure U3 case temperature, input/output power and regulation at worst-case simultaneous ESP32/FPGA load and intended ambient; do not infer a guaranteed continuous 1 A board rating from the IC headline rating. TI recommends operating junction temperature ≤125 °C.

Catalog identities were checked; stock is not reserved and JLC assembly availability must be checked at order time. Existing RF/assembly release gates remain separate.

Sources:
- https://www.ti.com/product/TPS62160/part-details/TPS62160DGKR
- https://www.ti.com/lit/ds/symlink/tps62160.pdf (local `libraries/datasheets/tps62160.pdf`)
- https://www.lcsc.com/product-detail/C60726.html
- https://www.lcsc.com/product-detail/C25798.html
- https://www.lcsc.com/product-detail/C25769.html
