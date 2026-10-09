#!/usr/bin/env python3
"""Generate the v2 module schematic and symbol library from docs/circuit.json, then verify the netlist.

Blocks: ESP32-C6, FPGA, M.2 card edge, RF front end, crystal, reset/boot, 1.2 V regulator,
configuration link + LED, decoupling. Wires inside the small blocks; global labels between blocks.
Never writes the PCB.
"""
from pathlib import Path
import json, uuid, re, subprocess, tempfile, xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[2]; D = R / 'boards/esp32-fpga-module-v2'
parts = json.loads((D / 'docs/circuit.json').read_text())
uid = lambda s: str(uuid.uuid5(uuid.NAMESPACE_URL, 'bp-module-v2-sch/' + s))
q = lambda s: json.dumps(str(s))
items = []; symbols = {}; placed = {}; count = [0]
POWER = {'+3.3V', '+1.2V', '+1.2V_PLL', 'ESP_VDD3P3', 'GND'}

def E(size=1.27, just=''): return f'(effects (font (size {size} {size}))' + (f' (justify {just})' if just else '') + ')'
def prop(k, val, x, y, hide=False, just=''): return f'(property {q(k)} {q(val)} (at {x} {y} 0) {E(1.27, just)}' + (' (hide yes)' if hide else '') + ')'
def nid(prefix):
    count[0] += 1; return uid(prefix + str(count[0]))
def wire(a, b): items.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid "{nid("w")}"))')
def junction(a): items.append(f'(junction (at {a[0]} {a[1]}) (diameter 0) (color 0 0 0 0) (uuid "{nid("j")}"))')
def glabel(n, x, y, angle=0):
    just = 'right' if angle == 180 else 'left'
    items.append(f'(global_label {q(n)} (shape bidirectional) (at {x} {y} {angle}) (fields_autoplaced yes) {E(1.27, just)} (uuid "{nid("l")}") (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes))))')
def note(t, x, y, size=1.5): items.append(f'(text {q(t)} (at {x} {y} 0) {E(size, "left")} (uuid "{nid("t")}"))')
def box(title, x, y, w, h):
    items.append(f'(rectangle (start {x} {y}) (end {x + w} {y + h}) (stroke (width 0.254) (type dash)) (fill (type none)) (uuid "{nid("b")}"))'); note(title, x + 2.54, y + 5.08, 2.0)

