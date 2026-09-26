# Layout notes

## Mounting screw between connectors

H1 is located at the midpoint between connector centers J1 and J2, rather
than at the board-outline midpoint. The screw is intended to retain the
module against its mating connectors on the motherboard.

Current placement coordinates (mm):

| Item | X | Y |
| --- | ---: | ---: |
| J1 center | 10 | 16.5 |
| H1 center | 10 | 28.25 |
| J2 center | 10 | 40 |

All three lie on the board's longitudinal centerline. H1 is exactly
11.75 mm from each connector center. Preserve this midpoint relationship
if either connector is repositioned.

H1 has a 3.2 mm clearance hole for an M3 screw and a 7 mm diameter
screw-head/spacer keepout. The mating motherboard's spacer height must
match the connector mating height; the connectors should not serve as
hard stops for screw tightening.

## Fixed 3.3 V FPGA I/O

All FPGA I/O banks are supplied directly from +3.3V. The optional 1.8 V
regulator U5, bypass capacitors C64/C65, and selector SJ1 were removed to
free routing space. C46 and C66 remain as Bank 0 decoupling at U2 pin 33.
Carrier logic and pullups must use 3.3 V levels. The FPGA core remains 1.2 V.


## Routing preparation corrections

L1/L2 now use the original specified Murata BLM18KG101TN1D part with the
manufacturer's 0603 footprint, 100 ohm impedance at 100 MHz, and 30 milliohm
maximum DCR. The source's 0402 geometry and "1nH 70mOhm" display were inconsistent
with that part. Supplier candidate is C160981, replacing the unrelated original
candidate. Manufacturer reference:
https://www.murata.com/en-us/products/productdetail.aspx?partno=BLM18KG101TN1%23

L4's display now states its nominal 2.2 uH value; the incorrect 1.9 A saturation
claim has been removed. The selected XFL3012-222MEC still requires checking
against the operating load and ripple current during power validation.

Small passive references have moved to F.Fab to reduce silkscreen clutter.
The board outline, connector centers and mounting-hole center remain fixed.

## Routing workflow

Critical RF matching, crystal, USB, and buck switch-node traces are authored in
`tools/hardware/route_critical.py`. The remaining routing uses coordinated pad
escapes followed by clearance-constrained path searches. In1.Cu is primarily
ground; local signal escapes are permitted near the ICs, outside the antenna,
USB return region, and central regulator/mounting area. Intermediate routing
files in `tmp/module-layout/` are not manufacturing outputs. KiCad DRC and
schematic parity checks remain authoritative.

U1 is offset 1.5 mm right and U2 2 mm left from the board centerline to open
through-via escape space around the opposed underside connector pads. Connector
centers, the board outline, and the mounting hole are unchanged. The hole remains
at the midpoint of the connector centers so its clamping force tensions both
connectors symmetrically.

`refine_layout.py` is a fresh-placement script and deliberately removes routing;
do not run it on a routed board unless intentionally restarting the layout.
The routed PCB is the authoritative copper layout. Fabrication exports are gated
on connectivity, schematic parity, ERC, and a separate via/pad overlap audit.
RF, thermal, and assembly validation are still required before production.

## Silkscreen density

Keep only U1, U2, J1, J2 and SJ1 reference labels on silkscreen, alongside
the antenna keep-clear and connector function markings. Other component
references remain on the fabrication layers for assembly and inspection.
The board title is omitted to keep the solder-jumper area clear.

## Dense escape fabrication requirements

Signal escapes now use 0.30 mm copper / 0.15 mm drilled through-vias where
needed, with 0.10 mm minimum track width and clearance. Thermal and main power
vias remain 0.40 / 0.20 mm; constrained local supply escapes may also use
0.30 / 0.15 mm vias. These are mechanically drilled through-vias,
not blind microvias. The board remains four layers and 1.0 mm thick.
The 0.15 mm drill requires the fabricator's small-hole process and may add cost;
vias are now outside component solder pads, including the exposed ground pads.
Do not let the order system enlarge the drill automatically. Verify thermal
performance with the revised external ground fanouts.

Capability reference checked 2026-09-23:
https://jlcpcb.com/capabilities/Capab

## Carrier connector pin assignments

General-purpose signal contacts are assigned for compact fanout routing rather
than numerical GPIO order. This is a copper/connector mapping change, not a
hardware multiplexer or a change to the ESP32/FPGA pin functions. Power, ground,
USB, EN and BOOT contacts remain fixed. J1 contact 16 is now NC. UART contacts and FPGA bank signals
follow the final map in `carrier-pinout.csv`; its per-signal voltage notes must
be used when designing the motherboard. `pinout-overrides.json` preserves this
map when regenerating the extraction and schematic.

