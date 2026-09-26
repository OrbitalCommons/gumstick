# JLCPCB manufacturing notes

## Design rules

"DRC clean" means nothing until the rules are the fab's rules. The module's
generic limits hid real violations until they were replaced with JLCPCB's
published limits. Start every JLC board from
[`boards/esp32-fpga-module/module.kicad_dru`](../../boards/esp32-fpga-module/module.kicad_dru)
(4-layer, 1 oz outer / 0.5 oz inner, routed edges). Its key rules:

| Rule | Minimum |
| --- | ---: |
| Track / space (project choice) | 0.10 mm |
| Via pad / drill (no surcharge) | 0.45 / 0.20 mm |
| Via drill → foreign copper | 0.20 mm |
| Different-net SMD pad spacing | 0.15 mm |
| PTH drill → copper (outer / inner) | 0.28 / 0.30 mm |
| PTH annular ring | 0.15 mm |
| Silkscreen text height / stroke | 1.0 / 0.15 mm |
| Via types | through only |

Record the capability URL and the date the rules were checked in the
`.kicad-pcb.json` manufacturer block.

## Stackup and impedance

- 4-layer default: **JLC04101H-7628**, 1.0 mm nominal, 0.2104 mm prepreg
  top→In1.
- 50 Ω coated CPWG on that stack: **0.26 mm trace / 0.15 mm gap**
  (≈50.15 Ω, JLC calculator). Encode the gap as a netclass/zone rule, e.g.
  `/RF_*` to GND clearance.
- Specify the stackup *and* controlled impedance on the order, because board
  thickness alone doesn't fix the stackup. Save the calculator inputs in the repo.

## Parts

- Search JLCPCB/LCSC directly. Prefer Basic parts and high stock.
- Before assigning an LCSC number, confirm that its package matches the
  footprint.
- Check stock at order time. The session hit five out-of-stock parts (LED
  C125085, LED C72043, chip antenna, crystal, buck).
- Group the BOM by LCSC/MPN, not by value string.
- DNP parts: leave them off the JLC BOM but keep them in the review BOM.

## CPL placement corrections

KiCad's footprint zero orientation and origin often differ from JLCPCB's
library model. Keep **one table per board**
(`docs/jlcpcb-placement-offsets.json`), keyed by LCSC number, applied by the
exporter:

```json
"C113281": {
  "mpn": "SN74LVC541APWR",
  "rotation_offset_degrees": -90,
  "cpl_offset_x_mm": 0, "cpl_offset_y_mm": 0,
  "verified_native_rotation_degrees": 0,
  "reason": "JLC preview needs 90° CW; pin 1 upper-left with USB at top",
  "date": "2026-09-26"
}
```

These corrections were confirmed from the carrier's previews and are worth
reusing:

| LCSC | Part | Correction |
| --- | --- | --- |
| C113281 | SN74LVC541APWR (TSSOP-20) | −90° (90° CW) |
| C51118 | AP2112K-3.3 (SOT-23-5) | −90° |
| C7519 | USBLC6-2SC6 (SOT-23-6) | −90° |
| C221660 | JS102011SAQN slide switch | +2.75 mm Y (origin on terminal row) |
| C165948 | TYPE-C-31-M-12 | −1.425 mm Y at 180° |

To derive a new correction:
1. Use the pin-1 pad in the preview for rotation.
2. Use locating pegs or shield holes for translation.
3. Cross-check against the EasyEDA package origin.

The exporter should **assert** that the part's native rotation still equals
`verified_native_rotation_degrees`, so a rotated footprint forces
re-verification. Bottom-side corrections need their own verification.

## Release snapshot

Once an order is placed:

1. Tag the commit (`v1`) and push.
2. Copy the *exact ordered* Gerber ZIP, BOM, CPL, schematic PDF, and check
   results into `boards/<board>/releases/v1/`.
3. Write SHA-256 hashes of the sources and outputs, e.g.
   `fab/checks/revision-sha256.json` and `EXPORT.json`.
4. After further edits, compare the hashes to detect stale fab outputs. The
   module's working `fab/` diverged from its sources within an hour of the
   last export.
