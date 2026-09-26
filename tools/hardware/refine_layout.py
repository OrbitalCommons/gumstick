#!/usr/bin/env python3
"""Placement for the four-layer dev module. Run before routing, not after."""
from pathlib import Path
import pcbnew as p,math,json,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';path=D/'module.kicad_pcb';b=p.LoadBoard(str(path))
def pt(x,y):return p.VECTOR2I(p.FromMM(x+100),p.FromMM(y+100))
def v(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
loc={
'D1':(14,44,0),'U1':(10,15.5,-90),'U2':(10,39.5,180),'AE1':(17.175,8.5,180),'Y1':(16.8,15,-90),'H1':(10,28.25,0),
'J1':(10,15.75,0),'J2':(10,40.75,0),
'U3':(14.5,23,0),'L4':(17,23,0),'C60':(12,22.5,90),'C61':(17,26,0),'R62':(14.5,20.8,0),
'U4':(10,48,0),'C62':(7,48,90),'C63':(13,48,90),
'L3':(9.7,10.5,180),'C1':(12.8,10.6,90),'C2':(8,10.5,270),'L1':(13,8.6,0),'C34':(14.5,8.3,90),'C35':(11.4,10.7,0),
'R3':(14.9,13.7,0),'C6':(15.9,12.5,0),'C7':(17.5,17,270),
'R20':(7,22,90),'R22':(16.5,9.7,0),'C32':(18.2,9.7,90),'R60':(15.6,19.7,90),'R61':(18,19.7,90),
'R28':(5.3,36.3,90),'R29':(9.4,34.5,180),
'C33':(8.5,23.7,0),'C37':(13.7,10.5,90),'C38':(5,14.9,0),'C39':(10,20.7,0),'C40':(7.8,20.7,90),'C41':(15.2,18.2,90),'C42':(15,10.9,90),
'L2':(15,38.75,180),'C43':(15.2,35.5,180),'C44':(15.3,37.3,180),'C45':(3.8,39,90),
'C46':(5.1,42.25,180),'C48':(11.75,34.7,180),'C49':(5.1,40.25,180),'C50':(16.5,39.7,180),'C52':(16.5,41.5,180)}
loc.update({'C34':(17,8,0),'U3':(13.8,23,0),'L4':(17.3,23,0),'R60':(18.5,22,90),'R62':(13.8,20.8,0),'C33':(4.3,22.8,0),'C45':(3,38.5,90)})
loc.update({'D1': (17.8, 44, 0)})
# Larger-via escape lanes; keep decoupling close while opening side channels.
loc.update({'C44': (4.125, 38.75, 180.0), 'C49': (4.25, 39.95, 180.0), 'C50': (15.7, 40.25, 0.0), 'C52': (15.7, 42.25, 0.0)})
# Power islands flank the central M3 spacer; keep support parts with each regulator.
loc.update({'U3':(16,27,0),'L4':(16,30.5,0),'C60':(16.5,24,0),'C61':(16,33,0),'R62':(18.7,27,90),'U4':(3,27.5,0),'C62':(2.5,24.5,0),'C63':(2.5,30.5,0)})
loc.update({'U3':(16,24,0),'L4':(16,27.5,0),'C60':(16,21.8,0),'C61':(16,30,0),'R62':(18.7,24,90),'U4':(3,23.525,0),'C62':(2.5,20.5,0),'C63':(2.5,26.5,0),'C39':(13.5,21,90),'C40':(6,20.5,90),'R20':(5.5,22.2,90),'C33':(3.8,29,0)})
loc.update({'C66':(3,42.5,90),})
loc.update({'L3':(12.2,9.5,90),'C1':(13.8,11,90),'C2':(13.6,8.5,90),'L1':(17,11,90),'C37':(15.4,11,90),'U3':(16,24,-90)})
loc.update({'L1':(18,11.3,0),'L2':(16,38.75,180),'C35':(10.4,10.7,0),'C60':(16,21.3,0)})
loc.update({'C1':(13.8,10.5,90),'C2':(13.6,8.5,270)})
loc.update({'C2':(13.6,8.5,0),'C61':(16,30,180),'C7':(18,16.5,0)})
# Center the QFNs; the current revision uses external package via keepouts.
loc.update({'U1':(10,15.5,-90),'U2':(10,39.5,180),'Y1':(17.8,15,-90),
 'R3':(16.2,13.2,0),'C6':(17.2,12.5,0),'C7':(18.7,17,0),
 'C35':(11.3,10.7,0),'C38':(6.5,14.9,180),'C40':(7.5,20.5,90),'C41':(16.5,18.2,90),'C42':(14.7,10,90),
 'R28':(3.1,36.3,90),'C45':(1.5,38.5,90),'C46':(3,42.25,180),'C49':(3,40.25,180),'C66':(1.5,42.5,90),
 'C48':(9.75,34.7,180),'C43':(13.2,35.5,180),'C44':(13.3,37.3,180),'L2':(14,38.75,180),'C50':(13.1,39.7,180),'C52':(13.1,41.5,180)})
loc.update({'R3':(16.7,13.2,0),'C35':(10.4,10.7,0),'C48':(11.75,34.7,180),'C42':(14.5,9.9,90)})
loc.update({'C42':(15.2,9,90),'C6':(18.2,12.4,0),'C43':(13.7,35.7,180)})
loc.update({'C38':(5,14.9,180),'C43':(15.7,35.7,180),'C44':(15.3,37.3,180),'L2':(16,38.75,180),'C50':(16.5,39.7,180),'C52':(16.5,41.5,180),'TP1':(2.1,34.5,0),'TP2':(17.5,34,0)})
# Whole-run routing cleanup: align supply pads with their feeds.
loc.update({'C39':(13.5,21,270),'C60':(16.1,21.3,0),'R61':(18.15,19.7,90)})
# Decoupling placement: keep local capacitors alongside their supply pins.
loc.update({'C34': (10.0, 8.4, 0.0), 'C35': (11.2154, 10.75, 180.0), 'C37': (14.3, 11.75, 0.0), 'C39': (15.55, 17.0, 90.0), 'C40': (4.25, 17.6, 180.0), 'C41': (7.8, 20.65, -90.0), 'C42': (15.15, 12.9, 90.0), 'C43': (3.75, 37.7, 0.0), 'C44': (4.725, 38.75, 180.0), 'C46': (4.25, 41.25, 180.0), 'C48': (7.3, 34.6, 180.0), 'C49': (4.6, 39.95, 180.0), 'C50': (15.4, 40.25, 0.0), 'C52': (15.4, 42.25, 0.0), 'L2': (4.5, 34.8, 0.0)})
# Compact buck output capacitors and aligned left-side regulator capacitors.
loc.update({'C63': (1.95, 26.3, 0.0), 'C33': (1.95, 27.9, 0.0), 'C64': (1.95, 29.5, 0.0), 'C65': (4.95, 29.5, 0.0), 'C61': (16.0, 29.8, 180.0), 'C67': (16.0, 32.5, 180.0)})
# Remove development markings, imported dimensional artwork, and routes (fresh placement only).
for obj in list(b.GetTracks())+list(b.Zones())+list(b.GetDrawings()):
 b.RemoveNative(obj)
for a,c in [((0,1.45),(20,1.45)),((20,1.45),(20,46.45)),((20,46.45),(0,46.45)),((0,46.45),(0,1.45))]:
 edge=p.PCB_SHAPE(b);edge.SetShape(p.SHAPE_T_SEGMENT);edge.SetStart(pt(*a));edge.SetEnd(pt(*c));edge.SetLayer(p.Edge_Cuts);edge.SetWidth(p.FromMM(.05));b.Add(edge)
for f in b.GetFootprints():
 ref=f.GetReference();x,y,a=loc[ref]
 # Flip first so all placements use world orientation as specified.
 if f.GetLayer()==p.B_Cu:f.Flip(f.GetPosition(),False)
 f.SetOrientationDegrees(a);f.SetPosition(pt(x,y))
 if ref in ['J1','J2']:f.Flip(f.GetPosition(),False)
 for g in list(f.GraphicalItems()):
  if g.GetLayer() in [p.Dwgs_User,p.Cmts_User,p.F_SilkS,p.B_SilkS]:f.RemoveNative(g)
 for field in f.GetFields():field.SetVisible(False)
 f.Reference().SetVisible(True);f.Reference().SetLayer(p.B_SilkS if ref.startswith('J') else p.F_SilkS);f.Reference().SetTextSize(v(.8,.8));f.Reference().SetTextThickness(p.FromMM(.12));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetPosition(pt(x,y-1.8 if ref[0] in 'RCL' else y-4.7))
 for pad in f.Pads():pad.SetLocalSolderMaskMargin(0)
 if ref not in {'U1','U2','J1','J2'}:f.Reference().SetLayer(p.B_Fab if f.GetLayer()==p.B_Cu else p.F_Fab)
 if ref=='AE1':
  f.ClearNetTiePadGroups();f.AddNetTiePadGroup('P$1,P$2')
 if ref=='L4':
  for pad in f.Pads():pad.SetSize(v(1,2.9));pad.SetPosition(pt(x+(-1.015 if pad.GetNumber()=='1' else 1.015),y))
# Pad names including explicit unconnected nets are taken from the exported schematic.
r=E.parse(D/'fab/checks/module-netlist.xml').getroot();pn={};netmap={}
for n in r.find('nets'):
 net=p.NETINFO_ITEM(b,n.get('name'));b.Add(net);netmap[n.get('name')]=net
 for node in n.findall('node'):pn[node.get('ref'),node.get('pin')]=net
for f in b.GetFootprints():
 for pad in f.Pads():
  net=pn.get((f.GetReference(),pad.GetNumber()))
  if net:pad.SetNet(net)
# All-copper antenna exclusion (copper belonging to AE1 and its feed remains on top).
def keepout(poly,layers,tracks=False):
 z=p.ZONE(b);z.SetIsRuleArea(True);ls=p.LSET()
 for layer in layers:ls.AddLayer(layer)
 z.SetLayerSet(ls);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowTracks(tracks);z.SetDoNotAllowVias(True);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False)
 o=z.Outline();o.NewOutline()
 for x,y in poly:o.Append(pt(x,y).x,pt(x,y).y)
 b.Add(z)
