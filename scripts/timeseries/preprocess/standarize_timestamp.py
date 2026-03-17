#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 21:49:21 2026

@author: claudia
"""

import pandas as pd
from pathlib import Path

def standardize_timestamp_column(file_path):
    # 1. Load the file
    df = pd.read_csv(file_path)
    
    if 'corrected_timestamp' not in df.columns:
        print("❌ Column 'corrected_timestamp' not found.")
        return

    # 2. Clean the string: Remove EVERYTHING except numbers, slashes, colons, and spaces
    # This deletes hidden characters like 'Š' or symbols
    df['corrected_timestamp'] = df['corrected_timestamp'].astype(str).str.replace(r'[^0-9/:\-\s]', '', regex=True)

    # 3. Convert to Datetime
    # format='mixed' handles cases where some rows are Day/Month and others Month/Day
    df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'], format='mixed', errors='coerce')

    # 4. Save back to CSV 
    # This will save it in the standard YYYY-MM-DD HH:MM:SS format
    df.to_csv(file_path, index=False)
    print(f"✅ Corrected and standardized: {file_path}")

# Apply it to your problematic file
file_to_fix = Path("/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/OLD_DL/old_user_23.csv")
standardize_timestamp_column(file_to_fix)