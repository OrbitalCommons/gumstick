#!/usr/bin/env python3
"""Reroute audit-identified narrow runs at their neighboring wider width.

Same layer, fixed endpoints, no new vias. Checks geometry and existing contacts;
KiCad DRC/refill remains required after applying this candidate batch.
"""
from pathlib import Path
import sys,json,math,subprocess
import numpy as np
from collections import defaultdict
import pcbnew as p
from shapely.geometry import Point,LineString,Polygon
from shapely.strtree import STRtree
from shapely.ops import unary_union
from shapely import contains_xy
from audit_trace_widths import polygons,xy,uid,track_line
R=Path(__file__).resolve().parents[2];PATH=R/'boards/esp32-fpga-module/module.kicad_pcb';O=R/'tmp/width-fixes/search';O.mkdir(exist_ok=True);b=p.LoadBoard(str(PATH));report=json.loads(Path(sys.argv[1]).read_text());changes=[];attempted=set()
def pt(q):return p.VECTOR2I(round(q[0]*1e6),round(q[1]*1e6))
def ends(t):return xy(t.GetStart()),xy(t.GetEnd())
def geom(t,layer=None):
 if isinstance(t,p.PAD):
  poly=p.SHAPE_POLY_SET();t.TransformShapeToPolygon(poly,layer,0,1000,p.ERROR_OUTSIDE);return polygons(poly)
 if isinstance(t,p.PCB_VIA):return Point(xy(t.GetPosition())).buffer(t.GetWidth(p.F_Cu)/2e6,quad_segs=32)
 return track_line(t).buffer(t.GetWidth()/2e6,quad_segs=32)
def options(a,c):
 dx=c[0]-a[0];dy=c[1]-a[1];sx=1 if dx>=0 else -1;sy=1 if dy>=0 else -1;d=min(abs(dx),abs(dy))
 for q in [[a,(a[0]+sx*d,a[1]+sy*d),c],[a,(c[0]-sx*d,c[1]-sy*d),c],[a,(a[0],c[1]),c],[a,(c[0],a[1]),c]]:
  v=[]
  for x in q:
   x=tuple(round(z,6) for z in x)
   if not v or x!=v[-1]:v.append(x)
  if len(v)>1:yield v
