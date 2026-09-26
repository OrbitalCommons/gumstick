"""STEP equivalent of the handoff's illustrative antenna envelope; not vendor CAD."""
from pathlib import Path
import cadquery as cq
out=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module/3dmodels/ACAG0201-2450.step'
a=cq.Assembly(name='ACAG0201_2450_illustrative')
a.add(cq.Workplane('XY').box(2,1.25,.6).translate((0,0,.3)),name='nominal_body',color=cq.Color(.34,.47,.36))
for i,x in enumerate([-.7,.7]):
 a.add(cq.Workplane('XY').box(.6,1.25,.03).translate((x,0,.015)),name=f'terminal_{i+1}',color=cq.Color(.7,.7,.73))
# Approximate top marking from Abracon datasheet, revised 2025-09-20, p.4.
# Dimensions are read from the illustration; this remains illustrative CAD.
a.add(cq.Workplane('XY').box(.18,.18,.004).translate((-.59,.24,.602)),name='top_orientation_mark',color=cq.Color(.38,.39,.38))
a.export(str(out))
