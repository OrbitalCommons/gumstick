# ESP32 supply filter placement — 2026-09-26

L1/C33/C34 moved above-left of U1. C35 remains at the ESP_VDD3P3 pins 3/4. L1 output to C35 uses a direct component-side 0.30 mm route, approximately 3.39 mm, without the previous two signal vias and bottom-layer detour. C34 is vertical beside C35, forming the right-hand leg of the U-shaped filter; C33 is adjacent to its input. The input uses a 0.45/0.20 mm via to the existing 3.3 V plane. Capacitor grounds retain plane thermals. U.FL and QFN fanout courtyard/pad clearances pass DRC and via-pad audit. Placement coordinates are saved in placement.json; schematic topology is unchanged.

The complete filter group was subsequently shifted 1.0 mm down for additional U.FL cable/tool access. J3 was subsequently shifted right to align with the RF matching network.

Both ESP_VDD3P3 pins (U1.3 and U1.4) have explicit centered 0.15 mm track entries; the former corner-overlap connection has been removed.

L1 and C33 shifted 1.7 mm right to compact the filter around C34/C35. L1 is centered between the vertical capacitors, with assembly courtyard clearances preserved.
