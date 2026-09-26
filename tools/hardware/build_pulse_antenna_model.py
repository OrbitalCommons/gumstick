"""Illustrative Pulse ANT2012LL00R2400A envelope, datasheet p2 (not vendor CAD)."""
from pathlib import Path
import cadquery as cq
out=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module/3dmodels/ANT2012LL00R2400A.step'
a=cq.Assembly(name='ANT2012LL00R2400A_illustrative')
a.add(cq.Workplane('XY').box(2,1.25,1.1).translate((0,0,.55)),name='ceramic',color=cq.Color(.12,.38,.65))
for i,x in enumerate([-.925,.925]):
 a.add(cq.Workplane('XY').box(.15,1.26,1.11).translate((x,0,.555)),name=f'terminal_{i+1}',color=cq.Color(.75,.76,.78))
a.add(cq.Workplane('XY').circle(.09).extrude(.005).translate((-.55,-.3,1.102)),name='feed_mark',color=cq.Color(.92,.92,.92))
a.export(str(out))
