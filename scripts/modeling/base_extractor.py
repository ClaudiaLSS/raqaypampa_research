"""
Base extractor class with common metrics for all datalogger types.
Handles: structural profiling, reliability metrics, temporal analysis.
"""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """Abstract base class for datalogger extractors."""
    
    def __init__(self):
        """Initialize with common parameters."""
        self.INTERVAL_MINUTES = 5  # Standard interval
        self.BLACKOUT_THRESHOLD = 7  # 7 minutes = 1+ missed readings
        self.POWER_THRESHOLD = 0.5  # 0.5W minimum to consider "on"
        
    @abstractmethod
    def preprocess(self, filename):
        """Preprocess and standardize dataframe. Must return df with p_total, v_pv."""
        pass
    
    @abstractmethod
    def extract_hardware(self, df):
        """Extract appliance wattages. Returns dict."""
        pass
    
    @abstractmethod
    def extract_hourly_probs(self, df):
        """Extract hourly usage probabilities. Returns dict."""
        pass
    
    @abstractmethod
    def extract_ramp_params(self, df):
        """Extract RAMP parameters. Returns dict."""
        pass
    
    @abstractmethod
    def extract_power_variation(self, df):
        """Extract power variation metrics. Returns dict."""
        pass
    
    # --- COMMON METRICS (inherited by all extractors) ---
    
    def extract_structural_metrics(self, df):
        """Extract structural profiling & resilience metrics (TIER 2)."""
        total_power = df['p_total']
        
        # Modal Peak Hour: hour with highest median power
        hourly_medians = df.groupby(df['timestamp'].dt.hour)['p_total'].median()
        modal_peak_hour = int(hourly_medians.idxmax()) if len(hourly_medians) > 0 else 0
        
        # Base Load: 10th percentile of active power
        active_periods = total_power[total_power > self.POWER_THRESHOLD]
        base_load_W = round(active_periods.quantile(0.1), 2) if len(active_periods) > 0 else 0.0
        
        # MRSD (Mean Relative Standard Deviation) - Chaos Index
        daily_cv_list = []
        for date in df['date_only'].unique():
            day_power = df[df['date_only'] == date]['p_total']
            day_mean = day_power.mean()
            day_std = day_power.std()
            if day_mean > 0:
                daily_cv_list.append(day_std / day_mean)
        
        mrsd_chaos_index = round(np.mean(daily_cv_list), 3) if daily_cv_list else 0.0
        
        # Relative Mean Power by time-of-day
        time_periods = {
            'morning': df[(df['timestamp'].dt.hour >= 6) & (df['timestamp'].dt.hour < 12)]['p_total'].mean(),
            'daytime': df[(df['timestamp'].dt.hour >= 12) & (df['timestamp'].dt.hour < 18)]['p_total'].mean(),
            'evening': df[(df['timestamp'].dt.hour >= 18) & (df['timestamp'].dt.hour < 24)]['p_total'].mean(),
            'night': df[(df['timestamp'].dt.hour >= 0) & (df['timestamp'].dt.hour < 6)]['p_total'].mean()
        }
        
        overall_mean_power = df['p_total'].mean()
        relative_mean_power = {}
        for period, mean_val in time_periods.items():
            if overall_mean_power > 0:
                relative_mean_power[period] = round(mean_val / overall_mean_power, 3)
            else:
                relative_mean_power[period] = 0.0
        
        return {
            'modal_peak_hour': modal_peak_hour,
            'base_load_W': base_load_W,
            'mrsd_chaos_index': mrsd_chaos_index,
            'relative_mean_power': relative_mean_power,
            'overall_mean_power_W': round(overall_mean_power, 2)
        }
    
    def extract_reliability_metrics(self, df):
        """Extract blackout and reliability metrics."""
        df_copy = df.copy()
        df_copy['time_diff_minutes'] = df_copy['timestamp'].diff().dt.total_seconds() / 60
        df_copy['is_blackout'] = df_copy['time_diff_minutes'] > self.BLACKOUT_THRESHOLD
        
        # Group consecutive blackouts
        df_copy['blackout_block'] = (df_copy['is_blackout'] != df_copy['is_blackout'].shift()).cumsum()
        bo_blocks = df_copy[df_copy['is_blackout'] == True].groupby('blackout_block')
        
        total_bo_events = bo_blocks.ngroups
        
        # Mean Outage Duration
        mean_outage_duration = 0.0
        if total_bo_events > 0:
            outage_durations = [group['time_diff_minutes'].iloc[0] for _, group in bo_blocks]
            mean_outage_duration = round(np.mean(outage_durations), 1)
        
        # Reliability Index
        total_time_minutes = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60
        if total_time_minutes > 0:
            ri_percent = ((total_time_minutes - (bo_blocks.size().sum() * self.INTERVAL_MINUTES if total_bo_events > 0 else 0)) / total_time_minutes) * 100
        else:
            ri_percent = 0.0
        
        # Climatic vs Behavioral Blackout Rate
        climatic_events = 0
        df_copy['hour'] = df_copy['timestamp'].dt.hour
        
        for _, group in bo_blocks:
            blackout_start = group['timestamp'].min()
            lookback_start = blackout_start - pd.Timedelta(hours=24)
            prev_data = df[(df['timestamp'] >= lookback_start) & (df['timestamp'] < blackout_start)]
            
            if len(prev_data) > 0 and 'v_pv' in prev_data.columns:
                sun_hours = prev_data[(prev_data['timestamp'].dt.hour >= 10) & (prev_data['timestamp'].dt.hour <= 15)]
                if len(sun_hours) > 0 and sun_hours['v_pv'].mean() < 15.0:
                    climatic_events += 1
        
        behavioral_events = total_bo_events - climatic_events
        
        # Rates per 100 days
        num_days = max((df['timestamp'].max() - df['timestamp'].min()).days, 1)
        cbr = round((climatic_events / num_days) * 100, 2) if num_days > 0 else 0.0
        bbr = round((behavioral_events / num_days) * 100, 2) if num_days > 0 else 0.0
        
        return {
            'bo_freq_events': total_bo_events,
            'mean_outage_duration_min': mean_outage_duration,
            'ri_percent': round(ri_percent, 2),
            'climatic_blackout_events': climatic_events,
            'behavioral_blackout_events': behavioral_events,
            'cbr_events_per_100days': cbr,
            'bbr_events_per_100days': bbr
        }
