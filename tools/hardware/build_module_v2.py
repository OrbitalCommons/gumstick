#!/usr/bin/env python3
"""Construct the ESP32-C6 + iCE40UP5K M.2 module (v2): libraries, circuit contract, PCB.

Run with system Python (needs pcbnew). Writes boards/esp32-fpga-module-v2/.
Idempotent for libraries; refuses to overwrite a routed PCB unless --replace-draft.

Sources of truth used here:
- ESP32-C6 datasheet, QFN32 pin table (ESP32-C6FH4/FH8): docs/design-contract.json
- M.2 card edge: e-tec MPE-075-RXM9 recommended module drawing (PCI-SIG M.2 compatible)
- v1 module (boards/esp32-fpga-module) for the FPGA, crystal, LED, U.FL, LDO parts
"""
import sys, json, re, shutil, math, uuid
from pathlib import Path
import pcbnew as p

R = Path(__file__).resolve().parents[2]
D = R / 'boards/esp32-fpga-module-v2'
V1 = R / 'boards/esp32-fpga-module'
STD_FP = Path('/usr/share/kicad/footprints')
STD_3D = Path('/usr/share/kicad/3dmodels')
for d in ['Module2.pretty', 'docs', '3dmodels', 'fab/checks']:
    (D / d).mkdir(parents=True, exist_ok=True)

PCB = D / 'module.kicad_pcb'
if PCB.exists() and '--replace-draft' not in sys.argv:
    b = p.LoadBoard(str(PCB))
    if b.GetTracks().size() > 0:
        sys.exit('module.kicad_pcb already carries routing; rerun with --replace-draft to rebuild the draft')

uid = lambda s: str(uuid.uuid5(uuid.NAMESPACE_URL, 'bp-module-v2/' + s))
mm = p.FromMM
v = lambda x, y: p.VECTOR2I(mm(x), mm(y))

# ---------------------------------------------------------------- board frame
X0, Y0 = 100.0, 100.0          # board top-left corner (mounting end at top)
W, L = 22.0, 42.0              # M.2 2242
CL = X0 + W / 2                # longitudinal centerline x = 111
EDGE = Y0 + L                  # connector edge y = 142
TAB_W, TAB_L = 19.85, 3.5      # connector tab
NOTCH_X = CL - 6.125           # key M notch centre (pin 75 side)
NOTCH_W = 1.2
PIN1_X = CL + 9.25             # contact 1 (component side, right end)

def contact_x(n):              # odd and even rows share the 0.25 mm position grid
    return PIN1_X - (n - 1) * 0.25

KEY = set(range(59, 67))       # positions removed by the key notch
EDGE_SETBACK = 0.6             # copper setback from the routed edge for JLCPCB's 30 deg bevel (they quote ~1.13 mm at 1.6 mm;
                               # scaled to the 0.8 mm card and rounded up). The pad tops stay where the socket expects them.
WINDOW_TOP_F, WINDOW_TOP_B = 2.1, 2.6   # solder-mask window over the finger field (pad length + 0.1), per JLCPCB 'fully opened'

# ---------------------------------------------------------------- board
board = p.BOARD()
board.SetCopperLayerCount(4)
ds = board.GetDesignSettings()
ds.SetAuxOrigin(v(X0, EDGE)); ds.SetGridOrigin(v(X0, Y0))
ds.m_MinClearance = mm(0.1); ds.m_TrackMinWidth = mm(0.1)
ds.m_ViasMinSize = mm(0.4); ds.m_MinThroughDrill = mm(0.2)
ds.m_CopperEdgeClearance = mm(0.0)   # fingers reach the edge; module.kicad_dru restores 0.3 mm elsewhere; ds.m_HoleToHoleMin = mm(0.25)
ds.m_SilkClearance = mm(0.15); ds.m_HoleClearance = mm(0.2)
ds.m_SolderMaskExpansion = mm(0.0); ds.m_SolderMaskMinWidth = mm(0.0)

nets = {}; parts = {}; footprints = {}; saved_fps = set()
def net(n):
    if n not in nets:
        nets[n] = p.NETINFO_ITEM(board, n); board.Add(nets[n])
    return nets[n]

def copy_model(f, src_root):
    models = list(f.Models()); f.Models().clear()
    for m in models:
        src = Path(re.sub(r'\$\{KICAD\d+_3DMODEL_DIR\}', str(STD_3D), m.m_Filename).replace('${KIPRJMOD}', str(src_root)))
        if src.suffix == '.wrl' and src.with_suffix('.step').exists(): src = src.with_suffix('.step')
        if src.exists():
            dst = D / '3dmodels' / src.name
            if not dst.exists(): shutil.copy2(src, dst)
            m.m_Filename = '${KIPRJMOD}/3dmodels/' + src.name; f.Add3DModel(m)

def lib_save(f, name):
    f.SetOrientationDegrees(0); f.SetPosition(v(0, 0))
    f.SetFPID(p.LIB_ID('Module2', name))
    p.PCB_IO_KICAD_SEXPR().FootprintSave(str(D / 'Module2.pretty'), f)
    saved_fps.add(name)

