#!/usr/bin/env python3
"""One-time chip/selector removal and direct U.FL feed ECO."""
from pathlib import Path
import pcbnew as p,json
D=Path('boards/esp32-fpga-module');f=D/'module.kicad_pcb';b=p.LoadBoard(str(f));pt=lambda x,y:p.VECTOR2I(p.FromMM(x+100),p.FromMM(y+100));removed={'AE1','JP1','R63','C68','C69'}
for fp in list(b.GetFootprints()):
 if fp.GetReference() in removed:b.RemoveNative(fp)
for t in list(b.GetTracks()):
 if t.GetNetname() in ['/RF_ANT','/RF_CHIP','/RF_ANT_MATCH','/RF_EXT'] or (t.GetNetname()=='GND' and min(t.GetStart().y,t.GetEnd().y)<p.FromMM(107)) or (t.GetNetname()=='GND' and 103000000<t.GetStart().x<107000000 and 108500000<t.GetStart().y<111000000):b.RemoveNative(t)
for z in list(b.Zones()):
 if z.GetIsRuleArea() and ('Pulse antenna' in z.GetZoneName() or 'JP1 exposed' in z.GetZoneName()):b.RemoveNative(z)
j=next(x for x in b.GetFootprints() if x.GetReference()=='J3');j.SetOrientationDegrees(90);j.SetPosition(pt(10,5));j.Reference().SetPosition(pt(13,4));j.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
for pad in j.Pads():
 if pad.GetNumber()=='1':pad.SetNet(b.FindNet('/RF_ANT'))
def line(net,a,z,w):
 t=p.PCB_TRACK(b);t.SetNet(b.FindNet(net));t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(p.FromMM(w));t.SetLayer(p.F_Cu);b.Add(t)
line('/RF_ANT',(10,6.05),(12.05,8.1),.26)
line('/RF_ANT',(12.05,8.1),(12.2,8.1),.26)
line('/RF_ANT',(12.2,8.1),(12.2,8.66),.26)
for x,xx in [(8.525,7.3),(11.475,12.7)]:
 line('GND',(x,4.525),(xx,4.525),.3)
 v=p.PCB_VIA(b);v.SetPosition(pt(xx,4.525));v.SetWidth(450000);v.SetDrill(200000);v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(f),b)
f=D/'docs/module-connectivity.json';d=json.loads(f.read_text());d={k:v for k,v in d.items() if k not in removed};d['J3']['pins']['1']['net']='RF_ANT';f.write_text(json.dumps(d,indent=2)+'\n')
f=D/'docs/placement.json';d=json.loads(f.read_text());d={k:v for k,v in d.items() if k not in removed};d['J3']=[10,5,90];f.write_text(json.dumps(d,indent=2)+'\n')
