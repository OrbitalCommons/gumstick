# ESP32 + FPGA daughterboard v1 — interface control document

**Baseline:** ordered module Git tag **`v1`** in this repository. This document
consolidates the electrical, mechanical and firmware integration contract for
new carriers. It does not revise the ordered hardware. If historical notes
conflict, use the tagged native PCB/netlist and this explicitly audited contract;
never infer a new pinout from an old screenshot or an example firmware PCF.

The module contains **ESP32-S2FH4 (4MB embedded flash)**, **iCE40UP5K-SG48**,
onboard 5V→3.3V and 3.3V→1.2V regulators, a shared FPGA RGB indicator and an
external Wi-Fi U.FL connection. It is not ESP32-C3 and has no optional1.8V I/O bank
supply in v1. All general I/O interfaces are3.3V.

## Authoritative integration assets

| Asset | Use |
|---|---|
| [Module release](../releases/v1/README.md) | Ordered manufacturing snapshot; native source at Git tag `v1` |
| [Electrical contact CSV](carrier-pinout.csv) | All80 module contact assignments and restrictions |
| [ICD contact/package CSV](icd-v1-pinout.csv) | Same assignments cross-checked against tagged PCB, with physical MCU/FPGA pads |
| [Reusable symbol library](../../programming-carrier/Carrier.kicad_sym) | `Carrier:ESP32_FPGA_Module_v1`, two units: J1/ESP and J2/FPGA |
| [Composite footprint](../../programming-carrier/Carrier.pretty/ESP32_FPGA_Module_v1_Interface.kicad_mod) | `Carrier:ESP32_FPGA_Module_v1_Interface`; 80 signal/power pads plus mechanical hole/tabs |
| [Carrier J1 footprint](../../programming-carrier/Carrier.pretty/J1_Module_v1_Mate.kicad_mod) | Plug, module-contact pad numbering |
| [Carrier J2 footprint](../../programming-carrier/Carrier.pretty/J2_Module_v1_Mate.kicad_mod) | 2mm receptacle, module-contact pad numbering |
| [M3 footprint](../../programming-carrier/Carrier.pretty/MountingHole_3.2mm_M3.kicad_mod) | Mounting hole, check body and head clearances below |
| [Physical contact map](../../programming-carrier/docs/contact-map.json) | Module contact ↔ original vendor footprint pad mapping |
| [Frozen programmer pinout](../../programming-carrier/docs/module-v1-pinout.csv) | Independent carrier copy of v1 interface |
| [Programmer design](../../programming-carrier/docs/DESIGN.md) | Working carrier-source example, actual J1/J2/H1 procurement split |
| [Calibrator integration guide](../../gps-time-calibrator/docs/integration/README.md) | Application-specific use of this module |

### Library import and procurement

Add `Carrier.kicad_sym` and `Carrier.pretty` to the new project's **project-local**
symbol/footprint tables using `${KIPRJMOD}` relative paths (or copy and rename a
pinned library). Copy required models and fix model paths for that project.
Place both units of `ESP32_FPGA_Module_v1` under the same schematic reference;
its pin numbers are **J1_1…J1_40 / J2_1…J2_40** to match the composite footprint.
Check the exported netlist and all80contacts before routing.

The composite represents a mating interface, not a single purchasable component.
For assembly BOM/CPL use **two physical connector references and H1**, as the
programmer and calibrator do, with independent MPNs/placements. Alternatively,
write an explicit composite-to-two-parts assembly exporter. Do not silently emit
one “module interface” SMT placement and expect the assembler to infer connectors.
Do not place both the composite and separate connector footprints on top of each
other: that duplicates pads/holes. Procure the daughterboard separately.

**Known composite drawing discrepancy:** its electrical pads and center hole
match the carrier interface, but its F.Fab body rectangle is currently
`x=-10..10, y=-28.25..16.75` relative to H1. The tagged ordered module is actually
`x=-10..10, y=-26.80..18.20`. For a new carrier, correct the copied body drawing
and clearance reservation to the latter; do not shift the pads or hole to repair
an outline. Existing board fabrication files are not changed by this document.

## Mechanical contract

View the carrier from above, module component side visible, ESP32/U.FL end at
**top**. Coordinates in millimeters, X right, Y down, origin at **H1 screw center**:

| Feature | X | Y |
|---|---:|---:|
| J1 center (ESP/USB end) | 0 | −12.50 |
| H1 center | 0 | 0 |
| J2 center (FPGA end) | 0 | +12.50 |
| Module left/right edges | −10 /+10 | — |
| Module top/bottom edges | — | −26.80 /+18.20 |

