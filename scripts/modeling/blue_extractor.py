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
        self.INTERVAL_MINUTES = 2
        self.BLACKOUT_THRESHOLD = 4  # Gap > 2× sampling interval (2-min)
        self.MAX_POWER_W = 20  # LEDs 5W + phone charger 5-10W max = 15W realistic
    
    def preprocess(self, filename):
        """Load CSV and calculate total power."""
        df = pd.read_csv(filename)
        
        # Parse datetime - standardized like TPDIN and OLD
        if 'corrected_timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
        elif 'date' in df.columns and 'time' in df.columns:
            df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        elif 'datetime' in df.columns:
            df['timestamp'] = pd.to_datetime(df['datetime'])
        else:
            raise ValueError(f"Cannot find datetime columns in {filename}")
        
        df = df.dropna(subset=['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        df['date_only'] = df['timestamp'].dt.date
        
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
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        
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
        """Extract RAMP parameters for total consumption (whole day)."""
        df['date'] = df['timestamp'].dt.date
        df['minute_of_day'] = df['timestamp'].dt.hour * 60 + df['timestamp'].dt.minute
        
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
    
    def extract_ramp_params_by_period(self, df):
        """Extract RAMP parameters for total consumption broken down by time period."""
        # Define time periods
        periods = {
            'morning': (5, 8),      # 5:00-7:59
            'daytime': (8, 17),     # 8:00-16:59
            'evening': (17, 24),    # 17:00-23:59
            'night': (0, 5)         # 0:00-4:59
        }
        
        ramp_params_by_period = {}
        ramp_params_by_period['CONS'] = {}
        
        for period_name, (start_hour, end_hour) in periods.items():
            # Filter data for this period
            if start_hour < end_hour:
                # Normal case (e.g., morning 5-8)
                period_data = df[(df['timestamp'].dt.hour >= start_hour) & 
                                (df['timestamp'].dt.hour < end_hour)]
            else:
                # Wrap-around case (e.g., night 0-5)
                period_data = df[(df['timestamp'].dt.hour >= start_hour) | 
                                (df['timestamp'].dt.hour < end_hour)]
            
            if len(period_data) > 0:
                ramp_params_by_period['CONS'][period_name] = self._calculate_ramp_params_for_period(
                    period_data, period_name
                )
            else:
                # No data for this period
                ramp_params_by_period['CONS'][period_name] = {
                    'period': period_name,
                    'num_windows': 0,
                    'func_time': 0.0,
                    'func_cycle': 0.0,
                    'time_fraction_random_variability': 0.0,
                    'random_var_w': 0.0,
                    'occasional_use_probability': 0.0,
                    'num_days_with_data': 0
                }
        
        return ramp_params_by_period

    def _calculate_ramp_params_for_period(self, df_period, period_name):
        """Helper: Calculate RAMP parameters for total consumption within a specific time period."""
        df_period = df_period.copy()
        df_period['date'] = df_period['timestamp'].dt.date
        df_period['minute_of_day'] = df_period['timestamp'].dt.hour * 60 + df_period['timestamp'].dt.minute
        
        # Count days with data in this period
        num_days_with_data = df_period['date'].nunique()
        
        # For each day, find usage windows
        all_windows = []
        days_with_activity = 0
        
        for date in df_period['date'].unique():
            daily_data = df_period[df_period['date'] == date].sort_values('minute_of_day')
            active_periods = daily_data[daily_data['p_total'] > self.power_threshold]['minute_of_day'].values
            
            if len(active_periods) == 0:
                continue
            
            days_with_activity += 1
            
            # Find continuous windows
            windows = []
            start = active_periods[0]
            prev = active_periods[0]
            
            for minute in active_periods[1:]:
                # If gap > 5 minutes, start new window
                if minute - prev > 5:
                    windows.append((start, prev))
                    start = minute
                prev = minute
            windows.append((start, prev))
            
            all_windows.extend(windows)
        
        # Occasional use probability: fraction of days in this period where device was active
        occasional_use_prob = round(days_with_activity / num_days_with_data, 2) if num_days_with_data > 0 else 0.0
        
        if len(all_windows) == 0:
            ramp_result = {
                'period': period_name,
                'num_windows': 0,
                'func_time': 0.0,
                'func_cycle': 0.0,
                'time_fraction_random_variability': 0.0,
                'random_var_w': 0.0,
                'occasional_use_probability': occasional_use_prob,
                'num_days_with_data': num_days_with_data,
                'days_with_activity': days_with_activity
            }
        else:
            num_windows = len(all_windows)
            
            # Function time: mean duration of usage windows within this period
            window_durations = [end - start for start, end in all_windows]
            func_time = round(np.mean(window_durations), 1)
            
            # Function cycle: median continuous usage duration
            func_cycle = round(np.median(window_durations), 1)
            
            # Time variability: std of window start times (normalized by period length in minutes)
            window_starts = [start for start, _ in all_windows]
            period_length_minutes = self._get_period_length_minutes(period_name)
            time_var = round(np.std(window_starts) / period_length_minutes, 2) if len(window_starts) > 1 else 0.0
            
            # Random variability in window: coefficient of variation of durations
            window_var = round(np.std(window_durations) / func_time, 2) if func_time > 0 else 0.0
            
            ramp_result = {
                'period': period_name,
                'num_windows': num_windows,
                'func_time': func_time,
                'func_cycle': func_cycle,
                'time_fraction_random_variability': time_var,
                'random_var_w': window_var,
                'occasional_use_probability': occasional_use_prob,
                'num_days_with_data': num_days_with_data,
                'days_with_activity': days_with_activity
            }
            
            # Add up to 10 representative windows
            for i in range(min(10, len(all_windows))):
                ramp_result[f'window_{i+1}'] = [
                    float(all_windows[i][0]),
                    float(all_windows[i][1])
                ]
        
        return ramp_result
    
    def _get_period_length_minutes(self, period_name):
        """Helper: Get the length of a period in minutes."""
        periods = {
            'morning': 3 * 60,      # 5-8: 3 hours
            'daytime': 9 * 60,      # 8-17: 9 hours
            'evening': 7 * 60,      # 17-24: 7 hours
            'night': 5 * 60         # 0-5: 5 hours
        }
        return periods.get(period_name, 1440)
    
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