# ---------------------------------------------------------------- symbols
pins_of = {}   # ref -> {num: (x, y, angle)} in symbol coordinates (KiCad: y up)
def symdef(ref):
    c = parts[ref]; kind = c['kind']; names = c.get('names', {}); types = c.get('types', {}); pm = {}; shapes = []; pins = []
    hide_names = kind in ('r', 'c', 'l', 'testpoint', 'xtal', 'led')
    if kind in ('r', 'c', 'l'):
        pm = {'1': (-5.08, 0, 0), '2': (5.08, 0, 180)}; length = 2.54 if kind == 'r' else 2.54
        if kind == 'r':
            shapes = ['(polyline (pts (xy -2.54 0) (xy -1.905 1.016) (xy -0.635 -1.016) (xy 0.635 1.016) (xy 1.905 -1.016) (xy 2.54 0)) (stroke (width 0.254) (type default)) (fill (type none)))']
        elif kind == 'c':
            shapes = ['(polyline (pts (xy -0.635 -2.032) (xy -0.635 2.032)) (stroke (width 0.254) (type default)) (fill (type none)))',
                      '(polyline (pts (xy 0.635 -2.032) (xy 0.635 2.032)) (stroke (width 0.254) (type default)) (fill (type none)))',
                      '(polyline (pts (xy -2.54 0) (xy -0.635 0)) (stroke (width 0.254) (type default)) (fill (type none)))',
                      '(polyline (pts (xy 0.635 0) (xy 2.54 0)) (stroke (width 0.254) (type default)) (fill (type none)))']
        else:
            shapes = [f'(arc (start {x0} 0) (mid {x0 + 0.635} 0.8) (end {x0 + 1.27} 0) (stroke (width 0.254) (type default)) (fill (type none)))' for x0 in (-2.54, -1.27, 0, 1.27)]
        for num, (x, y, a) in pm.items(): pins.append(f'(pin passive line (at {x} {y} {a}) (length {length}) (name "~" {E()}) (number "{num}" {E()}))')
        w = h = 0
    elif kind == 'testpoint':
        pm = {'1': (0, -5.08, 90)}; shapes = ['(circle (center 0 0) (radius 0.762) (stroke (width 0.254) (type default)) (fill (type none)))']
        pins.append(f'(pin passive line (at 0 -5.08 90) (length 4.318) (name "~" {E()}) (number "1" {E()}))'); w = h = 0
    elif kind == 'xtal':
        pm = {'IN/OUT': (-7.62, 0, 0), 'OUT/IN': (7.62, 0, 180), 'GND-A': (-2.54, -5.08, 90), 'GND-B': (2.54, -5.08, 90)}
        shapes = ['(rectangle (start -1.27 -2.54) (end 1.27 2.54) (stroke (width 0.254) (type default)) (fill (type none)))',
                  '(polyline (pts (xy -2.032 -2.54) (xy -2.032 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))',
                  '(polyline (pts (xy 2.032 -2.54) (xy 2.032 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))']
        for num, (x, y, a) in pm.items(): pins.append(f'(pin passive line (at {x} {y} {a}) (length {5.08 if "GND" not in num else 2.54}) (name {q(names.get(num, num))} {E()}) (number {q(num)} {E()}))')
        w = h = 0
    elif kind == 'led':
        pm = {'P$1': (0, 7.62, 270), 'P$2': (-5.08, -7.62, 90), 'P$3': (0, -7.62, 90), 'P$4': (5.08, -7.62, 90)}
        shapes = ['(rectangle (start -7.62 -5.08) (end 7.62 5.08) (stroke (width 0.254) (type default)) (fill (type background)))',
                  '(text "RGB" (at 0 0 0) (effects (font (size 1.27 1.27))))']
        for num, (x, y, a) in pm.items(): pins.append(f'(pin passive line (at {x} {y} {a}) (length 2.54) (name {q(names.get(num, num))} {E()}) (number {q(num)} {E()}))')
        w = h = 0
    else:  # ic / connector: pins on the left/right at 2.54 pitch, ordered by the layout table
        left, right = IC_LAYOUT[ref]
        half = max(len(left), len(right)); h = (half + 1) * 2.54; w = 22.86 if ref in ('U1', 'U2') else 12.7
        for side, nums in ((-1, left), (1, right)):
            for i, num in enumerate(nums):
                if num is None: continue
                y = h / 2 - 2.54 - i * 2.54
                pm[num] = (side * (w / 2 + 5.08), y, 0 if side == -1 else 180)
                t = types.get(num, 'passive'); nm = names.get(num, num)
                pins.append(f'(pin {t} line (at {pm[num][0]} {pm[num][1]} {pm[num][2]}) (length 5.08) (name {q(nm)} (effects (font (size 1.0 1.0)))) (number {q(num)} {E(1.0)}))')
        shapes = [f'(rectangle (start {-w / 2} {h / 2}) (end {w / 2} {-h / 2}) (stroke (width 0.254) (type default)) (fill (type background)))']
    pins_of[ref] = pm
    symbols[ref] = (f'(symbol {q(ref)} (pin_names (offset 0.762){" hide" if hide_names else ""}) (in_bom {"yes" if c.get("bom", True) else "no"}) (on_board yes) '
                    f'{prop("Reference", ref, 0, h / 2 + 2.54)} {prop("Value", c["value"], 0, h / 2 + 0.0)} {prop("Footprint", c["footprint"], 0, 0, True)} {prop("Datasheet", "", 0, 0, True)} '
                    f'(symbol "{ref}_0_1" ' + ''.join(shapes) + f') (symbol "{ref}_1_1" ' + ''.join(pins) + '))')
    return pm

