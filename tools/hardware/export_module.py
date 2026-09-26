#!/usr/bin/env python3
"""Export checked module fabrication files and assembly CSVs from the active design."""
from pathlib import Path
import csv,json,subprocess,tempfile,shutil,zipfile,datetime
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';F=D/'fab';B=D/'module.kicad_pcb';S=D/'module.kicad_sch'
def run(*args):subprocess.run(['kicad-cli',*map(str,args)],check=True)
(F/'checks').mkdir(parents=True,exist_ok=True)
with (F/'checks/via-pad-clearance.json').open('w') as out:
 subprocess.run(['/usr/bin/python3',str(R/'tools/hardware/check_via_pad_clearance.py')],check=True,stdout=out)
run('pcb','drc','--schematic-parity','--refill-zones','--save-board','--format','json','-o',F/'checks/drc.json',B)
drc=json.loads((F/'checks/drc.json').read_text())
if drc['unconnected_items'] or drc.get('schematic_parity') or any(v['severity']=='error' for v in drc['violations']):raise SystemExit('Export blocked: PCB checks are not clean')
run('sch','erc','--format','json','-o',F/'checks/erc.json',S)
run('sch','export','netlist','--format','kicadxml','-o',F/'checks/module-netlist.xml',S)
erc=json.loads((F/'checks/erc.json').read_text())
erc_issues=erc.get('violations',[])+[v for sheet in erc.get('sheets',[]) for v in sheet.get('violations',[])]
if any(v['severity']=='error' for v in erc_issues):raise SystemExit('Export blocked: ERC errors')
subprocess.run(['/usr/bin/python3',str(R/'tools/hardware/generate_bom.py')],check=True)
rows=list(csv.DictReader((F/'bom/module-bom.csv').open()));purchased={r.strip() for row in rows for r in row['Designators'].split(',')}
(R/'tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='module-export-',dir=R/'tmp') as temp:
 stage=Path(temp);gerbers=stage/'gerbers';gerbers.mkdir()
 run('pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts','--use-drill-file-origin','--check-zones','-o',str(gerbers)+'/',B)
 run('pcb','export','drill','--drill-origin','plot','--excellon-separate-th','-o',str(gerbers)+'/',B)
 run('pcb','export','pos','--format','csv','--units','mm','--side','both','--use-drill-file-origin','--exclude-dnp','-o',stage/'native-cpl.csv',B)
 pos=list(csv.DictReader((stage/'native-cpl.csv').open()));pos=[r for r in pos if r['Ref'] in purchased]
 if {r['Ref'] for r in pos}!=purchased:raise SystemExit('Export blocked: placement references do not match the purchased BOM')
 target=F/'gerbers'
 if target.exists():
  backup=R/'tmp/module-layout'/('previous-gerbers-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(target),str(backup))
 shutil.copytree(gerbers,target)
 with zipfile.ZipFile(F/'module-gerbers.zip','w',zipfile.ZIP_DEFLATED) as z:
  for path in sorted(target.iterdir()):
   if path.suffix.lower()!='.gbrjob':z.write(path,path.name)
 (F/'jlcpcb').mkdir(exist_ok=True)
 with (F/'jlcpcb/BOM_module.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Comment','Designator','Footprint','LCSC Part #'])
  for row in rows:w.writerow([row['Value'],row['Designators'],row['Footprint family'],row['LCSC Part Number']])
 with (F/'jlcpcb/CPL_module.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
  for row in pos:w.writerow([row['Ref'],f"{float(row['PosX']):.4f}mm",f"{float(row['PosY']):.4f}mm",'Top' if row['Side'].lower() in ['top','front'] else 'Bottom',row['Rot']])
 shutil.copy(stage/'native-cpl.csv',F/'bom/module-native-cpl.csv')
run('sch','export','pdf','-o',F/'module-schematic.pdf',S)
print('Exported Gerbers, BOM and',len(purchased),'placements. RF and assembly validation remain separate release requirements.')
