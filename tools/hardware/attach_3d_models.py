"""Attach project-local STEP models without changing PCB geometry or connectivity."""
from pathlib import Path
import pcbnew as p,shutil,json
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';M=D/'3dmodels';base=Path('/usr/share/kicad/3dmodels');b=p.LoadBoard(str(D/'module.kicad_pcb'));manifest=[];prior={r['reference']:r for r in json.loads((D/'docs/3d-models.json').read_text())} if (D/'docs/3d-models.json').exists() else {}
for f in b.GetFootprints():
 ref=f.GetReference();old=list(f.Models());source=None
 if ref in ['AE1','H1','SJ1'] or ref.startswith('TP'):continue
 if ref in ['J1','J2']:name='DF40C_2_0_40DS.step' if ref=='J1' else 'DF40C_40DP.step';kind='manufacturer STEP, normalized axes/origin'
 elif ref=='D1':name='FC-B1010RGBT-HG_approx.step';kind='dimension-based approximation'
 elif ref=='L4':name='Coilcraft_XFL3012.step';kind='manufacturer STEP; original geometry and face colors'
 else:
  if old and old[0].m_Filename.startswith('${KIPRJMOD}'):source=prior[ref]['kicad_source']
  elif old:source=old[0].m_Filename.split('}/')[-1];source=str(Path(source).with_suffix('.step'))
  elif ref.startswith('C'):source='Capacitor_SMD.3dshapes/C_0402_1005Metric.step'
  elif ref.startswith('R'):source='Resistor_SMD.3dshapes/R_0402_1005Metric.step'
  elif ref=='L3':source='Inductor_SMD.3dshapes/L_0402_1005Metric.step'
  else:raise RuntimeError(ref)
  assert (base/source).is_file(),source
  name=Path(source).name;shutil.copy2(base/source,M/name);kind='KiCad package model'
 filename='${KIPRJMOD}/3dmodels/'+name
 f.Models().clear();model=p.FP_3DMODEL();model.m_Filename=filename;
 if ref=='L4':model.m_Rotation=p.VECTOR3D(-90,0,0);model.m_Offset=p.VECTOR3D(0,0,.05)
 f.Add3DModel(model)
 lib=p.FootprintLoad(str(D/'Module.pretty'),str(f.GetFPID().GetLibItemName()));assert lib is not None
 lib.Models().clear();model=p.FP_3DMODEL();model.m_Filename=filename;
 if ref=='L4':model.m_Rotation=p.VECTOR3D(-90,0,0);model.m_Offset=p.VECTOR3D(0,0,.05)
 lib.Add3DModel(model);p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Module.pretty'),lib)
 manifest.append({'reference':ref,'file':name,'kind':kind,'kicad_source':source})
p.SaveBoard(str(D/'module.kicad_pcb'),b)
(D/'docs/3d-models.json').write_text(json.dumps(sorted(manifest,key=lambda x:x['reference']),indent=2)+'\n')
shutil.copy2('/usr/share/doc/kicad-packages3d/LICENSE.md',M/'KiCad-LICENSE.md')
print('Attached',len(manifest),'component models')