# IC pin arrangement (left column, right column). None leaves a gap.
esp_left = ['1', None, '2', '3', None, '5', '28', '37', '40', None, '39', '38', None, '4', None, '18', '19', None, '20', '21', '22', '24', '25', '26', '23', None, '41']
esp_right = ['6', '7', '8', '9', '12', '13', '16', '17', None, '10', '11', '14', '15', '27', '29', '30', '31', '32', '33', '34', '35', '36']
fpga_left = ['1', '22', '24', '33', None, '5', '30', None, '29', None, 'PAD', None, '8', '7', None, '15', '17', '14', '16', '13', '18', None, '39', '40', '41']
fpga_right = ['2', '3', '4', '6', '9', '10', '11', '12', '19', '20', '21', '23', '25', '26', '27', '28', '31', '32', '34', '35', '36', '37', '38', '42', '43', '44', '45', '46', '47', '48']
j1_odd = [str(n) for n in range(1, 76, 2) if str(n) in parts['J1']['pins']]
j1_even = [str(n) for n in range(2, 76, 2) if str(n) in parts['J1']['pins']]
IC_LAYOUT = {'U4': (['1', '6', '5', '2', '3', '7'], ['8', None, '4', '9']), 'U1': (esp_left, esp_right), 'U2': (fpga_left, fpga_right), 'J1': (j1_odd, j1_even), 'U3': (['1', '3', None, '2'], ['5', None, '4']), 'J3': (['1', '2'], [])}

def place(ref, x, y, rot=0, mirror=False):
    """Place a symbol; return a dict of pin terminal coordinates in sheet space."""
    pm = symdef(ref); c = parts[ref]
    def tx(px, py):   # symbol coords (y up) -> sheet (y down), with rotation about the origin
        a = {0: (px, py), 90: (-py, px), 180: (-px, -py), 270: (py, -px)}[rot]
        return (round(x + a[0], 4), round(y - a[1], 4))
    term = {}
    for num, (px, py, pa) in pm.items(): term[num] = tx(px, py)
    kind = c['kind']
    label_off = {0: (0, -2.54), 90: (2.54, 0), 180: (0, 2.54), 270: (-2.54, 0)}
    rx, ry = x + (2.0 if kind in ('r', 'c', 'l') else 0), y - 3.0
    if kind in ('r', 'c', 'l') and rot in (90, 270): rx, ry = x + 2.54, y - 1.0
    if kind in ('ic', 'connector'):
        left, right = IC_LAYOUT[ref]; h = (max(len(left), len(right)) + 1) * 2.54; rx, ry = x, y - h / 2 - 2.54
    val = prop('Value', c['value'], rx, ry + 1.6 if kind in ('r', 'c', 'l') else ry + 2.54, kind in ('testpoint',))
    items.append(f'(symbol (lib_id "Module2:{ref}") (at {x} {y} {rot}) (unit 1) (in_bom {"yes" if c.get("bom", True) else "no"}) (on_board yes) (dnp no) (fields_autoplaced yes) (uuid "{uid("s" + ref)}") '
                 f'{prop("Reference", ref, rx, ry)} {val} {prop("Footprint", c["footprint"], x, y, True)} {prop("Datasheet", "", x, y, True)} '
                 f'(instances (project "module" (path "/{uid("root")}" (reference {q(ref)}) (unit 1)))))')
    placed[ref] = term; return term

pc = [0]
def power(net, x, y, down=False):
    """Power symbol at (x, y): the pin end sits at (x, y)."""
    pc[0] += 1; ref = f'#PWR{pc[0]:03d}'; name = 'PWR_' + re.sub(r'[^A-Za-z0-9]+', '_', net).strip('_')
    if name not in symbols:
        if net == 'GND':
            shape = '(polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -0.635 -1.905) (xy 0.635 -1.905)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy 0 -2.54) (xy 0 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))'
            vy = -3.81
        else:
            shape = '(polyline (pts (xy -1.27 1.27) (xy 1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy 0 0) (xy 0 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))'
            vy = 2.54
        symbols[name] = (f'(symbol "{name}" (power) (pin_names (offset 0)) (in_bom no) (on_board no) {prop("Reference", "#PWR", 0, -2.54, True)} {prop("Value", net, 0, vy)} '
                         f'(symbol "{name}_0_1" {shape}) (symbol "{name}_1_1" (pin power_in line (at 0 0 90) (length 0) (name {q(net)} {E()}) (number "1" {E()}))))')
    rot = 180 if net == 'GND' else 0
    vy = y + 3.81 if net == 'GND' else y - 2.54
    items.append(f'(symbol (lib_id "Module2:{name}") (at {x} {y} {rot}) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid "{uid(ref)}") {prop("Reference", ref, x, y, True)} {prop("Value", net, x, vy)} '
                 f'(instances (project "module" (path "/{uid("root")}" (reference {q(ref)}) (unit 1)))))')