PASSIVE_FPS = {'C_0402', 'C_0603', 'R_0402', 'L_0402', 'L_0603', 'TestPoint_0p8', 'LED_RGB_1010'}
def import_fp(lib_dir, src_name, name, src_root):
    if name not in saved_fps and not (D / 'Module2.pretty' / f'{name}.kicad_mod').exists():
        f = p.FootprintLoad(str(lib_dir), src_name); assert f, (lib_dir, src_name)
        copy_model(f, src_root)
        for g in list(f.GraphicalItems()):
            if g.GetLayer() == p.F_SilkS:
                if name in PASSIVE_FPS or name.startswith(('QFN-32', 'ICE40', 'SOT-23')): g.SetLayer(p.F_Fab)
                elif isinstance(g, p.PCB_TEXT) and g.GetTextThickness() < mm(0.15): g.SetTextThickness(mm(0.15)); g.SetTextSize(v(1.0, 1.0))
        if name == 'ICE40-QFN':
            # the vendor footprint ships its datasheet dimension drawing, pad-style notes and a hatched fab body;
            # keep only copper, paste and mask, then draw a plain 7 mm body with a pin-1 chamfer and a courtyard
            for g in list(f.GraphicalItems()):
                if g.GetLayer() in (p.Dwgs_User, p.Cmts_User, p.F_Fab, p.B_Fab, p.F_CrtYd): f.Remove(g)
            h = 3.5; ch = 0.75
            for a_, b_ in [((-h + ch, -h), (h, -h)), ((h, -h), (h, h)), ((h, h), (-h, h)), ((-h, h), (-h, -h + ch)), ((-h, -h + ch), (-h + ch, -h))]:
                s_ = p.PCB_SHAPE(f); s_.SetShape(p.SHAPE_T_SEGMENT); s_.SetStart(v(*a_)); s_.SetEnd(v(*b_)); s_.SetLayer(p.F_Fab); s_.SetWidth(mm(0.1)); f.Add(s_)
            c_ = p.PCB_SHAPE(f); c_.SetShape(p.SHAPE_T_RECT); c_.SetStart(v(-3.75, -3.75)); c_.SetEnd(v(3.75, 3.75)); c_.SetLayer(p.F_CrtYd); c_.SetWidth(mm(0.05)); f.Add(c_)
        lib_save(f, name)
    return p.FootprintLoad(str(D / 'Module2.pretty'), name)

def v1fp(src, name): return import_fp(V1 / 'Module.pretty', src, name, V1)
def stdfp(lib, src, name): return import_fp(STD_FP / f'{lib}.pretty', src, name, STD_3D)

# ---------------------------------------------------------------- M.2 card edge footprint
def build_m2_edge():
    name = 'M2_CardEdge_KeyM_2242'
    path = D / 'Module2.pretty' / f'{name}.kicad_mod'
    if path.exists(): return p.FootprintLoad(str(D / 'Module2.pretty'), name)
    f = p.FOOTPRINT(board); f.SetReference('J1'); f.SetValue('M.2 Key M card edge')
    f.SetAttributes(p.FP_SMD | p.FP_EXCLUDE_FROM_BOM | p.FP_EXCLUDE_FROM_POS_FILES)
    f.SetLayer(p.F_Cu)
    for n in range(1, 76):
        if n in KEY: continue
        pad = p.PAD(f); pad.SetNumber(str(n)); pad.SetShape(p.PAD_SHAPE_RECT); pad.SetAttribute(p.PAD_ATTRIB_SMD)
        top = (n % 2 == 1)
        length = (2.0 if top else 2.5) - EDGE_SETBACK      # fingers keep their inner ends (2.0 / 2.5 mm from the edge), the bevel zone is copper-free
        pad.SetSize(v(0.35, length)); pad.SetPosition(v(contact_x(n) - CL, -(EDGE_SETBACK + length / 2)))
        ls = p.LSET()
        ls.AddLayer(p.F_Cu if top else p.B_Cu); ls.AddLayer(p.F_Mask if top else p.B_Mask)
        pad.SetLayerSet(ls)                   # no paste on gold fingers
        pad.SetLayer(p.F_Cu if top else p.B_Cu)
        pad.SetLocalSolderMaskMargin(mm(0))       # the field-wide window below exposes the fingers
        f.Add(pad)
    # JLCPCB: the gold-finger area must have the solder mask fully opened; one window per side over the whole field, past the edge
    for layer, top in ((p.F_Mask, WINDOW_TOP_F), (p.B_Mask, WINDOW_TOP_B)):
        r = p.PCB_SHAPE(f); r.SetShape(p.SHAPE_T_RECT); r.SetStart(v(-TAB_W / 2, -top)); r.SetEnd(v(TAB_W / 2, 0.5))
        r.SetFilled(True); r.SetWidth(0); r.SetLayer(layer); f.Add(r)
    # fab outline of the tab and key for reference (board edge is drawn on the PCB)
    for a, b in [((-TAB_W / 2, 0), (TAB_W / 2, 0)), ((-TAB_W / 2, 0), (-TAB_W / 2, -TAB_L)), ((TAB_W / 2, 0), (TAB_W / 2, -TAB_L))]:
        s = p.PCB_SHAPE(f); s.SetShape(p.SHAPE_T_SEGMENT); s.SetStart(v(*a)); s.SetEnd(v(*b)); s.SetLayer(p.F_Fab); s.SetWidth(mm(0.1)); f.Add(s)
    f.Reference().SetVisible(False); f.Value().SetVisible(False)
    lib_save(f, name)
    return p.FootprintLoad(str(D / 'Module2.pretty'), name)

