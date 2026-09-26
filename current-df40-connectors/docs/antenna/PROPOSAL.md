> Historical Abracon proposal, superseded by the Pulse integration in INTEGRATION.md. Do not use these old coordinates or part numbers for assembly.

# Replace the module PCB antenna with Abracon ACAG0201-2450-T

**Handoff revision B — 2026-09-24.** Component CAD and proposed placement are complete. This is an integration proposal, **not released RF artwork or a fabrication package**. No production schematic, PCB, routing, or fabrication outputs were edited.

## Revision B: selectable external antenna

Read **EXTERNAL-ANTENNA.md** for the new U.FL port, default chip connection, and marked cut/solder procedure. This revision adds JP_ANT before the chip tuning network, so external mode disconnects the complete chip branch. The updated drawings and placements.json are authoritative. Original chip-footprint dimensions and unresolved RF-release gates below are unchanged.

## Decision and scope

Replace AE1's etched radiator with ACAG0201-2450-T at the existing antenna end. Keep the 20 × 44.15 mm board outline and the ESP32/FPGA/connector placements unchanged for the first prototype. Add a dedicated antenna-tuning π network while retaining the existing ESP32 matching network as the initial baseline. Carrier clearance is part of this change.

The footprint can be integrated now. Before releasing antenna copper, resolve the reference-layout ambiguity with Abracon and obtain the fabricator's actual stackup. Matching values and performance then require measurement on the populated module and carrier. A small package or successful DRC cannot establish antenna efficiency.

## Deliverables

- `Abracon.pretty/ACAG0201-2450_2.0x1.25mm.kicad_mod`: real two-pad SMD footprint, assembly outline, polarity marker, courtyard, paste/mask, and model reference.
- `Abracon.kicad_sym`: two-pin symbol with explicit RF/GND functions and correct footprint assignment.
- `3dmodels/ACAG0201-2450.wrl`: illustrative nominal mechanical envelope; not vendor geometry or an RF model.
- `antenna-floorplan.kicad_pcb`: four-layer, placement-only integration template in the parent board's absolute coordinates. It contains six new/proposed components, reservation rule area, and non-copper feed guides. Other parts are approximate drawing-layer context only. **Do not replace the production PCB with this file.**
- `placements.json`: precise proposed component positions and pad/net assignments. Symbolic new references must be allocated to unused numeric references during integration.
- `drawings/footprint.svg`, `floorplan.svg`, `rf-topology.svg`, `stackup-carrier.svg`: dimensioned review drawings.
- `calculations/cpwg.py`, `cpwg-sweep.csv`: reproducible transmission-line planning calculations.
- `build.py`: regenerates proposal CAD and first three drawings, using system Python and KiCad 10 pcbnew.
- `validate.py`, `validation.json`, `floorplan-drc.json`: geometric and parser checks. DRC: zero physical violations; nine unconnected items expected because this is intentionally unrouted.
- `ABRACON-QUESTIONS.md`: exact missing vendor information, prepared for inquiry but not sent.

## Coordinate system and fit

All coordinates below are **absolute KiCad mm**, top view, X right and Y down. Existing board bounds are X=100…120, Y=101.45…145.60. Do not subtract 100 when placing in the production board.

| Feature | Position / extent | Status |
|---|---|---|
| AE1 center | (116.000, 103.075), rotation 0°, F.Cu | Proposed |
| AE1 pad 1, RF | (115.300, 103.075) | Exact footprint transform |
| AE1 pad 2, GND | (116.700, 103.075) | Exact footprint transform |
| Antenna planning reservation | X=114.5…117.5; Y=101.45…106.45 | 3 × 5 mm envelope; **not final shaped ground cutout** |
| R_ANT series tuning element | (112.400, 103.075), 0° | 0402; initial 0 Ω |
| C_ANT_IN | (110.800, 103.555), −90° | 0402; initial DNP |
| C_ANT_OUT | (114.000, 103.555), −90° | 0402; initial DNP |
| C34 | Existing location (117,108) | Retained; context drawing is approximate |
| Suggested carrier leading edge | Y≥107.50 | Initial overhang arrangement; not a measured RF limit |

