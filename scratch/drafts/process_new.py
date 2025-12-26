#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:39:42 2024

@author: claudia

Plot
"""

import pandas as pd


# Load DataFrame from CSV
input_csv_path = 'celestina_may.csv'
df = pd.read_csv(input_csv_path)

# Perform operations on columns and create new columns
df['time'] = pd.date_range('2023-05-01 00:00:00', '2023-05-31 23:10:00', freq='10T')  # '10T' stands for 10 minutes
df['Ppv'] = df['V3']* df['I4']
df['Pusb'] = df['V2']* df['I2']
df['Pjack'] = df['V1']* df['I1']
df['Pdl'] = df['I3'] * df['V1']
df['Vbat'] = df['V1']
df['Vusb'] = df['V2']
df['Vpv'] = df['V3']
df['Ijack'] = df['I1']
df['Iusb'] = df['I2']
df['Idl'] = df['I3']
df['Ipv'] = df['I4']
df['VOC'] = df['O1']
df['ISC'] = df['O2']
df['Pcons'] = (df['V2']* df['I2'])+(df['V1']* df['I1'])+(df['I3'] * df['V1'])


# Save the modified DataFrame to a new CSV file
output_csv_path = 'celestina_mod.csv'
df.to_csv(output_csv_path, index=False)

# Display the path to the saved CSV file
print(f'Modified DataFrame saved to: {output_csv_path}')

