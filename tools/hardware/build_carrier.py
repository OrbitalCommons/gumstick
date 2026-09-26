#!/usr/bin/env python3
"""Programming carrier sources. Frozen v1 contact geometry is the interface authority.
Run with system Python (KiCad pcbnew). Does not modify the daughterboard.
"""
from pathlib import Path
import pcbnew as p, json,csv,uuid,re,shutil,math
R=Path(__file__).resolve().parents[2]; D=R/'boards/programming-carrier'; M=R/'boards/esp32-fpga-module'
for d in ['Carrier.pretty','docs','3dmodels','fab/checks']: (D/d).mkdir(parents=True,exist_ok=True)
uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,'bp-carrier-v1/'+s))
q=lambda s:json.dumps(str(s))
mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
board=p.BOARD();board.SetCopperLayerCount(4)
board.GetDesignSettings().SetAuxOrigin(v(20,165));board.GetDesignSettings().SetGridOrigin(v(20,20))
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
  f.SetFPID(p.LIB_ID('Carrier',key));p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Carrier.pretty'),f)
  libraries[key]=True
 return p.FootprintLoad(str(D/'Carrier.pretty'),key)
def std(lib,name):return load('/usr/share/kicad/footprints/'+lib+'.pretty',name)
def add(ref,val,f,pins,x,y,angle=0,lcsc='',mpn='',kind='ic',types=None,names=None,bom=True):
 f.SetFPID(p.LIB_ID('Carrier',str(f.GetFPID().GetLibItemName())));f.SetReference(ref);f.SetValue(val);f.SetPosition(v(x,y));f.SetOrientationDegrees(angle)
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
 parts[ref]={'value':val,'mpn':mpn or val,'lcsc':lcsc,'footprint':'Carrier:'+str(f.GetFPID().GetLibItemName()),'pins':pins,'kind':kind,'types':types or {},'names':names or {},'bom':bom,'position':[x,y,angle]}
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
# Contact-by-contact mapping uses actual v1 B.Cu pad locations, not its inconsistent numbering convention.
module=p.LoadBoard(str(M/'module.kicad_pcb'));mapping=[];pinout={}
for c,y,mate in [('J1',46,'J2_DF40C_40DP'),('J2',71,'J1_DF40C_40DS_2mm')]:
 mf=module.FindFootprintByReference(c);f=load(M/'Module.pretty',mate)
 f.SetPosition(v(0,0));f.SetOrientationDegrees(0)
 mpads={a.GetNumber():a for a in mf.Pads() if a.GetNumber()}
 pins={};renumber=[]
 for pad in f.Pads():
  if not pad.GetNumber():continue
  x0=p.ToMM(pad.GetPosition().x);y0=p.ToMM(pad.GetPosition().y)
  key=min(mpads,key=lambda k:abs(p.ToMM(mpads[k].GetPosition().x)-110-x0)+abs(p.ToMM(mpads[k].GetPosition().y)-p.ToMM(mf.GetPosition().y)-y0))
  target=mpads[key];assert abs(p.ToMM(target.GetPosition().x)-110-x0)<.001
  assert abs(p.ToMM(target.GetPosition().y)-p.ToMM(mf.GetPosition().y)-y0)<.1
  name=target.GetNetname().lstrip('/');pins[key]=name
  mapping.append({'connector':c,'module_pin':key,'carrier_original_pad':pad.GetNumber(),'x':100+x0,'y':y+y0,'signal':name})
  renumber.append((pad,key))
 for pad,key in renumber:pad.SetNumber(key)
 newname=c+'_Module_v1_Mate';f.SetFPID(p.LIB_ID('Carrier',newname));p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Carrier.pretty'),f)
 f=p.FootprintLoad(str(D/'Carrier.pretty'),newname)
 val='DF40C-40DP-0.4V(51)' if c=='J1' else 'DF40C(2.0)-40DS-0.4V(51)'
 add(c,val,f,pins,100,y,lcsc='C424643' if c=='J1' else 'C597934',kind='connector',names=pins)
 pinout[c]=pins
