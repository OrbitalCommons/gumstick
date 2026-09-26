# Routing verification — 2026-09-26

- KiCad DRC: 0 violations, 0 unconnected items, 0 schematic-parity issues.
- KiCad ERC: 0 violations.
- Via audit: no component-pad or QFN-body overlaps; all vias meet 0.45/0.20 mm minimum geometry.
- No component-side routing beneath QFN bodies except exposed-pad GND connections.
- All track centerlines use 45/90-degree geometry (5 nm comparison tolerance).
- QSPI copper lengths 28.151–34.668 mm (6.517 mm spread); USB mismatch 0.615 mm. Excludes via-barrel/package delays; see routing-lengths.json.
- RF reference-plane sample check: all 52 RF feed samples have In1 GND beneath them.
- Earlier four-layer inspection is retained; current external-only revision has clean DRC and a reviewed native top render. No unexpected intersections or omitted inner layers observed; this is not a fabrication/RF release.

See ../ASSEMBLY-STATUS.md for unresolved antenna and procurement gates. revision-sha256.json identifies the checked design and exports.

Component-pad thermal reliefs are enabled; no starved-thermal errors remain. Fine-pitch manual necks and solid thermal/RF exceptions are documented in thermal-reliefs.json.

Connector centers are 25.00 mm apart and 12.50 mm from H1. See connector-geometry.json and the revised docs/carrier-pinout.csv before designing a carrier.
