# Schematic style

These rules are distilled from your schematic cleanup requests on the ESP32 +
FPGA module.

## Structure

- **Group by function in labeled boxes**: power (one box per regulator), MCU,
  FPGA, RF, crystal, boot/reset, LED, connectors, decoupling. Follow the
  grouping style of the source design when porting.
- **Size boxes to their contents.** Oversized boxes and boxes touching the
  sheet's double border are both defects.
- **Reflow sheets for aesthetics**: aligned blocks, consistent spacing,
  filters/decoupling centered at the bottom, and related sections merged (e.g.
  one antenna block, not two).
- **Remove lost labels** that float without a connection.

## Wiring

- **Draw wires between components within a block.** Use net labels only
  *between* blocks. *"Usually people use lines between schematic components."*
- **No unnecessary crossings.** Reorder ground/power stubs so they don't cross.
- **No wasted horizontal space.** Remove lone wires trailing off to the
  right, and keep regulators compact (e.g. R62 under L4, caps close together).
- **Give labels a tail.** A net label on a block's input/output gets a short
  wire stub, not a label sitting directly on a pin.
- **Draw filters as filters.** A π filter reads C–L–C left to right in a
  compact span.
- **Put power symbols outside the signal labels** and stagger adjacent ones
  so they don't overlap. Power symbols point up; ground points down.

## Text

- **Value directly below the reference** unless something conflicts. Not
  offset right and down.
- **Signal label text sits above its wire**, aligned to the wire's side
  (left-aligned on left-side pins).
- **Use conventional symbols.** A real inductor symbol rather than a
  rectangle, and a proper three-pad solder-jumper symbol showing the default
  bridge.
- **Align related parts.** Rotate parts to run parallel with their
  neighbors, and vertically align cap columns (e.g. C60/C61/C67).

## Naming

- **Use dev-board signal names** (`ESP_GPIO4`, `FPGA_IO_12`, `USB_D+`) rather
  than the application names from the board the design was hoisted from.
- Drop application-specific nets (e.g. `SYNC_IO`) when porting a subsystem.
