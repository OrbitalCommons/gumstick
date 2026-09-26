#!/usr/bin/env python3
"""Retain the original U9 RGB LED and its original FPGA drive connections as D1."""
from pathlib import Path
import json,uuid
import pcbnew as p
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module'
x=json.loads((D/'docs/module-connectivity.json').read_text())
x['D1']={'source_ref':'U9','value':'FC-B1010RGBT-HG','footprint':'Module:RGBLED','lcsc':'C158099','pins':{f'P${i}':{'name':'A' if i==1 else f'K_RGB{i-2}','type':'passive','net':'+3.3V' if i==1 else f'FPGA_RGB{i-2}'} for i in range(1,5)},'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'gps-time-module/D1'))}
(D/'docs/module-connectivity.json').write_text(json.dumps(x,indent=2)+'\n')
b=p.LoadBoard(str(D/'module.kicad_pcb'))
if not any(f.GetReference()=='D1' for f in b.GetFootprints()):
 src=p.LoadBoard(str(R/'boards/mainboard-reference/MainBoard.kicad_pcb'))
 f=p.Cast_to_FOOTPRINT(next(f for f in src.GetFootprints() if f.GetReference()=='U9').Duplicate(False))
 f.SetReference('D1');f.SetValue('FC-B1010RGBT-HG');f.SetFPID(p.LIB_ID('Module','RGBLED'));f.SetUuid(p.KIID(x['D1']['uuid']))
 for pad in f.Pads():pad.SetNetCode(0)
 f.SetOrientationDegrees(0);f.SetPosition(p.VECTOR2I(0,0))
 p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Module.pretty'),f)
 b.Add(f);p.SaveBoard(str(D/'module.kicad_pcb'),b)
