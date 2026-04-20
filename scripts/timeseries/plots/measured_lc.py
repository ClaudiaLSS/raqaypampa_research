#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 10:36:41 2026

@author: claudia
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file_path = '/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/TPDIN/tpdin_user_74.csv'

# 1. Load and Prepare Data
df = pd.read_csv(file_path)
df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'])
df = df.set_index('corrected_timestamp').sort_index()

# Calculate Power components (P = V * I)
df['p_usb'] = (df['v_usb'] * df['c_usb']).clip(lower=0)
df['p_led1'] = (df['v_led_1'] * df['c_led_1']).clip(lower=0)
df['p_led2'] = (df['v_led_2'] * df['c_led_2']).clip(lower=0)
df['total_power'] = df['p_usb'] + df['p_led1'] + df['p_led2']

# --- PLOT 1: All Daily Load Curves ---
plt.figure(figsize=(10, 5))
for date, group in df.groupby(df.index.date):
    # Convert time to float hours (0-24)
    times = group.index.hour + group.index.minute / 60.0
    plt.plot(times, group['total_power'], color='blue', alpha=0.1)
plt.title('Daily Load Curves Distribution - User 74')
plt.xlabel('Hour of Day'); plt.ylabel('Power (W)')
plt.savefig('distribution_plot.png')

# --- PLOT 2: Specific Day ---
# Configuración del día y datos
target_day = '2025-04-12'
day_data = df.loc[target_day]

plt.figure(figsize=(14, 8))

# Graficar componentes individuales
plt.plot(day_data.index, day_data['p_usb'], label='USB (Phones/Radios)', linewidth=3, color='tab:blue')
plt.plot(day_data.index, day_data['p_led1'], label='LED 1 (Lighting)', linewidth=3, color='tab:orange')
plt.plot(day_data.index, day_data['p_led2'], label='LED 2 (Lighting)', linewidth=3, color='tab:green')

# Sombreado del consumo total (sin solar)
plt.fill_between(day_data.index, day_data['total_power'], alpha=0.15, color='gray', label='Total Consumption')

# FORMATEO DEL EJE X (HH:MM)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))

# AJUSTES DE TEXTO Y TAMAÑO
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title(f'Loads for {target_day}', fontsize=28, pad=20)
plt.xlabel('Time', fontsize=22, labelpad=15)
plt.ylabel('Power (W)', fontsize=22, labelpad=15)

plt.legend(fontsize=16, loc='upper left')
plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()

plt.savefig('day_plot_no_solar.png')

# --- PLOT 3: Specific Week ---
start_week = '2025-02-10' # <--- CHANGE THIS START DATE
end_week = pd.to_datetime(start_week) + pd.Timedelta(days=7)
week_data = df.loc[start_week:end_week]
plt.figure(figsize=(15, 5))
plt.plot(week_data.index, week_data['total_power'], color='black', alpha=0.3)
plt.plot(week_data.index, week_data['p_usb'], label='USB')
plt.plot(week_data.index, week_data['p_led1'], label='LED 1')
plt.plot(week_data.index, week_data['p_led2'], label='LED 2')
plt.title(f'Weekly Loads Starting {start_week}'); plt.legend()
plt.savefig('week_plot.png')