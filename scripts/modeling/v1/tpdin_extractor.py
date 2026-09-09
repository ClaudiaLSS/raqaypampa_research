"""
Extractor for TPDIN (newest) dataloggers.
Measures: v_led_1, v_led_2, v_usb, c_led_1, c_led_2, c_usb (3 separate appliances)
"""
import pandas as pd
import numpy as np
from base_extractor import BaseExtractor


class TPDINExtractor(BaseExtractor):
    """Handler for TPDIN (newest) datalogger format."""
    
    def __init__(self):
        super().__init__()
        self.appliances = ['LED_1', 'LED_2', 'USB']
        self.power_cols = ['p_led_1', 'p_led_2', 'p_usb']
        self.voltage_cols = ['v_led_1', 'v_led_2', 'v_usb']
        self.current_cols = ['c_led_1', 'c_led_2', 'c_usb']
        self.INTERVAL_MINUTES = 5
        self.BLACKOUT_THRESHOLD = 10  # Gap > 2× sampling interval (5-min)
        self.MAX_POWER_W = 100  # 3 appliances: 3×LED (20W each) + USB (20W) = ~80W max realistic
    
    def preprocess(self, filename):
        """Load and standardize TPDIN dataframe."""
        df = pd.read_csv(filename)
        
        # Standardize timestamp
        df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df['date_only'] = df['timestamp'].dt.date
        
        # Calculate power for each appliance
        df['p_led_1'] = (df['v_led_1'] * df['c_led_1']).clip(lower=0)
        df['p_led_2'] = (df['v_led_2'] * df['c_led_2']).clip(lower=0)
        df['p_usb'] = (df['v_usb'] * df['c_usb']).clip(lower=0)
        
        # Total system power
        df['p_total'] = df['p_led_1'] + df['p_led_2'] + df['p_usb']
        
        # Fill missing PV voltage with 0 (indicates blackout/no sun)
        if 'v_pv' in df.columns:
            df['v_pv'] = df['v_pv'].fillna(0)
        
        return df
    
    def extract_hardware(self, df):
        """Extract median wattage for each appliance when ON."""
        hardware = {}
        for app, col in zip(self.appliances, self.power_cols):
            active = df[df[col] > self.POWER_THRESHOLD][col]
            hardware[f'{app}_W'] = round(active.median(), 2) if len(active) > 0 else 0.0
        return hardware
    
    def extract_hourly_probs(self, df):
        """Extract hourly usage probabilities for each appliance."""
        hourly_probs = {}
        
        for hour in range(24):
            hour_data = df[df['timestamp'].dt.hour == hour]
            if len(hour_data) > 0:
                daily = hour_data.groupby('date_only')[self.power_cols].max()
                hourly_probs[f'hour_{hour:02d}'] = {
                    'LED_1_Prob': round((daily['p_led_1'] > self.POWER_THRESHOLD).mean(), 2),
                    'LED_2_Prob': round((daily['p_led_2'] > self.POWER_THRESHOLD).mean(), 2),
                    'USB_Prob': round((daily['p_usb'] > self.POWER_THRESHOLD).mean(), 2)
                }
            else:
                hourly_probs[f'hour_{hour:02d}'] = {
                    'LED_1_Prob': 0.0,
                    'LED_2_Prob': 0.0,
                    'USB_Prob': 0.0
                }
        
        # Find peak hours for each appliance
        peak_hours = {}
        for app in self.appliances:
            max_prob = 0.0
            peak_hour = 0
            for hour in range(24):
                prob = hourly_probs[f'hour_{hour:02d}'][f'{app}_Prob']
                if prob > max_prob:
                    max_prob = prob
                    peak_hour = hour
            peak_hours[app] = {'hour': peak_hour, 'probability': max_prob}
        
        # Daily event probabilities
        daily_all = df.groupby('date_only')[self.power_cols].max()
        daily_event_probs = {
            'LED_1_Prob': round((daily_all['p_led_1'] > self.POWER_THRESHOLD).mean(), 2),
            'LED_2_Prob': round((daily_all['p_led_2'] > self.POWER_THRESHOLD).mean(), 2),
            'USB_Prob': round((daily_all['p_usb'] > self.POWER_THRESHOLD).mean(), 2)
        }
        
        return {
            'hourly_probs': hourly_probs,
            'peak_hours': peak_hours,
            'daily_event_probs': daily_event_probs
        }
    
    def extract_ramp_params(self, df):
        """Extract RAMP parameters for each appliance (whole day)."""
        ramp_params = {}
        
        for app, col in zip(self.appliances, self.power_cols):
            ramp_params[app] = self._calculate_ramp_params(df, col)
        
        return ramp_params
    
    def extract_ramp_params_by_period(self, df, virtual_appliances=None):
        """Extract RAMP parameters for each appliance broken down by time period.
        
        Args:
            df: DataFrame with timeseries data
            virtual_appliances: Dict of {appliance_name: (start_minute, end_minute)} from markdown.
                               If None, uses default hardcoded periods.
        """
        # Use virtual appliances if provided, otherwise fall back to hardcoded periods
        if virtual_appliances is None:
            # Default hardcoded periods for backward compatibility
            periods = {
                'morning': (5, 8),      # 5:00-7:59
                'daytime': (8, 17),     # 8:00-16:59
                'evening': (17, 24),    # 17:00-23:59
                'night': (0, 5)         # 0:00-4:59
            }
            use_hourly = True
        else:
            # Convert virtual appliances to minute-based periods
            periods = virtual_appliances
            use_hourly = False
        
        ramp_params_by_period = {}
        
        for app, col in zip(self.appliances, self.power_cols):
            ramp_params_by_period[app] = {}
            
            for period_name, (start_val, end_val) in periods.items():
                # Filter data for this period
                if use_hourly:
                    # Hour-based filtering (old behavior)
                    start_hour, end_hour = start_val, end_val
                    if start_hour < end_hour:
                        period_data = df[(df['timestamp'].dt.hour >= start_hour) & 
                                        (df['timestamp'].dt.hour < end_hour)]
                    else:
                        # Wrap-around case (e.g., night 0-5)
                        period_data = df[(df['timestamp'].dt.hour >= start_hour) | 
                                        (df['timestamp'].dt.hour < end_hour)]
                else:
                    # Minute-based filtering (new behavior)
                    start_min, end_min = start_val, end_val
                    df['minute_of_day'] = df['timestamp'].dt.hour * 60 + df['timestamp'].dt.minute
                    
                    if start_min < end_min:
                        # Normal case
                        period_data = df[(df['minute_of_day'] >= start_min) & 
                                        (df['minute_of_day'] < end_min)].copy()
                    else:
                        # Wrap-around case (e.g., [1380, 60] = 23:00-01:00)
                        period_data = df[(df['minute_of_day'] >= start_min) | 
                                        (df['minute_of_day'] < end_min)].copy()
                
                if len(period_data) > 0:
                    ramp_params_by_period[app][period_name] = self._calculate_ramp_params_for_period(
                        period_data, col, period_name, (start_val, end_val), use_hourly
                    )
                else:
                    # No data for this period
                    ramp_params_by_period[app][period_name] = {
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
    
    def _calculate_ramp_params(self, df, power_col):
        """Helper: Calculate RAMP parameters for a single appliance."""
        df_temp = pd.DataFrame({
            'timestamp': df['timestamp'],
            'date_only': df['date_only'],
            'power': df[power_col],
            'hour': df['timestamp'].dt.hour
        })
        df_temp['active'] = df_temp['power'] > self.POWER_THRESHOLD
        
        # Functional time
        daily_minutes = []
        for date in df_temp['date_only'].unique():
            day_data = df_temp[df_temp['date_only'] == date]
            if day_data['active'].any():
                daily_minutes.append(day_data['active'].sum() * self.INTERVAL_MINUTES)
        
        daily_minutes = np.array(daily_minutes)
        func_time = round(daily_minutes.mean(), 1) if len(daily_minutes) > 0 else 0.0
        
        # Functional cycle (median usage period)
        usage_periods = []
        for date in df_temp['date_only'].unique():
            day_active = df_temp[df_temp['date_only'] == date]['active'].values
            if day_active.any():
                day_active_padded = np.concatenate(([False], day_active, [False]))
                changes = np.diff(day_active_padded.astype(int))
                starts = np.where(changes == 1)[0]
                ends = np.where(changes == -1)[0]
                for start, end in zip(starts, ends):
                    usage_periods.append((end - start) * self.INTERVAL_MINUTES)
        
        func_cycle = np.median(usage_periods) if usage_periods else 5.0
        time_variability = round(daily_minutes.std() / daily_minutes.mean(), 2) if (func_time > 0 and len(daily_minutes) > 1) else 0.0
        
        # Active windows (time periods with >10% daily probability)
        hour_probs = []
        for hour in range(24):
            hour_data = df[df['timestamp'].dt.hour == hour]
            if len(hour_data) > 0:
                hour_probs.append((hour_data.groupby('date_only')[power_col].max() > self.POWER_THRESHOLD).mean())
            else:
                hour_probs.append(0)
        
        windows = []
        in_window = False
        window_start = None
        
        for hour in range(24):
            if hour_probs[hour] > 0.1:
                if not in_window:
                    window_start = hour * 60
                    in_window = True
            elif in_window:
                windows.append([window_start, hour * 60])
                in_window = False
        
        if in_window:
            windows.append([window_start, 24 * 60])
        
        num_windows = len(windows) if len(windows) > 0 else 1
        if num_windows > 1:
            window_sizes = [w[1] - w[0] for w in windows]
            random_var_w = round(np.std(window_sizes) / np.mean(window_sizes), 2) if sum(window_sizes) > 0 else 0.0
        else:
            random_var_w = 0.0
        
        ramp_result = {
            'num_windows': num_windows,
            'func_time': func_time,
            'func_cycle': func_cycle,
            'time_fraction_random_variability': time_variability,
            'random_var_w': random_var_w
        }
        
        windows_to_add = windows if windows else [[0, 24 * 60]]
        for idx, window in enumerate(windows_to_add, start=1):
            ramp_result[f'window_{idx}'] = window
        
        return ramp_result
    
    def _calculate_ramp_params_for_period(self, df_period, power_col, period_name, period_bounds=None, use_hourly=True):
        """Helper: Calculate RAMP parameters for a single appliance within a specific time period.
        
        Args:
            df_period: DataFrame filtered to period
            power_col: Power column name
            period_name: Name of the period (e.g., 'morning', 'Indoor task light')
            period_bounds: Tuple of (start, end) in minutes or hours
            use_hourly: If True, period_bounds are in hours; if False, in minutes
        """
        df_temp = pd.DataFrame({
            'timestamp': df_period['timestamp'],
            'date_only': df_period['date_only'],
            'power': df_period[power_col],
        })
        df_temp['active'] = df_temp['power'] > self.POWER_THRESHOLD
        
        # Count days with data in this period
        num_days_with_data = df_period['date_only'].nunique()
        
        # Functional time (average active minutes per day in this period)
        daily_minutes_period = []
        days_with_activity = 0
        
        for date in df_temp['date_only'].unique():
            day_data = df_temp[df_temp['date_only'] == date]
            if day_data['active'].any():
                daily_minutes_period.append(day_data['active'].sum() * self.INTERVAL_MINUTES)
                days_with_activity += 1
        
        daily_minutes_period = np.array(daily_minutes_period)
        func_time = round(daily_minutes_period.mean(), 1) if len(daily_minutes_period) > 0 else 0.0
        
        # Occasional use probability: fraction of days in this period where appliance was used
        occasional_use_prob = round(days_with_activity / num_days_with_data, 2) if num_days_with_data > 0 else 0.0
        
        # Functional cycle (median usage period within this period)
        usage_periods = []
        for date in df_temp['date_only'].unique():
            day_active = df_temp[df_temp['date_only'] == date]['active'].values
            if day_active.any():
                day_active_padded = np.concatenate(([False], day_active, [False]))
                changes = np.diff(day_active_padded.astype(int))
                starts = np.where(changes == 1)[0]
                ends = np.where(changes == -1)[0]
                for start, end in zip(starts, ends):
                    usage_periods.append((end - start) * self.INTERVAL_MINUTES)
        
        func_cycle = round(np.median(usage_periods), 1) if usage_periods else 0.0
        time_variability = round(daily_minutes_period.std() / daily_minutes_period.mean(), 2) if (func_time > 0 and len(daily_minutes_period) > 1) else 0.0
        
        # Determine hours in period dynamically from period_bounds
        if use_hourly and period_bounds:
            start_hour, end_hour = period_bounds
            hours_in_period = self._get_hours_for_period(period_name)
        elif period_bounds:
            # Compute hours from minute boundaries
            start_min, end_min = period_bounds
            if start_min < end_min:
                hours_in_period = list(range(start_min // 60, (end_min + 59) // 60))
            else:
                # Wrap-around: e.g., [1380, 60] = 23:00-01:00
                hours_in_period = list(range(start_min // 60, 24)) + list(range(0, (end_min + 59) // 60))
        else:
            # Fallback to all hours
            hours_in_period = list(range(24))
        
        # Windows for this period (continuous time windows when appliance is typically active)
        hour_probs_period = []
        
        for hour in hours_in_period:
            hour_data = df_period[df_period['timestamp'].dt.hour == hour]
            if len(hour_data) > 0:
                prob = (hour_data.groupby('date_only')[power_col].max() > self.POWER_THRESHOLD).mean()
                hour_probs_period.append(prob)
            else:
                hour_probs_period.append(0)
        
        # Build windows within this period
        windows = []
        in_window = False
        window_start = None
        
        for idx, hour in enumerate(hours_in_period):
            if hour_probs_period[idx] > 0.1:
                if not in_window:
                    window_start = hour * 60
                    in_window = True
            elif in_window:
                windows.append([window_start, hour * 60])
                in_window = False
        
        if in_window:
            windows.append([window_start, (hours_in_period[-1] + 1) * 60])
        
        num_windows = len(windows) if len(windows) > 0 else 1
        if num_windows > 1:
            window_sizes = [w[1] - w[0] for w in windows]
            random_var_w = round(np.std(window_sizes) / np.mean(window_sizes), 2) if sum(window_sizes) > 0 else 0.0
        else:
            random_var_w = 0.0
        
        ramp_result = {
            'period': period_name,
            'num_windows': num_windows,
            'func_time': func_time,
            'func_cycle': func_cycle,
            'time_fraction_random_variability': time_variability,
            'random_var_w': random_var_w,
            'occasional_use_probability': occasional_use_prob,
            'num_days_with_data': num_days_with_data,
            'days_with_activity': days_with_activity
        }
        
        windows_to_add = windows if windows else [[0, 0]]
        for idx, window in enumerate(windows_to_add, start=1):
            ramp_result[f'window_{idx}'] = window
        
        return ramp_result
    
    def _get_hours_for_period(self, period_name):
        """Helper: Get list of hours for a given period."""
        periods = {
            'morning': list(range(5, 8)),      # 5, 6, 7
            'daytime': list(range(8, 17)),     # 8, 9, ..., 16
            'evening': list(range(17, 24)),    # 17, 18, ..., 23
            'night': list(range(0, 5))         # 0, 1, 2, 3, 4
        }
        return periods.get(period_name, [])

    
    def extract_power_variation(self, df):
        """Extract power variation metrics for each appliance."""
        power_variation = {}
        thermal_p_var = {}
        
        for app, col in zip(self.appliances, self.power_cols):
            stats = self._calculate_power_stats(df[col])
            power_variation[app] = stats
            thermal_p_var[app] = stats['coeff_variation']
        
        return {'power_variation': power_variation, 'thermal_p_var': thermal_p_var}
    
    def _calculate_power_stats(self, power_series):
        """Helper: Calculate power statistics for a single appliance."""
        active_power = power_series[power_series > self.POWER_THRESHOLD]
        
        if len(active_power) == 0:
            return {k: 0.0 for k in ['mean_power_W', 'std_power_W', 'coeff_variation', 'min_power_W', 'max_power_W', 'range_power_W', 'median_power_W', 'q25_power_W', 'q75_power_W']}
        
        mean_power = active_power.mean()
        std_power = active_power.std()
        
        return {
            'mean_power_W': round(mean_power, 2),
            'std_power_W': round(std_power, 2),
            'coeff_variation': round((std_power / mean_power) if mean_power > 0 else 0.0, 2),
            'min_power_W': round(active_power.min(), 2),
            'max_power_W': round(active_power.max(), 2),
            'range_power_W': round(active_power.max() - active_power.min(), 2),
            'median_power_W': round(active_power.median(), 2),
            'q25_power_W': round(active_power.quantile(0.25), 2),
            'q75_power_W': round(active_power.quantile(0.75), 2)
        }
