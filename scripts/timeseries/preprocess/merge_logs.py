#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 15:24:36 2026

@author: claudia
"""

from pathlib import Path
import pandas as pd
import re

def combine_logs_chronologically(input_folder: Path, output_file: Path):
    if not input_folder.exists():
        print(f"❌ Error: Folder {input_folder} does not exist.")
        return

    # 1. Get all CSV files
    files = [f for f in input_folder.iterdir() if f.suffix.lower() == ".csv"]
    if not files:
        print("No CSV files found.")
        return

    # 2. SORT FILES: Highest number to lowest (Oldest File to Newest File)
    # Result: log(9), log(8), ..., log(1), log.csv
    def get_log_number(f):
        match = re.search(r"\((\d+)\)", f.name)
        return int(match.group(1)) if match else 0

    files.sort(key=get_log_number, reverse=True)

    print("Merging Order (Processing oldest file first):")
    all_dataframes = []
    
    for file in files:
        print(f" - Reading and flipping rows of: {file.name}")
        
        # Read the file (Assuming no header based on your sample)
        df = pd.read_csv(file, header=None)
        
        # 3. REVERSE ROWS: Flip THIS log upside down 
        # (Internal Newest->Oldest becomes Oldest->Newest)
        df_flipped = df.iloc[::-1].reset_index(drop=True)
        
        all_dataframes.append(df_flipped)

    # 4. UNIFY: Concatenate the flipped blocks
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        # 5. SAVE: Create directory if it doesn't exist and save
        output_file.parent.mkdir(parents=True, exist_ok=True)
        combined_df.to_csv(output_file, index=False, header=False)
        
        print(f"\n✅ Success! Merged {len(files)} files.")
        print(f"Final timeseries: Oldest data at the top -> Newest data at the bottom.")
        print(f"Saved to: {output_file}")

if __name__ == "__main__":
    # Adjusting to reach the project root 'raqaypampa_research'
    # Based on your structure, it is 3 levels up from this script
    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    USER_ID = "user_11"
    LOGGER_TYPE = "TPDIN"

    INPUT_FOLDER = (
        PROJECT_ROOT / "data" / "raw" / "timeseries" / LOGGER_TYPE / USER_ID
    )

    OUTPUT_FILE = (
        PROJECT_ROOT / "data" / "raw" / "timeseries" / "merged" / LOGGER_TYPE / f"{USER_ID}_merged_raw.csv"
    )

    combine_logs_chronologically(INPUT_FOLDER, OUTPUT_FILE)