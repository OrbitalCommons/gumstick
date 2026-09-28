#!/usr/bin/env python3
"""Verify MAX-M10S reference topology and reset mapping to the frozen module."""
import json, hashlib
from pathlib import Path
import pcbnew as p
D=Path(__file__).resolve().parents[2]/'boards/gps-time-calibrator'
b=p.LoadBoard(str(D/'calibrator.kicad_pcb'))
m=p.LoadBoard(str(D.parent/'esp32-fpga-module/module.kicad_pcb'))
def net(board,ref,n):
 return next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber()==str(n)).GetNetname().lstrip('/')
parts=json.loads((D/'docs/circuit.json').read_text())
assert not any(b.FindFootprintByReference(r) for r in ['U8','U16','C12','C79'])
assert net(b,'U6',14)==net(b,'R5',1)=='ANT_PWR'
assert net(b,'R5',2)==net(b,'C10',1)==net(b,'L1',2)=='ANT_BIAS'
assert net(b,'L1',1)==net(b,'U6',11)==net(b,'J5',1)=='GNSS_RF'
assert net(b,'U6',4)==net(b,'R6',1)==net(b,'R7',1)==net(b,'R179',1)=='GPS_PPS'
assert net(b,'R179',2)==net(b,'D74',2)=='PPS_LED_A' and net(b,'D74',1)=='GND'
assert parts['R179']['value']=='1k'
assert all(parts[r]['value']=='33R' for r in ['R6','R7','R180'])
assert net(b,'J1',21)==net(b,'R180',1)==net(m,'J1',21)==net(m,'U1',44)=='ESP_GPIO40'
assert net(b,'R180',2)==net(b,'U6',9)=='GPS_RESET_N'
for pin,name in [('15','VIO_SEL'),('16','SDA'),('17','SCL'),('18','SAFEBOOT_N')]:
 assert parts['U6']['names'][pin]==name and parts['U6']['pins'][pin] is None
report={'pcb_sha256':hashlib.sha256((D/'calibrator.kicad_pcb').read_bytes()).hexdigest(),
 'checks':'VCC_RF bias tee, direct 1k PPS LED, separate 33R timing fanouts, reset end-to-end module mapping, corrected unused pin names',
 'reset':'ESP32 U1.44 GPIO40 -> module/carrier J1.21 -> R180 33R -> MAX-M10S U6.9',
 'result':'pass'}
(D/'docs/gps-reference-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
