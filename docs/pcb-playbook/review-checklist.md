# Layout review checklist (beyond DRC)

Every item here passed KiCad DRC with zero violations on this project and was
still caught by your visual review. Run through this list before reporting a
layout as done. Where possible, automate the item (see
[reusable-tooling.md](reusable-tooling.md)).

## Copper geometry

- [ ] **Stubs/tails**: no copper extending past a junction. KiCad's
  dangling-track check misses stubs that touch same-net copper.
- [ ] **Kinks/doglegs**: no unnecessary jogs, and no wraparound routes between
  adjacent pins (the U4 VIN→EN route).
- [ ] **Width islands**: no short wide section between two narrow ones.
  No thick→thin transition without a clearance reason.
- [ ] **Octilinear**: no off-angle segments, and no circle approximations
  around keepouts.
- [ ] **Pad exits**: traces leave centered and straight, and bends occur
  outside the pad.
- [ ] **Pad contact**: no trace grazing a second pad, even on the same net.
- [ ] **Merged segments**: collinear, equal-width segments merged.
  One cleanup pass removed 1,522 redundant segments.

## Vias

- [ ] None in pads; none under QFN/BGA bodies (keepout enforced).
- [ ] No orphan vias. For each via, verify it connects at least two layers
  that need it. The user caught about 12 "lost vias" by clock position
  relative to the M3 hole.
- [ ] Redundant ground vias removed, *except* decoupling and RF return vias.
  Justify each one kept.
- [ ] None under regulators or small parts where they block inspection.
- [ ] Fanout vias staggered, not crammed.

## Power integrity (placement)

- [ ] Every IC supply pin has its decoupler within ~1–2 mm, on the same
  side. Measure it (`audit_decoupling_placement.py`); don't eyeball it.
- [ ] Each decoupler has a short return via to the ground plane.
- [ ] π-filters are placed between their source and the pin they feed, on
  that pin's side of the IC.
- [ ] Cap functions make sense. *C66 was "just shorting V+ and GND" with no
  pin nearby.*
- [ ] Plane-connected pads have thermal reliefs, and the fill leaves none
  disconnected.

## RF / high-speed

- [ ] RF feed width/gap calculated for the *actual* fab stackup (record the
  inputs), and continuous ground beneath it.
- [ ] Feed is as short and straight as possible.
- [ ] Length-matched groups (QSPI, USB pair) report their spread.
- [ ] Crystal and its load caps are compact, symmetric, and clear of the edge.

## Silkscreen and assembly

- [ ] Only IC, connector, and jumper references; uniform size; none
  eclipsed by vias or pads.
- [ ] Visible pin-1 dots on every polarized part.
- [ ] Every part has a 3D model, and the 3D view matches the PCB.
- [ ] JLCPCB assembly preview checked for rotation and offset on every IC,
  connector, and switch (see [jlcpcb-manufacturing.md](jlcpcb-manufacturing.md)).
- [ ] LED polarity in the preview matches the footprint.

## Schematic ↔ layout

- [ ] ERC, DRC, *and schematic parity*. The first board's schematic had both
  LEDs facing the same way while the PCB reversed one, and ERC/DRC alone
  passed.
- [ ] Carrier/pinout CSV regenerated after any connector repin.

## Outputs

- [ ] Fab outputs regenerated *after* the last PCB/schematic save. Compare
  source hashes against the recorded export manifest.
- [ ] BOM rows grouped by part number. Identical parts must not split on
  value/notes formatting.
