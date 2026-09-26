# v1 — first ten-board order

On 2026-09-26 the user reported ordering **10 ESP32 + FPGA modules** from the current fabrication and assembly files. Git tag `v1` preserves that design snapshot. This records the reported order, not a received or electrically validated production batch.

Frozen order files (paths relative to this release directory):

- `manufacturing/module-gerbers.zip` — Gerbers and drills
- `manufacturing/BOM_module.csv` — assembly BOM
- `manufacturing/CPL_module.csv` — component placement

`manufacturing/module-schematic.pdf` accompanies the order files. `SHA256SUMS` records the exact bytes of the frozen manufacturing files. `checks/` preserves the validation reports and source/3D artifact hashes. Run `sha256sum -c SHA256SUMS` from this directory to verify. Checks passed before ordering: zero DRC violations, zero unrouted connections, zero schematic parity issues, and zero ERC violations. No manufacturing outputs were regenerated while creating this release.

The design includes the external-only U.FL antenna connection, TPS62160DGKR exposed-lead buck with 3.3 V feedback divider, manufacturer Coilcraft inductor model, and aligned crystal passives. Existing RF, oscillator and full-load thermal validation notes remain applicable to prototype bring-up. Existing drawing revision strings are retained exactly as supplied for this order; `v1` is the repository release identifier.

The canonical board and its project-local libraries are authoritative. Historical import/placement/routing scripts capture development stages and are not a single reproducible build pipeline; do not rerun them wholesale to recreate v1.
