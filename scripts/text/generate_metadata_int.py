#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 10:25:03 2026

@author: claudia
"""

import pandas as pd
from pathlib import Path

# --- SET YOUR PATHS ---
RAW_INT_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/clean/interviews/all")
OUTPUT_CSV = Path("/home/claudia/Documents/raqaypampa_research/data/clean/interviews/all/interview_attributes.csv")

def extract_metadata_from_text():
    metadata_list = []
    
    # Ensure output directory exists
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Scanning transcripts in {RAW_INT_DIR}...")

    for file_path in RAW_INT_DIR.glob("*.txt"):
        try:
            # We open with utf-8 to handle accents in names/communities
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().splitlines()
                
            # Initialize a dictionary for this file
            file_data = {
                "file_name": file_path.name,
                "case_id": file_path.stem,
                "user_id": "",
                "participant_type": "Unknown",
                "gender": "",
                "community": "",
                "date": ""
            }

            # Scan the first 15 lines for the header info
            for line in content[:15]:
                line = line.lower()
                if "user_id:" in line:
                    file_data["user_id"] = line.split(":")[1].strip()
                elif "category:" in line:
                    # Normalizing 'user' to 'User' and everything else to 'Authority'
                    cat = line.split(":")[1].strip()
                    file_data["participant_type"] = "User" if "user" in cat else "Authority"
                elif "gender:" in line:
                    file_data["gender"] = line.split(":")[1].strip().capitalize()
                elif "community:" in line:
                    file_data["community"] = line.split(":")[1].strip().capitalize()
                elif "date:" in line:
                    file_data["date"] = line.split(":")[1].strip()

            metadata_list.append(file_data)
            print(f" ✅ Processed: {file_path.name} ({file_data['participant_type']})")

        except Exception as e:
            print(f" ❌ Error reading {file_path.name}: {e}")

    # Create DataFrame and save
    if metadata_list:
        df = pd.DataFrame(metadata_list)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n🚀 Success! Created metadata for {len(df)} interviews.")
        print(f"📍 Location: {OUTPUT_CSV}")
    else:
        print(" ⚠️ No files found or processed.")

if __name__ == "__main__":
    extract_metadata_from_text()