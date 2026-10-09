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

W_SIG, W_PWR, W_RF, W_LINK, W_BUS = 0.15, 0.25, 0.14, 0.15, 0.15   # W_RF: 50 ohm coated CPWG, 0.15 gap, JLC04081H-3313 (docs/rf-feed.json)
M_FEED = 0.8                    # corner miter on the nested ESP feeders (EN .. D-)
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
for x, y in [(110.3, 113.3), (111.7, 113.3), (110.3, 114.7), (111.7, 114.7), (110.75, 129.2), (112.3, 129.2), (110.75, 131.8), (112.3, 131.8)]:
    V(GND, x, y)

# ============================================================== ESP32-C6 (QFN40) power
# U1 at (111, 114), 0.4 mm pitch: left pads x 108.56 (pins 1-10, y 112.2..115.8), bottom y 116.44 (11-20, x 109.2..112.8),
# right x 113.44 (21-30, y 115.8..112.2), top y 111.56 (31-40, x 112.8..109.2).
# VDDA3P3 (pins 2, 3): bus on x = 105.0 through C35/C36/C34 to the bead L1
T(VDDA, [P('U1.3'), (105.0, 113.0)], F, 0.15)
T(VDDA, [P('U1.2'), (107.8, 112.6), (107.4, 113.0)], F, 0.15)
T(VDDA, [(105.0, 113.0), (105.0, 117.25)], F, 0.25)
for pad, via in (('C35.2', (103.3, 113.35)), ('C36.2', (103.3, 114.35)), ('C34.2', (102.65, 115.7))): pin_via(GND, pad, via, F, 0.25)
pin_via(V33, 'L1.1', (102.65, 117.25), F, 0.25)
# CHIP_PU (pin 4) -> via between the VDDA and VDDPST1 lines; EN runs on B.Cu (x 107.3) and feeds the RC west of the link columns
T('ESP_EN', [P('U1.4'), (107.7, 113.4)]); V('ESP_EN', 107.7, 113.4)
T('ESP_EN', [(107.7, 113.4), (107.3, 113.8), (107.3, 121.6 - M_FEED), (107.3 + M_FEED, 121.6), (115.4, 121.6)], B, W_BUS)
T('ESP_EN', [(107.3, 119.62), (105.9, 119.62)], B, W_BUS); V('ESP_EN', 105.9, 119.62)
T('ESP_EN', [P('R22.1'), P('C32.1')], F, 0.15)
pin_via(V33, 'R22.2', (105.9, 117.4), F, 0.2)
pin_via(GND, 'C32.2', (105.9, 121.75), F, 0.2)
# VDDPST1 (pin 5) -> C37 west of the link columns, plane via on the line
T(V33, [P('U1.5'), P('C37.1')], F, 0.15); V(V33, 106.9, 113.8)
pin_via(GND, 'C37.2', (105.9, 115.45), F, 0.2)
# VDDA2 (pin 40) turns west onto C40; VDDA1 (pin 37) drops into a 0.4 mm plane via with C39 (0201) on the pin line above it
T(V33, [P('U1.40'), (109.2, 111.0), (108.7, 111.0)], F, 0.15)
T(V33, [P('C40.1'), (108.0, 110.785)], F, 0.15); V(V33, 108.0, 110.785)
pin_via(GND, 'C40.2', (108.7, 109.15), F, 0.2)
T(V33, [P('U1.37'), P('C39.1')], F, 0.15); V(V33, 110.4, 110.85, 0.4)
pin_via(GND, 'C39.2', (110.4, 109.15), F, 0.15)
# VDDPST2 (pin 28) runs east between the TXD and GPIO15 vias, then north to C38; its vias sit between the B.Cu bus legs
T(V33, [P('U1.28'), (115.35, 113.0), P('C38.1')], F, 0.15)
T(V33, [(115.35, 112.25), (115.65, 112.25)], F, 0.15); V(V33, 115.65, 112.25)   # c = -3.4 midline (RXD / GPIO18 legs)
pin_via(GND, 'C38.2', (115.35, 110.15), F, 0.15)       # on the c = -5.2 midline between the GPIO19 and GPIO20 legs
# C33: 10 uF on the ESP side of the 3.3 V plane (plane cap)
pin_via(V33, 'C33.1', (113.2, 105.775), F, 0.25); pin_via(GND, 'C33.2', (113.2, 104.225), F, 0.25)
# input bulk at the power contacts: each 3.3 V pad runs into its contact's In2 via, each ground pad has its own via
T(V33, [P('C67.1'), (103.0, 137.0)], F, 0.25)                                 # contact 70
T(V33, [P('C60.1'), (101.4, 136.5), (102.5, 137.6)], F, 0.25)                 # contact 72
T(V33, [P('C61.1'), (120.0, 136.675), (120.0, 138.3)], F, 0.25)               # contact 2 (west exit, then straight down)
pin_via(GND, 'C67.2', (103.0, 133.2), F, 0.25); pin_via(GND, 'C60.2', (101.4, 133.2), F, 0.25)
# C66 feeds past C61 on its west side into the same contact via; the ESP bus lanes end at x 120.15, so both ground pads get vias
T(V33, [P('C66.1'), (119.6, 133.575), (119.6, 136.275), (120.0, 136.675)], F, 0.25)
pin_via(GND, 'C66.2', (120.55, 131.2), F, 0.25); pin_via(GND, 'C61.2', (120.55, 134.35), F, 0.25)

