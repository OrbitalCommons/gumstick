#!/usr/bin/env python3
"""Readable carrier schematic and standalone, two-unit module-v1 interface symbol."""
from pathlib import Path
import json,uuid,re
R=Path(__file__).resolve().parents[2];D=R/'boards/programming-carrier';parts=json.loads((D/'docs/circuit.json').read_text());channels=json.loads((D/'docs/led-map.json').read_text())
uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,'bp-carrier-v1/'+s));q=lambda s:json.dumps(str(s));items=[];symbols={};pins={};count=0
E=lambda size=1.27,justify='':f'(effects (font (size {size} {size})) '+(f'(justify {justify})' if justify else '')+')'
def prop(k,val,x,y,hide=False):return f'(property {q(k)} {q(val)} (at {x} {y} 0) {E()}'+(' (hide yes)' if hide else '')+')'
def wire(a,b):
 global count
 count+=1;items.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid "{uid("wire"+str(count))}"))')
def label(n,x,y,angle=0,right=False):
 global count
 count+=1;items.append(f'(global_label {q(n)} (shape bidirectional) (at {x} {y} {angle}) {E(.65 if n.startswith(('BUF_','LED_')) else .95,"right" if right else "left")} (uuid "{uid("lab"+str(count))}"))')
def note(t,x,y,size=1.27):items.append(f'(text {q(t)} (at {x} {y} 0) {E(size,"left")} (uuid "{uid(t+str(x)+str(y))}"))')
def box(title,x,y,w,h):
 items.append(f'(rectangle (start {x} {y}) (end {x+w} {y+h}) (stroke (width 0.254) (type default)) (fill (type none)) (uuid "{uid(title)}"))');note(title,x+2.54,y+3.81,1.8)
def symdef(ref):
 c=parts[ref];kind=c['kind'];name=ref;pinmap={};shapes=[];s=[]
 if kind in ['r','c','led']:
  # Horizontal KiCad-standard passive geometry, connected directly in each LED chain.
  pinmap={'1':(-5.08,0,0),'2':(5.08,0,180)}
  if kind=='r':shapes=['(polyline (pts (xy -2.54 0) (xy -1.905 1.016) (xy -0.635 -1.016) (xy 0.635 1.016) (xy 1.905 -1.016) (xy 2.54 0)) (stroke (width 0.254) (type default)) (fill (type none)))']
  elif kind=='c':shapes=['(polyline (pts (xy -0.635 -2.032) (xy -0.635 2.032)) (stroke (width 0.254) (type default)) (fill (type none)))','(polyline (pts (xy 0.635 -2.032) (xy 0.635 2.032)) (stroke (width 0.254) (type default)) (fill (type none)))']
  else:shapes=['(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))','(polyline (pts (xy -1.27 0) (xy 1.27 1.27) (xy 1.27 -1.27) (xy -1.27 0)) (stroke (width 0.254) (type default)) (fill (type none)))','(polyline (pts (xy 0 2) (xy -1.8 3.8) (xy -1.2 2.5)) (stroke (width 0.18) (type default)) (fill (type none)))']
  if kind=='led':
   pinmap={'1':(5.08,0,180),'2':(-5.08,0,0)}
   shapes=[re.sub(r'\(xy (-?[0-9.]+) (-?[0-9.]+)\)',lambda m:f'(xy {-float(m[1])} {m[2]})',t) for t in shapes]
  length=2.54 if kind=='r' else 4.445 if kind=='c' else 3.81
  for num,(x,y,a) in pinmap.items():s.append(f'(pin passive line (at {x} {y} {a}) (length {length}) (name "~" {E()}) (number "{num}" {E()}))')
  h=0;w=0
 else:
  if ref.startswith('U') and int(ref[1:])>=3:
   pinmap={str(i+2):(-20.32,17.78-i*5.08,0) for i in range(8)};pinmap.update({str(18-i):(20.32,17.78-i*5.08,180) for i in range(8)});pinmap.update({'1':(-20.32,-25.4,0),'19':(-20.32,-30.48,0),'10':(0,-38.1,90),'20':(0,38.1,270)});w=15.24;h=33.02
  elif kind=='connector' and ref in ['J1','J2']:
   nums=sorted(c['pins'],key=int);pinmap={n:((-12.7 if i<20 else 12.7),24.13-(i%20)*2.54,(0 if i<20 else 180)) for i,n in enumerate(nums)};w=7.62;h=26.67
  else:
   nums=list(c['pins']);half=(len(nums)+1)//2;w=7.62;h=max(5.08,(half+1)*2.54)
   pinmap={n:((-12.7 if i<half else 12.7),h-5.08-(i%half)*5.08,(0 if i<half else 180)) for i,n in enumerate(nums)}
  if kind=='hole':w=2.54;h=2.54
  shapes=[f'(rectangle (start {-w} {h}) (end {w} {-h}) (stroke (width 0.254) (type default)) (fill (type background)))']
  for num,(x,y,a) in pinmap.items():
   nm=c['names'].get(num,num);tp=c['types'].get(num,'passive')
   if ref in ['J1','J2']:nm='~'
   s.append(f'(pin {tp} line (at {x} {y} {a}) (length 5.08) (name {q(nm)} {E(1.0)}) (number {q(num)} {E(1.0)}))')
 symbols[name]=f'(symbol {q(name)} (pin_names (offset 0.762)'+(' hide' if kind in ['r','c','led'] else '')+') '+('(pin_numbers hide)' if kind in ['r','c','led'] else '')+f' (in_bom {"yes" if c["bom"] else "no"}) (on_board yes) {prop("Reference",ref,0,h+5.08)} {prop("Value",c["value"],0,h+2.54)} (symbol "{name}_0_1" '+''.join(shapes)+f') (symbol "{name}_1_1" '+''.join(s)+'))'
 return pinmap,h