def pwr_flag(x, y):
    pc[0] += 1; ref = f'#FLG{pc[0]:03d}'
    if 'FLAG' not in symbols:
        symbols['FLAG'] = (f'(symbol "FLAG" (power) (pin_names (offset 0)) (in_bom no) (on_board no) {prop("Reference", "#FLG", 0, 0, True)} {prop("Value", "PWR_FLAG", 0, 3.81)} '
                           f'(symbol "FLAG_0_1" (polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))) '
                           f'(symbol "FLAG_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" {E()}) (number "1" {E()}))))')
    items.append(f'(symbol (lib_id "Module2:FLAG") (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid "{uid(ref)}") {prop("Reference", ref, x, y, True)} {prop("Value", "PWR_FLAG", x, y - 3.81)} '
                 f'(instances (project "module" (path "/{uid("root")}" (reference {q(ref)}) (unit 1)))))')

def pin_label(term, net, side):
    """Short stub from an IC pin terminal and a global label (left side: label to the left)."""
    x, y = term
    if side == 'L': wire((x, y), (x - 5.08, y)); glabel(net, x - 5.08, y, 180)
    else: wire((x, y), (x + 5.08, y)); glabel(net, x + 5.08, y, 0)
def pin_power(term, net, side):
    x, y = term
    if net == 'GND':
        wire((x, y), (x - 2.54 if side == 'L' else x + 2.54, y)); xx = x - 2.54 if side == 'L' else x + 2.54
        wire((xx, y), (xx, y + 2.54)); power('GND', xx, y + 2.54)
    else:
        xx = x - 2.54 if side == 'L' else x + 2.54
        wire((x, y), (xx, y)); wire((xx, y), (xx, y - 2.54)); power(net, xx, y - 2.54)

def ic_block(ref, x, y, title, w, h):
    box(title, x, y, w, h)
    left, right = IC_LAYOUT[ref]; sh = (max(len(left), len(right)) + 1) * 2.54
    cx, cy = x + w / 2, y + 12.7 + sh / 2
    term = place(ref, cx, cy)
    c = parts[ref]
    for side, col in (('L', left), ('R', right)):
        i = 0
        while i < len(col):
            num = col[i]
            if num is None: i += 1; continue
            net = c['pins'].get(num)
            if net is None:
                t = term[num]; items.append(f'(no_connect (at {t[0]} {t[1]}) (uuid "{nid("nc")}"))'); i += 1; continue
            if net not in POWER:
                pin_label(term[num], net, side); i += 1; continue
            j = i
            while j + 1 < len(col) and col[j + 1] is not None and c['pins'].get(col[j + 1]) == net: j += 1
            run = col[i:j + 1]; xs = term[run[0]][0] - 2.54 if side == 'L' else term[run[0]][0] + 2.54
            ys = [term[n][1] for n in run]
            for n in run: wire(term[n], (xs, term[n][1]))
            if net == 'GND':
                wire((xs, min(ys)), (xs, max(ys) + 2.54)); power('GND', xs, max(ys) + 2.54)
                for n in run:
                    if term[n][1] != min(ys): junction((xs, term[n][1]))
            else:
                wire((xs, max(ys)), (xs, min(ys) - 2.54)); power(net, xs, min(ys) - 2.54)
                for n in run:
                    if term[n][1] != max(ys): junction((xs, term[n][1]))
            i = j + 1
    return term