(D/'docs/contact-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
# Reusable physical module interface: both mated connectors plus aligned M3 hole and module envelope.
combo=p.FOOTPRINT(board);combo.SetFPID(p.LIB_ID('Carrier','ESP32_FPGA_Module_v1_Interface'));combo.SetReference('M**');combo.SetValue('ESP32_FPGA_Module_v1_Interface')
for c in ['J1','J2']:
 f=footprints[c]
 for pad in f.Pads():
  new=p.PAD(combo);new.SetAttribute(pad.GetAttribute());new.SetShape(pad.GetShape());new.SetSize(pad.GetSize());new.SetLayerSet(pad.GetLayerSet());new.SetPosition(v(p.ToMM(pad.GetPosition().x)-100,p.ToMM(pad.GetPosition().y)-58.5));new.SetNumber(c+'_'+pad.GetNumber() if pad.GetNumber() else '');combo.Add(new)
h=p.PAD(combo);h.SetAttribute(p.PAD_ATTRIB_NPTH);h.SetShape(p.PAD_SHAPE_CIRCLE);h.SetSize(v(3.2,3.2));h.SetDrillSize(v(3.2,3.2));h.SetLayerSet(p.LSET.AllCuMask());h.SetPosition(v(0,0));combo.Add(h)
for a,b in [((-10,-28.25),(10,-28.25)),((10,-28.25),(10,16.75)),((10,16.75),(-10,16.75)),((-10,16.75),(-10,-28.25))]:
 g=p.PCB_SHAPE();g.SetShape(p.SHAPE_T_SEGMENT);g.SetStart(v(*a));g.SetEnd(v(*b));g.SetLayer(p.F_Fab);g.SetWidth(mm(.1));combo.Add(g)
p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Carrier.pretty'),combo)
# Mechanics and outline, daughter bottom at 2mm above carrier.
for ref,x,y in [('H1',100,58.5),('H2',24,24),('H3',176,24),('H4',24,161),('H5',176,161)]:
 add(ref,'M3',std('MountingHole','MountingHole_3.2mm_M3'),{},x,y,kind='hole',bom=False)
for a,b in [((20,20),(180,20)),((180,20),(180,165)),((180,165),(20,165)),((20,165),(20,20))]:line(a,b)
for a,b in [((90,30.25),(110,30.25)),((110,30.25),(110,75.25)),((110,75.25),(90,75.25)),((90,75.25),(90,30.25))]:line(a,b,p.F_SilkS,.15)
text('MODULE v1',100,53,.9);text('2.0 mm spacer',100,63,.8)
# USB and carrier power.
usbp={'A1':'GND','B12':'GND','A12':'GND','B1':'GND','A4':'VBUS','B9':'VBUS','A9':'VBUS','B4':'VBUS','A5':'CC1','B5':'CC2','A6':'USB_D+','B6':'USB_D+','A7':'USB_D-','B7':'USB_D-','A8':None,'B8':None,'S1':'GND'}
add('J3','USB-C USB2',std('Connector_USB','USB_C_Receptacle_HRO_TYPE-C-31-M-12'),usbp,100,22.8,180,'C165948','TYPE-C-31-M-12',kind='connector')
add('U1','AP2112K-3.3',std('Package_TO_SOT_SMD','SOT-23-5'),{'1':'VIN_5V','2':'GND','3':'VIN_5V','4':None,'5':'+3V3_TEST'},80,31,lcsc='C51118',mpn='AP2112K-3.3TRG1',names={'1':'VIN','2':'GND','3':'EN','4':'NC','5':'VOUT'},types={'1':'power_in','2':'power_in','3':'input','4':'no_connect','5':'power_out'})
add('U2','USBLC6-2SC6',std('Package_TO_SOT_SMD','SOT-23-6'),{'1':'USB_D+','2':'GND','3':'USB_D-','4':'USB_D-','5':'VBUS','6':'USB_D+'},100,31,90,'C7519',names={'1':'IO1','2':'GND','3':'IO2','4':'IO2','5':'VBUS','6':'IO1'})
add('F1','500mA PTC',std('Fuse','Fuse_1206_3216Metric'),{'1':'VBUS','2':'VIN_5V'},87,27,0,'C151162','1206L050/15YR',kind='r')
resistor('R1','5.1kR','CC1','GND',93,30,90,'C23186');resistor('R2','5.1kR','CC2','GND',107,30,90,'C23186')
capacitor('C1','4.7uF','VIN_5V','GND',76,31,90,'C19666');capacitor('C2','4.7uF','+3V3_TEST','GND',84,31,90,'C19666');capacitor('C3','100nF','VBUS','GND',104,31,90)
resistor('R3','2.2kR','VIN_5V','P5_LED',70,28,0,'C4190');led('D1','P5_LED','GND',73,28,'5V')
resistor('R4','1kR','+3V3_TEST','P3_LED',70,35);led('D2','P3_LED','GND',73,35,'3V3 TEST')
add('SW1','BOOT / RUN',std('Button_Switch_SMD','SW_SPDT_CK_JS102011SAQN'),{'1':'GND','2':'ESP_GPIO0_BOOT','3':None},65,47,0,'C221660','JS102011SAQN',kind='switch')
for ref,signal,x,y,label in [('SW2','ESP_EN',65,60,'RESET'),('SW3','GPIO46_TEST',130,35,'GPIO46 INPUT')]:
 add(ref,label,std('Button_Switch_SMD','SW_SPST_TL3342'),{'1':'GND' if ref=='SW2' else '+3V3_TEST','2':signal},x,y,0,'C2886898','TL3342F160QG',kind='switch');text(label,x,y+5.5,.9)
resistor('R5','1kR','GPIO46_TEST','ESP_GPIO46',135,41)
text('BOOT       RUN',65,43,.85);text('FLASH: BOOT, tap RESET',53,70,.9,left=True);text('Then RUN, tap RESET',53,72,.9,left=True)
# LEDs: eight regular groups + 3 dedicated sink-driven RGB monitor channels.
esp=[n for n in pinout['J1'].values() if n.startswith('ESP_')]
esp=sorted(set(esp),key=lambda s:(s!='ESP_EN',int(re.search(r'GPIO(\d+)',s).group(1)) if 'GPIO' in s else -1))
fpga=sorted({n for n in pinout['J2'].values() if n.startswith('FPGA_') and 'RGB' not in n},key=lambda s:(0 if 'IOB' in s else 1,int(re.search(r'_(\d+)',s).group(1))))
groups=[('ESP',esp[i:i+8],x,y) for i,x,y in [(0,32,92),(8,69,92),(16,32,133),(24,69,133)]]
groups += [('FPGA',fpga[i:i+8],x,y) for i,x,y in [(0,116,92),(8,153,92),(16,116,133),(24,153,133)]]
groups += [('RGB',['FPGA_RGB0','FPGA_RGB1','FPGA_RGB2'],142,57)]
channels=[]
for bi,(bank,signals,x,y) in enumerate(groups):
 ref='U'+str(3+bi);pins={'1':'GND','19':'GND','10':'GND','20':'+3V3_TEST'};names={'1':'~{OE1}','19':'~{OE2}','10':'GND','20':'VCC'};types={'1':'input','19':'input','10':'power_in','20':'power_in'}
 for k in range(8):
  n=signals[k] if k<len(signals) else None;out='BUF_'+n if n else None
  pins[str(k+2)]=n or 'GND';pins[str(18-k)]=out;names[str(k+2)]='A'+str(k+1);names[str(18-k)]='Y'+str(k+1);types[str(k+2)]='input';types[str(18-k)]='tri_state'
 add(ref,'SN74LVC541APWR',std('Package_SO','TSSOP-20_4.4x6.5mm_P0.65mm'),pins,x,y,0,'C113281',names=names,types=types)
 capacitor('C'+str(10+bi),'100nF','+3V3_TEST','GND',x+3,y-5.5)
 text(bank+' '+str(bi%4+1) if bank!='RGB' else 'RGB (LOW = ON)',x+6,y-16,1)
 for k,n in enumerate(signals):
  idx=bi*8+k;yy=y-10.5+3*k;rr='R'+str(10+idx);rp='R'+str(110+idx);dd='D'+str(10+idx);active_low=bank=='RGB'
  resistor(rp,'100kR',n,'+3V3_TEST' if active_low or n=='ESP_GPIO0_BOOT' else 'GND',x-7,yy,0,'C25803')
  resistor(rr,'1kR',('+3V3_TEST' if active_low else 'BUF_'+n),'LED_'+n,x+9,yy)
  label=n.replace('ESP_','').replace('FPGA_','').replace('GPIO','IO')
  led(dd,'LED_'+n,'BUF_'+n if active_low else 'GND',x+13,yy,label,red=active_low)
  channels.append({'signal':n,'buffer':ref,'input':k+2,'output':18-k,'led':dd,'resistor':rr,'bias':rp,'active_low':active_low,'bank':bank})
# A usable test fixture can also probe the inputs on exposed labeled LED-bank pull resistor pads.
text('ESP32 + FPGA / PROGRAM & GPIO TEST',100,156,1.5)
text('Power OFF before mating   |   Green: HIGH   Red RGB: LOW   |   GPIO46 input only',100,159,.9)
text('USB programming: BOOT + RESET, then RUN + RESET',100,162,.9)
# Save sources (routing is a separate step, so rerunning does not silently clobber routed production).
(D/'docs/circuit.json').write_text(json.dumps(parts,indent=2)+'\n');(D/'docs/led-map.json').write_text(json.dumps(channels,indent=2)+'\n')
(D/'fp-lib-table').write_text('(fp_lib_table (lib (name "Carrier") (type "KiCad") (uri "${KIPRJMOD}/Carrier.pretty") (options "") (descr "Self-contained carrier libraries")))\n')
(D/'sym-lib-table').write_text('(sym_lib_table (lib (name "Carrier") (type "KiCad") (uri "${KIPRJMOD}/Carrier.kicad_sym") (options "") (descr "Carrier and reusable v1 interface")))\n')
p.SaveBoard(str(D/'carrier.kicad_pcb'),board)
print('Created',len(parts),'parts,',len(channels),'indicators,',len(nets),'nets')
