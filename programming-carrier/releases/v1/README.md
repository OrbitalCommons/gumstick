# Programming carrier v1 — ordered 2026-09-26

User confirmed the carrier was ordered. This snapshot preserves the final
locally supplied Gerber ZIP, BOM, and corrected JLCPCB CPL without regenerating
them. Quantity and vendor order ID were not supplied. Any additional edits
made in the JLCPCB ordering interface are not captured here.

- 160 × 145 mm, four-layer carrier for the separately ordered module v1.
- 217 populated components, 17 BOM groups.
- Green LEDs: C965805 / XL-1608SYGC-06.
- CPL corrections: U1/U2/U3–U11 clockwise 90°; SW1 upward 2.75 mm;
  J3 downward 1.425 mm. These are already included; do not apply twice.
- DRC/ERC/parity reports are included. Hardware bring-up remains pending.

Keep this folder immutable. Future revisions should create a new release folder.
The existing daughterboard v1 release and tag are unchanged.
