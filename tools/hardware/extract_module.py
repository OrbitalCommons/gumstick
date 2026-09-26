#!/usr/bin/env python3
"""Extract auditable module connectivity from the saved native reference netlist."""
from pathlib import Path
import xml.etree.ElementTree as E
import json,csv
ROOT=Path(__file__).resolve().parents[2]
r=E.parse(ROOT/'docs/hardware/original-netlist.xml').getroot()
cs={c.get('ref'):c for c in r.find('components')}
libs={p.get('part'):p for p in r.find('libparts')}
nets={}
for n in r.find('nets'):
 for p in n.findall('node'):
  nets[p.get('ref'),p.get('pin')]=None if n.get('name').startswith('unconnected-') else n.get('name')
eagle=json.loads((ROOT/'docs/hardware/eagle-pad-nets.json').read_text())
for (ref,pin),net in list(nets.items()):
 original=eagle.get(f'{ref}.{pin}')
 if original and not original.startswith('N$'):nets[ref,pin]=original
refs=['U1','U2','U5','U$1','L1','L2','L3','R3','R20','R22','R28','R29','C1','C2','C6','C7','C32','C33','C34','C35']+[f'C{i}' for i in range(37,51) if f'C{i}' in cs]+['C52']
# C47 is a core rail decoupler? All candidate two-terminal parts must belong to retained rails.
parts={}
rename={'U$1':'AE1','U5':'Y1'}
netrename={'ESP_38':'ESP_GPIO34','ESP_39':'ESP_GPIO35','GPS_RESET':'ESP_GPIO33','CPU_LED':'ESP_GPIO2','GPS-RX':'ESP_TXD','GPS-TX':'ESP_RXD','GPS-PPS':'PPS','Net-(C6-Pad1)':'XTAL_P_CRYSTAL','+5V':'VIN_5V'}
for ref in refs:
 c=cs[ref]; lp=libs[c.find('libsource').get('part')]
 pins={p.get('num'):{'name':p.get('name'),'type':p.get('type'),'net':netrename.get(nets.get((ref,p.get('num'))),nets.get((ref,p.get('num'))))} for p in lp.find('pins')}
 parts[rename.get(ref,ref)]={'source_ref':ref,'value':c.findtext('value'),'footprint':c.findtext('footprint'),'pins':pins}
p=parts['U1']['pins']
for i in [29,31,32,33,34,35,36]:p[str(i)]['net']=None
for pin,gpio in {6:1,8:3,9:4,10:5,11:6,12:7,13:8,21:15,22:16,23:17,24:18,28:21,43:39,44:40,46:41,47:42}.items():p[str(pin)]['net']=f'ESP_GPIO{gpio}'
p['50']['net']=None;p['55']['net']=None  # Internal reset pull-downs; no external straps.
parts['U1']['value']='ESP32-S2FH4';parts['U2']['value']='iCE40UP5K-SG48';parts['Y1']['value']='40MHz / CL10pF'
def add(ref,value,footprint,pins):
 parts[ref]={'value':value,'footprint':footprint,'pins':{str(i):{'name':name,'net':net,'type':typ} for i,name,net,typ in pins}}
def passive(ref,value,a,b,kind='R',footprint=None):
 fp=footprint or {'R':'Resistor_SMD:R_0402_1005Metric','C':'Capacitor_SMD:C_0603_1608Metric','L':'Inductor_SMD:L_0402_1005Metric'}[kind]
 add(ref,value,fp,[(1,'1',a,'passive'),(2,'2',b,'passive')])