Existing antenna keepout is X=101…119, Y=101.45…107.50 (18 × 6.05 mm). New reservation fits inside it: left/right margins 13.5/1.5 mm, trailing margin 1.05 mm. Nominal ceramic is 1.0 mm from the board's leading edge; maximum-sized centered body reduces this to 0.90 mm. Courtyard leading-edge clearance is 0.65 mm. These are mechanical fit calculations, not Abracon placement tolerances.

Reservation area is 15 mm² versus the old 108.9 mm²; the 93.9 mm² difference is **not automatically usable layout space**. Matching components, ground currents, feed clearance, and carrier interaction still constrain it. Preserve board outline until RF validation.

## Footprint dimensions and assembly

The explicit land pattern on Abracon datasheet p.5 takes precedence for the component pads:

- Pad 1 center (−0.70,0), pad 2 (+0.70,0); each rectangular 0.60 × 1.25 mm.
- Pitch 1.40 mm; copper gap 0.80 mm; total copper span 2.00 mm.
- Pin 1 is INPUT, pin 2 GND, per the function table on p.4. Keep marked end aligned with pad 1; do not treat the antenna as a nonpolar capacitor.
- Body nominal 2.00 × 1.25 × 0.60 mm, maximum 2.20 × 1.45 × 0.70 mm.
- Courtyard 2.70 × 1.95 mm: maximum body plus 0.25 mm on each side, our assembly allowance.
- Paste apertures equal copper; solder-mask expansion +0.05 mm on each side, our starting process choice. Verify stencil/paste process with assembler; do not silently resize copper.
- Silkscreen uses short lines and a pad-1 mark, kept clear of mask openings. Final board reference location must be checked after integration.
- The 3D file depicts nominal external volume and terminal surfaces only. Copy it to the production project's `3dmodels/` directory or update the footprint model path.

## Electrical change and explicit old-to-new mapping

Parent snapshot: AE1 `P$1` is GND; `P$2` is `/RF_ANT`. **Do not map these by numerical resemblance.** New AE1 **1 → antenna RF**, **2 → GND**.

Existing path: U1 RF pin 2 on `/RF_IN`, existing C1/L3/C2 matching network, `/RF_ANT`, old radiator. Preserve the existing network initially; its inherited 3.3 pF / 2.2 nH values are not asserted to be optimized for this antenna.

New path: existing `/RF_ANT` feeds JP_ANT common; JP_ANT chip output `/RF_CHIP` feeds the following network. JP_ANT external output `/RF_EXT` feeds J_EXT, bypassing this chip-specific network.

```
JP_ANT chip output ──┬── R_ANT ──┬── AE1 pin 1
                  │           │
               C_ANT_IN    C_ANT_OUT
                  │           │
                 GND         GND

AE1 pin 2 ── prescribed short ground connection ── GND
```

Use `/RF_ANT_MATCH` for the series element's antenna side in the integrated hierarchical schematic. The template's unprefixed `RF_ANT`/`RF_CHIP`/`RF_EXT`/`RF_ANT_MATCH` names are local placeholders; schematic-generated nets remain authoritative. The shunt capacitors' pad 1 is on the signal row at Y=103.075 and pad 2 at Y=104.035 is GND. Series element pad 1 faces input/left, pad 2 faces antenna/right.

Initial tuning population is series 0 Ω and both shunts DNP. This is a measurement starting point, **not a working-value guarantee**. The old EVB note's 0.5 pF and 6.5 nH values are not a BOM prescription for this module. Use RF-grade high-Q inductors and C0G capacitors with appropriate self-resonance for final tuning; choose actual values from measurement.

## Ground and routing instructions