outline=p.SHAPE_POLY_SET();assert b.GetBoardPolygonOutlines(outline,False);boundary=polygons(outline).buffer(-.3)
for row in report['transitions']:
 if row['contact']=='copper_overlap':continue
 key=tuple(row['narrow_run_tracks']);w=row['wide_mm']
 if (key,w) in attempted:continue
 attempted.add((key,w));index={uid(t):t for t in b.GetTracks()}
 if not all(k in index for k in key):continue
 tracks=[index[k] for k in key];net=tracks[0].GetNetname();layer=tracks[0].GetLayer();adj=defaultdict(list)
 for t in tracks:
  for a in ends(t):adj[a].append(t)
 terminals=[a for a,ts in adj.items() if len(ts)==1]
 if len(terminals)!=2 or any(len(ts)>2 for ts in adj.values()):continue
 a,c=terminals;oldlength=sum(t.GetLength()/1e6 for t in tracks)
 others=[geom(pad,layer) for f in b.GetFootprints() for pad in f.Pads() if pad.GetNetname()!=net and pad.IsOnLayer(layer)]
 others += [geom(t) for t in b.GetTracks() if t.GetNetname()!=net and ((isinstance(t,p.PCB_VIA) and t.IsOnLayer(layer)) or t.GetLayer()==layer)]
 keep=[polygons(z.Outline()) for z in b.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowTracks() and z.IsOnLayer(layer)]
 tree=STRtree(others);clear=.1+w/2-.000002
 def valid(q):
  if len(q)<2:return False
  g=LineString(q);cu=g.buffer(w/2,quad_segs=32)
  return not len(tree.query(g,predicate='dwithin',distance=clear)) and boundary.buffer(.000002).covers(cu) and not any(cu.intersects(k) for k in keep)
 def best(a,c):return next((q for q in sorted(options(a,c),key=lambda q:sum(math.dist(a,c) for a,c in zip(q,q[1:]))) if valid(q)),None)
 if any(len(tree.query(Point(e),predicate='dwithin',distance=clear)) for e in [a,c]):continue
 result=best(a,c)
 for margin in [.7,1.5,3.]:
  if result is not None:break
  S=.01;x0=max(100.3+w/2,math.floor((min(a[0],c[0])-margin)/S)*S);y0=max(101.75+w/2,math.floor((min(a[1],c[1])-margin)/S)*S)
  x1=min(119.7-w/2,max(a[0],c[0])+margin);y1=min(145.3-w/2,max(a[1],c[1])+margin);W=round((x1-x0)/S)+1;H=round((y1-y0)/S)+1
  if W<3 or H<3:continue
  mask=np.zeros((H,W),np.uint8)
  for g in [o.buffer(clear+.000003) for o in others]+[o.buffer(w/2) for o in keep]:
   l,bot,r,top=g.bounds;ix=max(0,math.floor((l-x0)/S));ex=min(W,math.ceil((r-x0)/S)+1);iy=max(0,math.floor((bot-y0)/S));ey=min(H,math.ceil((top-y0)/S)+1)
   if ex<=ix or ey<=iy:continue
   xx,yy=np.meshgrid(x0+np.arange(ix,ex)*S,y0+np.arange(iy,ey)*S);mask[iy:ey,ix:ex]|=contains_xy(g,xx,yy)
  def launch(v):
   d={};vx=round((v[0]-x0)/S);vy=round((v[1]-y0)/S)
   for y in range(max(1,vy-10),min(H-1,vy+11)):
    for x in range(max(1,vx-10),min(W-1,vx+11)):
     if mask[y,x]:continue
     e=(round(x0+x*S,6),round(y0+y*S,6));q=[v] if e==v else best(v,e)
     if q is not None:d[y*W+x]=q
   return d
  src,dst=launch(a),launch(c)
  if not src or not dst:continue
  with (O/'search.bin').open('wb') as f:
   np.array([W,H,1,len(src),len(dst)],np.int32).tofile(f);mask.tofile(f);np.ones((H,W),np.uint8).tofile(f);np.array(list(src),np.int32).tofile(f);np.array(list(dst),np.int32).tofile(f)
  rr=subprocess.run([str(R/'tmp/module-layout/finish'),str(O)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if rr.returncode:continue
  raw=[tuple(map(int,l.split())) for l in (O/'path.txt').read_text().splitlines()];q=src[raw[0][1]*W+raw[0][0]][:]
  q.extend((round(x0+x*S,6),round(y0+y*S,6)) for x,y,z in raw[1:]);q.extend(list(reversed(dst[raw[-1][1]*W+raw[-1][0]]))[1:]);simple=[q[0]];i=0
  while i<len(q)-1:
   for j in range(len(q)-1,i,-1):
    v=best(q[i],q[j])
    if v:simple.extend(v[1:]);i=j;break
   else:simple.append(q[i+1]);i+=1
  if valid(simple):result=simple
 if result is None or sum(math.dist(a,c) for a,c in zip(result,result[1:]))>oldlength*1.5+.5:continue
 oldc=unary_union([geom(t) for t in tracks]);newc=LineString(result).buffer(w/2+.000002,quad_segs=32)
 contacts=[geom(pad,layer) for f in b.GetFootprints() for pad in f.Pads() if pad.GetNetname()==net and pad.IsOnLayer(layer)]
 contacts += [geom(t) for t in b.GetTracks() if uid(t) not in key and t.GetNetname()==net and ((isinstance(t,p.PCB_VIA) and t.IsOnLayer(layer)) or t.GetLayer()==layer)]
 if any(oldc.intersects(g) and not newc.intersects(g) for g in contacts):continue
 r={'net':net,'layer':b.GetLayerName(layer),'from':row['narrow_mm'],'to':w,'old':list(key),'new':[],'path':result}
 for a,c in zip(result,result[1:]):
  if a==c:continue
  t=p.PCB_TRACK(b);t.SetStart(pt(a));t.SetEnd(pt(c));t.SetWidth(round(w*1e6));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t);r['new'].append(uid(t))
 for t in tracks:b.RemoveNative(t)
 changes.append(r);print('WIDENED',net,r['layer'],row['narrow_mm'],'to',w,'segments',len(key),'->',len(r['new']),flush=True)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(PATH),b);(O.parent/'neck-reroutes.json').write_text(json.dumps(changes,indent=2)+'\n');print('DONE',len(changes),flush=True)
