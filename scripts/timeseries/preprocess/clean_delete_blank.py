#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 17:41:33 2026

@author: claudia
"""

import pandas as pd
from pathlib import Path

# --- SET YOUR PATHS ---
BASE_DIR = Path("/home/claudia/Documents/raqaypampa_research")
INPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "raw_merged_user_63.csv"
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "raw_merged_user_63_clean.csv"

def delete_blank_logs(file_path, output_path):
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    # 1. Load the data
    df = pd.read_csv(file_path)
    initial_count = len(df)
    
    # 2. Drop rows where BOTH date and time are missing
    # Change how='all' to how='any' if you want to delete rows where even one is missing
    df_clean = df.dropna(subset=['date', 'time'], how='all')
    
    final_count = len(df_clean)
    deleted_rows = initial_count - final_count

    # 3. Save the result
    df_clean.to_csv(output_path, index=False)
    
    print(f"✅ Success!")
    print(f"🗑️ Deleted {deleted_rows} blank rows.")
    print(f"💾 Saved cleaned file to: {output_path.name}")

if __name__ == "__main__":
    delete_blank_logs(INPUT_FILE, OUTPUT_FILE)