#!/usr/bin/env python3
"""Check F.Cu routes against QFN bodies, allowing pad landings and exposed-pad ground."""
import json
from pathlib import Path
import pcbnew as p
from shapely.geometry import box, LineString
from shapely.ops import unary_union
from routing_constraints import pad_geometry
root=Path(__file__).resolve().parents[2]
b=p.LoadBoard(str(root/'boards/esp32-fpga-module/module.kicad_pcb'))
issues=[]
xy=lambda q:(p.ToMM(q.x)-100,p.ToMM(q.y)-100)
for f in b.GetFootprints():
 if f.GetReference() not in ['U1','U2']:continue
 x,y=xy(f.GetPosition());body=box(x-3.5,y-3.5,x+3.5,y+3.5)
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA) or t.GetLayer()!=p.F_Cu or t.GetNetname()=='GND':continue
  copper=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2)
  hit=copper.intersection(body)
  if hit.is_empty:continue
  lands=unary_union([pad_geometry(a).buffer(.002) for a in f.Pads() if a.GetNetname()==t.GetNetname()])
  if hit.difference(lands).area>1e-7:issues.append({'reference':f.GetReference(),'net':t.GetNetname(),'track':t.m_Uuid.AsString()})
print(json.dumps({'ok':not issues,'front_body_routes':issues,'exception':'GND exposed-pad connections'},indent=2))
raise SystemExit(bool(issues))
