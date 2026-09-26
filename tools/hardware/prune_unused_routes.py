#!/usr/bin/env python3
"""Remove dangling routing stubs only on nets with no reported opens."""
from pathlib import Path
import pcbnew as p,json,re,math,sys,subprocess
from collections import Counter
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';O=R/'tmp/module-layout'
original=(D/'module.kicad_pcb').read_bytes()
b=p.LoadBoard(str(D/'module.kicad_pcb'));j=json.loads((O/'current.json').read_text())
opens=set()
for issue in j['unconnected_items']:
 for a in issue['items']:
  m=re.search(r'\[([^]]+)\]',a['description'])
  if m:opens.add(m[1])
uids={a['uuid'] for v in j['violations'] if v['type'] in ['via_dangling','track_dangling'] for a in v['items']}
n=0
for t in list(b.GetTracks()):
 if t.m_Uuid.AsString() not in uids or t.GetNetname() in opens:continue
 if '--tracks-only' in sys.argv and isinstance(t,p.PCB_VIA):continue
 if isinstance(t,p.PCB_VIA):
  # Preserve same-layer junctions that depended on the via's copper annulus.
  center=t.GetPosition();radius=t.GetWidth(p.F_Cu)/2
  for other in b.GetTracks():
   if isinstance(other,p.PCB_VIA) or other.GetNetCode()!=t.GetNetCode():continue
   limit=radius+other.GetWidth()/2
   for get,setter in [(other.GetStart,other.SetStart),(other.GetEnd,other.SetEnd)]:
    end=get()
    if math.hypot(end.x-center.x,end.y-center.y)<=limit:setter(center)
 b.RemoveNative(t);n+=1
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
def counts(report):
 return Counter(re.search(r'\[([^]]+)\]',v['items'][0]['description'])[1] for v in report['unconnected_items'])
try:
 out=O/'prune-validation.json'
 subprocess.run(['kicad-cli','pcb','drc','--schematic-parity','--format','json','-o',str(out),str(D/'module.kicad_pcb')],check=True,stdout=subprocess.DEVNULL)
 after=json.loads(out.read_text());before_count=counts(j);after_count=counts(after)
 if any(v>before_count[k] for k,v in after_count.items()) or sum(v['severity']=='error' for v in after['violations'])>sum(v['severity']=='error' for v in j['violations']):
  (D/'module.kicad_pcb').write_bytes(original);print('Removed 0 unused routing items: connectivity guard restored board')
 else:
  (O/'current.json').write_text(json.dumps(after));print('Removed',n,'unused routing items')
except Exception:
 (D/'module.kicad_pcb').write_bytes(original)
 raise
