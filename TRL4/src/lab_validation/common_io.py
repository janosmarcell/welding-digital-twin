from __future__ import annotations
import argparse, csv, json, os, re, zipfile
from pathlib import Path
from typing import Dict, List, Tuple

CSV_ZIP_HINT = Path('data/raw/csv_light2.zip')

def resolve_zip(cli_zip: str | None = None) -> Path:
    candidates = []
    if cli_zip:
        candidates.append(Path(cli_zip))
    candidates.append(CSV_ZIP_HINT)
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError('csv_light2.zip nem található. Add meg --zip argumentummal, vagy másold a data/raw mappába.')

def list_zip_assets(zip_path: Path) -> Dict:
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if not n.endswith('/')]
    files = {'csv': [], 'jpg': [], 'ply': [], 'other': []}
    for n in names:
        ext = Path(n).suffix.lower().strip('.')
        if ext in files:
            files[ext].append(n)
        else:
            files['other'].append(n)
    return files

def detect_group(path: str) -> str:
    m = re.search(r'g(\d{2})_(\d+)', path)
    if m:
        return f"g{m.group(1)}_{m.group(2)}"
    m = re.search(r'g(\d{2})', path)
    return f"g{m.group(1)}" if m else 'unknown'

def read_csv_from_zip(zip_path: Path, member: str) -> Tuple[List[str], List[Dict[str,str]]]:
    with zipfile.ZipFile(zip_path) as z:
        raw = z.read(member)
    text = raw.decode('utf-8', errors='replace')
    # Let csv detect separator conservatively
    sample = text[:2048]
    dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
    reader = csv.DictReader(text.splitlines(), dialect=dialect)
    rows = list(reader)
    return reader.fieldnames or [], rows

def find_torch_col(fields: List[str]) -> str | None:
    for f in fields:
        if f and f.lower().strip() in {'torchsignal','torch_signal','torch signal'}:
            return f
    for f in fields:
        if f and 'torch' in f.lower():
            return f
    return None

def active_segments(rows: List[Dict[str,str]], torch_col: str | None) -> List[Tuple[int,int]]:
    if not torch_col:
        return []
    segs = []
    in_seg = False
    start = 0
    for i, row in enumerate(rows):
        val = str(row.get(torch_col, '')).strip().replace(',', '.')
        active = val in {'1','1.0','True','true'}
        if active and not in_seg:
            start = i
            in_seg = True
        if in_seg and (not active):
            segs.append((start, i-1))
            in_seg = False
    if in_seg:
        segs.append((start, len(rows)-1))
    return segs

def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def write_markdown(path: Path, title: str, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('# '+title+'\n\n'+'\n'.join(lines)+'\n', encoding='utf-8')
