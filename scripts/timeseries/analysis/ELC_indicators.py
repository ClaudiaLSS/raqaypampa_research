#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:29:55 2026

@author: claudia
"""

import pandas as pd
import numpy as np
from scipy.stats import entropy
import os

class LoadCurveAnalizer:
    def __init__(self, data_path=None, output_path=None, nominal_power=20):
        """
        Initialize the analyzer.
        data_path: Folder where CSVs are stored.
        output_path: Folder where results will be saved.
        """
        self.data_path = data_path
        self.output_path = output_path
        self.nominal_power = nominal_power

    def preprocess(self, input_source):
        """
        Standardizes data. input_source can be a filename (str) or a DataFrame.
        """
        if isinstance(input_source, str):
            # If data_path is set, join it; otherwise assume it's a full path
            path = os.path.join(self.data_path, input_source) if self.data_path else input_source
            df = pd.read_csv(path)
        else:
            df = input_source.copy()
            
        # 1. Standardize Timestamps
        df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'])
        df = df.sort_values('corrected_timestamp').reset_index(drop=True)
        
        # 2. Time Features
        df['hour'] = df['corrected_timestamp'].dt.hour
        df['date'] = df['corrected_timestamp'].dt.date
        df['month'] = df['corrected_timestamp'].dt.month
        df['is_weekend'] = df['corrected_timestamp'].dt.weekday >= 5
        
        # 3. Identify Blackouts
        df['is_blackout'] = df['v_pv'].isna()
        
        # 4. Handle Missing Values & Power
        cols = ['v_pv', 'v_usb', 'v_led_1', 'v_led_2', 'c_usb', 'c_led_1', 'c_led_2']
        df[cols] = df[cols].fillna(0)
        
        # Power Calculation (ensure p_total exists)
        if 'p_total' not in df.columns:
            df['p_usb'] = df['v_usb'] * df['c_usb']
            df['p_led1'] = df['v_led_1'] * df['c_led_1']
            df['p_led2'] = df['v_led_2'] * df['c_led_2']
            df['p_total'] = df['p_usb'] + df['p_led1'] + df['p_led2']
            
        return df

    # --- METRIC BLOCKS ---

    def get_magnitude_metrics(self, df):
        metrics = {}
        total_energy_wh = (df['p_total'].sum() * 5.0) / 60.0
        time_span = df['corrected_timestamp'].max() - df['corrected_timestamp'].min()
        num_days = max(time_span.days + (time_span.seconds / 86400), 1e-6)
        
        metrics['peak_load_W'] = df['p_total'].max()
        metrics['base_load_W'] = df['p_total'].min()
        metrics['monthly_cons_Wh_month'] = (total_energy_wh / num_days) * 30
        metrics['avg_daily_cons_Wh_day'] = total_energy_wh / num_days
        return metrics

    def get_reliability_metrics(self, df):
        metrics = {}
        df['block'] = (df['is_blackout'] != df['is_blackout'].shift()).cumsum()
        bo_blocks = df[df['is_blackout'] == True].groupby('block')
        
        total_events = bo_blocks.ngroups
        metrics['bo_freq_events'] = total_events
        metrics['mod_min'] = (bo_blocks.size() * 5.0).mean() if total_events > 0 else 0
        metrics['ri_percent'] = ((len(df) - df['is_blackout'].sum()) / len(df)) * 100
        
        # Climatic & Behavioral Rates
        climatic = 0
        for _, group in bo_blocks:
            start = group['corrected_timestamp'].min()
            prev = df[(df['corrected_timestamp'] >= start - pd.Timedelta(hours=24)) & (df['corrected_timestamp'] < start)]
            sun = prev[(prev['hour'] >= 10) & (prev['hour'] <= 15)]
            if not sun.empty and sun['v_pv'].mean() < 15.0:
                climatic += 1
        
        metrics['cbr_events'] = climatic
        metrics['bbr_events'] = total_events - climatic # Behavioral is the remainder
        return metrics

    def get_temporal_metrics(self, df):
        metrics = {}
        mu = df['p_total'].mean()
        if mu <= 0: return metrics

        peak_times = df.loc[df.groupby('date')['p_total'].idxmax(), 'corrected_timestamp'].dt.strftime('%H:%M')
        metrics['time_peak_hhmm'] = peak_times.mode().iloc[0] if not peak_times.empty else None
        
        # Seasonal & Weekend
        wd = df[df['is_weekend'] == False].groupby('hour')['p_total'].mean()
        we = df[df['is_weekend'] == True].groupby('hour')['p_total'].mean()
        metrics['wd_score_ratio'] = (we - wd).abs().sum() / mu if not we.empty and not wd.empty else 0
        
        # Coincidence
        indiv_sum = df[['p_usb', 'p_led1', 'p_led2']].max().sum()
        metrics['coincidence_factor_ratio'] = df['p_total'].max() / indiv_sum if indiv_sum > 0 else 0
        return metrics

    def get_variability_metrics(self, df):
        metrics = {}
        data = df['p_total'].values
        
        metrics['iqr_W'] = df['p_total'].quantile(0.75) - df['p_total'].quantile(0.25)
        metrics['r_24h_coeff'] = df['p_total'].autocorr(lag=288)
        
        # Higuchi Fractal Dimension Helper
        def get_fd(x, k_max=10):
            L, x = [], x[~np.isnan(x)]
            if len(x) < k_max*2: return 0
            for k in range(1, k_max + 1):
                Lk = []
                for m in range(k):
                    idx = np.arange(m, len(x), k)
                    if len(idx) < 2: continue
                    L_mk = np.sum(np.abs(np.diff(x[idx]))) * (len(x) - 1) / (((len(x) - m) // k) * k * k)
                    Lk.append(L_mk)
                L.append(np.log(np.mean(Lk)))
            return np.polyfit(np.log(1.0 / np.arange(1, k_max + 1)), L, 1)[0]

        metrics['fractal_dimension_higuchi'] = get_fd(data)
        return metrics

    def get_shape_metrics(self, df):
        metrics = {}
        mu = df['p_total'].mean()
        threshold = 1.5 * mu if mu > 0 else 0
        
        def count_peaks(g):
            above = g > threshold
            return (above & (~above.shift(1).fillna(False))).sum()

        metrics['pnc_avg_peaks_day'] = df.groupby('date')['p_total'].apply(count_peaks).mean()
        metrics['par_ratio'] = df['p_total'].max() / mu if mu > 0 else 0
        return metrics
    
    
    def get_all_metrics(self, df):
        """ Runs all individual metric blocks and returns a combined dictionary. """
        results = {}
        results.update(self.get_magnitude_metrics(df))
        results.update(self.get_reliability_metrics(df))
        results.update(self.get_temporal_metrics(df))
        results.update(self.get_variability_metrics(df))
        results.update(self.get_shape_metrics(df))
        return results

    def get_comparison_metrics(self, df_meas, df_mod):
        """ 
        Block G: Comparison Indicators (Using Corrected Timestamps only)
        """
        # 1. Align data using only the corrected timestamps
        combined = pd.merge(
            df_meas[['corrected_timestamp', 'p_total']], 
            df_mod[['corrected_timestamp', 'p_total']], 
            on='corrected_timestamp', 
            suffixes=('_meas', '_mod')
        ).dropna()
        
        if combined.empty: 
            return {"error": "No timestamp overlap found between datasets."}

        # 2. CREATE A CORRECTED DATE COLUMN from the timestamp
        # This ensures we don't use the "bad" original date
        combined['corr_date'] = combined['corrected_timestamp'].dt.date

        y_true, y_pred = combined['p_total_meas'].values, combined['p_total_mod'].values
        
        c = {}
        # --- Standard Error Metrics ---
        c['rmse_W'] = np.sqrt(np.mean((y_true - y_pred)**2))
        c['mae_W'] = np.mean(np.abs(y_true - y_pred))
        
        mask = y_true > 0.1
        c['mape_pct'] = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100 if any(mask) else 0
        c['nvf_ratio'] = np.std(y_pred) / np.std(y_true) if np.std(y_true) > 0 else 0
        
        # LCSS (Longest Common Subsequence)
        thresh = 0.1 * y_true.mean()
        matches = np.abs(y_true - y_pred) < thresh
        max_s = current_s = 0
        for m in matches:
            current_s = current_s + 1 if m else 0
            max_s = max(max_s, current_s)
        c['lcss_score'] = max_s / len(y_true)

        # --- MPDADA & MPDADMA (Using corr_date) ---
        # We group by the NEW column we just made
        daily_stats = combined.groupby('corr_date').agg(
            peak_meas=('p_total_meas', 'max'),
            peak_mod=('p_total_mod', 'max'),
            avg_meas=('p_total_meas', 'mean')
        )

        # MPDADA calculation
        daily_stats['mpdada'] = (np.abs(daily_stats['peak_meas'] - daily_stats['peak_mod']) / 
                                 daily_stats['avg_meas'].replace(0, np.nan)) * 100
        c['mpdada_pct'] = daily_stats['mpdada'].mean()

        # MPDADMA calculation
        combined['mv_avg_meas'] = combined['p_total_meas'].rolling(window=12, center=True).mean()
        daily_dma = combined.groupby('corr_date')['mv_avg_meas'].mean()
        
        daily_stats['mpdadma'] = (np.abs(daily_stats['peak_meas'] - daily_stats['peak_mod']) / 
                                  daily_dma.replace(0, np.nan)) * 100
        c['mpdadma_pct'] = daily_stats['mpdadma'].mean()
        
        return c
    
    
    
# ==========================================
#           FINAL CONTROL PANEL
# ==========================================
# Select Mode: "single", "folder", or "validation"
MODE = "validation" 

# --- Paths for Single & Folder Mode ---
DATA_DIR = "/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/TPDIN"
USER_FILE = "tpdin_user_11.csv"  # Only used if MODE is "single"

# --- Paths for Validation Mode ---
# Comparing Measured vs. Modeled data
MEASURED_PATH = "/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/TPDIN/tpdin_user_74.csv"
MODELED_PATH  = "/home/claudia/Documents/raqaypampa_research/data/clean/timeseries/TPDIN/tpdin_user_72.csv"

# ==========================================

if __name__ == "__main__":
    analyzer = LoadCurveAnalizer(data_path=DATA_DIR, nominal_power=20)

    # --- OPTION 1: VALIDATION MODE (A vs B) ---
    if MODE == "validation":
        print(f" RUNNING VALIDATION: {os.path.basename(MEASURED_PATH)} vs {os.path.basename(MODELED_PATH)}")
        df_real = analyzer.preprocess(MEASURED_PATH)
        df_mod  = analyzer.preprocess(MODELED_PATH)
        
        # Calculate individual metrics and alignment errors
        m_real = analyzer.get_all_metrics(df_real)
        m_mod  = analyzer.get_all_metrics(df_mod)
        comp   = analyzer.get_comparison_metrics(df_real, df_mod)
        
        # Create side-by-side report
        report = pd.DataFrame({'Measured': m_real, 'Modeled': m_mod})
        
        # --- LOGIC TO AVOID STRING ERROR ---
        # 1. Identify which rows are numeric
        numeric_measured = pd.to_numeric(report['Measured'], errors='coerce')
        numeric_modeled  = pd.to_numeric(report['Modeled'], errors='coerce')
        
        # 2. Only subtract if BOTH values are numbers
        report['Difference'] = numeric_modeled - numeric_measured
        # ----------------------------------------
        
        print("\n[PART 1: METRIC COMPARISON]")
        print(report)
        print("\n[PART 2: ALIGNMENT & ERROR SCORES]")
        print(pd.Series(comp))

    # --- OPTION 2: SINGLE USER MODE ---
    elif MODE == "single":
        print(f"👤 ANALYZING SINGLE USER: {USER_FILE}")
        df = analyzer.preprocess(USER_FILE)
        results = analyzer.get_all_metrics(df)
        print("\n[User Summary Results]")
        print(pd.Series(results))

    # --- OPTION 3: FOLDER (COMMUNITY) MODE ---
    elif MODE == "folder":
        print(f"📂 SCANNING ALL USERS IN: {DATA_DIR}")
        all_rows = []
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        
        for f_name in files:
            try:
                df = analyzer.preprocess(f_name)
                row = {'user_id': f_name.replace('.csv', '')}
                row.update(analyzer.get_all_metrics(df))
                all_rows.append(row)
            except Exception as e:
                print(f"❌ Error in {f_name}: {e}")
        
        df_results = pd.DataFrame(all_rows)
        print(f"\n✅ Finished! Processed {len(df_results)} users.")
        print(df_results.head()) # View the first 5 rows in console

    # Auto-save a copy
    # output_path = os.path.join(SCRIPT_DIR, "Community_Metrics_Report.csv")
    # df_results.to_csv(output_path, index=False)