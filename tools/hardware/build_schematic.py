#!/usr/bin/env python3
"""Generate the module schematic and local symbols from audited pin data."""
from pathlib import Path
import json,uuid,re
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';parts=json.loads((D/'docs/module-connectivity.json').read_text())
uid=lambda key:str(uuid.uuid5(uuid.NAMESPACE_URL,'gps-time-module/'+key))
q=lambda s:json.dumps(str(s))
items=[];symbols={};positions={};terminals={}
power_symbols=set()
power_ref_count=0
power_lead_columns={}
POWER_NETS={'VIN_5V','GND','+3.3V','ESP_VDD3P3','+1.2V','+1.2V_PLL'}
PIN_LABEL_STUB=20.32
wired=set(['U3','U4','L4','R62','C60','C61','C62','C63','Y1','R3','C6','C7','AE1','L3','C1','C2'])
wired.update(['R64','R65','L1','L2','R22','C32','JP1','J3','R63','C68','C69'])
wired.update(k for k in parts if k.startswith('C') and k not in ['C32'])
def eff(size=1.27,justify=''):
 return f'(effects (font (size {size} {size})) {"(justify "+justify+")" if justify else ""})'
def prop(k,v,x=0,y=0,hide=False):return f'(property {q(k)} {q(v)} (at {x} {y} 0) {"(hide yes)" if hide else ""} {eff()})'
def wire(x,y,a,b):items.append(f'(wire (pts (xy {x} {y}) (xy {a} {b})) (stroke (width 0) (type default)) (uuid "{uid(str((x,y,a,b)))}"))')
def label(n,x,y,ang=0,justify='left bottom'):items.append(f'(label {q(n)} (at {x} {y} {ang}) {eff(1.27,justify)} (uuid "{uid(str((n,x,y)))}"))')
def note(t,x,y,size=1.5):items.append(f'(text {q(t)} (at {x} {y} 0) {eff(size,"left")} (uuid "{uid(t)}"))')
def power_name(net):return 'PWR_'+re.sub(r'[^A-Za-z0-9]+','_',net).strip('_')
def ensure_power(net):
 if net in power_symbols:return
 power_symbols.add(net);name=power_name(net)
 if net=='GND':
  shape='(polyline (pts (xy -2.54 -1.27) (xy 2.54 -1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -1.524 -2.286) (xy 1.524 -2.286)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -0.508 -3.302) (xy 0.508 -3.302)) (stroke (width 0.254) (type default)) (fill (type none)))'
  value_at='0 -4.826'
 else:
  shape='(polyline (pts (xy 0 0) (xy 0 -4.064)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -1.524 -2.54) (xy 0 -4.064) (xy 1.524 -2.54)) (stroke (width 0.254) (type default)) (fill (type none)))'
  value_at='0 -5.334'
 symbols[name]=f'(symbol "{name}" (power) (pin_names hide) (pin_numbers hide) (in_bom no) (on_board no) {prop("Reference","#PWR",hide=True)} (property "Value" {q(net)} (at {value_at} 0) {eff(1.27)}) (symbol "{name}_0_1" {shape}) (symbol "{name}_1_1" (pin power_in line (at 0 0 90) (length 0) (name {q(net)} {eff()}) (number "1" {eff()}))))'
def power_port(net,x,y,orientation=0):
 global power_ref_count
 power_ref_count+=1
 power_ref=f'#PWR{power_ref_count:03d}'
 ensure_power(net)
 if net!='GND' and orientation==0:orientation=180
 items.append(f'(symbol (lib_id "Module:{power_name(net)}") (at {x} {y} {orientation}) (unit 1) (in_bom no) (on_board no) (uuid "{uid("power"+str((net,x,y,orientation)))}") {prop("Reference",power_ref,x,y,True)} (property "Value" {q(net)} (at {x} {y-5.334 if net!="GND" else y-4.826} 0) {eff(1.27)}) (instances (project "module" (path "/{uid("root")}" (reference "{power_ref}") (unit 1)))))')