Vias are kept outside solder pads on both board faces, including QFN exposed
pads. `check_via_pad_clearance.py` verifies this independently of normal net
clearance checks, and the fabrication exporter refuses pad-overlapping vias.

## Previous revision: external via routing completion — 2026-09-24

All through-vias are outside solder pads on both faces and tented on both sides.
The footprint locations, board outline, connector centers, and mounting hole
are unchanged. Local ground connections replace the former in-pad thermal vias;
check IC temperatures on the assembled prototype.

The final cleanup swaps J1 contacts 35/39 (GPIO18/GPIO7) and J2 contacts 5/7
(IOB_9B/IOB_2A). The current carrier CSV, schematic, and extraction overrides
include those assignments. Chip pin functions and I/O supply-bank constraints
have not changed.

`fanout-plan.json` records the coordinated initial escape plan, not a replay of
the completed routing. Later local escape refinements are in `module.kicad_pcb`;
do not apply the seed plan over the completed board.

Checks for that previous revision: 0 DRC violations, 0 unconnected items, 0 schematic parity issues,
0 ERC violations, and 0 via/pad overlaps across 262 vias. Assembly exports contain
50 placements (48 top, 2 bottom). Gerber, drill and placement exports share the
auxiliary origin at native KiCad (100, 100) mm; the placement CSV retains KiCad's
negative-Y convention. Inspect side/rotation in the assembler's preview.

## Complementary connector revision

J1 remains DF40C(2.0)-40DS-0.4V(51); J2 is now DF40C-40DP-0.4V(51).
Both lie horizontally at their existing centers; H1 remains their exact midpoint.
U1/U2 are centered on x=10 mm. Their adjacent decouplers move to preserve
package clearance. See carrier-keying.md; earlier routing observations below
refer to the superseded perpendicular-receptacle layout.

### ESP32 reroute completed — 2026-09-25

Power, ESP32–FPGA links, and GPIO/USB routes are complete. The current J1 carrier assignments are in `carrier-pinout.csv`, `module-connectivity.json`, and `pinout-overrides.json`; these supersede the intermediate connector assignments from the fanout work. The schematic was regenerated from the same connectivity source. GPIO numbers and chip functions were not reassigned.

L1's ESP_VDD via moved from between its pads to local (18.7875,10.35), above and outside its body. R22 and C32 are aligned at y=9.7 mm, with their EN pads facing each other and a short straight connection; C32 ground exits away from the group. Updated placement coordinates are in `placement.json`.

All signal/power vias remain outside QFN bodies and all component pads. Vias use at least 0.45 mm copper / 0.20 mm drill. Component-side QFN routing stays outside the bodies except the intended exposed-pad ground connections. Ground islands at J1 have explicit plane connections. Copper zones are refilled.

QSPI matching detours were removed at the user's request. Current track-centerline totals: IO3 29.186 mm, CS 29.803 mm, MOSI 29.992 mm, SCK 32.358 mm, MISO 34.790 mm, IO2 29.717 mm. Longest–shortest spread: 5.604 mm. These exclude via-barrel and package delays. USB D− 8.293 mm and D+ 8.334 mm, one via each, unchanged.

Validation and measurements are under `fab/checks/`. Refreshed fabrication and assembly files are engineering previews; antenna reference artwork, RF tuning and final assembly-part verification remain release gates. See `docs/antenna/STACKUP-AND-FEED.md`.

### Ground-tail cleanup — 2026-09-25

Removed seven redundant F.Cu GND segments beside C33 and the left side of H1: the C33 pad tail and the unused branch ending at the (6.7,30.925) stitching via. Retained the stitching vias and capacitor return connection. These tails escaped dangling-track DRC because they were connected to the ground pour. Refilled zones and regenerated exports; DRC, connectivity and schematic parity remain clean.

### Regulator via access — 2026-09-25

Removed U4's three under-body 3.3 V vias and replaced them with one accessible via beside C62 at local (1.775,21.5). Its enable/input tie runs around the package's left side; the supply joins the existing outside via on B.Cu. Moved U3's edge-overlapping ground via from (14.85,24.55) to (14.4,24.8), with its pad connection rerouted. No regulator-body via overlaps remain.

### ESP32 south-side and schematic cleanup — 2026-09-25

The 5 V connector feed now follows the outer right-hand corridor to a via above C60, clear of the ESP32 fanout. Removed overlapping output/feedback copper beneath U3 and three dangling power items. R20 now sits beside its BOOT via. GPIO16/17/18 use shorter inner-layer escapes; J1 pins 36/37/38 are now GPIO17/GPIO16/GPIO18 respectively, synchronized in schematic and carrier pinout.

