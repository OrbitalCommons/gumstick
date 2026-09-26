# External antenna only — 2026-09-26

J3 (Hirose U.FL-R-SMT-1(01)) directly connects to the original ESP32 matching network L3/C1/C2 on RF_ANT. AE1, JP1, R63, C68 and C69 have been removed, along with their chip feed, selector, and antenna keepout. An attached external 2.4 GHz antenna is required for Wi-Fi. There is no cut/bridge selection procedure.

J3 is aligned directly above the RF matching network: absolute X=112.2 mm (local X=12.2 mm). Footprint origin is local (12.2,5) mm, rotation 90 degrees. Its original model registration offset is retained. The matching-to-jack copper is 2.61 mm, entirely F.Cu, 0.26 mm wide, with a straight vertical approach and continuous In1 GND reference. The original ESP32 matching network is unchanged.

Use the specified 1.0 mm JLC stackup and have fabrication confirm the 50-ohm geometry (see STACKUP-AND-FEED.md). Connector launch, matching parts, cable and antenna still require RF verification. J3 still needs a confirmed supplier ordering ID; verify mating cable and tool clearance. These engineering exports are not a measured RF qualification.

Earlier Abracon/Pulse proposal documents, footprints, and model files are historical only and are not populated in this revision.
