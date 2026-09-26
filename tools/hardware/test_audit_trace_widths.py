"""Regression fixtures for width-audit connectivity and triage (no production edits)."""
import hashlib, tempfile, unittest
from pathlib import Path
import pcbnew as p
from audit_trace_widths import audit

def pt(x,y):return p.VECTOR2I(round(x*1e6),round(y*1e6))
class WidthAuditTest(unittest.TestCase):
 def test_contacts_and_clearance(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'fixture.kicad_pcb';b=p.BOARD();nets={}
   for name in ['A','B','C','D','BLOCK']:
    net=p.NETINFO_ITEM(b,name);b.Add(net);nets[name]=net
   for a,c in [((0,0),(20,0)),((20,0),(20,20)),((20,20),(0,20)),((0,20),(0,0))]:
    edge=p.PCB_SHAPE();edge.SetShape(p.SHAPE_T_SEGMENT);edge.SetStart(pt(*a));edge.SetEnd(pt(*c));edge.SetLayer(p.Edge_Cuts);edge.SetWidth(50000);b.Add(edge)
   def trace(net,a,c,w,layer=p.F_Cu):
    t=p.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*c));t.SetWidth(round(w*1e6));t.SetLayer(layer);t.SetNet(nets[net]);b.Add(t)
   trace('A',(2,2),(4,2),.1);trace('A',(4,2),(6,2),.4);trace('A',(6,2),(8,2),.1)
   trace('B',(2,5),(8,5),.4);trace('B',(5,5),(5,6),.1)
   trace('C',(2,8),(4,8),.4);trace('C',(4.1,8.05),(6,8.05),.1)
   trace('D',(2,11),(4,11),.1);trace('D',(4,11),(6,11),.4)
   trace('BLOCK',(2,11.3),(3.5,11.3),.1)
   trace('A',(2,2),(8,2),.6,p.B_Cu) # same net, different layer: not a contact
   trace('BLOCK',(2,2),(8,2),.8,p.In1_Cu)
   p.SaveBoard(str(path),b);before=hashlib.sha256(path.read_bytes()).hexdigest();r=audit(path)
   self.assertEqual(before,hashlib.sha256(path.read_bytes()).hexdigest())
   self.assertEqual(r['transition_pair_count'],5)
   bynet={n:[v for v in r['transitions'] if v['net']==n] for n in nets}
   self.assertEqual([v['category'] for v in bynet['A']],['widen_run_candidate']*2)
   self.assertEqual(bynet['B'][0]['category'],'branch_review')
   self.assertEqual(bynet['C'][0]['contact'],'copper_overlap')
   self.assertEqual(bynet['C'][0]['category'],'overlap_topology_review')
   self.assertEqual(bynet['D'][0]['category'],'constrained_run_review')
   self.assertTrue(any(x['object'].startswith('track ') for x in bynet['D'][0]['widening_blockers']))
   self.assertTrue(any(x['kind']=='wide_island' and x['net']=='A' and x['length_mm']==2 for x in r['width_islands']))
if __name__=='__main__':unittest.main()
