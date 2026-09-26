#!/usr/bin/env python3
from pathlib import Path
import pcbnew as p,json
R=Path(__file__).resolve().parents[2];D=R/'boards/programming-carrier';b=p.LoadBoard(str(D/'carrier.kicad_pcb'));v=lambda x,y:p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for f in b.GetFootprints():
 r=f.GetReference();x,y=[p.ToMM(z) for z in [f.GetPosition().x,f.GetPosition().y]]
 if r.startswith(('H','SW')):f.Reference().SetVisible(False)
 elif r in ['J1','J2']:f.Reference().SetPosition(v(112,y))
 elif r=='J3':f.Reference().SetPosition(v(107,23))
 elif r=='U2':f.Reference().SetPosition(v(104.5,34.5))
 elif r.startswith('U') and int(r[1:])>=3:f.Reference().SetPosition(v(x,y+8))
 for g in f.GraphicalItems():
  if isinstance(g,p.PCB_TEXT) and g.GetText()=='${REFERENCE}':g.SetVisible(False)
for t in b.GetDrawings():
 if isinstance(t,p.PCB_TEXT):
  if t.GetText()=='BOOT       RUN':t.SetPosition(v(65,41.5))
  if t.GetText()=='GPIO46 INPUT':t.SetPosition(v(124,43.5))
 if isinstance(t,p.PCB_SHAPE) and t.GetLayer()==p.F_SilkS and abs(p.ToMM(t.GetStart().y)-30.25)<.01 and abs(p.ToMM(t.GetEnd().y)-30.25)<.01:t.SetLayer(p.F_Fab)
# Update footprint library copies from the final instances; do not leave divergent settings.
done=set()
for f in b.GetFootprints():
 name=str(f.GetFPID().GetLibItemName())
 if name in done:continue
 done.add(name);dup=p.Cast_to_FOOTPRINT(f.Duplicate(False));dup.SetPosition(v(0,0));dup.SetOrientationDegrees(0)
 for a in dup.Pads():a.SetNetCode(0)
 p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Carrier.pretty'),dup)
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
