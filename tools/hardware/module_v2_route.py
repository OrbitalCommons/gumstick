#!/usr/bin/env python3
"""Hand routing for the ESP32-C6 + iCE40 M.2 module (v2).

Run after build_module_v2.py. Adds all copper (tracks, vias, the +1.2 V inner-layer island) to
boards/esp32-fpga-module-v2/module.kicad_pcb and saves it in place. Every segment is octilinear.

Layer plan
  F.Cu   component side: RF, crystal, QSPI link, CRESET/CDONE, decoupling, FPGA I/O that stays on top,
         odd (front) M.2 contacts
  In1    GND plane
  In2    +3.3 V plane with a +1.2 V island under the FPGA
  B.Cu   ESP signal bus (15 lanes, 0.25 mm pitch) down the east margin, FPGA I/O lanes to the even
         (back) M.2 contacts

Contact field: every front ground contact gets its own via 1.3 mm above the pad; the two back contacts
beside it step 0.15 mm away so the via clears them, then step back into their pads. All lanes arrive
as nested 45-degree fans (y + x = const, increasing eastwards) that end above the via row.
"""
import sys, json
from pathlib import Path
import pcbnew as p

R = Path(__file__).resolve().parents[2]
D = R / 'boards/esp32-fpga-module-v2'
PCB = D / 'module.kicad_pcb'

board = p.LoadBoard(str(PCB))
def mm(x): return int(round(x * 1e6))
def v(x, y): return p.VECTOR2I(mm(x), mm(y))
nets = {n: board.FindNet(n) for n in [ni.GetNetname() for ni in board.GetNetInfo().NetsByNetcode().values()] if n}
pads = {}
fingers = {}            # contact number -> (x, y, net)
for fp in board.GetFootprints():
    for pd in fp.Pads():
        key = f'{fp.GetReference()}.{pd.GetNumber()}'
        pads[key] = (p.ToMM(pd.GetPosition().x), p.ToMM(pd.GetPosition().y), pd.GetNetname())
        if fp.GetReference() == 'J1': fingers[int(pd.GetNumber())] = pads[key]
def P(name):
    x, y, _ = pads[name]; return (x, y)
def NET(name): return pads[name][2]
finger_of = {n: (x, y, k) for k, (x, y, n) in fingers.items()}

W_SIG, W_PWR, W_RF, W_LINK, W_BUS = 0.15, 0.25, 0.26, 0.15, 0.15
VIA_D, VIA_DR = 0.45, 0.2
stats = {'tracks': 0, 'vias': 0}

def T(net, pts, layer=p.F_Cu, w=W_SIG):
    """Polyline on one layer. Consecutive points must be octilinear."""
    assert net in nets, net
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 2e-3: dx = 0
        if abs(dy) < 2e-3: dy = 0
        if dx == 0 and dy == 0: continue
        assert dx == 0 or dy == 0 or abs(abs(dx) - abs(dy)) < 2e-3, f'{net}: non-octilinear {a}->{b}'
        t = p.PCB_TRACK(board); t.SetStart(v(*a)); t.SetEnd(v(*b)); t.SetWidth(mm(w)); t.SetLayer(layer); t.SetNet(nets[net]); board.Add(t)
        stats['tracks'] += 1

def V(net, x, y, d=VIA_D):
    assert net in nets, net
    via = p.PCB_VIA(board); via.SetPosition(v(x, y)); via.SetDrill(mm(VIA_DR)); via.SetWidth(mm(d)); via.SetViaType(p.VIATYPE_THROUGH)
    via.SetLayerPair(p.F_Cu, p.B_Cu); via.SetNet(nets[net]); board.Add(via); stats['vias'] += 1
    return (x, y)

def pin_via(net, pad, via_xy, layer=p.F_Cu, w=W_SIG, d=VIA_D):
    """Straight stub from a pad to a via (same x or y)."""
    T(net, [P(pad), via_xy], layer, w); V(net, *via_xy, d)

F, B = p.F_Cu, p.B_Cu
GND, V33, V12, PLL, VDDA = 'GND', '+3.3V', '+1.2V', '+1.2V_PLL', 'ESP_VDD3P3'

