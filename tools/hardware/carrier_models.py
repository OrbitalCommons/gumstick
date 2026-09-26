#!/usr/bin/env python3
"""Attach installed KiCad STEP models and the audited Hirose mating models."""
from pathlib import Path
import pcbnew as p,re,shutil
R=Path(__file__).resolve().parents[2];D=R/'boards/programming-carrier';b=p.LoadBoard(str(D/'carrier.kicad_pcb'))
for f in b.GetFootprints():
 name=str(f.GetFPID().GetLibItemName());lib=p.FootprintLoad(str(D/'Carrier.pretty'),name)
 if len(list(lib.Models()))==0:
  matches=list(Path('/usr/share/kicad/footprints').glob('*.pretty/'+name+'.kicad_mod'))
  if matches:
   src=p.FootprintLoad(str(matches[0].parent),name)
   for old in src.Models():
    path=Path(re.sub(r'\$\{KICAD\d+_3DMODEL_DIR\}','/usr/share/kicad/3dmodels',old.m_Filename)).with_suffix('.step')
    if path.exists():
     shutil.copy2(path,D/'3dmodels'/path.name);m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/'+path.name;m.m_Offset=old.m_Offset;m.m_Rotation=old.m_Rotation;m.m_Scale=old.m_Scale;lib.Add3DModel(m)
 if f.GetReference()=='J3' and (D/'3dmodels/USB_C_HRO_envelope.step').exists():
  lib.Models().clear();m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/USB_C_HRO_envelope.step';lib.Add3DModel(m)
 if f.GetReference()=='SW1' and (D/'3dmodels/CK_JS102011SAQN_envelope.step').exists():
  lib.Models().clear();m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/CK_JS102011SAQN_envelope.step';lib.Add3DModel(m)
 f.Models().clear()
 for m in lib.Models():f.Add3DModel(m)
 p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Carrier.pretty'),lib)
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
print('Missing models:',[(f.GetReference(),str(f.GetFPID().GetLibItemName())) for f in b.GetFootprints() if not list(f.Models()) and not f.GetReference().startswith('H')])
