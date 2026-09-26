# Module v1 programming and GPIO test carrier

160 × 145 mm desktop carrier, four copper layers. The existing daughterboard
and its ordered v1 fabrication snapshot are unchanged. No firmware is included.

## How to use it

1. Disconnect USB power. Align the module with the silkscreen outline, antenna
   end toward USB. Press both DF40 connectors together evenly.
2. Use a **2.0 mm board-to-board spacer** and M3 screw at H1. Do not tighten a
   screw to force incomplete connector engagement. Corner holes accept feet.
3. Connect a USB **data** cable. The 5V and 3V3 TEST indicators show carrier
   power; they do not independently prove the module's internal rails.
4. Select BOOT, press/release RESET, and flash through the ESP32-S2 ROM USB
   interface. Select RUN and press RESET afterward.
5. Test firmware can walk the labeled GPIO LEDs. GPIO46 is input-only: release
   its test button during reset, then press it to test a HIGH input after boot.
   OTA is a future firmware feature, not supplied by this carrier hardware.

## Coverage and loading

There are 60 high-impedance monitored signals: 27 ESP interface signals
(including EN and input-only GPIO46), 30 ordinary FPGA outputs, and three FPGA
RGB current-sink outputs. Eight regular banks use green LEDs (HIGH = lit);
the three RGB channels use red LEDs (LOW = lit). 74LVC541 buffers drive the
LEDs; GPIOs see a 100k bias and buffer input capacitance/leakage rather than LED
current. All unused buffer inputs are grounded. Outputs are always enabled.

GPIO0 has a 100k pull-up for RUN. GPIO45 and GPIO46 have pull-downs to preserve
boot-strapping behavior. Do not hold the GPIO46 test button while resetting.
The EN node retains its module pull-up and reset capacitor. RGB pull-ups are
100k and the module's own RGB LED remains connected.

The module's internal ESP/FPGA QSPI link, embedded-flash pins, FPGA reset and
CDONE are not independent carrier GPIO indicators. ESP32 firmware can control
FPGA configuration through the existing module interconnect. This carrier is
for slow functional GPIO walking/status tests, not high-speed signal analysis;
the long monitor traces add capacitance.

## Interface contract

- Module J1 socket mates with carrier J1 **DF40C-40DP-0.4V(51)**.
- Module J2 plug mates with carrier J2 **DF40C(2.0)-40DS-0.4V(51)**.
- Contact centers: J1 (100,46), J2 (100,71), H1 (100,58.5) mm in PCB coordinates.
- Contact spacing 25.00 mm; H1 is the midpoint, 12.50 mm from each connector.
- Complementary genders prevent normal reversed engagement. Avoid offset or
  forced engagement. Neither connector is intended for hot-plugging.
- All four VIN_5V contacts are connected. All original ground contacts remain.
- `module-v1-pinout.csv` is the frozen electrical contract; `contact-map.json`
  records the physical-to-vendor-footprint number mapping. Carrier connector
  pad numbers intentionally use **module contact numbers**, not raw vendor
  numbering. Do not replace footprints by nominally similar stock footprints.

`Carrier:ESP32_FPGA_Module_v1` is a reusable two-unit schematic symbol, with
`Carrier:ESP32_FPGA_Module_v1_Interface` as its composite footprint. Pads are
named J1_1…J1_40 / J2_1…J2_40, and the footprint includes the module outline and
M3 clearance hole. The actual carrier uses separate J1/J2/H1 so its assembly
BOM and placement file contain the two purchased connectors, not an ambiguous
single module entry. When reusing the composite, split procurement into the
two mate parts; the daughterboard is a separate assembly.

## Power and USB

USB-C sink with separate 5.1k CC resistors; USB 2.0 full speed data goes to the
module through an ST USBLC6-2SC6. A 500mA-hold resettable fuse protects the 5V
feed. AP2112K-3.3 powers only the carrier buffers and LEDs; the module uses its
own regulators. There is no USB-PD controller and no other power input.