placed=set()
def place(ref,x,y,auto=True):
 c=parts[ref];pm,h=symdef(ref);placed.add(ref);pins[ref]={n:(round(x+a,4),round(y-b,4)) for n,(a,b,_) in pm.items()}
 val=c['value'];hide=c['kind']=='connector' and ref in ['J1','J2']
 items.append(f'(symbol (lib_id "Carrier:{ref}") (at {x} {y} 0) (unit 1) (in_bom {"yes" if c["bom"] else "no"}) (on_board yes) (uuid "{uid(ref)}") '+prop('Reference',ref,x,y-h-(2.54 if c['kind'] in ['r','c','led'] else 5.08)).replace('(size 1.27 1.27)','(size 0.95 0.95)')+prop('Value',val,x,y-h-(1.27 if c['kind'] in ['r','c','led'] else 2.54),hide or c['kind']=='led').replace('(size 1.27 1.27)','(size 0.95 0.95)')+prop('Footprint',c['footprint'],x,y,True)+prop('LCSC',c['lcsc'],x,y,True)+prop('MPN',c['mpn'],x,y,True)+f'(instances (project "carrier" (path "/{uid("root")}" (reference "{ref}") (unit 1)))))')
 if auto:
  for n,(a,b) in pins[ref].items():
   nn=c['pins'][n]
   if nn is None:items.append(f'(no_connect (at {a} {b}) (uuid "{uid(ref+n+"nc")}"))');continue
   dx=-5.08 if pm[n][2]==0 else 5.08 if pm[n][2]==180 else 0
   dy=5.08 if pm[n][2]==90 else -5.08 if pm[n][2]==270 else 0
   wire((a,b),(round(a+dx,4),round(b+dy,4)));label(nn,round(a+dx,4),round(b+dy,4),0,right=dx<0)
 return pins[ref]
