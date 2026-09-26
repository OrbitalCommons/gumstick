#!/usr/bin/env python3
"""Remove unused signal copper branches, guarded by a fresh KiCad DRC."""
from pathlib import Path
import pcbnew as p,json,subprocess
from shapely.geometry import Point,LineString,box
from shapely.strtree import STRtree
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';path=D/'module.kicad_pcb';out=R/'tmp/module-layout/current.json';original=path.read_bytes();b=p.LoadBoard(str(path));layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu];groups={}
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
def wanted(n):return n.startswith(('/ESP_GPIO','/FPGA_IO','/LINK_','/SYNC_IO'))
for f in b.GetFootprints():
 for a in f.Pads():
  n=a.GetNetname()
  if not wanted(n):continue
  x,y=xy(a.GetPosition());sx,sy=p.ToMM(a.GetSize().x)/2,p.ToMM(a.GetSize().y)/2
  if round(a.GetOrientationDegrees())%180==90:sx,sy=sy,sx
  groups.setdefault(n,[]).append((a,box(x-sx,y-sy,x+sx,y+sy),{l for l in layers if a.IsOnLayer(l)},False))
for t in b.GetTracks():
 n=t.GetNetname()
 if not wanted(n):continue
 if isinstance(t,p.PCB_VIA):g=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2);ls=set(layers)
 else:g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2);ls={t.GetLayer()}
 groups.setdefault(n,[]).append((t,g,ls,True))
removed=0
for net,arr in groups.items():
 tree=STRtree([a[1] for a in arr]);adj=[set() for _ in arr]
 for i,a in enumerate(arr):
  for j in tree.query(a[1],predicate='dwithin',distance=.000001):
   j=int(j)
   if j!=i and a[2]&arr[j][2]:adj[i].add(j)
 todo=[i for i,a in enumerate(arr) if a[3] and len(adj[i])<2];dead=set()
 while todo:
  i=todo.pop()
  if i in dead or not arr[i][3] or len(adj[i])>1:continue
  dead.add(i)
  for j in list(adj[i]):
   adj[j].discard(i)
   if arr[j][3] and len(adj[j])<2:todo.append(j)
  adj[i].clear()
 for i in dead:b.RemoveNative(arr[i][0]);removed+=1
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
subprocess.run(['kicad-cli','pcb','drc','--schematic-parity','--format','json','-o',str(out),str(path)],check=True,stdout=subprocess.DEVNULL)
j=json.loads(out.read_text())
if j['unconnected_items'] or j.get('schematic_parity') or any(v['severity']=='error' for v in j['violations']):
 path.write_bytes(original);raise SystemExit('Pruning reverted: DRC guard failed')
print('Removed',removed,'unused signal copper items; remaining violations',len(j['violations']))
