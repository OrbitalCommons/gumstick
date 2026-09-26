#!/usr/bin/env python3
"""Use solderable thermal pad connections; preserve thermal/RF ground exceptions."""
from pathlib import Path
import json,pcbnew as p
D=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module'
b=p.LoadBoard(str(D/'module.kicad_pcb'))
exceptions={('U1','57'):'ESP32 exposed ground/thermal pad',('U1','PAD'):'ESP32 exposed ground/thermal pad',('U2','PAD'):'FPGA exposed ground/thermal pad',('U3','9'):'Buck exposed ground/thermal pad',('AE1','2'):'Antenna RF ground termination',('J3','2'):'U.FL shield/RF ground'}
report=[]
# These pads use existing routed thermal necks. Preserve their topology rather
# than inserting absolute-coordinate tracks from an older connector placement.
manual_pads={(fp.GetReference(),a.GetNumber()) for fp in b.GetFootprints()
             for a in fp.Pads() if a.GetNetname()=='GND'
             and a.GetLocalZoneConnection()==p.ZONE_CONNECTION_NONE}
for z in b.Zones():
 if not z.GetIsRuleArea():
  z.SetPadConnection(p.ZONE_CONNECTION_THERMAL)
  z.SetThermalReliefGap(p.FromMM(.15));z.SetThermalReliefSpokeWidth(p.FromMM(.15));z.SetMinThickness(p.FromMM(.1))
for fp in b.GetFootprints():
 fp.SetLocalZoneConnection(p.ZONE_CONNECTION_INHERITED)
 for a in fp.Pads():
  key=(fp.GetReference(),a.GetNumber());reason=exceptions.get(key)
  a.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL if reason else p.ZONE_CONNECTION_INHERITED)
  # Preserve individually reviewed spoke angles on the routed board.
  if fp.GetReference() in ['J1','J2']:
   a.SetLocalThermalSpokeWidthOverride(p.FromMM(.1));a.SetThermalGap(p.FromMM(.1))
  if key in manual_pads:a.SetLocalZoneConnection(p.ZONE_CONNECTION_NONE)
  if reason:report.append({'reference':key[0],'pad':key[1],'reason':reason})
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
(D/'fab/checks/thermal-reliefs.json').write_text(json.dumps({'default':'thermal','gap_mm':.15,'spoke_width_mm':.15,'connector_spoke_width_mm':.1,'solid_pad_exceptions':report,'vias':'Solid zone connections retained','manual_neck_pads':[f'{ref}.{pin}' for ref,pin in sorted(manual_pads)],'manual_neck_width_mm':.1,'connector_gap_mm':.1},indent=2)+'\n')
