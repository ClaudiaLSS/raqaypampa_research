#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 20:32:14 2026

@author: claudia
"""

import pandas as pd
import re
from pathlib import Path

# --- SET YOUR PATHS ---
BASE_DIR = Path("/home/claudia/Documents/raqaypampa_research")
INPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "raw_merged_user_23.csv"
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "raw_merged_user_23_corrected.csv"

def clean_datalogger_symbols(file_path, output_path):
    # 1. Load the dataset
    df = pd.read_csv(file_path)
    
    # Columns we expect to be numeric
    numeric_cols = ['v_led_1', 'v_pv', 'c_pv', 'c_cons']
    
    print("🔍 Searching for special characters...")
    
    for col in numeric_cols:
        if col not in df.columns:
            continue
            
        # Identify rows with symbols (anything that isn't a digit, dot, or minus sign)
        # This helps us answer "which symbols are there"
        all_text = "".join(df[col].astype(str).unique())
        symbols = set(re.findall(r'[^0-9.\-\s]', all_text))
        
        if symbols:
            print(f"📍 Column '{col}' contains these symbols: {symbols}")
        
        # 2. CONVERT TO NUMERIC
        # errors='coerce' turns strings with symbols into NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 3. REPLACE WITH PREVIOUS VALUE (Forward Fill)
        # This takes the previous valid numeric value and copies it down
        df[col] = df[col].ffill()
        
        # Optional: Backfill in case the very first row was a symbol
        df[col] = df[col].bfill()

    # 4. Cleanup: Remove the empty trailing column if it exists
    if 'Unnamed: 5' in df.columns:
        df = df.drop(columns=['Unnamed: 5'])

    # 5. Save the cleaned file
    df.to_csv(output_path, index=False)
    print(f"\n✅ Success! Cleaned file saved to: {output_path}")

if __name__ == "__main__":
    clean_datalogger_symbols(INPUT_FILE, OUTPUT_FILE)