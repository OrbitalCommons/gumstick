# ESP32 + FPGA module

**For new carriers, use the [ordered-v1 interface control document](docs/ICD-v1.md).** It supersedes historical integration dimensions and pin notes below.

A 20 × 45 mm, four-layer development module extracted from the original
Eagle/Fusion MainBoard. It combines an ESP32-S2FH4 with an iCE40UP5K-SG48I,
a U.FL jack for an external antenna, an RGB indicator and onboard power regulation.
Routing is complete for the complementary connector pair and centered ICs.
Trace centerlines use 90/45-degree geometry with standardized power widths.
KiCad reports zero DRC violations, unconnected items, schematic-parity issues,
and ERC violations.
RF, thermal, and manufacturing review remain prototype validation requirements.
The [ordered v1 snapshot](releases/v1/README.md) preserves the manufactured revision.
Current working fabrication outputs and historical review notes are not a substitute for that snapshot.
The [width-cleanup report](docs/trace-width-audit/README.md) records the final
placement improvements and the clearance-limited neck-downs retained.

Two underside Hirose DF40 40-pin connectors carry power, programming and
GPIO signals. J1 is a receptacle and J2 a plug; both are horizontal. The
complementary genders prevent reversed full mating with the carrier pair. The [programming carrier](../programming-carrier/README.md) supplies USB, buttons
and mating connectors; the [GPS calibrator](../gps-time-calibrator/README.md) is a separate application carrier.

## Power

The board takes 5 V from the carrier. U3 produces 3.3 V; U4 produces the
FPGA's 1.2 V core supply. All FPGA I/O banks use 3.3 V. The optional 1.8 V
regulator and voltage-selection jumper have been removed.

L1 and L2 are Murata BLM18KG101TN1D **0603 ferrite beads, 100 ohm at 100 MHz**,
not 1 nH inductors. They form the ESP32 and FPGA PLL supply filters.
L3 is the separate 2.2 nH RF matching inductor.

## Mechanical and assembly notes

- J1, H1 and J2 lie on the longitudinal centerline, with 25 mm connector
  spacing and the hole 12.5 mm from each connector. Use the H1-relative
  body datums in the [v1 ICD](docs/ICD-v1.md); older top-edge offsets were stale.
- U1 and U2 are centered across the 20 mm board width.
- H1 has a 3.2 mm hole and a 7 mm screw-head/spacer keepout. Match the carrier
  spacer height to the connector stack height so tightening cannot crush them.
- The ordered board uses external U.FL only. Reserve cable/plug access and
  validate the chosen antenna in the carrier/enclosure; chip-antenna notes are historical.
- Vias must remain outside component solder pads and the complete QFN package bodies.
  The via-access audit passes with no pad or QFN-body overlaps.
  Confirm the stackup and validate IC temperatures with the revised ground fanouts.
- Silkscreen keeps main IC, connector and solder-jumper references. Other
  component references remain available on fabrication layers.

D1 is the original FC-B1010RGBT-HG common-anode LED. Its RGB cathodes connect
to the FPGA's RGB current drivers and share J2 pins 26, 27 and 29. Firmware must use
those drivers correctly; the carrier pins are not unloaded independent GPIOs.

## Files

- `module.kicad_pro`, `module.kicad_sch`, `module.kicad_pcb`: active design.
- `Module.kicad_sym`, `Module.pretty`, library tables: project-local libraries.
- [3D model provenance](3dmodels/README.md): local component models; LED, antenna and power-inductor envelopes include approximations.
- [3D assembly](fab/module.glb).
- [Carrier pinout](docs/carrier-pinout.csv) and [layout notes](docs/layout-notes.md).
- [Component sourcing](docs/component-sourcing.md): selected manufacturer parts,
  supplier links and procurement caveats; the current BOM has 49 purchased placements.
- [BOM](fab/bom/module-bom.csv); [non-purchased PCB features](fab/bom/pcb-features.csv).
- `fab/checks`: ERC, DRC, via/pad overlap audit, and the schematic netlist.
- [Gerber ZIP](fab/module-gerbers.zip), [assembly BOM](fab/jlcpcb/BOM_module.csv),
  [placement CSV](fab/jlcpcb/CPL_module.csv), and [schematic PDF](fab/module-schematic.pdf).

The ESP32-C3 is not pin-compatible with the S2. It remains an architecture
option requiring a new footprint and pinout; the current design retains S2.

Original exports are preserved in `../../source/fusion`, with the native
import reference in `../mainboard-reference`. The module restores Eagle's
C49/C50 power assignments that were split by the initial native import.

TP1 exposes FPGA_CRESET_N (active-low reset); TP2 exposes FPGA_CDONE.
The application-specific SYNC_IO connection is removed. ESP GPIO38 is exposed
on J1.39 and FPGA physical pin 44 / G6 on J2.32; they are not joined on the module.
ESP32 package pins 31–36 remain unconnected externally
because they serve the S2FH4 internal flash.

See [carrier mating requirements](docs/carrier-keying.md) for the connector
MPNs, 2 mm stack, mounting-tab requirements, and carrier contact mapping.
