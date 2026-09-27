#!/usr/bin/env python3
"""Programming carrier sources. Frozen v1 contact geometry is the interface authority.
Run with system Python (KiCad pcbnew). Does not modify the daughterboard.
"""
import sys
if '--rebuild-unrouted' not in sys.argv:
 raise SystemExit('Historical construction step: requires --rebuild-unrouted; will overwrite routed work. Use calibrator_export.py for deliverables.')

from pathlib import Path
import pcbnew as p, json,csv,uuid,re,shutil,math
R=Path(__file__).resolve().parents[2]; D=R/'boards/gps-time-calibrator'; M=R/'boards/esp32-fpga-module'
for d in ['Calibrator.pretty','docs','3dmodels','fab/checks']: (D/d).mkdir(parents=True,exist_ok=True)
uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,'bp-calibrator-a/'+s))
q=lambda s:json.dumps(str(s))
mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
board=p.BOARD();board.SetCopperLayerCount(4)
board.GetDesignSettings().SetAuxOrigin(v(20,110));board.GetDesignSettings().SetGridOrigin(v(20,20))
parts={}; footprints={};nets={};libraries={}; routes=[]
def net(n):
 if n not in nets:
  nets[n]=p.NETINFO_ITEM(board,n);board.Add(nets[n])
 return nets[n]
def model_local(f):
 models=list(f.Models());f.Models().clear()
 for m in models:
  source=Path(re.sub(r'\$\{KICAD\d+_3DMODEL_DIR\}','/usr/share/kicad/3dmodels',m.m_Filename).replace('${KIPRJMOD}',str(M)))
  if source.suffix=='.wrl' and source.with_suffix('.step').exists():source=source.with_suffix('.step')
  if source.exists():
   target=D/'3dmodels'/source.name
   if not target.exists():shutil.copy2(source,target)
   m.m_Filename='${KIPRJMOD}/3dmodels/'+source.name;f.Add3DModel(m)
def load(lib,name):
 key=name
 if key not in libraries:
  f=p.FootprintLoad(str(lib),name);assert f,name
  f.SetOrientationDegrees(0);f.SetPosition(v(0,0));model_local(f)
  f.SetFPID(p.LIB_ID('Calibrator',key));p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Calibrator.pretty'),f)
  libraries[key]=True
 return p.FootprintLoad(str(D/'Calibrator.pretty'),key)
