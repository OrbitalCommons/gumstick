from pathlib import Path
import xml.etree.ElementTree as E
import json
R=Path(__file__).resolve().parents[2];e=E.parse(R/'source/fusion/MainBoard.sch').getroot()
parts={p.get('name'):p for p in e.findall('.//schematic/parts/part')};libs={p.get('name'):p for p in e.findall('.//schematic/libraries/library')}
original={}
for n in e.findall('.//sheets/sheet/nets/net'):
 for p in n.findall('.//pinref'):
  ref=p.get('part');part=parts[ref];lib=next(l for l in e.findall('.//schematic/libraries/library') if l.get('name')==part.get('library') and any(ds.get('name')==part.get('deviceset') for ds in l.findall('./devicesets/deviceset')))
  dev=next(d for ds in lib.findall('./devicesets/deviceset') if ds.get('name')==part.get('deviceset') for d in ds.findall('./devices/device') if d.get('name')==part.get('device'))
  for conn in dev.findall('./connects/connect'):
   if conn.get('gate')==p.get('gate') and conn.get('pin')==p.get('pin'):
    for pad in conn.get('pad','').split():original[ref,pad]=n.get('name')
r=E.parse(R/'docs/hardware/original-netlist.xml').getroot();native={}
for n in r.find('nets'):
 for p in n.findall('node'):native[p.get('ref'),p.get('pin')]=n.get('name')
# Compare connectivity equivalence, allowing generated net names to differ.
groups={}
for k,v in original.items():groups.setdefault(v,[]).append(k)
issues=[]
for name,ks in groups.items():
 found={native[k] for k in ks if k in native}
 if len(found)>1:issues.append({'eagle_net':name,'native_nets':sorted(found),'pins':{f'{r}.{p}':native.get((r,p)) for r,p in ks if (r,p) in native}})
(R/'docs/hardware/import-connectivity-audit.json').write_text(json.dumps(issues,indent=2)+'\n')
(R/'docs/hardware/eagle-pad-nets.json').write_text(json.dumps({f'{r}.{p}':n for (r,p),n in original.items()},indent=2)+'\n')
print('Split Eagle nets:',[i['eagle_net'] for i in issues])