# ---------------------------------------------------------------- part placement helper
REF_POS = {'U1': (111.0, 118.0, 0), 'U2': (111.0, 136.2, 0), 'U3': (104.6, 122.0, 0), 'J3': (102.4, 108.4, 0)}
def add(ref, val, f, pins, x, y, angle=0, kind='ic', mpn='', lcsc='', names=None, types=None, bom=True, ref_vis=None):
    f.SetFPID(p.LIB_ID('Module2', str(f.GetFPID().GetLibItemName())))
    f.SetReference(ref); f.SetValue(val); f.SetPosition(v(x, y)); f.SetOrientationDegrees(angle)
    f.SetPath(p.KIID_PATH('/' + uid('root') + '/' + uid(ref)))
    attrs = p.FP_SMD
    if not bom: attrs |= p.FP_EXCLUDE_FROM_BOM | p.FP_EXCLUDE_FROM_POS_FILES
    f.SetAttributes(attrs)
    for pad in f.Pads():
        n = pins.get(pad.GetNumber())
        if n: pad.SetNet(net(n))
    f.Reference().SetTextSize(v(1.0, 1.0)); f.Reference().SetTextThickness(mm(0.15))
    vis = ref_vis if ref_vis is not None else kind in ['ic', 'connector']
    f.Reference().SetLayer(p.F_SilkS if vis else p.F_Fab)
    f.Reference().SetVisible(vis)
    if vis:
        bb = f.GetBoundingBox(False, False)
        f.Reference().SetPosition(v(p.ToMM(bb.GetRight()) + 0.9, p.ToMM(bb.GetBottom()) - 0.6))   # bottom-right corner per the playbook
        if ref in REF_POS:
            x_, y_, a_ = REF_POS[ref]; f.Reference().SetPosition(v(x_, y_)); f.Reference().SetTextAngleDegrees(a_)
    f.Value().SetVisible(False)
    for k, val2 in [('MPN', mpn or val), ('LCSC', lcsc)]:
        f.SetField(k, val2); f.GetField(k).SetVisible(False)
    board.Add(f); footprints[ref] = f
    parts[ref] = {'value': val, 'mpn': mpn or val, 'lcsc': lcsc, 'footprint': 'Module2:' + str(f.GetFPID().GetLibItemName()),
                  'pins': pins, 'kind': kind, 'names': names or {}, 'types': types or {}, 'bom': bom, 'position': [x, y, angle]}
    return f

def cap0402(ref, val, a, b, x, y, ang=0, lcsc='C1525', mpn=''):
    return add(ref, val, v1fp('CAPC1005X60', 'C_0402'), {'1': a, '2': b}, x, y, ang, 'c', mpn, lcsc)
def cap0603(ref, val, a, b, x, y, ang=0, lcsc='C19702', mpn=''):
    return add(ref, val, v1fp('C33_C_0603_1608Metric', 'C_0603'), {'1': a, '2': b}, x, y, ang, 'c', mpn, lcsc)
def res0402(ref, val, a, b, x, y, ang=0, lcsc='C60490', mpn=''):
    return add(ref, val, v1fp('R20_RESC1005X40', 'R_0402'), {'1': a, '2': b}, x, y, ang, 'r', mpn, lcsc)
def ind0402(ref, val, a, b, x, y, ang=0, lcsc='', mpn='', land='L_0402'):
    src = {'L_0402': 'L3_INDC1006X60N', 'C_0402': 'CAPC1005X60'}[land]       # the crystal series inductor uses the narrower 0402 land to clear XTAL_N
    return add(ref, val, v1fp(src, land), {'1': a, '2': b}, x, y, ang, 'l', mpn, lcsc)
def bead0603(ref, val, a, b, x, y, ang=0):
    return add(ref, val, v1fp('L1_L_0603_1608Metric', 'L_0603'), {'1': a, '2': b}, x, y, ang, 'l', 'BLM18KG101TN1D', 'C160981')

# ---------------------------------------------------------------- placement (absolute mm)
U1X, U1Y = CL, 113.5           # ESP32-C6, rotation 0: ANT at left-top, crystal pins at top-left, USB at bottom-right
U2X, U2Y = CL, 130.5           # iCE40, rotation 180: SPI pins at top-right, RGB at bottom

# ESP32-C6FH8 QFN32 (datasheet Table 2-2); QFN32 has GPIO14 and no GPIO10/11; no VDD_SPI pin.
esp_names = {'1': 'ANT', '2': 'VDDA3P3', '3': 'VDDA3P3', '4': 'CHIP_PU', '5': 'VDDPST1', '6': 'GPIO0/XTAL_32K_P', '7': 'GPIO1/XTAL_32K_N',
             '8': 'GPIO2/FSPIQ', '9': 'GPIO3', '10': 'GPIO4/MTMS', '11': 'GPIO5/MTDI', '12': 'GPIO6/MTCK/FSPICLK', '13': 'GPIO7/MTDO/FSPID',
             '14': 'GPIO8', '15': 'GPIO9', '16': 'GPIO12/USB_D-', '17': 'GPIO13/USB_D+', '18': 'GPIO14', '19': 'GPIO15', '20': 'VDDPST2',
             '21': 'GPIO16/U0TXD', '22': 'GPIO17/U0RXD', '23': 'GPIO18', '24': 'GPIO19', '25': 'GPIO20', '26': 'GPIO21', '27': 'GPIO22',
             '28': 'GPIO23', '29': 'VDDA1', '30': 'XTAL_N', '31': 'XTAL_P', '32': 'VDDA2', '33': 'GND'}
esp_pins = {'1': 'RF_IN', '2': 'ESP_VDD3P3', '3': 'ESP_VDD3P3', '4': 'ESP_EN', '5': '+3.3V', '6': 'FPGA_SPI_IO3', '7': 'FPGA_SPI_MOSI',
            '8': 'FPGA_SPI_CS_N', '9': 'FPGA_SPI_SCK', '10': 'ESP_GPIO4', '11': 'ESP_GPIO5', '12': 'FPGA_SPI_MISO', '13': 'FPGA_SPI_IO2',
            '14': 'ESP_GPIO8', '15': 'ESP_GPIO9_BOOT', '16': 'USB_D-', '17': 'USB_D+', '18': 'FPGA_CRESET_N', '19': 'ESP_GPIO15', '20': '+3.3V',
            '21': 'ESP_GPIO16_TXD', '22': 'ESP_GPIO17_RXD', '23': 'FPGA_CDONE', '24': 'ESP_GPIO19', '25': 'ESP_GPIO20', '26': 'ESP_GPIO21',
            '27': 'ESP_GPIO22', '28': 'ESP_GPIO23', '29': '+3.3V', '30': 'XTAL_N', '31': 'XTAL_P', '32': '+3.3V', '33': 'GND'}
