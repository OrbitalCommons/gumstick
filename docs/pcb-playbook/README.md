# PCB playbook

Reusable preferences, review criteria and tooling distilled from the bp-test
Codex session (`91d7cd67`, 2026-09-22 → 2026-09-26). That session took three
boards to order:

- **Direction LED tester**: 32 × 20 mm, two-layer, four parts.
- **ESP32-S2 + iCE40UP5K module**: 20 × 45 mm, four-layer, 10 ordered as `v1`.
- **Programming carrier**: USB, boot switch, a buffered LED per GPIO, and
  mating DF40 sockets for the module.

The session contained 274 user messages. Most of the rules below come from
your corrections: things that passed DRC but that you flagged when looking at
the board.

| File | Use it when |
| --- | --- |
| [layout-preferences.md](layout-preferences.md) | Placing, routing, and silkscreening any new board |
| [schematic-style.md](schematic-style.md) | Drawing or cleaning up a schematic |
| [review-checklist.md](review-checklist.md) | Before calling a layout "done" (the things DRC misses) |
| [jlcpcb-manufacturing.md](jlcpcb-manufacturing.md) | Rules, stackup, parts, CPL rotation/offsets, release snapshots |
| [agent-workflow.md](agent-workflow.md) | Instructions for an agent doing layout work |
| [reusable-tooling.md](reusable-tooling.md) | Which `tools/hardware` scripts to lift into a shared library, and how |
| [pcb-profile.yaml](pcb-profile.yaml) | Machine-readable profile for automated layout-quality checks |

## The short version

1. **DRC clean is the minimum, not the finish line.** Routing quality
   (stubs, kinks, width steps, lost vias, cap proximity) is reviewed separately,
   and "done" is only claimed after that review.
2. **Straight 45°/90° routing, one width per run, straight pad exits.**
3. **No vias in pads or under QFN bodies. Use the space you have** for big
   vias and staggered fanouts.
4. **Symmetry and centerlines**: mount holes, connectors and main ICs sit on
   the board centerline, and screws are placed where they clamp the connectors.
5. **Minimal, uniform silkscreen**: ICs and connectors only, placed pertinently,
   plus visible pin-1 dots on polarized parts.
6. **Inspectable, available parts**: 0402 minimum, leaded packages where
   bodging matters, and in-stock JLCPCB/LCSC parts.
7. **Power first, then critical signals, then I/O.** Repin connectors freely
   to simplify routing.
8. **Freeze exactly what was ordered**: tag it, archive fab outputs with
   hashes, and record every JLCPCB placement correction.
