#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 10:31:31 2026

@author: claudia
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from pathlib import Path
# --- SET YOUR PATHS ---
BASE_DIR = Path("/home/claudia/Documents/raqaypampa_research")
INPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "cleaned_user_96_2_merged.csv"
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "timeseries" / "merged" / "filled_user_96_2.csv"

def fill_jumps_with_new_rows(file_path, output_path, step_min=5):
    # 1. Load data
    df = pd.read_csv(file_path)
    
    # 2. Convert to datetime to detect jumps
    # We use the logger's original date/time as the source of truth
    df['temp_dt'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
    
    # 3. Create a list to store rows (it is faster to build a list than modify a DF in a loop)
    new_rows = []
    
    print(f"🔍 Scanning for jumps larger than {step_min} minutes...")

    for i in range(len(df)):
        # Always add the current existing row
        new_rows.append(df.iloc[i].to_dict())
        
        # Check if there is a jump to the next row
        if i + 1 < len(df):
            start_time = df.at[i, 'temp_dt']
            end_time = df.at[i+1, 'temp_dt']
            
            if pd.notna(start_time) and pd.notna(end_time):
                diff = (end_time - start_time).total_seconds() / 60
                
                # If the jump is significantly larger than our step (e.g., > 11 mins)
                if diff > (step_min + 1):
                    # Calculate how many rows to add
                    # We subtract 1 because the 'end_time' row already exists
                    steps_to_add = int(diff // step_min) - 1
                    
                    if steps_to_add > 0:
                        # Safety limit: don't fill gaps larger than 24 hours (144 rows) 
                        # to prevent infinite loops if the clock reset to 2015
                        steps_to_add = min(steps_to_add, 144) 
                        
                        for s in range(1, steps_to_add + 1):
                            fill_time = start_time + timedelta(minutes=s * step_min)
                            
                            # Create a blank row with only the new time/date
                            blank_row = {col: np.nan for col in df.columns}
                            blank_row['date'] = fill_time.strftime('%Y-%m-%d')
                            blank_row['time'] = fill_time.strftime('%H:%M:%S')
                            blank_row['temp_dt'] = fill_time
                            
                            new_rows.append(blank_row)

    # 4. Convert list back to DataFrame
    df_final = pd.DataFrame(new_rows)
    
    # 5. Cleanup and Save
    df_final = df_final.drop(columns=['temp_dt'])
    df_final.to_csv(output_path, index=False)
    
    print(f"✅ Success! Added {len(df_final) - len(df)} blank rows into the gaps.")
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    fill_jumps_with_new_rows(INPUT_FILE, OUTPUT_FILE)