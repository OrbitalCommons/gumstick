#!/usr/bin/env python3
"""Checks and review exports for the v2 module draft; never fabricate from this script's outputs."""
import subprocess, json, hashlib
from pathlib import Path
D = Path(__file__).resolve().parents[2] / 'boards/esp32-fpga-module-v2'; out = D / 'fab/checks'; out.mkdir(parents=True, exist_ok=True)
def run(*args): subprocess.run(['kicad-cli', *map(str, args)], check=True, capture_output=True)
run('sch', 'erc', '--format', 'json', '--severity-error', '--severity-warning', '-o', out / 'erc.json', D / 'module.kicad_sch')
run('pcb', 'drc', '--schematic-parity', '--refill-zones', '--format', 'json', '--severity-error', '--severity-warning', '-o', out / 'drc.json', D / 'module.kicad_pcb')
e = json.loads((out / 'erc.json').read_text()); d = json.loads((out / 'drc.json').read_text())
r = {'stage': 'Development draft: placed and routed; carrier, RF match, 0.8 mm stackup and C6 sourcing still open',
     'erc': sum(len(s.get('violations', [])) for s in e.get('sheets', [])), 'physical_drc': len(d['violations']),
     'schematic_parity': len(d['schematic_parity']), 'unconnected_items': len(d['unconnected_items']), 'fabrication_ready': False,
     'sha256': {f: hashlib.sha256((D / f).read_bytes()).hexdigest() for f in ['module.kicad_sch', 'module.kicad_pcb', 'module.kicad_pro', 'module.kicad_dru']}}
(D / 'docs/validation.json').write_text(json.dumps(r, indent=2) + '\n')
assert not any(r[k] for k in ['erc', 'physical_drc', 'schematic_parity', 'unconnected_items']), r
run('sch', 'export', 'pdf', '-o', D / 'docs/module-schematic.pdf', D / 'module.kicad_sch')
for layers, name in (('F.Cu,F.SilkS,Edge.Cuts', 'front'), ('B.Cu,Edge.Cuts', 'back'), ('In1.Cu,Edge.Cuts', 'in1-gnd'), ('In2.Cu,Edge.Cuts', 'in2-power')):
    run('pcb', 'export', 'svg', '--page-size-mode', '2', '--exclude-drawing-sheet', '--layers', layers, '-o', D / f'docs/module-{name}.svg', D / 'module.kicad_pcb')
print(json.dumps(r, indent=2))
