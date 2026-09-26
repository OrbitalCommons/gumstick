# Layout preferences

These are stated preferences. Where a rule came from a specific correction, the
triggering example is in *italics*.

## Board shape and mechanics

- **Tight outlines.** Trim the board to the functional extents (e.g. antenna
  edge to bottom of the last connector), then adjust to a round number if
  requested (the module went 44.15 → 45 mm).
- **Centerline everything.** Mount holes, board-to-board connectors, main ICs,
  and the RF connector align on the board's longitudinal centerline. *"Please
  center the 2 QFN packages along the vertical centerline"; "Align that
  connector spot with the board centerline too."*
- **Screws clamp connectors.** A single central M3 goes at the midpoint
  between the mating connectors, not at the board's geometric center, because
  it tensions them. Record the dimension in a notes file. Round, symmetric
  numbers are preferred (connectors 25 mm apart, 12.5 mm each side of H1).
- **Match spacer height to connector stack height** so tightening can't crush
  the connectors.
- **Keying by physics, not silkscreen.** For board-to-board pairs, use one
  plug and one receptacle (M/F keying) in the same connector family. Pin
  count or position asymmetry also works, but M/F was preferred because it
  adds no unused contacts.
- **Gum-stick form factor** for modules: RF at one end → MCU → hole → FPGA →
  connectors under. Regulators to the left/right of the center hole.
- **Check mechanical clearance of mating boards** (daughterboard vs USB jack)
  against the *ordered* outline, and report the actual margin.

## Placement

- **Power first.** Place regulators next to where their rails are consumed,
  and put the decoupling right at the supply pins. Check each decoupler's
  distance to its pin; don't assume. *FPGA PLL caps were 9–10 mm away on the
  other side of the package and still passed DRC.*
- **Filters look like filters.** A π filter is placed compactly, e.g. `|_|`,
  on the side of the IC it feeds. *"Does it make more sense for those
  components to be on the left side of the QFN?"* Yes: it removed two vias
  and a bottom-layer detour.
- **Align and orient passive groups.** Same-size passives around a crystal
  or beside an IC are placed in tidy rows/columns with consistent orientation.
  Rotate passives 180° when that makes power/ground land nearer their vias.
  *"Rotate and align R20 with C41."*
- **Keep clearance for connectors.** Leave generous room around RF/U.FL and
  USB, and keep noisy or tall parts out of RF zones. *"Rotate C34 down to keep it
  away from the RF zone."*
- **Keep crystal load caps symmetric** and away from the board edge.
- **Shorter RF beats pretty RF.** The U.FL moved to a straight shot above the
  matching network (3.61 → 2.61 mm) at a small aesthetic cost. On a small
  module, an external U.FL is preferred over a chip antenna with a long feed and a
  keepout.
- **Consolidate bulk caps.** Replace one oversized cap with parallel parts in
  the board's standard size. Check capacitance under DC bias: a 22 µF 0603
  is about 10 µF at 3.3 V, so use two.

## Routing

- **Octilinear only**: straight runs with 45° miters. No point-to-point
  diagonals, no wiggles, and no polygonal approximations of circles around
  keepouts (use 45° miters around the M3 exclusion).
- **One width per run.** Width steps are only acceptable where clearance
  forces a neck-down, and then they should be deliberate and short. *"I still
  see a lot of unnecessary line width changes, make a script that finds all of
  them and triage."*
- **Straight pad exits.** Traces leave a pad centered and straight, and bend
  only outside the pad. *"There are lots of places the trace could come
  straight out of the pad, but it is instead offset."*
- **Don't touch neighboring pads.** A feed that barely overlaps a second pin
  is a defect, even when both are the same net. Route it centered into each pad.
