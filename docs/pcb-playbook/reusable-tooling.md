# Reusable tooling: what to lift out of `tools/hardware`

`tools/hardware/` has about 70 scripts (≈4.3k lines) written during the
session. **Almost all of them hard-code** `boards/esp32-fpga-module/module.kicad_pcb`,
refs like `U1`/`U2`, or net names like `/RF_*`. They are good prototypes but
not yet a library. This file ranks which ones earn generalization and sets
out the shape of a shared library.

## Target shape

A small package (e.g. `pcbtools/`, or folded into the Backplane plugin
alongside the `kicad-*` skills):

```
pcbtools/
  board.py        # load/save, snapshot+revert, zone refill, run DRC/ERC via kicad-cli
  guard.py        # @drc_guarded transaction: apply → refill → DRC+parity → keep/revert
  geometry.py     # pad shapes (circle/oval/roundrect), octilinear helpers, run/graph building
  config.py       # per-board YAML/JSON: QFN refs, protected nets, decoupling map, plane nets
  audits/         # read-only, emit JSON + CSV + Markdown into docs/
  fixes/          # mutating passes, all DRC-guarded
  export/         # fab outputs, JLC CPL offsets, release snapshot
```

Hard-coded values become a per-board config, e.g. `boards/<b>/pcbtools.json`:

```json
{
  "pcb": "module.kicad_pcb",
  "no_via_under": ["U1", "U2"],
  "protected_nets": ["/RF_*", "/XTAL_*", "/USB_D*", "/BUCK_SW"],
  "plane_nets": ["GND", "+3V3"],
  "decoupling": {"U1": {"3": "C35", "45": "C39"}, "U2": {"29": "C44"}},
  "length_groups": {"qspi": ["/QSPI_*"], "usb": ["/USB_D+", "/USB_D-"]}
}
```

## Tier 1: generalize first (board-agnostic value, covers checklist gaps)

| Script | Becomes | Why |
| --- | --- | --- |
| `audit_trace_widths.py` (+ test) | `audits/width_transitions` | Finds width islands/necks. Already has argparse and tests; only the default paths are board-specific. |
| `check_via_pad_clearance.py` | `audits/via_in_pad` | Real pad-shape overlap check. Needs the QFN list from config. |
| `check_qfn_front_routing.py` + `routing_constraints.py` + `add_qfn_via_keepouts.py` | `audits/under_package` + `fixes/package_keepouts` | "No vias under QFN / no F.Cu under QFN" as both an audit and a DRC rule. |
| `audit_decoupling_placement.py` | `audits/decoupling_distance` | Pin→cap distance. The pin map moves to config. It could auto-infer from netlist (nearest cap on same supply net). |
| `straighten_routes.py`, `octilinear_escape.py` | `fixes/octilinear` | 45°/90° enforcement. |
| `merge_collinear_tracks.py` | `fixes/merge_collinear` | Trivially generic. |
| `trim_unused_copper.py`, `prune_unused_routes.py`, `prune_signal_trees.py`, `remove_orphan_signal_copper.py`, `remove_orphan_plane_copper.py` | `fixes/prune` (one tool, modes) | Stub/tail/orphan removal. Covers KiCad's dangling-track blind spot. Consolidate five near-duplicates. |
| `remove_redundant_pad_vias.py`, `clean_copper.py` | `fixes/redundant_vias` | With a "keep decoupling/RF return vias" policy. |
| `remove_via_in_pad.py` | `fixes/via_out_of_pad` | Generic relocation plus DRC guard. |
| `apply_thermal_reliefs.py` | `fixes/thermal_reliefs` | Policy: spokes for ordinary pads, solid for EP/RF. |
| `add_visible_pin1_markers.py` | `fixes/pin1_dots` | Needs a "has polarity" heuristic instead of ref skips. |
| `place_silkscreen.py` | `fixes/silkscreen` | Uniform size, hide passives, corner placement, avoid vias. |
| `carrier_export.py` + `jlcpcb-placement-offsets.json` | `export/jlc` | CPL with LCSC-keyed rotation/offset table and native-rotation assertion. **Also share the offsets table across boards.** |
| `export_module.py` | `export/fab` | ERC/DRC/Gerbers/drill/BOM/CPL/STEP/GLB plus hash manifest. Overlaps the `kicad-export` skill; merge into it. |

## Tier 2: worth extracting with more work

| Script | Notes |
| --- | --- |
| `repair_width_runs.py`, `reroute_width_necks.py`, `widen_power_routes.py`, `normalize_power_widths.py`, `apply_width_triage.py` | Consolidate into one "normalize run widths" fix driven by the width audit. |
| `optimize_connector_fanouts.py`, `optimize_open_connector_assignments.py` | **Connector repinning**: assign movable GPIO nets to the nearest free contact to uncross routes. Very reusable for any board-to-board module; needs a "movable contacts" config. |
| `apply_coordinated_fanout.py`, `apply_external_fanouts.py` | Staggered near/far external QFN fanout planner. Valuable but tightly coupled to pad geometry; generalize by package pitch/side. |
| `stitch_planes.py`, `connect_plane_components.py` | Plane stitching with clearance checks. |
| `grid_route.cpp`, `grid_ripup.cpp`, `route_grid.cpp`, `finish_routing.py`, `ripup_*` | Custom grid router. Compare it against Freerouting (see `logs/freerouting.log`) before investing. Keep it only if it beats Freerouting on residual nets. |
| `color_connector_models.py`, `attach_3d_models.py`, `build_package_models.py` | 3D model attach/finish (gold pins). Generic with a model map. |
| `generate_bom.py`, `carrier_bom.py` | Group by LCSC/MPN. Merge into the `kicad-bom` skill. |
| `devboard_names.py` | Net rename map. Generic if driven by a CSV. |

## Tier 3: leave as project history

One-time ECOs and board builders: `extract_module.py`, `build_schematic.py`,
`build_placement.py`, `refine_layout.py`, `add_rgb.py`, `add_vccio_selector.py`
(retired), `revise_carrier_keying.py`, `replace_antenna_pulse.py`,
`convert_ufl_only.py`, `build_*antenna_model.py`, `carrier_*` builders,
`audit_import.py`. Keep them for provenance; don't generalize.

## New checks that should exist (gaps found by review)

- **Stub detector** that also catches tails touching same-net copper.
- **Orphan-via detector**: vias whose removal leaves connectivity unchanged
  and that aren't tagged as return/stitching vias.
- **Pad-exit check**: the trace endpoint is off the pad centerline, or the
  first bend is inside the pad.
- **Grazing-pad check**: a track overlaps a pad it isn't meant to terminate on.
- **Length-group report** (QSPI/USB spread) from config.
- **Stale-output check**: source hashes vs `revision-sha256.json`. Fail the
  export or the portal badge when they differ.
- **Silkscreen occlusion check**: reference text overlapping vias, pads, or
  package bodies.

## Suggested path

1. Create `pcbtools/` with `board.py` + `guard.py` + `config.py`, and port the
   Tier 1 audits (read-only, lowest risk). Run them on all three boards to
   prove they're board-agnostic.
2. Port the Tier 1 fixes behind the DRC guard.
3. Hand the audits to the Backplane plugin as a "Layout quality" check tab
   next to ERC/DRC, so they appear in the portal.
4. Move the JLC offsets table to a shared location (plugin data or a repo
   such as `pcb-common`) keyed by LCSC number, so each correction is verified
   once.