# ============================================================== +1.2 V island on In2 under the FPGA
z = p.ZONE(board); z.SetNet(nets[V12]); z.SetLayer(p.In2_Cu); z.SetAssignedPriority(2)
z.SetPadConnection(p.ZONE_CONNECTION_THERMAL); z.SetThermalReliefGap(mm(0.15)); z.SetThermalReliefSpokeWidth(mm(0.15))
z.SetLocalClearance(mm(0.15)); z.SetMinThickness(mm(0.1)); z.SetZoneName('+1.2V island')
ol = z.Outline(); ol.NewOutline()
for x, y in [(102.7, 127.4), (116.2, 127.4), (116.2, 133.8), (107.3, 133.8), (107.3, 131.0), (105.5, 131.0), (105.5, 130.6), (102.7, 130.6)]: ol.Append(mm(x), mm(y))   # west lobe carries the regulator trunk; notch keeps the pin-33 plane via (106.75) outside
board.Add(z)

# ============================================================== exposed pads: ground vias
for x, y in [(110.3, 112.8), (111.7, 112.8), (110.3, 114.2), (111.7, 114.2), (110.75, 129.2), (112.3, 129.2), (110.75, 131.8), (112.3, 131.8)]:
    V(GND, x, y)

# ============================================================== ESP32-C6 power
# VDDA3P3 (pins 2, 3): filter column west of U1, bused on x = 105.3 through C35/C36/C34 to the bead L1.
T(VDDA, [P('U1.3'), (105.3, 112.75)], F, 0.25)
T(VDDA, [P('U1.2'), (107.8, 112.25), (107.55, 112.5), (105.3, 112.5), (105.3, 116.75)], F, 0.25)   # bus through C35.1, C36.1, C34.1 to L1.2
for pad, via in (('C35.2', (103.6, 112.75)), ('C36.2', (103.6, 113.85)), ('C34.2', (102.95, 115.2))): pin_via(GND, pad, via, F, 0.25)
pin_via(V33, 'L1.1', (102.95, 116.75), F, 0.25)
# VDDPST1 (pin 5) -> C37; EN RC: R22/C32 share the EN via (in-line) and R22's 3.3 V via sits west of it
T(V33, [P('U1.5'), P('C37.1')], F, 0.2)
pin_via(V33, 'C37.1', (106.1, 113.75), F, 0.2)
pin_via(GND, 'C37.2', (106.7, 115.45), F, 0.2)
T(V33, [P('R22.2'), (106.1, 116.1925)], F, 0.15); V(V33, 106.1, 116.1925)
T('ESP_EN', [P('R22.1'), P('C32.1')], F, 0.15); V('ESP_EN', 106.7, 117.865)
pin_via(GND, 'C32.2', (106.7, 120.2), F, 0.2)
# CHIP_PU (pin 4) leaves west, drops to B.Cu, feeds the RC column and the bus (lane 0)
T('ESP_EN', [P('U1.4'), (107.5, 113.25)], F); V('ESP_EN', 107.5, 113.25)
T('ESP_EN', [(107.5, 113.25), (107.5, 120.9), (116.3, 120.9)], B, W_BUS)
T('ESP_EN', [(107.5, 117.865), (106.7, 117.865)], B, W_BUS)
# VDDA1/VDDA2 (pins 29, 32): C39 above pin 29 via a 0.4 mm via, C40 west of pin 32 on a short bar
T(V33, [P('U1.32'), (109.25, 110.15), P('C40.1')], F, 0.15)
pin_via(V33, 'C40.1', (108.0846, 109.3), F, 0.15)
pin_via(GND, 'C40.2', (107.1154, 109.4), F, 0.2)
T(V33, [P('U1.29'), (110.75, 110.3), P('C39.1')], F, 0.2); V(V33, 110.75, 110.3, 0.4)
# C39.2 returns through the front pour around the crystal (no via fits between XTAL_N and the GPIO23 drop)
# VDDPST2 (pin 20) -> C38 east of U1
T(V33, [P('U1.20'), P('C38.1')], F, 0.2); V(V33, 114.75, 113.75)
T(GND, [P('C38.2'), (117.1, 113.75)], F, 0.2); V(GND, 117.1, 113.75)
# bulk 3.3 V at the NE corner (plane caps)
pin_via(V33, 'C33.1', (113.5, 105.775), F, 0.25); pin_via(GND, 'C33.2', (113.5, 104.225), F, 0.25)
for c in ('C66', 'C60', 'C61', 'C67'):
    x1, y1 = P(c + '.1'); x2, y2 = P(c + '.2')
    pin_via(V33, c + '.1', (x1, 106.0), F, 0.25); pin_via(GND, c + '.2', (x2, 102.3), F, 0.25)

