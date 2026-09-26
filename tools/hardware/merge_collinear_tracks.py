#!/usr/bin/env python3
"""Merge consecutive collinear, equal-width tracks without changing copper."""
from pathlib import Path
from collections import defaultdict
import pcbnew as p
path=Path(__file__).resolve().parents[2]/'boards/esp32-fpga-module/module.kicad_pcb'
b=p.LoadBoard(str(path));count=0
while True:
 adj=defaultdict(list)
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):continue
  for a in [t.GetStart(),t.GetEnd()]:adj[(t.GetNetCode(),t.GetLayer(),a.x,a.y)].append(t)
 used=set();n=0
 for (net,layer,x,y),ts in adj.items():
  if len(ts)!=2 or any(t.m_Uuid.AsString() in used for t in ts) or ts[0].GetWidth()!=ts[1].GetWidth():continue
  ends=[]
  for t in ts:
   a,c=t.GetStart(),t.GetEnd();ends.append(c if (a.x,a.y)==(x,y) else a)
  a,c=ends;u=(a.x-x,a.y-y);v=(c.x-x,c.y-y)
  if u[0]*v[1]!=u[1]*v[0] or u[0]*v[0]+u[1]*v[1]>=0:continue
  t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(c);t.SetLayer(layer);t.SetWidth(ts[0].GetWidth());t.SetNet(ts[0].GetNet());b.Add(t)
  for old in ts:used.add(old.m_Uuid.AsString());b.RemoveNative(old)
  n+=1
 count+=n
 if not n:break
p.SaveBoard(str(path),b);print('Merged',count,'collinear segments')
