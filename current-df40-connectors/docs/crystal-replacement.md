# Crystal and passive cleanup — 2026-09-26

Y1: JGHC S2240000101050, LCSC/JLCPCB C426970, replaces ECS-400-10-36-CKY-TR. Supplier listings specify 40 MHz, CL=10 pF, +/-10 ppm initial tolerance, ESR=50 ohm and -40..85 C. LCSC lists 1040 and JLCPCB lists 1069 at review; inventory is not reserved.

Sources: https://www.lcsc.com/product-detail/C426970.html and https://jlcpcb.com/partdetail/JGHC-S2240000101050/C426970 . Manufacturer family datasheet downloaded from the JLC product page into libraries/datasheets/JGHC-S2240000101050.pdf.

The 2520 package has signal terminals 1/3 and ground terminals 2/4. The local footprint retains the established schematic pin names, preserving this mapping. Updated lands follow the manufacturer suggested 1.0 x 0.9 mm pads with 0.85 / 0.65 mm gaps. Existing 2520 model is an approximate package visualization, not exact vendor CAD.

The linked manufacturer sheet is generic: it quotes 60-ohm family ESR, selectable +/-10 or +/-30 ppm temperature stability, and -10..70 C or specified temperature grades. Thus catalog-specific ESR/temperature claims require exact-order confirmation before production; do not infer temperature stability from initial tolerance. Verify oscillator startup, drive level and frequency over intended temperature on hardware. Existing 12 pF C0G load capacitors and 0-ohm R3 are retained as starting values for the same nominal CL. They are not a measured load calibration. Espressif guidance: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s2/schematic-checklist.html .

C6 and C7 are aligned above/below the crystal with symmetric centerline spacing and signal-facing orientations; R3 remains close to the XTAL_P branch. R20 is rotated vertically and aligned to C41, with a corrected upper supply-pad feed. Schematic topology unchanged.
