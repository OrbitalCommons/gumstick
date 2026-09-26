#!/usr/bin/env python3
"""Build conservative clearance grids around the checked critical routes."""
from pathlib import Path
import pcbnew as p,numpy as np,json,math
from shapely.geometry import box,LineString,Point
from shapely import contains_xy
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';O=R/'tmp/module-layout';b=p.LoadBoard(str(D/'module.kicad_pcb'))
STEP=.05;W=681;H=721;A=np.zeros((3,H,W),dtype=np.int16);V=np.zeros((H,W),dtype=np.int16);K=np.zeros((H,W),dtype=np.uint8)
# Slightly more than nominal 0.127 mm clearance to cover quantization.
CLEAR=.135;TW=.10;VR=.20
names=sorted({a.GetNetname() for f in b.GetFootprints() for a in f.Pads() if a.GetNetname()});ids={n:i+1 for i,n in enumerate(names)}
def xy(pos):return p.ToMM(pos.x)-100,p.ToMM(pos.y)-100
def paint(arr,shape,owner):
 x0,y0,x1,y1=shape.bounds;x0=max(0,int(math.floor(x0/STEP)));y0=max(0,int(math.floor(y0/STEP)));x1=min(W-1,int(math.ceil(x1/STEP)));y1=min(H-1,int(math.ceil(y1/STEP)))
 if x1<x0 or y1<y0:return
 xx,yy=np.meshgrid(np.arange(x0,x1+1)*STEP,np.arange(y0,y1+1)*STEP);m=contains_xy(shape.buffer(.00001),xx,yy);a=arr[y0:y1+1,x0:x1+1]
 if arr.dtype==np.uint8:a[m]=1
 elif owner==-1:a[m]=-1
 else:a[m&(a==0)]=owner;a[m&(a!=owner)]=-1
hole=Point(17,18).buffer(3.5+TW/2+CLEAR)
antenna=box(8.3,0,25.8,7.5)
for layer in A:
 paint(layer,hole,-1);paint(layer,antenna,-1)
 paint(layer,box(0,0,.4,36),-1);paint(layer,box(33.6,0,34,36),-1);paint(layer,box(0,0,34,.4),-1);paint(layer,box(0,35.6,34,36),-1)
paint(V,Point(17,18).buffer(3.5+VR+CLEAR),-1);paint(V,antenna.buffer(VR),-1)
for shape in [box(0,0,.65,36),box(33.35,0,34,36),box(0,0,34,.65),box(0,35.35,34,36)]:paint(V,shape,-1)
terms={n:[] for n in names}
for f in b.GetFootprints():
 for pad in f.Pads():
  if not pad.IsOnLayer(p.F_Cu) and not pad.IsOnLayer(p.B_Cu):continue
  name=pad.GetNetname();nid=ids.get(name,-1);x,y=xy(pad.GetPosition());sx=p.ToMM(pad.GetSize().x);sy=p.ToMM(pad.GetSize().y);ang=pad.GetOrientationDegrees()%180
  if abs(ang-90)<1:sx,sy=sy,sx
  shape=box(x-sx/2,y-sy/2,x+sx/2,y+sy/2)
  # No unfilled vias inside any component's solder lands. Thermal vias were placed explicitly.
  paint(K,shape.buffer(VR+.10),1)
  paint(V,shape.buffer(VR+CLEAR),nid)
  for z,layer in [(0,p.F_Cu),(2,p.B_Cu)]:
   if pad.IsOnLayer(layer):paint(A[z],shape.buffer(TW/2+CLEAR),nid)
  if name and not name.startswith('unconnected-'):
   if f.GetReference()=='AE1':continue
   if f.GetReference() in ['U1','U2','U3'] and name=='/GND':continue
   terms[name].append([round(x/STEP),round(y/STEP),0 if pad.IsOnLayer(p.F_Cu) else 2,f.GetReference(),pad.GetNumber()])
for t in b.GetTracks():
 name=t.GetNetname();nid=ids[name]
 if isinstance(t,p.PCB_VIA):
  shape=Point(*xy(t.GetPosition()));radius=p.ToMM(t.GetWidth(p.F_Cu))/2
  for a in A:paint(a,shape.buffer(radius+CLEAR+TW/2),nid)
  paint(V,shape.buffer(radius+CLEAR+VR),nid)
 else:
  shape=LineString([xy(t.GetStart()),xy(t.GetEnd())]);radius=p.ToMM(t.GetWidth())/2;z={p.F_Cu:0,p.In2_Cu:1,p.B_Cu:2}[t.GetLayer()]
  paint(A[z],shape.buffer(radius+CLEAR+TW/2),nid);paint(V,shape.buffer(radius+CLEAR+VR),nid)
# Skip already completed, intentionally hand-routed networks.
skip={'/RF_IN','/RF_ANT','/XTAL_P','/XTAL_P_CRYSTAL','/XTAL_N','/BUCK_SW','/USB_D-','/USB_D+'}

# Reserve outward escapes before other nets can block fine-pitch pads.
escapes=[]
for name,ps in terms.items():
 if name in skip:continue
 for term in ps:
  x,y,z,ref,padnum=term
  if ref not in ['U1','U2','J1','J2']:continue
  fp=b.FindFootprintByReference(ref);fx,fy=xy(fp.GetPosition());wx=x*STEP;wy=y*STEP
  dx,dy=wx-fx,wy-fy
  if ref in ['J1','J2']:
   # J1 is vertical, J2 horizontal.
   dx,dy=(1 if dx>0 else -1,0) if ref=='J1' else (0,1 if dy>0 else -1)
  else:dx,dy=(1 if dx>0 else -1,0) if abs(dx)>abs(dy) else (0,1 if dy>0 else -1)
  for dist in [1.0,.85,.7,.55]:
   end=(round(x+dx*dist/STEP),round(y+dy*dist/STEP));valid=True
   for t in np.linspace(0,1,round(dist/STEP)+1):
    xx=round(x+(end[0]-x)*t);yy=round(y+(end[1]-y)*t)
    if xx<1 or xx>=W-1 or yy<1 or yy>=H-1 or A[z,yy,xx] not in [0,ids[name]]:valid=False;break
   if valid:
    shape=LineString([(wx,wy),(end[0]*STEP,end[1]*STEP)])
    paint(A[z],shape.buffer(TW/2+CLEAR),ids[name]);paint(V,shape.buffer(TW/2+CLEAR+VR),ids[name]);escapes.append(f'T {ids[name]} {z} {x} {y} {end[0]} {end[1]}');term[0],term[1]=end;break
(O/'escapes.txt').write_text('\n'.join(escapes)+'\n')

with (O/'grid.bin').open('wb') as f:
 np.array([W,H,3],dtype=np.int32).tofile(f);A.tofile(f);V.tofile(f);K.tofile(f)
with (O/'nets.txt').open('w') as f:
 for n in names:
  if n in skip or not terms[n]:continue
  # Ground pads connect individually to the solid ground plane; other nets form trees.
  mode=1 if n in ['/GND','/+3.3V'] else 0
  if len(terms[n])<2 and mode==0:continue
  priority=0 if n.startswith('/LINK') else 1 if n.startswith('/USB') else 2 if n.startswith('/FPGA_C') or n=='/SYNC_IO' else 3
  f.write(f'{ids[n]} {mode} {priority} {len(terms[n])}\n')
  for x,y,z,ref,pad in terms[n]:f.write(f'{x} {y} {z}\n')
(O/'route-meta.json').write_text(json.dumps({'step':STEP,'names':{v:k for k,v in ids.items()},'terms':terms},indent=2))
print('Routing grid:',A.shape,'nets:',len(names))