# ============================================================== RF front end
T('RF_IN', [P('U1.1'), P('C1.1')], F, W_RF)
T('RF_IN', [P('C1.1'), P('L3.1')], F, W_RF)
T('RF_ANT', [P('L3.2'), P('C2.1')], F, W_RF)
T('RF_ANT', [(104.95, 111.75), P('J3.1')], F, W_RF)
pin_via(GND, 'C1.2', (106.3, 110.7808), F, 0.2)
pin_via(GND, 'C2.2', (104.35, 110.0), F, 0.2)
pin_via(GND, 'J3.2', (106.425, 104.4), F, 0.25)

# ============================================================== crystal
T('XTAL_P', [P('U1.31'), P('L5.1')], F)
T('XTAL_P_CRYSTAL', [P('L5.2'), (109.75, 107.775)], F)
T('XTAL_P_CRYSTAL', [P('C6.1'), P('Y1.IN/OUT')], F)
pin_via(GND, 'C6.2', (108.3, 106.0), F)
T('XTAL_N', [P('U1.30'), (110.25, 106.225), P('Y1.OUT/IN')], F)
T('XTAL_N', [P('Y1.OUT/IN'), P('C7.1')], F)
pin_via(GND, 'C7.2', (112.6, 107.75), F)
pin_via(GND, 'Y1.GND-A', (109.475, 105.3), F, 0.2)

# ============================================================== QSPI link U1 -> U2 (F.Cu, uncrossed)
# left-column pins leave west and turn south; bottom pins go straight south; all meet U2's top row with 45 deg legs.
# Legs are y - x = k with k stepping 0.45 so parallel legs keep the Link clearance.
for net, a, b, col, k in (('FPGA_SPI_IO3', 'U1.6', 'U2.18', 107.2, 14.05), ('FPGA_SPI_MOSI', 'U1.7', 'U2.17', 107.56, 13.6), ('FPGA_SPI_CS_N', 'U1.8', 'U2.16', 107.92, 13.15)):
    ax, ay = P(a); bx, by = P(b)
    T(net, [(ax, ay), (col, ay), (col, k + col), (bx, k + bx), (bx, by)], F, W_LINK)
for net, a, b, k in (('FPGA_SPI_SCK', 'U1.9', 'U2.15', 12.7), ('FPGA_SPI_MISO', 'U1.12', 'U2.14', 12.25), ('FPGA_SPI_IO2', 'U1.13', 'U2.13', 11.8)):
    ax, ay = P(a); bx, by = P(b)
    T(net, [(ax, ay), (ax, k + ax), (bx, k + bx), (bx, by)], F, W_LINK)

# ============================================================== CRESET / CDONE (F.Cu runs east of U1, B.Cu legs into U2)
CR, CD = 'FPGA_CRESET_N', 'FPGA_CDONE'
T(CR, [P('U1.18'), (117.5, 114.75), (117.5, 126.0), (117.2, 126.3)], F); V(CR, 117.2, 126.3)
T(CR, [(117.2, 126.3), (115.25, 128.25), (115.25, 129.75)], B); V(CR, 115.25, 129.75)
T(CR, [P('U2.8'), (115.25, 129.75)], F)
T(CR, [P('R28.2'), (117.5, 124.4)], F); pin_via(GND, 'R28.1', (115.0, 124.4), F)
T(CR, [P('TP1.1'), (117.5, 122.2)], F); T(CD, [P('TP2.1'), (118.0, 120.6)], F)
T(CD, [P('U1.23'), (118.0, 112.25), (118.0, 126.6), (117.7, 126.9)], F); V(CD, 117.7, 126.9)
T(CD, [(117.7, 126.9), (115.95, 128.65), (115.95, 130.25)], B); V(CD, 115.95, 130.25)
T(CD, [P('U2.7'), (115.95, 130.25)], F)
T(CD, [(116.9, 112.25), P('R29.1')], F); pin_via(V33, 'R29.2', (116.9, 109.9), F)

