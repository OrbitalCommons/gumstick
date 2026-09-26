#!/usr/bin/env python3
"""Route repeated LED cells by construction and prepare wide power / ground feeds."""
from pathlib import Path
import pcbnew as p,json,math
R=Path(__file__).resolve().parents[2];D=R/'boards/programming-carrier';b=p.LoadBoard(str(D/'carrier.kicad_pcb'));fp={f.GetReference():f for f in b.GetFootprints()};ch=json.loads((D/'docs/led-map.json').read_text());mm=p.FromMM;v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
def xy(pos):return p.ToMM(pos.x),p.ToMM(pos.y)
def pad(ref,num):return next(a for a in fp[ref].Pads() if a.GetNumber()==str(num))
def pos(ref,num):return xy(pad(ref,num).GetPosition())
def route(n,pts,layer=p.F_Cu,width=.2):
 pts=[tuple(round(z,6) for z in a) for a in pts];clean=[]
 for a in pts:
  if not clean or a!=clean[-1]:clean.append(a)
 # Miter right-angle corners without altering endpoints.
 pts=clean;out=[pts[0]]
 for i in range(1,len(pts)-1):
  a,c,z=pts[i-1:i+2];u=(c[0]-a[0],c[1]-a[1]);w=(z[0]-c[0],z[1]-c[1]);lu=math.hypot(*u);lw=math.hypot(*w)
  if lu and lw and abs(u[0]*w[0]+u[1]*w[1])<1e-6:
   d=min(.3,lu/3,lw/3);out.extend([(c[0]-d*u[0]/lu,c[1]-d*u[1]/lu),(c[0]+d*w[0]/lw,c[1]+d*w[1]/lw)])
  else:out.append(c)
 out.append(pts[-1])
 for a,z in zip(out,out[1:]):
  if a==z:continue
  t=p.PCB_TRACK(b);t.SetNet(b.FindNet(n));t.SetWidth(mm(width));t.SetLayer(layer);t.SetStart(v(*a));t.SetEnd(v(*z));b.Add(t)
vias=set()
def via(n,a):
 key=(n,round(a[0],5),round(a[1],5))
 if key in vias:return
 vias.add(key)
 t=p.PCB_VIA(b);t.SetPosition(v(*a));t.SetWidth(mm(.5));t.SetDrill(mm(.25));t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetViaType(p.VIATYPE_THROUGH);t.SetNet(b.FindNet(n));b.Add(t)
def stub(ref,num,dx,dy,width=.2):
 a=pos(ref,num);n=pad(ref,num).GetNetname();z=(a[0]+dx,a[1]+dy);route(n,[a,z],width=width);via(n,z);return z
for t in list(b.GetTracks()):b.RemoveNative(t)
for z in list(b.Zones()):b.RemoveNative(z)
# Prepare all regular groups symmetrically. No via-in-pad.
for bi in range(9):
 ref='U'+str(3+bi);x,y=xy(fp[ref].GetPosition());cap='C'+str(10+bi);fp[cap].SetPosition(v(x,y-5.5));fp[cap].Reference().SetVisible(False)
 route('+3V3_TEST',[pos(ref,20),(x+1,y-2.925),(x-.825,y-4.75),pos(cap,1)],width=.25)
 stub(cap,1,0,-1.3,.25);stub(cap,2,0,-1.3,.25)
 # OE2 goes inward between leads, then leaves beneath the body to an exposed ground via.
 route('GND',[pos(ref,19),(x,y-2.275),(x,y+5.5)],width=.2);via('GND',(x,y+5.5))
 route('GND',[pos(ref,1),(x-2.5,y-2.925),(x-2.5,y-4.5)]);via('GND',(x-2.5,y-4.5))
 route('GND',[pos(ref,10),(x-2.5,y+2.925),(x-2.5,y+4.5)]);via('GND',(x-2.5,y+4.5))
 cs=[c for c in ch if c['buffer']==ref]
 for c in cs:
  k=c['input']-2;rr=c['resistor'];rp=c['bias'];dd=c['led'];yy=p.ToMM(fp[rp].GetPosition().y);fp[rp].SetOrientationDegrees(180)
  a=pos(ref,c['input']);z=pos(rp,1);xx=x-4.0-(k if k<4 else 7-k)*.55
  route(c['signal'],[a,(xx,a[1]),(xx,z[1]),z]);stub(rp,1,0,1.25)
  stub(rp,2,-1.4,0)
  route(pad(rr,2).GetNetname(),[pos(rr,2),pos(dd,2)])
  if not c['active_low']:
   a=pos(ref,c['output']);z=pos(rr,1);xx=x+4.0+(k if k<4 else 7-k)*.55
   route(pad(ref,c['output']).GetNetname(),[a,(xx,a[1]),(xx,z[1]),z]);stub(dd,1,1.3,0)
  else:
   stub(rr,1,0,-1.25);a=stub(ref,c['output'],1.3,0);z=stub(dd,1,1.3,0);xx=a[0]+2+k*.6;route(pad(ref,c['output']).GetNetname(),[a,(xx,a[1]),(xx,z[1]),z],p.B_Cu)
 for k in range(len(cs),8):
  a=pos(ref,k+2);route('GND',[a,(x-4.3625,a[1]),(x-4.3625,y+2.925)]);via('GND',(x-4.3625,y+2.925))
# Power planes: In1 solid GND; In2 signals with GND fill. 3.3V distribution runs on B.Cu.
for layer in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet('GND'));z.SetLocalClearance(mm(.2));z.SetThermalReliefGap(mm(.2));z.SetThermalReliefSpokeWidth(mm(.25));z.SetPadConnection(p.ZONE_CONNECTION_THERMAL);z.SetMinThickness(mm(.15));z.Outline().NewOutline()
 for a in [(20.5,20.5),(179.5,20.5),(179.5,164.5),(20.5,164.5)]:z.Outline().Append(int(mm(a[0])),int(mm(a[1])))
 b.Add(z)
# Ground vias near power block and module connector grounds are added explicitly later.
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
print('Repeated indicator cells routed; ground planes added')
