#!/usr/bin/env python3
"""Import the locally generated routing session and refill copper in KiCad."""
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';b=p.LoadBoard(str(D/'module.kicad_pcb'))
assert p.ImportSpecctraSES(b,str(R/'tmp/module-layout/module.ses'))
# Ground on the outer layers supplies short return paths for local decoupling.
for layer,net in [(p.F_Cu,'GND'),(p.B_Cu,'GND'),(p.In2_Cu,'+3.3V')]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet(net));z.SetLocalClearance(p.FromMM(.127));z.SetMinThickness(p.FromMM(.15));z.SetPadConnection(p.ZONE_CONNECTION_FULL);o=z.Outline();o.NewOutline()
 for x,y in [(.3,1.75),(19.7,1.75),(19.7,45.3),(.3,45.3)]:o.Append(p.FromMM(100+x),p.FromMM(100+y))
 b.Add(z)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
print('Imported',len(b.GetTracks()),'tracks/vias')
