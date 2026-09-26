#!/usr/bin/env python3
"""Simplify complete power runs; preserve contacts and bound resistance increase.

Candidate-only geometry repair. Requires full KiCad DRC/refill after execution.
Never changes RF widths, vias, pads, or component placement. No blanket thinning.
"""
from pathlib import Path
import json,math
from collections import defaultdict,Counter
import pcbnew as p
from shapely.geometry import Point,LineString,Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
from audit_trace_widths import polygons,xy,uid,track_line
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';PATH=D/'module.kicad_pcb';OUT=R/'tmp/width-fixes';OUT.mkdir(exist_ok=True)
b=p.LoadBoard(str(PATH));TARGETS={'VIN_5V':.4,'+3.3V':.4,'+1.2V':.25,'+1.8V':.25,'FPGA_VCCIO0':.25,'ESP_VDD3P3':.25,'+1.2V_PLL':.25,'GND':.25}
EPS=.000002

def pt(q):return p.VECTOR2I(round(q[0]*1e6),round(q[1]*1e6))
def ends(t):return (xy(t.GetStart()),xy(t.GetEnd()))
def geom(t,layer=None):
 if isinstance(t,p.PAD):
  poly=p.SHAPE_POLY_SET();t.TransformShapeToPolygon(poly,layer,0,1000,p.ERROR_OUTSIDE);return polygons(poly)
 if isinstance(t,p.PCB_VIA):return Point(xy(t.GetPosition())).buffer(t.GetWidth(p.F_Cu)/2e6,quad_segs=32)
 return track_line(t).buffer(t.GetWidth()/2e6,quad_segs=32)
def routes(a,c):
 dx=c[0]-a[0];dy=c[1]-a[1];sx=1 if dx>=0 else -1;sy=1 if dy>=0 else -1;m=min(abs(dx),abs(dy))
 yield [a,(a[0]+sx*m,a[1]+sy*m),c];yield [a,(c[0]-sx*m,c[1]-sy*m),c]
 yield [a,(a[0],c[1]),c];yield [a,(c[0],a[1]),c]
 for frac in [.25,.5,.75]:
  if abs(dx)>=abs(dy):
   z=(abs(dx)-abs(dy))*frac;yield [a,(a[0]+sx*z,a[1]),(a[0]+sx*(z+abs(dy)),c[1]),c]
  else:
   z=(abs(dy)-abs(dx))*frac;yield [a,(a[0],a[1]+sy*z),(c[0],a[1]+sy*(z+abs(dx))),c]
def tidy(q):
 arr=[]
 for a in q:
  a=tuple(round(v,6) for v in a)
  if not arr or a!=arr[-1]:arr.append(a)
 return arr

def score(segments):
 steps=sum(abs(a[2]-c[2])>EPS for a,c in zip(segments,segments[1:]));length=sum(math.dist(a,c) for a,c,w in segments)
 return steps*8+len(segments)*.15+length*.03

def squares(segments):return sum(math.dist(a,c)/w for a,c,w in segments)
# Remove literal duplicate segments first, retaining the wider duplicate.
seen={};duplicates=0
for t in list(b.GetTracks()):
 if isinstance(t,(p.PCB_VIA,p.PCB_ARC)):continue
 key=(t.GetNetCode(),t.GetLayer(),tuple(sorted(ends(t))))
 if key in seen:
  keep=seen[key]
  if t.GetWidth()>keep.GetWidth():keep.SetWidth(t.GetWidth())
  b.RemoveNative(t);duplicates+=1
 else:seen[key]=t