# ============================================================== contact field geometry
GND_FINGERS = {1, 3, 9, 15, 21, 27, 33, 39, 45, 51, 57, 71, 73, 75}
Y_GVIA, Y_JOG, Y_END_MAX = 138.7, 139.0, 138.2
def squeezed_x(n):
    """Back-contact lane x near the pads: step 0.15 mm away from an adjacent front ground contact."""
    x = fingers[n][0]
    if n - 1 in GND_FINGERS and n + 1 in GND_FINGERS: raise ValueError(n)      # handled by hand (power contacts)
    if n - 1 in GND_FINGERS: return x - 0.15           # n-1 is east (x falls with n)
    if n + 1 in GND_FINGERS: return x + 0.15
    return x
def back_entry(net, n, lane_x, c):
    """B.Cu lane from (lane_x, c - lane_x) south-west along y + x = c to the squeezed column, then into pad n."""
    fx, fy, _ = fingers[n]; sx = squeezed_x(n)
    y_turn, y_end = c - lane_x, c - sx
    assert y_end <= Y_END_MAX + 1e-6, (net, n, y_end)
    assert abs(lane_x - sx) < 1e-6 or lane_x > sx, (net, n, lane_x, sx)
    pts = [(lane_x, y_turn), (sx, y_end), (sx, Y_JOG), (fx, Y_JOG + abs(fx - sx)), (fx, fy)]
    T(net, pts, B, W_BUS)
    return y_turn

# ============================================================== ESP signal bus (B.Cu)
# feeders: (net, via x, via y, feeder level y, lane x, miter x); each feeder runs east on its level to the miter x, then takes a
# 45-degree leg into its lane. Legs are y - x = level - miter_x, nested (stepping >= 0.36 mm) so none cross; the miter x values
# keep the legs 0.4 mm off the R20/R21/C38/R29 vias. Lanes are ordered west->east, so are their contacts (34 .. 6).
bus = [('ESP_EN',          None,  None,  120.9, 118.1, 116.3),
       ('ESP_GPIO4',       109.75, 117.0, 120.4, 118.35, 116.3),
       ('ESP_GPIO5',       110.25, 117.8, 119.9, 118.6, 116.3),
       ('ESP_GPIO8',       111.75, 117.0, 119.4, 118.85, 116.3),
       ('ESP_GPIO9_BOOT',  112.25, 117.8, 118.9, 119.1, 116.3),
       ('USB_D-',          112.75, 117.0, 118.4, 119.35, 116.3),
       ('USB_D+',          115.0, 115.25, 115.25, 119.6, 115.0),
       ('ESP_GPIO15',      114.3, 114.25, 114.25, 119.85, 114.65),
       ('ESP_GPIO16_TXD',  114.3, 113.25, 113.25, 120.1, 115.0),
       ('ESP_GPIO17_RXD',  115.0, 112.75, 112.75, 120.35, 115.0),
       ('ESP_GPIO19',      114.3, 111.75, 111.75, 120.6, 115.7),
       ('ESP_GPIO20',      112.75, 110.3, 110.3, 120.85, 114.8),
       ('ESP_GPIO21',      112.25, 109.0, 109.3, 121.1, 114.3),
       ('ESP_GPIO22',      111.75, 109.6, 108.55, 121.35, 114.05),
       ('ESP_GPIO23',      111.25, 110.3, 108.3, 121.6, 114.3)]
