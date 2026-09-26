#!/usr/bin/env python3
"""Assign unfinished two-terminal GPIO nets to nearby connector copper."""
from pathlib import Path
import pcbnew as p,json,csv,sys,re
from shapely.geometry import Point,LineString,box
from shapely.strtree import STRtree
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';b=p.LoadBoard(str(D/'module.kicad_pcb'));layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]
parts=json.loads((D/'docs/module-connectivity.json').read_text());report=json.loads((R/'tmp/module-layout/current.json').read_text());opens={re.search(r'\[([^]]+)\]',v['items'][0]['description'])[1] for v in report['unconnected_items']}
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
data={}
for f in b.GetFootprints():
 for a in f.Pads():
  net=a.GetNetname()
  if net not in opens or not (re.fullmatch(r'/ESP_GPIO\d+',net) or net.startswith('/FPGA_IO')):continue
  x,y=xy(a.GetPosition());sx,sy=p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)
  if round(a.GetOrientationDegrees())%180==90:sx,sy=sy,sx
  data.setdefault(net,[]).append((a,box(x-sx/2,y-sy/2,x+sx/2,y+sy/2),{l for l in layers if a.IsOnLayer(l)},f.GetReference()))
for t in b.GetTracks():
 if t.GetNetname() not in data:continue
 if isinstance(t,p.PCB_VIA):g=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2);ls=set(layers)
 else:g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2);ls={t.GetLayer()}
 data[t.GetNetname()].append((t,g,ls,None))
entries=[]
for net,items in data.items():
 pads=[(i,t,ref) for i,(t,g,ls,ref) in enumerate(items) if ref]
 if len(pads)!=2:continue
 source=next((i for i,t,ref in pads if ref in ['U1','U2']),None);target=next((i for i,t,ref in pads if ref in ['J1','J2']),None)
 if source is None or target is None:continue
 tree=STRtree([g for t,g,ls,ref in items])
 def component(start):
  seen={start};todo=[start]
  while todo:
   i=todo.pop()
   for k in tree.query(items[i][1],predicate='dwithin',distance=.00001):
    k=int(k)
    if k not in seen and items[i][2]&items[k][2]:seen.add(k);todo.append(k)
  return [items[i] for i in seen]
 src,tgt=component(source),component(target)
 if any(x[0]==items[target][0] for x in src):continue
 entries.append({'net':net,'source':src,'target':tgt,'pad':items[target][0],'connector':items[target][3]})
changes=[]
for connector in ['J1','J2']:
 es=[e for e in entries if e['connector']==connector];n=len(es)
 if n<2:continue
 def shapes(group):return {l:unary_union([g for t,g,ls,ref in group if l in ls]) for l in layers}
 ss=[shapes(e['source']) for e in es];ts=[shapes(e['target']) for e in es]
 cost=[[min([ss[i][l].distance(ts[j][l]) for l in layers if not ss[i][l].is_empty and not ts[j][l].is_empty] or [min(a[1].distance(b[1]) for a in es[i]['source'] for b in es[j]['target'])+.5])+(.01 if i!=j else 0) for j in range(n)] for i in range(n)]
 from ortools.graph.python import linear_sum_assignment
 solver=linear_sum_assignment.SimpleLinearSumAssignment()
 for i in range(n):
  for j in range(n):solver.add_arc_with_cost(i,j,round(cost[i][j]*1000000))
 assert solver.solve()==solver.OPTIMAL
 assignment=[solver.right_mate(i) for i in range(n)]
 value=solver.optimal_cost()/1000000;print(connector,'eligible',n,'gap cost',round(sum(cost[i][i] for i in range(n)),3),'->',round(value,3))
 for i,j in enumerate(assignment):
  if i==j:continue
  changes.append({'connector':connector,'pin':es[j]['pad'].GetNumber(),'old':es[j]['net'][1:],'new':es[i]['net'][1:]})
  for t,g,ls,ref in es[j]['target']:t.SetNet(b.FindNet(es[i]['net']))
print(json.dumps(changes,indent=2))
if '--apply' not in sys.argv or not changes:raise SystemExit()
override_path=D/'docs/pinout-overrides.json';overrides=json.loads(override_path.read_text()) if override_path.exists() else {}
rows=list(csv.DictReader((D/'docs/carrier-pinout.csv').open()));notes={r['Signal']:r['Direction / constraint'] for r in rows}
for c in changes:
 ref,pin,net=c['connector'],c['pin'],c['new'];parts[ref]['pins'][pin]['net']=net;overrides.setdefault(ref,{})[pin]=net
 for row in rows:
  if row['Connector']==ref and row['Pin']==pin:row['Signal']=net;row['Direction / constraint']=notes[net]
(D/'docs/module-connectivity.json').write_text(json.dumps(parts,indent=2)+'\n');override_path.write_text(json.dumps(overrides,indent=2)+'\n')
with (D/'docs/carrier-pinout.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
with (D/'docs/layout-notes.md').open('a') as f:
 f.write('\n### Connector reassignment for pad-free via fanout\n\n')
 for c in changes:f.write(f"- {c['connector']} pin {c['pin']}: {c['old']} → {c['new']}.\n")
 f.write('\nThese change carrier contact assignments, not chip pin functions or GPIO numbers.\n')
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
