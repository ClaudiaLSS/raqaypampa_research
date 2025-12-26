#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:01:00 2024

@author: claudia
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# def SOC_estimation():
#     if Vbat => 13.6 :
#         SOC = 100


# df = pd.read_csv('celestina_mod.csv')

# df['time'] = pd.to_datetime(df['time'])

# df['Vbat_round'] = df['Vbat'].round(1)

# df['SOC'] =

# output_csv_path = 'soc_celestina.csv'
# df.to_csv(output_csv_path, index=False)



# Create a DataFrame with your voltage-SOC mapping
soc_mapping = {
    'VoltageRange': [
        (float('-inf'), 13.6),
        (13.4, 13.5),
        (13.3, 13.3),
        (13.2, 13.2),
        (13.1, 13.1),
        (13.0, 13.0),
        (12.9, 12.9),
        (12.8, 12.8),
        (12.5, 12.7),
        (12.0, 12.4),
        (10.0, 11.9)
    ],
    'SOC': [100, 99, 90, 70, 40, 30, 20, 17, 14, 9, 0]
}

soc_df = pd.DataFrame(soc_mapping)

# Function to get SOC from a voltage value
def get_soc(voltage):
    soc_entry = soc_df[soc_df['VoltageRange'].apply(lambda x: x[0] <= voltage <= x[1])]['SOC'].values
    return soc_entry[0] if soc_entry else None

# Test the function
voltage_value = 13.2
resulting_soc = get_soc(voltage_value)

if resulting_soc is not None:
    print(f"For a voltage of {voltage_value}V, the SOC is {resulting_soc}%.")
else:
    print(f"No SOC found for the given voltage.")