esp_pad = {'ESP_GPIO4': 'U1.10', 'ESP_GPIO5': 'U1.11', 'ESP_GPIO8': 'U1.14', 'ESP_GPIO9_BOOT': 'U1.15', 'USB_D-': 'U1.16', 'USB_D+': 'U1.17',
           'ESP_GPIO15': 'U1.19', 'ESP_GPIO16_TXD': 'U1.21', 'ESP_GPIO17_RXD': 'U1.22', 'ESP_GPIO19': 'U1.24', 'ESP_GPIO20': 'U1.25',
           'ESP_GPIO21': 'U1.26', 'ESP_GPIO22': 'U1.27', 'ESP_GPIO23': 'U1.28'}
C_ESP0, DC = 249.75, 0.36
prev_c = None
for k, (net, vx, vy, lvl, lane, xt) in enumerate(bus):
    if vx is not None:
        px, py = P(esp_pad[net])
        T(net, [(px, py), (vx, vy)] if (px == vx or py == vy) else [(px, py), (px, vy), (vx, vy)], F)   # straight pin exit to the via
        V(net, vx, vy, 0.4 if net == 'ESP_GPIO23' else VIA_D)
        if vy == lvl: T(net, [(vx, vy), (xt, lvl)], B, W_BUS)
        else:         T(net, [(vx, vy), (vx, lvl), (xt, lvl)], B, W_BUS)
    c = lvl - xt                                                     # leg y - x = c; must fall by >= 0.36 per lane outwards
    assert prev_c is None or c <= prev_c - 0.36 + 1e-6 or k <= 5 and c >= prev_c + 0.36 - 1e-6, (net, c, prev_c)
    prev_c = c
    y_in = lvl + (lane - xt)
    n = finger_of[net][2]
    y_turn = back_entry(net, n, lane, C_ESP0 + DC * k)
    assert y_turn > y_in, (net, y_turn, y_in)
    T(net, [(xt, lvl), (lane, y_in), (lane, y_turn)], B, W_BUS)

# R20 / R21 pull-ups hang off the GPIO9 / GPIO8 feeders through in-line vias
T('ESP_GPIO9_BOOT', [P('R20.1'), (115.0, 118.9)], F); V('ESP_GPIO9_BOOT', 115.0, 118.9)
pin_via(V33, 'R20.2', (115.0, 116.5), F)
T('ESP_GPIO8', [P('R21.1'), (116.0, 119.4)], F); V('ESP_GPIO8', 116.0, 119.4)
pin_via(V33, 'R21.2', (116.0, 117.0), F)

# ============================================================== FPGA power / decoupling
# top row: pins 22 and 24 share a short 3.3 V bar with C52
T(V33, [P('U2.24'), (108.25, 125.6)], F, 0.2); T(V33, [P('U2.22'), (109.25, 125.6)], F, 0.2)
T(V33, [P('C52.1'), (109.25, 125.6)], F, 0.2); pin_via(V33, 'C52.1', (107.9846, 124.7), F, 0.2)
pin_via(GND, 'C52.2', (106.4, 125.6), F, 0.2)
# west column: PLL (29) and VCC (30) lines run west past the I/O via columns to C44 / C49
T(PLL, [P('U2.29'), (104.6846, 129.75), P('C44.1')], F, 0.15)           # 0.15 wide: C49 sits 0.11 mm below the pin-29 line
T(PLL, [(104.6846, 128.4), P('C44.1')], F, 0.15); V(PLL, 104.6846, 128.4)
pin_via(GND, 'C44.2', (103.7154, 128.5), F, 0.2)
T(V12, [P('U2.30'), P('C49.1')], F, 0.25)                             # C49 sits on the pin line, 1.9 mm from the pad
V(V12, 106.75, 130.25)                                                   # island feed, on the pin-30 line (zig-zag column A)
pin_via(GND, 'C49.2', (104.615, 131.1), F, 0.2)
# VCCIO_0 (33): plane via at the exit, cap further west
T(V33, [P('U2.33'), (106.75, 131.75)], F, 0.2); V(V33, 106.75, 131.75)    # column A; the island wall sits at 107.3
pin_via(V33, 'C46.1', (103.7846, 131.0), F, 0.2)
pin_via(GND, 'C46.2', (102.0, 131.75), F, 0.2)
# east column: VCCIO_2 (1) south to C48, VCC (5) east to the island. C48.2/C50.2 return through the front pour
# (the back-contact fan passes under them); the pour region holds the contact-27 ground via.
T(V33, [P('U2.1'), P('C48.1')], F, 0.2); V(V33, 114.48, 134.4)
T(V12, [P('U2.5'), (115.45, 131.25)], F, 0.25); V(V12, 115.45, 131.25)
T(V12, [(115.45, 133.3), P('C50.1')], F, 0.2); V(V12, 115.45, 133.3)

