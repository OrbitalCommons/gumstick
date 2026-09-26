#!/usr/bin/env python3
"""One-time Abracon→Pulse antenna ECO. Run on the pre-Pulse routed board only."""
from pathlib import Path
import json,pcbnew as p,math
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';f=str(D/'module.kicad_pcb');b=p.LoadBoard(f)
pt=lambda x,y:p.VECTOR2I(p.FromMM(x+100),p.FromMM(y+100))
xy=lambda v:(p.ToMM(v.x)-100,p.ToMM(v.y)-100)
fps={fp.GetReference():fp for fp in b.GetFootprints()}
assert fps['AE1'].GetValue()=='ACAG0201-2450-T','ECO already applied or wrong input'
# RF-only reroute. Keep original ESP32 matching (RF_IN) and all digital/power nets.
for t in list(b.GetTracks()):
 q=xy(t.GetStart());z=xy(t.GetEnd())
 if t.GetNetname() in ['/RF_ANT','/RF_CHIP','/RF_ANT_MATCH','/RF_EXT'] or (t.GetNetname()=='GND' and (min(q[1],z[1])<7.0 or math.dist(q,(10.04332,7.26256))<.001)):b.RemoveNative(t)
for z in list(b.Zones()):
 if z.GetIsRuleArea() and ('PROVISIONAL_RF' in z.GetZoneName() or 'JP1 exposed' in z.GetZoneName()):b.RemoveNative(z)
name='AE1_Pulse_ANT2012LL00R2400A'
# Datasheet p3: inner land gap 1.70 mm; feed land .40 x 1.40;
# isolated solder land 1.00 x 1.40. Component envelope centered at (0,0).
fptext=f'''(footprint "{name}" (version 20240108) (generator pcbnew) (layer "F.Cu")
 (descr "Pulse ANT2012LL00R2400A; datasheet p2/p3; pad2 isolated solder terminal")
 (attr smd)
 (fp_text reference "AE1" (at 0 1.3) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
 (fp_text value "ANT2012LL00R2400A" (at 0 -1.5) (layer "F.Fab") hide (effects (font (size 1 1) (thickness .15))))
 (fp_rect (start -1 -.625) (end 1 .625) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
 (fp_rect (start -1.5 -.95) (end 2.1 .95) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
 (pad "1" smd rect (at -1.05 0) (size .4 1.4) (layers "F.Cu" "F.Paste" "F.Mask"))
 (pad "1" smd rect (at -2.75 0) (size 3 1.4) (layers "F.Cu"))
 (pad "2" smd rect (at 1.35 0) (size 1.0 1.4) (layers "F.Cu" "F.Paste" "F.Mask"))
 (model "${{KIPRJMOD}}/3dmodels/ANT2012LL00R2400A.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))))'''
(D/'Module.pretty'/f'{name}.kicad_mod').write_text(fptext)
old=fps['AE1'];new=p.FootprintLoad(str(D/'Module.pretty'),name);new.SetReference('AE1');new.SetValue('ANT2012LL00R2400A');new.SetUuid(old.m_Uuid);new.SetPath(old.GetPath());new.SetFPID(p.LIB_ID('Module',name));b.RemoveNative(old);b.Add(new);fps['AE1']=new
placements={'AE1':(2,4.2,90),'JP1':(11,5.8,180),'J3':(15.5,4,0),'R63':(2,9.7,90),'C68':(3.6,10.5,0),'C69':(3.6,8.9,0)}
for ref,(x,y,ang) in placements.items():
 fp=fps[ref];fp.SetOrientationDegrees(ang);fp.SetPosition(pt(x,y))
