# ESP32-C6 + iCE40UP5K M.2 module (v2, development draft)

Successor to `boards/esp32-fpga-module`: the same iCE40UP5K-SG48 FPGA and QSPI configuration link,
with the ESP32-S2 module replaced by a bare ESP32-C6FH8 (QFN32) and the board-to-board connector replaced
by an M.2 2242 key-M card edge with a custom pinout. **Not PCIe/NVMe compatible. Not for fabrication yet.**

| Item | Value |
| --- | --- |
| Card | 22 x 42 mm, 0.8 mm, 4 layers (JLC 0.8 mm stackup to be confirmed) |
| Layers | F.Cu parts and signals, In1 GND, In2 +3.3 V (with a +1.2 V island under U2), B.Cu ESP bus and FPGA lanes |
| Contacts | 67 (positions 59-66 are the key notch); pinout in `docs/icd-v2-pinout.csv` |
| Power in | +3.3 V on 2/4/70/72/74, GND on 1/3/9/15/21/27/33/39/45/51/57/71/73/75 |
| Core | TLV75512 1.2 V LDO (U3), PLL fed through L2 |
| RF | ESP32-C6 pin 1 -> C1/L3/C2 pi match -> U.FL J3, 0.26 mm CPWG carried from v1 (re-tune on the 0.8 mm stackup) |

## Files

- `module.kicad_pro/.kicad_sch/.kicad_pcb`, `module.kicad_dru`, `Module2.pretty/`, `Module2.kicad_sym`, `3dmodels/`.
- `docs/design-contract.json`: what was agreed before layout plus the final pin/contact tables.
- `docs/icd-v2-pinout.csv`: every contact with its side (odd = front copper, even = back copper), signal, IC pad and constraint.
- `docs/c6-fpga-link.csv`: the ESP32-C6 GPIO / QFN32 pad / SG48 pad mapping of the configuration link.
- `docs/contact-assignment.json`, `docs/circuit.json`, `docs/placement.json`: generator outputs.
- `docs/validation.json`, `docs/module-schematic.pdf`, `docs/module-*.svg`: checks and review exports.

## Regenerating

```sh
/usr/bin/python3 tools/hardware/build_module_v2.py --replace-draft   # libraries, placement, outline, zones, project settings
/usr/bin/python3 tools/hardware/module_v2_route.py                   # all copper, +1.2 V island, lint via roles
/usr/bin/python3 tools/hardware/module_v2_schematic.py               # symbols and schematic from docs/circuit.json
/usr/bin/python3 tools/hardware/module_v2_docs.py                    # ICD CSVs and contract tables from the board
/usr/bin/python3 tools/hardware/check_module_v2.py                   # ERC, parity DRC, PDF/SVG exports
```

## Known compromises (see `layout.deviations` in the contract)

- Eight ground vias sit in the two exposed pads. The playbook forbids vias under packages; a grounded exposed pad has no other return path, so these are kept deliberately.
- C48, C50 (FPGA VCCIO_2 / VCC east) and C39 (VDDA1) return to ground through the front pour rather than a dedicated via.
- Decoupling further than 2 mm: U2 pins 5, 29, 30 (2.9 mm), U2 pin 33 (3.7 mm, plane via at the pin), U1 VDDA3P3 (3.3 mm to the pi filter), U1 pin 20 (2.2 mm).
- The QSPI link runs through the GPIO matrix on every lane (no native FSPI pins are free of strapping/USB duties); verify the achievable configuration clock.
- ESP32-C6FH8/FH4 showed no LCSC stock on 2026-10-07.

## Open before any fabrication

Carrier design and socket fit (TE 1-2199230-6), 0.8 mm stackup selection and RF/USB re-calculation, antenna match,
finger plating/bevel confirmation against the socket drawing, firmware bring-up of the C6 target.
