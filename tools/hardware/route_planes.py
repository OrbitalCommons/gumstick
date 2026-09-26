#!/usr/bin/env python3
"""Route residual connections on a conservative grid; KiCad DRC is authoritative."""
from pathlib import Path
import pcbnew as p,numpy as np,json,math,subprocess,sys
from shapely.geometry import box,LineString,Point,Polygon
from shapely import contains_xy
from shapely.strtree import STRtree
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';O=R/'tmp/module-layout'
S=.025;W=801;H=1825;layers=[p.F_Cu,p.In2_Cu,p.B_Cu,p.In1_Cu];TW=.1;CLEAR=.105;VR=.15
if '--four' in sys.argv:layers=[p.F_Cu,p.In2_Cu,p.B_Cu,p.In1_Cu]
b=p.LoadBoard(str(D/'module.kicad_pcb'))
def xy(v):return p.ToMM(v.x)-100,p.ToMM(v.y)-100
def pt(x,y):return p.VECTOR2I(p.FromMM(100+x),p.FromMM(100+y))
def objects():
 arr=[]
 for f in b.GetFootprints():
  for a in f.Pads():
   ls=[z for z,l in enumerate(layers) if a.IsOnLayer(l)]
   if not ls:continue
   x,y=xy(a.GetPosition());sx=p.ToMM(a.GetSize().x);sy=p.ToMM(a.GetSize().y)
   if round(a.GetOrientationDegrees())%180==90:sx,sy=sy,sx
   geom=Point(x,y).buffer(sx/2) if a.GetShape()==p.PAD_SHAPE_CIRCLE else box(x-sx/2,y-sy/2,x+sx/2,y+sy/2)
   arr.append((a.GetNetname(),ls,geom,a))
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):ls=list(range(len(layers)));geom=Point(*xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2)
  else:
   if t.GetLayer() not in layers:continue
   ls=[layers.index(t.GetLayer())];geom=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2)
  arr.append((t.GetNetname(),ls,geom,t))
 for z in b.Zones():
  if z.GetIsRuleArea() or z.GetLayer() not in layers:continue
  polys=z.GetFilledPolysList(z.GetLayer())
  for i in range(polys.OutlineCount()):
   c=polys.COutline(i);outer=[xy(c.CPoint(j)) for j in range(c.PointCount())]
   holes=[]
   for h in range(polys.HoleCount(i)):
    c=polys.CHole(i,h);holes.append([xy(c.CPoint(j)) for j in range(c.PointCount())])
   geom=Polygon(outer,holes).buffer(0)
   if not geom.is_empty:arr.append((z.GetNetname(),[layers.index(z.GetLayer())],geom,z))
 return arr
paint_cache={}
def paint(a,shape):
 key=shape.wkb
 if key in paint_cache:
  a.reshape(-1)[paint_cache[key]]=1
  return
 x0,y0,x1,y1=shape.bounds;x0=max(0,math.floor(x0/S));x1=min(W-1,math.ceil(x1/S));y0=max(0,math.floor(y0/S));y1=min(H-1,math.ceil(y1/S))
 if x1<x0 or y1<y0:return
 xx,yy=np.meshgrid(np.arange(x0,x1+1)*S,np.arange(y0,y1+1)*S);m=contains_xy(shape.buffer(.000001),xx,yy);a[y0:y1+1,x0:x1+1]|=m;yy0,xx0=np.nonzero(m);paint_cache[key]=((yy0+y0)*W+xx0+x0).astype(np.int32)
def group(arr,uid,pos):
 matches=[i for i,a in enumerate(arr) if a[3].m_Uuid.AsString()==uid]
 start=min(matches,key=lambda i:arr[i][2].distance(Point(pos['x']-100,pos['y']-100))) if matches else None
 if start is None:return []
 net=arr[start][0];indices=[i for i,a in enumerate(arr) if a[0]==net];tree=STRtree([arr[i][2] for i in indices]);seen={start};todo=[start]
 while todo:
  i=todo.pop();a=arr[i]
  for k in tree.query(a[2],predicate='dwithin',distance=.00001):
   j=indices[k];c=arr[j]
   if j not in seen and set(a[1])&set(c[1]):seen.add(j);todo.append(j)
 return [arr[i] for i in seen]
