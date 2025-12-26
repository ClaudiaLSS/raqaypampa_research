#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 15:27:16 2024

@author: claudia
"""


import pandas as pd

input_csv_path = 'output_file_4_raq.csv'
df = pd.read_csv(input_csv_path)


df['time'] = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:59:00', freq='1T')  # '1T' stands for 1 minutes



output_csv_path = 'output_file_4_min.csv'
df.to_csv(output_csv_path, index=False)