def net_marker(net,x,y,ang=0,source=None):
 if net in POWER_NETS:
  if source:
   sx,sy=source
   if abs(sy-y)<0.001 and abs(sx-x)>0.001:
    # Dense IC/connector pin fields read better when power symbols leave the
    # signal-label row. Run the pin lead outward, then jog V+ rails upward and
    # GND downward into conventional local power symbols.
    # Put power annotations beyond the signal labels; stagger nearby
    # supply pins so their arrows and names do not stack on one another.
    direction=-1 if x<sx else 1
    key=(round(sx,3),direction,net=='GND')
    previous=power_lead_columns.setdefault(key,[])
    used={lane for py,lane in previous if abs(py-y)<12.7}
    lane=next(i for i in range(12) if i not in used)
    previous.append((y,lane))
    # Ground leads turn downward, so the upper pin must use the
    # farther column; supply leads turn upward and use the opposite order.
    reach=12.7+7.62*(3-lane if net=='GND' else lane)
    outer=round(x+direction*reach,4)
    wire(x,y,outer,y);x=outer
    vertical=-5.08 if net!='GND' else 5.08
    wire(x,y,x,round(y+vertical,4))
    power_port(net,x,round(y+vertical,4))
    return
  power_port(net,x,y)
 else:
  # Right-facing signals start their text just beyond the pin, over the wire.
  if source and x>source[0] and abs(y-source[1])<0.001:
   label(net,x,y,0,'right bottom')
  elif source and x<source[0] and abs(y-source[1])<0.001:
   label(net,x,y,0,'left bottom')
  else:label(net,x,y,ang)
def solder_selector(ref):
 # KiCad standard solder-jumper artwork, embedded locally for portability.
 template=(R/'tools/hardware/symbols/solder-jumper-3-bridged12.sexpr').read_text()
 symbols[ref]=template.replace('SolderJumper_3_Bridged12',ref)
 return ref,{'1':(-5.08,0,0),'2':(0,3.81,90),'3':(5.08,0,180)},1.016

def custom(ref):
 if ref=='J3':
  symbols[ref]=f'(symbol "J3" (pin_names hide) (pin_numbers hide) (in_bom yes) (on_board yes) {prop("Reference",ref)} {prop("Value",parts[ref]["value"])} (symbol "J3_0_1" (circle (center 0 0) (radius 2.54) (stroke (width 0.254) (type default)) (fill (type none))) (circle (center 0 0) (radius 0.508) (stroke (width 0.254) (type default)) (fill (type outline)))) (symbol "J3_1_1" (pin passive line (at -7.62 0 0) (length 7.62) (name "RF" {eff()}) (number "1" {eff()})) (pin passive line (at 0 -7.62 90) (length 5.08) (name "GND" {eff()}) (number "2" {eff()}))))'
  return ref,{'1':(-7.62,0,0),'2':(0,7.62,90)},5.08
 if ref in ['AE1','JP1']:
  symbols[ref]=(R/('tools/hardware/symbols/'+ref+'-rf.sexpr')).read_text()
  return ref,({'1':(-6.35,0,0),'2':(0,5.08,90)} if ref=='AE1' else {'1':(-5.08,0,0),'2':(5.08,0,180),'3':(0,5.08,90)}),5.08
 c=parts[ref];pins=list(c['pins'].items());name=ref;side={};ps=[]
 if ref.startswith('TP'):
  symbols[ref]=f'(symbol "{ref}" (pin_names hide) (pin_numbers hide) (in_bom no) (on_board yes) {prop("Reference",ref)} {prop("Value",c["value"])} (symbol "{ref}_0_1" (circle (center 0 2.54) (radius 1.016) (stroke (width .254) (type default)) (fill (type none)))) (symbol "{ref}_1_1" (pin passive line (at 0 0 90) (length 1.524) (name "1" {eff()}) (number "1" {eff()}))))'
  return ref,{'1':(0,0,90)},5.08
 half=(len(pins)+1)//2
 if ref in ['J1','J2']:half=20
 width=17.78 if ref in ['U1','U2'] else 10.16
 height=max(5.08,(half+1)*2.54/2)
 special={
 'U3':{'2':(-15.24,5.08,0),'3':(-15.24,0,0),'7':(15.24,5.08,180),'8':(15.24,-5.08,180),'6':(15.24,0,180),'1':(-5.08,-15.24,90),'4':(0,-15.24,90),'9':(5.08,-15.24,90),'5':(7.62,-15.24,90)},
 'U4':{'1':(-15.24,2.54,0),'3':(-15.24,-2.54,0),'2':(0,-10.16,90),'5':(15.24,2.54,180),'4':(15.24,-2.54,180)},
 'Y1':{'IN/OUT':(-15.24,0,0),'OUT/IN':(15.24,0,180),'GND-A':(-2.54,-10.16,90),'GND-B':(2.54,-10.16,90)},
 'J3':{'1':(-7.62,0,0),'2':(0,-7.62,90)}}
 special['U5']=special['U4']
 if ref=='U3':height=10.16
 for idx,(num,p) in enumerate(pins):
  left=idx<half;j=idx if left else idx-half
  # Connector odds/even rows, physical numbering remains provisional.
  y=(half-1)*1.27-j*2.54;x=-width-5.08 if left else width+5.08;ang=0 if left else 180
  if ref in special:x,y,ang=special[ref][num]
  typ=p['type'];pn=p['name']
  if ref=='U1':typ='power_in' if pn.startswith('VDD') or pn=='EPAD' else 'bidirectional'
  if ref=='AE1':typ='passive'
  ps.append(f'(pin {typ} line (at {x} {y} {ang}) (length 5.08) (name {q(pn)} {eff(.95)}) (number {q(num)} {eff(.95)}))')
  side[num]=(x,-y,ang)
 symbols[name]=f'(symbol "{name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes) {prop("Reference",ref)} {prop("Value",c["value"])} (symbol "{name}_0_1" (rectangle (start {-width} {height}) (end {width} {-height}) (stroke (width .254) (type default)) (fill (type background)))) (symbol "{name}_1_1" {"".join(ps)}))'
 return name,side,height

