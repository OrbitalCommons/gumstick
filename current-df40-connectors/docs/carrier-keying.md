# Complementary DF40 carrier keying

Historical design notes. Use [ICD-v1.md](ICD-v1.md) for the consolidated ordered-v1 interface, corrected body datum, existing carrier libraries and full pin contract.

| Module | Module component | Carrier mate |
| --- | --- | --- |
| J1 | DF40C(2.0)-40DS-0.4V(51), receptacle | DF40C-40DP-0.4V(51), plug |
| J2 | DF40C-40DP-0.4V(51), plug | DF40C(2.0)-40DS-0.4V(51), receptacle |

Both connections have a nominal **2.0 mm board-to-board mating height**.
Do not substitute the 1.5 mm receptacle. Both module connectors are on the
bottom and run across the 20 mm board width. Their centers are (10,15.75)
and (10,40.75) mm, separated by 25.00 mm. H1 is at (10,28.25), exactly midway, 12.50 mm from either connector center.
A reversed module presents plug-to-plug and socket-to-socket, preventing
correct full engagement. This is orientation keying, not permission to force
or partially offset the connectors. Use the center screw/spacer to retain the
assembly at its intended mating height, not to pull misaligned connectors in.

The plug has a different footprint: 0.23 × 0.66 mm electrical lands at
0.4 mm pitch, row centers ±1.355 mm, plus four isolated 0.35 × 0.66 mm
mounting lands at x=±4.275 mm. The four mounting tabs have no electrical
continuity and no signal numbers. Socket lands remain 0.20 × 1.14 mm.
Footprints include exact, normalized Hirose STEP models. Use a 0.12 mm
stencil and review Hirose's recommended aperture reduction during assembly.

The project's contact numbering runs 1–20 across one row and 40–21 across
the other in the local footprint view. **Do not assume identical local pad
numbers automatically mate on opposite board faces.** For the future carrier,
mirror the physical mating interface and assign each carrier contact by the
module's physical contact location; check the resulting contact-by-contact
map against carrier-pinout.csv and the manufacturer drawings before routing.
No carrier PCB is generated in this task.

The 25 mm spacing revision also reassigns J2 signal contacts to simplify fanout.
J1-21 is now GPIO40 and J1-22 is ground. Use the current carrier-pinout.csv;
previous carrier pin maps are not compatible with this revision.

SYNC_IO has been removed entirely. GPIO38 is J1-39, GPIO45 is J1-34,
and GPIO46 is J1-33. FPGA pin 44 is J2-32; J1-16 is GPIO4.
J1-33/J1-34 must no longer be grounded on the carrier. GPIO45 is a flash-voltage
boot strap; keep low or high-impedance at reset. GPIO46 is input-only and a
boot strap; keep low or high-impedance at reset. TP1 is FPGA_CRESET_N; TP2 is FPGA_CDONE. Test points are exposed
0.8 mm copper pads without paste and are excluded from purchased BOM/CPL.
ESP32-S2FH4 package pins 31–36 remain externally NC because they are tied
to the embedded flash.

Sources:
- https://www.hirose.com/en/product/p/CL0684-4042-5-51
- https://www.hirose.com/en/product/p/CL0684-4013-7-51
- Plug drawing EDC-311351-00, archived in libraries/datasheets.
- LCSC plug identifier C424643; verify live stock/JLC assembly availability.