esp_types = {k: ('power_in' if n in ('VDDA3P3', 'VDDPST1', 'VDDPST2', 'VDDA1', 'VDDA2', 'GND') else 'input' if n in ('CHIP_PU',) else 'passive' if n in ('ANT', 'XTAL_N', 'XTAL_P') else 'bidirectional') for k, n in esp_names.items()}
add('U1', 'ESP32-C6FH8', stdfp('Package_DFN_QFN', 'QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm', 'QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm'),
    esp_pins, U1X, U1Y, 0, 'ic', 'ESP32-C6FH8', 'C41459370', esp_names, esp_types)

# iCE40UP5K-SG48 (pin names from the v1 contract; same QSPI configuration link as v1)
fpga_names = {'1': 'VCCIO_2', '2': 'IOB_6A', '3': 'IOB_9B', '4': 'IOB_8A', '5': 'VCC', '6': 'IOB_13B', '7': 'CDONE', '8': 'CRESET_B', '9': 'IOB_16A', '10': 'IOB_18A',
              '11': 'IOB_20A', '12': 'IOB_22A', '13': 'IOB_24A', '14': 'IOB_32A_SPI_SO', '15': 'IOB_34A_SPI_SCK', '16': 'IOB_35B_SPI_SS', '17': 'IOB_33B_SPI_SI',
              '18': 'IOB_31B', '19': 'IOB_29B', '20': 'IOB_25B_G3', '21': 'IOB_23B', '22': 'SPI_VCCIO1', '23': 'IOT_37A', '24': 'VPP_2V5', '25': 'IOT_36B',
              '26': 'IOT_39A', '27': 'IOT_38B', '28': 'IOT_41A', '29': 'VCCPLL', '30': 'VCC', '31': 'IOT_42B', '32': 'IOT_43A', '33': 'VCCIO_0', '34': 'IOT_44B',
              '35': 'IOT_46B_G0', '36': 'IOT_48B', '37': 'IOT_45A_G1', '38': 'IOT_50B', '39': 'RGB0', '40': 'RGB1', '41': 'RGB2', '42': 'IOT_51A', '43': 'IOT_49A',
              '44': 'IOB_3B_G6', '45': 'IOB_5B', '46': 'IOB_0A', '47': 'IOB_2A', '48': 'IOB_4A', 'PAD': 'GND'}
fpga_pins = {}
for k, n in fpga_names.items():
    if n.startswith(('IOB_', 'IOT_')) and 'SPI' not in n: fpga_pins[k] = 'FPGA_' + n
fpga_pins.update({'1': '+3.3V', '5': '+1.2V', '7': 'FPGA_CDONE', '8': 'FPGA_CRESET_N', '14': 'FPGA_SPI_MISO', '15': 'FPGA_SPI_SCK', '16': 'FPGA_SPI_CS_N',
                  '17': 'FPGA_SPI_MOSI', '13': 'FPGA_SPI_IO2', '18': 'FPGA_SPI_IO3', '22': '+3.3V', '24': '+3.3V', '29': '+1.2V_PLL', '30': '+1.2V',
                  '33': '+3.3V', '39': 'FPGA_RGB0', '40': 'FPGA_RGB1', '41': 'FPGA_RGB2', 'PAD': 'GND'})
fpga_types = {k: ('power_in' if n in ('VCCIO_2', 'VCC', 'SPI_VCCIO1', 'VPP_2V5', 'VCCPLL', 'VCCIO_0', 'GND') else 'output' if n == 'CDONE' else 'input' if n == 'CRESET_B' else 'bidirectional') for k, n in fpga_names.items()}
add('U2', 'iCE40UP5K-SG48', v1fp('ICE40-QFN', 'ICE40-QFN'), fpga_pins, U2X, U2Y, 180, 'ic', 'ICE40UP5K-SG48I', 'C2678152', fpga_names, fpga_types)

add('Y1', '40MHz / CL10pF', v1fp('Y1_JGHC_S2240000101050', 'Crystal_2520_4pin'), {'IN/OUT': 'XTAL_P_CRYSTAL', 'OUT/IN': 'XTAL_N', 'GND-A': 'GND', 'GND-B': 'GND'},
    110.4, 107.0, 0, 'xtal', 'S2240000101050', 'C426970', {'IN/OUT': 'IN/OUT', 'OUT/IN': 'OUT/IN', 'GND-A': 'GND', 'GND-B': 'GND'})
add('J3', 'U.FL-R-SMT-1(01)', v1fp('J3_U.FL_Hirose_U.FL-R-SMT-1_Vertical', 'UFL_Vertical'), {'1': 'RF_ANT', '2': 'GND'}, 104.95, 106.5, 90, 'connector', 'U.FL-R-SMT-1(01)', '')
add('TP1', 'FPGA_CRESET_N', v1fp('TestPoint_0p8', 'TestPoint_0p8'), {'1': 'FPGA_CRESET_N'}, 116.8, 122.2, 0, 'testpoint', bom=False)
add('TP2', 'FPGA_CDONE', v1fp('TestPoint_0p8', 'TestPoint_0p8'), {'1': 'FPGA_CDONE'}, 118.7, 120.6, 0, 'testpoint', bom=False)

