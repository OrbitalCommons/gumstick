#!/usr/bin/env python3
"""USB full-speed pair, connector escape and wide power distribution."""
from pathlib import Path
# Reuse geometry helpers without executing the repeated-cell routing phase.
exec((Path(__file__).with_name('carrier_route_local.py')).read_text().split('for t in list(b.GetTracks())')[0])
# Straight, through-flow USB ESD, D+ to the right of D-.
fp['U2'].SetOrientationDegrees(-90)
# USB front pads: optional reversible-plug branches use separate layers; main pair stays F.Cu.
for n,main,other,x,layer in [('USB_D+','A6','B6',100.95,p.B_Cu),('USB_D-','A7','B7',99.05,p.In2_Cu)]:
 a=pos('J3',main);route(n,[a,(a[0],27.85),(x,27.85+abs(x-a[0])),(x,29.8625)],width=.2)
 av=(pos('J3',other)[0],25.4);route(n,[pos('J3',other),av],width=.15);via(n,av)
 zv=(x,28.65);via(n,zv);xx=101.7 if n.endswith('+') else 98.3;yy=24.5 if n.endswith('+') else 24;route(n,[av,(av[0],yy),(xx,yy),(xx,27.9),zv],layer,.2)
 # ESD device ties its front and rear channel pads internally. Copper parallels the pin pair underneath.
 source=pos('U2',6 if n.endswith('+') else 4);dest=pos('J1',7 if n.endswith('+') else 8)
 route(n,[source,(source[0],33),(dest[0],33+abs(dest[0]-source[0])),dest],width=.2)
# Small power supply island.
route('VIN_5V',[pos('F1',2),(88.4,34),(86.4,36),(76,36),pos('C1',1)],width=.6)
route('VIN_5V',[pos('C1',1),(77,31.775),(77.5,31.275),(77.5,30.05),pos('U1',1)],width=.4)
route('VIN_5V',[pos('U1',3),(78.0,31.95),(78.0,33),(76,33),pos('C1',1)],width=.35)
route('+3V3_TEST',[pos('U1',5),(82.5,30.05),(84,31.55),pos('C2',1)],width=.4)
stub('C2',1,1.5,0,.4);stub('C1',2,-1.3,0);stub('C2',2,1.3,0);stub('U1',2,0,0.0) if False else None
# Ground pin leaves left then down, clear of both supply pins.
route('GND',[pos('U1',2),(79.8,31),(79.8,34)],width=.2);via('GND',(79.8,34))
# Source voltage entry via; all four 5V contacts are connected individually with a 0.2mm escape.
for k in [1,2,3,4]:
 a=pos('J1',k);route('VIN_5V',[a,(a[0],43.3)],width=.2)
route('VIN_5V',[(102.6,43.3),(103.8,43.3)],width=.5);via('VIN_5V',(103,43.3));via('VIN_5V',(103.8,43.3))
via('VIN_5V',(88.4,33.5));route('VIN_5V',[(88.4,33.5),(99.6,33.5),(103.8,41.7),(103.8,43.3)],p.B_Cu,.75)
# All remaining fine-pitch signals get monotonically spread, alternating close/far escape vias.
for ref in ['J1','J2']:
 f=fp[ref];fx,fy=xy(f.GetPosition())
 for sign in [-1,1]:
  row=sorted([a for a in f.Pads() if a.GetNumber() and (p.ToMM(a.GetPosition().y)-fy)*sign>0],key=lambda a:a.GetPosition().x)
  for j,a in enumerate(row):
   n=a.GetNetname();px,py=xy(a.GetPosition())
   if n in ['USB_D+','USB_D-','VIN_5V','GND']:continue
   vx=fx+(j-9.5)*.65;vy=py+sign*(3.4+(j%2)*.8)
   route(n,[(px,py),(px,py+sign*.75),(vx,py+sign*(.75+abs(vx-px))),(vx,vy)],width=.15);via(n,(vx,vy))
 for dx in [-6.8,6.8]:via('GND',(fx+dx,fy))
# Broad 3.3V LED power buses, no switching regulator noise.
route('+3V3_TEST',[(85.5,31.775),(85.5,79.5),(153,79.5)],p.B_Cu,.6)
route('+3V3_TEST',[(85.5,79.5),(31.175,79.5)],p.B_Cu,.6)
for xx in [31.175,68.175,115.175,152.175]:
 route('+3V3_TEST',[(xx,79.5),(xx,126.2)],p.B_Cu,.5)
# Expose ordinary ground connection to planes; short power indicator chains.
for rr,dd in [('R3','D1'),('R4','D2')]:route(pad(rr,2).GetNetname(),[pos(rr,2),pos(dd,2)])
# Mechanical screw clearance, all copper layers. No routing below the metal spacer.
for ref in ['H1','H2','H3','H4','H5']:
 x,y=xy(fp[ref].GetPosition());z=p.ZONE(b);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowPads(False);ls=p.LSET();[ls.AddLayer(l) for l in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]];z.SetLayerSet(ls);z.Outline().NewOutline()
 for i in range(16):z.Outline().Append(int(mm(x+3.5*math.cos(i*math.pi/8))),int(mm(y+3.5*math.sin(i*math.pi/8))))
 b.Add(z)
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
