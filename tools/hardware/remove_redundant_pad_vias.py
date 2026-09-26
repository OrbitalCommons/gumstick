#!/usr/bin/env python3
"""Delete pad vias only when full KiCad DRC verifies connectivity is preserved."""
from pathlib import Path
import pcbnew as p,json,subprocess
from shapely.geometry import Point,box
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';path=D/'module.kicad_pcb';out=R/'tmp/module-layout/current.json'
def check():
 subprocess.run(['kicad-cli','pcb','drc','--schematic-parity','--format','json','-o',str(out),str(path)],check=True,stdout=subprocess.DEVNULL)
 j=json.loads(out.read_text());return not j['unconnected_items'] and not j.get('schematic_parity') and not any(v['severity']=='error' for v in j['violations'])
assert check()
b=p.LoadBoard(str(path));uids=[]
for v in b.GetTracks():
 if not isinstance(v,p.PCB_VIA):continue
 g=Point(p.ToMM(v.GetPosition().x),p.ToMM(v.GetPosition().y)).buffer(p.ToMM(v.GetWidth(p.F_Cu))/2);hit=False
 for f in b.GetFootprints():
  for a in f.Pads():
   x,y=p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y);sx,sy=p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)
   if round(a.GetOrientationDegrees())%180==90:sx,sy=sy,sx
   if g.intersects(box(x-sx/2,y-sy/2,x+sx/2,y+sy/2)):hit=True;break
  if hit:break
 if hit:uids.append(v.m_Uuid.AsString())
for uid in uids:
 original=path.read_bytes();b=p.LoadBoard(str(path));v=next(t for t in b.GetTracks() if t.m_Uuid.AsString()==uid);net=v.GetNetname();center=v.GetPosition();radius=v.GetWidth(p.F_Cu)/2
 for t in list(b.GetTracks()):
  if isinstance(t,p.PCB_VIA) or t.GetNetCode()!=v.GetNetCode():continue
  for end in [t.GetStart(),t.GetEnd()]:
   if (end-center).EuclideanNorm()<=radius+t.GetWidth()/2 and end!=center:
    seg=p.PCB_TRACK(b);seg.SetStart(end);seg.SetEnd(center);seg.SetLayer(t.GetLayer());seg.SetWidth(p.FromMM(.1));seg.SetNet(v.GetNet());b.Add(seg)
 b.RemoveNative(v);p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
 if check():print('Removed redundant',net,uid,flush=True)
 else:path.write_bytes(original);print('Retained necessary',net,uid,flush=True)
check()
