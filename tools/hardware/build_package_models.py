"""Build explicitly approximate visualization models; requires cadquery."""
from pathlib import Path
import cadquery as cq
D=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module/3dmodels'
def block(x,y,z,at):return cq.Workplane('XY').box(x,y,z).translate(at)
a=cq.Assembly(name='FC-B1010RGBT-HG_approx')
a.add(block(1,1,.8,(0,0,.5)),name='black_package',color=cq.Color(.045,.045,.05))
for i,(x,y) in enumerate([(.325,.325),(.325,-.325),(-.325,-.325),(-.325,.325)]):a.add(block(.35,.35,.1,(x,y,.05)),name=f'terminal_{i+1}',color=cq.Color(.75,.65,.3))
a.export(str(D/'FC-B1010RGBT-HG_approx.step'))
a=cq.Assembly(name='XFL3012_approx');a.add(block(3,3,1.2,(0,0,.7)),name='molded_body',color=cq.Color(.13,.13,.14))
for i,x in enumerate([-1.1,1.1]):a.add(block(.8,2.4,.1,(x,0,.05)),name=f'terminal_{i+1}',color=cq.Color(.65,.67,.7))
a.export(str(D/'XFL3012_approx.step'))
