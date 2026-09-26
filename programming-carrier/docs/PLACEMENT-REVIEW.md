# JLCPCB placement-anchor review

2026-09-26: user reports USB and switch centers appear displaced in JLCPCB.
Native CPL is using footprint origins, not pad averages. Both footprints place
the origin at the package body center. No verified JLCPCB translation offset
is currently available, so none has been applied.

With USB at the top, coordinates in KiCad absolute mm:

- J3 TYPE-C-31-M-12: origin (100,22.8), rotation 180 degrees;
  signal row Y=26.845; locating holes (97.11,25.4)/(102.89,25.4);
  shield holes X=95.68/104.32, Y=21.75/25.93.
  CPL center (80,142.2), referenced to board lower-left drill origin.
- SW1 JS102011SAQN: body center (65,47), rotation 0 degrees;
  signal pads (62.5,44.25)/(65,44.25)/(67.5,44.25);
  locating holes (61.6,47)/(68.4,47).
  CPL center (45,118).
- SW2/SW3 tactile switches also have symmetric, body-centered origins.

C&K drawing page 4 confirms 2.5 mm terminal pitch, 6.8 mm locating-hole
spacing and 2.75 mm terminal-pad-center offset from hole row. USB drawing
confirms 5.78 mm locating-hole spacing and 4.18 mm shield-row spacing.
Compare **pins and locating/shield holes**, not the visual bounding box or
slide actuator. JLCPCB may use a different model/package anchor. A screenshot
of its pad overlay or measured correction is required before assigning an
export translation. Do not shift PCB copper to compensate for a preview anchor.

Sources:
- https://datasheet.lcsc.com/datasheet/pdf/facc684708fd3febef29363c3f43748d.pdf (C&K)
- https://datasheet.lcsc.com/datasheet/pdf/9e56b777c022540fcce7c7f67825f55e.pdf (HRO)

## Corrections resolved from preview and supplier library

Screenshots `portal_pasted_image_260926_121947.png` and
`portal_pasted_image_260926_122020.png` resolved the offsets above:

- SW1: CPL Y +2.75 mm, final (45,120.75). Supplier-library origin is terminal
  row, not housing center. Supplier locating holes are 2.750058 mm below it.
- J3: CPL Y -1.425 mm, final (80,140.775), rotation remains 180 degrees.
  Supplier-library shield rows relative to origin are -1.705737 / +2.474087
  mm; KiCad local rows are -3.13 / +1.05 mm. Mean difference is 1.425012 mm.
  At the installed 180-degree orientation this is downward on the board.
- U1: -90-degree correction, final CPL rotation 270 degrees; pin 1 upper-left.
- U2: -90-degree correction, final CPL rotation 180 degrees; pin 1 upper-right.
- U3–U11: retain their previously established -90-degree correction.

Evidence: official supplier-contributed EasyEDA package data retrieved from
`https://easyeda.com/api/products/C221660/components?version=6.4.19.5` and
`https://easyeda.com/api/products/C165948/components?version=6.4.19.5`.
Translation applies only at the verified native top-side rotation; exporter
assertions require re-verification if that orientation changes. PCB copper
and native KiCad position export are unchanged. Recheck the new JLCPCB preview
and avoid applying the old manual corrections on top of the corrected CPL.