# ---------------------------------------------------------------- sheet
sheet_w, sheet_h = 520.0, 330.0
ic_block('U1', 15.24, 15.24, 'ESP32-C6  (QFN40, external flash U4; VDD_SPI unused)', 93.98, 101.6)
ic_block('U4', 320.04, 15.24, 'W25Q128JV 16 MB quad SPI flash (3.3 V from the plane)', 71.12, 45.72)
ic_block('U2', 124.46, 15.24, 'iCE40UP5K-SG48  (3.3 V I/O, 1.2 V core)', 93.98, 101.6)
ic_block('J1', 233.68, 15.24, 'M.2 key M card edge J1  (custom pinout, 3.3 V in, see docs/icd-v2-pinout.csv)', 71.12, 114.3)

# RF front end: ANT -> C1 shunt -> L3 -> C2 shunt -> J3
bx, by = 15.24, 134.62; box('RF front end (initial C-L-C match, tune on hardware)', bx, by, 96.52, 50.8)
yl = by + 25.4
glabel('RF_IN', bx + 7.62, yl, 180); wire((bx + 7.62, yl), (bx + 22.86, yl))
t = place('C1', bx + 22.86, yl + 5.08, 270); wire((bx + 22.86, yl), t['1']) if t['1'][1] > yl else None
wire(t['2'], (t['2'][0], t['2'][1] + 2.54)); power('GND', t['2'][0], t['2'][1] + 2.54); junction((bx + 22.86, yl))
t3 = place('L3', bx + 35.56, yl, 0); wire((bx + 22.86, yl), t3['1'])
t2 = place('C2', bx + 48.26, yl + 5.08, 270); wire(t3['2'], (bx + 48.26, yl)); junction((bx + 48.26, yl))
wire(t2['2'], (t2['2'][0], t2['2'][1] + 2.54)); power('GND', t2['2'][0], t2['2'][1] + 2.54)
glabel('RF_ANT', bx + 55.88, yl - 2.54, 0); wire((bx + 55.88, yl - 2.54), (bx + 55.88, yl)); junction((bx + 55.88, yl))
tj = place('J3', bx + 71.12, yl + 1.27, 0)
wire((bx + 48.26, yl), (tj['1'][0], yl)); wire((tj['1'][0], yl), tj['1']) if tj['1'][1] != yl else None
wire(tj['2'], (tj['2'][0] - 2.54, tj['2'][1])); wire((tj['2'][0] - 2.54, tj['2'][1]), (tj['2'][0] - 2.54, tj['2'][1] + 5.08)); power('GND', tj['2'][0] - 2.54, tj['2'][1] + 5.08)

# crystal
bx, by = 124.46, 134.62; box('40 MHz crystal (24 nH series on XTAL_P per C6 checklist)', bx, by, 96.52, 50.8)
yl = by + 22.86
glabel('XTAL_P', bx + 5.08, yl, 180); t5 = place('L5', bx + 15.24, yl, 0); wire((bx + 5.08, yl), t5['1'])
nx = bx + 27.94; wire(t5['2'], (nx, yl)); junction((nx, yl))
t6 = place('C6', nx, yl + 7.62, 270); wire((nx, yl), t6['1']); wire(t6['2'], (nx, t6['2'][1] + 2.54)); power('GND', nx, t6['2'][1] + 2.54)
glabel('XTAL_P_CRYSTAL', nx + 5.08, yl - 2.54, 0); wire((nx + 5.08, yl - 2.54), (nx + 5.08, yl)); junction((nx + 5.08, yl))
ty = place('Y1', bx + 48.26, yl, 0); wire((nx, yl), ty['IN/OUT'])
nx2 = bx + 68.58; wire(ty['OUT/IN'], (nx2, yl)); junction((nx2, yl))
t7 = place('C7', nx2, yl + 7.62, 270); wire((nx2, yl), t7['1']); wire(t7['2'], (nx2, t7['2'][1] + 2.54)); power('GND', nx2, t7['2'][1] + 2.54)
wire((nx2, yl), (bx + 86.36, yl)); glabel('XTAL_N', bx + 86.36, yl, 0)
wire(ty['GND-A'], (ty['GND-A'][0], ty['GND-A'][1] + 2.54)); power('GND', ty['GND-A'][0], ty['GND-A'][1] + 2.54)
wire(ty['GND-B'], (ty['GND-B'][0], ty['GND-B'][1] + 2.54)); power('GND', ty['GND-B'][0], ty['GND-B'][1] + 2.54)

