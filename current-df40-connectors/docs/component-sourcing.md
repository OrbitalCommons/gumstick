# Component sourcing

Catalog identities checked 2026-09-23 for the current ESP32-S2 module.
All 50 purchased component placements now have a manufacturer part number
and an LCSC product link (21 unique part numbers). Catalog identity and
package size were checked; this is not a reservation of assembly stock.
Confirm JLCPCB assembly availability and the final land patterns before ordering.

## Corrected imported IDs

- U1: C2841141 is ESP32-S2FH2, not the requested 4 MB part. Use C2840995, ESP32-S2FH4.
- Y1: C555614 is a JGHC crystal. The selected ECS-400-10-36-CKY-TR is C2449947.
- L3: the imported manufacturer part number was a ferrite bead. The 2.2 nH RF inductor is Murata LQG15HS2N2S02D, C86061.
- C33/C34/C43/C45: the old 0402 supplier ID no longer matched their 0603 footprints. These now use the same 10 V, 0603 part as C60.
- C61/C67 are now matched 10 V 0603 output capacitors; C62–C66 retain their selected 50 V parts.

## Selected parts

| References | Manufacturer part | LCSC | Specification |
| --- | --- | --- | --- |
| C1, C2 | GJM1555C1H3R3BB01D | [C76906](https://www.lcsc.com/product-detail/C76906.html) | 0402; 3.3 pF; C0G; 50 V |
| C32 | CL05A105KO5NNNC | [C29266](https://www.lcsc.com/product-detail/C29266.html) | 0402; 1 uF; X5R; 16 V |
| C33, C34, C43, C45, C60 | CL10A106KP8NNNC | [C19702](https://www.lcsc.com/product-detail/C19702.html) | 0603; 10 uF; X5R; 10 V |
| C35, C37, C38, C39, C40, C41, C42, C44, C46, C48, C49, C50, C52 | CL05B104KO5NNNC | [C1525](https://www.lcsc.com/product-detail/C1525.html) | 0402; 100 nF; X7R; 16 V |
| C6, C7 | CL05C120JB5NNNC | [C26406](https://www.lcsc.com/product-detail/C26406.html) | 0402; 12 pF; C0G; 50 V |
| C61, C67 | CL10A226MPCNUBE | [C5355402](https://jlcpcb.com/partdetail/6155917-CL10A226MPCNUBE/C5355402) | 0603; 22 uF each; X5R; 10 V; two in parallel |
| C62, C63, C66 | CL10A105KB8NNNC | [C15849](https://www.lcsc.com/product-detail/C15849.html) | 0603; 1 uF; X5R; 50 V |
| D1 | FC-B1010RGBT-HG | [C158099](https://www.lcsc.com/product-detail/C158099.html) | Common-anode RGB; 1.0 x 1.0 mm |
| J1 | DF40C(2.0)-40DS-0.4V(51) | [C597934](https://www.lcsc.com/product-detail/C597934.html) | 40 contacts; 0.4 mm pitch; receptacle |
| L1, L2 | BLM18KG101TN1D | [C160981](https://www.lcsc.com/product-detail/C160981.html) | 0603; ferrite bead; 100 ohm at 100 MHz |
| L3 | LQG15HS2N2S02D | [C86061](https://www.lcsc.com/product-detail/C86061.html) | 0402; 2.2 nH; RF inductor |
| L4 | XFL3012-222MEC | [C3911432](https://www.lcsc.com/product-detail/C3911432.html) | 3 x 3 mm; 2.2 uH |
| R20, R22, R28, R29, R60, R61 | RC0402FR-0710KL | [C60490](https://www.lcsc.com/product-detail/C60490.html) | 0402; 10 kohm; 1% |
| R3 | 0402WGF0000TCE | [C17168](https://www.lcsc.com/product-detail/C17168.html) | 0402; 0 ohm |
| R62 | RC0402FR-07100KL | [C60491](https://www.lcsc.com/product-detail/C60491.html) | 0402; 100 kohm; 1% |
| U1 | ESP32-S2FH4 | [C2840995](https://www.lcsc.com/product-detail/C2840995.html) | QFN56; 7 x 7 mm; 4 MB flash |
| U2 | ICE40UP5K-SG48I | [C2678152](https://www.lcsc.com/product-detail/C2678152.html) | QFN48; industrial temperature grade |
| U3 | TPS62160DGKR | [C60726](https://www.lcsc.com/product-detail/C60726.html) | VSSOP8; exposed leads; R64/R65 set 3.3 V |
| U4 | TLV75512PDBVR | [C2877864](https://www.lcsc.com/product-detail/C2877864.html) | SOT-23-5; 1.2 V LDO |
| Y1 | ECS-400-10-36-CKY-TR | [C2449947](https://www.lcsc.com/product-detail/C2449947.html) | 2520; 40 MHz; CL 10 pF |

AE1 is a purchased Pulse chip antenna, and H1 is
a drilled mounting hole; none is a purchased assembly component. The M3
screw/spacer and mating motherboard connectors belong to the future carrier BOM.

## ESP32-C3 option

The ESP32-C3 is not a pin-compatible substitute: its QFN32 package is 5 x 5 mm,
whereas ESP32-S2FH4 is QFN56, 7 x 7 mm. A change to C3 requires a new footprint,
pin assignment, power/boot review and routing. Its smaller GPIO budget also
requires reviewing the FPGA link and carrier signals. The current files and
BOM retain the S2 until that architecture decision is made.

Sources: [Espressif ESP32-C3 datasheet](https://documentation.espressif.com/esp32-c3_datasheet_en.html),
[Espressif ESP32-S2 datasheet](https://documentation.espressif.com/esp32-s2_datasheet_en.html).

## Chip antenna option

A ceramic chip antenna could free part of the antenna end, but the entire
manufacturer-defined copper keepout, matching network and carrier clearance
must be compared—not just the component body. No antenna substitution or
outline reduction has been made. See [Johanson antenna layout guidance](https://www.johansontechnology.com/docs/3827/Antenna-2450AT18A0100001E-Rev4.0.pdf).

## Procurement follow-up

The exact ECS crystal is currently listed out of stock at LCSC.
[DigiKey lists the same ECS part as XC2666CT-ND](https://www.digikey.com/en/products/detail/ecs-inc/ECS-400-10-36-CKY-TR/8023601),
so it can be sourced without changing the crystal circuit. Arrange the
assembler's supported procurement/consignment method before ordering.
The original C555614 (JGHC S2240000101050JY) has similar catalog frequency,
load and package specifications, but is not silently substituted for ECS.

J2 is now the complementary **DF40C-40DP-0.4V(51)** plug, LCSC
[C424643](https://www.lcsc.com/product-detail/C424643.html). The plug is
manufacturer-listed as mating to J1’s receptacle type. Verify current
stock and JLCPCB assembly availability; prior shared J1/J2 sourcing is obsolete.
TP1/TP2 are bare probe pads and require no purchased parts.

## Smaller buck output capacitors — 2026-09-24

C61's former 0805 is replaced by two matched 0603 capacitors, C61/C67. JLCPCB listed 3,154 in stock (2,642 available to order) when checked; stock must be rechecked at order time. Samsung specifies 1.6 × 0.8 × 0.85 mm, 10 V, ±20%, X5R (−55 to +85 °C). Its typical 25 °C DC-bias curve gives about −55% at 3.3 V: about 10 µF each, or 20 µF combined. Applying −20% initial tolerance and −15% temperature variation as a conservative budgeting exercise gives approximately 13.5 µF combined, not a guaranteed manufacturer minimum. TI TPS62162 Table 2 supports 2.2 µH with 10/22/47 µF nominal ceramic outputs; the pair provides margin over a single small 22 µF part. Bench transient/stability validation remains part of prototype validation.

Sources: [Samsung characteristics](https://product.samsungsem.com/mlcc/CL10A226MPCNUB.do), [TI TPS62162](https://www.ti.com/lit/ds/symlink/tps62162.pdf). The sampled manufacturer DC-bias curve is saved in `capacitor-output-selection.json`.

### Minimum capacitor package

Use 0402 or larger capacitors. C35 is restored to Samsung CL05B104KO5NNNC (C1525), 100 nF, 16 V, X7R, 0402, and moved outward to leave fanout space. Prefer moving components outward over shrinking below 0402. Confirm stock at order.

### Antenna Revision B

AE1 is now purchased Pulse ANT2012LL00R2400A (LCSC C3284792; 363 listed in stock on 2026-09-26); J3 is Hirose U.FL-R-SMT-1(01), supplier pending. R63 is a populated 0402 zero-ohm link: UNI-ROYAL 0402WGF0000TCE, C17168 (JLCPCB Basic listing checked 2026-09-26). Final RF tuning remains pending. C68/C69 are DNP 0402 tuning sites. JP1 is an etched cut/bridge selector, not a purchased component. See antenna/INTEGRATION.md for release gates.

## Current RF revision — external only
AE1, JP1, R63, C68 and C69 are removed. Their preceding sourcing history is superseded. J3 remains Hirose U.FL-R-SMT-1(01), supplier ordering ID pending. No chip antenna or chip-tuning components are purchased.

## Crystal replacement — 2026-09-26
Y1 now uses JGHC S2240000101050, C426970, replacing the unavailable ECS part referenced in the historical table above. LCSC lists 1040 and JLCPCB lists 1069. See crystal-replacement.md for footprint and oscillator validation details.

## Inspectable buck update — 2026-09-26

U3 is TPS62160DGKR (C60726), with R64 75kR (C25798) and R65 24kR (C25769), both 0402 1%. See `inspectable-buck-option.md` for circuit, layout, and thermal validation requirements. This supersedes the original fixed-output WSON selection.
