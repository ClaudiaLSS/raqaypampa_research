#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:27:06 2024

@author: claudia
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

#plotting average daily profiles

df1 = pd.read_csv('tiers.csv')
df1['time'] = pd.to_datetime(df1['time'])

df2 = pd.read_csv('HH_raq.csv')
df2['time'] = pd.to_datetime(df2['time'])

df3 = pd.read_csv('raq_compiled.csv')
df3['time'] = pd.to_datetime(df3['time'])

#df_month = pd.read_csv('celestina_mod.py')

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df1['time'], df1['1'], label='Tier_1', color = 'gold', zorder=1)
ax.plot(df1['time'], df1['2'], label='Tier_2', color = 'green', zorder=2)
#ax.plot(df1['time'], df1['tier_3'], label='Tier_3', color = 'blue', zorder=1)
#ax.plot(df1['time'], df1['tier_4'], label='Tier_4', color = 'orange', zorder=1)

ax.plot(df2['time'], df2['HH_1'], label='HH_1', color = 'tomato', zorder=1)
ax.plot(df2['time'], df2['HH_2'], label='HH_2', color = 'tomato', zorder=2)
ax.plot(df2['time'], df2['HH_3'], label='HH_3', color = 'tomato', zorder=1)
ax.plot(df2['time'], df2['HH_4'], label='HH_4', color = 'tomato', zorder=1)


ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))  # Adjust interval as needed
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# Customize the plot
plt.title('Daily load profile')
plt.xlabel('Time (h)')
plt.ylabel('P (W)')
plt.legend()


plt.show()

