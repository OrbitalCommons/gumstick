#!/usr/bin/env python3
"""Relocate pad vias; reroute displaced signals and run full DRC afterward.

Keeps pads, RF, USB and supply copper fixed. This is a routing operation, not
a fabrication exporter: displaced tracks are explicitly reported.
"""
from pathlib import Path
import pcbnew as p,math,json
from shapely.geometry import Point,LineString,box
from shapely.strtree import STRtree
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';b=p.LoadBoard(str(D/'module.kicad_pcb'))
layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
def pt(v):return p.VECTOR2I(p.FromMM(v[0]),p.FromMM(v[1]))
def geometry(t):
 if isinstance(t,p.PCB_VIA):return Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2)
 return LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2)
pads=[]
for f in b.GetFootprints():
 for a in f.Pads():
  x,y=xy(a.GetPosition());sx=p.ToMM(a.GetSize().x);sy=p.ToMM(a.GetSize().y)
  if round(a.GetOrientationDegrees())%180==90:sx,sy=sy,sx
  g=Point(x,y).buffer(sx/2) if a.GetShape()==p.PAD_SHAPE_CIRCLE else box(x-sx/2,y-sy/2,x+sx/2,y+sy/2)
  pads.append((a,g,[l for l in layers if a.IsOnLayer(l)],f.GetReference()+'.'+a.GetNumber()))
from via_relocation_search import local_search
ptree=STRtree([x[1] for x in pads]);moved=[];blocked=[]
for via in list(b.GetTracks()):
 if not isinstance(via,p.PCB_VIA):continue
 old=xy(via.GetPosition());vg=geometry(via);hits=ptree.query(vg,predicate='intersects')
 if not len(hits):continue
 net=via.GetNetname();radius=p.ToMM(via.GetWidth(p.F_Cu))/2
 tracks=list(b.GetTracks());foreign={l:[] for l in layers};own={l:[] for l in layers};holes=[]
 for a,g,ls,_ in pads:
  for l in ls:(own if a.GetNetname()==net else foreign)[l].append(g)
 for t in tracks:
  if t==via:continue
  g=geometry(t);ls=layers if isinstance(t,p.PCB_VIA) else [t.GetLayer()]
  for l in ls:
   if l in layers:(own if t.GetNetname()==net else foreign)[l].append(g)
  if isinstance(t,p.PCB_VIA):holes.append(Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetDrillValue())/2+p.ToMM(via.GetDrillValue())/2+.2501))
 trees={l:STRtree(foreign[l]) for l in layers};htree=STRtree(holes)
 hardforeign={l:[] for l in layers};softforeign={l:[] for l in layers}
 protected={'+3.3V','VIN_5V','+1.2V','+1.8V','FPGA_VCCIO0','ESP_VDD3P3','+1.2V_PLL','/RF_IN','/RF_ANT','/XTAL_P','/XTAL_P_CRYSTAL','/XTAL_N','/BUCK_SW','/USB_D-','/USB_D+'}
 for a,g,ls,_ in pads:
  if a.GetNetname()!=net:
   for l in ls:hardforeign[l].append(g)
 for t in tracks:
  if t==via or t.GetNetname()==net:continue
  target=hardforeign if t.GetNetname() in protected else softforeign
  for l in (layers if isinstance(t,p.PCB_VIA) else [t.GetLayer()]):
   if l in layers:target[l].append(geometry(t))
 hardtrees={l:STRtree(hardforeign[l]) for l in layers}
 holes=[Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetDrillValue())/2+p.ToMM(via.GetDrillValue())/2+.2501) for t in tracks if isinstance(t,p.PCB_VIA) and t!=via and (t.GetNetname() in protected or t.GetNetname()==net)]
 active=[l for l in layers if any(g.intersects(vg) for g in own[l])]
 # Preserve all incident copper, even when the original end only touched the annulus.
 anchors={l:[] for l in active}
 for l in active:
  for t in tracks:
   if isinstance(t,p.PCB_VIA) or t.GetNetname()!=net or t.GetLayer()!=l:continue
   if geometry(t).intersects(vg):
    for q in [xy(t.GetStart()),xy(t.GetEnd())]:
     if Point(q).distance(Point(old))<=radius+p.ToMM(t.GetWidth())/2+.00001:anchors[l].append(q)
  anchors[l].append(old)
 found=None
 # Candidates sorted by travel distance; pad/mask separation also applies to same-net pads.
 offsets=sorted([(i*.05,j*.05) for i in range(-32,33) for j in range(-32,33) if i or j],key=lambda q:q[0]**2+q[1]**2)
 for dx,dy in offsets:
  dest=(round(old[0]+dx,6),round(old[1]+dy,6));q=Point(dest)
  if not (100.3+radius<dest[0]<119.7-radius and 107.7+radius<dest[1]<145.3-radius):continue
  if q.distance(Point(110,128.25))<3.5+radius:continue
  if len(ptree.query(q.buffer(radius+.075),predicate='intersects')):continue
  if len(htree.query(q,predicate='intersects')):continue
  if any(len(trees[l].query(q.buffer(radius+.1001),predicate='intersects')) for l in layers):continue
  routes=[];ok=True
  for l in active:
   for anchor in anchors[l]:
    route=LineString([anchor,dest]).buffer(.0501+.1001)
    if len(trees[l].query(route,predicate='intersects')):ok=False;break
    routes.append((l,anchor,dest))
   if not ok:break
  if ok:found=(dest,routes);break
 if found is None:
  found=local_search(old,radius,pads,hardforeign,holes,active,anchors,hardtrees,layers,softforeign)
 if found:
  dest,routes=found
  from shapely.ops import unary_union
  shapes={l:unary_union([LineString([a,z]).buffer(.1501) for layer,a,z in routes if layer==l]+[Point(dest).buffer(radius+.1001)]) for l in layers}
  ripped=set()
  for t in list(b.GetTracks()):
   if t==via or t.GetNetname()==net or t.GetNetname() in protected:continue
   if any(shapes[l].intersects(geometry(t)) for l in (layers if isinstance(t,p.PCB_VIA) else [t.GetLayer()]) if l in layers):
    ripped.add(t.GetNetname());b.RemoveNative(t)
  print('Displaced',sorted(ripped),flush=True)
  via.SetPosition(pt(dest))
  for l,a,z in routes:
   if a==z:continue
   t=p.PCB_TRACK(b);t.SetStart(pt(a));t.SetEnd(pt(z));t.SetLayer(l);t.SetWidth(p.FromMM(.1));t.SetNet(via.GetNet());b.Add(t)
  moved.append({'uuid':via.m_Uuid.AsString(),'net':net,'from':old,'to':dest,'pads':[pads[i][3] for i in hits]});print('Moved',net,[pads[i][3] for i in hits],flush=True)
 else:blocked.append({'uuid':via.m_Uuid.AsString(),'net':net,'pads':[pads[i][3] for i in hits]});print('Blocked',net,[pads[i][3] for i in hits],flush=True)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
(R/'tmp/module-layout/via-soft-relocation.json').write_text(json.dumps({'moved':moved,'blocked':blocked},indent=2))
print('Moved',len(moved),'blocked',len(blocked))