nc=p.NETINFO_ITEM(b,'unconnected-(AE1-NC-Pad2)');b.Add(nc)
new.SetValue('ANT2012LL00R2400A')
for a in new.Pads():a.SetNet(b.FindNet('/RF_ANT_MATCH') if a.GetNumber()=='1' else b.FindNet('unconnected-(AE1-NC-Pad2)'))
for k,v in {'MPN':'ANT2012LL00R2400A','Manufacturer':'Pulse Electronics','LCSC':'C3284792'}.items():new.SetField(k,v);new.GetField(k).SetVisible(False)
new.Reference().SetPosition(pt(4.1,4.2));new.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));new.Reference().SetTextSize(p.VECTOR2I(800000,800000));new.Reference().SetTextThickness(120000)
fps['J3'].Reference().SetPosition(pt(18.5,4));fps['J3'].Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
# 7 mm tip clearance on all copper layers. Antenna's own F.Cu feed/lands are allowed.
def keepout(name,poly,layers,tracks=False,vias=True):
 z=p.ZONE(b);z.SetIsRuleArea(True);z.SetZoneName(name);ls=p.LSET()
 for layer in layers:ls.AddLayer(layer)
 z.SetLayerSet(ls);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowTracks(tracks);z.SetDoNotAllowVias(vias);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False)
 o=z.Outline();o.NewOutline()
 for x,y in poly:o.Append(pt(x,y).x,pt(x,y).y)
 b.Add(z)
keepout('Pulse antenna 7mm clearance - F copper feed only',[(0,1.45),(10,1.45),(10,8.45),(0,8.45)],[p.F_Cu])
keepout('Pulse antenna 7mm clearance - no inner or bottom copper',[(0,1.45),(10,1.45),(10,8.45),(0,8.45)],[p.In1_Cu,p.In2_Cu,p.B_Cu],True)
keepout('JP1 exposed selector ground-pour clearance',[(10,5.25),(12,5.25),(12,6.35),(10,6.35)],[p.F_Cu],False,False)
def line(net,points,w=.26,layer=p.F_Cu):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(p.FromMM(w));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t)
def via(x,y):
 v=p.PCB_VIA(b);v.SetPosition(pt(x,y));v.SetWidth(450000);v.SetDrill(200000);v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));b.Add(v)
# Original chip matching output is L3.2 at y=8.66, joined to C2.1.
for ref in placements:print(ref,[(a.GetNumber(),xy(a.GetPosition()),a.GetNetname()) for a in fps[ref].Pads()])
line('/RF_ANT',[(12.2,8.1),(12.2,8.66)])
line('/RF_ANT',[(12.2,8.1),(11,6.9),(11,5.8)])
line('/RF_EXT',[(11.6,5.8),(12.65,5.8),(14.45,4)])
line('/RF_CHIP',[(10.4,5.8),(10.3,5.9),(10.3,8.0),(9.6,8.7),(5.9,8.7),(5.2,9.4),(5.2,10.8),(4.6,11.4),(2,11.4),(2,10.21)])
line('/RF_CHIP',[(2,10.5),(3.12,10.5)])
# Broad feed is rectangular copper-only pad artwork in the footprint.
line('/RF_ANT_MATCH',[(2,8.45),(2,9.19)])
line('/RF_ANT_MATCH',[(2,8.9),(3.12,8.9)])
line('GND',[(4.08,8.9),(4.08,9.7),(4.08,10.5)],.25);via(4.08,9.7)
for y in [2.525,5.475]:line('GND',[(15.975,y),(17.8,y)],.3);via(17.8,y)
for x,y in [(10.6,2.2),(10.6,3.5),(13,2.2),(13,6.8),(12.6,7.2),(10.95,7.8),(5.9,9.7),(1,9.1)]:via(x,y)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(f,b)
# Persist selected identity and physical coordinates.
f=D/'docs/module-connectivity.json';data=json.loads(f.read_text());data['AE1'].update(value='ANT2012LL00R2400A',footprint='Module:'+name,mpn='ANT2012LL00R2400A',manufacturer='Pulse Electronics',lcsc='C3284792',sourcing_url='https://www.lcsc.com/product-detail/C3284792.html',sourcing_status='LCSC listed 363 in stock 2026-09-26; RF prototype tuning still required');data['AE1']['pins']['2'].update(name='NC',net=None);f.write_text(json.dumps(data,indent=2)+'\n')
f=D/'docs/placement.json';data=json.loads(f.read_text());data.update(placements);f.write_text(json.dumps(data,indent=2)+'\n')
