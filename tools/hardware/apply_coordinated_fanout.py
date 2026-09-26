#!/usr/bin/env python3
"""Apply a checked coordinated pad-free fanout plan, retaining supply/RF/USB copper."""
from pathlib import Path
import pcbnew as p,json
from shapely.geometry import Point,LineString
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';O=R/'tmp/module-layout';plan=json.loads((D/'docs/fanout-plan.json').read_text());b=p.LoadBoard(str(D/'module.kicad_pcb'));layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]
def xy(v):return p.ToMM(v.x)-100,p.ToMM(v.y)-100
def pt(q):return p.VECTOR2I(p.FromMM(round(100+q[0],6)),p.FromMM(round(100+q[1],6)))
nets={a['net'] for a in plan};shapes={l:[] for l in layers}
for a in plan:
 shapes[a['layer']].append(LineString(a['points']).buffer(.149999))
 for l in layers:shapes[l].append(Point(a['end']).buffer(.249999))
shapes={l:unary_union(gs) for l,gs in shapes.items()}
protected={'VIN_5V','+3.3V','+1.2V','+1.8V','FPGA_VCCIO0','ESP_VDD3P3','+1.2V_PLL','/RF_IN','/RF_ANT','/XTAL_P','/XTAL_P_CRYSTAL','/XTAL_N','/BUCK_SW','/USB_D-','/USB_D+'}
removed=0
for t in list(b.GetTracks()):
 net=t.GetNetname()
 if net in nets:b.RemoveNative(t);removed+=1;continue
 if net in protected:continue
 if isinstance(t,p.PCB_VIA):geom=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2);ls=layers
 else:geom=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2);ls=[t.GetLayer()]
 if any(shapes[l].intersects(geom) for l in ls):b.RemoveNative(t);removed+=1
ids=[];vias={}
for a in plan:
 for x,z in zip(a['points'],a['points'][1:]):
  if Point(x).distance(Point(z))<1e-6:continue
  t=p.PCB_TRACK(b);t.SetStart(pt(x));t.SetEnd(pt(z));t.SetLayer(a['layer']);t.SetWidth(p.FromMM(.1));t.SetNet(b.FindNet(a['net']));b.Add(t);ids.append(t.m_Uuid.AsString())
 key=(a['net'],*map(lambda x:round(x,6),a['end']))
 if key in vias:continue
 v=p.PCB_VIA(b);v.SetPosition(pt(a['end']));v.SetWidth(p.FromMM(.3));v.SetDrill(p.FromMM(.15));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetFrontTentingMode(p.TENTING_MODE_TENTED);v.SetBackTentingMode(p.TENTING_MODE_TENTED);v.SetNet(b.FindNet(a['net']));b.Add(v);ids.append(v.m_Uuid.AsString());vias[key]=v
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b);(O/'fanout-protected.json').write_text(json.dumps(ids,indent=2));print('Applied',len(plan),'fanouts;',len(vias),'vias;',removed,'old routing items removed')
