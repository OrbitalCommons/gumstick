#!/usr/bin/env python3
"""Remove isolated plane-net copper with no component-pad connection."""
from pathlib import Path
source=Path(__file__).with_name('connect_plane_components.py')
exec(compile(source.read_text().split('done=0;failed=set()')[0],str(source),'exec'))
arr=objects();removed=0
for net in ['GND','+3.3V']:
 indices=[i for i,a in enumerate(arr) if a[0]==net];tree=STRtree([arr[i][2] for i in indices]);seen=set();components=[]
 for seed in indices:
  if seed in seen:continue
  seen.add(seed);todo=[seed];members=[]
  while todo:
   i=todo.pop();members.append(i);a=arr[i]
   for k in tree.query(a[2],predicate='dwithin',distance=.00001):
    j=indices[k]
    if j not in seen and set(a[1])&set(arr[j][1]):seen.add(j);todo.append(j)
  components.append(members)
 if not components:continue
 main=max(components,key=lambda g:sum(arr[i][2].area for i in g))
 for group in components:
  if group is main or any(isinstance(arr[i][3],p.PAD) for i in group):continue
  for i in group:
   t=arr[i][3]
   if not isinstance(t,p.ZONE):b.RemoveNative(t);removed+=1
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(D/'module.kicad_pcb'),b);print('Removed isolated plane copper',removed)
