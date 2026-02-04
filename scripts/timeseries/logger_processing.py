#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 11:37:54 2025

@author: claudia
"""

import os
import pandas as pd
import re

def combine_logs(input_folder, output_file):
    all_dataframes = []

    # Collect and sort files numerically by log number
    files = sorted(
        [f for f in os.listdir(input_folder) if f.lower().endswith(".csv")],
        key=lambda x: int(re.search(r"log\((\d+)\)", x).group(1)) if re.search(r"log\((\d+)\)", x) else 0
    )

    for file in files:
        file_path = os.path.join(input_folder, file)
        print(f"Reading {file_path}")
        # No headers → header=None
        df = pd.read_csv(file_path, header=None)
        all_dataframes.append(df)

    # Concatenate vertically (row-wise)
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # Save to output
    combined_df.to_csv(output_file, index=False, header=False)
    print(f"\n✅ Combined logs saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    combine_logs(
        "../data/timeseries/test",        # input folder
        "../results/combined_timeseries.csv"  # output file
    )