def candidates(group,A):
 pts=set()
 for _,ls,geom,t in group:
  if isinstance(t,p.ZONE):
   z=ls[0];safe=geom.buffer(-.08)
   if safe.is_empty:continue
   x0,y0,x1,y1=safe.bounds
   xx,yy=np.meshgrid(np.arange(max(1,round(x0/S)),min(W-1,round(x1/S))+1,4),np.arange(max(1,round(y0/S)),min(H-1,round(y1/S))+1,4))
   valid=contains_xy(safe,xx*S,yy*S)&(A[z,yy,xx]==0)
   pts.update((z*H*W+yy[valid]*W+xx[valid]).tolist());continue
  if isinstance(t,p.PCB_VIA) or isinstance(t,p.PAD):coords=[xy(t.GetPosition())]
  else:
   a=np.array(xy(t.GetStart()));e=np.array(xy(t.GetEnd()));coords=[a+(e-a)*v for v in np.linspace(0,1,max(2,int(np.linalg.norm(e-a)/.07)))]
  for x,y in coords:
   xx=round(x/S);yy=round(y/S)
   if not 0<xx<W-1 or not 0<yy<H-1:continue
   for z in ls:
    if not A[z,yy,xx]:pts.add(z*H*W+yy*W+xx)
 return list(pts)
report=json.loads((O/'current.json').read_text());done=0
for item in report['unconnected_items']:
 arr=objects();g1=group(arr,item['items'][0]['uuid'],item['items'][0]['pos']);g2=group(arr,item['items'][1]['uuid'],item['items'][1]['pos'])
 if not g1 or not g2:continue
 if {id(a) for a in g1}&{id(a) for a in g2}:continue
 net=g1[0][0]
 if net not in ['GND','+3.3V']:continue
 A=np.zeros((len(layers),H,W),np.uint8);V=np.zeros((H,W),np.uint8)
 for a in A:
  paint(a,box(0,0,20,7.7));paint(a,Point(10,28.25).buffer(3.5+TW/2+.01))
  for sh in [box(0,0,.36,46),box(19.64,0,20,46),box(0,45.24,20,46)]:paint(a,sh)
 paint(V,box(0,0,20,7.9));paint(V,Point(10,28.25).buffer(3.5+VR+.01))
 for sh in [box(0,0,.52,46),box(19.48,0,20,46),box(0,45.08,20,46)]:paint(V,sh)
 for n,ls,geom,t in arr:
  # Keep via copper and a solder-mask gap outside every component pad.
  if isinstance(t,p.PAD):
   paint(V,geom.buffer(VR+.0751))
  if isinstance(t,p.PCB_VIA):paint(V,Point(*xy(t.GetPosition())).buffer(p.ToMM(t.GetDrillValue())/2+0.15/2+.255))
  if n==net or isinstance(t,p.ZONE):continue
  for z in ls:paint(A[z],geom.buffer(CLEAR+TW/2))
  paint(V,geom.buffer(CLEAR+VR))
 src=candidates(g1,A);tgt=candidates(g2,A)
 if not src or not tgt:print('No escape',net,len(src),len(tgt),flush=True);continue
 with (O/'search.bin').open('wb') as f:
  np.array([W,H,len(layers),len(src),len(tgt)],np.int32).tofile(f);A.tofile(f);V.tofile(f);np.array(src,np.int32).tofile(f);np.array(tgt,np.int32).tofile(f)
 r=subprocess.run([str(O/'finish'),str(O)])
 if r.returncode:print('No path',net,flush=True);continue
 path=[tuple(map(int,l.split())) for l in (O/'path.txt').read_text().splitlines()]
 def track(a,e):
  if a==e:return
  t=p.PCB_TRACK(b);t.SetStart(pt(a[0]*S,a[1]*S));t.SetEnd(pt(e[0]*S,e[1]*S));t.SetLayer(layers[a[2]]);t.SetWidth(p.FromMM(TW));t.SetNet(b.FindNet(net));b.Add(t)
 start=path[0]
 for j in range(1,len(path)):
  a,e=path[j-1],path[j]
  if a[2]!=e[2]:
   track(start,a);v=p.PCB_VIA(b);v.SetPosition(pt(e[0]*S,e[1]*S));v.SetWidth(p.FromMM(.3));v.SetDrill(p.FromMM(.15));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));b.Add(v);start=e
  elif j==len(path)-1 or (path[j+1][0]-e[0],path[j+1][1]-e[1],path[j+1][2]-e[2])!=(e[0]-a[0],e[1]-a[1],0):track(start,e);start=e
 done+=1;print('Routed',net,len(path),flush=True);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b);print('Finished connections',done)