def passive(ref):
 c=parts[ref];name=ref;kind=ref[0]
 pins=f'(pin passive line (at 0 3.81 270) (length 2.286) (name "~" {eff(1.27)}) (number "1" {eff(1)})) (pin passive line (at 0 -3.81 90) (length 2.286) (name "~" {eff(1.27)}) (number "2" {eff(1)}))'
 if kind=='C':shape='(polyline (pts (xy -2.032 .762) (xy 2.032 .762)) (stroke (width .254) (type default)) (fill (type none))) (polyline (pts (xy -2.032 -.762) (xy 2.032 -.762)) (stroke (width .254) (type default)) (fill (type none)))';pins=pins.replace('2.286','3.048')
 else:shape='(rectangle (start -1.016 1.524) (end 1.016 -1.524) (stroke (width .254) (type default)) (fill (type none)))'
 if ref in ['L4','L3','R3','L1','L2','R22','R63','R62']:
  pins=f'(pin passive line (at -3.81 0 0) (length 2.286) (name "~" {eff()}) (number "1" {eff()})) (pin passive line (at 3.81 0 180) (length 2.286) (name "~" {eff()}) (number "2" {eff()}))'
  shape='(rectangle (start -1.524 1.016) (end 1.524 -1.016) (stroke (width 0.254) (type default)) (fill (type none)))'
 if ref in ['R22','R20','R28','R29']:pins=pins.replace('(number "1"','(number "TEMP"').replace('(number "2"','(number "1"').replace('(number "TEMP"','(number "2"')
 symbols[name]=f'(symbol "{name}" (pin_names hide) (pin_numbers hide) (in_bom yes) (on_board yes) {prop("Reference",ref)} {prop("Value",c["value"])} (symbol "{name}_0_1" {shape}) (symbol "{name}_1_1" {pins}))'
 return name,({'2':(-3.81,0,0),'1':(3.81,0,180)} if ref=='R22' else {'1':(-3.81,0,0),'2':(3.81,0,180)} if ref in ['L4','L3','R3','L1','L2','R22','R63','R62'] else {'2':(0,-3.81,270),'1':(0,3.81,90)} if ref in ['R20','R28','R29'] else {'1':(0,-3.81,270),'2':(0,3.81,90)}),3.81