pads=[a for f in b.GetFootprints() for a in f.Pads()];changes=[]
outline=p.SHAPE_POLY_SET();assert b.GetBoardPolygonOutlines(outline,False);inside=polygons(outline).buffer(-.3)
for net,target in TARGETS.items():
 for layer in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]:
  tracks=[t for t in b.GetTracks() if not isinstance(t,(p.PCB_VIA,p.PCB_ARC)) and t.GetNetname()==net and t.GetLayer()==layer]
  if not tracks:continue
  others=[geom(a,layer) for a in pads if a.GetNetname()!=net and a.IsOnLayer(layer)]
  others += [geom(t) for t in b.GetTracks() if t.GetNetname()!=net and ((isinstance(t,p.PCB_VIA) and t.IsOnLayer(layer)) or t.GetLayer()==layer)]
  keepouts=[polygons(z.Outline()) for z in b.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowTracks() and z.IsOnLayer(layer)]
  tree=STRtree(others)
  def valid(q,w):
   if len(q)<2:return False
   line=LineString(q);copper=line.buffer(w/2,quad_segs=32)
   return inside.buffer(EPS).covers(copper) and not len(tree.query(line,predicate='dwithin',distance=.1+w/2-EPS)) and not any(copper.intersects(g) for g in keepouts)
  def best(a,c,w):
   options=sorted((tidy(q) for q in routes(a,c)),key=lambda q:sum(math.dist(a,c) for a,c in zip(q,q[1:]))+.05*len(q))
   return next((q for q in options if valid(q,w)),None)
  def simplify(q,w):
   out=[q[0]];i=0
   while i<len(q)-1:
    for j in range(len(q)-1,i,-1):
     v=best(q[i],q[j],w)
     if v:out.extend(v[1:]);i=j;break
    else:return None
   return out
  adj=defaultdict(list)
  for t in tracks:
   for a in ends(t):adj[a].append(t)
  terminal=[geom(a,layer) for a in pads if a.GetNetname()==net and a.IsOnLayer(layer)]
  terminal += [geom(t) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()==net and t.IsOnLayer(layer)]
  anchors={a for a,ts in adj.items() if len(ts)!=2 or any(g.distance(Point(a))<EPS for g in terminal)}
  # Preserve interior centerline branches as anchors at adjacent endpoints.
  ct=STRtree([track_line(t) for t in tracks])
  for a,ts in adj.items():
   touching=ct.query(Point(a),predicate='dwithin',distance=EPS)
   if len(touching)>len(ts):anchors.add(a)
  used=set();chains=[]
  for start in list(anchors)+list(adj):
   for first in adj[start]:
    if uid(first) in used:continue
    chain=[];q=[start];t=first
    while True:
     used.add(uid(t));chain.append(t);a,c=ends(t);end=c if a==q[-1] else a;q.append(end)
     if end in anchors:break
     nxt=[t for t in adj[end] if uid(t) not in used]
     if len(nxt)!=1:break
     t=nxt[0]
    chains.append((chain,q))
  for chain,q in chains:
   old=[(a,c,t.GetWidth()/1e6) for (a,c),t in zip(zip(q,q[1:]),chain)]
   # Include constant-width chains to remove kinks, but never increase complexity.
   winner=old;oldscore=score(old);oldres=squares(old);minw=min(w for a,c,w in old)
   for w in sorted(set([target,minw]+[v for v in [.15,.2,.25,.3,.4] if minw<=v<=target]),reverse=True):
    # Keep any required short neck at either end. Only original path vertices
    # within 0.8 mm can bound necks, so no arbitrary mid-run width island remains.
    lens=[0.]
    for a,c in zip(q,q[1:]):lens.append(lens[-1]+math.dist(a,c))
    starts=[0]+[i for i in range(1,len(q)-1) if lens[i]<=.8]
    finishes=[len(q)-1]+[i for i in range(1,len(q)-1) if lens[-1]-lens[i]<=.8]
    # Limit dense grid fanout candidates to representative neck lengths.
    starts=sorted(set(starts[::max(1,len(starts)//5)]+starts[-1:]))
    finishes=sorted(set(finishes[::max(1,len(finishes)//5)]+finishes[-1:]))
    for st in starts:
     for en in finishes:
      if st>=en:continue
      mid=simplify(q[st:en+1],w)
      if not mid:continue
      pre=simplify(q[:st+1],old[0][2]) if st else [q[0]]
      post=simplify(q[en:],old[-1][2]) if en<len(q)-1 else [q[-1]]
      if pre is None or post is None:continue
      proposal=[(a,c,old[0][2]) for a,c in zip(pre,pre[1:])]+[(a,c,w) for a,c in zip(mid,mid[1:])]+[(a,c,old[-1][2]) for a,c in zip(post,post[1:])]
      # <=1 mOhm added resistance at 35 um copper, also <=2% for long runs.
      if squares(proposal)>oldres+min(2.,oldres*.02)+EPS or score(proposal)>=score(winner)-EPS:continue
      oldc=unary_union([geom(t) for t in chain]);newc=unary_union([LineString([a,c]).buffer(ww/2+EPS,quad_segs=32) for a,c,ww in proposal]);ids={uid(t) for t in chain}
      same=terminal+[geom(t) for t in b.GetTracks() if uid(t) not in ids and t.GetNetname()==net and not isinstance(t,p.PCB_VIA) and t.GetLayer()==layer]
      if any(oldc.intersects(g) and not newc.intersects(g) for g in same):continue
      winner=proposal
   if winner==old:continue
   record={'net':net,'layer':b.GetLayerName(layer),'old':[{'uuid':uid(t),'start':a,'end':c,'width':w} for t,(a,c,w) in zip(chain,old)],'new':[],'old_squares':oldres,'new_squares':squares(winner),'old_score':oldscore,'new_score':score(winner)}
   for a,c,w in winner:
    if a==c:continue
    t=p.PCB_TRACK(b);t.SetStart(pt(a));t.SetEnd(pt(c));t.SetWidth(round(w*1e6));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t);record['new'].append(uid(t))
   for t in chain:b.RemoveNative(t)
   changes.append(record)
  print(net,b.GetLayerName(layer),'changed',len(changes),flush=True)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(PATH),b);(OUT/'run-repairs.json').write_text(json.dumps({'duplicates_removed':duplicates,'changes':changes},indent=2)+'\n');print('DONE',len(changes),'runs;',duplicates,'duplicates',flush=True)
