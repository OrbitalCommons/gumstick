# JLCPCB fabrication rules

The active KiCad project and `module.kicad_dru` use JLCPCB FR-4 multilayer capabilities checked 2026-09-24: https://jlcpcb.com/capabilities/Capab .

Assumed process: four layers, 1 oz outer copper, 0.5 oz inner copper, green solder mask and routed board edges. The actual dielectric stackup and RF impedance geometry remain to be selected and verified.

## Project choices

- Minimum through-via copper diameter 0.45 mm and drill 0.20 mm. Spread the fan-outs into available board space; keep vias outside solder pads and both QFN bodies. Existing larger vias need not shrink.
- Minimum tracks and copper clearance 0.10 mm; routed-edge clearance 0.30 mm.
- Via drill to foreign copper 0.20 mm; hole-to-hole clearance 0.25 mm.
- Different-net SMD pad spacing 0.15 mm.
- Plated pad drill to foreign copper 0.28 mm outside, 0.30 mm on inner layers; plated pad annular ring 0.15 mm.
- Drilled pad hole spacing 0.45 mm; NPTH diameter 0.50 mm minimum; plated slots 0.35 mm and nonplated slots 1.0 mm minimum.
- Solder-mask openings match pad copper; mask web 0.10 mm and opening-to-neighboring-copper clearance 0.09 mm.
- Silkscreen text height 1.0 mm and stroke 0.15 mm; pad-to-silk clearance 0.15 mm. Capacitor and resistor references remain hidden as requested.

These are project checks, not a complete fabricator acceptance model. Same-net copper details, assembly clearance, RF stackup, panelization and the eventual order selections still need review. Fabrication outputs must be regenerated after the larger-via routing passes DRC/ERC and schematic parity. Do not use earlier fabrication files as evidence that this revision passed the stricter rules.

## Larger-via migration checkpoint

The original 245 vias have been enlarged/repositioned (244 at 0.45/0.20 mm, one retained at 0.60/0.30 mm). The congested QFN fan-outs are being reconnected; this intermediate revision has open connections and is not a fabrication release. Check the current DRC report rather than earlier clean checkpoints. Work logs and geometric backups are under `tmp/jlc-vias/`.