# ============================================================== RF front end
T('RF_IN', [P('U1.1'), P('C1.1')], F, W_RF)
T('RF_IN', [P('C1.1'), P('L3.1')], F, W_RF)
T('RF_ANT', [P('L3.2'), P('C2.1')], F, W_RF)
T('RF_ANT', [(104.95, 112.2), P('J3.1')], F, W_RF)
pin_via(GND, 'C1.2', (106.3, 111.23), F, 0.2)
pin_via(GND, 'C2.2', (104.35, 110.5), F, 0.2)
pin_via(GND, 'J3.2', (106.425, 104.4), F, 0.25)

# ============================================================== crystal
T('XTAL_P', [P('U1.39'), P('L5.1')], F)
T('XTAL_P_CRYSTAL', [P('L5.2'), (109.6, 108.0)], F)                            # straight up into the crystal's IN/OUT pad
T('XTAL_P_CRYSTAL', [P('C6.1'), P('Y1.IN/OUT')], F)
pin_via(GND, 'C6.2', (108.3, 106.0), F)
T('XTAL_N', [P('U1.38'), (110.0, 108.65), (110.25, 108.4), (110.25, 106.225), P('Y1.OUT/IN')], F)   # passes under the crystal body
T('XTAL_N', [P('Y1.OUT/IN'), P('C7.1')], F)
pin_via(GND, 'C7.2', (112.6, 107.75), F)
pin_via(GND, 'Y1.GND-A', (109.475, 105.3), F, 0.2)

# ============================================================== QSPI link U1 -> U2 (F.Cu, uncrossed)
# GPIO0-3 leave the left side and turn south in columns; GPIO6/7 drop from the bottom row. All meet U2's top row with 45 deg legs
# y - x = k (stepping 0.45 so parallel legs keep the Link clearance).
for net, a, b, col, k in (('FPGA_SPI_IO3', 'U1.6', 'U2.18', 106.42, 14.05), ('FPGA_SPI_MOSI', 'U1.7', 'U2.17', 106.78, 13.6),
                          ('FPGA_SPI_CS_N', 'U1.8', 'U2.16', 107.14, 13.15), ('FPGA_SPI_SCK', 'U1.9', 'U2.15', 107.5, 12.7)):
    ax, ay = P(a); bx, by = P(b)
    T(net, [(ax, ay), (col, ay), (col, k + col), (bx, k + bx), (bx, by)], F, W_LINK)
for net, a, b, k in (('FPGA_SPI_MISO', 'U1.12', 'U2.14', 12.25), ('FPGA_SPI_IO2', 'U1.13', 'U2.13', 11.8)):
    ax, ay = P(a); bx, by = P(b)
    T(net, [(ax, ay), (ax, k + ax), (bx, k + bx), (bx, by)], F, W_LINK)

# ============================================================== CRESET / CDONE (GPIO10/11 on the bottom row)
# Both drop between the bus vias, turn east above the link legs, run down x 117.5 / 118.0 and turn west to vias on the pin-8 / pin-7
# via columns; the B.Cu hops are straight drops into U2.
CR, CD = 'FPGA_CRESET_N', 'FPGA_CDONE'
T(CR, [P('U1.16'), (111.2, 118.8), (117.5, 118.8), (117.5, 125.6), (115.25, 125.6)], F); V(CR, 115.25, 125.6)
T(CR, [(115.25, 125.6), (115.25, 129.75)], B); V(CR, 115.25, 129.75)
T(CR, [P('U2.8'), (115.25, 129.75)], F)
T(CR, [P('R28.2'), (117.5, 124.4)], F); pin_via(GND, 'R28.1', (115.0, 124.4), F)
T(CR, [P('TP1.1'), (117.5, 122.2)], F)
T(CD, [P('U1.17'), (111.6, 118.4), (118.0, 118.4), (118.0, 126.3), (115.95, 126.3)], F); V(CD, 115.95, 126.3)
T(CD, [(115.95, 126.3), (115.95, 130.25)], B); V(CD, 115.95, 130.25)
T(CD, [P('U2.7'), (115.95, 130.25)], F)
T(CD, [P('TP2.1'), (118.0, 120.6)], F)
T(CD, [(118.0, 123.2), P('R29.1')], F); pin_via(V33, 'R29.2', (120.65, 123.2), F)      # pull-up's plane via sits east of the bus lanes

