#!/usr/bin/env python3
"""Regenerate the v2 module interface documents from the routed board.

Writes boards/esp32-fpga-module-v2/docs/icd-v2-pinout.csv (every M.2 contact), c6-fpga-link.csv (the
ESP32-C6 <-> iCE40 configuration link) and refreshes the pin tables inside design-contract.json so the
documents can never drift from the copper. Run after build_module_v2.py / module_v2_route.py.
"""
import csv, json
from pathlib import Path
import pcbnew as p

R = Path(__file__).resolve().parents[2]
D = R / 'boards/esp32-fpga-module-v2'
board = p.LoadBoard(str(D / 'module.kicad_pcb'))

pads = {}            # ref -> {num: net}
for fp in board.GetFootprints():
    pads[fp.GetReference()] = {pd.GetNumber(): pd.GetNetname() for pd in fp.Pads()}
esp = {n: k for k, n in pads['U1'].items() if n}
fpga = {n: k for k, n in pads['U2'].items() if n}
esp_gpio = {'ESP_GPIO4': 4, 'ESP_GPIO5': 5, 'ESP_GPIO8': 8, 'ESP_GPIO9_BOOT': 9, 'ESP_GPIO15': 15, 'ESP_GPIO16_TXD': 16, 'ESP_GPIO17_RXD': 17,
            'ESP_GPIO18': 18, 'ESP_GPIO19': 19, 'ESP_GPIO20': 20, 'ESP_GPIO21': 21, 'ESP_GPIO22': 22, 'ESP_GPIO23': 23,
            'FPGA_SPI_IO3': 0, 'FPGA_SPI_MOSI': 1, 'FPGA_SPI_CS_N': 2, 'FPGA_SPI_SCK': 3, 'FPGA_SPI_MISO': 6, 'FPGA_SPI_IO2': 7,
            'FPGA_CRESET_N': 10, 'FPGA_CDONE': 11, 'USB_D-': 12, 'USB_D+': 13}
strap = {4: 'JTAG-select strap (sampled at reset): keep the documented default or leave floating',
         5: 'JTAG-select strap (sampled at reset): keep the documented default or leave floating',
         8: 'Boot strap: must be high for serial download (weak internal pull-up); R21 10k pull-up on module',
         9: 'Boot strap: high for normal SPI boot, low for serial download; R20 10k pull-up on module',
         15: 'Strap (sampled at reset): keep the documented default or leave floating'}

def constraint(n, net):
    if net == 'GND': return 'Ground'
    if net == '+3.3V': return 'Regulated 3.3 V input; connect all five power contacts'
    if net.startswith('USB_D'): return 'USB Serial/JTAG full-speed pair (D+/D- on adjacent back contacts 22/24)'
    if net == 'ESP_EN': return 'Active-high CHIP_PU; 10k pull-up and 1 uF on module; open-drain reset permitted'
    if net.startswith('ESP_GPIO'):
        g = esp_gpio[net]
        return strap.get(g, 'UART0 TXD by default' if g == 16 else 'UART0 RXD by default' if g == 17 else '3.3 V GPIO')
    if net.startswith('FPGA_RGB'): return 'iCE40 RGB current-sink driver (open-drain style, not plain GPIO); no on-module LED in v2'
    if net.startswith('FPGA_IO'): return '3.3 V FPGA I/O (bank 0/2 at VCCIO 3.3 V)'
    return ''

rows = []
for n in range(1, 76):
    if 59 <= n <= 66: continue
    net = pads['J1'][str(n)]
    side = 'front (odd)' if n % 2 else 'back (even)'
    ic = pad = ''
    if net in ('GND', '+3.3V'): pass
    elif net in esp: ic, pad = 'U1', esp[net]
    elif net in fpga: ic, pad = 'U2', fpga[net]
    gpio = f'GPIO{esp_gpio[net]}' if net in esp_gpio and ic == 'U1' else ''
    rows.append({'Connector': 'J1', 'Contact': n, 'Side': side, 'Signal': net, 'IC': ic, 'Package_pad': pad, 'ESP32_C6_GPIO': gpio, 'Constraint': constraint(n, net)})
