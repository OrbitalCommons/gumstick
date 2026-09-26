"""Enforce accessible external QFN vias in both KiCad DRC and routing tools."""
from pathlib import Path
import pcbnew as p
from shapely.geometry import Point
from routing_constraints import qfn_regions
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';path=D/'module.kicad_pcb';b=p.LoadBoard(str(path));regions=list(qfn_regions(b))
pt=lambda x,y:p.VECTOR2I(p.FromMM(x+100),p.FromMM(y+100))
for z in list(b.Zones()):
 if z.GetIsRuleArea() and z.GetZoneName().startswith('QFN via access'):b.Remove(z)
for ref,g in regions:
 z=p.ZONE(b);z.SetIsRuleArea(True);z.SetZoneName('QFN via access '+ref)
 ls=p.LSET()
 for l in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]:ls.AddLayer(l)
 z.SetLayerSet(ls);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(True);z.SetDoNotAllowPads(False);z.SetDoNotAllowZoneFills(False);z.SetDoNotAllowFootprints(False)
 x0,y0,x1,y1=g.bounds;o=z.Outline();o.NewOutline()
 for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]:v=pt(x,y);o.Append(v.x,v.y)
 b.Add(z)
removed=0
for v in list(b.GetTracks()):
 if not isinstance(v,p.PCB_VIA):continue
 q=v.GetPosition();g=Point(p.ToMM(q.x)-100,p.ToMM(q.y)-100).buffer(p.ToMM(v.GetWidth(p.F_Cu))/2)
 if any(g.intersects(region) for _,region in regions):b.RemoveNative(v);removed+=1
p.SaveBoard(str(path),b);print('Removed',removed,'vias beneath QFN package envelopes; keepouts added')