# --- ESP32 cluster. U1 at (111,113.5) rotation 0: pads 1-8 left (x 108.5), 9-16 bottom (y 115.95), 17-24 right (x 113.5), 25-32 top (y 111.05).
# RF front end west of pin 1 (ANT at 108.5,111.75): C1 shunt, L3 series, C2 shunt, then north to the U.FL.
cap0402('C1', '1.5pF', 'RF_IN', 'GND', 107.0, 111.2654, 90, '', 'GJM1555C1H1R5WB01D')
ind0402('L3', '2.2nH', 'RF_IN', 'RF_ANT', 105.8, 111.75, 180, 'C86061', 'LQG15HS2N2S02D')
cap0402('C2', '1.5pF', 'RF_ANT', 'GND', 104.35, 111.2654, 90, '', 'GJM1555C1H1R5WB01D')
# crystal north of pins 30/31 with the series inductor on XTAL_P and symmetric load capacitors
ind0402('L5', '24nH', 'XTAL_P', 'XTAL_P_CRYSTAL', 109.75, 109.5, 90, 'C86061', 'LQG15HS24NJ02D', land='C_0402')
cap0402('C6', '12pF', 'XTAL_P_CRYSTAL', 'GND', 108.3, 107.29, 90, 'C26406')
cap0402('C7', '12pF', 'XTAL_N', 'GND', 112.6, 106.7096, -90, 'C26406')
cap0402('C40', '0.1uF', '+3.3V', 'GND', 107.6, 110.15, 180)         # VDDA2 pin 32
cap0402('C39', '0.1uF', '+3.3V', 'GND', 110.75, 109.15, 90)          # VDDA1 pin 29
# VDDA3P3 (pins 2,3) filter: bead from the 3.3 V plane, 10 uF + 1 uF + 0.1 uF
cap0402('C35', '0.1uF', 'ESP_VDD3P3', 'GND', 104.8154, 112.75, 180)
cap0402('C36', '1uF', 'ESP_VDD3P3', 'GND', 104.8154, 113.85, 180, 'C29266')
cap0603('C34', '10uF', 'ESP_VDD3P3', 'GND', 104.525, 115.2, 180)
bead0603('L1', '100ohm @100MHz', '+3.3V', 'ESP_VDD3P3', 104.5125, 116.75, 0)
cap0402('C37', '0.1uF', '+3.3V', 'GND', 106.7, 114.2346, -90)        # VDDPST1 pin 5 (pad 1 on the pin-5 line)
res0402('R22', '10k', 'ESP_EN', '+3.3V', 106.7, 116.7, 90)
cap0402('C32', '1uF', 'ESP_EN', 'GND', 106.7, 119.0, -90, 'C29266')
cap0402('C38', '0.1uF', '+3.3V', 'GND', 115.9, 113.75, 0)           # VDDPST2 pin 20 (fed by a short east trace)
cap0603('C33', '10uF', '+3.3V', 'GND', 114.3, 105.0, 90)
res0402('R20', '10k', 'ESP_GPIO9_BOOT', '+3.3V', 115.0, 117.8, 90)
res0402('R21', '10k', 'ESP_GPIO8', '+3.3V', 116.0, 118.3, 90)

# --- 1.2 V regulator cluster west of the FPGA; FPGA decoupling at its pins.
# U2 at (111,130.5) rotation 180: pins 13-24 top (y 127.0), 25-36 left (x 107.5), 37-48 bottom (y 134.0), 1-12 right (x 114.5).
add('U3', 'TLV75512PDBVR', v1fp('U4_SOT-23-5', 'SOT-23-5'), {'1': '+3.3V', '2': 'GND', '3': '+3.3V', '5': '+1.2V'}, 102.0, 122.0, 270, 'ic', 'TLV75512PDBVR', 'C2877864',
    {'1': 'IN', '2': 'GND', '3': 'EN', '4': 'NC', '5': 'OUT'}, {'1': 'power_in', '2': 'power_in', '3': 'input', '4': 'no_connect', '5': 'power_out'})
cap0603('C62', '1uF / 6.3V', '+3.3V', 'GND', 102.175, 119.0, 180, 'C15849')
cap0603('C63', '1uF / 6.3V', '+1.2V', 'GND', 103.725, 125.0, 0, 'C15849')
cap0603('C45', '10uF', '+1.2V', 'GND', 103.725, 126.6, 0)
bead0603('L2', '100ohm @100MHz', '+1.2V', '+1.2V_PLL', 101.0, 126.5, -90)
cap0603('C43', '10uF', '+1.2V_PLL', 'GND', 101.0, 129.75, -90)
cap0402('C44', '0.1uF', '+1.2V_PLL', 'GND', 104.2, 129.4, 180)       # VCCPLL pin 29 (pad 1 at the bottom, fed from the south)
cap0402('C49', '0.1uF', '+1.2V', 'GND', 105.1, 130.25, 180)             # VCC pin 30 (left), on the pin line
cap0402('C46', '0.1uF', '+3.3V', 'GND', 103.3, 131.75, 180)           # VCCIO_0 pin 33 (left); pin fed by an In2 via at its exit
cap0603('C66', '1uF / 6.3V', '+3.3V', 'GND', 117.6, 104.0, 90, 'C15849')
cap0402('C50', '0.1uF', '+1.2V', 'GND', 115.45, 134.5, -90)           # VCC pin 5 (right)
cap0402('C48', '0.1uF', '+3.3V', 'GND', 114.48, 135.6, -90)           # VCCIO_2 pin 1 (right)
cap0402('C52', '0.1uF', '+3.3V', 'GND', 107.5, 125.6, 180)          # SPI_VCCIO1 pin 22 and VPP_2V5 pin 24 (top), shared on a short 3.3 V bar
# 3.3 V input bulk beside the power contacts (2/4 right, 70/72/74 left)
cap0603('C60', '10uF / 10V', '+3.3V', 'GND', 119.3, 104.0, 90)
cap0603('C61', '22uF / 10V', '+3.3V', 'GND', 121.0, 104.0, 90, 'C5355402', 'CL10A226MPCNUBE')
cap0603('C67', '22uF / 10V', '+3.3V', 'GND', 115.9, 104.0, 90, 'C5355402', 'CL10A226MPCNUBE')
# configuration link pull resistors
res0402('R28', '10k', 'GND', 'FPGA_CRESET_N', 116.2, 124.4, 0)
res0402('R29', '10k', 'FPGA_CDONE', '+3.3V', 116.9, 111.2425, 90)