# ============================================================== SPI flash U4 (W25Q128JV, QIO) in the north-east corner
# DI/CLK/HOLD leave the right side, turn north in a channel (x 116.1..117.9) and fan into U4's south row; WP/DO/CS run up the east
# side (x 120.65 / 121.1 / 121.55). The chip's pin order is mirrored against the C6's, so WP and DO cross under CS on B.Cu in the
# empty corner above U4 (vias at y 101.45 / 101.9); CS stays on F.Cu over the top.
K0 = 232.4                                                      # jog lines x + y = K0 - 0.5 i (CS, DO, WP, HD, CLK)
chan = [('FLASH_DI', 'U1.26', 116.095, None), ('FLASH_CLK', 'U1.25', 116.455, ('U4.6', K0 - 2.0)), ('FLASH_HD', 'U1.24', 116.815, ('U4.7', K0 - 1.5)),
        ('FLASH_WP', 'U1.22', 117.175, (120.65, K0 - 1.0)), ('FLASH_DO', 'U1.21', 117.535, (121.1, K0 - 0.5))]
for net, pad, col, jog in chan:
    px, py = P(pad)
    if jog is None:
        T(net, [(px, py), (col, py), P('U4.5')], F); continue
    tgt, K = jog
    ex = P(tgt)[0] if isinstance(tgt, str) else tgt
    pts = [(px, py), (col, py), (col, K - col), (ex, K - ex)]
    if isinstance(tgt, str): pts.append(P(tgt))
    T(net, pts, F)
cx, cy = P('U1.20')
T('FLASH_CS', [(cx, cy), (cx, 117.25), (117.895, 117.25), (117.895, K0 - 117.895), (121.55, K0 - 121.55), (121.55, 101.0), (119.905, 101.0), P('U4.1')], F)
T('FLASH_DO', [(121.1, K0 - 0.5 - 121.1), (121.1, 101.45)], F); V('FLASH_DO', 121.1, 101.45)
T('FLASH_DO', [(121.1, 101.45), (118.635, 101.45)], B); V('FLASH_DO', 118.635, 101.45); T('FLASH_DO', [(118.635, 101.45), P('U4.2')], F)
T('FLASH_WP', [(120.65, K0 - 1.0 - 120.65), (120.65, 101.9)], F); V('FLASH_WP', 120.65, 101.9)
T('FLASH_WP', [(120.65, 101.9), (117.365, 101.9)], B); V('FLASH_WP', 117.365, 101.9); T('FLASH_WP', [(117.365, 101.9), P('U4.3')], F)
pin_via(GND, 'U4.4', (116.095, 101.85), F, 0.25)
T(GND, [P('U4.4'), (116.095, 103.5)], F, 0.25)                    # ground pin into the exposed pad
# supply: plane via beside pin 8 and the 0.1 uF (0201) in the pocket south of the chip
T(V33, [P('U4.8'), (119.905, 108.85)], F, 0.25); V(V33, 119.905, 108.85)
T(V33, [(119.905, 108.85), P('C68.1')], F, 0.25)
pin_via(GND, 'C68.2', (119.265, 110.1), F, 0.15)

