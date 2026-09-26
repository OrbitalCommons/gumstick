#!/usr/bin/env python3
"""Remove disconnected non-plane copper fragments that reach no component pad."""
from pathlib import Path
import pcbnew as p,sys
from shapely.geometry import Point,LineString,box
from shapely.strtree import STRtree
from collections import defaultdict
R=Path(__file__).resolve().parents[2];path=R/'boards/esp32-fpga-module/module.kicad_pcb';b=p.LoadBoard(str(path));layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu];nets=defaultdict(list)
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
for f in b.GetFootprints():
 for a in f.Pads():
  n=a.GetNetname()
  if not n or n in ['GND','+3.3V']:continue
  x,y=xy(a.GetPosition());sx,sy=p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)
  if round(a.GetOrientationDegrees())%180==90:sx,sy=sy,sx
  from routing_constraints import pad_geometry
  from shapely.affinity import translate
  nets[n].append((a,translate(pad_geometry(a),100,100),{l for l in layers if a.IsOnLayer(l)}))
for t in b.GetTracks():
 n=t.GetNetname()
 if not n or n in ['GND','+3.3V']:continue
 if isinstance(t,p.PCB_VIA):g=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2);ls=set(layers)
 else:g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2);ls={t.GetLayer()}
 nets[n].append((t,g,ls))
removed=0
for net,items in nets.items():
 if net in ['/RF_IN','/RF_ANT','/XTAL_P','/XTAL_N','/XTAL_P_CRYSTAL','/USB_D-','/USB_D+','/BUCK_SW']:continue
 tree=STRtree([g for t,g,l in items]);seen=set();count=0
 for start in range(len(items)):
  if start in seen:continue
  todo=[start];seen.add(start);component=[];haspad=False
  while todo:
   i=todo.pop();component.append(i);t,g,ls=items[i];haspad|=isinstance(t,p.PAD)
   for k in tree.query(g,predicate='dwithin',distance=.00001):
    k=int(k)
    if k not in seen and ls&items[k][2]:seen.add(k);todo.append(k)
  if not haspad:
   for i in component:b.RemoveNative(items[i][0]);count+=1
 if count:print(net,count);removed+=count
if '--no-fill' not in sys.argv:p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(path),b);print('Removed orphan items',removed)
