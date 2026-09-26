#!/usr/bin/env python3
"""Route residual connections on a conservative grid; KiCad DRC is authoritative."""
from pathlib import Path
import pcbnew as p,numpy as np,json,math,subprocess,sys
from routing_constraints import VIA_DIAMETER_MM, VIA_DRILL_MM, VIA_HOLE_GAP_MM
from shapely.geometry import box,LineString,Point
from shapely import contains_xy
from shapely.strtree import STRtree
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';O=R/'tmp/module-layout'
S=.025;W=801;H=1825;layers=[p.F_Cu,p.In2_Cu,p.B_Cu];TW=.1;CLEAR=.105;VR=VIA_DIAMETER_MM/2
if '--four' in sys.argv:layers=[p.F_Cu,p.In2_Cu,p.B_Cu,p.In1_Cu]
# Use the project's exact 0.10 mm rule for dense escapes; DRC remains authoritative.
if '--exact-clearance' in sys.argv:CLEAR=.099999
# Avoid reconnecting obsolete floating remnants from prior fan-out changes.
subprocess.run([sys.executable,str(R/'tools/hardware/remove_orphan_signal_copper.py'),'--no-fill'],check=True)
subprocess.run(['kicad-cli','pcb','drc','--format','json','-o',str(O/'current.json'),str(D/'module.kicad_pcb')],check=True,stdout=subprocess.DEVNULL)
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
   from routing_constraints import pad_geometry
   geom=pad_geometry(a)
   arr.append((a.GetNetname(),ls,geom,a))
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):ls=list(range(len(layers)));geom=Point(*xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2)
  else:
   if t.GetLayer() not in layers:continue
   ls=[layers.index(t.GetLayer())];geom=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2)
  arr.append((t.GetNetname(),ls,geom,t))
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
def group(arr,uid):
 start=next((i for i,a in enumerate(arr) if a[3].m_Uuid.AsString()==uid),None)
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
 if any(n in item['items'][0]['description'] for n in ['[GND]','[+3.3V]']):continue
 if any('Zone' in a['description'] for a in item['items']):continue
 arr=objects();g1=group(arr,item['items'][0]['uuid']);g2=group(arr,item['items'][1]['uuid'])
 if not g1 or not g2:continue
 if {a[3].m_Uuid.AsString() for a in g1}&{a[3].m_Uuid.AsString() for a in g2}:continue
 net=g1[0][0]
 TW={'+1.2V':.25,'+1.2V_PLL':.15,'+1.8V':.25,'FPGA_VCCIO0':.25,'ESP_VDD3P3':.25,'VIN_5V':.4,'/USB_D-':.125,'/USB_D+':.125}.get(net,.1)
 if net in ['GND','+3.3V']:continue
 A=np.zeros((len(layers),H,W),np.uint8);V=np.zeros((H,W),np.uint8)
 for a in A:
  paint(a,box(0,0,20,7.7));paint(a,Point(10,28.25).buffer(3.5+TW/2+.01))
  for sh in [box(0,0,.36,46),box(19.64,0,20,46),box(0,45.24,20,46)]:paint(a,sh)
 if len(layers)==4:
  for sh in [box(0,0,20,9),box(11.5,0,20,12),box(0,21,20,34),box(0,0,1,46),box(19,0,20,46)]:paint(A[3],sh)
 from routing_constraints import paint_qfn_front_keepouts
 paint_qfn_front_keepouts(b,A[0],paint,net,TW)
 from routing_constraints import paint_qfn_via_keepouts
 paint_qfn_via_keepouts(b,V,paint,VR)
 paint(V,box(0,0,20,7.9));paint(V,Point(10,28.25).buffer(3.5+VR+.01))
 for sh in [box(0,0,.52,46),box(19.48,0,20,46),box(0,45.08,20,46)]:paint(V,sh)
 for n,ls,geom,t in arr:
  # Keep via copper and a solder-mask gap outside every component pad.
  if isinstance(t,p.PAD):
   paint(V,geom.buffer(VR+(.0251 if '--tight-tented-vias' in sys.argv else .0751)))
  if len(layers)==4 and n in ['/USB_D-','/USB_D+','/XTAL_P','/XTAL_P_CRYSTAL','/XTAL_N','/RF_IN','/RF_ANT'] and not ('--local-usb-crossing' in sys.argv and n in ['/USB_D-','/USB_D+']):
   paint(A[3],geom.buffer(.35))
  if isinstance(t,p.PCB_VIA):paint(V,Point(*xy(t.GetPosition())).buffer(p.ToMM(t.GetDrillValue())/2+VIA_DRILL_MM/2+VIA_HOLE_GAP_MM+.005))
  if n==net:continue
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
   track(start,a);v=p.PCB_VIA(b);v.SetPosition(pt(e[0]*S,e[1]*S));v.SetWidth(p.FromMM(VIA_DIAMETER_MM));v.SetDrill(p.FromMM(VIA_DRILL_MM));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));b.Add(v);start=e
  elif j==len(path)-1 or (path[j+1][0]-e[0],path[j+1][1]-e[1],path[j+1][2]-e[2])!=(e[0]-a[0],e[1]-a[1],0):track(start,e);start=e
 done+=1;print('Routed',net,len(path),flush=True);p.SaveBoard(str(D/'module.kicad_pcb'),b)
if '--no-fill' not in sys.argv:p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(D/'module.kicad_pcb'),b);print('Finished connections',done)
