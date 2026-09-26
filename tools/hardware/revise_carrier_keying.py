#!/usr/bin/env python3
"""One-time migration to a complementary horizontal DF40 pair and debug pads.
Hirose plug drawing EDC-311351-00: 0.4 pitch, 0.23x0.66 pads,
2.71 row-center spacing, 0.35x0.66 mounting tabs at x=+-4.275.
"""
from pathlib import Path
import pcbnew as p,json,uuid,csv
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module'
b=p.LoadBoard(str(D/'module.kicad_pcb'));parts=json.loads((D/'docs/module-connectivity.json').read_text())
assert parts['J2']['value']!='DF40C-40DP-0.4V(51)','Migration already applied'
pt=lambda x,y:p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def layers(*ls):
 out=p.LSET()
 for l in ls:out.AddLayer(l)
 return out
f=p.FOOTPRINT(b);f.SetFPID(p.LIB_ID('Module','J2_DF40C_40DP'));f.SetReference('J2');f.SetValue('DF40C-40DP-0.4V(51)');f.SetAttributes(p.FP_SMD)
for row in range(2):
 for i in range(20):
  a=p.PAD(f);a.SetNumber(str(i+1 if row==0 else 40-i));a.SetAttribute(p.PAD_ATTRIB_SMD);a.SetShape(p.PAD_SHAPE_RECT);a.SetSize(pt(.23,.66));a.SetPosition(pt(-3.8+.4*i,(-1 if row==0 else 1)*1.355));a.SetLayerSet(layers(p.F_Cu,p.F_Mask,p.F_Paste));f.Add(a)
for x in [-4.275,4.275]:
 for y in [-1.355,1.355]:
  a=p.PAD(f);a.SetNumber('');a.SetAttribute(p.PAD_ATTRIB_SMD);a.SetShape(p.PAD_SHAPE_RECT);a.SetSize(pt(.35,.66));a.SetPosition(pt(x,y));a.SetLayerSet(layers(p.F_Cu,p.F_Mask,p.F_Paste));f.Add(a)
for layer,x,y in [(p.F_Fab,4.76,1.485),(p.F_CrtYd,5.01,1.94)]:
 for a,e in [((-x,-y),(x,-y)),((x,-y),(x,y)),((x,y),(-x,y)),((-x,y),(-x,-y))]:
  g=p.PCB_SHAPE(f);g.SetShape(p.SHAPE_T_SEGMENT);g.SetStart(pt(*a));g.SetEnd(pt(*e));g.SetLayer(layer);g.SetWidth(p.FromMM(.05));f.Add(g)
f.Reference().SetPosition(pt(0,-2.4));f.Reference().SetTextSize(pt(.7,.7));f.Reference().SetTextThickness(p.FromMM(.12));f.Value().SetVisible(False)
m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/3dmodels/DF40C_40DP.step';f.Add3DModel(m)
p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Module.pretty'),f)
old=next(x for x in b.GetFootprints() if x.GetReference()=='J2');f.SetUuid(old.m_Uuid);f.SetPath(old.GetPath());b.Remove(old);b.Add(f);f.SetPosition(pt(110,140));f.Flip(f.GetPosition(),True);f.SetOrientationDegrees(180)
parts['J2'].update(value='DF40C-40DP-0.4V(51)',mpn='DF40C-40DP-0.4V(51)',footprint='Module:J2_DF40C_40DP',lcsc='C424643',manufacturer='Hirose',sourcing_url='https://www.hirose.com/en/product/p/CL0684-4013-7-51',sourcing_status='Manufacturer footprint and mate verified; confirm distributor stock before order')
for a in f.Pads():
 if a.GetNumber():
  n=parts['J2']['pins'][a.GetNumber()]['net'];a.SetNet(b.FindNet(n if n in ['GND','+3.3V'] else '/'+n))
# Remove the legacy application-specific shared connection entirely.
for ref,num in [('U1','42'),('U2','44'),('J1','16')]:
 parts[ref]['pins'][num]['net']=None
 fp=next(x for x in b.GetFootprints() if x.GetReference()==ref)
 next(a for a in fp.Pads() if a.GetNumber()==num).SetNetCode(0)
for t in list(b.GetTracks()):
 if t.GetNetname()=='/SYNC_IO':b.RemoveNative(t)
# Debug pads: accessible from top, no solder paste or fitted component.
for ref,net,x,y in [('TP1','FPGA_CRESET_N',1,34.5),('TP2','FPGA_CDONE',17,35)]:
 fp=p.FOOTPRINT(b);fp.SetReference(ref);fp.SetValue(net);fp.SetFPID(p.LIB_ID('Module','TestPoint_0p8'));fp.SetAttributes(p.FP_SMD|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
 a=p.PAD(fp);a.SetNumber('1');a.SetAttribute(p.PAD_ATTRIB_SMD);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetSize(pt(.8,.8));a.SetLayerSet(layers(p.F_Cu,p.F_Mask));fp.Add(a)
 fp.Reference().SetPosition(pt(0,-.9));fp.Reference().SetTextSize(pt(.6,.6));fp.Reference().SetTextThickness(p.FromMM(.1));fp.Value().SetVisible(False)
 p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D/'Module.pretty'),fp)
 uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'gps-time-module/'+ref));fp.SetUuid(p.KIID(uid));fp.SetPath(p.KIID_PATH('/'+str(uuid.uuid5(uuid.NAMESPACE_URL,'gps-time-module/root'))+'/'+uid))
 b.Add(fp);fp.SetPosition(pt(100+x,100+y));a.SetNet(b.FindNet('/'+net));parts[ref]={'value':net,'footprint':'Module:TestPoint_0p8','uuid':uid,'pins':{'1':{'name':'1','type':'passive','net':net}}}
(D/'docs/module-connectivity.json').write_text(json.dumps(parts,indent=2)+'\n')
ov=json.loads((D/'docs/pinout-overrides.json').read_text());ov['J1']['16']=None;(D/'docs/pinout-overrides.json').write_text(json.dumps(ov,indent=2)+'\n')
rows=list(csv.DictReader((D/'docs/carrier-pinout.csv').open()))
for row in rows:
 if row['Connector']=='J1' and row['Pin']=='16':row.update(Signal='NC',**{'Direction / constraint':'Reserved; no connection on module'})
with (D/'docs/carrier-pinout.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
pl=json.loads((D/'docs/placement.json').read_text());pl['J2']=[10,40,0];pl['TP1']=[1,34.5,0];pl['TP2']=[17,35,0];(D/'docs/placement.json').write_text(json.dumps(pl,indent=2)+'\n')
p.SaveBoard(str(D/'module.kicad_pcb'),b)