C6/C7 are mirrored around the crystal at local (17.5,12.4) and (18.1,17.6), with opposite orientations and accessible ground vias. Their outer pad edges are at least approximately 1.1 mm inside the right board edge.

Combined ESP32 RF matching, antenna selection, chip tuning and U.FL into one schematic block. Aligned section edges into three columns and grouped supply filtering with its respective decoupling. This is presentation-only for the schematic topology.

### Final FPGA GPIO breakout — 2026-09-25

U2 pin 44 (IOB_3B_G6) now connects to J2 pin 33 as FPGA_IOB_3B_G6, replacing that contact's GND assignment. Seven other J2 ground contacts remain. This changes the carrier pinout: J2.33 must not remain grounded on a mating motherboard. Added one 0.45/0.20 mm via outside the FPGA body and adjusted adjacent backside routes for clearance. Schematic metadata, pinout overrides and carrier CSV are synchronized.

Added short schematic wire tails at crystal/RF block boundaries and regulator outputs. Moved R62 beneath L4, tightened output-capacitor spacing, and aligned passive values directly beneath reference labels. Inductor text is raised where the feedback/filter wiring would otherwise cross it.

### Passive alignment and copper cleanup — 2026-09-25

Rotated C45 by 180 degrees to 0 degrees and centered it at local (3.3,34.2), matching L2. Its ground via is now outside the body at (3.7,33.3). R28/R29 moved to x=17 mm, aligned with C50/C52; capacitor positions are preserved. Simplified C61/C67 ground connections and the L4-to-output-capacitor supply path. Replaced the stepped/tail-bearing 3.3 V branch below H1 with one 0.25 mm route; this branch is necessary to connect the power copper, not a redundant tail. Removed the two redundant 3.3 V vias near (4.875,31.2)/(5.475,30.7) and the isolated via/stub at (10.75,24.025). Retained the (6.7,30.925) GND via connecting F.Cu, B.Cu and In1 ground pours. Simplified the U4 output trace while preserving clearance to its lower pins. H1/L1 references hidden, including duplicate footprint reference text; silkscreen script preserves that choice.

### Thermal-relief policy — 2026-09-25

All copper zones now default to thermal-relief component-pad connections: 0.15 mm gap/spokes, with zone minimum thickness 0.10 mm. J1/J2 fine-pitch pads use 0.10 mm gap/spokes. C42 uses diagonal spokes to avoid nearby routing. J1.30, J1.31 and J2.23 cannot form adequate automatic reliefs in the routed geometry, so they instead use explicit 0.10 mm copper necks with direct zone attachment disabled. Connectivity and thermal-starvation DRC must remain clean after refilling.

Solid exceptions: U1/U2 exposed ground pads, U3 exposed thermal pad, AE1 RF ground and J3 shield grounds. Vias retain solid plane attachment. See `fab/checks/thermal-reliefs.json`; `tools/hardware/apply_thermal_reliefs.py` reapplies the settings and explicit necks. This changes copper geometry, including RF shunt-capacitor ground connections; existing RF validation/tuning release gates still apply.

Silkscreen follow-up: U1 and U2 labels moved into open right-side space at local (18.1,19.7) and (18.1,36.5). J3 moved to the connector's left at (2.2,4.0); L3's reference and duplicate Fab reference were hidden. Placement preferences persist in place_silkscreen.py. Native 3D render and DRC confirm the labels are clear of components/pads.

### Ground-via cleanup, 2026-09-25
Removed seven redundant GND stitching vias around C6/C7, northwest of U3,
south of ESP32, and southwest of the M3 hole, including associated leftover
trace branches. Removed the separate R28 pulldown ground via; the filled top
GND pour retains its thermal connection. Kept the FPGA decoupling return vias:
C43/C44/C46/C49/C50/C52/C66 have a nearby inner-plane return approximately
0.8 mm from the ground pad center; C45's is approximately 0.975 mm away.
These serve local capacitor return paths, distinct from the top-pour thermal
spokes. Connectivity checks do not establish high-frequency impedance.

C66 reservoir placement: moved to (3.3,42.65) mm relative to board datum, beside C46; added direct 0.25 mm connection to C46 and its FPGA pin 33 feed. Consolidated their power-plane connection and moved C66 ground via with the capacitor. DRC/parity: zero issues.

### ESP32–FPGA link simplification
Removed avoidable 45/90 detours and four duplicate signal segments. Simplified runs use uniform 0.10 mm width (existing project signal minimum). Remaining bends clear pads, vias and the M3 exclusion. Copper centerline lengths, excluding via barrel lengths: /LINK_IO3 29.186 mm, /LINK_CS_N 28.151 mm, /LINK_MOSI 27.453 mm, /LINK_SCK 32.067 mm, /LINK_MISO 34.666 mm, /LINK_IO2 29.702 mm. QSPI spread 7.213 mm; USB unchanged. This is a geometry measurement, not a timing validation.

