"""Check explicitly supplied milestone dates. Does not calculate legal deadlines."""
import argparse
import csv
from datetime import date
import json
import re

FIELDS = ['milestone_id', 'milestone', 'approved_date', 'source_id', 'reviewer', 'approval_status']

def iso_date(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value): raise ValueError('expected YYYY-MM-DD')
    return date.fromisoformat(value)

def review(path):
    records = []
    groups = {}
    with open(path, encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, strict=True)
        if reader.fieldnames != FIELDS: raise ValueError('headers must be exactly: ' + ','.join(FIELDS))
        for n, raw in enumerate(reader, 2):
            if None in raw or any(v is None for v in raw.values()): raise ValueError('wrong number of fields at record ' + str(n))
            row = {k: v.strip() for k,v in raw.items()}
            codes = []
            for name in ('milestone_id', 'milestone', 'source_id', 'reviewer'):
                if not row[name]: codes.append('missing_' + name)
            if row['approval_status'] not in ('approved', 'pending', 'superseded'):
                codes.append('invalid_approval_status')
            elif row['approval_status'] != 'approved': codes.append('not_approved')
            if not row['approved_date']: codes.append('missing_date')
            else:
                try: iso_date(row['approved_date'])
                except ValueError: codes.append('invalid_date')
            record = {'record': n, **row, 'issues': codes}
            records.append(record)
            if row['milestone_id']: groups.setdefault(row['milestone_id'], []).append(record)
    if not records: raise ValueError('no data records')
    for group in groups.values():
        if len(group) < 2: continue
        active_dates = {r['approved_date'] for r in group if r['approval_status'] != 'superseded' and r['approved_date']}
        code = 'conflicting_dates' if len(active_dates) > 1 else 'repeated_milestone_id'
        for row in group: row['issues'].append(code)
    ready = [{'milestone_id': r['milestone_id'], 'milestone': r['milestone'], 'approved_date': r['approved_date'], 'source_id': r['source_id'], 'reviewer': r['reviewer']} for r in records if not r['issues']]
    return {'records': len(records), 'reviewable_dates': ready, 'issues': [{'record': r['record'], 'milestone_id': r['milestone_id'], 'issues': r['issues']} for r in records if r['issues']]}

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('csv_file'); args = p.parse_args()
    try: result = review(args.csv_file)
    except (ValueError, OSError, csv.Error) as error: p.exit(2, 'Input error: ' + str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == '__main__': main()
