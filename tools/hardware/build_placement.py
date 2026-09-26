#!/usr/bin/env python3
"""Initial four-layer placement, explicitly unrouted. Does not produce fab outputs."""
from pathlib import Path
import json,uuid,pcbnew as p
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';parts=json.loads((D/'docs/module-connectivity.json').read_text())
source=p.LoadBoard(str(R/'boards/mainboard-reference/MainBoard.kicad_pcb'));old={f.GetReference():f for f in source.GetFootprints()};lib=D/'Module.pretty';lib.mkdir(exist_ok=True)
def layers():
 s=p.LSET()
 for l in [p.F_Cu,p.F_Paste,p.F_Mask]:s.AddLayer(l)
 return s
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
# Preserve imported chip and PCB antenna copper geometry in self-contained footprints.
for ref,c in parts.items():
 if c['footprint'].startswith('MainBoard:'):
  f=p.Cast_to_FOOTPRINT(old[c['source_ref']].Duplicate(False));f.SetOrientationDegrees(0);f.SetPosition(pt(0,0));f.SetReference('REF**')
  name=c['footprint'].split(':')[1];f.SetFPID(p.LIB_ID('Module',name))
  for pad in f.Pads():pad.SetNetCode(0)
  p.PCB_IO_KICAD_SEXPR().FootprintSave(str(lib),f);c['footprint']='Module:'+name
# DF40 placement envelope; final pad numbering and manufacturer pattern verification pending.
f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('Module','DF40C_40DS_2mm'));f.SetAttributes(p.FP_SMD)
for i in range(40):
 pad=p.PAD(f);pad.SetNumber(str(i+1));pad.SetAttribute(p.PAD_ATTRIB_SMD);pad.SetShape(p.PAD_SHAPE_RECT);pad.SetSize(pt(.2,1.14));pad.SetPosition(pt(-3.8+(i%20)*.4,-1.32 if i<20 else 1.32));pad.SetLayerSet(layers());f.Add(pad)
for a,b in [((-5.3,-1.69),(5.3,-1.69)),((5.3,-1.69),(5.3,1.69)),((5.3,1.69),(-5.3,1.69)),((-5.3,1.69),(-5.3,-1.69))]:
 s=p.PCB_SHAPE(f);s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(pt(*a));s.SetEnd(pt(*b));s.SetWidth(p.FromMM(.1));s.SetLayer(p.F_Fab);f.Add(s)
p.PCB_IO_KICAD_SEXPR().FootprintSave(str(lib),f)
# Provisional 3 mm inductor envelope; manufacturer land pattern remains a review item.
f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('Module','L_XFL3012_222MEC'));f.SetAttributes(p.FP_SMD)
for i,x in [(1,-1.2),(2,1.2)]:
 pad=p.PAD(f);pad.SetNumber(str(i));pad.SetAttribute(p.PAD_ATTRIB_SMD);pad.SetShape(p.PAD_SHAPE_RECT);pad.SetSize(pt(1.2,2.8));pad.SetPosition(pt(x,0));pad.SetLayerSet(layers());f.Add(pad)
p.PCB_IO_KICAD_SEXPR().FootprintSave(str(lib),f)
b=p.BOARD();b.SetCopperLayerCount(4)
netnames=sorted({pin['net'] for c in parts.values() for pin in c['pins'].values()}-{None});nets={}
for name in netnames:
 n=p.NETINFO_ITEM(b,"/"+name);b.Add(n);nets[name]=n
# 34 x 36 mm envelope. Antenna radiator occupies upper edge; center fixing at (17,18).
loc={'U1':(10,13,0),'U2':(25,13,0),'AE1':(9,.5,0),'Y1':(5,20,0),'U3':(10,29,0),'U4':(24,28,0),'J1':(5,14,90),'J2':(29,25,90),'L4':(14,29,0),'L1':(5,9,90),'L2':(28,8,0),'L3':(11,8,0),'C1':(9,8,90),'C2':(13,8,90),'R3':(7,19,0),'C6':(3,18,90),'C7':(3,22,90),'C60':(7,29,90),'C61':(14,32,0),'C62':(22,27,90),'C63':(26,28,90)}
rest=[ref for ref in parts if ref not in loc]
spots=[(8+i*2.4,22+j*2.2,90) for j in range(3) for i in range(8)]+[(5+i*2.4,33,90) for i in range(9)]
for ref,pos in zip(rest,spots):loc[ref]=pos
for ref,c in parts.items():
 library,name=c['footprint'].split(':');path=lib if library=='Module' else Path('/usr/share/kicad/footprints')/(library+'.pretty')
 f=p.FootprintLoad(str(path),name)
 if f is None:raise RuntimeError(c['footprint'])
 b.Add(f);f.SetReference(ref);f.SetValue(c['value']);f.SetFPID(p.LIB_ID(library,name));f.SetPath(p.KIID_PATH('/'+str(uuid.uuid5(uuid.NAMESPACE_URL,'gps-time-module/root'))+'/'+c['uuid']))
 x,y,a=loc[ref];f.SetPosition(pt(100+x,100+y));f.SetOrientationDegrees(a)
 if ref in ['J1','J2']:f.Flip(f.GetPosition(),False)
 for pad in f.Pads():
  n=c['pins'].get(pad.GetNumber(),{}).get('net');pad.SetNet(nets[n]) if n else pad.SetNetCode(0)
 for field in f.GetFields():field.SetVisible(False)
 f.Reference().SetVisible(True);f.Reference().SetTextSize(pt(.7,.7));f.Reference().SetTextThickness(p.FromMM(.12));f.Reference().SetPosition(pt(100+x,100+y-2));f.Value().SetVisible(False)
# Center fixing keeps both copper and component area clear in the later routing pass.
f=p.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');b.Add(f);f.SetReference('H1');f.SetAttributes(f.GetAttributes()|p.FP_BOARD_ONLY);f.SetPosition(pt(117,118));f.Value().SetVisible(False)
for a,z in [((100,100),(134,100)),((134,100),(134,136)),((134,136),(100,136)),((100,136),(100,100))]:
 s=p.PCB_SHAPE(b);s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(pt(*a));s.SetEnd(pt(*z));s.SetLayer(p.Edge_Cuts);s.SetWidth(p.FromMM(.05));b.Add(s)
for txt,x,y in [('ESP32 + FPGA / DRAFT',117,135),('UNROUTED',117,130)]:
 t=p.PCB_TEXT(b);t.SetText(txt);t.SetPosition(pt(x,y));t.SetTextSize(pt(.8,.8));t.SetTextThickness(p.FromMM(.12));t.SetLayer(p.F_SilkS);b.Add(t)
p.SaveBoard(str(D/'module.kicad_pcb'),b)
(D/'docs/module-connectivity.json').write_text(json.dumps(parts,indent=2)+'\n')
(D/'fp-lib-table').write_text('(fp_lib_table (lib (name "Module") (type "KiCad") (uri "${KIPRJMOD}/Module.pretty") (options "") (descr "Module local footprints")))\n')
(D/'module.kicad_pro').write_text(json.dumps({'meta':{'filename':'module.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.1,'min_track_width':.1,'min_via_diameter':.45,'min_through_hole_diameter':.2}}}},indent=2)+'\n')
print('Saved 4-layer development placement:',len(parts),'components plus center M3 hole')
