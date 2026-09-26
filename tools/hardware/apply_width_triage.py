#!/usr/bin/env python3
"""Apply only clear whole-run widening candidates, transactionally guarded by DRC."""
from pathlib import Path
import json,subprocess,hashlib
import pcbnew as p
from audit_trace_widths import audit,write_reports
R=Path(__file__).resolve().parents[2];path=R/'boards/esp32-fpga-module/module.kicad_pcb';out=R/'tmp/width-fixes';history=[]
for iteration in range(12):
 report=audit(path);changes={}
 for row in report['transitions']:
  if not row['widening_blockers'] and row['net'] in {'VIN_5V','+3.3V','+1.2V','+1.8V','FPGA_VCCIO0','ESP_VDD3P3','+1.2V_PLL','GND'}:
   for ident in row['narrow_run_tracks']:changes[ident]=max(changes.get(ident,0),row['wide_mm'])
 if not changes:break
 before=path.read_bytes();b=p.LoadBoard(str(path));records=[]
 for t in b.GetTracks():
  ident=t.m_Uuid.AsString()
  if ident in changes:
   records.append({'uuid':ident,'net':t.GetNetname(),'old_width_mm':t.GetWidth()/1e6,'new_width_mm':changes[ident]});t.SetWidth(round(changes[ident]*1e6))
 p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
 subprocess.run(['kicad-cli','pcb','drc','--schematic-parity','--format','json','-o',str(out/'direct-check.json'),str(path)],check=True,stdout=subprocess.DEVNULL)
 after=json.loads((out/'direct-check.json').read_text())
 if after['violations'] or after['unconnected_items'] or after.get('schematic_parity'):
  path.write_bytes(before);print('REVERTED widening batch: DRC needs manual review',flush=True);break
 history.extend(records);print('PASS',iteration,len(records),'segments',flush=True)
else:raise RuntimeError('Widening did not converge')
(out/'direct-widening.json').write_text(json.dumps(history,indent=2)+'\n')
final=audit(path);write_reports(final,R/'boards/esp32-fpga-module/docs/trace-width-audit');print('FINAL',final['summary'],flush=True)