### Remaining ESP32 GPIO breakout
GPIO38 (U1-42) → J1-39 (previously NC); GPIO45 (U1-50) → J1-34 and GPIO46 (U1-55) → J1-33 (previously GND). J1 retains seven GND contacts, including grounds adjacent to USB and VIN. USB traces unchanged. Added routes use inner copper where existing fanouts obstruct outer-layer paths. Removed the GND stitch at (14.3,13.1) to provide an external-QFN GPIO46 launch. GPIO45/46 carrier reset restrictions are recorded in carrier-pinout.csv; GPIO46 is input-only. Source: https://docs.espressif.com/projects/esp-idf/en/v5.0/esp32s2/api-reference/peripherals/gpio.html

Crystal clearance cleanup: Y1 shifted 0.5 mm downward to (17.8,15.5), C7 shifted to (18.1,18.0); R3 retained at original position, now outside Y1 courtyard. Crystal links rerouted and GND-B thermal spokes rotated 45 degrees to provide a complete thermal connection. DRC/ERC/parity clean; fabrication outputs regenerated.

### Symmetric 25 mm connector spacing and routing cleanup — 2026-09-25

J1 is at local (10,15.75) mm and J2 at (10,40.75) mm: 25.00 mm center-to-center. H1 stays at (10,28.25), exactly 12.50 mm from each connector. Outline and mounting-hole position are unchanged. The complementary plug/socket keying remains.

J2 signal contacts were reassigned for direct fanout; the GPIO numbers/functions on the FPGA itself did not change. J1.21 is now ESP_GPIO40 and J1.22 GND. The current carrier-pinout.csv, pinout-overrides.json and schematic connectivity agree; earlier pin mappings above are historical and must not be used for a new carrier. FPGA IOB_3B_G6 is now J2.32.

Completed all signal and ground connections, removed 72 redundant route segments in the first cleanup pass, and beveled 51 orthogonal corners. Further QSPI cleanup removed a small SCK jog and normalized a MISO junction. Every track is horizontal, vertical or 45 degrees. Trace widths were preserved during simplification. Added two external-body ground stitches to reconnect connector return islands; fine-pitch manual ground necks preserve solderability. All vias remain outside component pads/QFN bodies, and F.Cu avoids QFN bodies except exposed-pad ground connections.

Current copper-centerline lengths (excluding via barrels/package delays): IO3 29.186 mm, CS_N 28.151 mm, MOSI 29.418 mm, SCK 31.949 mm, MISO 34.668 mm, IO2 29.702 mm, USB_D- 9.245 mm, USB_D+ 8.630 mm. QSPI spread 6.517 mm; USB mismatch 0.615 mm, one via per USB signal. USB backside traces use 0.15 mm width to clear the fanout; these geometry checks do not establish controlled impedance or timing closure.

DRC: zero violations, zero unconnected items and zero schematic-parity differences; ERC: zero violations. Regenerated Gerbers/drills, BOM/CPL, schematic PDF and GLB. Antenna reference artwork, stackup/impedance, RF tuning and assembly verification remain the documented release gates.

### 45 mm board length — 2026-09-26

Extended the bottom edge by 0.85 mm, from local y=45.60 to 46.45 mm. The top stays at y=1.45 mm, giving a 20.00 × 45.00 mm outline. Copper pours extend into the new area with the existing 0.30 mm edge setback. Components, routing, H1 and the 25 mm connector spacing are unchanged. Fabrication and assembly outputs were refreshed.

## Exposed-lead buck — 2026-09-26

Replaced U3 with TPS62160DGKR VSSOP8 and added R64/R65 feedback divider. Repositioned C60, rotated L4/C61/C67, rerouted input/switch/output and a separate VOS sense connection. Pin-one dots remain only on orientation-sensitive parts. See `inspectable-buck-option.md`; canonical placement and connectivity JSON are updated. Historical initial-import/routing scripts are not full reconstruction scripts for the current board.

## Crystal passive alignment — 2026-09-26

R3/C6 form the upper row (absolute y=113.2 mm), C39/C7 the lower row (y=117.8 mm). Column centers are x=116.7/118.3 mm. Both rows are 2.3 mm from Y1 center. R3 stays fixed; C6/C7/C39 moved slightly, and their short copper connections were adjusted. Original capacitance/resistance values and nets are unchanged. DRC, connectivity and schematic parity are clean with the existing JLC rules.
