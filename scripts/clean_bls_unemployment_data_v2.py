"""
Standardize BLS 14-month county-level unemployment data into CSV

- https://www.bls.gov/lau/tables.htm


Usage:
    python clean_bls_unemployment_data_v2.py [local_path_to_laucntycur14.txt]

"""
import csv
import datetime
import sys
import zipfile
from pathlib import Path

import fastexcel
import requests
import polars as pl



def main(local_path):
    local_zipfile = Path(local_path)
    if local_zipfile.is_absolute():
        output_dir = infile.parent
    else:
        output_dir = Path.cwd()
    excel_file = extract_zip(local_zipfile)
    reader = fastexcel.read_excel(excel_file)
    sheet = reader.load_sheet(0, header_row=2)

    # Convert to Polars DataFrame for easier manipulation
    orig_df = sheet.to_polars()
    # Rename columns to match our desired output
    df = orig_df.rename({
        'LAUS Code': 'laus_area_code',
        'State FIPS Code': 'fips_state',
        'County FIPS Code': 'fips_county',
        'County Name/State Abbreviation': 'county_state',
        'Period': 'period',
        'Labor Force': 'labor_force',
        'Employed': 'employed',
        'Unemployed': 'unemployed',
        'Unemploy-ment Rate (%)': 'unemployed_rate',
    })
    # Remove annotation rows at end of file (which should be only rows with null fips state/county
    df = df.filter( pl.col('fips_state').is_not_null())
    df_new_cols = df.with_columns([
        pl.col('county_state').str.split(',').list.get(0).str.strip_chars().alias('county'),
        # District of Columbia is an outlier with no comma, so we get the second element of the split and fill nulls with 'DC'
        pl.col('county_state').str.split(',').list.get(1, null_on_oob=True).str.strip_chars().fill_null('DC').alias('state'),
    ]).with_columns(
        # Remove any trailing whitespace and letters
        pl.col("period").str.replace(r"\s+[a-zA-Z]+$", "").alias("date_clean")
    ).with_columns(
        (pl.col("date_clean") + "-01").str.to_date("%b-%y-%d").alias("_parsed")
    ).with_columns([
        pl.col("_parsed").dt.strftime("%B").alias("month"),
        pl.col("_parsed").dt.month().alias("month_num"),
        pl.col("_parsed").dt.year().cast(pl.Int32).alias("year"),
        pl.col("_parsed").dt.strftime("%Y-%m-%d").alias("date"),
    ]).drop(["_parsed", "date_clean"])
    # Write data to CSV, sans index
    output_file = output_dir / "bls_county_unemployment.csv"
    #df_new_cols.write_csv(output_file, null_value='NULL', quote_style="non_numeric")
    df_new_cols.write_csv(output_file, quote_style="non_numeric")

def extract_zip(zip_path):
    # Extract to current working directory
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()
        # Return the name of the extracted file
        return zip_ref.namelist()[0]


if __name__ == '__main__':
    try:
        local_path = sys.argv[1]
    except IndexError:
        local_path = 'laucntycur14.zip'
    main(local_path)
