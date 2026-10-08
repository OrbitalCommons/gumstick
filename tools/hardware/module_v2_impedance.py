#!/usr/bin/env python3
"""RF feed geometry for the v2 module on JLC04081H-3313: JLCPCB's coated-CPWG calculator (geometry only, no PCB upload)
plus an independent 2D field solve. Writes boards/esp32-fpga-module-v2/docs/rf-feed.json.
Run with: uv run --with websocket-client --with numpy python tools/hardware/module_v2_impedance.py"""
import json, uuid, hashlib, urllib.request, sys
from pathlib import Path
import websocket
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cpwg_fieldsolve import solve
OUT = Path(__file__).resolve().parents[2] / 'boards/esp32-fpga-module-v2/docs/rf-feed.json'
STACK = {'name': 'JLC04081H-3313', 'prepreg_mm': 0.0994, 'prepreg_er': 4.1, 'copper_mm': 0.035,
         'mask': 'LPI er 3.8, 1.2 mil over substrate, 0.6 mil over copper', 'reference': 'In1.Cu GND'}
GAP, CHOSEN = 0.15, 0.14
uid = uuid.uuid4().hex
ws = websocket.create_connection('wss://tools.jlc.com/jlcTools/webSocket/' + uid, timeout=25)
def jlc(w, gap, h=STACK['prepreg_mm'], er=STACK['prepreg_er'], t=STACK['copper_mm']):
    params = {'dCalculateMode': 3, 'H1': h / .0254, 'Er1': er, 'W1': w / .0254, 'W2': w / .0254 - .5, 'G1': 20, 'D1': gap / .0254, 'T1': t / .0254,
              'C1': 1.2, 'C2': .6, 'CEr': 3.8, 'isLinkComputingMode': False, 'W2LinkW1Incr': .5, 'ZoTol': .5}
    aid = uuid.uuid4().hex
    body = {'accessId': aid, 'impedance_calc_mark': 'CoatedCoplanarWaveguideWithLowerGnd1B',
            'paramMd5': hashlib.md5(json.dumps(params, separators=(',', ':')).encode()).hexdigest(), 'impedance_calc_arg': params, 'uuid': uid}
    req = urllib.request.Request('https://jlcpcb.com/api/jlcTools/impedance/calc', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    json.load(urllib.request.urlopen(req, timeout=20))
    while True:
        m = json.loads(ws.recv())
        if m.get('accessId') == aid: return params, m.get('impedance_calc_result')
sweep = []
for gap in (0.15, 0.20):
    for w in (0.12, 0.13, 0.14, 0.15, 0.16):
        params, r = jlc(w, gap); sweep.append({'width_mm': w, 'gap_mm': gap, 'Z0_ohm': round(r['dImpedance'], 2), 'er_eff': round(r['dErEff'], 3)})
        print('JLC', w, gap, sweep[-1]['Z0_ohm'], flush=True)
calib = jlc(0.26, 0.15, h=0.2104, er=4.4)[1]          # the old 7628 geometry, for comparison with the playbook figure
ws.close()
zc, _ = solve(CHOSEN, GAP, STACK['prepreg_mm'], STACK['prepreg_er'], d=0.005)
zf, ee = solve(CHOSEN, GAP, STACK['prepreg_mm'], STACK['prepreg_er'], d=0.0025)
field = {'width_mm': CHOSEN, 'gap_mm': GAP, 'Z0_d5um': round(zc, 2), 'Z0_d2p5um': round(zf, 2), 'Z0_extrapolated': round(2 * zf - zc, 2), 'er_eff': round(ee, 3)}
print('field', field)
OUT.write_text(json.dumps({'stackup': STACK, 'chosen': {'width_mm': CHOSEN, 'gap_mm': GAP},
                           'jlc_calculator': {'model': 'CoatedCoplanarWaveguideWithLowerGnd1B', 'sweep': sweep,
                                              'old_7628_0.26_0.15_ohm': round(calib['dImpedance'], 2)},
                           'field_solve': field}, indent=2) + '\n')
print('wrote', OUT)
