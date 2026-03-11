#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:29:55 2026

@author: claudia
"""

import pandas as pd
import numpy as np
import os

class LoadCurveAnalizer:
    def __init__(self, data_path, output_path):
        """
        Initialize the analyzer with paths for data and results.
        
        Args:
            data_path (str): Path to the folder containing clean TPDIN timeseries.
            output_path (str): Path where the analysis results/scripts are stored.
        """
        self.data_path = data_path
        self.output_path = output_path
        self.gap_threshold_min = 7.0  # Safety buffer for actual missing rows

    def preprocess(self, file_name):
        """
        Block A: Data Cleaning and Power Calculation
        Identifies blackouts where the timestamp exists but data cells are empty.
        """
        file_path = os.path.join(self.data_path, file_name)
        df = pd.read_csv(file_path)
        
        # 1. Standardize Timestamps
        df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'])
        df = df.sort_values('corrected_timestamp').reset_index(drop=True)
        
        # 2. Identify "Empty" records (Blackouts)
        # Per user: "timestamp continues but with no records (empty cells)"
        # We flag rows where sensor data is missing (NaNs). 
        # v_pv is a reliable proxy: if it's NaN, the sensor was not logging.
        df['is_blackout'] = df['v_pv'].isna()
        
        # 3. Handle Missing Values
        # Fill NaNs with 0 to allow power calculations during those periods
        cols_to_fill = ['v_usb', 'v_led_1', 'v_led_2', 'c_usb', 'c_led_1', 'c_led_2', 'c_extra', 'v_pv']
        df[cols_to_fill] = df[cols_to_fill].fillna(0)
        
        # 4. Calculate Power (Watts)
        # v_batt is assumed to be the average of the LED port voltages
        v_batt = df[['v_led_1', 'v_led_2']].mean(axis=1)
        
        df['p_usb'] = df['v_usb'] * df['c_usb']
        df['p_led1'] = df['v_led_1'] * df['c_led_1']
        df['p_led2'] = df['v_led_2'] * df['c_led_2']
        df['p_extra'] = v_batt * df['c_extra'].abs()
        
        # Total Power Demand (W)
        df['p_total'] = df['p_usb'] + df['p_led1'] + df['p_led2'] + df['p_extra']
        
        return df

    def get_magnitude_metrics(self, df):
        """
        Block B: Magnitude Indicators (Magnitude type in ELC_indicators.csv)
        """
        metrics = {}
        
        # 1. Peak Load (Maximum Power Value)
        metrics['peak_load'] = df['p_total'].max()
        
        # 2. Base Load (Minimum Power Value - often 0 during night or blackouts)
        metrics['base_load'] = df['p_total'].min()
        
        # 3. Monthly average load (Arithmetic mean of all intervals)
        metrics['avg_load_month'] = df['p_total'].mean()
        
        # 4. Total Consumption (Wh)
        # Logic: Sum(Power) * (5 minutes / 60 minutes per hour)
        total_energy_wh = (df['p_total'].sum() * 5.0) / 60.0
        metrics['total_cons_wh'] = total_energy_wh
        
        # 5. Average Daily Consumption (Wh/day)
        time_span = df['corrected_timestamp'].max() - df['corrected_timestamp'].min()
        num_days = time_span.days + (time_span.seconds / 86400)
        metrics['avg_daily_cons_wh'] = total_energy_wh / num_days if num_days > 0 else total_energy_wh
        
        return metrics
    
# --- Example of usage ---
if __name__ == "__main__":
    DATA_DIR = "/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/TPDIN"
    SCRIPT_DIR = "/home/claudia/Documents/raqaypampa_research/scripts/timeseries/analysis"
    
    # Initialize the class with your specified name
    analyzer = LoadCurveAnalizer(DATA_DIR, SCRIPT_DIR)
    
    # Run Preprocessing (Block A)
    df = analyzer.preprocess("tpdin_user_11.csv")
    
    # Run Magnitude Analysis (Block B)
    mag_results = analyzer.get_magnitude_metrics(df)