def place(ref,x,y):
 c=parts[ref];ispass=ref[0] in 'RCL';name,pins,h=solder_selector(ref) if ref.startswith('SJ') else passive(ref) if ispass else custom(ref)
 c['uuid']=uid(ref);positions[ref]=(x,y)
 if ispass:
  text_dy=-5.0 if ref in ['L1','L2','L4'] else 0
  props=''.join(prop(k,v,x+4,y+dy+text_dy).replace(eff(),eff(1.27,'left')) for k,v,dy in [('Reference',ref,-1.5),('Value',c['value'],1.5)])
 else:
  props=prop('Reference',ref,x,y-h-5.08)+prop('Value',c['value'],x,y-h-2.54)
 props+=prop('Footprint',c['footprint'],x,y,True)
 for field,key in [('MPN','mpn'),('Manufacturer','manufacturer'),('LCSC','lcsc')]:
  if c.get(key):props+=prop(field,c[key],x,y,True)
 items.append(f'(symbol (lib_id "Module:{name}") (at {x} {y} 0) (unit 1) (in_bom {'no' if ref.startswith(('SJ','TP')) or c.get('pcb_feature') else 'yes'}) (on_board yes) (dnp {'yes' if c.get('dnp') else 'no'}) (uuid "{c["uuid"]}") {props} (instances (project "module" (path "{chr(47)+uid("root")}" (reference "{ref}") (unit 1)))))')
 for num,(dx,dy,ang) in pins.items():
  n=c['pins'][num]['net'];a=round(x+dx,4);b=round(y+dy,4)
  if n is None:items.append(f'(no_connect (at {a} {b}) (uuid "{uid(ref+num+"nc")}"))');continue
  terminals[ref,num]=(a,b)
  if ref in wired:continue
  if ispass:
   by=round(b+(-5.08 if dy<0 else 5.08),4);wire(a,b,a,by);net_marker(n,a,by,source=(a,b))
  else:
   ax=round(a+(-PIN_LABEL_STUB if dx<0 else PIN_LABEL_STUB),4);wire(a,b,ax,b);net_marker(n,ax,b,180 if dx<0 else 0,source=(a,b))

def section(title,x,y,w,h):
 # Keep section outlines clear of the A2 drawing-sheet inner border.
 right=min(x+w,581.3);left=max(x,12.7);w=right-left;x=left
 note(title,x+5,y+7,1.8)
 items.append(f'(rectangle (start {x} {y}) (end {x+w} {y+h}) (stroke (width 0.254) (type dash)) (fill (type none)) (uuid "{uid("section-"+title)}"))')

note('ESP32-S2 + iCE40UP5K | Development module | Rev A',15,12,2.3)
section('ESP32 / integrated flash',10,20,175,112)
section('FPGA / shared processor interface',190,20,175,112)
section('Motherboard connectors',370,20,210,178)
place('U1',93.98,78.74);place('U2',276.86,78.74)
place('J1',469.9,62.23);place('J2',469.9,142.24)
section('40 MHz crystal',10,138,175,58)
place('Y1',91.44,162.56)
place('R3',38.1,162.56);place('C6',63.5,177.8);place('C7',119.38,177.8)
section('RF matching / external antenna',190,138,175,66)
place('L3',224.79,162.56);place('C1',205.74,177.8);place('C2',245.11,177.8)
place('J3',279.4,162.56)
note('U.FL external antenna required for Wi-Fi.',195.58,198.12,1.05)
section('Boot and reset defaults',10,202,175,42)
for ref,x in zip(['R20','R28','R29'],[25.4,127.0,165.1]):place(ref,x,226.06)
place('R22',63.5,220.98);place('C32',83.82,231.14)
section('RGB status indicator',370,204,210,40)
if 'D1' in parts:place('D1',469.9,226.06)
section('3.3 V buck regulator / 5 V input',10,250,175,72)
BUCK_DX=22.86
bx=lambda x:round(x+BUCK_DX,4)
place('U3',bx(55.88),274.32)
place('R64',bx(76.2),294.64);place('R65',bx(76.2),308.61)
for ref,x,y in [('L4',88.9,269.24),('R62',88.9,279.4),('C60',25.4,297.18),('C61',111.76,297.18),('C67',132.08,297.18)]:place(ref,bx(x),y)
section('1.2 V LDO / FPGA core supply',190,250,175,72)
place('U4',269.24,274.32)
place('C62',228.6,289.56);place('C63',309.88,289.56)
section('ESP32 supply filtering / decoupling',370,250,210,72)
section('FPGA supply filtering / decoupling',10,330,355,44)
section('FPGA debug test points',370,330,210,44)
place('TP1',391.16,353.06);place('TP2',490.22,353.06)
filter_groups=[('L1','C33','C34','C35',381.0,275.59,'+3.3V','ESP_VDD3P3'),
               ('L2','C45','C43','C44',20.32,345.44,'+1.2V','+1.2V_PLL')]
for ind,cin,cout,cbypass,x,y,_,_ in filter_groups:
 place(ind,x+15.24,y)
 for ref,dx in [(cin,0),(cout,30.48),(cbypass,43.18)]:place(ref,x+dx,y+10.16)
