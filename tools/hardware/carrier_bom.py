#!/usr/bin/env python3
"""Generate grouped carrier BOMs from native KiCad schematic export."""
import csv
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
BOARD = ROOT / 'boards/programming-carrier'
def refkey(ref):
    return (re.sub(r'\d+', '', ref), int(re.search(r'\d+', ref).group()))
def main():
    with tempfile.TemporaryDirectory() as td:
        xml = Path(td) / 'netlist.xml'
        subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadxml', '-o', str(xml), str(BOARD / 'carrier.kicad_sch')], check=True)
        root = ET.parse(xml)
    groups = defaultdict(list)
    excluded = []
    for comp in root.findall('./components/comp'):
        ref = comp.get('ref')
        props = {p.get('name') for p in comp.findall('property')}
        if props & {'exclude_from_bom', 'dnp'}:
            excluded.append(ref)
            continue
        fields = {f.get('name'): f.text or '' for f in comp.findall('./fields/field')}
        mpn, lcsc = fields.get('MPN', ''), fields.get('LCSC', '')
        assert mpn and re.fullmatch(r'C\d+', lcsc), (ref, 'Missing exact purchasing fields')
        footprint = comp.findtext('footprint')
        groups[(mpn, lcsc, footprint)].append((ref, comp.findtext('value')))
    rows = []
    for (mpn, lcsc, footprint), items in groups.items():
        items.sort(key=lambda x: refkey(x[0]))
        values = list(dict.fromkeys(v for _, v in items))
        rows.append({'Comment': ' / '.join(values), 'Designator': ','.join(r for r, _ in items), 'Footprint': footprint, 'LCSC Part #': lcsc, 'Quantity': len(items), 'MPN': mpn, 'Supplier URL': f'https://www.lcsc.com/product-detail/{lcsc}.html'})
    rows.sort(key=lambda r: refkey(r['Designator'].split(',')[0]))
    for relative, columns in [
        ('fab/bom/carrier-bom.csv', ['Comment','Designator','Quantity','Footprint','MPN','LCSC Part #','Supplier URL']),
        ('fab/jlcpcb/BOM_carrier.csv', ['Comment','Designator','Footprint','LCSC Part #']),
    ]:
        output = BOARD / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
            writer.writeheader(); writer.writerows(rows)
    print(f'{len(rows)} BOM groups; {sum(r["Quantity"] for r in rows)} populated parts; excluded {", ".join(sorted(excluded, key=refkey))}')
if __name__ == '__main__':
    main()
