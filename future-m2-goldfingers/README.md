# ESP32-C6 + iCE40UP5K M.2 module (v2, development draft)

Successor to `boards/esp32-fpga-module`: the same iCE40UP5K-SG48 FPGA and QSPI configuration link,
with the ESP32-S2 module replaced by a bare ESP32-C6 (QFN40) plus a 16 MB quad SPI flash, and the board-to-board connector replaced
by an M.2 2242 key-M card edge with a custom pinout. **Not PCIe/NVMe compatible. Not for fabrication yet.**

| Item | Value |
| --- | --- |
| Card | 22 x 42 mm, 0.8 mm (M.2 0.8 +/- 0.08), 4 layers, JLCPCB JLC04081H-3313 (nominal 0.799 mm) |
| Layers | F.Cu parts and signals, In1 GND, In2 +3.3 V (with a +1.2 V island under U2), B.Cu ESP bus and FPGA lanes |
| Contacts | 67 (positions 59-66 are the key notch); pinout in `docs/icd-v2-pinout.csv` |
| Power in | +3.3 V on 2/4/70/72/74, GND on 1/3/9/15/21/27/39/45/51/57/71/73/75 (33 now carries ESP_GPIO4) |
| MCU | ESP32-C6 QFN40 (U1), external 16 MB W25Q128JV flash (U4, QIO); 13 GPIOs + USB + EN on the connector |
| Core | TLV75512 1.2 V LDO (U3), PLL fed through L2 |
| RF | ESP32-C6 pin 1 -> C1/L3/C2 pi match -> U.FL J3, 50 ohm coated CPWG 0.14 mm / 0.15 mm gap on 0.0994 mm 3313 prepreg (`docs/rf-feed.json`); match values still to re-tune |

## Files

- `module.kicad_pro/.kicad_sch/.kicad_pcb`, `module.kicad_dru`, `Module2.pretty/`, `Module2.kicad_sym`, `3dmodels/`.
- `docs/design-contract.json`: what was agreed before layout plus the final pin/contact tables.
- `docs/icd-v2-pinout.csv`: every contact with its side (odd = front copper, even = back copper), signal, IC pad and constraint.
- `docs/c6-fpga-link.csv`: the ESP32-C6 GPIO / QFN40 pad / SG48 pad mapping of the configuration link.
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
- The 3.3 V input bulk sits at the power contacts: C67/C60 feed straight into the contact 70/72 vias, C61/C66 into the contact 2 via.
- Decoupling further than 2 mm: U2 pin 5 (2.9 mm), U2 pin 29 (2.9 mm), U2 pin 33 (3.7 mm, plane via at the pin), U1 VDDA3P3 (3.6 mm to the pi filter), U1 VDDPST1 (2.7 mm) and VDDPST2 (2.4 mm), both boxed in by the 0.4 mm-pitch fan-out. Each of these pins has an I/O exit on both neighbours at 0.5 mm pitch, so only a cap lying on the pin's own line fits and adjacent lines cannot both carry one; the contract records the per-pin reason.
- The QSPI link runs through the GPIO matrix on every lane (no native FSPI pins are free of strapping/USB duties); verify the achievable configuration clock.
- The flash (U4, W25Q128JVPIQ) runs from the 3.3 V plane and the ESP's VDD_SPI pin is left unconnected: that pin sits between the flash data pins, so its 0.1/1 uF pair has no room. U4 has 0.1 uF at its supply pin and C33 (10 uF) 4 mm away.
- The flash pin order is mirrored against the ESP's SPI pins, so WP and DO cross under CS on the back layer above U4 (four vias).
- L5 (24 nH, 0201) still needs an LCSC part number.

## Card edge (JLCPCB gold-finger rules, see `layout.card_edge` in the contract)

- ENIG finish with the gold-finger option; 30 degree bevel (JLCPCB offers 30/45, the M.2 drawing shows 20: confirm socket fit).
- Fingers stop 0.6 mm inside the routed edge (JLCPCB's copper setback for a 30 degree bevel, scaled from 1.13 mm at 1.6 mm); their inner ends stay at 2.0 / 2.5 mm.
- The finger field has one solder-mask window per side and a rule area that keeps pours and vias out of it.
- JLCPCB needs at least 50 x 50 mm for a board with gold fingers (and >= 5 x 5 cm for a chamfer), so the 22 x 42 mm card must be ordered as a panel with the connector edge on the panel outline and no V-cut through the fingers.

## Stackup

- M.2 fixes the card at 0.8 +/- 0.08 mm. JLCPCB's 0.8 mm four-layer builds range from 0.721 to 0.803 mm nominal, and their tolerance below 1.0 mm is +/- 0.1 mm. JLC04081H-3313 (0.799 mm) is the best-centred build; order it by name with impedance control and confirm the finished thickness over the fingers.
- Layers: 35 um Cu / 0.0994 mm 3313 prepreg (er 4.1) / In1 GND / 0.5 mm core / In2 +3.3 V / 0.0994 mm 3313 / 35 um Cu.
- The RF width comes from `tools/hardware/module_v2_impedance.py`: JLCPCB's coated-CPWG calculator gives 50.4 ohm and a 2D field solve 49.9 ohm for 0.14 mm / 0.15 mm.

## Open before any fabrication

Carrier design and socket fit (TE 1-2199230-6), 0.8 mm stackup selection and RF/USB re-calculation, antenna match,
finger plating/bevel confirmation against the socket drawing, firmware bring-up of the C6 target.