# reset and boot straps
bx, by = 233.68, 134.62; box('Reset and boot straps', bx, by, 71.12, 50.8)
y1 = by + 17.78
power('+3.3V', bx + 10.16, y1 - 5.08); wire((bx + 10.16, y1 - 5.08), (bx + 10.16, y1))
tr = place('R22', bx + 20.32, y1, 180); wire((bx + 10.16, y1), tr['2']); nx = bx + 30.48; wire(tr['1'], (nx, y1)); junction((nx, y1))
tc = place('C32', nx, y1 + 7.62, 270); wire((nx, y1), tc['1']); wire(tc['2'], (nx, tc['2'][1] + 2.54)); power('GND', nx, tc['2'][1] + 2.54)
wire((nx, y1), (bx + 43.18, y1)); glabel('ESP_EN', bx + 43.18, y1, 0)
y2 = by + 35.56
power('+3.3V', bx + 10.16, y2 - 5.08); wire((bx + 10.16, y2 - 5.08), (bx + 10.16, y2)); wire((bx + 10.16, y2), (bx + 10.16, y2 + 7.62)); junction((bx + 10.16, y2))
tr = place('R20', bx + 20.32, y2, 180); wire((bx + 10.16, y2), tr['2']); wire(tr['1'], (bx + 35.56, y2)); glabel('ESP_GPIO9_BOOT', bx + 35.56, y2, 0)
tr = place('R21', bx + 20.32, y2 + 7.62, 180); wire((bx + 10.16, y2 + 7.62), tr['2']); wire(tr['1'], (bx + 35.56, y2 + 7.62)); glabel('ESP_GPIO8', bx + 35.56, y2 + 7.62, 0)
note('GPIO9 low with GPIO8 high enters serial download; GPIO4/5/15 straps left at chip defaults.', bx + 2.54, by + 48.26, 1.1)

# 1.2 V regulator
bx, by = 15.24, 193.04; box('1.2 V FPGA core regulator', bx, by, 134.62, 55.88)
yl = by + 22.86
power('+3.3V', bx + 7.62, yl - 7.62); wire((bx + 7.62, yl - 7.62), (bx + 7.62, yl + 2.54)); junction((bx + 7.62, yl))
tc = place('C62', bx + 7.62, yl + 7.62 + 2.54, 270); wire((bx + 7.62, yl + 2.54), tc['1']); wire(tc['2'], (bx + 7.62, tc['2'][1] + 2.54)); power('GND', bx + 7.62, tc['2'][1] + 2.54)
tu = place('U3', bx + 38.1, yl + 2.54, 0)
wire((bx + 7.62, yl), (tu['1'][0], yl)); wire((tu['1'][0], yl), tu['1']) if tu['1'][1] != yl else None
wire(tu['3'], (tu['3'][0] - 2.54, tu['3'][1])); wire((tu['3'][0] - 2.54, tu['3'][1]), (tu['3'][0] - 2.54, tu['1'][1])); wire((tu['3'][0] - 2.54, tu['1'][1]), tu['1']); junction(tu['1'])
wire(tu['2'], (tu['2'][0] - 2.54, tu['2'][1])); wire((tu['2'][0] - 2.54, tu['2'][1]), (tu['2'][0] - 2.54, tu['2'][1] + 5.08)); power('GND', tu['2'][0] - 2.54, tu['2'][1] + 5.08)
items.append(f'(no_connect (at {tu["4"][0]} {tu["4"][1]}) (uuid "{nid("nc")}"))')
ox = tu['5'][0] + 7.62; wire(tu['5'], (ox, tu['5'][1])); junction((ox, tu['5'][1]))
yo = tu['5'][1]
tc = place('C63', ox, yo + 10.16, 270); wire((ox, yo), tc['1']); wire(tc['2'], (ox, tc['2'][1] + 2.54)); power('GND', ox, tc['2'][1] + 2.54)
ox2 = ox + 12.7; wire((ox, yo), (ox2, yo)); junction((ox2, yo))
tc = place('C45', ox2, yo + 10.16, 270); wire((ox2, yo), tc['1']); wire(tc['2'], (ox2, tc['2'][1] + 2.54)); power('GND', ox2, tc['2'][1] + 2.54)
wire((ox2, yo), (ox2 + 7.62, yo)); power('+1.2V', ox2 + 7.62, yo - 2.54); wire((ox2 + 7.62, yo), (ox2 + 7.62, yo - 2.54)); wire((ox2 + 7.62, yo), (ox2 + 7.62 + 5.08, yo)); junction((ox2 + 7.62, yo))
# PLL filter
tl = place('L2', ox2 + 7.62 + 17.78, yo, 0); wire((ox2 + 7.62 + 5.08, yo), tl['1'])
px = tl['2'][0] + 5.08; wire(tl['2'], (px, yo)); junction((px, yo))
tc = place('C43', px, yo + 10.16, 270); wire((px, yo), tc['1']); wire(tc['2'], (px, tc['2'][1] + 2.54)); power('GND', px, tc['2'][1] + 2.54)
px2 = px + 12.7; wire((px, yo), (px2, yo)); junction((px2, yo))
tc = place('C44', px2, yo + 10.16, 270); wire((px2, yo), tc['1']); wire(tc['2'], (px2, tc['2'][1] + 2.54)); power('GND', px2, tc['2'][1] + 2.54)
wire((px2, yo), (px2 + 7.62, yo)); wire((px2 + 7.62, yo), (px2 + 7.62, yo - 2.54)); power('+1.2V_PLL', px2 + 7.62, yo - 2.54); pwr_flag(px2 + 7.62 + 5.08, yo); wire((px2 + 7.62, yo), (px2 + 7.62 + 5.08, yo)); junction((px2 + 7.62, yo))

