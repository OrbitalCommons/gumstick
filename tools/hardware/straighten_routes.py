#!/usr/bin/env python3
"""Simplify routed chains to octilinear geometry without moving pads or vias.

Uses actual KiCad pad polygons and foreign-net clearance obstacles. A subsequent
KiCad DRC comparison is required before accepting the resulting board.
"""
import sys, json, math
from pathlib import Path
from collections import defaultdict, Counter
import pcbnew as p
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'boards/esp32-fpga-module/module.kicad_pcb'
OUT=ROOT/'tmp/octilinear';OUT.mkdir(exist_ok=True,parents=True)
b=p.LoadBoard(str(PATH))

def xy(v):return (v.x/1e6,v.y/1e6)
def point(q):return p.VECTOR2I(round(q[0]*1e6),round(q[1]*1e6))
def uid(t):return t.m_Uuid.AsString()
def ends(t):return (xy(t.GetStart()),xy(t.GetEnd()))
def geo(t,layer=None):
 if isinstance(t,p.PAD):
  poly=p.SHAPE_POLY_SET();t.TransformShapeToPolygon(poly,layer,0,1000,p.ERROR_OUTSIDE)
  shapes=[]
  for i in range(poly.OutlineCount()):
   o=poly.COutline(i);shapes.append(Polygon([xy(o.CPoint(j)) for j in range(o.PointCount())]))
  return unary_union(shapes)
 if isinstance(t,p.PCB_VIA):return Point(xy(t.GetPosition())).buffer(t.GetWidth(p.F_Cu)/2e6,quad_segs=24)
 return LineString(ends(t)).buffer(t.GetWidth()/2e6,quad_segs=16)
def octi(a,c):
 dx=abs(round((c[0]-a[0])*1e6));dy=abs(round((c[1]-a[1])*1e6))
 return min(dx,dy)<=1 or abs(dx-dy)<=1

def routes(a,c):
 dx=c[0]-a[0];dy=c[1]-a[1];sx=1 if dx>=0 else -1;sy=1 if dy>=0 else -1;m=min(abs(dx),abs(dy))
 yield [a,(a[0]+sx*m,a[1]+sy*m),c]
 yield [a,(c[0]-sx*m,c[1]-sy*m),c]
 yield [a,(a[0],c[1]),c];yield [a,(c[0],a[1]),c]
 # Symmetric doglegs are useful when a direct corner clips adjacent pads.
 for frac in [.5,.25,.75]:
  if abs(dx)>=abs(dy):
   z=(abs(dx)-abs(dy))*frac
   yield [a,(a[0]+sx*z,a[1]),(a[0]+sx*(z+abs(dy)),c[1]),c]
  else:
   z=(abs(dy)-abs(dx))*frac
   yield [a,(a[0],a[1]+sy*z),(c[0],a[1]+sy*(z+abs(dx))),c]
def tidy(qs):
 q=[]
 for a in qs:
  a=tuple(round(v,6) for v in a)
  if not q or a!=q[-1]:q.append(a)
 return q