1. Remove the old AE1 footprint **including its printed antenna copper**, its obsolete RF/GND fanout, and obsolete antenna-specific keepout. Preserve unrelated routes. Update the generator if it owns those objects, so regeneration cannot restore the old antenna.
2. Place the new antenna and tuning parts at the provided coordinates. The KiCad template has no courtyard overlap; adjust only after reviewing RF geometry.
3. The 3 × 5 envelope is a planning reservation. Abracon p.6 contains **shaped ground and feed islands**, not an empty rectangle with arbitrary wires across it. Obtain/confirm current reference CAD and reproduce the required geometry before fabrication.
4. The provisional template rule area blocks zone fill and vias on F.Cu, In1.Cu, In2.Cu, and B.Cu. Tracks/pads are deliberately allowed for future prescribed geometry. It does **not** enforce RF correctness or prevent unrelated traces. Audit all layers and replace it with the final shaped restrictions. Do not copy a rectangle and assume the antenna is finished.
5. Only the intended antenna feed/terminal/ground geometry may enter the RF clearance. Keep inner/bottom copper, unrelated signals, vias, and components out of the required clearance. Ground outside the clearance should be continuous and tied between layers.
6. Restore the appropriate ground outside the final clearance, particularly under/beside the matching network and feed. Retaining the old broad keepout would deprive the new CPWG path of its reference plane.
7. Route F.Cu grounded coplanar waveguide from the existing RF network into the new π network; keep it short and avoid signal-layer transitions. Its ground-backed portion needs uninterrupted In1.Cu GND. The terminal/cutout transition is antenna-specific and is not described by a uniform CPWG formula.
8. AE1 pad 2 requires a short, broad connection into the vendor's ground geometry, not a long skinny wire to distant GND. Place ground vias outside the RF clearance and SMD pads; no new via-in-pad is required.
9. Reserve a ground-via row beside the feed, initially ≤1 mm pitch, subject to DRC and the final vendor geometry. This is a conservative design target, not a vendor requirement. Do not scatter vias into the antenna cutout.
10. Do not route a permanent tee/testpoint stub on the RF feed. For tuning, remove R_ANT to isolate the radio and attach temporary coax at its antenna-side pad plus adjacent ground. Account for the launch/cable by calibration/de-embedding; then remove coax and restore the tuned series part.

## Transmission-line calculations and missing stackup

The inspected board has four copper layers and 1.0 mm overall thickness, but no explicit dielectric stackup. **Overall thickness is not the F.Cu–In1.Cu separation.** Required fabrication inputs: pressed dielectric height to In1, frequency-appropriate Dk, finished top copper thickness/etch geometry, solder-mask thickness/Dk, and controlled-impedance tolerances.

`calculations/cpwg.py` implements Qucs grounded-CPW equations 12.10–12.13 using complete elliptic integrals evaluated by AGM. For width w, gap s and ground depth h:

```
k1 = w / (w + 2s)
k3 = tanh(pi*w/(4h)) / tanh(pi*(w+2s)/(4h))
A = K(k1)/K(sqrt(1-k1²)); B = K(k3)/K(sqrt(1-k3²))
effective_er = 1 + (er-1)*B/(A+B)
Z0 = 60*pi / (sqrt(effective_er)*(A+B))
```

At assumed er=4.2 and side gap s=0.15 mm, the **zero-copper-thickness, no-mask planning** widths for 50 Ω are:

| Assumed F.Cu–In1 separation | Calculated width |
|---|---|
| 0.10 mm | 0.197 mm |
| 0.12 mm | 0.231 mm |
| 0.15 mm | 0.280 mm |
| 0.20 mm | 0.354 mm |

These are **not final trace widths**. Copper thickness and mask matter at these dimensions. Have the fabricator/field solver determine final w/s with actual stackup; target 50 Ω, proposed tolerance ±10%. Include a controlled-impedance coupon if supported.

Example h=0.12, er=4.2 gives effective er≈3.114 and guided wavelength≈69.34 mm at 2.45 GHz. A 1 mm via pitch is about lambda_g/69. Antenna matching cannot be calculated from these transmission-line equations without the assembled antenna impedance/S-parameters.

