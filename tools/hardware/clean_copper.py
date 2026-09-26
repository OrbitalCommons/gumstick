#!/usr/bin/env python3
"""Remove duplicate vias and disconnected pour islands, then refill."""
from pathlib import Path
import pcbnew as p
D=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module'
b=p.LoadBoard(str(D/'module.kicad_pcb'));seen=set();removed=0
for t in list(b.GetTracks()):
 if not isinstance(t,p.PCB_VIA):continue
 key=(t.GetPosition().x,t.GetPosition().y,t.GetNetCode())
 if key in seen:b.RemoveNative(t);removed+=1
 else:seen.add(key)
for z in b.Zones():
 if not z.GetIsRuleArea():z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
print('Removed duplicate vias:',removed)
