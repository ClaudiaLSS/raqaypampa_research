#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 12:55:42 2024

@author: claudia

Processing datalogger data (Spanish DL)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


# Load DataFrame from CSV
input_csv_path = 'celestina_inturias/20000106.csv'
df = pd.read_csv(input_csv_path)

# Perform operations on columns and create new columns
df['time'] = pd.to_datetime(df['time'])
df['Ppv'] = (df['V3']/1000) * (df['I4']/1000)
df['Pusb'] = (df['V2']/1000)* (df['I2']/1000)
df['Pjack'] = (df['V1']/1000) * (df['I1']/1000)
df['Pdl'] = (df['I3']/1000) * (df['V1']/1000)
df['Vbat'] = df['V1']/1000
df['Vusb'] = df['V2']/1000
df['Vpv'] = df['V3']/1000
df['Ijack'] = df['I1']/1000
df['Iusb'] = df['I2']/1000
df['Idl'] = df['I3']/1000
df['Ipv'] = df['I4']/1000
df['VOC'] = df['O1']/1000
df['ISC'] = df['O2']/1000


# Save the modified DataFrame to a new CSV file
output_csv_path = 'test_file.csv'
df.to_csv(output_csv_path, index=False)

# Display the path to the saved CSV file
print(f'Modified DataFrame saved to: {output_csv_path}')

#Plots

# Load DataFrame from CSV
df = pd.read_csv(output_csv_path)
df['time'] = pd.to_datetime(df['time'])

#plotting

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['time'], df['Ppv'], label='Ppv')
ax.plot(df['time'], df['Pusb'], label='Pusb')
ax.plot(df['time'], df['Pjack'], label='Pjack')
ax.plot(df['time'], df['Pdl'], label='Pdl')



# Customize the plot
plt.title('Power generation and consumption')
plt.xlabel('Time (h)')
plt.ylabel('P (W)')
plt.legend()

ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))  # Adjust interval as needed
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()