# L4 manufacturer 3D model — 2026-09-26

Replaced the approximate block with Coilcraft’s original XFL3012 STEP, obtained through the manufacturer’s XFL3012 page / 3D Model popup. Geometry and face colors are unchanged. Original STEP SHA256 is recorded in the revision manifest via the bundled model archive.

Source: https://www.coilcraft.com/getmedia/959de638-4a4c-4509-9841-81badc8b8b4e/XFL3012.STEP
Download used the manufacturer’s public Azure web host for the same /getmedia path because the main host returned a browser challenge.

Model axes: original Y is height; KiCad model rotation X=-90°, Z offset +0.05 mm brings the bottom terminals to the footprint plane. The manufacturer model envelope is 3.2 × 3.2 × 1.3 mm, centered in XY after transformation. Terminal centers are ±1.015 mm along footprint X, matching the copper lands. Manufacturer artwork says “777”; this is generic model artwork, not the ordered 2.2 µH value or a PCB silk annotation. No component or copper placement changed.

Also removed U3’s extra package-outline silkscreen and redundant generated remote pin-one dot. The native visible pin-one triangle and U3 reference remain. Hidden MPN/manufacturer/value metadata on U3/R64/R65 is assigned to F.Fab, not F.Silkscreen.
