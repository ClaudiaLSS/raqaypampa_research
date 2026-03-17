#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 20:56:47 2026

@author: claudia
"""

import pandas as pd
from pathlib import Path

# --- SET YOUR PATHS ---
BASE_DIR = Path("/home/claudia/Documents/raqaypampa_research")
INPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "raw_merged_user_15_corrected.csv"
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "shortened_user_15.csv"

def delete_initial_rows(file_path, output_path, stop_index):
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    # 1. Load the data
    print(f"📂 Loading file...")
    df = pd.read_csv(file_path)
    
    initial_rows = len(df)
    print(f"📊 Current row count: {initial_rows}")

    # 2. Slice the dataframe
    # stop_index + 1 ensures that row 101949 is deleted and we start at 101950
    print(f"✂️ Deleting rows 0 to {stop_index}...")
    df_short = df.iloc[stop_index + 1:].reset_index(drop=True)

    # 3. Save the result
    df_short.to_csv(output_path, index=False)
    
    final_rows = len(df_short)
    print(f"✅ Success!")
    print(f"🗑️ Rows removed: {initial_rows - final_rows}")
    print(f"💾 New file saved as: {output_path.name}")

if __name__ == "__main__":
    # We use 101949 as the stop index
    delete_initial_rows(INPUT_FILE, OUTPUT_FILE, 101949)