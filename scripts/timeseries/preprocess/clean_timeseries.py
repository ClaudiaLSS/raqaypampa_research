#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 15:51:57 2026

@author: claudia
"""

import pandas as pd
import re
from pathlib import Path

# 1. Setup paths according to your structure
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "timeseries" / "raw_timeseries" 
PROCESSED_DIR = BASE_DIR / "data" / "raw" / "timeseries" / "raw_timeseries" 

def clean_tp_din_file(file_name):
    input_path = PROCESSED_DIR / f"reordered_{file_name}"
    output_path = PROCESSED_DIR / f"cleaned_{file_name}"
    
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return

    # Load data without headers
    df = pd.read_csv(input_path, header=None)

    # 2. Split Column 0 into Date and Time
    # Handles the extra spaces between date and time
    datetime_split = df[0].str.split(expand=True)
    df_date = datetime_split[0]
    df_time = datetime_split[1]

    # 3. Split Column 1 into Day and Time_log
    # Handles "0 days 00:19:57" or "Event 254: Log Cleared"
    def split_log_info(val):
        val = str(val)
        if ' days ' in val:
            return val.split(' days ')
        elif ': ' in val:
            return val.split(': ', 1)
        return [val, ""]

    log_split = df[1].apply(split_log_info).apply(pd.Series)
    df_day = log_split[0]
    df_time_log = log_split[1]

    # 4. Remove 'V', 'A', and 'C' from numeric columns
    # Using regex to strip the units while keeping the numbers and signs
    def strip_units(val):
        if pd.isna(val): return val
        return re.sub(r'[VAC]', '', str(val))

    df_numeric = df.iloc[:, 2:].applymap(strip_units)

    # 5. Combine and assign headers
    # Note: Added 'c_extra' to account for the 9th data column in your file
    headers = [
        'date', 'time', 'day', 'time_log',
        'v_pv', 'v_usb', 'v_led_1', 'v_led_2',
        'c_usb', 'c_led_1', 'c_led_2', 'c_extra', 'temp'
    ]
    
    df_final = pd.concat([df_date, df_time, df_day, df_time_log, df_numeric], axis=1)
    df_final.columns = headers
    
    # --- NEW: 6. Calculate Interval Column ---
    # Create a temporary datetime series to calculate the difference
    temp_dt = pd.to_datetime(df_final['date'] + ' ' + df_final['time'])
    
    # Calculate difference between current and previous row
    # result is a Timedelta; we convert it to total minutes
    df_final['interval_min'] = temp_dt.diff().dt.total_seconds() / 60.0
    
    # Optional: Fill the first row (which will be NaN) with 0 or 5
    df_final['interval_min'] = df_final['interval_min'].fillna(0)

    # 6. Save final cleaned CSV
    df_final.to_csv(output_path, index=False)
    print(f"✅ Success! Cleaned file saved to: {output_path}")

if __name__ == "__main__":
    clean_tp_din_file("user_96_2_merged.csv")