# ============================================================== 1.2 V regulator (NW cluster)
T(V33, [P('U3.1'), P('C62.1')], F, 0.25); pin_via(V33, 'C62.1', (103.8, 119.0), F, 0.25)
pin_via(GND, 'C62.2', (100.6, 119.0), F, 0.25)
pin_via(GND, 'U3.2', (102.0, 119.9), F, 0.25)
T(V33, [P('U3.3'), (101.05, 121.7), (100.55, 122.2)], F, 0.25); V(V33, 100.55, 122.2)
T(V12, [P('U3.5'), (102.95, 129.3)], F, W_PWR); V(V12, 102.95, 129.3)   # trunk through C63.1 and C45.1 into the island's west lobe
pin_via(GND, 'C63.2', (105.2, 125.0), F, 0.25)
pin_via(GND, 'C45.2', (105.2, 126.6), F, 0.25)
T(V12, [(102.95, 125.7125), P('L2.1')], F, 0.25)
T(PLL, [P('L2.2'), P('C43.1')], F, 0.25); V(PLL, 101.0, 128.13)
T(PLL, [(101.0, 128.13), (101.43, 127.7), (104.6846, 127.7), (104.6846, 128.4)], B, 0.2)
pin_via(GND, 'C43.2', (101.0, 131.4), F, 0.25)

# ============================================================== FPGA I/O: east column (F.Cu columns -> odd contacts)
east = [('U2.2', 116.35), ('U2.3', 116.75), ('U2.4', 117.15), ('U2.6', 117.55), ('U2.9', 117.95), ('U2.10', 118.35), ('U2.11', 118.75), ('U2.12', 119.25)]
for i, (pad, col) in enumerate(east):
    net = NET(pad); px, py = P(pad); fx, fy, _ = finger_of[net]
    c = 252.45 + 0.4 * i
    if abs(fx - col) < 1e-6: T(net, [(px, py), (col, py), (col, fy)], F)
    else:
        assert c - fx <= Y_END_MAX + 1e-6, (pad, c - fx)
        T(net, [(px, py), (col, py), (col, c - col), (fx, c - fx), (fx, fy)], F)
# bottom row: straight drops on F.Cu
for pad in ('U2.37', 'U2.38', 'U2.40', 'U2.41', 'U2.43', 'U2.44', 'U2.46', 'U2.47'):
    net = NET(pad); px, py = P(pad); fx, fy, _ = finger_of[net]; assert abs(fx - px) < 1e-6, (pad, fx, px)
    T(net, [(px, py), (fx, fy)], F)
# bottom row via drops and top row vias -> B.Cu lanes under the package -> even contacts (nested SW fan)
lanes = [('U2.23', 108.75, 126.1, 108.75, 246.0), ('U2.39', 109.25, 135.3, 109.25, 246.36), ('U2.21', 109.75, 126.1, 109.75, 246.72),
         ('U2.20', 110.25, 125.0, 110.25, 247.08), ('U2.42', 110.75, 135.3, 110.75, 247.44), ('U2.19', 110.75, 126.1, 111.25, 247.8),
         ('U2.45', 112.25, 135.3, 112.25, 249.0), ('U2.48', 113.75, 135.3, 113.75, 249.36)]