with open(D / 'docs/icd-v2-pinout.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['Connector', 'Contact', 'Side', 'Signal', 'IC', 'Package_pad', 'ESP32_C6_GPIO', 'Constraint']); w.writeheader(); w.writerows(rows)

link_notes = {'FPGA_SPI_SCK': 'GPIO matrix clock (not the native FSPICLK pin); keep the configuration SPI clock modest and verify timing',
              'FPGA_SPI_MOSI': 'GPIO matrix', 'FPGA_SPI_MISO': 'GPIO matrix', 'FPGA_SPI_CS_N': 'GPIO matrix chip select',
              'FPGA_SPI_IO2': 'GPIO matrix; quad lane, avoids strapping pins', 'FPGA_SPI_IO3': 'GPIO matrix; quad lane, avoids strapping pins',
              'FPGA_CRESET_N': 'R28 10k pull-down keeps the FPGA in reset until the ESP releases it; TP1', 'FPGA_CDONE': 'R29 10k pull-up to 3.3 V; TP2'}
with open(D / 'docs/c6-fpga-link.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['Signal', 'ESP32_C6_GPIO', 'ESP32_C6_QFN40_pad', 'FPGA_SG48_pad', 'Notes'])
    for net in ('FPGA_SPI_SCK', 'FPGA_SPI_MOSI', 'FPGA_SPI_MISO', 'FPGA_SPI_CS_N', 'FPGA_SPI_IO2', 'FPGA_SPI_IO3', 'FPGA_CRESET_N', 'FPGA_CDONE'):
        w.writerow([net, esp_gpio[net], esp[net], fpga[net], link_notes[net]])

c = json.load(open(D / 'docs/design-contract.json'))
c['status'] = 'design_draft_routed_not_for_fabrication'
c['processor'].update({'mpn': 'ESP32-C6', 'package': 'QFN40 5x5 mm, 0.4 mm pitch, 3.3 mm exposed pad (flashless ESP32-C6; LCSC C5364646)',
                       'flash': 'W25Q128JVPIQ 16 MB quad SPI NOR (WSON-8 6x5, LCSC C190862) on SPI0/1 (QIO), powered from the 3.3 V plane; VDD_SPI (pin 23) unconnected',
                       'gpio_exposed': 13, 'link': {net: {'gpio': esp_gpio[net], 'c6_pad': esp[net], 'fpga_pad': fpga[net]} for net in link_notes},
                       'spi_routing': 'All six QSPI link signals and CRESET/CDONE go through the GPIO matrix (pads 6-9, 12, 13, 16, 17); no strapping pin is used. Verify the configuration clock the C6 can drive through the matrix before relying on quad mode.',
                       'usb': 'USB Serial/JTAG on GPIO12/13 (pads 18/19) to back contacts 26 (D-) and 24 (D+)'})
c['contacts'] = {str(r['Contact']): r['Signal'] for r in rows}
c['sourcing'] = {'ESP32-C6': 'LCSC C5364646 (QFN40, flashless)', 'W25Q128JVPIQ': 'LCSC C190862 (about 12k in stock on 2026-10-08)',
                 'LQP03TG24NJ02D': 'L5, 24 nH 0201 for XTAL_P: LCSC number still to assign', 'confirm': 'Check stock for all parts at order time'}
c['layout'] = {'layers': 'F.Cu signal/components, In1 GND, In2 +3.3V plane with a +1.2V island under U2, B.Cu ESP bus and FPGA lanes to the back contacts',
               'contact_field': 'Front ground contacts each carry a via 1.3 mm above the pad; the back-contact lanes beside them step 0.15 mm aside and re-enter their pads straight. Contact 33 (formerly ground) carries ESP_GPIO4 through the same via.',
               'flash': 'U4 north-east of U1, rotated so DI/CLK/HOLD fan straight into its south row; WP/DO/CS run up the east side. The flash pin order is mirrored against the C6 SPI pins, so WP and DO cross under CS on B.Cu in the corner above U4 (two vias each).',
               'stackup': {'name': 'JLCPCB JLC04081H-3313', 'nominal_mm': 0.799, 'why': 'M.2 requires 0.8 +/- 0.08 mm; JLCPCB 0.8 mm 4-layer builds are 0.721-0.803 mm nominal with +/- 0.1 mm tolerance, so the best-centred build was chosen',
                           'layers': '35 um Cu / 0.0994 mm 3313 prepreg er 4.1 / In1 GND / 0.5 mm core er 4.48 / In2 +3.3V / 0.0994 mm 3313 / 35 um Cu',
                           'rf_feed': '50 ohm coated CPWG 0.14 mm trace / 0.15 mm gap (JLCPCB calculator 50.4 ohm, field solve 49.9 ohm; docs/rf-feed.json)'},
               'card_edge': {'source': 'https://jlcpcb.com/help/article/jlcpcb-gold-fingers (read 2026-10-07)',
                             'finish': 'ENIG with the gold-finger option (JLCPCB plates fingers gold only under ENIG; HASL would tin them)',
                             'bevel': '30 deg (JLCPCB offers 30/45 only; the M.2 drawing shows 20 deg, confirm socket fit). Copper setback 0.6 mm from the routed edge: JLCPCB quotes ~1.13 mm at 1.6 mm board thickness for 30 deg, scaled to 0.8 mm and rounded up.',
                             'solder_mask': 'Finger field fully opened on both sides (window in the J1 footprint); no pour or via inside the window (rule area m2-finger-window).',
                             'panel': 'A board or panel with gold fingers must be at least 50 x 50 mm and chamfers need >= 5 x 5 cm, so the 22 x 42 mm card is ordered as a panel with the connector edge on the panel outline; a V-cut may not cross the fingers.'},
               'deviations': ['Eight ground vias sit in the two exposed pads (U1 four, U2 four); the playbook forbids vias under packages but a grounded exposed pad has no other return.',
                              'C48/C50 and C39 return to ground through the front pour (no dedicated via fits beside the contact fan / the XTAL_N drop).',
                              'VDD_SPI (U1 pin 23) is left unconnected: the flash is powered from the 3.3 V plane (allowed by the datasheet) because pin 23 sits between the flash data pins and its 0.1/1 uF pair would not fit. The flash has 0.1 uF (C68) at pin 8 and C33 (10 uF) on the plane 4 mm away; no 1 uF at the flash.',
                              'Decoupling beyond 2 mm: U2 pin 5 (C50 2.9 mm, boxed in by the CRESET/CDONE drops and the pin-4/6 exits), U2 pin 29 (C44 2.9 mm; pins 28/30 exit either side so only one cap fits on the 29/30 pair and it went to the core pin 30), U2 pin 33 (C46 3.7 mm, plane via at the pin), U1 VDDA3P3 pins 2/3 (C35 3.6 mm; the RF match owns the space beside pins 1-3), U1 VDDPST1 pin 5 (C37 2.7 mm, west of the four link columns), U1 VDDPST2 pin 28 (C38 2.4 mm, beyond the GPIO15/TXD/RXD vias at 0.4 mm pitch).']}
json.dump(c, open(D / 'docs/design-contract.json', 'w'), indent=2); open(D / 'docs/design-contract.json', 'a').write('\n')
print('wrote icd-v2-pinout.csv', len(rows), 'contacts; c6-fpga-link.csv; design-contract.json')
