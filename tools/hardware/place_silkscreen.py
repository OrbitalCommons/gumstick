#!/usr/bin/env python3
"""Compact, pad-clear module markings; leaves placement and copper untouched."""
from pathlib import Path
import json, math
import pcbnew as p
from shapely.geometry import box,Point
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';path=D/'module.kicad_pcb';b=p.LoadBoard(str(path))
def pt(x,y):return p.VECTOR2I(p.FromMM(x+100),p.FromMM(y+100))
def rect(bb):return box(p.ToMM(bb.GetX())-100,p.ToMM(bb.GetY())-100,p.ToMM(bb.GetRight())-100,p.ToMM(bb.GetBottom())-100)
# Labels flank their packages; sparse passives retain fabrication-layer references.
preferred={'U1':(14.5,20.0),'U2':(14.5,44.0),'J3':(2.2,4.0),'U3':(13.5,24),'U4':(5.8,25.5),'U5':(5.8,32),'J1':(10,13.7),'J2':(10,37.5),'SJ1':(12.3,33.1),'TP1':(.8,35.7),'TP2':(17.5,33.1)}
obstacles={p.F_SilkS:[],p.B_SilkS:[]}
for f in b.GetFootprints():
 silk=p.B_SilkS if f.GetLayer()==p.B_Cu else p.F_SilkS
 pads=list(f.Pads())
 for pad in pads:obstacles[silk].append(rect(pad.GetBoundingBox()).buffer(.18))
 if pads and f.GetReference() not in ['TP1','TP2','H1','AE1']:
  # Keep references off the assembled component envelope as well as its lands.
  bounds=[rect(a.GetBoundingBox()).bounds for a in pads];obstacles[silk].append(box(min(a[0] for a in bounds),min(a[1] for a in bounds),max(a[2] for a in bounds),max(a[3] for a in bounds)).buffer(.15))
for obs in obstacles.values():obs.append(Point(10,28.25).buffer(3.6))
report={}
for f in b.GetFootprints():
 t=f.Reference();t.SetTextSize(p.VECTOR2I(p.FromMM(.75),p.FromMM(1.0)));t.SetTextThickness(p.FromMM(.15))
 if f.GetReference() not in preferred:continue
 layer=p.B_SilkS if f.GetLayer()==p.B_Cu else p.F_SilkS;t.SetLayer(layer);t.SetVisible(True);t.SetMirrored(layer==p.B_SilkS);t.SetTextAngle(p.EDA_ANGLE(90 if f.GetReference()=='TP1' else 0,p.DEGREES_T));t.SetHorizJustify(p.GR_TEXT_H_ALIGN_CENTER);t.SetVertJustify(p.GR_TEXT_V_ALIGN_CENTER)
 x,y=preferred[f.GetReference()];candidates=sorted([(x+dx*.1,y+dy*.1) for dx in range(-20,21) for dy in range(-20,21)],key=lambda q:math.dist(q,(x,y)))
 for q in candidates:
  t.SetPosition(pt(*q));bb=rect(t.GetBoundingBox()); hw=(bb.bounds[2]-bb.bounds[0])*.5; g=(box(q[0]-.58,q[1]-1.17,q[0]+.58,q[1]+1.17) if f.GetReference()=='TP1' else box(q[0]-hw,q[1]-.58,q[0]+hw,q[1]+.58)).buffer(.04)
  if box(.15,1.60,19.85,45.45).contains(g) and not any(g.intersects(o) for o in obstacles[layer]):break
 else:raise RuntimeError('No clear label position: '+f.GetReference())
 obstacles[layer].append(g.buffer(.12));report[f.GetReference()]=[round(v,3) for v in q]
# Keep a single readable label per IC, outside its package.
for ic in b.GetFootprints():
 if ic.GetReference().startswith('U'):
  for text in list(ic.GraphicalItems()):
   if isinstance(text,p.PCB_TEXT) and text.GetText() in ['${REFERENCE}','%R',ic.GetReference()]:ic.RemoveNative(text)
for t in b.GetDrawings():
 if isinstance(t,p.PCB_TEXT) and t.GetLayer() in obstacles:t.SetTextSize(p.VECTOR2I(p.FromMM(.75),p.FromMM(1.0)));t.SetTextThickness(p.FromMM(.15))
# Capacitor and resistor references clutter the PCB view, including duplicate Fab text.
for cap in b.GetFootprints():
 if cap.GetReference().startswith(('C','R')) or cap.GetReference() in ['H1','L1','L3','D1','L2']:
  cap.Reference().SetVisible(False)
  for text in list(cap.GraphicalItems()):
   if isinstance(text,p.PCB_TEXT) and text.GetText() in ['${REFERENCE}','%R',cap.GetReference()]:cap.RemoveNative(text)
p.SaveBoard(str(path),b);(D/'docs/silkscreen-placement.json').write_text(json.dumps({'text_height_mm':1.0,'text_width_mm':.75,'stroke_mm':.15,'positions_mm':report},indent=2)+'\n');print(report)