# ============================================================== contact field geometry
GND_FINGERS = {1, 3, 9, 15, 21, 27, 39, 45, 51, 57, 71, 73, 75}
VIA_FINGERS = GND_FINGERS | {33}        # front contacts that carry a via at Y_GVIA (33 is ESP_GPIO4 now)
Y_GVIA, Y_JOG, Y_END_MAX = 138.7, 139.0, 138.2
def squeezed_x(n):
    """Back-contact lane x near the pads: step 0.15 mm away from an adjacent front ground contact."""
    x = fingers[n][0]
    if n - 1 in VIA_FINGERS and n + 1 in VIA_FINGERS: raise ValueError(n)      # handled by hand (power contacts)
    if n - 1 in VIA_FINGERS: return x - 0.15           # n-1 is east (x falls with n)
    if n + 1 in VIA_FINGERS: return x + 0.15
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
# feeders: (net, via x, via y, feeder level y, miter x). Each feeder leaves its via on B.Cu, runs east on its level to the miter x and
# takes a 45-degree leg y - x = level - miter_x into its lane (x 116.4 + 0.25 k). Bottom-row feeders (EN .. D+) drop to their levels
# with a 45-degree corner (M_FEED); the right-side and top-row feeders leave at their via height. Legs are nested (c falls by >= 0.55
# per lane outwards); the VDDPST2 plane via and the C38 ground via sit on the midlines of two widened gaps (c -3.4 and -5.2).
bus = [('ESP_EN',          None,   None,   121.6,  115.4),
       ('ESP_GPIO4',       107.9,  116.35, 121.15, 115.5),
       ('ESP_GPIO5',       109.2,  117.35, 120.7,  115.6),
       ('ESP_GPIO8',       110.4,  117.35, 120.25, 115.7),
       ('ESP_GPIO9_BOOT',  110.8,  117.95, 119.8,  115.8),
       ('USB_D-',          112.0,  117.35, 119.35, 115.9),
       ('USB_D+',          112.4,  117.95, 118.9,  116.0),
       ('ESP_GPIO15',      114.8,  113.4,  113.4,  114.8),
       ('ESP_GPIO16_TXD',  114.8,  112.6,  112.6,  114.8),
       ('ESP_GPIO17_RXD',  114.25, 112.2,  112.2,  115.0),
       ('ESP_GPIO18',      112.8,  110.6,  110.6,  114.6),
       ('ESP_GPIO19',      112.4,  110.0,  110.0,  114.6),
       ('ESP_GPIO20',      112.0,  110.6,  109.55, 115.35),
       ('ESP_GPIO21',      111.6,  110.0,  109.1,  115.5),
       ('ESP_GPIO22',      111.2,  110.6,  108.65, 115.65),
       ('ESP_GPIO23',      110.8,  108.55, 108.2,  115.8)]
esp_pad = {'ESP_GPIO4': 'U1.10', 'ESP_GPIO5': 'U1.11', 'ESP_GPIO8': 'U1.14', 'ESP_GPIO9_BOOT': 'U1.15', 'USB_D-': 'U1.18', 'USB_D+': 'U1.19',
           'ESP_GPIO15': 'U1.27', 'ESP_GPIO16_TXD': 'U1.29', 'ESP_GPIO17_RXD': 'U1.30', 'ESP_GPIO18': 'U1.31', 'ESP_GPIO19': 'U1.32',
           'ESP_GPIO20': 'U1.33', 'ESP_GPIO21': 'U1.34', 'ESP_GPIO22': 'U1.35', 'ESP_GPIO23': 'U1.36'}
LANE0, LANE_P = 116.4, 0.25
C_ESP0, DC = 249.75, 0.36
prev_c = None
for k, (net, vx, vy, lvl, xt) in enumerate(bus):
    lane = LANE0 + LANE_P * k
    if vx is not None:
        px, py = P(esp_pad[net])
        if net == 'ESP_GPIO4': T(net, [(px, py), (vx, py), (vx, vy)], F)                        # west, then down to the via
        else: T(net, [(px, py), (vx, vy)] if (abs(px - vx) < 1e-6 or abs(py - vy) < 1e-6) else [(px, py), (px, vy), (vx, vy)], F)
        V(net, vx, vy)
        if abs(vy - lvl) < 1e-6: T(net, [(vx, vy), (xt, lvl)], B, W_BUS)
        elif vy > lvl:   T(net, [(vx, vy), (vx, lvl), (xt, lvl)], B, W_BUS)                        # top row: north to the level
        else:            T(net, [(vx, vy), (vx, lvl - M_FEED), (vx + M_FEED, lvl), (xt, lvl)], B, W_BUS)   # mitered corner
    c = lvl - xt
    assert prev_c is None or c <= prev_c - 0.55 + 1e-6, (net, c, prev_c)
    prev_c = c
    y_in = lvl + (lane - xt)
    n = finger_of[net][2]
    if n in VIA_FINGERS:                                         # front contact: lane ends on the contact's via, F.Cu stub to the pad
        fx, fy, _ = fingers[n]; cc = C_ESP0 + DC * k
        y_turn = cc - lane; assert cc - fx <= Y_END_MAX + 1e-6
        T(net, [(lane, y_turn), (fx, cc - fx), (fx, Y_GVIA)], B, W_BUS); V(net, fx, Y_GVIA); T(net, [(fx, Y_GVIA), (fx, fy)], F)
    else:
        y_turn = back_entry(net, n, lane, C_ESP0 + DC * k)
    assert y_turn > y_in, (net, y_turn, y_in)
    T(net, [(xt, lvl), (lane, y_in), (lane, y_turn)], B, W_BUS)

