"""
This pythong script is for concatenates all monthly CRMLSSOLD CSV files into one combined
sold.csv, where filters to PropertyType == 'Residential'.
"""

import pandas as pd
import glob
import os


DATA_FOLDER = "/Users/yanxif/Documents/IDX/summer analyst"  

SOLD_PATTERN = os.path.join(DATA_FOLDER, "CRMLSSold*.csv")
OUTPUT_FILE = os.path.join(DATA_FOLDER, "sold.csv")


def main():
    files = sorted(glob.glob(SOLD_PATTERN))

    if not files:
        raise FileNotFoundError(
            f"No files found matching {SOLD_PATTERN}. Check DATA_FOLDER and file naming."
        )

    print(f"Found {len(files)} monthly sold files:")
    for f in files:
        print(f"  {os.path.basename(f)}")

    dfs = []
    total_rows_before = 0
    for f in files:
        try:
            df = pd.read_csv(f, low_memory=False, encoding="utf-8")
        except UnicodeDecodeError:
            print(f"  (utf-8 failed for {os.path.basename(f)}, retrying with latin-1)")
            df = pd.read_csv(f, low_memory=False, encoding="latin1")
        total_rows_before += len(df)
        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal rows across individual files (before concat): {total_rows_before}")
    print(f"Rows after concat: {len(combined)}")


    print("\nUnique PropertyType values before filtering:")
    print(combined["PropertyType"].unique())

    before = len(combined)
    residential = combined[combined["PropertyType"] == "Residential"].copy()
    after = len(residential)

    print(f"\nRows before Residential filter: {before}")
    print(f"Rows after Residential filter: {after}")
    print(f"Rows dropped: {before - after}")

    residential.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()