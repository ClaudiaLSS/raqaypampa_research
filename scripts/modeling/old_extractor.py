"""
Extractor for OLD (legacy) dataloggers.
Measures: v_led_1, v_usb, c_led, c_usb (LEDs combined, USB separate)
"""
import pandas as pd
import numpy as np
from base_extractor import BaseExtractor


class OldExtractor(BaseExtractor):
    """Handler for OLD (legacy) datalogger format."""
    
    def __init__(self):
        super().__init__()
        self.appliances = ['LED', 'USB']  # Combined LEDs
        self.power_cols = ['p_led', 'p_usb']
        self.voltage_cols = ['v_led_1', 'v_usb']
        self.current_cols = ['c_led', 'c_usb']
    
    def preprocess(self, filename):
        """Load and standardize OLD dataframe."""
        df = pd.read_csv(filename)
        
        # Standardize timestamp
        df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df['date_only'] = df['timestamp'].dt.date
        
        # Calculate power for each appliance
        # Old format: v_led_1 for LED, c_led for LED current
        df['p_led'] = (df['v_led_1'] * df['c_led']).clip(lower=0)
        df['p_usb'] = (df['v_usb'] * df['c_usb']).clip(lower=0)
        
        # Total system power
        df['p_total'] = df['p_led'] + df['p_usb']
        
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
                    'LED_Prob': round((daily['p_led'] > self.POWER_THRESHOLD).mean(), 2),
                    'USB_Prob': round((daily['p_usb'] > self.POWER_THRESHOLD).mean(), 2)
                }
            else:
                hourly_probs[f'hour_{hour:02d}'] = {
                    'LED_Prob': 0.0,
                    'USB_Prob': 0.0
                }
        
        # Find peak hours for each appliance
        peak_hours = {}
        for app in self.appliances:
            prob_key = f'{app}_Prob'
            max_prob = 0.0
            peak_hour = 0
            for hour in range(24):
                prob = hourly_probs[f'hour_{hour:02d}'][prob_key]
                if prob > max_prob:
                    max_prob = prob
                    peak_hour = hour
            peak_hours[app] = {'hour': peak_hour, 'probability': max_prob}
        
        # Daily event probabilities
        daily_all = df.groupby('date_only')[self.power_cols].max()
        daily_event_probs = {
            'LED_Prob': round((daily_all['p_led'] > self.POWER_THRESHOLD).mean(), 2),
            'USB_Prob': round((daily_all['p_usb'] > self.POWER_THRESHOLD).mean(), 2)
        }
        
        return {
            'hourly_probs': hourly_probs,
            'peak_hours': peak_hours,
            'daily_event_probs': daily_event_probs
        }
    
    def extract_ramp_params(self, df):
        """Extract RAMP parameters for each appliance."""
        ramp_params = {}
        
        for app, col in zip(self.appliances, self.power_cols):
            ramp_params[app] = self._calculate_ramp_params(df, col)
        
        return ramp_params
    
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
        
        # Functional cycle
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
        
        # Active windows
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