def measure(q):return sum(math.dist(a,c) for a,c in zip(q,q[1:]))+.18*(len(q)-2)
allpads=[a for f in b.GetFootprints() for a in f.Pads()]
changes=[];stats=Counter()
netnames=sorted({t.GetNetname() for t in b.GetTracks() if not isinstance(t,p.PCB_VIA)})
for net in netnames:
 tracks=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()==net]
 grouped=defaultdict(list)
 for t in tracks:grouped[(t.GetLayer(),t.GetWidth())].append(t)
 for (layer,width),ts in grouped.items():
  other=[]
  for a in allpads:
   if a.GetNetname()!=net and a.IsOnLayer(layer):other.append(geo(a,layer))
  for t in b.GetTracks():
   if t.GetNetname()!=net and (isinstance(t,p.PCB_VIA) or t.GetLayer()==layer):other.append(geo(t))
  for zone in b.Zones():
   if zone.GetIsRuleArea() and zone.GetDoNotAllowTracks() and zone.IsOnLayer(layer):
    poly=zone.Outline()
    for oi in range(poly.OutlineCount()):
     o=poly.COutline(oi);other.append(Polygon([xy(o.CPoint(j)) for j in range(o.PointCount())]))
  tree=STRtree(other);clearance=.1+width/2e6-.000001
  def valid(q):
   if len(q)<2:return False
   ln=LineString(q)
   return not len(tree.query(ln,predicate='dwithin',distance=clearance))
  def best(a,c):
   options=sorted((tidy(q) for q in routes(a,c)),key=measure)
   return next((q for q in options if valid(q)),None)
  adj=defaultdict(list)
  for t in ts:
   for a in ends(t):adj[a].append(t)
  anchors=set(a for a,tt in adj.items() if len(tt)!=2)
  # Pad/via contacts and changes of width/layer must remain fixed.
  contacts=[geo(a,layer) for a in allpads if a.GetNetname()==net and a.IsOnLayer(layer)]
  contacts += [geo(t) for t in b.GetTracks() if t.GetNetname()==net and (isinstance(t,p.PCB_VIA) or (t.GetLayer()==layer and t.GetWidth()!=width))]
  ct=STRtree(contacts)
  for a in adj:
   if len(ct.query(Point(a),predicate='dwithin',distance=width/2e6+.000001)):anchors.add(a)
  seen=set()
  for first in ts:
   if uid(first) in seen:continue
   e=ends(first);start=next((a for a in e if a in anchors),e[0]);q=[start];chain=[];t=first
   while True:
    seen.add(uid(t));chain.append(t);a,c=ends(t);n=c if a==q[-1] else a;q.append(n)
    if n in anchors:break
    nxt=[v for v in adj[n] if uid(v) not in seen]
    if not nxt:break
    t=nxt[0]
   # Greedy longest visible shortcuts remove stair-stepping while retaining
   # attachment points. Individual odd segments use the same clearance test.
   result=[q[0]];i=0
   while i<len(q)-1:
    chosen=None
    for j in range(len(q)-1,i,-1):
     cand=best(q[i],q[j])
     if cand is not None and (measure(cand)<=measure(q[i:j+1])+.00001 or j==i+1):
      chosen=(j,cand);break
    if chosen is None:result.append(q[i+1]);i+=1
    else:i,cand=chosen;result.extend(cand[1:])
   if result==q:continue
   # A shortcut must retain every copper contact with the rest of this net,
   # including T junctions that KiCad stores without splitting the track.
   oldc=LineString(q).buffer(width/2e6)
   newc=LineString(result).buffer(width/2e6+.000001)
   chainids={uid(v) for v in chain}
   touching=[geo(a,layer) for a in allpads if a.GetNetname()==net and a.IsOnLayer(layer)]
   touching += [geo(v) for v in b.GetTracks() if uid(v) not in chainids and v.GetNetname()==net and (isinstance(v,p.PCB_VIA) or v.GetLayer()==layer)]
   if any(oldc.intersects(g) and not newc.intersects(g) for g in touching):
    stats['contact_preserved_chains']+=1
    continue
   # Preserve all existing same-net contacts: DRC also independently checks
   # topology after the complete batch.
   olds=[{'uuid':uid(v),'start':ends(v)[0],'end':ends(v)[1]} for v in chain]
   new=[]
   for a,c in zip(result,result[1:]):
    if a==c:continue
    t=p.PCB_TRACK(b);t.SetStart(point(a));t.SetEnd(point(c));t.SetLayer(layer);t.SetWidth(width);t.SetNet(b.FindNet(net));b.Add(t);new.append(uid(t))
   for v in chain:b.RemoveNative(v)
   changes.append({'net':net,'layer':layer,'width':width,'old':olds,'new':new})
   stats['removed_segments']+=len(chain);stats['added_segments']+=len(new)
  print(net,dict(stats),flush=True)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(PATH),b)
(OUT/'changes.json').write_text(json.dumps(changes,indent=2))
print('RESULT',dict(stats))
