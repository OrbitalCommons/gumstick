"""Shared QFN access constraint: no via copper beneath U1/U2 package bodies."""
import pcbnew as p
VIA_DIAMETER_MM = 0.45
VIA_DRILL_MM = 0.20
VIA_HOLE_GAP_MM = 0.25

QFN_HALF=3.65  # 7 mm package plus outline/placement margin

def qfn_regions(board):
 from shapely.geometry import box
 for f in board.GetFootprints():
  if f.GetReference() not in ['U1','U2']:continue
  x,y=p.ToMM(f.GetPosition().x)-100,p.ToMM(f.GetPosition().y)-100
  yield f.GetReference(),box(x-QFN_HALF,y-QFN_HALF,x+QFN_HALF,y+QFN_HALF)

def paint_qfn_via_keepouts(board,mask,paint,radius):
 for _,region in qfn_regions(board):paint(mask,region.buffer(radius+.01))


def pad_geometry(pad):
 """Actual copper outline in the routing tools' local (100 mm offset) frame."""
 from shapely.geometry import Polygon
 from shapely.ops import unary_union
 layer=next(l for l in [p.F_Cu,p.B_Cu,p.In1_Cu,p.In2_Cu] if pad.IsOnLayer(l))
 poly=p.SHAPE_POLY_SET()
 pad.TransformShapeToPolygon(poly,layer,0,1000,p.ERROR_OUTSIDE)
 shapes=[]
 for i in range(poly.OutlineCount()):
  o=poly.COutline(i)
  shapes.append(Polygon([(p.ToMM(o.CPoint(j).x)-100,p.ToMM(o.CPoint(j).y)-100) for j in range(o.PointCount())]))
 return unary_union(shapes)


def paint_qfn_front_keepouts(board, mask, paint, net, width):
 """Block front tracks beneath QFNs except their own solder lands and ground."""
 if net == 'GND': return
 import numpy as np
 from shapely.geometry import box
 for f in board.GetFootprints():
  if f.GetReference() not in ['U1', 'U2']: continue
  x,y=p.ToMM(f.GetPosition().x)-100,p.ToMM(f.GetPosition().y)-100
  paint(mask,box(x-3.5,y-3.5,x+3.5,y+3.5).buffer(width/2))
  land=np.zeros_like(mask)
  for a in f.Pads():
   if a.GetNetname()==net:
    shape=pad_geometry(a).buffer(-width/2+.000001)
    if not shape.is_empty: paint(land,shape)
  mask[land!=0]=0
