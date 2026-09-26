#!/usr/bin/env python3
"""Apply routing-assistant output to the active board, retaining manual critical routes."""
from pathlib import Path
import pcbnew as p,json
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';O=R/'tmp/module-layout';b=p.LoadBoard(str(O/'critical.kicad_pcb'))
meta=json.loads((O/'route-meta.json').read_text());names=meta['names'];S=meta['step'];layers=[p.F_Cu,p.In2_Cu,p.B_Cu]
def pt(x,y):return p.VECTOR2I(p.FromMM(100+x*S),p.FromMM(100+y*S))
seen=set()
for fn in ['escapes.txt','routes.txt']:
 for line in (O/fn).read_text().splitlines():
  a=line.split()
  if not a:continue
  if a[0]=='V':
   _,n,x,y=a;x=int(x);y=int(y);key=(n,x,y)
   if key in seen:continue
   seen.add(key);t=p.PCB_VIA(b);t.SetPosition(pt(x,y));t.SetWidth(p.FromMM(.4));t.SetDrill(p.FromMM(.2));t.SetViaType(p.VIATYPE_THROUGH);t.SetLayerPair(p.F_Cu,p.B_Cu)
  else:
   _,n,z,x,y,u,v=a;t=p.PCB_TRACK(b);t.SetStart(pt(int(x),int(y)));t.SetEnd(pt(int(u),int(v)));t.SetWidth(p.FromMM(.1));t.SetLayer(layers[int(z)])
  t.SetNet(b.FindNet(names[n]));b.Add(t)
for layer,net in [(p.In1_Cu,'/GND'),(p.In2_Cu,'/+3.3V'),(p.F_Cu,'/GND'),(p.B_Cu,'/GND')]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet(net));z.SetLocalClearance(p.FromMM(.15));z.SetMinThickness(p.FromMM(.15));z.SetThermalReliefGap(p.FromMM(.2));z.SetThermalReliefSpokeWidth(p.FromMM(.2));z.SetPadConnection(p.ZONE_CONNECTION_FULL if layer in [p.In1_Cu,p.In2_Cu] else p.ZONE_CONNECTION_THERMAL);o=z.Outline();o.NewOutline()
 for x,y in [(.3,.3),(33.7,.3),(33.7,35.7),(.3,35.7)]:o.Append(p.FromMM(100+x),p.FromMM(100+y))
 b.Add(z)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
print('Applied',len(b.GetTracks()),'tracks/vias; filled ground and 3.3 V planes')
