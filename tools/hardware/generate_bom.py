#!/usr/bin/env python3
"""Generate a review BOM, preserving original supplier IDs as unverified candidates."""
from pathlib import Path
import csv,json,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';out=D/'fab/bom';out.mkdir(parents=True,exist_ok=True)
parts=json.loads((D/'docs/module-connectivity.json').read_text())
original={c.get('ref'):{f.get('name'):f.text or '' for f in c.findall('./fields/field')} for c in E.parse(R/'docs/hardware/original-netlist.xml').getroot().find('components')}
# Enumerate the actual schematic, so stale metadata cannot silently add components.
net=E.parse(D/'fab/checks/module-netlist.xml').getroot();refs={c.get('ref') for c in net.find('components') if not c.get('ref').startswith('#')}
assert refs==set(parts),(refs-set(parts),set(parts)-refs)
groups={};excluded=[]
for ref,c in parts.items():
 if c.get('dnp'):
  excluded.append((ref,c['value'],'DNP tuning position; no purchased component'));continue
 if c.get('pcb_feature') or ref=='SJ1' or ref.startswith('TP'):
  excluded.append((ref,c['value'],'PCB copper feature; no purchased component'));continue
 src=original.get(c.get('source_ref'),{})
 candidate=c.get('lcsc') or src.get('LCSC') or src.get('LCSC_PART') or ''
 mpn=c.get('mpn') or src.get('MPN','')
 if ref in ['U1','U2','U3','U4','U5','D1','J1','J2']:mpn=c.get('mpn') or c['value']
 if ref=='Y1':mpn=c.get('mpn','')
 if ref=='L4':mpn='XFL3012-222MEC'
 notes=[c.get('sourcing_status','Review required: supplier availability and footprint compatibility not verified')]
 if not candidate:notes.append('LCSC part not selected')
 if ref.startswith('C') and c['value'].startswith('10u') and c.get('source_ref') and not c.get('sourcing_url'):notes.append('Footprint changed to 0603; original supplier ID must be requalified')
 fp=c['footprint'];lib,base=fp.split(':',1)
 if base.startswith(ref+'_'):base=base[len(ref)+1:]
 # Exact purchased identities group independently of presentation and notes.
 # Unresolved parts retain their value in the key to avoid accidental merging.
 key=(lib+':'+base,mpn,candidate,'' if mpn and candidate else c['value'])
 groups.setdefault(key,[]).append((ref,c['value'],'; '.join(notes)))
with (out/'module-bom.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['Designators','Quantity','Value','Footprint family','Manufacturer Part Number','LCSC Part Number','Notes'])
 for (fp,mpn,lcsc,_),items in sorted(groups.items(),key=lambda t:t[1][0][0]):
  rs=[item[0] for item in items]
  values=list(dict.fromkeys(item[1] for item in items))
  # Keep the most informative rating when only a rating suffix differs.
  value=max(values,key=len) if len({v.split(' / ')[0] for v in values})==1 else ' | '.join(values)
  notes='; '.join(dict.fromkeys(item[2] for item in items))
  w.writerow([', '.join(rs),len(rs),value,fp,mpn,lcsc,notes])
with (out/'pcb-features.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['Reference','Description','Notes']);w.writerows(excluded);w.writerow(['H1','M3 clearance hole','Board hole only; screw/spacer selected with motherboard'])
print(f'{sum(map(len,groups.values()))} purchased placements in {len(groups)} BOM rows')