# R20 / R21 pull-ups hang off the GPIO9 / GPIO8 levels through in-line vias; their 3.3 V vias sit south of the EN level
T('ESP_GPIO9_BOOT', [P('R20.1'), (115.1, 119.8)], F); V('ESP_GPIO9_BOOT', 115.1, 119.8)
pin_via(V33, 'R20.2', (115.1, 122.2), F)
T('ESP_GPIO8', [P('R21.1'), (114.15, 120.25)], F); V('ESP_GPIO8', 114.15, 120.25)
pin_via(V33, 'R21.2', (114.15, 122.45), F)

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
for n in (9, 15, 21, 27, 39, 45, 51, 57):
    fx, fy, _ = fingers[n]; T(GND, [(fx, fy), (fx, Y_GVIA)], F); V(GND, fx, Y_GVIA)
# end ground contacts 1/3 and 71/73/75: the pour stays out of the finger window, so they run up to the board-end vias by hand,
# squeezing past the back power-contact vias (2 at 120.0/138.3, 4 at 119.625/139.175, 74 at 102.0/138.3) and 0.3 mm off the tab edge
V(GND, 120.7, 137.75); V(GND, 101.6, 137.7)                                   # 120.7: clear of C61's feed into the contact-2 via
T(GND, [P('J1.1'), (120.25, 139.0), (120.55, 138.7), (120.55, 137.9), (120.7, 137.75)], F)
T(GND, [P('J1.3'), (119.75, 139.6), (120.25, 139.6)], F)                 # 90-degree tee into the contact-1 column
T(GND, [P('J1.75'), (101.75, 139.0), (101.45, 138.7), (101.45, 137.85), (101.6, 137.7)], F)
T(GND, [P('J1.71'), (102.75, 139.6), (101.75, 139.6)], F)                # one bar; contact 73 tees into it
T(GND, [P('J1.73'), (102.25, 139.6)], F)
# back power contacts weave past the ground vias (0.15 mm lanes), then drop to the 3.3 V plane
def stub(n, pts, via):
    fx, fy, _ = fingers[n]; T(V33, [(fx, fy)] + pts, B, W_BUS); V(V33, *via)
stub(2,  [(120.0, 138.3)], (120.0, 138.3))
fx4, fy4, _ = fingers[4]; T(V33, [(fx4, fy4), (119.5, 139.3), (119.625, 139.175)], B, W_BUS); V(V33, 119.625, 139.175, 0.4)
stub(70, [(103.0, 137.0)], (103.0, 137.0))
stub(72, [(102.5, 137.6)], (102.5, 137.6))
stub(74, [(102.0, 138.3)], (102.0, 138.3))
# No free-standing stitching vias: every via carries a pad, a trace or a contact. In1 is a solid ground plane and the outer
# ground pours tie to it through the decoupling, thermal and contact-field vias.

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
pol['config']['min_trace_mm'] = 0.10                               # fab minimum (DRU / board setup); the 50 ohm RF feed is 0.14 mm on 3313
ep = {'U1': (111.0, 113.5, 1.85), 'U2': (111.0, 130.5, 1.9)}
# roles follow attachment: a via earns a role only if a same-net track touches it (or it sits in an exposed pad);
# anything else is left unroled so `lint` reports it as a stray (via.role_missing)
segs = [s for s in board.GetTracks() if s.GetClass() == 'PCB_TRACK']
roles = {}
for t in board.GetTracks():
    if t.GetClass() != 'PCB_VIA': continue
    x, y = p.ToMM(t.GetPosition().x), p.ToMM(t.GetPosition().y); n = t.GetNetname()
    attached = any(s.GetNetCode() == t.GetNetCode() and s.HitTest(t.GetPosition()) for s in segs)   # a same-net track touches it
    if n == 'GND' and any(abs(x - cx) <= h and abs(y - cy) <= h for cx, cy, h in ep.values()): role = 'thermal'
    elif not attached: continue
    elif n == 'GND': role = 'return'
    elif n in ('+3.3V', '+1.2V', '+1.2V_PLL'): role = 'feed'
    else: continue
    roles[str(t.m_Uuid.AsString())] = role
intent['roles'] = roles
json.dump(pol, open(LINT, 'w'), indent=2); open(LINT, 'a').write('\n')
stats['roles'] = len(roles)
print('routed:', stats)