# ---------------------------------------------------------------- M.2 contacts (custom pinout; see docs/icd-v2-pinout.csv)
GND_CONTACTS = [1, 3, 9, 15, 21, 27, 33, 39, 45, 51, 57, 71, 73, 75]
PWR_CONTACTS = [2, 4, 70, 72, 74]
# ESP signals ride a B.Cu bus down the east margin to the even (B.Cu) contacts 6..34; order follows the bus nesting.
esp_contacts = {34: 'ESP_EN', 32: 'ESP_GPIO4', 30: 'ESP_GPIO5', 28: 'ESP_GPIO8', 26: 'ESP_GPIO9_BOOT', 24: 'USB_D-', 22: 'USB_D+', 20: 'ESP_GPIO15',
                18: 'ESP_GPIO16_TXD', 16: 'ESP_GPIO17_RXD', 14: 'ESP_GPIO19', 12: 'ESP_GPIO20', 10: 'ESP_GPIO21', 8: 'ESP_GPIO22', 6: 'ESP_GPIO23'}
rgb_contacts = {}
# FPGA I/O contacts: assign by physical order to keep the fanout uncrossed.
# Right-side pins 1-12 (x fixed, y bottom->top) feed the right odd contacts 11..29 (F.Cu);
# bottom pins 37-48 (x left->right) feed the middle contacts 31..45; left-side pins 25-36 feed the left contacts 49..69.
fpga_io_pins = [k for k, n in fpga_pins.items() if n.startswith(('FPGA_IOB', 'FPGA_IOT'))]
def pin_xy(ref, num):
    pad = [pd for pd in footprints[ref].Pads() if pd.GetNumber() == num][0]
    return p.ToMM(pad.GetPosition().x), p.ToMM(pad.GetPosition().y)
# U2 is rotated 180: pins 13-24 top (x descending with pin number), 25-36 left (y ascending), 37-48 bottom (x ascending), 1-12 right (y descending)
top = sorted([k for k in fpga_io_pins if 13 <= int(k) <= 24], key=lambda k: pin_xy('U2', k)[0])
left = sorted([k for k in fpga_io_pins if 25 <= int(k) <= 36], key=lambda k: pin_xy('U2', k)[1])
bottom = sorted([k for k in fpga_io_pins if 37 <= int(k) <= 48], key=lambda k: pin_xy('U2', k)[0])
right = sorted([k for k in fpga_io_pins if 1 <= int(k) <= 12], key=lambda k: -pin_xy('U2', k)[1])
# FPGA contacts follow the routing plan: odd (F.Cu) contacts take pins that stay on the front, even (B.Cu) contacts take pins that drop
# through a via at the package. East column -> F.Cu columns east of U2 -> contacts 5..25; bottom row -> straight F.Cu drops or a via;
# top row -> vias north of U2 and B.Cu lanes under the package; west column -> via columns west of U2 (pins 35/36 stay on F.Cu).
fpga_contact_pins = {12: '5', 11: '7', 10: '11', 9: '13', 6: '17', 4: '19', 3: '23', 2: '25',
                     37: '49', 38: '47', 40: '43', 41: '41', 43: '37', 44: '35', 46: '31', 47: '29',
                     23: '50', 39: '48', 21: '46', 20: '44', 42: '42', 19: '40', 45: '38', 48: '36',
                     36: '53', 35: '55', 25: '52', 26: '68', 27: '54', 28: '58', 31: '56', 32: '69', 34: '67'}
fpga_contacts = {int(n): fpga_pins[str(k)] for k, n in fpga_contact_pins.items()}
assert len(fpga_contacts) == 33 and len(set(fpga_contact_pins.values())) == 33, len(fpga_contacts)

contacts = {}
for n in GND_CONTACTS: contacts[str(n)] = 'GND'
for n in PWR_CONTACTS: contacts[str(n)] = '+3.3V'
for n, s in esp_contacts.items(): contacts[str(n)] = s
for n, s in rgb_contacts.items(): contacts[str(n)] = s
for n, s in fpga_contacts.items(): contacts[str(n)] = s
assert len(contacts) == 67, len(contacts)
add('J1', 'M.2 Key M card edge (custom pinout)', build_m2_edge(), contacts, CL, EDGE, 0, 'connector', 'PCB card edge', '', bom=False, ref_vis=False)

for ref, dx, dy in [('U1', -3.4, -2.2), ('U2', 3.9, 3.25), ('U3', 1.5, -1.9)]:   # board-frame offsets from the part centre to the pin-1 corner
    fp = footprints[ref]; x, y = parts[ref]['position'][:2]
    c = p.PCB_SHAPE(fp); c.SetShape(p.SHAPE_T_CIRCLE); c.SetCenter(v(x + dx, y + dy)); c.SetEnd(v(x + dx + 0.15, y + dy)); c.SetLayer(p.F_SilkS); c.SetWidth(mm(0.15)); c.SetFilled(True); fp.Add(c)
for g in footprints['J3'].GraphicalItems():
    if g.GetLayer() == p.F_SilkS and hasattr(g, 'SetWidth'): g.SetWidth(mm(0.15))
footprints['J1'].SetAllowSolderMaskBridges(True)   # the finger window deliberately exposes every contact in one aperture
for fp in board.GetFootprints():                 # mask apertures follow the fab's own expansion; local margins only confuse the bridge check
    if fp.GetReference() != 'J1':
        for pd in fp.Pads(): pd.SetLocalSolderMaskMargin(mm(0.0))
for pd in footprints['U3'].Pads():                # the no-connect pin carries the schematic's unconnected-net name so parity is exact
    if pd.GetNumber() == '4': pd.SetNet(net('unconnected-(U3-NC-Pad4)'))
for pd in footprints['J1'].Pads():                # front ground contacts merge solidly into the front pour (no spokes on 0.35 mm fingers)
    if pd.GetNetname() == 'GND': pd.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
for ref, num in (('U1', '33'), ('U2', 'PAD')):
    for pd in footprints[ref].Pads():
        if pd.GetNumber() == num: pd.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
# ---------------------------------------------------------------- outline (Edge.Cuts)
def seg(a, b, layer=p.Edge_Cuts, w=0.1):
    s = p.PCB_SHAPE(board); s.SetShape(p.SHAPE_T_SEGMENT); s.SetStart(v(*a)); s.SetEnd(v(*b)); s.SetLayer(layer); s.SetWidth(mm(w)); board.Add(s)
