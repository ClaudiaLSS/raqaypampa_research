#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 11:07:32 2026

@author: claudia
"""
'''
#From last to first / TPDIN
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
        "cleaned_user_15_merged.csv", 
        anchor_timestamp_str="2025-10-01 12:18:00"
    )

'''
#From firts to last/TPDIN

import pandas as pd
from datetime import timedelta
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CLEAN_DIR = BASE_DIR / "data" / "raw" / "timeseries" / "merged"

def reconstruct_segment_forward(file_name, start_row=0, anchor_timestamp_str=None):
    input_path = CLEAN_DIR / file_name
    output_path = CLEAN_DIR / f"forward_segmented_{file_name}"
    
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return

    # 1. Load the data
    df = pd.read_csv(input_path)
    
    # --- Calculate time_step_min if it doesn't exist ---
    if 'time_step_min' not in df.columns:
        print("🔍 'time_step_min' not found. Calculating intervals...")
        temp_dt = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
        df['time_step_min'] = temp_dt.diff().dt.total_seconds() / 60.0
        df['time_step_min'] = df['time_step_min'].fillna(0)
    
    # 2. Determine the starting Anchor
    # If no anchor string is provided, use the value already in the CSV at start_row
    # if anchor_timestamp_str:
    #     current_time = pd.to_datetime(anchor_timestamp_str)
    # else:
    #     current_time = pd.to_datetime(df.at[start_row, 'date'] + ' ' + df.at[start_row, 'time'])
    # --- 1. SET THE STARTING ANCHOR ---
    # We take the value already present in the first row of 'corrected_timestamp'
    first_val = df.at[0, 'corrected_timestamp']
    
    if pd.isna(first_val):
        print("❌ Error: The first row of 'corrected_timestamp' is empty. Cannot start.")
        return
        
    current_time = pd.to_datetime(first_val)
    print(f"🚀 Starting timeline reconstruction from: {current_time}")
    
    # 3. Initialize the corrected column
    df['corrected_timestamp'] = pd.NaT
    
    print(f"🚀 Starting forward reconstruction from row {start_row} at {current_time}")

    # 4. Perform Forward Calculation
    for i in range(start_row, len(df)):
        # Assign the current calculated time
        df.at[i, 'corrected_timestamp'] = current_time
        
        # # --- STOP CONDITION: Check the NEXT row's 'day' column ---
        # We check i + 1 because we want to stop BEFORE processing the 'System Initialized' row
        if i + 1 < len(df):
            next_val = df.at[i + 1, 'day']
            try:
                float(next_val) # Continue if it's a number
            except (ValueError, TypeError):
                print(f"🛑 Stopped: Non-numeric event '{next_val}' detected at row {i+1}")
                break
   # --- UPDATED STOP CONDITION ---
        # if i + 1 < len(df):
        #     next_date = df.at[i + 1, 'date']
        #     next_time = df.at[i + 1, 'time']
        #     next_gap = df.at[i + 1, 'time_step_min']
            
        #     # Stop if data is missing OR if the gap is too large (> 15 min)
        #     if pd.isna(next_date) or pd.isna(next_time) or next_gap > 200:
        #         if pd.isna(next_date) or pd.isna(next_time):
        #             reason = "Missing Date/Time"
        #         else:
        #             reason = f"Large Gap ({next_gap} min)"
                
        #         print(f"🛑 Stopped: {reason} detected at row {i+1}")
        #         break
        
        # --- INTERVAL LOGIC ---
        # We look at the interval of the NEXT row to step forward
        if i + 1 < len(df):
            raw_interval = df.at[i+1, 'time_step_min']
            
            # Apply your logic: if NaN, > 6, or < 4, use 5.0 default
            if pd.isna(raw_interval) or raw_interval > 6 or raw_interval < 4:
                use_interval = 5.0
            else:
                use_interval = float(raw_interval)
                
            current_time = current_time + timedelta(minutes=use_interval)
        

    # 5. Save the result
    cols = ['corrected_timestamp'] + [c for c in df.columns if c != 'corrected_timestamp']
    df = df[cols]
    
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Forward reconstruction saved to: {output_path.name}")

if __name__ == "__main__":
    # If the first row is correct, we don't need to provide a date string
    reconstruct_segment_forward("filled_user_96_2.csv", start_row=0)

'''
import pandas as pd
from datetime import timedelta
from pathlib import Path


##For OLD DL

# --- DEFINE YOUR PATHS HERE ---
# Based on your previous messages, this is the standard structure
BASE_DIR = Path("/home/claudia/Documents/raqaypampa_research")
INPUT_DIR = BASE_DIR / "data" / "raw" / "timeseries" / "merged"
OUTPUT_DIR = BASE_DIR /'data'/'raw'/'timeseries'/'raw_timeseries'

def fix_and_resample_timeline(file_name, anchor_time="2023-04-26 14:24:57"):
    input_path = INPUT_DIR / file_name
    output_path = OUTPUT_DIR / f"resampled_{file_name}"
    
    # 1. Load data
    df = pd.read_csv(input_path)
    
    # 2. Reconstruct a continuous timeline from the START
    # We ignore the 'corrected_timestamp' column and start fresh
    current_time = pd.to_datetime(anchor_time)
    df['corrected_timestamp'] = pd.NaT
    
    print(f"🔄 Rebuilding timeline from {anchor_time}...")

    # Calculate intervals from logger (handling NaNs)
    df['logger_dt'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
    
    # Walk through the file
    for i in range(len(df)):
        df.at[i, 'corrected_timestamp'] = current_time
        
        if i + 1 < len(df):
            # Calculate gap to the next row
            if pd.isna(df.at[i, 'logger_dt']) or pd.isna(df.at[i+1, 'logger_dt']):
                # If either row is empty (NaN), we only step 5 mins 
                # to avoid double-counting the 10-min interval
                interval = 5.0 
            else:
                interval = (df.at[i+1, 'logger_dt'] - df.at[i, 'logger_dt']).total_seconds() / 60.0
            
            # Sane check for jumps or clock resets
            if interval > 15 or interval <= 0:
                interval = 10.0 # Default to your logger frequency
            
            current_time = current_time + timedelta(minutes=interval)

    # 3. OPTIONAL: Resample to create the missing rows for the 6-hour gap
    # This will turn the "Jump" into hundreds of empty rows with correct timestamps
    df = df.set_index('corrected_timestamp')
    # Resample to 10 minutes and fill in the missing timestamps
    df_resampled = df.resample('10min').asfreq()
    
    # 4. Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_resampled.reset_index().drop(columns=['logger_dt']).to_csv(output_path, index=False)
    print(f"✅ Success! Continuous 10-min data saved to: {output_path}")

if __name__ == "__main__":
    fix_and_resample_timeline("raw_merged_user_63_primer.csv")
'''