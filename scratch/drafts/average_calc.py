#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 16:03:39 2024

@author: claudia
"""

import numpy as np
import pandas as pd



# Load DataFrame from CSV
df1 = pd.read_csv('output_file_1_min.csv')
df1['time'] = pd.to_datetime(df1['time'])

df2 = pd.read_csv('output_file_2_min.csv')
df2['time'] = pd.to_datetime(df2['time'])

df3 = pd.read_csv('output_file_3_min.csv')
df3['time'] = pd.to_datetime(df3['time'])

df4 = pd.read_csv('output_file_4_min.csv')
df4['time'] = pd.to_datetime(df4['time'])

#calculate averages and save them in new columns

average_P1 = df1.groupby(['date', 'time'])['P'].mean().reset_index()
average_P2 = df2.groupby(['date', 'time'])['P'].mean().reset_index()
average_P3 = df3.groupby(['date', 'time'])['P'].mean().reset_index()
average_P4 = df4.groupby(['date', 'time'])['P'].mean().reset_index()

# Pivot the data to have time points as columns
average_P1_pivot = average_P1.pivot(index='date', columns='time', values='P')
average_P2_pivot = average_P2.pivot(index='date', columns='time', values='P')
average_P3_pivot = average_P3.pivot(index='date', columns='time', values='P')
average_P4_pivot = average_P4.pivot(index='date', columns='time', values='P')

# Calculate the average load for each time point across all days
average_daily_P1 = average_P1_pivot.mean(axis=0)
average_daily_P2 = average_P2_pivot.mean(axis=0)
average_daily_P3 = average_P3_pivot.mean(axis=0)
average_daily_P4 = average_P4_pivot.mean(axis=0)


average_profiles = pd.concat([average_daily_P1, average_daily_P2, average_daily_P3, average_daily_P4], axis=1)
headers = ['HH_1', 'HH_2', 'HH_3','HH_4']
# Save the modified DataFrame to a new CSV file
output_csv_path = 'HH_raq.csv'
average_profiles.to_csv(output_csv_path, index=True, header=headers)