def arc(start, mid, end, layer=p.Edge_Cuts, w=0.1):
    s = p.PCB_SHAPE(board); s.SetShape(p.SHAPE_T_ARC); s.SetArcGeometry(v(*start), v(*mid), v(*end)); s.SetLayer(layer); s.SetWidth(mm(w)); board.Add(s)
tl, tr = X0 + (W - TAB_W) / 2, X0 + (W - TAB_W) / 2 + TAB_W     # tab x extents 101.075 .. 120.925
step = EDGE - TAB_L                                             # 138.5
nl, nr = NOTCH_X - NOTCH_W / 2, NOTCH_X + NOTCH_W / 2
notch_top = EDGE - TAB_L + NOTCH_W / 2                          # arc centre y = 139.1
seg((tl, EDGE), (nl, EDGE)); seg((nl, EDGE), (nl, notch_top))
arc((nl, notch_top), (NOTCH_X, notch_top - NOTCH_W / 2), (nr, notch_top))
seg((nr, notch_top), (nr, EDGE)); seg((nr, EDGE), (tr, EDGE))
seg((tr, EDGE), (tr, step)); seg((tr, step), (X0 + W, step)); seg((X0 + W, step), (X0 + W, Y0))
seg((X0 + W, Y0), (CL + 1.75, Y0)); arc((CL + 1.75, Y0), (CL, Y0 + 1.75), (CL - 1.75, Y0)); seg((CL - 1.75, Y0), (X0, Y0))
seg((X0, Y0), (X0, step)); seg((X0, step), (tl, step)); seg((tl, step), (tl, EDGE))
# fabrication notes: bevel and keep-outs
def text(t, x, y, layer, size=0.8, angle=0):
    tx = p.PCB_TEXT(board); tx.SetText(t); tx.SetPosition(v(x, y)); tx.SetLayer(layer); tx.SetTextSize(v(size, size)); tx.SetTextThickness(mm(0.15)); tx.SetTextAngleDegrees(angle); board.Add(tx)
text('Card edge: ENIG + gold fingers, 30 deg bevel (copper setback 0.6 mm, mask open); PCB 0.80 +/-0.08 mm; M.2 2242 key M', CL, EDGE + 1.2, p.Cmts_User, 0.6)
text('Order as a panel >= 50 x 50 mm with this edge on the panel outline (no V-cut through the fingers)', CL, EDGE + 2.0, p.Cmts_User, 0.6)
text('ESP32-C6 + iCE40UP5K module v2', CL, Y0 - 1.5, p.Cmts_User, 0.8)
# component keep-out strips (fab/courtyard guidance): connector tab 4.0 mm top / 5.2 mm bottom, mounting end 3.8 mm
for y, layer in [(EDGE - 4.0, p.F_Fab), (EDGE - 5.2, p.B_Fab), (Y0 + 3.8, p.F_Fab)]:
    seg((X0, y), (X0 + W, y), layer, 0.05)

# ---------------------------------------------------------------- planes: In1 GND, In2 +3.3V (and GND fill on outer layers later)
def zone(netname, layer, prio, pts):
    z = p.ZONE(board); z.SetNet(net(netname)); z.SetLayer(layer); z.SetAssignedPriority(prio)
    z.SetPadConnection(p.ZONE_CONNECTION_THERMAL); z.SetThermalReliefGap(mm(0.15)); z.SetThermalReliefSpokeWidth(mm(0.15))
    z.SetLocalClearance(mm(0.15)); z.SetMinThickness(mm(0.1))
    ol = z.Outline(); ol.NewOutline()
    for x, y in pts: ol.Append(mm(x), mm(y))
    board.Add(z); return z
