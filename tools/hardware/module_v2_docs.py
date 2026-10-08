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
            'ESP_GPIO19': 19, 'ESP_GPIO20': 20, 'ESP_GPIO21': 21, 'ESP_GPIO22': 22, 'ESP_GPIO23': 23,
            'FPGA_SPI_IO3': 0, 'FPGA_SPI_MOSI': 1, 'FPGA_SPI_CS_N': 2, 'FPGA_SPI_SCK': 3, 'FPGA_SPI_MISO': 6, 'FPGA_SPI_IO2': 7,
            'FPGA_CRESET_N': 14, 'FPGA_CDONE': 18, 'USB_D-': 12, 'USB_D+': 13}
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
    w = csv.writer(f); w.writerow(['Signal', 'ESP32_C6_GPIO', 'ESP32_C6_QFN32_pad', 'FPGA_SG48_pad', 'Notes'])
    for net in ('FPGA_SPI_SCK', 'FPGA_SPI_MOSI', 'FPGA_SPI_MISO', 'FPGA_SPI_CS_N', 'FPGA_SPI_IO2', 'FPGA_SPI_IO3', 'FPGA_CRESET_N', 'FPGA_CDONE'):
        w.writerow([net, esp_gpio[net], esp[net], fpga[net], link_notes[net]])

c = json.load(open(D / 'docs/design-contract.json'))
c['status'] = 'design_draft_routed_not_for_fabrication'
c['processor'].update({'package': 'QFN32 5x5 mm, 0.5 mm pitch (ESP32-C6FH8 / FH4; flashless ESP32-C6 is QFN40 and does not fit)',
                       'gpio_exposed': 12, 'link': {net: {'gpio': esp_gpio[net], 'c6_pad': esp[net], 'fpga_pad': fpga[net]} for net in link_notes},
                       'spi_routing': 'All six QSPI link signals and CRESET/CDONE go through the GPIO matrix (pads 6-9, 12, 13, 18, 23); no strapping pin is used. Verify the configuration clock the C6 can drive through the matrix before relying on quad mode.',
                       'usb': 'USB Serial/JTAG on GPIO12/13 (pads 16/17) to back contacts 24 (D-) and 22 (D+)'})
c['contacts'] = {str(r['Contact']): r['Signal'] for r in rows}
c['sourcing'] = {'ESP32-C6FH8': 'LCSC C41459370 (no stock on 2026-10-07); ESP32-C6FH4 C6908287 (no stock); plan a distributor buy or confirm stock before ordering assembly'}
c['layout'] = {'layers': 'F.Cu signal/components, In1 GND, In2 +3.3V plane with a +1.2V island under U2, B.Cu ESP bus and FPGA lanes to the back contacts',
               'contact_field': 'Front ground contacts each carry a via 1.3 mm above the pad; the back-contact lanes beside them step 0.15 mm aside and re-enter their pads straight.',
               'deviations': ['Eight ground vias sit in the two exposed pads (U1 four, U2 four); the playbook forbids vias under packages but a grounded exposed pad has no other return.',
                              'C48/C50 and C39 return to ground through the front pour (no dedicated via fits beside the contact fan / the XTAL_N drop).',
                              'Decoupling beyond 2 mm: U2 pins 5/29/30 (2.9 mm), U2 pin 33 (3.7 mm, plane via at the pin), U1 VDDA3P3 pins 2/3 (3.3 mm to the pi filter), U1 pin 20 (2.2 mm).']}
json.dump(c, open(D / 'docs/design-contract.json', 'w'), indent=2); open(D / 'docs/design-contract.json', 'a').write('\n')
print('wrote icd-v2-pinout.csv', len(rows), 'contacts; c6-fpga-link.csv; design-contract.json')