for pad, vx, vy, lane, c in lanes:
    net = NET(pad); px, py = P(pad); n = finger_of[net][2]
    T(net, [(px, py), (vx, vy)], F); V(net, vx, vy)
    if lane != vx: T(net, [(vx, vy), (vx, vy + 0.3), (lane, vy + 0.3 + abs(lane - vx))], B, W_BUS); y0 = vy + 0.3 + abs(lane - vx)
    else: y0 = vy
    y_turn = back_entry(net, n, lane, c)
    assert y_turn >= y0 + 0.3, (pad, y_turn, y0)
    T(net, [(lane, y0), (lane, y_turn)], B, W_BUS)
# west column: a tight zig-zag, columns A (x 106.75) and B (x 106.2) alternating pin by pin: 25 A, 26 B, 27 A, 28 B, 30 A (island
# feed), 31 B, 33 A (plane via). Pins 25/27 lane east (SW fans), 26/28/31 lane west; 28 and 31 re-enter their contacts with SE legs.
# Pins 32, 34, 35, 36 stay on F.Cu and drop to the odd contacts 69, 67, 55, 53.
west = [('U2.25', 106.75, 107.85, 245.1), ('U2.26', 106.2, 105.2, 241.7), ('U2.27', 106.75, 107.5, 244.3), ('U2.28', 106.2, 105.55, 243.3), ('U2.31', 106.2, 105.9, 243.6)]
for pad, vx, lane, c in west:
    net = NET(pad); px, py = P(pad); n = finger_of[net][2]
    T(net, [(px, py), (vx, py)], F); V(net, vx, py)
    d = abs(lane - vx)
    y0 = py + d
    if d: T(net, [(vx, py), (lane, y0)], B, W_BUS)                 # 45-degree leg straight off the via
    fx = fingers[n][0]; sx = squeezed_x(n)
    if sx > lane:                                   # contacts 58 / 56 lie east of lanes 28 / 31: south-east leg instead
        y_turn = c - lane; y_end = y_turn + (sx - lane)
        T(net, [(lane, y0), (lane, y_turn), (sx, y_end), (sx, Y_JOG), (fx, Y_JOG + abs(fx - sx)), (fx, fingers[n][1])], B, W_BUS)
    else:
        y_turn = back_entry(net, n, lane, c)
        T(net, [(lane, y0), (lane, y_turn)], B, W_BUS)
for pad, col, c in (('U2.32', 105.95, 241.15), ('U2.34', 106.35, 241.55)):          # SW legs y + x = c
    net = NET(pad); px, py = P(pad); fx, fy, _ = finger_of[net]
    T(net, [(px, py), (col, py), (col, c - col), (fx, c - fx), (fx, fy)], F)
for pad, col in (('U2.35', 106.75), ('U2.36', 107.1)):
    net = NET(pad); px, py = P(pad); fx, fy, _ = finger_of[net]
    if pad == 'U2.35': T(net, [(px, py), (col, py), (col, fy)], F)
    else: T(net, [(px, py), (px, 133.7), (col, 133.7 + (px - col)), (col, 139.0), (fx, 139.0 + abs(fx - col)), (fx, fy)], F)

# ============================================================== M.2 ground and power contacts
# front ground contacts: stub north to a via (3 and 73 reach the pour region that holds the neighbouring via)
for n in (9, 15, 21, 27, 33, 39, 45, 51, 57):
    fx, fy, _ = fingers[n]; T(GND, [(fx, fy), (fx, Y_GVIA)], F); V(GND, fx, Y_GVIA)
V(GND, 120.4, 137.7); V(GND, 101.6, 137.7)          # contacts 1/3 and 71/73/75 join the front pour at the board ends
# back power contacts weave past the ground vias (0.15 mm lanes), then drop to the 3.3 V plane
def stub(n, pts, via):
    fx, fy, _ = fingers[n]; T(V33, [(fx, fy)] + pts, B, W_BUS); V(V33, *via)