def std(lib,name):return load('/usr/share/kicad/footprints/'+lib+'.pretty',name)
def add(ref,val,f,pins,x,y,angle=0,lcsc='',mpn='',kind='ic',types=None,names=None,bom=True):
 f.SetFPID(p.LIB_ID('Calibrator',str(f.GetFPID().GetLibItemName())));f.SetReference(ref);f.SetValue(val);f.SetPosition(v(x,y));f.SetOrientationDegrees(angle)
 f.SetPath(p.KIID_PATH('/'+uid('root')+'/'+uid(ref)))
 f.SetAttributes(p.FP_SMD if all(a.GetAttribute()!=p.PAD_ATTRIB_PTH for a in f.Pads()) else p.FP_THROUGH_HOLE)
 if not bom:f.SetAttributes(f.GetAttributes()|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
 for pad in f.Pads():
  n=pins.get(pad.GetNumber());
  if n:pad.SetNet(net(n))
 f.Reference().SetTextSize(v(.8,.8));f.Reference().SetTextThickness(mm(.12));f.Reference().SetPosition(v(x,y-4));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
 f.Reference().SetVisible(kind not in ['r','c','led'])
 f.Value().SetVisible(False)
 for g in list(f.GraphicalItems()):
  if hasattr(g,"SetVisible"):g.SetVisible(False)

 for key,value in [('LCSC',lcsc),('MPN',mpn or val)]:
  f.SetField(key,value);f.GetField(key).SetVisible(False)
 board.Add(f);footprints[ref]=f
 parts[ref]={'value':val,'mpn':mpn or val,'lcsc':lcsc,'footprint':'Calibrator:'+str(f.GetFPID().GetLibItemName()),'pins':pins,'kind':kind,'types':types or {},'names':names or {},'bom':bom,'position':[x,y,angle]}
 return f
def resistor(ref,value,a,b,x,y,angle=0,lcsc='C21190'):
 return add(ref,value,std('Resistor_SMD','R_0603_1608Metric'),{'1':a,'2':b},x,y,angle,lcsc,kind='r')
def capacitor(ref,value,a,b,x,y,angle=0,lcsc='C14663'):
 return add(ref,value,std('Capacitor_SMD','C_0603_1608Metric'),{'1':a,'2':b},x,y,angle,lcsc,kind='c')
def led(ref,a,k,x,y,label='',red=False):
 f=add(ref,'RED' if red else 'GREEN',std('LED_SMD','LED_0603_1608Metric'),{'1':k,'2':a},x,y,180,'C2286' if red else 'C965805','KT-0603R' if red else 'XL-1608SYGC-06',kind='led')
 if label:text(label,x+2,y,.85,left=True)
 return f
def text(s,x,y,size=1,left=False,layer=p.F_SilkS):
 t=p.PCB_TEXT(board);t.SetText(s);t.SetPosition(v(x,y));t.SetTextSize(v(size,size));t.SetTextThickness(mm(.12 if size<1 else .15));t.SetLayer(layer)
 if left:t.SetHorizJustify(p.GR_TEXT_H_ALIGN_LEFT)
 board.Add(t)
def line(a,b,layer=p.Edge_Cuts,width=.05):
 t=p.PCB_SHAPE();t.SetShape(p.SHAPE_T_SEGMENT);t.SetStart(v(*a));t.SetEnd(v(*b));t.SetLayer(layer);t.SetWidth(mm(width));board.Add(t)
def route(n,pts,layer=p.F_Cu,width=.2):
 for a,b in zip(pts,pts[1:]):
  if a==b:continue
  t=p.PCB_TRACK(board);t.SetStart(v(*a));t.SetEnd(v(*b));t.SetWidth(mm(width));t.SetLayer(layer);t.SetNet(net(n));board.Add(t)
def via(n,x,y):
 t=p.PCB_VIA(board);t.SetPosition(v(x,y));t.SetWidth(mm(.5));t.SetDrill(mm(.25));t.SetViaType(p.VIATYPE_THROUGH);t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetNet(net(n));board.Add(t)
def padxy(ref,num):
 pad=next(a for a in footprints[ref].Pads() if a.GetNumber()==str(num));return tuple(p.ToMM(z) for z in [pad.GetPosition().x,pad.GetPosition().y])
# Reuse the ordered carrier's RENNUMBERED mating footprints byte-for-byte in geometry.
C=R/'boards/programming-carrier'
contract=json.loads((C/'docs/circuit.json').read_text())
# Sixteen switch channels; remaining clock-capable pin reserved for PPS.
display_contacts=[2,4,5,6,7,10,11,12,14,15,16,17,19,20,21,24]
display_signals=[contract['J2']['pins'][str(n)] for n in display_contacts]
used_esp={'VIN_5V','GND','USB_D+','USB_D-','ESP_EN','ESP_GPIO0_BOOT','ESP_GPIO43_TXD','ESP_GPIO44_RXD','ESP_GPIO38','ESP_GPIO21'}
used_fpga={'GND',*display_signals,'FPGA_IOT_46B_G0','FPGA_IOT_50B'}
for ref,y in [('J1',44),('J2',69)]:
 c=contract[ref];pins={k:(n if n in (used_esp if ref=='J1' else used_fpga) else None) for k,n in c['pins'].items()}
 f=load(C/'Carrier.pretty',ref+'_Module_v1_Mate')
 # Models in this library are project relative to the carrier.
 f.Models().clear()
 original=p.FootprintLoad(str(C/'Carrier.pretty'),ref+'_Module_v1_Mate')
 for model in original.Models():
  source=C/model.m_Filename.replace('${KIPRJMOD}/','')
  if source.exists():shutil.copy2(source,D/'3dmodels'/source.name);model.m_Filename='${KIPRJMOD}/3dmodels/'+source.name;f.Add3DModel(model)
 add(ref,c['value'],f,pins,155,y,lcsc=c['lcsc'],mpn=c['mpn'],kind='connector',names=c['pins'])
 footprints[ref].Reference().SetPosition(v(168,y))
for ref,x,y in [('H1',155,56.5),('H2',24,14),('H3',196,14),('H4',24,106),('H5',196,106)]:
 add(ref,'M3',std('MountingHole','MountingHole_3.2mm_M3'),{},x,y,kind='hole',bom=False)
for a,z in [((20,10),(200,10)),((200,10),(200,110)),((200,110),(20,110)),((20,110),(20,10))]:line(a,z)
for a,z in [((145,29.7),(165,29.7)),((165,29.7),(165,74.7)),((165,74.7),(145,74.7)),((145,74.7),(145,29.7))]:line(a,z,p.F_SilkS,.12)
text('MODULE v1',155,52,.9);text('2.0 mm spacer',155,61,.8)
# Power is externally supplied; USB VBUS only feeds the ESD clamp, preventing backfeed/inrush.
usbp={'A1':'GND','B12':'GND','A12':'GND','B1':'GND','A4':'USB_VBUS','B9':'USB_VBUS','A9':'USB_VBUS','B4':'USB_VBUS','A5':'CC1','B5':'CC2','A6':'USB_D+','B6':'USB_D+','A7':'USB_D-','B7':'USB_D-','A8':None,'B8':None,'S1':'GND'}
add('J3','USB-C DATA',std('Connector_USB','USB_C_Receptacle_HRO_TYPE-C-31-M-12'),usbp,155,12.8,180,'C165948','TYPE-C-31-M-12',kind='connector')
add('U1','USBLC6-2SC6',std('Package_TO_SOT_SMD','SOT-23-6'),{'1':'USB_D+','2':'GND','3':'USB_D-','4':'USB_D-','5':'USB_VBUS','6':'USB_D+'},155,21,90,'C7519',names={'1':'IO1','2':'GND','3':'IO2','4':'IO2','5':'VBUS','6':'IO1'})
resistor('R1','5.1k','CC1','GND',148,17,90,'C23186');resistor('R2','5.1k','CC2','GND',162,17,90,'C23186')
capacitor('C1','100nF','USB_VBUS','GND',160,24)
# Two-wire input terminal footprint: 5.08 pitch; verify body against supplier drawing before release.
add('J4','5V INPUT',load(D/'Calibrator.pretty','KF128_5_08_2P'),{'1':'VIN_5V','2':'GND'},180,25,180,'C474952','KF128-5.08-2P-AA',kind='connector')
text('5V REGULATED / 1A',182,35,.9);text('+    GND',178,30,.8)
for ref,x,y,rail in [('U2',181,42,'+3V3_LOGIC'),('U5',179,85,'+3V3_GPS')]:
 add(ref,'AP2112K-3.3',std('Package_TO_SOT_SMD','SOT-23-5'),{'1':'VIN_5V','2':'GND','3':'VIN_5V','4':None,'5':rail},x,y,lcsc='C51118',mpn='AP2112K-3.3TRG1',names={'1':'VIN','2':'GND','3':'EN','4':'NC','5':'VOUT'},types={'1':'power_in','2':'power_in','3':'input','4':'no_connect','5':'power_out'})
 capacitor('C2' if ref=='U2' else 'C6','4.7uF','VIN_5V','GND',x-4,y,90,'C19666')
 capacitor('C3' if ref=='U2' else 'C7','4.7uF',rail,'GND',x+4,y,90,'C19666')
resistor('R3','2.2k','VIN_5V','POWER_LED',177,49,lcsc='C4190');led('D1','POWER_LED','GND',181,49,'POWER')
add('SW1','BOOT / RUN',std('Button_Switch_SMD','SW_SPDT_CK_JS102011SAQN'),{'1':'GND','2':'ESP_GPIO0_BOOT','3':None},181,61,0,'C221660','JS102011SAQN',kind='switch')
add('SW2','RESET',std('Button_Switch_SMD','SW_SPST_TL3342'),{'1':'GND','2':'ESP_EN'},181,73,0,'C2886898','TL3342F160QG',kind='switch')
resistor('R4','100k','ESP_GPIO0_BOOT','+3V3_LOGIC',174,58,lcsc='C25803')
text('BOOT / RUN',181,55,.8);text('RESET',181,78,.8)
# Four identical optical rows. Each LED gets its own 1% resistor.
# Identical branch geometry and a low-resistance 5V distribution plane control supply droop.
channels=[]
for col in range(16):
 x=32+6*col;bit=15-col;drain=f'LED_K{bit}';gate=f'GATE{bit}';drive=f'DRIVE{bit}'
 add('Q'+str(col+1),'AO3400A',std('Package_TO_SOT_SMD','SOT-23'),{'1':gate,'2':'GND','3':drain},x,38,270,'C20917','AO3400A',kind='mosfet',names={'1':'G','2':'S','3':'D'})
 resistor('R'+str(100+col),'100R',drive,gate,x,33,270,'C22775')
 resistor('R'+str(120+col),'100k',gate,'GND',x+2.6,36,90,'C25803')
 for row in range(4):
  idx=row*16+col;yy=48+12*row;an=f'LED_A{idx}';rr='R'+str(10+idx);dd='D'+str(10+idx)
  resistor(rr,'470R 1%', 'VIN_5V',an,x,yy+4,90,'C114669')
  add(dd,'BLUE',std('LED_SMD','LED_1206_3216Metric'),{'1':drain,'2':an},x,yy,270,'C28310438','YLED1206B',kind='led')
 channels.append({'bit':bit,'column':col,'signal':display_signals[col],'module_contact':display_contacts[col],'gate':gate,'drive':drive,'drain':drain,'mosfet':'Q'+str(col+1)})
 text(str(bit),x,43,.85)
 # Every column has a small bypass capacitor at the switch and bulk at the far end.
 capacitor('C'+str(20+col),'100nF','VIN_5V','GND',x+2.5,40.5,90,lcsc='C14663')
 add('C'+str(40+col),'10uF',std('Capacitor_SMD','C_0805_2012Metric'),{'1':'VIN_5V','2':'GND'},x,94,lcsc='C15850',mpn='CL21A106KAYNNNE',kind='c')
for row in range(4):text('ROW '+str(row),24.5,48+12*row,.8)
# Two strong 3.3V gate buffers, each bypassed at VCC. Gates held off during FPGA configuration.
for bank,x in [(0,57),(1,105)]:
 pins={'1':'GND','19':'GND','10':'GND','20':'+3V3_LOGIC'};names={'1':'~OE1','19':'~OE2','10':'GND','20':'VCC'};types={'1':'input','19':'input','10':'power_in','20':'power_in'}
 for k in range(8):
  col=bank*8+k;ch=channels[col];pins[str(k+2)]=ch['signal'];pins[str(18-k)]=ch['drive'];names[str(k+2)]='A'+str(k);names[str(18-k)]='Y'+str(k);types[str(k+2)]='input';types[str(18-k)]='output'
  resistor('R'+str(140+col),'100k',ch['signal'],'GND',34+col*6,15,90,'C25803')
 add('U'+str(3+bank),'SN74LVC541APWR',std('Package_SO','TSSOP-20_4.4x6.5mm_P0.65mm'),pins,x,24,90,'C113281','SN74LVC541APWR',names=names,types=types)
 capacitor('C'+str(4+bank),'100nF','+3V3_LOGIC','GND',x+5.5,24,90)
# GNSS: UART from ESP32, PPS to both processors; trigger to FPGA and receiver EXTINT.
gpspins={'1':'GND','2':'ESP_GPIO44_RXD','3':'ESP_GPIO43_TXD','4':'GPS_PPS','5':'TRIGGER_3V3','6':'+3V3_GPS','7':'+3V3_GPS','8':'+3V3_GPS','9':None,'10':'GND','11':'GNSS_RF','12':'GND','13':None,'14':None,'15':None,'16':None,'17':None,'18':None}
gpsnames=dict(zip(map(str,range(1,19)),['GND','TXD','RXD','TIMEPULSE','EXTINT','V_BCKP','V_IO','VCC','RESET_N','GND','RF_IN','GND','LNA_EN','VCC_RF','RESERVED','RESERVED','SDA','SCL']))
add('U6','MAX-M10S-00B-01',std('RF_GPS','ublox_MAX'),gpspins,187,96,0,'C24834155','MAX-M10S-00B-01',names=gpsnames)
capacitor('C8','100nF','+3V3_GPS','GND',179,95,90)
capacitor('C9','4.7uF','+3V3_GPS','GND',179,99,90,'C19666')
# GNSS coax: U.FL pigtail to an external antenna; no Wi-Fi antenna circuitry on this carrier.
add('J5','GNSS ANTENNA',std('Connector_Coaxial','U.FL_Hirose_U.FL-R-SMT-1_Vertical'),{'1':'GNSS_RF','2':'GND'},195,98,0,'C88373','U.FL-R-SMT-1(10)',kind='connector')
add('L1','27nH',std('Inductor_SMD','L_0402_1005Metric'),{'1':'GNSS_RF','2':'ANT_BIAS'},195,93,90,'C12669','LQG15HS27NJ02D',kind='l')
add('R5','10R 0.25W',std('Resistor_SMD','R_1206_3216Metric'),{'1':'ANT_PWR','2':'ANT_BIAS'},190,86,0,'C17903','1206W4F100JT5E',kind='r')
capacitor('C10','10nF','ANT_BIAS','GND',195,89,0,'C1589')
# Use clock input G0 for PPS. Small series resistors separate destinations and aid probing.
resistor('R6','100R','GPS_PPS','FPGA_IOT_46B_G0',172,92,lcsc='C22775')
resistor('R7','100R','GPS_PPS','ESP_GPIO38',172,96,lcsc='C22775')
# External trigger is 3.3/5V logic input, not a 50-ohm terminated analog input.
add('J6','TRIGGER / PPS',std('Connector_PinHeader_2.54mm','PinHeader_1x04_P2.54mm_Vertical'),{'1':'GND','2':'TRIGGER_IN','3':'GND','4':'PPS_MON'},142,100,90,kind='connector',bom=False)
add('U7','SN74LVC1G17DBVR',std('Package_TO_SOT_SMD','SOT-23-5'),{'1':None,'2':'TRIGGER_LIMIT','3':'GND','4':'TRIGGER_3V3','5':'+3V3_LOGIC'},158,94,lcsc='C7836',names={'1':'NC','2':'A','3':'GND','4':'Y','5':'VCC'})
resistor('R8','1k','TRIGGER_IN','TRIGGER_LIMIT',153,94)
resistor('R9','100k','TRIGGER_LIMIT','GND',153,98,lcsc='C25803')
resistor('R80','100R','TRIGGER_3V3','FPGA_IOT_50B',164,98,lcsc='C22775')
resistor('R81','100R','TRIGGER_3V3','ESP_GPIO21',164,101,lcsc='C22775')
resistor('R82','100R','GPS_PPS','PPS_MON',161,105,lcsc='C22775')
capacitor('C11','100nF','+3V3_LOGIC','GND',158,90)
for i in range(4):add('C'+str(60+i),'10uF',std('Capacitor_SMD','C_0805_2012Metric'),{'1':'VIN_5V','2':'GND'},174+i*5,39,lcsc='C15850',mpn='CL21A106KAYNNNE',kind='c')
text('GPS TIME / OPTICAL CALIBRATOR',80,101,1.5)
text('4 x 16 bits | MSB LEFT | 1/65536 s = 15.259 us',80,104,.95)
text('5V EXTERNAL POWER REQUIRED | USB DATA ONLY',113,108,.8)
text('G  TRIG  G  PPS',145,104,.8);text('GNSS',192,104,.8)
# Current-limit active antenna supply independently of the receiver's VCC_RF output.
add('U8','TPS2553DBVR',std('Package_TO_SOT_SMD','SOT-23-6'),{'1':'+3V3_GPS','2':'GND','3':'+3V3_GPS','4':None,'5':'+3V3_GPS','6':'ANT_PWR'},191,78,lcsc='C55266',mpn='TPS2553DBVR',names={'1':'IN','2':'GND','3':'EN','4':'~FAULT','5':'ILIM','6':'OUT'},types={'1':'power_in','2':'power_in','3':'input','4':'open_collector','5':'passive','6':'power_out'})
capacitor('C12','100nF','+3V3_GPS','GND',187,78)

# Normalize passive exact MPN metadata from the already-purchased carrier where possible.
lookup={c['lcsc']:c['mpn'] for c in contract.values() if c['lcsc']}
lookup.update({'C114669':'RC0603FR-07470RL','C22775':'0603WAF1000T5E','C25803':'0603WAF1003T5E','C1589':'CL10B103KB8NNNC','C14663':'CC0603KRX7R9BB104','C19666':'CL10A475KO8NNNC'})
for ref,c in parts.items():
 if c['lcsc'] in lookup:c['mpn']=lookup[c['lcsc']];footprints[ref].SetField('MPN',c['mpn']);footprints[ref].GetField('MPN').SetVisible(False)
(D/'docs/circuit.json').write_text(json.dumps(parts,indent=2)+'\n');(D/'docs/display-map.json').write_text(json.dumps(channels,indent=2)+'\n')
for kind in ['fp','sym']:
 uri='Calibrator.pretty' if kind=='fp' else 'Calibrator.kicad_sym'
 (D/(kind+'-lib-table')).write_text(f'({kind}_lib_table (lib (name "Calibrator") (type "KiCad") (uri "${{KIPRJMOD}}/{uri}") (options "") (descr "Calibrator local libraries")))\n')
p.SaveBoard(str(D/'calibrator.kicad_pcb'),board)
pro=json.loads((C/'carrier.kicad_pro').read_text());pro['meta']['filename']='calibrator.kicad_pro';pro['board']['design_settings']['drc_exclusions']=[]
(D/'calibrator.kicad_pro').write_text(json.dumps(pro,indent=2)+'\n')
print('Created',len(parts),'parts /',len(nets),'nets')
