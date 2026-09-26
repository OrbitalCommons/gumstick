#!/usr/bin/env python3
"""Trim dangling copper to its actual junctions, with a DRC connectivity guard."""
from pathlib import Path
import pcbnew as p,json,subprocess,re,sys
from collections import Counter
from shapely.geometry import Point,LineString,box
from shapely.ops import nearest_points
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';path=D/'module.kicad_pcb';O=R/'tmp/module-layout';original=path.read_bytes();b=p.LoadBoard(str(path));before=json.loads((O/'current.json').read_text())
def count(j):return Counter(re.search(r'\[([^]]+)\]',v['items'][0]['description'])[1] for v in j['unconnected_items'])
opens=set(count(before));wanted={x['uuid'] for v in before['violations'] if v['type'] in ['via_dangling','track_dangling'] for x in v['items']}
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
def pt(q):return p.VECTOR2I(p.FromMM(q[0]),p.FromMM(q[1]))
def shape(t):
 if isinstance(t,p.PAD):
  x,y=xy(t.GetPosition());sx,sy=p.ToMM(t.GetSize().x)/2,p.ToMM(t.GetSize().y)/2
  if round(t.GetOrientationDegrees())%180==90:sx,sy=sy,sx
  return box(x-sx,y-sy,x+sx,y+sy)
 if isinstance(t,p.PCB_VIA):return Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2)
 return LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2)
def coords(g):
 if hasattr(g,'geoms'):
  for x in g.geoms:yield from coords(x)
 elif hasattr(g,'coords'):yield from g.coords
trimmed=removed=0
for t in list(b.GetTracks()):
 if t.m_Uuid.AsString() not in wanted or t.GetNetname() in opens:continue
 if '--vias-only' in sys.argv and not isinstance(t,p.PCB_VIA):continue
 if '--tracks-only' in sys.argv and isinstance(t,p.PCB_VIA):continue
 net=t.GetNetname();g=shape(t)
 if isinstance(t,p.PCB_VIA):
  center=xy(t.GetPosition());bridges=set()
  for other in list(b.GetTracks()):
   if isinstance(other,p.PCB_VIA) or other.GetNetname()!=net or not shape(other).intersects(g):continue
   line=LineString([xy(other.GetStart()),xy(other.GetEnd())]);q=nearest_points(line,Point(center))[0]
   if q.distance(Point(center))<1e-7:continue
   start=q.coords[0];key=(other.GetLayer(),tuple(round(v,6) for v in start),tuple(round(v,6) for v in center))
   if key in bridges:continue
   bridges.add(key)
   dx,dy=center[0]-start[0],center[1]-start[1];d=min(abs(dx),abs(dy))
   corner=(start[0]+(d if dx>=0 else -d),start[1]+(d if dy>=0 else -d))
   # Retain the adjoining trace width and use only 45/90-degree segments.
   # The board-wide DRC guard below rejects any newly introduced conflict.
   for a,z in zip([start,corner],[corner,center]):
    a=tuple(round(v,6) for v in a);z=tuple(round(v,6) for v in z)
    if a==z:continue
    spur=p.PCB_TRACK(b);spur.SetStart(pt(a));spur.SetEnd(pt(z));spur.SetLayer(other.GetLayer());spur.SetWidth(other.GetWidth());spur.SetNet(t.GetNet());b.Add(spur)
  b.RemoveNative(t);removed+=1;continue
 line=LineString([xy(t.GetStart()),xy(t.GetEnd())]);layer=t.GetLayer();contact=[]
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.GetNetname()==net and a.IsOnLayer(layer) and g.intersects(shape(a)):contact.append(line.project(Point(xy(a.GetPosition()))))
 for other in b.GetTracks():
  if other==t or other.GetNetname()!=net:continue
  if not isinstance(other,p.PCB_VIA) and other.GetLayer()!=layer:continue
  if not g.buffer(.000001).intersects(shape(other)):continue
  if isinstance(other,p.PCB_VIA):contact.append(line.project(Point(xy(other.GetPosition()))));continue
  ol=LineString([xy(other.GetStart()),xy(other.GetEnd())]);hit=line.intersection(ol)
  if not hit.is_empty:contact.extend(line.project(Point(q)) for q in coords(hit))
  else:contact.append(line.project(nearest_points(line,ol)[0]))
 if not contact or max(contact)-min(contact)<1e-6:b.RemoveNative(t);removed+=1
 else:
  lo,hi=min(contact),max(contact)
  if lo>1e-6 or hi<line.length-1e-6:t.SetStart(pt(line.interpolate(lo).coords[0]));t.SetEnd(pt(line.interpolate(hi).coords[0]));trimmed+=1
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
out=O/'trim-check.json';subprocess.run(['kicad-cli','pcb','drc','--schematic-parity','--format','json','-o',str(out),str(path)],check=True,stdout=subprocess.DEVNULL);after=json.loads(out.read_text())
if any(v>count(before)[k] for k,v in count(after).items()) or sum(v['severity']=='error' for v in after['violations'])>sum(v['severity']=='error' for v in before['violations']):path.write_bytes(original);print('Connectivity guard restored board')
else:(O/'current.json').write_text(json.dumps(after));print('Removed',removed,'trimmed',trimmed)
