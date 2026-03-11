#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 21:10:09 2026

@author: claudia
"""

import pandas as pd
from pathlib import Path

# --- SET YOUR PATHS ---
BASE_DIR = Path("/home/claudia/Documents/raqaypampa_research")
INPUT_FILE = BASE_DIR / "data" / "clean" / "timeseries" / "OLD_DL" / "user_84_clean.csv"
OUTPUT_FILE = BASE_DIR / "data" / "clean" / "timeseries" / "OLD_DL" / "user_84_clean_corrected.csv"


def scale_parameters(file_path, output_path, divisor=1000):
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    # 1. Load the data
    df = pd.read_csv(file_path)
    
    # 2. Define protected columns that SHOULD NOT be divided
    protected_cols = ['datetime', 'date', 'time', 'corrected_timestamp', 'Unnamed: 5']
    
    print(f"⚖️ Scaling numeric parameters by {divisor}...")

    # 3. Iterate through columns and divide if they are numeric and not protected
    for col in df.columns:
        if col in protected_cols:
            continue
            
        # Try to convert to numeric to verify it's a data column
        # This prevents errors if there are stray text columns
        converted_series = pd.to_numeric(df[col], errors='coerce')
        
        if not converted_series.isna().all():
            # Apply the division
            df[col] = converted_series / divisor
            print(f" ✅ Divided column: {col}")
        else:
            print(f" ⏩ Skipped non-numeric column: {col}")

    # 4. Save the result
    OUTPUT_DIR = output_path.parent
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Success! Scaled file saved to: {output_path.name}")

if __name__ == "__main__":
    scale_parameters(INPUT_FILE, OUTPUT_FILE)