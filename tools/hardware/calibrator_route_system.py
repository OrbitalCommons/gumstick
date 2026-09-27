#!/usr/bin/env python3
"""Local system connections and frozen programmer USB geometry translated to this board."""
import sys
if '--rebuild-unrouted' not in sys.argv:
 raise SystemExit('Historical construction step: requires --rebuild-unrouted; will overwrite routed work. Use calibrator_export.py for deliverables.')

from pathlib import Path
# Load only helper definitions, not the local-route mutation phase.
exec((Path(__file__).with_name('calibrator_route.py')).read_text().split('for t in list(b.GetTracks())')[0])
# Reuse verified USB topology, extending only the straight pair to the module.
fp['U1'].SetOrientationDegrees(270)
source=p.LoadBoard(str(R/'boards/programming-carrier/carrier.kicad_pcb'))
def tr(a):
 x,y=xy(a);return x+55,y-10 if y<35 else y-2
for t in source.GetTracks():
 if t.GetNetname() not in ['USB_D+','USB_D-']:continue
 if isinstance(t,p.PCB_VIA):via(t.GetNetname(),tr(t.GetPosition()))
 else:route(t.GetNetname(),[tr(t.GetStart()),tr(t.GetEnd())],t.GetLayer(),p.ToMM(t.GetWidth()))
# No traces or vias beneath module screw / contact areas except necessary pad escapes.
for ref in ['J1','J2']:
 f=fp[ref];fx,fy=xy(f.GetPosition())
 for sign in [-1,1]:
  row=sorted([a for a in f.Pads() if a.GetNumber() and (p.ToMM(a.GetPosition().y)-fy)*sign>0],key=lambda a:a.GetPosition().x)
  for j,pa in enumerate(row):
   n=pa.GetNetname();px,py=xy(pa.GetPosition())
   if not n or n.startswith('unconnected-') or n in ['USB_D+','USB_D-','VIN_5V','GND']:continue
   vx=fx+(j-9.5)*.65;vy=py+sign*(3.4+(j%2)*.8)
   route(n,[(px,py),(px,py+sign*.75),(vx,py+sign*(.75+abs(vx-px))),(vx,vy)],width=.15);via(n,(vx,vy))
 for dx in [-6.8,6.8]:via('GND',(fx+dx,fy))
for k in [1,2,3,4]:
 a=pos('J1',k);route('VIN_5V',[a,(a[0],41.1)],width=.2)
route('VIN_5V',[(157.6,41.1),(158.8,41.1)],width=.5);via('VIN_5V',(157.9,41.1));via('VIN_5V',(158.8,41.1))
# Regulators: input and return to planes, output capacitor directly beside package.
for ref,ci,co in [('U2','C2','C3'),('U5','C6','C7')]:
 fp[co].SetOrientationDegrees(270)
 a=pos(ref,1);z=pos(ref,3);xx=a[0]-1.3
 route('VIN_5V',[a,(xx,a[1]),(xx,z[1]),z],width=.3);via('VIN_5V',(xx,a[1]))
 stub(ref,2,.0,0) if False else None
 # Ground exits under the package toward an exposed via above the body.
 a=pos(ref,2);cx,cy=xy(fp[ref].GetPosition());route('GND',[a,(cx,cy),(cx,cy-2.5)],width=.25);via('GND',(cx,cy-2.5))
 a=pos(ref,5);z=pos(co,1);route(pad(ref,5).GetNetname(),[a,(z[0],a[1]),z],width=.4)
 for cr in [ci,co]:
  for n in [1,2]:stub(cr,n,-1.2 if cr==ci else 1.2,0,.3)
# GNSS RF direct 45-degree launch. Nominal short 0.26mm feed; stackup must be confirmed.
route('GNSS_RF',[pos('U6',11),(192.65,99.3),pos('J5',1)],width=.26)
route('GNSS_RF',[pos('L1',1),(193.95,94.8375),pos('J5',1)],width=.26)
route('ANT_BIAS',[pos('R5',2),(193,86),(195,88),pos('C10',1)],width=.25)
route('ANT_BIAS',[pos('C10',1),(194.225,91.4375),pos('L1',2)],width=.25)
a=stub('U6',14,1.2,0);z=stub('R5',1,0,-1.2);route('GNSS_VCC_RF',[a,(a[0],z[1]+2),(a[0]-2,z[1]),z],p.B_Cu,.3)
# Ground stitching directly next to GPS ground pads and coax shields.
for n in [1,10,12]:stub('U6',n,-1.25 if n==1 else 1.0,0,.3)
for pa in fp['J5'].Pads():
 if pa.GetNumber()=='2':
  a=xy(pa.GetPosition());z=(a[0]+1.2,a[1]);route('GND',[a,z],width=.4);via('GND',z)
# GPS decoupling: low-impedance local 3.3V bus on B.Cu, with each IC supply pin escaping outward.
anchors=[]
for n in [6,7,8]:anchors.append(stub('U6',n,-1.25,0,.3))
for ref in ['C8','C9']:
 anchors.append(stub(ref,1,-1.2,0,.3));stub(ref,2,-1.2,0,.3)
anchors.append(pos('C7',1));via('+3V3_GPS',anchors[-1]) if False else None
# C7 already has an exposed output via.
anchors[-1]=(pos('C7',1)[0]+1.2,pos('C7',1)[1])
route('+3V3_GPS',anchors[:3],p.B_Cu,.4)
# Remaining ground / 5V passives connect to local planes through exposed vias.
for ref,f in fp.items():
 if ref in ['J1','J2','J5','U2','U3','U4','U5','U6'] or ref.startswith(('Q','H')):continue
 if ref.startswith('R') and (10<=int(ref[1:])<74 or 100<=int(ref[1:])<156):continue
 if ref.startswith('C') and (20<=int(ref[1:])<56 or ref in ['C2','C3','C4','C5','C6','C7','C8','C9']):continue
 for pa in f.Pads():
  if pa.GetNetname() not in ['GND','VIN_5V'] or pa.GetAttribute()==p.PAD_ATTRIB_PTH:continue
  a=xy(pa.GetPosition());cx,cy=xy(f.GetPosition());dx=1.2 if a[0]>=cx else -1.2
  # IC ground exits vertically to avoid adjacent terminals.
  if ref=='U1':stub(ref,pa.GetNumber(),0,1.2,.2)
  elif ref=='U7':stub(ref,pa.GetNumber(),-1.2,0,.2)
  else:
   z=(a[0]+dx,a[1]);route(pa.GetNetname(),[a,z],width=.3);via(pa.GetNetname(),z)
for ref in ['H1','H2','H3','H4','H5']:
 x,y=xy(fp[ref].GetPosition());z=p.ZONE(b);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowPads(False);ls=p.LSET();[ls.AddLayer(l) for l in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]];z.SetLayerSet(ls);z.Outline().NewOutline()
 for i in range(16):z.Outline().Append(int(mm(x+3.5*math.cos(i*math.pi/8))),int(mm(y+3.5*math.sin(i*math.pi/8))))
 b.Add(z)
p.SaveBoard(str(D/'calibrator.kicad_pcb'),b)
print('USB, module escapes, regulator and RF local routes added')