This is a prototype test fixture, not a certified USB product. The fuse is
protection, not a negotiated current limiter. Validate total module + carrier
current and plug-in inrush on a current-limited, adequately powered USB hub.
Do not back-power the module from another source while connected here.
The approximate worst-case LED-resistor current bound is 62 × 3.3mA plus
buffer quiescent current (real current is lower because of LED forward voltage).
The 3.3V regulator's thermal margin must be checked with the all-LED test on
actual hardware. Native USB programming is only full speed, not high speed.

## Assembly and inspection

0603 LED/resistor/capacitor footprints, exposed-lead TSSOP buffers, SOT-23 LDO
and ESD parts. Review both Hirose connector genders and **2.0 mm** socket
height in the assembler's preview. Check rotation/polarity in the JLCPCB
placement preview; do not silently substitute the 1.5 mm socket.
Models are project-local. Standard packages come from KiCad's 3D libraries;
Hirose models are the existing audited module models. The USB and slide-switch
STEPs are illustrative envelopes, not vendor mechanical CAD.

The GPIO LED test verifies output-level functionality and continuity; it does
not certify drive strength, RF performance, USB signal integrity, FPGA timing,
or every input path. Prototype bring-up still includes current, boot-mode,
USB enumeration in both plug orientations, and module seating checks.

## Source references

- [TI SN74LVC541A](https://www.ti.com/lit/ds/symlink/sn74lvc541a.pdf): pinout, logic levels, Ioff, input loading.
- [Diodes AP2112](https://www.diodes.com/datasheet/download/AP2112.pdf): pinout and ceramic capacitor requirements.
- [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf): USB ESD channel and VBUS wiring.
- [ESP32-S2 boot mode](https://docs.espressif.com/projects/esptool/en/latest/esp32s2/advanced-topics/boot-mode-selection.html).
- Hirose drawings remain in the repository's `libraries/datasheets/` directory.
- Each assembly part's LCSC URL is recorded in the generated review BOM.

## Routing validation — 2026-09-26

Carrier routing is complete. KiCad 10.0.6, after refilling all copper zones,
reports zero DRC violations, zero unconnected items and zero schematic-parity
issues. ERC also reports zero violations. Reports and a board SHA-256 are in
`fab/checks/`. The schematic pin contract and all 80 interface contact net
assignments were checked. In1.Cu is reserved for ground with no routed tracks.
The isolated front-copper ground island at the USB ESD device now has a direct
ground stitching via. Dangling route branches and unused fanout vias were
removed, followed by another full DRC pass. The top-side native 3D render was
reviewed for component/label placement.

This is layout verification, not electrical testing of assembled hardware.
Fabrication/placement exports must be generated from this completed revision;
the BOM is generated separately with `tools/hardware/carrier_bom.py`.

### Green LED sourcing update — 2026-09-26

The 59 green LEDs now use XINGLIGHT XL-1608SYGC-06, LCSC C965805,
in place of unavailable C72043. LCSC's listing showed 1,023,900 units:
https://www.lcsc.com/product-detail/C965805.html . This is yellow-green,
565–575 nm per the manufacturer datasheet, 0603 / 1.6 × 0.8 × 0.6 mm.
Datasheet page 7 confirms pin 1 cathode and pin 2 anode, matching the board.
Forward voltage is 1.8–2.4 V at 20 mA; existing 1k indicator resistors and
2.2k 5V power-indicator resistor remain appropriate. No copper or placement
changes. Inventory is a sourcing snapshot, not a reservation or a guarantee
of JLCPCB assembly stock. All assembly exports were regenerated.

### JLCPCB placement orientation correction

User review of the JLCPCB placement preview established that C113281
(SN74LVC541APWR, U3–U11) needs 90 degrees clockwise relative to the native
KiCad placement angle. `docs/jlcpcb-placement-offsets.json` records a -90°
correction; the exporter applies it only to the JLCPCB CPL, yielding 270° for
these nine top-side buffers. Native KiCad footprints and position export stay
at 0°. Confirm the pin-1 marker is at each buffer's upper-left corner when
viewing the board from the component side with USB at the top. Reuploading the
corrected CPL replaces the need for the same manual rotation; do not apply it
a second time in the assembler preview.