stub(2,  [(120.0, 138.3)], (120.0, 138.3))
fx4, fy4, _ = fingers[4]; T(V33, [(fx4, fy4), (119.5, 139.3), (119.625, 139.175)], B, W_BUS); V(V33, 119.625, 139.175, 0.4)
stub(70, [(103.0, 137.0)], (103.0, 137.0))
stub(72, [(102.5, 137.6)], (102.5, 137.6))
stub(74, [(102.0, 138.3)], (102.0, 138.3))
# plane stitching in open areas
for xy in [(113.0, 103.0), (110.5, 104.5), (107.0, 103.5), (102.5, 104.0), (100.9, 110.0), (100.9, 114.5), (106.0, 121.5), (108.8, 119.8),
           (113.8, 123.6), (100.9, 134.5), (102.3, 135.5), (121.3, 106.8)]:
    V(GND, *xy)

def merge_collinear():
    tracks = [t for t in board.GetTracks() if t.GetClass() == 'PCB_TRACK']
    def key(pt): return (pt.x, pt.y)
    ends = {}
    for t in tracks:
        for pt in (t.GetStart(), t.GetEnd()): ends.setdefault(key(pt), []).append(t)
    merged = 0; changed = True
    while changed:
        changed = False
        for pt, ts in list(ends.items()):
            ts = [t for t in ts if t in tracks]
            if len(ts) != 2: continue
            a, b = ts
            if a.GetNetCode() != b.GetNetCode() or a.GetLayer() != b.GetLayer() or a.GetWidth() != b.GetWidth(): continue
            pa = a.GetEnd() if key(a.GetStart()) == pt else a.GetStart()
            pb = b.GetEnd() if key(b.GetStart()) == pt else b.GetStart()
            cross = (pa.x - pt[0]) * (pb.y - pt[1]) - (pa.y - pt[1]) * (pb.x - pt[0])
            dot = (pa.x - pt[0]) * (pb.x - pt[0]) + (pa.y - pt[1]) * (pb.y - pt[1])
            if cross != 0 or dot >= 0: continue
            a.SetStart(pa); a.SetEnd(pb); board.Remove(b); tracks.remove(b)
            ends[key(pb)] = [a if t is b else t for t in ends[key(pb)]]; ends[pt] = []
            merged += 1; changed = True; break
    stats['merged'] = merged
merge_collinear()
filler = p.ZONE_FILLER(board); filler.Fill(board.Zones())
board.Save(str(PCB))

# ---------------------------------------------------------------- lint policy: via roles and the finger-strip edge margin
# Via UUIDs are regenerated on every build, so the roles map is rewritten here rather than hand-maintained.
LINT = D / 'module.lint.json'
pol = json.load(open(LINT)) if LINT.exists() else {}
intent = pol.setdefault('config', {}).setdefault('intent', {})
intent.setdefault('route', {})['edge_clearance_mm'] = 0.14          # M.2 fingers end 0.15 mm inside the routed edge (0.3 mm elsewhere via the DRU)
ep = {'U1': (111.0, 113.5, 1.85), 'U2': (111.0, 130.5, 1.9)}
cap_gnd = [(p.ToMM(pd.GetPosition().x), p.ToMM(pd.GetPosition().y)) for fp in board.GetFootprints() if fp.GetReference()[0] in 'CR' for pd in fp.Pads() if pd.GetNetname() == 'GND']
roles = {}
for t in board.GetTracks():
    if t.GetClass() != 'PCB_VIA': continue
    x, y = p.ToMM(t.GetPosition().x), p.ToMM(t.GetPosition().y); n = t.GetNetname()
    if n == 'GND':
        if any(abs(x - cx) <= h and abs(y - cy) <= h + 0.7 for cx, cy, h in ep.values()): role = 'thermal'
        elif any(abs(x - gx) < 1.6 and abs(y - gy) < 1.6 for gx, gy in cap_gnd): role = 'return'
        elif y > 136: role = 'return'                                   # contact-field ground vias
        else: role = 'stitching'
    elif n in ('+3.3V', '+1.2V', '+1.2V_PLL'): role = 'feed'
    else: continue
    roles[str(t.m_Uuid.AsString())] = role
intent['roles'] = roles
json.dump(pol, open(LINT, 'w'), indent=2); open(LINT, 'a').write('\n')
stats['roles'] = len(roles)
print('routed:', stats)
