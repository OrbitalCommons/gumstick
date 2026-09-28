#!/usr/bin/env python3
"""Check the carrier display remap against the frozen module and buffer pin pairs."""
import json, math, hashlib
from pathlib import Path
import pcbnew as p
D=Path(__file__).resolve().parents[2]/'boards/gps-time-calibrator'
b=p.LoadBoard(str(D/'calibrator.kicad_pcb'))
m=p.LoadBoard(str(D.parent/'esp32-fpga-module/module.kicad_pcb'))
def pad(board,ref,num):
 return next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==str(num))
def norm(net):return net.lstrip('/')
rows=json.loads((D/'docs/display-map.json').read_text());parts=json.loads((D/'docs/circuit.json').read_text());results=[]
assert len(rows)==16 and len({r['signal'] for r in rows})==16
for r in sorted(rows,key=lambda r:r['bit'],reverse=True):
 sig=r['signal'];contact=r['module_contact'];ref=r['buffer'];a=r['buffer_input_pin'];y=r['buffer_output_pin']
 assert int(a)+int(y)==20
 assert pad(b,ref,a).GetNetname()==pad(b,'J2',contact).GetNetname()==sig
 assert norm(pad(m,'J2',contact).GetNetname())==sig
 fpga=[q.GetNumber() for q in m.FindFootprintByReference('U2').Pads() if norm(q.GetNetname())==sig];assert len(fpga)==1
 assert pad(b,ref,y).GetNetname()==f'DRIVE{r["bit"]}'
 assert b.FindFootprintByReference(ref).GetOrientationDegrees()%360==270
 tracks=[t for t in b.GetTracks() if t.GetNetname()==sig]
 vias=[t for t in tracks if isinstance(t,p.PCB_VIA)]
 length=sum(math.dist((t.GetStart().x,t.GetStart().y),(t.GetEnd().x,t.GetEnd().y))/1e6 for t in tracks if not isinstance(t,p.PCB_VIA))
 results.append(dict(r,fpga_package_pin=fpga[0],input_copper_length_mm=round(length,3),input_vias=len(vias)))
for ref in ['U3','U4']:
 assert pad(b,ref,1).GetNetname()=='FPGA_IOT_44B'
 assert pad(b,ref,19).GetNetname()=='GND'
assert pad(b,'R140',1).GetNetname()=='+3V3_LOGIC' and pad(b,'R140',2).GetNetname()=='FPGA_IOT_44B'
assert parts['R140']['value']=='10k'
assert not any(f.GetReference() in {f'R{i}' for i in range(141,156)} for f in b.GetFootprints())
assert pad(b,'Y1',3).GetNetname()==pad(b,'R173',1).GetNetname()=='OCXO_CLK'
assert pad(b,'R173',2).GetNetname()==pad(b,'J2',32).GetNetname()=='FPGA_IOB_3B_G6'
assert norm(pad(m,'J2',32).GetNetname())==norm(pad(m,'U2',44).GetNetname())=='FPGA_IOB_3B_G6'
assert norm(pad(m,'J2',22).GetNetname())==pad(b,'J2',22).GetNetname()=='FPGA_IOT_46B_G0'
out={'pcb_sha256':hashlib.sha256((D/'calibrator.kicad_pcb').read_bytes()).hexdigest(),'ocxo':'Y1.3 -> R173 33R -> carrier J2.32 -> module U2.44 IOB_3B/G6 -> GBUF6','enable':'J2.33 FPGA_IOT_44B, active low, R140 10k pull-up; OE2 grounded','rows':results}
(D/'docs/display-bus-audit.json').write_text(json.dumps(out,indent=2)+'\n')
positions={f.GetReference():{'x_mm':p.ToMM(f.GetPosition().x),'y_mm':p.ToMM(f.GetPosition().y),'rotation_deg':f.GetOrientationDegrees(),'footprint':f.GetFPID().GetUniStringLibId()} for f in b.GetFootprints()}
(D/'docs/final-placements.json').write_text(json.dumps(positions,indent=2)+'\n')
print('Verified 16 buffer channels, carrier/module pin mapping, OE and OCXO G6; saved current placements.')