note('ESP32 pi filter: U1 pins 3, 4.',381.0,301.0,1.05)
note('PLL pi filter: U2 pin 29.',20.32,371.0,1.05)
esp_groups=[('+3.3V',['C37','C38','C39','C40','C41','C42'],474.98,285.75,'ESP32 3.3 V decoupling')]
fpga_groups=[
 ('+1.2V',['C49','C50'],180.34,355.6,'Core: U2 pins 5, 30'),
 ('+3.3V',['C48','C52'],241.3,355.6,'Fixed 3.3 V supplies'),
 ('+3.3V',['C46','C66'],302.26,355.6,'Bank 0: U2 pin 33')]
decoupling_groups=esp_groups+fpga_groups
for _,refs,x0,y0,text in decoupling_groups:
 for i,ref in enumerate(refs):place(ref,x0+i*12.7,y0)
 note(text,x0,y0+15.24,1.05)
# Explicit local wiring. Net labels remain only at block boundaries.
def path(*pts):
 for a,b in zip(pts,pts[1:]):
  if a!=b:wire(*a,*b)
def pin(ref,num):return terminals[ref,str(num)]
def junction(x,y):items.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid("junction"+str((x,y)))}"))')
def rail(net,points,y):
 xs=sorted(set(x for x,_ in points))
 for x,py in points:path((x,py),(x,y))
 for x1,x2 in zip(xs,xs[1:]):wire(x1,y,x2,y)
 for x in xs[1:-1]:junction(x,y)
 net_marker(net,xs[0],y)
# Buck input/enable, switch/inductor, feedback, output, power-good pullup.
rail('VIN_5V',[pin('C60',1),(bx(35.56),274.32)],269.24)
path(pin('U3',2),(bx(35.56),269.24));path(pin('U3',3),(bx(35.56),274.32));junction(bx(35.56),269.24)
path(pin('U3',7),pin('L4',1));label('BUCK_SW',bx(72.39),269.24)
path(pin('L4',2),(bx(111.76),269.24),pin('C61',1))
path((bx(111.76),269.24),(bx(132.08),269.24),pin('C67',1));junction(bx(111.76),269.24)
path((bx(132.08),269.24),(167.64,269.24));junction(bx(132.08),269.24);label('+3.3V',167.64,269.24,0,'right bottom')
path(pin('R62',2),(bx(111.76),279.4));junction(bx(111.76),279.4)
path(pin('U3',6),(bx(96.52),274.32),(bx(96.52),269.24));junction(bx(96.52),269.24)
path(pin('U3',8),pin('R62',1));label('PG_3V3',bx(76.2),279.4)
rail('GND',[pin('C60',2),pin('C61',2),pin('C67',2)]+[pin('U3',n) for n in [1,4]],314.96)
# Adjustable buck divider, sensed from the output rail.
path(pin('R64',1),(bx(76.2),287.02));net_marker('+3.3V',bx(76.2),287.02)
path(pin('R64',2),pin('R65',1));junction(bx(76.2),302.26)
path(pin('U3',5),(bx(63.5),302.26),(bx(76.2),302.26));label('BUCK_FB',bx(63.5),302.26)
path(pin('R65',2),(bx(76.2),314.96));junction(bx(76.2),314.96)
# LDO with bypass capacitors and enable tied to its input.
rail('+3.3V',[pin('C62',1),pin('U4',1)],271.78)
path(pin('U4',3),(246.38,276.86),(246.38,271.78));junction(246.38,271.78)
rail('+1.2V',[pin('U4',5),pin('C63',1)],271.78)
path((309.88,271.78),(325.12,271.78));junction(309.88,271.78);label('+1.2V',325.12,271.78,0,'right bottom')
rail('GND',[pin('C62',2),pin('U4',2),pin('C63',2)],307.34)
# ESP_EN reset RC: supply -> pull-up -> enable node, shunt capacitor to ground.
path((50.8,220.98),pin('R22',2));net_marker('+3.3V',50.8,220.98)
path(pin('R22',1),(83.82,220.98),(96.52,220.98));label('ESP_EN',96.52,220.98)
path((83.82,220.98),pin('C32',1));junction(83.82,220.98)
path(pin('C32',2),(83.82,237.49));net_marker('GND',83.82,237.49)
items[-1]=items[-1].replace('(property "Value" "GND"', '(property "Value" "GND" (hide yes)')
# Crystal series link and load capacitors.
path(pin('R3',1),(25.4,162.56));label('XTAL_P',25.4,162.56)
path(pin('R3',2),pin('Y1','IN/OUT'));path(pin('C6',1),(63.5,162.56));junction(63.5,162.56)
label('XTAL_P_CRYSTAL',45.72,162.56)
path(pin('Y1','OUT/IN'),(119.38,162.56),pin('C7',1));path((119.38,162.56),(134.62,162.56));junction(119.38,162.56);label('XTAL_N',134.62,162.56,0,'right bottom')
rail('GND',[pin('C6',2),pin('C7',2),pin('Y1','GND-A'),pin('Y1','GND-B')],190.5)
# Original ESP32 matching directly feeds U.FL, without selector or chip branch.
path(pin('C1',1),(205.74,162.56),pin('L3',1));path((196.85,162.56),(205.74,162.56));junction(205.74,162.56);label('RF_IN',196.85,162.56)
path(pin('L3',2),pin('J3',1));path(pin('C2',1),(245.11,162.56));junction(245.11,162.56);label('RF_ANT',252.73,162.56)
rail('GND',[pin('C1',2),pin('C2',2),pin('J3',2)],190.5)
# Each filter has an input shunt capacitor, series inductor, and output shunts.
for ind,cin,cout,cbypass,x,y,vin,vout in filter_groups:
 path(pin(cin,1),(x,y),pin(ind,1));net_marker(vin,x,y)
 path(pin(ind,2),(x+30.48,y),(x+43.18,y))
 path(pin(cout,1),(x+30.48,y));junction(x+30.48,y)
 path(pin(cbypass,1),(x+43.18,y));net_marker(vout,x+43.18,y)
 rail('GND',[pin(cin,2),pin(cout,2),pin(cbypass,2)],round(y+17.78,4))