rect = [(X0, Y0), (X0 + W, Y0), (X0 + W, EDGE), (X0, EDGE)]
zone('GND', p.In1_Cu, 1, rect)
zone('+3.3V', p.In2_Cu, 1, rect)
zone('GND', p.F_Cu, 0, rect)
zone('GND', p.B_Cu, 0, rect)
# rule area naming the finger strip (used by module.kicad_dru to allow fingers at the routed edge)
za = p.ZONE(board); za.SetIsRuleArea(True); za.SetZoneName('m2-fingers')
for fn in ('SetDoNotAllowPads', 'SetDoNotAllowTracks', 'SetDoNotAllowVias', 'SetDoNotAllowZoneFills', 'SetDoNotAllowFootprints'): getattr(za, fn)(False)
lsa = p.LSET()
for l in (p.F_Cu, p.B_Cu): lsa.AddLayer(l)
za.SetLayerSet(lsa); ola = za.Outline(); ola.NewOutline()
for x, y in [(X0, EDGE - 2.8), (X0 + W, EDGE - 2.8), (X0 + W, EDGE + 0.5), (X0, EDGE + 0.5)]: ola.Append(mm(x), mm(y))
board.Add(za)
# no pour inside the finger window: nothing but the fingers (and their entry tracks) may be exposed there or sit in the bevel zone
zw = p.ZONE(board); zw.SetIsRuleArea(True); zw.SetZoneName('m2-finger-window')
zw.SetDoNotAllowZoneFills(True); zw.SetDoNotAllowVias(False)      # contact 4's via sits 0.2 mm above the window
for fn in ('SetDoNotAllowPads', 'SetDoNotAllowTracks', 'SetDoNotAllowFootprints'): getattr(zw, fn)(False)
lsw = p.LSET()
for l in (p.F_Cu, p.B_Cu): lsw.AddLayer(l)
zw.SetLayerSet(lsw); olw = zw.Outline(); olw.NewOutline()
for x, y in [(CL - TAB_W / 2, EDGE - WINDOW_TOP_B - 0.2), (CL + TAB_W / 2, EDGE - WINDOW_TOP_B - 0.2), (CL + TAB_W / 2, EDGE + 0.5), (CL - TAB_W / 2, EDGE + 0.5)]: olw.Append(mm(x), mm(y))
board.Add(zw)
# via keep-outs under the QFN bodies (debuggability rule from the playbook)
for ref, half, ex, ey in [('U1', 2.5, 1.85, 1.85), ('U2', 3.5, 1.9, 2.54)]:   # ring between the exposed pad and the body edge
    x, y = parts[ref]['position'][:2]
    for i, (x0, y0, x1, y1) in enumerate([(-half, -half, half, -ey), (-half, ey, half, half), (-half, -ey, -ex, ey), (ex, -ey, half, ey)]):
        z = p.ZONE(board); z.SetIsRuleArea(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowTracks(False); z.SetDoNotAllowZoneFills(False)
        z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
        ls = p.LSET();
        for l in (p.F_Cu, p.In1_Cu, p.In2_Cu, p.B_Cu): ls.AddLayer(l)
        z.SetLayerSet(ls); ol = z.Outline(); ol.NewOutline()
        for dx, dy in [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]: ol.Append(mm(x + dx), mm(y + dy))
        z.SetZoneName(f'no-vias-under-{ref}-{i}'); board.Add(z)

# ---------------------------------------------------------------- save
board.Save(str(PCB))
# stackup: JLCPCB JLC04081H-3313 (4 layers, 0.8 mm, 1 oz outer / 0.5 oz inner), nominal 0.799 mm, the JLCPCB 0.8 mm
# build closest to the M.2 card thickness (0.8 +/- 0.08 mm); JLCPCB only guarantees +/- 0.1 mm below 1.0 mm, so a centred
# nominal matters. Layer data: JLCPCB impedance page via github.com/gsuberland/jlcpcb_autogenerated_stackups.
def sl(name, typ, t=None, mat=None, er=None):
    body = f'(type "{typ}")' + (f' (thickness {t})' if t is not None else '') + (f' (material "{mat}")' if mat else '') + (f' (epsilon_r {er}) (loss_tangent 0.02)' if er else '')
    return f'(layer "{name}" {body})'
STACK = ('(stackup ' + ' '.join([
    sl('F.SilkS', 'Top Silk Screen'), sl('F.Paste', 'Top Solder Paste'), sl('F.Mask', 'Top Solder Mask', 0.01524),
    sl('F.Cu', 'copper', 0.035), sl('dielectric 1', 'prepreg', 0.0994, '3313 RC57%', 4.1),
    sl('In1.Cu', 'copper', 0.0152), sl('dielectric 2', 'core', 0.5, 'FR4', 4.48),
    sl('In2.Cu', 'copper', 0.0152), sl('dielectric 3', 'prepreg', 0.0994, '3313 RC57%', 4.1),
    sl('B.Cu', 'copper', 0.035), sl('B.Mask', 'Bottom Solder Mask', 0.01524), sl('B.Paste', 'Bottom Solder Paste'), sl('B.SilkS', 'Bottom Silk Screen')])
    + ' (copper_finish "ENIG") (dielectric_constraints yes))\n')
s = PCB.read_text()
k = s.index('(pad_to_mask_clearance'); s = s[:k] + STACK + s[k:]
s = s.replace('(thickness 1.6)', '(thickness 0.8)', 1)              # board thickness in (general)
PCB.write_text(s)

pro_path = D / 'module.kicad_pro'
pro = json.loads(pro_path.read_text()); v1pro = json.loads((V1 / 'module.kicad_pro').read_text())
pro['board'] = v1pro['board']; pro['net_settings'] = v1pro['net_settings']
for k in ('schematic', 'pcbnew'):
    if k in v1pro: pro[k] = v1pro[k]
pro['meta']['filename'] = 'module.kicad_pro'
cls0 = dict(pro['net_settings']['classes'][0]); cls0.update({'clearance': 0.1, 'track_width': 0.15, 'via_diameter': 0.45, 'via_drill': 0.2, 'diff_pair_width': 0.18, 'diff_pair_gap': 0.15})
def ncls(name, **kw):
    c = dict(cls0); c['name'] = name; c.update(kw); return c
pro['net_settings']['classes'] = [cls0, ncls('Power', track_width=0.3), ncls('RF', track_width=0.14, clearance=0.15), ncls('USB', track_width=0.18), ncls('Link', track_width=0.15)]
pro['net_settings']['netclass_patterns'] = [{'netclass': 'Power', 'pattern': '+3.3V'}, {'netclass': 'Power', 'pattern': '+1.2V*'}, {'netclass': 'Power', 'pattern': 'ESP_VDD3P3'},
                                            {'netclass': 'RF', 'pattern': 'RF_*'}, {'netclass': 'USB', 'pattern': 'USB_D*'}, {'netclass': 'Link', 'pattern': 'FPGA_SPI_*'}]
rules = pro['board']['design_settings']['rules']
rules.update({'min_clearance': 0.1, 'min_track_width': 0.1, 'min_via_diameter': 0.4, 'min_through_hole_diameter': 0.2, 'min_copper_edge_clearance': 0.0})
sev = pro['board']['design_settings'].setdefault('rule_severities', {})
sev['lib_footprint_mismatch'] = 'ignore'; sev['lib_footprint_issues'] = 'ignore'
pro_path.write_text(json.dumps(pro, indent=2) + '\n')

(D / 'docs/circuit.json').write_text(json.dumps(parts, indent=2) + '\n')
(D / 'docs/placement.json').write_text(json.dumps({r: c['position'] for r, c in parts.items()}, indent=2) + '\n')
contract = {'fpga_contacts': fpga_contacts, 'esp_contacts': esp_contacts, 'rgb_contacts': rgb_contacts, 'gnd': GND_CONTACTS, 'power': PWR_CONTACTS}
(D / 'docs/contact-assignment.json').write_text(json.dumps(contract, indent=2, sort_keys=True) + '\n')
print('parts', len(parts), 'nets', len(nets), 'contacts', len(contacts))