- **No routing under QFNs on the component side.** Other layers are OK.
- **Order: power → critical signals → I/O.** For the ESP32 module:
  1. Power and decoupling.
  2. ESP32↔FPGA QSPI, kept roughly length-matched. Report the spread; it
     was 5.6 mm.
  3. USB D+/D− as a clean equal-length pair.
  4. General I/O to the back connector.
- **Repin connectors freely.** General-purpose connector contacts may be
  reassigned to untangle routing. Update the schematic and the carrier pinout
  CSV to match.
- **When a region is a mess, rip it up.** Delete all routing between a QFN
  and its connector, reposition, then reroute from scratch rather than
  patching.
- **Route directly.** Power feeds take direct paths that don't crowd fanouts.
  *"The power line that comes in from the back connector… takes a completely
  crazy route."*

## Vias and planes

- **No vias in pads.** Relocate them with short traces.
- **No vias under QFN bodies.** They are hard to debug. Enforce this with a
  via-only keepout under each package so later passes can't reintroduce them.
- **Use the board space.** Prefer larger vias: 0.45 mm pad / 0.20 mm drill
  avoids JLC's small-via surcharge. Fan out wide rather than packing
  tight.
- **Stagger fanout vias**: alternate near/far rows when many vias leave one
  QFN side.
- **No lost or dead vias.** Every via must earn its place. Remove orphan
  vias, redundant stitching and leftover branches. The exceptions to keep are
  decoupling-cap vias to the inner ground (short HF return, even when a
  top-pour thermal also exists) and RF shunt-part ground vias.
- **Put vias straight below their pad** when a pad needs one.
- **Thermal reliefs on plane-connected pads** (0.15 mm gap/spokes). Keep
  exposed IC pads and RF grounds solid. Fine-pitch connector grounds get
  explicit narrow connections rather than being left disconnected.
- **Four layers for dense MCU+FPGA work**: Top signals / In1 solid GND / In2
  power / Bottom signals and connectors.

## Silkscreen

- **Minimal.** Keep references for ICs, connectors, and jumpers. Hide
  passive references (caps, resistors, ferrites, H/L/D as requested). They
  stay on the Fab layer.
- **Uniform and small.** Use one text size for all references, at JLC's
  minimum (1.0 mm / 0.15 mm stroke).
- **Pertinent placement.** Put the label at a consistent corner of its part
  (U1/U2 bottom-right), never eclipsed by vias, and never under a package.
  Antenna label directly under the antenna; crystal label directly left of it.
- **No explanatory clutter.** Remove notes like "RF KEEP CLEAR", "EXT", "CUT
  CHIP", and board titles when they're crowded. Keep the keepout itself in
  copper and rules, not text.
- **Visible pin-1 dots**, outside the package outline, for ICs and
  orientation-sensitive parts, so they can be seen in 3D and on the assembled
  board. Not on unpolarized passives.
- **Check new footprints for junk silkscreen** (duplicate outlines or markers)
  after a package swap.

## Parts

- **0402 is the smallest package** (you typed "0403"). 0201 only as a last
  resort, then reverted.
- **Inspectable packages.** Prefer leaded parts (VSSOP) over leadless ones with
  hidden thermal pads when bodging or inspection matters (TPS62160DGKR
  replaced a leadless buck).
- **Buck over LDO for 5 → 3.3 V** at ESP32 Wi-Fi currents: 1.7 V × I is too
  much heat.
- **Availability decides.** Swap out-of-stock parts for high-stock JLCPCB/LCSC
  equivalents in the same footprint, and note any performance delta (e.g.
  dimmer LED color).
- **Search JLCPCB/LCSC directly** for replacements. Don't block on a
  parts-connector MCP.
- **Verify the LCSC number matches the footprint size.** *C364372 is 01005,
  not 0402.*
- **Remove parts the board doesn't need** (strap resistors, unused 1.8 V
  bank option) when they cost space.
- **Real 3D models for everything.** Get vendor STEP files (Hirose, Coilcraft)
  and add legible finishes and markings: gold connector pins, antenna marking.
