#!/usr/bin/env python3
"""Replace residual off-angle tracks using same-layer octilinear search."""
from pathlib import Path
# Share geometry helpers without running the whole-board simplification pass.
exec((Path(__file__).with_name('straighten_routes.py')).read_text().split('netnames=')[0])
import numpy as np,subprocess
from shapely import contains_xy
changes=[]
for t in list(b.GetTracks()):
 if isinstance(t,p.PCB_VIA) or octi(*ends(t)):continue
 a,c=ends(t);net=t.GetNetname();layer=t.GetLayer();width=t.GetWidth();clearance=.1+width/2e6-.000001
 other=[geo(v,layer) for v in allpads if v.GetNetname()!=net and v.IsOnLayer(layer)]
 other += [geo(v) for v in b.GetTracks() if v.GetNetname()!=net and (isinstance(v,p.PCB_VIA) or v.GetLayer()==layer)]
 for z in b.Zones():
  if z.GetIsRuleArea() and z.GetDoNotAllowTracks() and z.IsOnLayer(layer):
   ps=z.Outline()
   for i in range(ps.OutlineCount()):
    o=ps.COutline(i);other.append(Polygon([xy(o.CPoint(j)) for j in range(o.PointCount())]))
 tree=STRtree(other)
 def valid(q):return not len(tree.query(LineString(q),predicate='dwithin',distance=clearance))
 def best(u,v):return next((q for q in sorted((tidy(q) for q in routes(u,v)),key=measure) if len(q)>1 and valid(q)),None)
 result=best(a,c)
 for margin in [.7,2.,5.]:
  if result is not None:break
  S=.01;x0=max(100.36,math.floor((min(a[0],c[0])-margin)/S)*S);y0=max(101.81,math.floor((min(a[1],c[1])-margin)/S)*S)
  x1=min(119.64,max(a[0],c[0])+margin);y1=min(145.24,max(a[1],c[1])+margin)
  W=round((x1-x0)/S)+1;H=round((y1-y0)/S)+1
  A=np.zeros((H,W),np.uint8)
  for g in other:
   g=g.buffer(clearance+.000002);l,bot,r,top=g.bounds
   ix=max(0,math.floor((l-x0)/S));ex=min(W,math.ceil((r-x0)/S)+1);iy=max(0,math.floor((bot-y0)/S));ey=min(H,math.ceil((top-y0)/S)+1)
   if ex<=ix or ey<=iy:continue
   xx,yy=np.meshgrid(x0+np.arange(ix,ex)*S,y0+np.arange(iy,ey)*S);A[iy:ey,ix:ex]|=contains_xy(g,xx,yy)
  def launches(v):
   d={};vx=round((v[0]-x0)/S);vy=round((v[1]-y0)/S)
   for yy in range(max(1,vy-12),min(H-1,vy+13)):
    for xx in range(max(1,vx-12),min(W-1,vx+13)):
     if A[yy,xx]:continue
     e=(round(x0+xx*S,6),round(y0+yy*S,6));q=[v] if v==e else best(v,e)
     if q is not None:d[yy*W+xx]=q
   return d
  src=launches(a);dst=launches(c)
  if not src or not dst:continue
  with (OUT/'search.bin').open('wb') as f:
   np.array([W,H,1,len(src),len(dst)],np.int32).tofile(f);A.tofile(f);np.ones((H,W),np.uint8).tofile(f);np.array(list(src),np.int32).tofile(f);np.array(list(dst),np.int32).tofile(f)
  r=subprocess.run([str(ROOT/'tmp/module-layout/finish'),str(OUT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if r.returncode:continue
  raw=[tuple(map(int,l.split())) for l in (OUT/'path.txt').read_text().splitlines()]
  q=src[raw[0][1]*W+raw[0][0]][:]
  q.extend((round(x0+x*S,6),round(y0+y*S,6)) for x,y,z in raw[1:]);q.extend(list(reversed(dst[raw[-1][1]*W+raw[-1][0]]))[1:])
  # Remove grid stair steps using long, clearance-checked octilinear shortcuts.
  simple=[q[0]];i=0
  while i<len(q)-1:
   found=False
   for j in range(len(q)-1,i,-1):
    cand=best(q[i],q[j])
    if cand is not None:simple.extend(cand[1:]);i=j;found=True;break
   if not found:simple.append(q[i+1]);i+=1
  if valid(simple):result=simple
 if result is None:print('UNRESOLVED',net,a,c,flush=True);continue
 old={'uuid':uid(t),'start':a,'end':c};new=[]
 for u,v in zip(result,result[1:]):
  nt=p.PCB_TRACK(b);nt.SetStart(point(u));nt.SetEnd(point(v));nt.SetLayer(layer);nt.SetWidth(width);nt.SetNet(t.GetNet());b.Add(nt);new.append(uid(nt))
 b.RemoveNative(t);changes.append({'net':net,'layer':layer,'width':width,'old':[old],'new':new})
 print('CONVERTED',net,len(new),flush=True)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(PATH),b)
(OUT/'escape-changes.json').write_text(json.dumps(changes,indent=2))
