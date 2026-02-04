#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 11:07:32 2026

@author: claudia
"""

import pandas as pd
from datetime import timedelta
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CLEAN_DIR = BASE_DIR / "data" / "raw" / "timeseries" / "raw_timeseries"

def reconstruct_segment_backward(file_name, anchor_timestamp_str):
    input_path = CLEAN_DIR / file_name
    output_path = CLEAN_DIR / f"segmented_{file_name}"
    
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return

    # 1. Load the data
    df = pd.read_csv(input_path)
    
    # --- Calculate time_step_min if it doesn't exist ---
    if 'time_step_min' not in df.columns:
        print("🔍 'time_step_min' not found. Calculating intervals now...")
        temp_dt = pd.to_datetime(df['date'] + ' ' + df['time'])
        df['time_step_min'] = temp_dt.diff().dt.total_seconds() / 60.0
        df['time_step_min'] = df['time_step_min'].fillna(0)
    
    # 2. Convert anchor to datetime
    anchor_dt = pd.to_datetime(anchor_timestamp_str)
    
    # 3. Initialize the new column
    df['corrected_timestamp'] = pd.NaT
    
    # 4. Perform Backward Calculation
    current_time = anchor_dt
    
    # Iterate from the last row down to 0
    for i in range(len(df) - 1, -1, -1):
        # Assign the calculated time to the current row
        df.at[i, 'corrected_timestamp'] = current_time
        
        # --- STOP CONDITION: Non-numeric Event ---
        val = df.at[i, 'day']
        try:
            float(val)
        except (ValueError, TypeError):
            print(f"🛑 Stopped: Non-numeric event '{val}' detected at row {i}")
            break
            
        # --- INTERVAL LOGIC with 5-min Default ---
        interval = float(df.at[i, 'time_step_min'])
        
        # If the jump is more than 10 mins or negative (clock reset), use 5 mins
        if interval > 10 or interval < 1:
            print(f"⚠️ Row {i}: Interval ({interval} min) is invalid. Using default 5 min.")
            use_interval = 5.0
        else:
            use_interval = interval

        # Subtract the interval (actual or default) for the row ABOVE
        current_time = current_time - timedelta(minutes=use_interval)
    
    # 5. Save the result
    cols = ['corrected_timestamp'] + [c for c in df.columns if c != 'corrected_timestamp']
    df = df[cols]
    
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Saved to: {output_path.name}")

if __name__ == "__main__":
    reconstruct_segment_backward(
        "cleaned_user_72_merged.csv", 
        anchor_timestamp_str="2025-10-02 09:23:00"
    )