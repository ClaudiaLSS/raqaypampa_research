#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 12:03:59 2026

@author: claudia
"""
'''
import os
import re
from pathlib import Path

# Setup paths
SOURCE_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/raw/timeseries/OLD_DL/user_63")
OUTPUT_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/raw/timeseries/merged")

def extract_number(path):
    numbers = re.findall(r'\d+', path.name)
    return int(numbers[0]) if numbers else 0

def merge_numeric_files(user_id):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"raw_merged_user_{user_id}.csv"
    
    files = list(SOURCE_DIR.glob("*.txt"))
    files.sort(key=extract_number)
    
    if not files:
        print(f"❌ No .txt files found.")
        return

    print(f"🔗 Merging and converting {len(files)} files...")

    # We save as utf-8 (standard), but we READ as latin-1 (safe for old loggers)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, file_path in enumerate(files):
            try:
                with open(file_path, 'r', encoding='latin-1') as infile:
                    for line_idx, line in enumerate(infile):
                        # 1. Skip headers for files after the first one
                        # If it's not the first file and the first line has letters, skip it
                        if i > 0 and line_idx == 0 and any(c.isalpha() for c in line):
                            continue
                        
                        # 2. REPLACE SEMICOLONS WITH COMMAS
                        # This "separates" the columns in a standard CSV format
                        clean_line = line.replace(';', ',')
                        
                        # 3. Write the cleaned line
                        outfile.write(clean_line)
                        
                    # Ensure there is a newline between files
                    outfile.write('\n')
                    
            except Exception as e:
                print(f"⚠️ Error in {file_path.name}: {e}")

    print(f"✅ Success! Standardized CSV saved to: {output_file}")

if __name__ == "__main__":
    merge_numeric_files("63")
    
'''

import os
import re
from pathlib import Path

# Setup paths based on your provided directory
SOURCE_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/raw/timeseries/OLD_DL/user_69")
OUTPUT_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/raw/timeseries/merged")

def extract_number(path):
    """Extracts the integer from the filename to ensure 2.txt comes before 10.txt"""
    numbers = re.findall(r'\d+', path.name)
    return int(numbers[0]) if numbers else 0

def merge_numeric_files(user_id):
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"raw_merged_user_{user_id}.csv"
    
    # 1. Get and sort files numerically
    files = list(SOURCE_DIR.glob("*.txt"))
    files.sort(key=extract_number)
    
    if not files:
        print(f"❌ No .txt files found in {SOURCE_DIR}")
        return

    print(f"🔗 Merging {len(files)} files for User {user_id} in numeric order...")

    # 2. Open the master file for writing
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, file_path in enumerate(files):
            with open(file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()
                
                if not lines:
                    continue
                
                # --- HEADER HANDLING ---
                # If these files have headers (e.g., Date, Time...), 
                # keep the header from the first file, but skip it for all others.
                if i == 0:
                    outfile.writelines(lines)
                else:
                    # Skip the first line (header) for file 2, 3, 4...
                    outfile.writelines(lines[1:])
                
                # Ensure each file's data ends with a clean newline
                if not lines[-1].endswith('\n'):
                    outfile.write('\n')

    print(f"✅ Success! Merged file saved to: {output_file}")

if __name__ == "__main__":
    merge_numeric_files("69")