# Upper third: interface, power and manual programming controls.
box('Frozen v1 module mating interface',10,10,160,127)
place('J1',51,65);place('J2',131,65)
note('J1 PLUG / J2 SOCKET, 2.0 mm mating height',14,107)
note('Contact numbers = module v1 contact map, not vendor numbering',14,111,.95)
note('25.00 mm centers; M3 midpoint at 12.50 mm',14,115)
note('GPIO46: INPUT ONLY. GPIO45: keep LOW at reset.',14,120)
note('Module internal QSPI and flash pins are not carrier GPIO.',14,125)
box('USB-C, ESD, 5 V input and independent indicator supply',173,10,214,127)
place('J3',210,68);place('U2',266,48);place('F1',314,32);place('U1',337,60)
for ref,x,y in [('R1',247,91),('R2',282,91),('C1',314,91),('C2',351,91),('C3',248,112),('R3',282,112),('D1',314,112),('R4',348,112),('D2',372,112)]:place(ref,x,y)
box('Programming controls / input-only test',390,10,192,127)
place('SW1',425,35);place('SW2',478,35);place('SW3',539,35);place('R5',539,65)
note('FLASH: BOOT, tap RESET; flash over native USB.',397,86)
note('After flashing: RUN, tap RESET. Firmware enables later OTA.',397,92)
note('GPIO46 TEST: use after boot; release before RESET.',397,98)
note('Power down before plugging/unplugging the module.',397,104)
note('All indicators use 3.3 V buffers; GPIO sees 100k bias only.',397,110)
note('RGB channels are active LOW, shared with on-module RGB.',397,116)
# Eight regular banks: labels, real buffer pins, wired resistor/LED pairs.
for bi in range(8):
 x=10+(bi%4)*143;y=142+(bi//4)*119;ref='U'+str(3+bi);bank=[c for c in channels if c['buffer']==ref]
 box(('ESP32' if bi<4 else 'FPGA')+' GPIO indicators '+str(bi%4+1),x,y,140,116)
 place(ref,x+49,y+48,False)
 for k in range(8):
  ni=str(2+k);no=str(18-k);a=pins[ref][ni];z=pins[ref][no]
  n=parts[ref]['pins'][ni];wire(a,(x+24,a[1]));label(n,x+24,a[1],right=True)
  ch=next((c for c in bank if c['input']==k+2),None)
  if ch:
   # Output -> resistor -> LED anode; diode pin1 is cathode on right via 180? use wires around standard symbol.
   rr=place(ch['resistor'],x+83,z[1],False);dd=place(ch['led'],x+106,z[1],False)
   wire(z,rr['1']);label(parts[ch['resistor']]['pins']['1'],*z)
   wire(rr['2'],dd['2']);label(parts[ch['resistor']]['pins']['2'],*rr['2'])
   wire(dd['1'],(x+121,z[1]));label('GND',x+121,z[1])
  else:items.append(f'(no_connect (at {z[0]} {z[1]}) (uuid "{uid(ref+no+"nc")}"))')
 for n in ['1','19','10','20']:
  a=pins[ref][n];nn=parts[ref]['pins'][n];dx=-5.08 if n in ['1','19'] else 0;dy=5.08 if n=='10' else -5.08 if n=='20' else 0;end=(a[0]+dx,a[1]+dy);wire(a,end);label(nn,*end)
 place('C'+str(10+bi),x+105,y+88)
# RGB sink monitor, physically near module. Separate small page to keep main diagram readable.
# Place this small group in unused margin on the main sheet below the banks.
# Remaining components are represented on second sheet (RGB and mechanical); global signals connect.
mainitems=items[:];mainplaced=placed.copy();items=[]
box('Dedicated sink-output monitors and carrier mounting',10,10,277,175)
place('U11',58,68)
for k,ch in enumerate(c for c in channels if c['bank']=='RGB'):
 y=35+k*35;place(ch['bias'],123,y);place(ch['resistor'],170,y);place(ch['led'],220,y)
place('C18',58,130)
for i,ref in enumerate(['H1','H2','H3','H4','H5']):place(ref,30+i*42,164)
note('RGB0/1/2 are current-sink LED outputs on the FPGA, not ordinary push-pull GPIO.',18,193)
note('100k pull-ups; red carrier LEDs illuminate when the FPGA pin is LOW.',18,200)
note('The daughterboard RGB LEDs remain connected. This is a functional status test.',18,207)
note('H1: 2.0 mm board-to-board spacer, M3 screw; do not use screw to force mating.',18,220)
rgbitems=items[:];rgbplaced=placed-mainplaced;items=[]
box('High-impedance GPIO bias resistors (100k)',10,10,390,260)
for i,ch in enumerate(c for c in channels if c['bank']!='RGB'):
 xx=35+(i%6)*63.5;yy=40+(i//6)*22.86
 place(ch['bias'],xx,yy,False)
 a=pins[ch['bias']]['1'];bb=pins[ch['bias']]['2'];label(ch['signal'],*a,90);label(parts[ch['bias']]['pins']['2'],*bb,270)
note('Bias holds buffer inputs defined with the module removed. GPIO0 has a carrier pull-up; EN retains its module pull-up.',15,285)
note('GPIO45 / GPIO46 stay LOW at reset. RGB pull-ups are on the RGB sheet.',15,291)
biasitems=items[:];biasplaced=placed-mainplaced-rgbplaced;items=mainitems
sheetid=uid('rgb-sheet');items.append(f'(sheet (at 444.5 386.08) (size 116.84 12.7) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid "{sheetid}") (property "Sheetname" "RGB and mechanics" (at 444.5 384.81 0) {E()}) (property "Sheetfile" "rgb.kicad_sch" (at 444.5 401.32 0) {E()}) (instances (project "carrier" (path "/{uid("root")}" (page "2")))))')
# Explicit supply-entry flags document the USB-derived source and return.
for ni,nn in enumerate(['VIN_5V','GND']):
 name='FLAG_'+str(ni)
 symbols[name]=f'(symbol "{name}" (power) (pin_names hide) (pin_numbers hide) (in_bom no) (on_board no) {prop("Reference","#FLG",0,0,True)} {prop("Value","PWR_FLAG",0,0,True)} (symbol "{name}_0_1" (polyline (pts (xy 0 0) (xy 0 2.54) (xy 1.27 3.81) (xy 0 5.08) (xy -1.27 3.81) (xy 0 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))) (symbol "{name}_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" {E()}) (number "1" {E()}))))'
 xx=357+ni*15;yy=127
 items.append(f'(symbol (lib_id "Carrier:{name}") (at {xx} {yy} 0) (unit 1) (in_bom no) (on_board no) (uuid "{uid(name)}") {prop("Reference","#FLG0"+str(ni),xx,yy,True)} {prop("Value","PWR_FLAG",xx,yy,True)} (instances (project "carrier" (path "/{uid("root")}" (reference "#FLG0{ni}") (unit 1)))))')
 label(nn,xx,yy)
biasid=uid('bias-sheet')
items.append(f'(sheet (at 297.18 386.08) (size 116.84 12.7) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid "{biasid}") (property "Sheetname" "GPIO input bias" (at 297.18 384.81 0) {E()}) (property "Sheetfile" "bias.kicad_sch" (at 297.18 401.32 0) {E()}) (instances (project "carrier" (path "/{uid("root")}" (page "3")))))')
biasitems=[s.replace('/'+uid('root')+'"','/'+uid('root')+'/'+biasid+'"') for s in biasitems]
# Secondary sheet instances need a hierarchical root path.
rgbitems=[s.replace('/'+uid('root')+'"','/'+uid('root')+'/'+sheetid+'"') for s in rgbitems]
def write_sheet(path,its,sid,paper):
 its=[re.sub(r'\((at|xy|start|end) (-?[0-9.]+) (-?[0-9.]+)',lambda m:f'({m[1]} {round(round(float(m[2])/1.27)*1.27,4)} {round(round(float(m[3])/1.27)*1.27,4)}',a) for a in its]
 lib=''.join(s.replace('(symbol "'+n+'"','(symbol "Carrier:'+n+'"',1) for n,s in symbols.items())
 path.write_text(f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{sid}") (paper "{paper}") (title_block (title "Module v1 programming and GPIO test carrier") (rev "A") (company "bp-test")) (lib_symbols '+lib+') '+''.join(its)+')\n')
write_sheet(D/'carrier.kicad_sch',items,uid('root'),'A2');write_sheet(D/'rgb.kicad_sch',rgbitems,uid('rgbroot'),'A4');write_sheet(D/'bias.kicad_sch',biasitems,uid('biasroot'),'A3')
# Reusable module symbol: 80 pins split into two units and matching combined footprint.
pinout=json.loads((D/'docs/contact-map.json').read_text());units=[]
for unit,c in [(1,'J1'),(2,'J2')]:
 pp=sorted([a for a in pinout if a['connector']==c],key=lambda a:int(a['module_pin']));ss=[]
 for i,a in enumerate(pp):
  xx=-35.56 if i<20 else 35.56;yy=24.13-(i%20)*2.54;ang=0 if i<20 else 180;tp='power_in' if a['signal'] in ['VIN_5V','GND'] else 'bidirectional';ss.append(f'(pin {tp} line (at {xx} {yy} {ang}) (length 5.08) (name {q(a["signal"])} {E(1)}) (number {q(c+"_"+a["module_pin"])} {E(1)}))')
  # Composite symbol uses Jx_n pad names and therefore cannot silently use a standalone connector footprint.
 units.append(f'(symbol "ESP32_FPGA_Module_v1_{unit}_1" (rectangle (start -30.48 27.94) (end 30.48 -27.94) (stroke (width 0.254) (type default)) (fill (type background)))'+''.join(ss)+')')
module=f'(symbol "ESP32_FPGA_Module_v1" (pin_names (offset 0.762)) (in_bom yes) (on_board yes) {prop("Reference","M",0,33.02)} {prop("Value","ESP32_FPGA_Module_v1",0,30.48)} {prop("Footprint","Carrier:ESP32_FPGA_Module_v1_Interface",0,0,True)}'+''.join(units)+')'
(D/'Carrier.kicad_sym').write_text('(kicad_symbol_lib (version 20250114) (generator "kicad_symbol_editor") '+''.join(symbols.values())+module+')\n')
assert placed==set(parts),(set(parts)-placed)
# Match PCB schematic paths for secondary-sheet components, without changing any tracks.
import pcbnew as p
b=p.LoadBoard(str(D/'carrier.kicad_pcb'))
for f in b.GetFootprints():
 ref=f.GetReference();path='/'+uid('root')+('' if ref in mainplaced else '/'+sheetid if ref in rgbplaced else '/'+biasid)+'/'+uid(ref);f.SetPath(p.KIID_PATH(path))
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
print('Schematic:',len(placed),'parts, 2 sheets')