# configuration link resistors and test points
bx, by = 162.56, 193.04; box('FPGA configuration link', bx, by, 142.24, 55.88)
y1 = by + 15.24
power('GND', bx + 7.62, y1 + 7.62); wire((bx + 7.62, y1), (bx + 7.62, y1 + 7.62)); tr = place('R28', bx + 17.78, y1, 0); wire((bx + 7.62, y1), tr['1'])
nx = bx + 30.48; wire(tr['2'], (nx, y1)); junction((nx, y1)); tp = place('TP1', nx, y1 - 5.08, 0); wire((nx, y1), tp['1']) if tp['1'][1] != y1 else None
wire((nx, y1), (bx + 40.64, y1)); glabel('FPGA_CRESET_N', bx + 40.64, y1, 0)
y2 = by + 33.02
power('+3.3V', bx + 7.62, y2 - 5.08); wire((bx + 7.62, y2 - 5.08), (bx + 7.62, y2)); tr = place('R29', bx + 17.78, y2, 180); wire((bx + 7.62, y2), tr['2'])
nx = bx + 30.48; wire(tr['1'], (nx, y2)); junction((nx, y2)); tp = place('TP2', nx, y2 - 5.08, 0); wire((nx, y2), tp['1']) if tp['1'][1] != y2 else None
wire((nx, y2), (bx + 40.64, y2)); glabel('FPGA_CDONE', bx + 40.64, y2, 0)
note('RGB0-2 (FPGA current-sink drivers, not plain GPIO) go straight to contacts 48/43/41; the v1 on-module LED is gone.', bx + 55.88, by + 48.26, 1.1)

# decoupling rows: caps hanging between a rail and GND
bx, by = 15.24, 256.54; box('Decoupling and supply filters', bx, by, 289.56, 63.5)
def cap_row(caps, rail, x, y, label):
    note(label, x, y - 5.08, 1.2)
    power(rail, x, y); wire((x, y), (x + 12.7 * (len(caps) - 1) + 0.0, y)) if len(caps) > 1 else None
    for i, ref in enumerate(caps):
        cx = x + 12.7 * i
        if i > 0: junction((cx, y))
        tc = place(ref, cx, y + 7.62, 270); wire((cx, y), tc['1']); wire(tc['2'], (cx, tc['2'][1] + 2.54)); power('GND', cx, tc['2'][1] + 2.54)
