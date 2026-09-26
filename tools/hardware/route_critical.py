#!/usr/bin/env python3
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module';b=p.LoadBoard(str(D/'module.kicad_pcb'))
def xy(x,y):return p.VECTOR2I(p.FromMM(x+100),p.FromMM(y+100))
def pos(ref,num):
 pad=next(a for a in b.FindFootprintByReference(ref).Pads() if a.GetNumber()==str(num));return (p.ToMM(pad.GetPosition().x)-100,p.ToMM(pad.GetPosition().y)-100)
def line(net,pts,w=.15,layer=p.F_Cu):
 n=b.FindNet(net) or b.FindNet('/'+net)
 for a,c in zip(pts,pts[1:]):
  if a==c:continue
  t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*c));t.SetWidth(p.FromMM(w));t.SetLayer(layer);t.SetNet(n);b.Add(t)
def via(net,x,y):
 t=p.PCB_VIA(b);t.SetPosition(xy(x,y));t.SetWidth(p.FromMM(.4));t.SetDrill(p.FromMM(.2));t.SetViaType(p.VIATYPE_THROUGH);t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetNet(b.FindNet(net) or b.FindNet('/'+net));b.Add(t)
# Manual critical routes for the gumstick placement.
line('RF_IN',[pos('U1',2),(13.7,11.1),pos('L3',1)],.18)
line('RF_IN',[pos('C1',1),(13.7,11.1)],.18)
line('RF_ANT',[pos('L3',2),(12.2,7.6),(15,7.6),pos('AE1','P$2')],.18)
line('RF_ANT',[pos('L3',2),(pos('C2',1)[0],pos('L3',2)[1]),pos('C2',1)],.18)
line('GND',[pos('AE1','P$1'),(17.1,7.8),(17.7,7.8),(17.0,7.95)],.25);via('GND',17.0,7.95)
line('XTAL_P',[pos('U1',53),(15.85,14.1),(15.85,13.2),pos('R3',1)])
line('XTAL_P_CRYSTAL',[pos('R3',2),pos('Y1','IN/OUT')])
line('XTAL_P_CRYSTAL',[pos('R3',2),pos('C6',1)])
line('XTAL_N',[pos('U1',52),(15.7,14.5),(16,14.5),(16.5,15),(18,15),(18.45,15.45),pos('Y1','OUT/IN')])
line('XTAL_N',[pos('Y1','OUT/IN'),pos('C7',1)])
line('USB_D-',[pos('U1',25),(7.75,16.9),(7.625,17.025),(5.6,17.025),(5.475,16.9),(5.1,16.9)],.125)
line('USB_D+',[pos('U1',26),(6.0,17.3),(5.7,17.5)],.125)
via('USB_D-',5.1,16.9);via('USB_D+',5.7,17.5)
line('USB_D-',[(5.1,16.9),(5.1,13.2),(11.4,13.2),pos('J1',7)],.17,p.B_Cu)
line('USB_D+',[(5.7,17.5),(5.7,17.25),(5.6,17.15),(5.6,16.75),(5.45,16.6),(5.45,13.65),(5.6,13.5),(11,13.5),pos('J1',8)],.17,p.B_Cu)
via('GND',4.5,17.3)
line('BUCK_SW',[pos('U3',7),(16.25,25.5),(14.985,26.765),pos('L4',1)],.3)
line('+3.3V',[pos('L4',2),pos('C61',1)],.4)
# Ground fanouts are routed to vias outside the exposed pads; do not seed vias in pads.
p.SaveBoard(str(D/'module.kicad_pcb'),b)
print('Critical RF, crystal and switch-node routes saved')
