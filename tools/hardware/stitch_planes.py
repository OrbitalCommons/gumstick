#!/usr/bin/env python3
"""Connect isolated local power/ground copper to the inner planes with clearance-checked vias."""
from pathlib import Path
prefix=(Path(__file__).with_name('finish_routing.py')).read_text().split('report=json.loads')[0]
exec(prefix.replace("layers=[p.F_Cu,p.In2_Cu,p.B_Cu];TW", "layers=[p.F_Cu,p.In2_Cu,p.B_Cu,p.In1_Cu];TW"))
VR=.2
report=json.loads((O/'current.json').read_text())
needed={a['uuid'] for issue in report['unconnected_items'] for a in issue['items']}
for net in ['GND','+3.3V']:
 pads=[a for f in b.GetFootprints() for a in f.Pads() if a.GetNetname()==net]
 seen=set()
 for pad in pads:
  arr=objects();g=group(arr,pad.m_Uuid.AsString());uu={a[3].m_Uuid.AsString() for a in g}
  if uu&seen or not uu&needed:continue
  seen.update(uu)
  if any(isinstance(a[3],p.PCB_VIA) for a in g):continue
  A=np.zeros((len(layers),H,W),np.uint8);V=np.zeros((H,W),np.uint8)
  for a in A:
   paint(a,box(0,0,20,7.7));paint(a,Point(10,28.25).buffer(3.5+TW/2+.01))
   for sh in [box(0,0,.36,46),box(19.64,0,20,46),box(0,45.24,20,46)]:paint(a,sh)
  paint(V,box(0,0,20,7.9));paint(V,Point(10,28.25).buffer(3.5+VR+.01))
  for sh in [box(0,0,.52,46),box(19.48,0,20,46),box(0,45.08,20,46)]:paint(V,sh)
  for n,ls,geom,t in arr:
   if n==net:continue
   for z in ls:paint(A[z],geom.buffer(CLEAR+TW/2))
   paint(V,geom.buffer(CLEAR+VR))
  src=candidates(g,A);zs={a[1][0] for a in g};tgt=[]
  for z in zs:tgt.extend((np.flatnonzero((V==0)&(A[z]==0))+z*H*W).tolist())
  if not src:print('No plane escape',pad.GetParentFootprint().GetReference(),pad.GetNumber(),flush=True);continue
  with (O/'search.bin').open('wb') as f:
   np.array([W,H,len(layers),len(src),len(tgt)],np.int32).tofile(f);A.tofile(f);V.tofile(f);np.array(src,np.int32).tofile(f);np.array(tgt,np.int32).tofile(f)
  rr=subprocess.run([str(O/'finish'),str(O)])
  if rr.returncode:print('No plane via path',net,pad.GetParentFootprint().GetReference(),pad.GetNumber(),flush=True);continue
  path=[tuple(map(int,l.split())) for l in (O/'path.txt').read_text().splitlines()]
  def addtrack(a,e):
   if a==e:return
   t=p.PCB_TRACK(b);t.SetStart(pt(a[0]*S,a[1]*S));t.SetEnd(pt(e[0]*S,e[1]*S));t.SetWidth(p.FromMM(.1));t.SetLayer(layers[a[2]]);t.SetNet(b.FindNet(net));b.Add(t)
  start=path[0]
  for i in range(1,len(path)):
   if i==len(path)-1 or tuple(path[i+1][k]-path[i][k] for k in range(3))!=tuple(path[i][k]-path[i-1][k] for k in range(3)):addtrack(start,path[i]);start=path[i]
  e=path[-1]
  if any(isinstance(t,p.PCB_VIA) and t.GetNetname()==net and (np.linalg.norm(np.array(xy(t.GetPosition()))-np.array(e[:2])*S)<.001) for t in b.GetTracks()):
   p.SaveBoard(str(D/'module.kicad_pcb'),b);continue
  v=p.PCB_VIA(b);v.SetPosition(pt(e[0]*S,e[1]*S));v.SetWidth(p.FromMM(.4));v.SetDrill(p.FromMM(.2));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));b.Add(v)
  print('Plane via',net,pad.GetParentFootprint().GetReference(),pad.GetNumber(),e,flush=True);p.SaveBoard(str(D/'module.kicad_pcb'),b)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b)
