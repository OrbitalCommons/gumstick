#!/usr/bin/env python3
"""Add the module's ground pours and 3.3 V distribution plane, idempotently."""
from pathlib import Path
import pcbnew as p
D=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module'
b=p.LoadBoard(str(D/'module.kicad_pcb'))
for layer,net in [(p.F_Cu,'GND'),(p.B_Cu,'GND'),(p.In1_Cu,'GND'),(p.In2_Cu,'+3.3V')]:
 if any(not z.GetIsRuleArea() and z.GetLayer()==layer and z.GetNetname()==net for z in b.Zones()):continue
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet(net));z.SetLocalClearance(p.FromMM(.127));z.SetMinThickness(p.FromMM(.15));z.SetPadConnection(p.ZONE_CONNECTION_FULL);o=z.Outline();o.NewOutline()
 for x,y in [(.3,1.75),(19.7,1.75),(19.7,45.3),(.3,45.3)]:o.Append(p.FromMM(100+x),p.FromMM(100+y))
 b.Add(z)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