keepout([(1,1.45),(19,1.45),(19,7.5),(1,7.5)],[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu])
# Screw-head / spacer keepout, 7 mm diameter, through all copper layers.
keepout([(10+3.5*math.cos(i*math.pi/32),28.25+3.5*math.sin(i*math.pi/32)) for i in range(64)],[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu],True)
for txt,x,y,layer in [('J1 / ESP + USB',10,20,p.B_SilkS),('J2 / FPGA',15,43,p.B_SilkS)]:
 t=p.PCB_TEXT(b);t.SetText(txt);t.SetPosition(pt(x,y));t.SetTextSize(v(.8,.8));t.SetTextThickness(p.FromMM(.12));t.SetLayer(layer);t.SetMirrored(layer==p.B_SilkS);b.Add(t)
b.GetDesignSettings().SetBoardThickness(p.FromMM(1.0));# Capacitor and resistor references clutter the PCB view, including duplicate Fab text.
for cap in b.GetFootprints():
 if cap.GetReference().startswith(('C','R')):
  cap.Reference().SetVisible(False)
  for text in list(cap.GraphicalItems()):
   if isinstance(text,p.PCB_TEXT) and text.GetText() in ['${REFERENCE}','%R',cap.GetReference()]:cap.RemoveNative(text)
p.SaveBoard(str(path),b)
(D/'docs/placement.json').write_text(json.dumps(loc,indent=2)+'\n')
print('Placed',len(loc),'footprints')
