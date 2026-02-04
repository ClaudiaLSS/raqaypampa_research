#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 15:02:59 2026

@author: claudia
"""

import pandas as pd
import os
from pathlib import Path

# .parent moves up to 'preprocess'
# .parent.parent moves up to 'timeseries'
# .parent.parent.parent moves up to 'scripts'
# .parent.parent.parent.parent moves up to the project root 'raqaypampa_research'
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Define the paths based on your specific structure
RAW_DIR = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "TPDIN"
PROCESSED_DIR = BASE_DIR / "data" / "raw" / "timeseries"/'raw_timeseries'

def reorder_no_headers(file_name):
    input_path = RAW_DIR / file_name
    output_path = PROCESSED_DIR / f"reordered_{file_name}"
    
    print(f"🔍 Searching for: {input_path}")
    
    if not input_path.exists():
        print(f"❌ Error: {file_name} not found.")
        return

    # header=None ensures the first row of data is treated as data, not column names
    df = pd.read_csv(input_path, header=None)

    # 1. Flip the rows vertically
    df_reversed = df.iloc[::-1].reset_index(drop=True)

    # 2. Save without writing a header row or index
    df_reversed.to_csv(output_path, index=False, header=False)
    
    print(f"✅ Success! Reordered {len(df_reversed)} rows.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    reorder_no_headers("user_96_merged.csv")