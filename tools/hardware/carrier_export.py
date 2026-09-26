#!/usr/bin/env python3
"""Checked, repeatable carrier fabrication and assembly export."""
from pathlib import Path
import csv, subprocess, tempfile, zipfile, shutil, hashlib, json
R=Path(__file__).resolve().parents[2];D=R/'boards/programming-carrier';F=D/'fab';P=D/'carrier.kicad_pcb';S=D/'carrier.kicad_sch'
def run(*args): subprocess.run(list(map(str,args)),check=True)
for sub in ['checks','gerbers','jlcpcb','bom']:(F/sub).mkdir(parents=True,exist_ok=True)
run('kicad-cli','sch','erc','--format','json','--exit-code-violations','-o',F/'checks/erc.json',S)
run('kicad-cli','pcb','drc','--schematic-parity','--refill-zones','--format','json','--exit-code-violations','-o',F/'checks/drc.json',P)
run('python3',R/'tools/hardware/carrier_bom.py')
with tempfile.TemporaryDirectory() as td:
 stage=Path(td)
 run('kicad-cli','pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts','--subtract-soldermask','--use-drill-file-origin','-o',str(stage)+'/',P)
 run('kicad-cli','pcb','export','drill','--format','excellon','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','-o',str(stage)+'/',P)
 files=sorted(x for x in stage.iterdir() if x.suffix in {'.gtl','.gbl','.g1','.g2','.gts','.gbs','.gto','.gbo','.gtp','.gbp','.gm1','.drl','.gbrjob'})
 assert any(x.suffix=='.g1' for x in files) and any(x.suffix=='.g2' for x in files)
 with zipfile.ZipFile(F/'gerbers/carrier-gerbers.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in files:
   shutil.copy2(f,F/'gerbers'/f.name);z.write(f,f.name)
run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--side','both','--exclude-dnp','--use-drill-file-origin','-o',F/'bom/carrier-native-positions.csv',P)
with (F/'jlcpcb/BOM_carrier.csv').open() as f:bom=list(csv.DictReader(f))
refs={r.strip() for row in bom for r in row['Designator'].split(',')}
part_by_ref={r.strip():row['LCSC Part #'] for row in bom for r in row['Designator'].split(',')}
offsets=json.loads((D/'docs/jlcpcb-placement-offsets.json').read_text())
with (F/'bom/carrier-native-positions.csv').open() as f:positions=[r for r in csv.DictReader(f) if r['Ref'] in refs]
assert {r['Ref'] for r in positions}==refs and len(positions)==len(refs)
with (F/'jlcpcb/CPL_carrier.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for r in positions:
  adjustment=offsets.get(part_by_ref[r['Ref']],{})
  correction=adjustment.get('rotation_offset_degrees',0)
  dx=adjustment.get('cpl_offset_x_mm',0);dy=adjustment.get('cpl_offset_y_mm',0)
  if dx or dy:
   assert r['Side']=='top' and float(r['Rot'])%360==adjustment['verified_native_rotation_degrees'], 'Reverify translation for changed placement rotation'
  if correction:assert r['Side']=='top', 'Bottom-side offsets need separate verification'
  rotation=(float(r['Rot'])+correction)%360
  w.writerow([r['Ref'],f"{float(r['PosX'])+dx:.6f}",f"{float(r['PosY'])+dy:.6f}",{'top':'T','bottom':'B'}[r['Side']],f'{rotation:.6f}'])
(F/'EXPORT.json').write_text(json.dumps({'pcb_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'assembly_components':len(refs),'bom_groups':len(bom),'coordinate_convention':'mm, board drill/place origin; native KiCad Y preserved; part-specific JLCPCB rotation offsets applied from docs/jlcpcb-placement-offsets.json; T/B layers'},indent=2)+'\n')
print('Exported Gerber ZIP, BOM and CPL:',len(refs),'placements')