cap_row(['C33', 'C37', 'C38', 'C39', 'C40', 'C68', 'C46', 'C48', 'C52', 'C66', 'C60', 'C61', 'C67'], '+3.3V', bx + 12.7, by + 17.78, '+3.3V: ESP VDDPST1/2, VDDA1/2; flash VCC; FPGA VCCIO/VPP; input bulk at the card edge')
cap_row(['C49', 'C50'], '+1.2V', bx + 198.12, by + 17.78, 'FPGA VCC')
# ESP VDDA3P3 filter: L1 from +3.3V, then the three capacitors
x0, y0 = bx + 218.44, by + 17.78
power('+3.3V', x0, y0); tl = place('L1', x0 + 10.16, y0, 0); wire((x0, y0), tl['1'])
fx = tl['2'][0] + 2.54; wire(tl['2'], (fx, y0)); junction((fx, y0)); wire((fx, y0), (fx + 25.4, y0))
for i, ref in enumerate(['C34', 'C36', 'C35']):
    cx = fx + 12.7 * i
    if i > 0: junction((cx, y0))
    tc = place(ref, cx, y0 + 7.62, 270); wire((cx, y0), tc['1']); wire(tc['2'], (cx, tc['2'][1] + 2.54)); power('GND', cx, tc['2'][1] + 2.54)
wire((fx + 25.4, y0), (fx + 33.02, y0)); wire((fx + 33.02, y0), (fx + 33.02, y0 - 2.54)); power('ESP_VDD3P3', fx + 33.02, y0 - 2.54); pwr_flag(fx + 33.02 + 5.08, y0); wire((fx + 33.02, y0), (fx + 33.02 + 5.08, y0)); junction((fx + 33.02, y0))
note('ESP VDDA3P3 (pins 2, 3)', x0, y0 - 5.08, 1.2)
# power flags for the rails that enter from the card edge
pwr_flag(bx + 269.24, by + 45.72); wire((bx + 269.24, by + 45.72), (bx + 269.24, by + 43.18)); power('+3.3V', bx + 269.24, by + 43.18)
pwr_flag(bx + 279.4, by + 45.72); wire((bx + 279.4, by + 45.72), (bx + 279.4, by + 48.26)); power('GND', bx + 279.4, by + 48.26)
note('PWR_FLAGs: +3.3V and GND enter on card-edge contacts 2/4/70/72/74 and 1/3/9/15/21/27/39/45/51/57/71/73/75.', bx + 170.18, by + 58.42, 1.1)

# ---------------------------------------------------------------- write
missing = [r for r in parts if r not in placed]
assert not missing, ('unplaced parts', missing)
lib = ''.join(s.replace('(symbol "' + n + '"', '(symbol "Module2:' + n + '"', 1) for n, s in symbols.items())
(D / 'Module2.kicad_sym').write_text('(kicad_symbol_lib (version 20250114) (generator "kicad_symbol_editor") ' + ''.join(symbols.values()) + ')\n')
sch = (f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{uid("root")}") (paper "User" {sheet_w:.2f} {sheet_h:.2f}) '
       f'(title_block (title "ESP32-C6 + iCE40UP5K M.2 module v2") (rev "B - NOT FOR FABRICATION")) (lib_symbols {lib}) ' + ''.join(items) +
       f' (sheet_instances (path "/" (page "1"))))\n')
(D / 'module.kicad_sch').write_text(sch)
print('wrote schematic with', len(placed), 'parts')

# ---------------------------------------------------------------- verify against the contract
with tempfile.TemporaryDirectory() as td:
    out = Path(td) / 'net.xml'
    r = subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadxml', '-o', str(out), str(D / 'module.kicad_sch')], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    actual = {(p.get('ref'), p.get('pin')): n.get('name') for n in ET.parse(out).findall('./nets/net') for p in n.findall('node')}
    bad = []
    for ref, c in parts.items():
        for pin, expected in c['pins'].items():
            got = actual.get((ref, pin))
            if got != expected and not (expected is None and (got is None or got.startswith('unconnected-'))): bad.append((ref, pin, expected, got))
    assert not bad, bad[:20]
print('Circuit contract verified against the schematic netlist.')
