#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 21:34:00 2026

@author: claudia
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# --- SET YOUR PATHS ---
BASE_CLEAN_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/clean/timeseries")
OUTPUT_METADATA = Path("/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/user_metadata_summary.csv")

def generate_metadata():
    metadata_list = []
    
    # Folders to scan
    subfolders = ["OLD_DL", "TPDIN"]
    
    for folder_name in subfolders:
        folder_path = BASE_CLEAN_DIR / folder_name
        
        if not folder_path.exists():
            print(f"⚠️ Folder not found: {folder_path}")
            continue
            
        print(f"📂 Scanning folder: {folder_name}...")
        
        for file in folder_path.glob("*.csv"):
            try:
                # Load only necessary columns to speed up processing
                df = pd.read_csv(file)
                
                # 1. Identify Time Columns
                # We check for corrected_timestamp first, then datetime, then date+time
                if 'corrected_timestamp' in df.columns:
                    time_col = pd.to_datetime(df['corrected_timestamp'])
                elif 'datetime' in df.columns:
                    time_col = pd.to_datetime(df['datetime'])
                else:
                    time_col = pd.to_datetime(df['date'] + ' ' + df['time'])

                # 2. Calculate Parameters
                start_ts = time_col.min()
                end_ts = time_col.max()
                duration = end_ts - start_ts
                
                # Calculate the most common time step (mode) in minutes
                time_diffs = time_col.diff().dt.total_seconds() / 60
                mode_step = time_diffs.mode()
                time_step = mode_step[0] if not mode_step.empty else 0
                
                # Quality Check: Count NaNs in sensor data
                # (Ignoring the time columns we just created)
                sensor_data = df.drop(columns=[col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()])
                nan_percent = (sensor_data.isna().sum().sum() / sensor_data.size) * 100

                # 3. Store Metadata
                metadata_list.append({
                    "file_name": file.name,
                    "user_id": file.stem.split('_')[-1], # Assumes format 'user_XX'
                    "dl_type": folder_name,
                    "start_timestamp": start_ts,
                    "end_timestamp": end_ts,
                    "total_days": round(duration.total_seconds() / 86400, 2),
                    "expected_step_min": round(time_step, 2),
                    "total_rows": len(df),
                    "missing_data_pct": round(nan_percent, 2),
                    "columns_found": ", ".join(df.columns.tolist())
                })
                
            except Exception as e:
                print(f"❌ Error processing {file.name}: {e}")

    # 4. Save Metadata File
    if metadata_list:
        summary_df = pd.DataFrame(metadata_list)
        summary_df.to_csv(OUTPUT_METADATA, index=False)
        print(f"\n✅ Success! Metadata summary saved to: {OUTPUT_METADATA}")
    else:
        print("❌ No data processed.")

if __name__ == "__main__":
    generate_metadata()