## Carrier and enclosure

Initial mechanical arrangement: extend the module's antenna end beyond the carrier so the carrier leading edge is at Y≥107.50 in module coordinates. This exposes the full original antenna band (6.05 mm) beyond the carrier, with 1.05 mm beyond the proposed reservation's trailing boundary. This is a sensible starting floorplan, **not a proven sufficient electromagnetic separation**.

If overhang is impossible, provide a carrier cutout/clearance proposal and have it reviewed/tuned as part of the assembly; copper removal alone does not make the dielectric and surrounding metal irrelevant. Keep fasteners, shields, cables, and conductive enclosure features away from the antenna end. Test in the actual intended enclosure and mating-board configuration. Preserve the existing mounting-hole and connector relationship.

## Integration sequence for the bp-test agent

1. Compare the current production board against the captured geometry; parent work may have advanced. Take a checkpoint before the change.
2. Copy footprint/symbol/model into project-local libraries. Merge library-table entries; **do not overwrite existing tables**. Existing Module library names can be used if both symbol footprint field and PCB ID are updated together.
3. Change schematic AE1, map old P$2 RF to new pin 1 and old P$1 GND to new pin 2, add the three tuning positions, JP_ANT selector and J_EXT port, and update the generator/source of truth. Allocate unused references and document DNP assembly variants.
4. Add the new placements, replace old antenna copper/keepouts with confirmed current reference geometry, and reroute the local RF section. Leave the remaining module intact.
5. Finalize stackup and CPWG dimensions, inspect all-layer clearance and RF return continuity, refill zones, run ERC and DRC **with schematic parity**, and verify zero unconnected items on the real board.
6. Update board/antenna notes, BOM/CPL and assembly drawings. Antenna order code is ACAG0201-2450-T; JLC listing is C3284598, but stock/assembly allocation is unverified. Do not equate catalog presence with procurability.
7. Generate Gerbers/drills/3D from the integrated PCB, inspect inner layers, and check antenna pin orientation and DNP markings in the assembly preview.
8. Build/tune prototypes before production release. Reissue final RF BOM after tuning.

## Validation and release gates

Completed: KiCad footprint and floorplan parser checks; symbol SVG export; exact pad size/pitch/net checks; all-four-layer reservation check; physical floorplan DRC; dimensioned drawing review. Nine airwires remain by design in the placement template. No ERC/parity success is claimed for the unintegrated proposal.

Outstanding gates:
- Abracon confirmation/reference CAD for current copper geometry and apparent 0.7/0.8 mm dimension discrepancy, plus pin-mark orientation confirmation for the supplied lot if needed.
- Actual fabrication stackup and finite-copper/mask CPWG solution.
- Antenna matching on the assembled module/carrier. Proposed return-loss goal ≥10 dB across 2.400–2.4835 GHz; if this cannot be met, evaluate measured efficiency and product link requirements rather than silently changing the criterion. This goal is a project target, not Abracon's guarantee.
- Radiated efficiency/pattern or controlled OTA link testing across orientations; return loss alone can hide dissipative loss.
- Check final antenna choice/integration against the product's applicable radio certification plan.

## Sources

- Abracon ACAG0201-2450-T datasheet, revised 2025-09-20, pp.4–6: https://abracon.com/datasheets/ACAG0201-2450-T.pdf — copied under `sources/`.
- Abracon EVB note, revised 2025-03-11: https://abracon.com/datasheets/ACAG0201-2450-EVB.pdf — older reference; not used for production matching values.
- Qucs grounded CPW equations 12.10–12.13: https://qucs.sourceforge.net/tech/node86.html.
- Parent PCB snapshot geometry inspected read-only: `/home/meawoppl/repos/bp-test/boards/esp32-fpga-module/module.kicad_pcb`. See `baseline.json` for hash/time.
