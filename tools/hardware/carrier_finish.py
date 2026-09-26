#!/usr/bin/env python3
from pathlib import Path
exec((Path(__file__).with_name('carrier_route_local.py')).read_text().split('for t in list(b.GetTracks())')[0])
for ref in ['J1','J2']:
 x,y=xy(fp[ref].GetPosition())
 for a in fp[ref].Pads():
  if a.GetNetname()=='GND':
   a.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL);aa=xy(a.GetPosition());route('GND',[aa,(aa[0],y)],width=.15)
 route('GND',[(x-3.8,y),(x+3.8,y)],width=.3)
 for xx in [x-3,x,x+3]:via('GND',(xx,y))
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
