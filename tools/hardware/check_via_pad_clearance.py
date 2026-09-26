#!/usr/bin/env python3
"""Copper-overlap audit using circle/oval/rounded-rectangle pad geometry."""
from pathlib import Path
import pcbnew as p,json,math,sys
R=Path(__file__).resolve().parents[2];board=R/'boards/esp32-fpga-module/module.kicad_pcb'
b=p.LoadBoard(str(board));pads=[]
for f in b.GetFootprints():
 for a in f.Pads():
  if not (a.IsOnLayer(p.F_Cu) or a.IsOnLayer(p.B_Cu)):continue
  pads.append((f.GetReference(),a))
issues=[];body_issues=[];size_issues=[];count=0
from routing_constraints import VIA_DIAMETER_MM, VIA_DRILL_MM
qfns=[(f.GetReference(),p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)) for f in b.GetFootprints() if f.GetReference() in ['U1','U2']]
for v in b.GetTracks():
 if not isinstance(v,p.PCB_VIA):continue
 count+=1;r=p.ToMM(v.GetWidth(p.F_Cu))/2
 if r*2<VIA_DIAMETER_MM-1e-6 or p.ToMM(v.GetDrillValue())<VIA_DRILL_MM-1e-6:
  size_issues.append({'via':v.m_Uuid.AsString(),'net':v.GetNetname(),'diameter_mm':r*2,'drill_mm':p.ToMM(v.GetDrillValue())})
 for ref,cx,cy in qfns:
  x,y=p.ToMM(v.GetPosition().x),p.ToMM(v.GetPosition().y)
  distance=math.hypot(max(0,abs(x-cx)-3.65),max(0,abs(y-cy)-3.65))
  if distance<r-1e-6:body_issues.append({'via':v.m_Uuid.AsString(),'net':v.GetNetname(),'component':ref})
 for ref,a in pads:
  delta=v.GetPosition()-a.GetPosition();dx,dy=p.ToMM(delta.x),p.ToMM(delta.y)
  angle=math.radians(a.GetOrientationDegrees());x=dx*math.cos(angle)+dy*math.sin(angle);y=-dx*math.sin(angle)+dy*math.cos(angle)
  sx,sy=p.ToMM(a.GetSize().x)/2,p.ToMM(a.GetSize().y)/2
  if a.GetShape()==p.PAD_SHAPE_CIRCLE:
   distance=max(0,math.hypot(x,y)-sx)
  elif a.GetShape()==p.PAD_SHAPE_OVAL:
   cap=min(sx,sy)
   distance=max(0,math.hypot(max(0,abs(x)-(sx-cap)),max(0,abs(y)-(sy-cap)))-cap)
  elif a.GetShape()==p.PAD_SHAPE_ROUNDRECT:
   corner=p.ToMM(a.GetRoundRectCornerRadius())
   distance=max(0,math.hypot(max(0,abs(x)-(sx-corner)),max(0,abs(y)-(sy-corner)))-corner)
  else:
   distance=math.hypot(max(0,abs(x)-sx),max(0,abs(y)-sy))
  if distance<r-1e-6:issues.append({'via':v.m_Uuid.AsString(),'net':v.GetNetname(),'component':ref,'pad':a.GetNumber()})
result={'ok':not issues and not body_issues and not size_issues,'via_count':count,'pad_overlaps':issues,'qfn_body_overlaps':body_issues,'undersized_vias':size_issues}
print(json.dumps(result,indent=2));sys.exit(bool(issues or body_issues or size_issues))
