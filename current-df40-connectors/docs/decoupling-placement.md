# Decoupling placement review

Straight-line pad-center distances, not routed lengths or electrical loop inductance. Ground-via proximity does not prove an unobstructed plane return.

Existing capacitors repositioned; shared-capacitor topology retained. This does not establish full manufacturer-checklist compliance.

| Pin | Supply | Capacitor | Before nearest 100 nF | After | GND via |
|---|---|---|---:|---:|---:|
| U1.1 | VDDA | C37 | — | 1.24 mm | 1.434 mm |
| U1.3 | VDD3P3 | C35 | — | 1.768 mm | 1.823 mm |
| U1.4 | VDD3P3_2 | C35 | — | 1.711 mm | 1.823 mm |
| U1.20 | VDD3P3_RTC | C38 | — | 1.91 mm | 3.988 mm |
| U1.27 | VDD3P3_RTC_IO | C40 | — | 1.763 mm | 1.382 mm |
| U1.30 | VDD_SPI | C41 | — | 1.16 mm | 1.792 mm |
| U1.45 | VDD3P3_CPU | C39 | — | 2.429 mm | 1.15 mm |
| U1.51 | VDDA_2 | C42 | — | 2.236 mm | 1.091 mm |
| U1.54 | VDDA_3 | C42 | — | 1.675 mm | 1.091 mm |
| U2.1 | VCCIO_2 | C52 | — | 3.036 mm | 0.8 mm |
| U2.5 | VCC_1 | C50 | — | 3.036 mm | 0.8 mm |
| U2.22 | SPI_VCCIO1 | C48 | — | 2.415 mm | 0.8 mm |
| U2.24 | VPP_2V5 | C48 | — | 2.43 mm | 0.8 mm |
| U2.29 | VCCPLL | C44 | — | 2.736 mm | 0.8 mm |
| U2.30 | VCC_2 | C49 | — | 2.824 mm | 0.8 mm |
| U2.33 | VCCIO_0 | C46 | — | 2.781 mm | 0.8 mm |

The baseline column compares the nearest existing 100 nF capacitor on the same net, not necessarily the same reference. Capacitors on a shared supply can serve multiple pins; this is not proof of effective decoupling.

Reference: [Lattice iCE40 Hardware Checklist](../../../libraries/datasheets/ice40-hardware-checklist.pdf), sections 2 and 7.

Board SHA-256: `87f79015ff1839fab969b1c949993c3161284cc376d5711af10f55e21a9c03d3`
