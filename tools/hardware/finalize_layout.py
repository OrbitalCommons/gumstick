#!/usr/bin/env python3
"""Finalize local footprint snapshots and readable markings without changing copper."""
from pathlib import Path
import pcbnew as p,json
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';b=p.LoadBoard(str(D/'module.kicad_pcb'));data=json.loads((D/'docs/module-connectivity.json').read_text())
def pt(x,y):return p.VECTOR2I(p.FromMM(100+x),p.FromMM(100+y))
refs={'U1':(7,10.7),'U2':(10,44.3),'J1':(10,11.5),'J2':(10,37.6),'SJ1':(13,33.1)}
for t in list(b.GetDrawings()):
 if isinstance(t,p.PCB_TEXT) and t.GetText() in ['ESP32 + FPGA','J1 / ESP + USB','J2 / FPGA']:b.RemoveNative(t)
for f in b.GetFootprints():
 ref=f.GetReference()
 f.Reference().SetLayer(p.B_SilkS if f.GetLayer()==p.B_Cu and ref in refs else p.F_SilkS if ref in refs else p.F_Fab)
 if ref in refs:
  f.Reference().SetHorizJustify(p.GR_TEXT_H_ALIGN_CENTER);f.Reference().SetVertJustify(p.GR_TEXT_V_ALIGN_CENTER);f.Reference().SetPosition(pt(*refs[ref]));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
 if ref=='H1':continue
 for field,key in [('MPN','mpn'),('Manufacturer','manufacturer'),('LCSC','lcsc')]:
  if data[ref].get(key):
   f.SetField(field,data[ref][key]);f.GetField(field).SetVisible(False);f.GetField(field).SetPosition(f.GetPosition())
 models={'U1':'Package_DFN_QFN.3dshapes/QFN-56-1EP_7x7mm_P0.4mm_EP4x4mm.step','U2':'Package_DFN_QFN.3dshapes/QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm.step','Y1':'Crystal.3dshapes/Crystal_SMD_2520-4Pin_2.5x2.0mm.step'}
 if ref in models and not len(f.Models()):
  model=p.FP_3DMODEL();model.m_Filename='${KICAD10_3DMODEL_DIR}/'+models[ref];f.Add3DModel(model)
 # Every edited footprint is project-local; the library snapshot matches its final geometry.
 old=data[ref]['footprint'].split(':')[-1];name=old if old.startswith(ref+'_') else ref+'_'+old
 f.SetFPID(p.LIB_ID('Module',name));data[ref]['footprint']='Module:'+name
 c=p.Cast_to_FOOTPRINT(f.Duplicate(False))
 if c.GetLayer()==p.B_Cu:c.Flip(c.GetPosition(),False)
 c.SetOrientationDegrees(0);c.SetPosition(p.VECTOR2I(0,0));c.SetReference('REF**')
 for a in c.Pads():a.SetNetCode(0)
 p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Module.pretty'),c)
p.SaveBoard(str(D/'module.kicad_pcb'),b)
(D/'docs/module-connectivity.json').write_text(json.dumps(data,indent=2)+'\n')
