#!/usr/bin/env python3
"""Defined ordinary electricity-bill ratios. No network, account access or input changes."""
import argparse
import csv
from decimal import Decimal, DecimalException, ROUND_HALF_UP
import json
from pathlib import Path
import re

def number(value):
    if len(value) > 50 or not re.fullmatch(r'(?:\d+(?:\.\d*)?|\.\d+)', value):
        raise ValueError('Use a nonnegative plain decimal within the example range')
    return Decimal(value)

def display(value, places):
    return str(value.quantize(Decimal(places), rounding=ROUND_HALF_UP))

def review(path):
    path = Path(path)
    if path.stat().st_size > 2_000_000:
        raise ValueError('CSV exceeds the two-megabyte example limit')
    fields = ['bill_id', 'meter_id', 'unit', 'usage', 'billed_days', 'amount', 'currency', 'reading_basis']
    results, seen, boundary = [], set(), None
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != fields:
            raise ValueError('Expected headers: ' + ','.join(fields))
        for row in reader:
            if len(results) >= 10000:
                raise ValueError('CSV exceeds the 10,000-row example limit')
            if None in row or any(not isinstance(row.get(k), str) or not row[k].strip() for k in fields):
                raise ValueError('Every row needs eight nonempty fields')
            row = {k: row[k].strip() for k in fields}
            if row['bill_id'] in seen:
                raise ValueError('Duplicate bill identifier')
            seen.add(row['bill_id'])
            if row['unit'] != 'kWh' or not re.fullmatch(r'[A-Z]{3}', row['currency']):
                raise ValueError('Use kWh and a consistent three-letter uppercase currency identifier')
            current = (row['meter_id'], row['currency'])
            if boundary is None:
                boundary = current
            if current != boundary:
                raise ValueError('This example requires one meter and currency per comparison file')
            if not re.fullmatch(r'[1-9]\d{0,5}', row['billed_days']):
                raise ValueError('Billed days must be a positive whole number within the example range')
            days = Decimal(row['billed_days'])
            usage, amount = number(row['usage']), number(row['amount'])
            results.append({**row, 'usage_per_billed_day_kWh': display(usage / days, '0.0001'),
                            'selected_amount_per_billed_day': display(amount / days, '0.01'),
                            'selected_amount_divided_by_usage': None if usage == 0 else display(amount / usage, '0.0001')})
    if not results:
        raise ValueError('No bill rows supplied')
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file')
    args = parser.parse_args()
    try:
        result = review(args.csv_file)
    except (ValueError, OSError, csv.Error, DecimalException) as exc:
        parser.exit(2, 'Input error: ' + str(exc) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
