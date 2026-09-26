# Trace-width cleanup results

The repair reduced **simple series width steps from 81 to 28**, and all
centerline width-changing contacts (including branches) from **195 to 66**.
The extended inventory decreased from 541 to 158 pairwise contacts, including
92 overlapping-copper contacts. Pair counts are not counts of separate defects.

**No isolated wide islands and no unobstructed whole-run widening candidates
remain.** Remaining width changes are retained pad escapes, via escapes, or
branches with identified clearance obstacles. `resolution.json` records the
reason and blocking geometry for every retained contact. This is a review of
the present routing, not proof that no alternative layout is possible.

## What changed

- Removed 119 literal duplicate trace segments and cleaned up redundant stubs.
- Simplified complete power runs and rerouted narrow sections at wider widths.
- Rotated C39 180 degrees to face the supply and ground vias directly.
- Moved SJ1 to (9, 33.1) mm and rotated it 180 degrees: 1.8 V approaches from
  the left, 3.3 V from the right, and the selected bank supply exits below.
  Pads 1–2 remain bridged by default, selecting 3.3 V.
- Shifted C60 right by 0.10 mm and R61 right by 0.15 mm to straighten the
  5 V buck-input feed while preserving footprint courtyard clearance.
- Rebuilt U4's input/enable and output connections as consistent-width runs.
- Moved one MOSI via down by 0.075 mm to clear the selector/pull-up channel.

The QFN placements, connector pair, mounting hole and antenna are unchanged.
Vias remain outside all solder pads and both QFN bodies. Routing still uses
90/45-degree centerlines. Final DRC, connectivity, schematic parity and ERC
are clean; fabrication/assembly outputs and 3D models were regenerated.

## Retained neck-downs

The residual series transitions occur at the U2 exposed-pad/peripheral-pad
escape, dense FPGA fanout vias, backside connector/signal routing, the ESP
filtered-supply path among C35/L3/L1/C42/R22, the crystal pads, and ground
routing around the USB/keepout region. Narrow sections retain their actual
clearance constraints; the script no longer widens isolated segments merely
because space is available.

## Reproduce / inspect

```sh
tmp/layout-venv/bin/python tools/hardware/audit_trace_widths.py
tmp/layout-venv/bin/python tools/hardware/test_audit_trace_widths.py
```

The audit is read-only and requires KiCad `pcbnew` plus Shapely 2. It accepts
a board path and `--out DIRECTORY`. Coordinates are in millimetres relative
to the drill origin. Reports include board SHA-256, track UUIDs, layers,
widths, full narrow-run lengths and clearance obstacles.

- `trace-width-audit.md`: complete geometric inventory.
- `trace-width-audit.csv`: filterable contact table.
- `trace-width-audit.json`: geometry findings and width-island groups.
- `resolution.json`: final dispositions tied to the board fingerprint.
- `../width-repair-summary.json`: before/after measurements and moved parts.

`apply_width_triage.py` applies unobstructed whole-run widening transactionally,
refills zones and rolls back a batch if DRC is not clean. The former
`normalize_power_widths.py` entry point now uses that guarded workflow.
`repair_width_runs.py` and `reroute_width_necks.py` are explicit candidate
geometry tools: changes require the documented subsequent DRC validation.

The audit conservatively uses configured clearances, but does not certify
custom rule semantics, impedance, thermal performance or current capacity.
RF/thermal/assembly validation remains a prototype release requirement.

After the subsequent ground-tail removal beside C48, the current inventory
is 157 contacts (65 centerline contacts plus 92 copper overlaps). The earlier
158/66 counts above describe the completed width-repair checkpoint.

After the decoupling-placement revision, the current inventory is 164
contacts: 63 centerline contacts and 101 copper overlaps. There are still
no isolated wide islands or unobstructed whole-run widening candidates.
The earlier counts describe historical routing checkpoints.
