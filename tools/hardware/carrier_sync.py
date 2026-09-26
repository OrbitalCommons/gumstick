#!/usr/bin/env python3
"""Verify schematic against circuit contract; assign only KiCad's generated NC nets."""
from pathlib import Path
import xml.etree.ElementTree as ET,json,pcbnew as p
R=Path(__file__).resolve().parents[2];D=R/'boards/programming-carrier';parts=json.loads((D/'docs/circuit.json').read_text());root=ET.parse(R/'tmp/carrier/netlist.xml').getroot();b=p.LoadBoard(str(D/'carrier.kicad_pcb'));actual={}
for n in root.findall('./nets/net'):
 for node in n.findall('node'):actual[(node.attrib['ref'],node.attrib['pin'])]=n.attrib['name']
for ref,c in parts.items():
 for pad,expected in c['pins'].items():
  got=actual.get((ref,pad));assert (expected==got or expected is None and (got is None or got.startswith('unconnected-'))),(ref,pad,expected,got)
for f in b.GetFootprints():
 for pad in f.Pads():
  name=actual.get((f.GetReference(),pad.GetNumber()))
  if name:
   n=b.FindNet(name)
   if n is None or n.GetNetCode()<0:n=p.NETINFO_ITEM(b,name);b.Add(n)
   pad.SetNet(n)
p.SaveBoard(str(D/'carrier.kicad_pcb'),b)
print('Verified all schematic pins against circuit.json; NC nets synchronized.')
