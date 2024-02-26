"""
Standardize BLS 14-month county-level unemployment data into CSV

- https://www.bls.gov/lau/#tables
- https://www.bls.gov/web/metro/laucntycur14.txt

Usage:
    python clean_bls_unemployment_data.py [local_path_to_laucntycur14.txt]

"""
import csv
import datetime
import sys
from pathlib import Path

def main(local_path):
    infile = Path(local_path)
    if infile.is_absolute():
        output_dir = infile.parent
    else:
        output_dir = Path.cwd()
    headers = [
        'laus_area_code',
        'fips_state',
        'fips_county',
        'area',
        'county',
        'state',
        'month_name',
        'month',
        'year',
        'date',
        'civ_labor_force',
        'employed',
        'unemployed',
        'unemployed_rate',
    ]
    clean_data_file = Path(output_dir, 'bls_monthly_unemployment_by_county.csv')
    print(f"Converting {infile} -> {clean_data_file}")
    with open(clean_data_file, 'w') as out:
        writer = csv.DictWriter(out, fieldnames=headers)
        writer.writeheader()
        for row in open(infile, 'r'):
            clean_row = row.strip()
            if clean_row.startswith('CN'):
                laus, fips_state, fips_cty, area, period, civ_labor_force, employed, unemployed, unemployed_rate = clean_row.split('|')
                try:
                    county, state = [bit.strip() for bit in area.split(',')]
                except ValueError:
                    if 'District' in area:
                        county = 'District of Columbia'
                        state = 'DC'
                    else:
                        breakpoint()
                period_clean = period.strip().replace('(p)','')
                period_dt = datetime.datetime.strptime(period_clean, '%b-%y')
                data = {
                    'laus_area_code': laus.strip(),
                    'fips_state': fips_state.strip(),
                    'fips_county': fips_cty.strip(),
                    'area': area.strip(),
                    'county': county,
                    'state': state,
                    'month_name': period.split('-')[0].strip(),
                    'month': period_dt.month,
                    'year': period_dt.year,
                    'date': period_dt.strftime('%Y-%m-%d'),
                    'civ_labor_force': clean_num(civ_labor_force),
                    'employed': clean_num(employed),
                    'unemployed':clean_num(unemployed),
                    'unemployed_rate': float(unemployed_rate.strip()),
                }
                writer.writerow(data)


def clean_num(num):
    return int(num.strip().replace(',',''))

if __name__ == '__main__':
    try:
        local_path = sys.argv[1]
    except IndexError:
        local_path = 'laucntycur14.txt'
    main(local_path)
