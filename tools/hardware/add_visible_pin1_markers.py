#!/usr/bin/env python3
"""Place external pin-one silk dots for orientation-sensitive component footprints."""
import pcbnew as p,math,json
from pathlib import Path
from shapely.geometry import box,Point
D=Path('boards/esp32-fpga-module');f=D/'module.kicad_pcb';b=p.LoadBoard(str(f))
def bb(item):
 q=item.GetBoundingBox();return box(p.ToMM(q.GetLeft()),p.ToMM(q.GetTop()),p.ToMM(q.GetRight()),p.ToMM(q.GetBottom()))
# Remove markers from the previous run; leave footprint-native silk intact.
record=D/'docs/pin1-markers.json'
if record.exists():
 old=json.loads(record.read_text())
 for drawing in list(b.GetDrawings()):
  if not isinstance(drawing,p.PCB_SHAPE) or drawing.GetShape()!=p.SHAPE_T_CIRCLE:continue
  q=drawing.GetCenter()
  if any(abs(p.ToMM(q.x)-v['x'])<.001 and abs(p.ToMM(q.y)-v['y'])<.001 and b.GetLayerName(drawing.GetLayer())==v['layer'] for v in old.values()):b.RemoveNative(drawing)
fps=list(b.GetFootprints());positions={}
for layer,side in [(p.F_Cu,p.F_SilkS),(p.B_Cu,p.B_SilkS)]:
 fs=[fp for fp in fps if fp.GetLayer()==layer]
 obstacles=[]
 for fp in fs:
  # Entire footprint envelope keeps the dot outside its body and solder lands.
  q=fp.GetBoundingBox(False,False);obstacles.append(box(p.ToMM(q.GetLeft()),p.ToMM(q.GetTop()),p.ToMM(q.GetRight()),p.ToMM(q.GetBottom())).buffer(.30))
  if fp.Reference().IsVisible():obstacles.append(bb(fp.Reference()).buffer(.25))
 for fp in fps:
  for pad in fp.Pads():
   if pad.GetDrillSize().x:obstacles.append(bb(pad).buffer(.35))
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):obstacles.append(Point(p.ToMM(t.GetPosition().x),p.ToMM(t.GetPosition().y)).buffer(.4))
 for fp in sorted(fs,key=lambda x:(0 if x.GetReference().startswith(('U','J','D','Y')) else 1,x.GetReference())):
  if not fp.GetReference().startswith(('U','J','D','Y')):continue
  if fp.GetReference()=='U3':continue # Native visible pin-one triangle already identifies it.
  pads=list(fp.Pads())
  if len(pads)<2:continue
  target='IN/OUT' if fp.GetReference()=='Y1' else 'P$1' if fp.GetReference()=='D1' else '1'
  pin=next((a for a in pads if a.GetNumber()==target),None)
  if pin is None:continue
  x,y=p.ToMM(pin.GetPosition().x),p.ToMM(pin.GetPosition().y);candidates=[]
  others=[(p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)) for a in pads if a.GetNumber()!=target]
  for i in range(-40,41):
   for j in range(-40,41):
    xx=round(x+i*.1,4);yy=round(y+j*.1,4)
    if not 100.5<xx<119.5 or not 101.95<yy<145.95:continue
    dist=math.hypot(xx-x,yy-y)
    if any(math.hypot(xx-a,yy-z)<dist-.03 for a,z in others):continue
    candidates.append((dist,xx,yy))
  for _,xx,yy in sorted(candidates):
   q=Point(xx,yy)
   if any(o.contains(q) for o in obstacles):continue
   s=p.PCB_SHAPE(b);s.SetShape(p.SHAPE_T_CIRCLE);s.SetCenter(p.VECTOR2I(p.FromMM(xx),p.FromMM(yy)));s.SetEnd(p.VECTOR2I(p.FromMM(xx+.15),p.FromMM(yy)));s.SetWidth(150000);s.SetFilled(True);s.SetLayer(side);b.Add(s);obstacles.append(q.buffer(.6));positions[fp.GetReference()]={'pin':target,'x':xx,'y':yy,'layer':b.GetLayerName(side)};break
  else:raise RuntimeError('No visible pin-one position for '+fp.GetReference())
p.SaveBoard(str(f),b);(D/'docs/pin1-markers.json').write_text(json.dumps(positions,indent=2)+'\n');print('Added',len(positions),'external markers')
