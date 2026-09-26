"""Apply readable display finishes to normalized exact Hirose connector geometry.
Run with CadQuery. Contact-face classification is visual metadata, not new CAD
geometry or a manufacturer material declaration.
"""
from pathlib import Path
import cadquery as cq
R=Path(__file__).resolve().parents[2];D=R/'boards/esp32-fpga-module/3dmodels'
for name in ['DF40C_2_0_40DS','DF40C_40DP']:
 s=cq.importers.importStep(str(D/(name+'.step'))).val();a=cq.Assembly(s,name=name,color=cq.Color(.065,.075,.09));count=0
 for face in s.Faces():
  b=face.BoundingBox();c=face.Center();dx=b.xlen
  # The thin contact profiles repeat every 0.4 mm across each connector row.
  contact=dx<.255 and abs(c.x)<=3.95 and min(abs(c.x-(-3.8+.4*i)) for i in range(20))<.135 and abs(c.y)>.30
  tab=name.endswith('40DP') and abs(c.x)>4.03 and b.zmax<.3
  if contact or tab:
   a.addSubshape(face,color=cq.Color(.88,.69,.30) if contact else cq.Color(.70,.72,.76));count+=1
 a.export(str(D/(name+'.step')));print(name,'metal faces',count,'/',len(s.Faces()))
