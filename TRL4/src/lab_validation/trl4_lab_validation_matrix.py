from pathlib import Path
import argparse, re
from common_io import resolve_zip, list_zip_assets, detect_group, write_json, write_markdown

def stem_key(path: str) -> str:
    return Path(path).stem

def main():
    ap = argparse.ArgumentParser(description='TRL4 CSV-2D-3D lefedettségi és robusztussági mátrix')
    ap.add_argument('--zip', default=None)
    args = ap.parse_args()
    zp = resolve_zip(args.zip)
    assets = list_zip_assets(zp)
    csv_keys = {stem_key(p): p for p in assets['csv']}
    jpg_keys = {stem_key(p): p for p in assets['jpg']}
    ply_keys = {stem_key(p): p for p in assets['ply']}
    matrix = []
    for k, p in sorted(csv_keys.items()):
        matrix.append({'sample': k, 'group': detect_group(p), 'csv': True, 'jpg': k in jpg_keys, 'ply': k in ply_keys, 'modalities': 1 + int(k in jpg_keys) + int(k in ply_keys)})
    coverage = {
        'csv_total': len(csv_keys), 'jpg_total': len(jpg_keys), 'ply_total': len(ply_keys),
        'csv_2d_3d_full': sum(1 for r in matrix if r['modalities'] == 3),
        'csv_2d': sum(1 for r in matrix if r['csv'] and r['jpg']),
        'csv_3d': sum(1 for r in matrix if r['csv'] and r['ply']),
    }
    out = {'trl':'TRL4', 'coverage': coverage, 'threshold_protocol': {'grid_percent':[91,92,93,94,95,96,97,98,99], 'start_percent':97, 'source':'GÉP 2026/1/1'}, 'matrix': matrix}
    write_json(Path('outputs/trl4_lab_validation_matrix.json'), out)
    lines = ['## Lefedettség'] + [f'- {k}: {v}' for k,v in coverage.items()]
    lines += ['', '## Robusztussági protokoll', '- Threshold grid: 91-99%.', '- Kezdőérték: 97%, de saját adaton újraellenőrizendő.', '- Repedés és belső hiba nem kezelhető önállóan 3D pontfelhővel.']
    write_markdown(Path('reports/trl4_lab_validation_report.md'), 'TRL4 laborvalidáció v5', lines)
    print('Kész: outputs/trl4_lab_validation_matrix.json és reports/trl4_lab_validation_report.md')
if __name__ == '__main__':
    main()