# Shared rails within each explicit decoupling group.
for _,refs,_,_,_ in decoupling_groups:
 groups={}
 for r in refs:
  for num in ['1','2']:
   net=parts[r]['pins'][num]['net'];groups.setdefault((num,net),[]).append(pin(r,num))
 for (num,net),pts in groups.items():
  rail(net,pts,round(pts[0][1]+(-2.54 if num=='1' else 2.54),4))
# Power flags represent driven rails after passive filters.
for i,n in enumerate(['VIN_5V','GND','+3.3V','ESP_VDD3P3','+1.2V_PLL']):
 name='PWR_FLAG';symbols[name]=f'(symbol "PWR_FLAG" (power) (pin_names hide) (pin_numbers hide) (in_bom no) (on_board no) {prop("Reference","#FLG",hide=True)} {prop("Value","PWR_FLAG",hide=True)} (symbol "PWR_FLAG_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" {eff()}) (number "1" {eff()}))))'
 x,y={'VIN_5V':(48.26,269.24),'GND':(48.26,314.96),'+3.3V':(134.62,269.24),'ESP_VDD3P3':(424.18,275.59),'+1.2V_PLL':(63.5,345.44)}[n]
 items.append(f'(symbol (lib_id "Module:PWR_FLAG") (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (uuid "{uid("flag"+n)}") {prop("Reference",f"#FLG0{i}",x,y,True)} {prop("Value","PWR_FLAG",x,y,True)} (instances (project "module" (path "/{uid("root")}" (reference "#FLG0{i}") (unit 1)))))')
lib='\n'.join(symbols.values());(D/'Module.kicad_sym').write_text(f'(kicad_symbol_lib (version 20231120) (generator "module_port") {lib})\n')
embedded='\n'.join(s.replace(f'(symbol "{n}"',f'(symbol "Module:{n}"',1) for n,s in symbols.items())
(D/'module.kicad_sch').write_text(f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{uid("root")}") (paper "A2") (title_block (title "ESP32 FPGA module - development") (rev "A-draft")) (lib_symbols {embedded}) {"".join(items)} (sheet_instances (path "/" (page "1"))))\n')
(D/'sym-lib-table').write_text('(sym_lib_table (lib (name "Module") (type "KiCad") (uri "${KIPRJMOD}/Module.kicad_sym") (options "") (descr "Project-local module symbols")))\n')
(D/'docs/module-connectivity.json').write_text(json.dumps(parts,indent=2)+'\n')
print('Generated schematic with',len(parts),'components')
# KiCad accepts .762, but the web viewer requires a leading zero for numbers.
for path in [D/'module.kicad_sch',D/'Module.kicad_sym']:
 path.write_text(re.sub(r'(?<=[\s(])(-?)\.(\d+)',r'\g<1>0.\2',path.read_text()))
