#!/usr/bin/env python3
"""Regenerate page-addressable Markdown extracts and the local datasheet index.
Requires poppler's pdftotext. Original PDFs are never modified.
"""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'libraries/datasheets'
manifest=json.loads((D/'sources.json').read_text());by_file={r['file']:r for r in manifest}
index=['# Datasheet library','','Original supplier/manufacturer PDFs and searchable, page-numbered Markdown extractions.','PDF drawings and tables remain authoritative; text extraction may lose symbols or layout.','This folder includes historical parts: presence here does not imply a part is fitted.','','Regenerate with `python3 tools/datasheets/extract.py` (requires Poppler `pdftotext`).','','| Document | PDF | Markdown | Source / status |','|---|---|---|---|']
for pdf in sorted(D.glob('*.pdf')):
 r=by_file.setdefault(pdf.name,{'file':pdf.name,'status':'existing design reference; source not yet catalogued'})
 digest=hashlib.sha256(pdf.read_bytes()).hexdigest();r['sha256']=digest
 raw=subprocess.check_output(['pdftotext','-layout','-enc','UTF-8',str(pdf),'-']).decode('utf-8');pages=raw.split('\f')
 if not pages[-1].strip():pages.pop()
 r['pages']=len(pages);r['extraction']='pdftotext -layout, UTF-8; no OCR'
 lines=['# '+pdf.stem,'',f'Original PDF: [{pdf.name}]({pdf.name})','',f'SHA-256: `{digest}`','']
 if r.get('source_url'):lines += ['Source: '+r['source_url'],'']
 if r.get('parts'):lines += ['Parts: '+', '.join(r['parts']),'']
 if r.get('calibrator_references'):lines += ['GPS calibrator references: '+', '.join(r['calibrator_references']),'']
 lines += ['Machine-extracted text; consult the original PDF for drawings, symbols and table alignment.','']
 for n,page in enumerate(pages,1):lines += [f'## Page {n}','','```text',page.rstrip().replace('```','~~~'),'```','']
 pdf.with_suffix('.md').write_text('\n'.join(lines))
 source=f"[Publisher/source]({r['source_url']})" if r.get('source_url') else r['status']
 index.append(f'| {pdf.stem} | [PDF]({pdf.name}) | [MD]({pdf.stem}.md) | {source} |')
errors=[r for r in by_file.values() if r.get('error')]
if errors:index+=['','## Downloads still missing','']+[f"- {r['file']}: {r['error']} — {r['source_url']}" for r in errors]
(D/'sources.json').write_text(json.dumps(list(by_file.values()),indent=2)+'\n');(D/'README.md').write_text('\n'.join(index)+'\n')
print(f'{len(list(D.glob("*.pdf")))} PDF/Markdown pairs; {len(errors)} missing downloads')