Nominal module outline **20×45mm**, PCB thickness **1.0mm**. The top edge is
14.30mm above J1 and the bottom is5.70mm below J2. In the tagged PCB, edges are
X100..120,Y101.45..146.45; J1=(110,115.75),H1=(110,128.25),J2=(110,140.75).
Edge-centerline dimensions exclude plotted line width.

```text
          U.FL / ESP32 end
        ┌──────────────────┐  y = -26.80
        │                  │
        │ ====== J1 ====== │  y = -12.50
        │                  │
        │        H1        │  y =   0.00
        │                  │
        │ ====== J2 ====== │  y = +12.50
        └──────────────────┘  y = +18.20
                 FPGA end
```

The hole is intentionally midway **between connectors**, not at the module
rectangle center: it tensions both connectors evenly. Connector spacing is
**25mm**, hole-to-connector distance **12.5mm** each. H1 is3.2mm NPTH; reserve a
7mm-diameter screw-head/spacer region and verify actual hardware. Use an
insulating **2.0mm board-to-board spacer** and suitable M3 hardware. Select screw
length for the actual carrier/module/spacer/washer/nut stack; do not use torque
to close an incompletely seated connector pair. No hot mating.

| Location | On module | Required carrier mate |
|---|---|---|
| J1 | DF40C(2.0)-40DS-0.4V(51), receptacle | DF40C-40DP-0.4V(51), plug |
| J2 | DF40C-40DP-0.4V(51), plug | DF40C(2.0)-40DS-0.4V(51), receptacle |

Both pairs have nominal2.0mm mating height. A1.5mm receptacle is not an equivalent
substitute. Mixed plug/socket arrangement prevents normal reversed engagement,
but not damage from force or partial offset. Leave space to press/support both
ends and to remove the module without twisting.

The mating gap is measured between the carrier top and module underside.
Account for bottom connectors, solder and tolerances; reserve the module envelope
instead of assuming all that gap is available for carrier parts. Also reserve
access for U.FL mating tool/cable, M3 hardware and top-side component height.
This ICD does not specify a validated maximum assembly height/cable bend envelope;
check the assembly STEP and actual parts for the new enclosure.

**Numbering warning:** carrier pad labels deliberately use module contact numbers.
They are already mirrored for the mating interface. A same-gender stock footprint
with the same numerical labels is not necessarily pin-compatible. Use the local
mating footprints and `contact-map.json`, inspect pin1, and audit every contact.
Carrier placement example: both local mating footprints at rotation0 on F.Cu,
J1=(0,−12.5), J2=(0,+12.5), H1=(0,0). Module connectors themselves are on B.Cu.

## Power, signal levels and reset

- Supply **regulated5V** on all J1.1–4. Connect every designated ground on both
  connectors. Do not use a subset of power contacts and assume unchanged rating.
- Carrier must budget measured ESP/Wi-Fi peaks, FPGA activity, regulator losses,
  attached loads and inrush. No validated fixed module peak-current budget is
  declared here. Validate5V droop and module3.3/1.2V under worst-case operation.
- The interface exposes **no general-purpose3.3V power output**. Carrier3.3V
  peripherals need a carrier regulator. Do not source power through GPIO clamps.
- J1.1–4 may be called `VIN_5V` on the module and `USB_VBUS` on a carrier; net
  names are local, contact functions are fixed. Never feed9/12/20V PD rails here.
- FPGA I/O banks and ESP I/O use3.3V; not5V tolerant. Unpowered-domain interfaces
  need appropriate isolation/high-Z sequencing. Review pull-ups and default states
  when carrier and daughterboard rails ramp differently.
- J1.11 **ESP_EN** is active-high chip enable/reset. Leave to module pull-up for
  normal operation; use open-drain/pushbutton low for reset, not an opposing driver.
- J1.12 **GPIO0** low at reset enters download mode; high normally. Avoid a carrier
  circuit pulling it low unintentionally. The programmer provides BOOT/RUN+RESET;
  the calibrator does not connect EN or add those switches.
- GPIO45/J1.34 is the flash-voltage strap: do not pull high at reset. GPIO46/J1.33
  is **input-only** and also a boot strap: keep low/high-Z at reset. Configure other
  usage only after boot and return safe states before resets.
- GPIO43/44 are normally UART0 pins; route console to native USB when using these
  for a peripheral. Check ROM boot output as well as application logging.
- Module package pins31–36 are used internally for ESP32-S2FH4 flash; they are
  not additional carrier GPIOs. Do not confuse package pads with GPIO numbers.

## Connector functions

[The full80-row CSV](icd-v1-pinout.csv) is part of this ICD, not optional background.
It includes physical MCU/FPGA pad cross-references derived from tag `v1`.

J1 groups:

