#!/usr/bin/env python3
"""Audit csv_light2.zip without extracting data or requiring external packages."""
import argparse
import collections
import csv
import io
import json
import re
import zipfile
from pathlib import Path

EXPECTED_COLUMNS = ['SysTimeMsecs','X','Y','Z','Rx','Ry','Rz','TorchSignal','Voltage','Current','WireFeedSpeed']
NAME = re.compile(r'^csv_light2/g(0[1-5])_(30|40|50|60|70)/g\1_s(\d{2,3})\.csv$')

def audit(archive):
    report = {'archive': Path(archive).name, 'groups': {}, 'warnings': [], 'errors': []}
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            if entry.is_dir() or not entry.filename.lower().endswith('.csv'):
                continue
            match = NAME.fullmatch(entry.filename)
            if not match:
                report['warnings'].append('Unexpected CSV path: '+entry.filename)
                continue
            group, speed, number = match.groups()
            expected_group = (int(number)-1)//30+1
            if int(group) != expected_group or int(speed) != int(group)*10+20:
                report['errors'].append(f'{entry.filename}: inconsistent group, speed, or sample ID')
            key = f'g{group}_{speed}'
            info = report['groups'].setdefault(key, {'speed_cm_min':int(speed), 'csv_count':0,'rows':0,'files':[]})
            with z.open(entry) as stream:
                reader = csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig', newline=''))
                if reader.fieldnames != EXPECTED_COLUMNS:
                    report['errors'].append(f'{entry.filename}: unexpected header {reader.fieldnames}')
                row_count = 0
                active = 0
                for row in reader:
                    row_count += 1
                    if row.get('TorchSignal','').strip() == '1':
                        active += 1
            info['csv_count'] += 1
            info['rows'] += row_count
            info['files'].append({'name':Path(entry.filename).name,'rows':row_count,'active_rows':active})
        all_names = [x.filename for x in z.infolist() if not x.is_dir()]
        report['file_types'] = dict(sorted(collections.Counter(Path(n).suffix.lower().lstrip('.') for n in all_names).items()))
    for g in report['groups'].values():
        g['files'].sort(key=lambda x: x['name'])
        if g['csv_count'] != 30:
            report['errors'].append(f"Speed {g['speed_cm_min']}: expected 30 CSV, got {g['csv_count']}")
    report['total_csv'] = sum(g['csv_count'] for g in report['groups'].values())
    report['total_rows'] = sum(g['rows'] for g in report['groups'].values())
    if report['total_csv'] != 150:
        report['errors'].append(f"Expected 150 CSV, got {report['total_csv']}")
    return report

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('archive', help='Path to csv_light2.zip')
    p.add_argument('--out', help='JSON output file (optional)')
    args = p.parse_args()
    report = audit(args.archive)
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(output+'\n',encoding='utf-8')
    print(f"CSV: {report['total_csv']}; rows: {report['total_rows']}; errors: {len(report['errors'])}; warnings: {len(report['warnings'])}")
    for key, g in sorted(report['groups'].items()):
        print(f"{key}: {g['csv_count']} files, {g['rows']} rows")
    for e in report['errors']:
        print('ERROR:',e)
    for w in report['warnings']:
        print('WARN:',w)
    raise SystemExit(1 if report['errors'] else 0)
