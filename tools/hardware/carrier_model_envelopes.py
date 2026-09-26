#!/usr/bin/env python3
"""Illustrative envelopes for two parts absent from installed KiCad STEP library.
Dimensions follow their named footprint bodies. These are not vendor mechanical CAD.
"""
from pathlib import Path
import cadquery as cq
D=Path(__file__).resolve().parents[2]/'boards/programming-carrier/3dmodels'
a=cq.Assembly(name='HRO_USB_C_envelope')
shell=cq.Workplane('XY').box(8.9,7.35,3.16,centered=(True,True,False)).translate((0,1.575,0.05))
# STEP y is opposite the footprint's y; front opening at negative model Y.
cut=cq.Workplane('XY').box(8.3,7.6,2.5,centered=(True,True,False)).translate((0,1.4,.35))
a.add(shell.cut(cut),name='shield',color=cq.Color(.7,.72,.74));a.add(cq.Workplane('XY').box(6.6,5.2,.7).translate((0,1.8,1.6)),name='tongue',color=cq.Color(.07,.07,.07))
a.save(str(D/'USB_C_HRO_envelope.step'))
a=cq.Assembly(name='CK_JS102011SAQN_envelope');a.add(cq.Workplane('XY').box(8.6,4.3,3,centered=(True,True,False)).translate((0,0,.1)),name='body',color=cq.Color(.45,.47,.49));a.add(cq.Workplane('XY').box(2,2,2,centered=(True,True,False)).translate((-1.5,0,3.1)),name='actuator',color=cq.Color(.1,.1,.1));a.save(str(D/'CK_JS102011SAQN_envelope.step'))