| Contacts | Function |
|---|---|
| 1–4 | 5V input |
| 5,6,9,10,22,30,31 | Ground |
| 7 /8 | Native USB D+ /D− (ESP GPIO20 /19) |
| 11 /12 | ESP_EN /GPIO0 boot strap |
| 13–20 | GPIO1–8 respectively |
| 21,23,24,25 | GPIO40,39,41,42 |
| 26,27 | GPIO43 TXD,44 RXD |
| 28,29,32 | GPIO35,33,34 |
| 33,34 | GPIO46 input-only, GPIO45 strap |
| 35,36,37,38 | GPIO15,17,16,18 |
| 39,40 | GPIO38,21 |

J2 has30 ordinary FPGA GPIOs,3 shared RGB sinks and7ground contacts.
Ground contacts:1,3,8,13,18,23,28. RGB sinks:26=RGB0,27=RGB1,29=RGB2
(FPGA pads39/40/41). These also connect to the module RGB LED: use the iCE40
RGB driver primitive/current controls, not arbitrary push-pull assumptions.
Global-clock-capable exposed signals include J2.22=G0/pad35,
J2.24=G1/pad37, J2.12=G3/pad20, J2.32=G6/pad44. Choose clock pins and global
routing intentionally; the calibrator uses G6 for10MHz OCXO and G0 for PPS.
All remaining J2 assignments are in the CSV; I/O names are not physical pin numbers.

The original application's `SYNC_IO` is gone. GPIO38 and FPGA pad44 are separately
exposed, not wired together on the module.

## USB and ESP/FPGA programming contract

Carrier supplies USB connector, CC/PD policy, ESD, power protection and routing.
The module has native **USB full-speed** data on J1.7/8; no USB-UART bridge is
required. Keep D+/D− a short coupled pair over a continuous reference, with
stackup-specific impedance and connector protection. Do not infer carrier PD
capability from the module; programmer and calibrator have different USB power designs.

Module-local link (unavailable as spare carrier signals):

| Signal | ESP GPIO | FPGA physical pin |
|---|---:|---:|
| CS_N | 10 | 16 |
| SCK | 12 | 15 |
| MOSI | 11 | 17 |
| MISO | 13 | 14 |
| IO2/WP | 14 | 13 |
| IO3/HD | 9 | 18 |
| CRESET_N | 36 | 8 |
| CDONE | 37 | 7 |

TP1/TP2 on the module expose CRESET_N/CDONE. Load FPGA configuration SRAM from
ESP flash each boot; no standalone FPGA configuration-flash device is fitted.
Check CDONE then a runtime protocol/ABI response. Runtime SPI mode, packet format,
clock rate, resets and timing constraints belong to the application ABI; the wire
map does not imply a preinstalled protocol or QSPI support.

Affogato provides loader/build blocks. See the [source-reviewed integration notes](../../gps-time-calibrator/docs/integration/affogato.md)
for actual APIs, implementation gaps, paired ESP+FPGA OTA and proposed4MB partitions.
The reusable module contract does not require a particular carrier's GPIO allocation.

## Wi-Fi and physical integration

Ordered v1 uses **external U.FL only**; older chip-antenna/cut-selector notes are
historical. Fit a suitable2.4GHz antenna/cable, reserve connector access and bend
clearance, and validate performance in the final enclosure/carrier. Do not reuse
an old chip-antenna keepout description as the current RF geometry. Module RF
feed and its1mm stackup do not set the host carrier's stackup or RF trace width.

## New-carrier acceptance checklist

1. Freeze module tag and verify all80contact nets against the CSV and native PCB.
2. Verify connector gender,2mm height, mirrored contact numbering and25mm spacing.
3. Place hole at connector midpoint; use the **actual body offsets above**, not
   historical body drawings. Review cable, screw and component clearance in3D.
4. Budget/measure5V supply and inrush; preserve allpower/ground contacts; prevent
   unpowered-domain backfeed and unsafe reset straps.
5. Validate USB enumeration/recovery, FPGA loading/CDONE, runtime SPI and each
   required GPIO. Keep programmer test firmware off application carriers.
6. Review BOM/CPL for both connectors separately, vendor rotations and model
   registration. Existing JLC offsets are part-specific, not generic footprint rules.
7. Record hardware/firmware/FPGA versions and pin-map hash in the new project's
   integration documentation. Changes to contact assignment or mechanical datums
   require a new interface revision, not silent v1 edits.

Historical `carrier-keying.md`, module README and old placement notes contained
obsolete11.75mm spacing, body datums, RGB contact numbers and “future carrier”
wording. This ICD uses the ordered v1 PCB and the already generated carrier mating
assets. It supersedes those historical integration claims without altering
ordered fabrication snapshots.
