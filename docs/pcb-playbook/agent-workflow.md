# Agent workflow for PCB work

This is how you worked with the Codex agent, and what an agent should do by
default on these boards.

## Interaction style

- **Short, visual, iterative.** You review in the Backplane portal pane
  (schematic / PCB / 3D / BOM / Gerbers) and send terse instructions,
  screenshots, or clock positions ("~8:00 from the M3 hole"). Act on them
  directly and reply in one or two lines with the result and check status.
- **Screenshots are specific.** "Why kink", "Why tail", "Size changes?" each
  point at a real defect. Identify the exact object (net, ref, coordinates)
  before answering, then fix it and look for the same pattern elsewhere.
- **Defaults when ambiguous:** decide and report rather than ask, unless the
  choice is architectural (e.g. S2 vs C3, or which spacing number was meant).
- **Always offer download links** after regenerating: Gerber ZIP, BOM, and
  CPL as *separate* `portal://file/...` links.
- **Be honest about DRC.** Never equate "DRC clean" with "done" or
  "fab-ready". State what the rules cover. When you catch a defect the agent
  called clean, own the overstatement and fix the checker, not just the
  instance.
- **Get approval before contacting vendors** or other external services.

## Order of operations for a layout

1. **Rules first.** Load the fab's DRC rules and stackup before routing.
2. **Mechanical skeleton.** Set the outline, centerline, holes, connectors,
   and RF end. Write the key dimensions into `docs/layout-notes.md`.
3. **Placement.** Put regulators near their loads, decouplers at their pins,
   and compact filter groups in place. Run the decoupling audit.
4. **Power routing** and plane connections.
5. **Critical signals**: RF, crystal, USB pair, and length-matched buses.
6. **I/O fanout.** Use staggered external vias and repin connectors to
   uncross routes.
7. **Cleanup passes**: octilinear straightening, collinear merging, width
   triage, stub/orphan pruning, and redundant-via removal. Guard each pass
   with DRC.
8. **Silkscreen and pin-1 markers**, then 3D models.
9. **Review** against [review-checklist.md](review-checklist.md).
10. **Export** Gerbers, BOM, and CPL with offsets, write hashes, and post links.

## Guardrails for scripted board edits

- **Make edits transactional.** Snapshot the board, apply the change, refill
  zones, run full DRC with schematic parity, and revert unless the result is
  no worse (see `apply_width_triage.py` and `remove_redundant_pad_vias.py`).
- **Separate read-only audits from mutations.** Audits write JSON/CSV/MD
  reports under `docs/` and never save the board.
- **Mark one-time ECO scripts clearly** ("run on the pre-X board only") so
  they aren't rerun.
- **Encode your rules as constraints** (e.g. QFN via keepouts in the DRC
  file) so later automated passes can't regress them.
- **Store routing-quality state in the repo.** Fanout plans, pinout overrides,
  and signal-name maps are JSON under `docs/`.
- **Leave boards open in KiCad alone.** Check for `~*.lck` before writing the
  file.
