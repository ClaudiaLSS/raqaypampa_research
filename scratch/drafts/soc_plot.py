#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:53:54 2024

@author: claudia
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

df1 = pd.read_csv('celestina_dia.csv')

df1['time'] = pd.to_datetime(df1['time'])

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(16, 8), gridspec_kw={'height_ratios': [3, 1]})

ax1.plot(df1['time'], df1['Ppv'], label='P_PV', color='gold')
ax1.plot(df1['time'], df1['Pjack'], label='P_LED', color='orange')
ax1.plot(df1['time'], df1['Pusb'], label='P_USB', color='blue',alpha=.8)
ax1.plot(df1['time'], df1['Pcons'], label='P_total', color='black', alpha=.8, linestyle='dashed')

ax1.set_xlabel('Time (h)')
ax1.set_ylabel('Power (W)')
ax1.legend()
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax2.plot(df1['time'], df1['SOC'], label='SOC', color='green', alpha=.8)

ax2.set_xlabel('Time (h)')
ax2.set_ylabel('SOC (%)')
ax2.legend()
ax2.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()