add('U3','TPS62162DSGR','Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm',[(1,'PGND','GND','power_in'),(2,'VIN','VIN_5V','power_in'),(3,'EN','VIN_5V','input'),(4,'AGND','GND','power_in'),(5,'FB','GND','input'),(6,'VOS','+3.3V','input'),(7,'SW','BUCK_SW','power_out'),(8,'PG','PG_3V3','open_collector'),(9,'EP','GND','power_in')])
add('U4','TLV75512PDBVR','Package_TO_SOT_SMD:SOT-23-5',[(1,'IN','+3.3V','power_in'),(2,'GND','GND','power_in'),(3,'EN','+3.3V','input'),(4,'NC',None,'no_connect'),(5,'OUT','+1.2V','power_out')])
passive('L4','2.2uH / Isat >= 1.9A','BUCK_SW','+3.3V','L','Module:L_XFL3012_222MEC')
passive('C60','10uF / 10V','VIN_5V','GND','C','Capacitor_SMD:C_0805_2012Metric');passive('C61','22uF / 10V','+3.3V','GND','C','Capacitor_SMD:C_0805_2012Metric')
passive('C62','1uF / 6.3V','+3.3V','GND','C');passive('C63','1uF / 6.3V','+1.2V','GND','C');passive('R62','100kR','PG_3V3','+3.3V')
# Explicit carrier interface, provisional physical pin assignments pending footprint/mate review.
j1=['VIN_5V','VIN_5V','VIN_5V','VIN_5V','GND','GND','USB_D-','USB_D+','GND','GND','CHIP_PU','GPIO0','ESP_TXD','ESP_RXD','GND','PPS','ESP_GPIO1','ESP_GPIO2','ESP_GPIO3','ESP_GPIO4','GND','ESP_GPIO5','ESP_GPIO6','ESP_GPIO7','ESP_GPIO8','GND','ESP_GPIO15','ESP_GPIO16','ESP_GPIO17','ESP_GPIO18','GND','ESP_GPIO21','ESP_GPIO33','ESP_GPIO34','ESP_GPIO35','GND','ESP_GPIO39','ESP_GPIO40','ESP_GPIO41','ESP_GPIO42']
j2=['GND','HQ_OSC','GND','BIT0','BIT1','BIT2','BIT3','GND','BIT4','BIT5','BIT6','BIT7','GND','BIT8','BIT9','BIT10','BIT11','GND','BIT12','BIT13','BIT14','BIT15','GND','F2','F3','F4','F6','GND','F9','F10','F19','F20','GND','F23','F25','EXT_33','EXT_EN','RGB_0','RGB_1','RGB_2']
# Connector positions follow routing, not GPIO numbering (carrier pinout revision 2).
j1[19],j1[27]=j1[27],j1[19]
for ref,ns in [('J1',j1),('J2',j2)]:
 assert len(ns)==40
 add(ref,'DF40C(2.0)-40DS-0.4V(51)','Module:DF40C_40DS_2mm',[(i,str(i),n,'passive') for i,n in enumerate(ns,1)])
parts['J2']['value']='DF40C-40DP-0.4V(51)'
parts['J2']['footprint']='Module:J2_DF40C_40DP'
# Original passives use source footprints, resized only for bulk ceramic capacitors.
for ref,c in parts.items():
 if ref.startswith('C') and c['value'].startswith('10u'):c['footprint']='Capacitor_SMD:C_0603_1608Metric'
 if ref.startswith('R') and c['value'].endswith('k'):c['value']+='R'
 if ref=='R3':c['value']='0R'
from devboard_names import apply
name_changes=apply(parts)
j1=[name_changes.get(n,n) for n in j1];j2=[name_changes.get(n,n) for n in j2]
# Preserve the reviewed carrier-contact assignments when re-extracting sources.
override_path=ROOT/'boards/esp32-fpga-module/docs/pinout-overrides.json'
if override_path.exists():
 for ref,mapping in json.loads(override_path.read_text()).items():
  ns=j1 if ref=='J1' else j2
  for pin,net in mapping.items():
   parts[ref]['pins'][pin]['net']=net;ns[int(pin)-1]=net
# All extracted source pins are kept, even where carrier circuitry was deliberately removed.
out=ROOT/'boards/esp32-fpga-module/docs';out.mkdir(parents=True,exist_ok=True)
(out/'signal-name-map.json').write_text(json.dumps(name_changes,indent=2)+'\n')
(out/'module-connectivity.json').write_text(json.dumps(parts,indent=2)+'\n')
with (out/'carrier-pinout.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['Connector','Pin','Signal','Direction / constraint'])
 for ref,ns in [('J1',j1),('J2',j2)]:
  for i,n in enumerate(ns,1):w.writerow([ref,i,n,'5V input; all four VIN contacts required' if n=='VIN_5V' else 'Ground' if n=='GND' else '3.3V logic; no 5V tolerance' if not (n or '').startswith('USB') else 'USB 2.0 full speed differential pair'])
print(f'{len(parts)} components; {len(set(p["net"] for c in parts.values() for p in c["pins"].values())-{None})} nets')
