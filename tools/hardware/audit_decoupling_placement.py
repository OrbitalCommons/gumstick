#!/usr/bin/env python3
"""Read-only supply-pin/capacitor placement measurements, not an SI/PI signoff."""
import argparse,hashlib,json,math
from pathlib import Path
import pcbnew as pcb
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'boards/esp32-fpga-module'
ASSIGNMENTS={
 'U1':{'1':'C37','3':'C35','4':'C35','20':'C38','27':'C40','30':'C41','45':'C39','51':'C42','54':'C42'},
 'U2':{'1':'C52','5':'C50','22':'C48','24':'C48','29':'C44','30':'C49','33':'C46'},
}
def xy(v):return [v.x/1e6-100,v.y/1e6-100]
def measure(board,baseline=None):
 b=pcb.LoadBoard(str(board));fs={f.GetReference():f for f in b.GetFootprints()}
 old=pcb.LoadBoard(str(baseline)) if baseline else None
 oldfs={f.GetReference():f for f in old.GetFootprints()} if old else {}
 names=json.loads((D/'docs/module-connectivity.json').read_text())
 vias=[v for v in b.GetTracks() if isinstance(v,pcb.PCB_VIA) and v.GetNetname()=='GND']
 rows=[]
 for ic,pins in ASSIGNMENTS.items():
  for pin,ref in pins.items():
   target=next(a for a in fs[ic].Pads() if a.GetNumber()==pin)
   power=next(a for a in fs[ref].Pads() if a.GetNetname()!='GND')
   ground=next(a for a in fs[ref].Pads() if a.GetNetname()=='GND')
   assert target.GetNetname()==power.GetNetname(),(ic,pin,ref)
   q=xy(target.GetPosition());c=xy(power.GetPosition());g=xy(ground.GetPosition())
   nearest=min(vias,key=lambda v:math.dist(g,xy(v.GetPosition())))
   row={'ic':ic,'pin':pin,'pin_name':names[ic]['pins'][pin]['name'],'net':target.GetNetname(),'capacitor':ref,'pin_xy_mm':q,'capacitor_supply_pad_xy_mm':c,'supply_pad_distance_mm':round(math.dist(q,c),3),'nearest_ground_via_xy_mm':xy(nearest.GetPosition()),'nearest_ground_via_distance_mm':round(math.dist(g,xy(nearest.GetPosition())),3)}
   if old:
    oq=xy(next(a for a in oldfs[ic].Pads() if a.GetNumber()==pin).GetPosition())
    choices=[(math.dist(oq,xy(a.GetPosition())),f.GetReference()) for f in old.GetFootprints() if f.GetReference().startswith('C') and f.GetValue().lower().replace(' ','') in ['0.1uf','100nf'] for a in f.Pads() if a.GetNetname()==target.GetNetname()]
    distance,cap=min(choices);row['before_nearest_100nf']={'capacitor':cap,'supply_pad_distance_mm':round(distance,3)}
   rows.append(row)
 return {'board_sha256':hashlib.sha256(Path(board).read_bytes()).hexdigest(),'measurements':'Straight-line pad-center distances, not routed lengths or electrical loop inductance. Ground-via proximity does not prove an unobstructed plane return.','assignments':rows,'shared_capacitors':{'C35':['U1.3','U1.4'],'C42':['U1.51','U1.54'],'C48':['U2.22','U2.24']},'scope':'Existing capacitors repositioned; shared-capacitor topology retained. This does not establish full manufacturer-checklist compliance.'}
def write(result,out):
 out.mkdir(parents=True,exist_ok=True);(out/'decoupling-placement.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['# Decoupling placement review','',result['measurements'],'',result['scope'],'','| Pin | Supply | Capacitor | Before nearest 100 nF | After | GND via |','|---|---|---|---:|---:|---:|']
 for r in result['assignments']:
  before=r.get('before_nearest_100nf',{}).get('supply_pad_distance_mm')
  lines.append(f"| {r['ic']}.{r['pin']} | {r['pin_name']} | {r['capacitor']} | {str(before)+' mm' if before is not None else '—'} | {r['supply_pad_distance_mm']} mm | {r['nearest_ground_via_distance_mm']} mm |")
 lines+=['','The baseline column compares the nearest existing 100 nF capacitor on the same net, not necessarily the same reference. Capacitors on a shared supply can serve multiple pins; this is not proof of effective decoupling.','', 'Reference: [Lattice iCE40 Hardware Checklist](../../../libraries/datasheets/ice40-hardware-checklist.pdf), sections 2 and 7.','',f"Board SHA-256: `{result['board_sha256']}`",'']
 (out/'decoupling-placement.md').write_text('\n'.join(lines))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--board',type=Path,default=D/'module.kicad_pcb');parser.add_argument('--baseline',type=Path);parser.add_argument('--out',type=Path,default=D/'docs');args=parser.parse_args();write(measure(args.board,args.baseline),args.out)
