#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 12:52:15 2024

@author: claudia
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

df1 = pd.read_csv('average_profiles_celestina.csv')
df2 = pd.read_csv('average_profiles_guillermo.csv')
df3 = pd.read_csv('average_profiles_carlos.csv')
df4 = pd.read_csv('RAMP_avg7.csv')



df1['time'] = pd.to_datetime(df1['time'])
df2['time'] = pd.to_datetime(df2['time'])
df3['time'] = pd.to_datetime(df3['time'])
df4['time'] = pd.to_datetime(df4['time'])


fig, ax = plt.subplots(figsize=(10, 6))

# Plotting columns from df1
#ax.plot(df1['time'], df1['CONSavg'], label='User_1', color='darkorange')

# Plotting columns from df2
#ax.plot(df2['time'], df2['CONSavg'], label='User_2', color='darkorange')

# Plotting columns from df3
ax.plot(df3['time'], df3['CONSavg'], label='Measured_load_curve', color='orange')

#RAMP courves
ax.plot(df4['time'], df4['LCavg'], label='RAMP_load_curve')

#ax.plot(df4['time'], df4['MCavg'], label='df3_column1')

#ax.plot(df4['time'], df4['HCavg'], label='df3_column1')


# Customize the plot
plt.title('Average daily load curves')
plt.xlabel('Time (h)')
plt.ylabel('P (W)')
plt.legend()

ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))  # Adjust interval as needed
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.show()