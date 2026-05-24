"""
BLUE Datalogger Extractor
Handles BLUE-type files with single total consumption measurement.
Format: v_led_1 (battery voltage), c_cons (total consumption current)
Calculates: p_total = v_led_1 × c_cons
"""
import pandas as pd
import numpy as np
from base_extractor import BaseExtractor


class BlueExtractor(BaseExtractor):
    """Extractor for BLUE datalogger format (1 appliance: total consumption)."""
    
    def __init__(self):
        super().__init__()
        self.appliance_col_mapping = {
            'CONS': {'voltage': 'v_led_1', 'current': 'c_cons'}
        }
        self.power_threshold = 0.5  # Watts
    
    def preprocess(self, filename):
        """Load CSV and calculate total power."""
        df = pd.read_csv(filename)
        
        # Parse datetime
        if 'date' in df.columns and 'time' in df.columns:
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        elif 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'])
        else:
            raise ValueError(f"Cannot find datetime columns in {filename}")
        
        df = df.sort_values('datetime').reset_index(drop=True)
        
        # Calculate total power
        df['p_total'] = df['v_led_1'] * df['c_cons']
        
        return df
    
    def extract_hardware(self, df):
        """Extract median wattage for total consumption when active."""
        p_total_active = df[df['p_total'] > self.power_threshold]['p_total']
        
        if len(p_total_active) == 0:
            hardware = {'CONS_W': 0.0}
        else:
            hardware = {'CONS_W': float(p_total_active.median())}
        
        return hardware
    
    def extract_hourly_probs(self, df):
        """Extract hourly usage probabilities."""
        df['date'] = df['datetime'].dt.date
        df['hour'] = df['datetime'].dt.hour
        
        # Calculate for each hour
        hourly_probs = {}
        peak_hour_max_prob = 0
        peak_hour = 0
        daily_event_days = 0
        
        for hour in range(24):
            hour_data = df[df['hour'] == hour]
            
            if len(hour_data) == 0:
                prob = 0.0
            else:
                # Probability that CONS is active (> threshold) in this hour
                active_count = len(hour_data[hour_data['p_total'] > self.power_threshold])
                prob = active_count / len(hour_data) if len(hour_data) > 0 else 0.0
            
            hourly_probs[f'hour_{hour:02d}'] = {'CONS_Prob': prob}
            
            if prob > peak_hour_max_prob:
                peak_hour_max_prob = prob
                peak_hour = hour
        
        # Daily probability: days where CONS was active at least once
        daily_usage = df.groupby('date').apply(
            lambda x: len(x[x['p_total'] > self.power_threshold]) > 0
        )
        daily_event_days = daily_usage.sum()
        total_days = len(daily_usage)
        daily_prob = daily_event_days / total_days if total_days > 0 else 0.0
        
        daily_event_probs = {'CONS_Prob': daily_prob}
        peak_hours = {'CONS': {'hour': peak_hour, 'probability': peak_hour_max_prob}}
        
        return {
            'hourly_probs': hourly_probs,
            'peak_hours': peak_hours,
            'daily_event_probs': daily_event_probs
        }
    
    def extract_ramp_params(self, df):
        """Extract RAMP parameters for total consumption."""
        df['date'] = df['datetime'].dt.date
        df['minute_of_day'] = df['datetime'].dt.hour * 60 + df['datetime'].dt.minute
        
        ramp_params = {}
        
        # For each day, find usage windows (continuous periods where power > threshold)
        all_windows = []
        
        for date in df['date'].unique():
            daily_data = df[df['date'] == date].sort_values('minute_of_day')
            active_periods = daily_data[daily_data['p_total'] > self.power_threshold]['minute_of_day'].values
            
            if len(active_periods) == 0:
                continue
            
            # Find continuous windows
            windows = []
            start = active_periods[0]
            prev = active_periods[0]
            
            for minute in active_periods[1:]:
                # If gap > 5 minutes (1 sample at 5-min resolution), start new window
                if minute - prev > 5:
                    windows.append((start, prev))
                    start = minute
                prev = minute
            windows.append((start, prev))
            
            all_windows.extend(windows)
        
        if len(all_windows) == 0:
            # No active periods found
            ramp_params['CONS'] = {
                'num_windows': 0,
                'func_time': 0.0,
                'func_cycle': 0.0,
                'time_fraction_random_variability': 0.0,
                'random_var_w': 0.0,
                'window_1': [0, 0]
            }
        else:
            num_windows = len(all_windows)
            
            # Function time: mean duration of usage windows across all days
            window_durations = [end - start for start, end in all_windows]
            func_time = np.mean(window_durations)
            
            # Function cycle: median continuous usage duration
            func_cycle = np.median(window_durations)
            
            # Time variability: std of window start times (normalized by day length)
            window_starts = [start for start, _ in all_windows]
            time_var = np.std(window_starts) / 1440.0 if len(window_starts) > 1 else 0.0
            
            # Random variability in window: coefficient of variation of durations
            window_var = np.std(window_durations) / func_time if func_time > 0 else 0.0
            
            ramp_params['CONS'] = {
                'num_windows': num_windows,
                'func_time': float(func_time),
                'func_cycle': float(func_cycle),
                'time_fraction_random_variability': float(time_var),
                'random_var_w': float(window_var),
                'window_1': [float(all_windows[0][0]), float(all_windows[0][1])]
            }
            
            # Add up to 10 representative windows
            for i in range(min(10, len(all_windows))):
                ramp_params['CONS'][f'window_{i+1}'] = [
                    float(all_windows[i][0]),
                    float(all_windows[i][1])
                ]
        
        return ramp_params
    
    def extract_power_variation(self, df):
        """Extract power variation statistics for total consumption."""
        p_total = df['p_total']
        p_total_active = p_total[p_total > self.power_threshold]
        
        if len(p_total_active) == 0:
            power_variation = {
                'CONS': {
                    'mean_power_W': 0.0,
                    'std_power_W': 0.0,
                    'coeff_variation': 0.0,
                    'min_power_W': 0.0,
                    'max_power_W': 0.0,
                    'range_power_W': 0.0,
                    'median_power_W': 0.0,
                    'q25_power_W': 0.0,
                    'q75_power_W': 0.0
                }
            }
            thermal_cv = {'CONS': 0.0}
        else:
            mean_p = p_total_active.mean()
            std_p = p_total_active.std()
            cv = std_p / mean_p if mean_p > 0 else 0.0
            
            power_variation = {
                'CONS': {
                    'mean_power_W': float(mean_p),
                    'std_power_W': float(std_p),
                    'coeff_variation': float(cv),
                    'min_power_W': float(p_total_active.min()),
                    'max_power_W': float(p_total_active.max()),
                    'range_power_W': float(p_total_active.max() - p_total_active.min()),
                    'median_power_W': float(p_total_active.median()),
                    'q25_power_W': float(p_total_active.quantile(0.25)),
                    'q75_power_W': float(p_total_active.quantile(0.75))
                }
            }
            thermal_cv = {'CONS': float(cv)}
        
        return {
            'power_variation': power_variation,
            'thermal_p_var': thermal_cv
        }
