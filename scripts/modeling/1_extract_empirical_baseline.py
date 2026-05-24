"""
DEPRECATED: Use extract_empirical_baseline.py instead (modular architecture)

This script is kept for reference only. The new pipeline supports both
OLD and TPDIN datalogger types automatically with a flexible architecture.

See README.md for the new modular design.
"""
import pandas as pd
import numpy as np
import json
import argparse
from pathlib import Path
import sys

# Define input and output directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_parameters(filename):
    """Extract parameters from a single CSV file.
    
    Returns: dict with extracted parameters and user identifier
    """
    print(f"Extracting parameters from {filename.name}...")
    
    try:
        df = pd.read_csv(filename)
        df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df['date_only'] = df['timestamp'].dt.date
        
        # Calculate Power (V * I)
        df['p_led_1'] = (df['v_led_1'] * df['c_led_1']).clip(lower=0)
        df['p_led_2'] = (df['v_led_2'] * df['c_led_2']).clip(lower=0)
        df['p_usb'] = (df['v_usb'] * df['c_usb']).clip(lower=0)
        
        # Calculate Total System Power
        df['p_total'] = df['p_led_1'] + df['p_led_2'] + df['p_usb']
            
        # 1. Extract Hardware Realities (Median Wattage when ON)
        hardware = {
            'led_1_W': round(df[df['p_led_1'] > 0.5]['p_led_1'].median(), 2),
            'led_2_W': round(df[df['p_led_2'] > 0.5]['p_led_2'].median(), 2),
            'usb_W': round(df[df['p_usb'] > 0.5]['p_usb'].median(), 2)
        }
        
        # 2. Extract Probabilities by Hour (24-hour analysis)
        def get_probs(sub_df):
            """Calculate probability of use (daily max > 0.5W) for a time period"""
            daily = sub_df.groupby('date_only')[['p_led_1', 'p_led_2', 'p_usb']].max()
            return {
                'LED_1_Prob': round((daily['p_led_1'] > 0.5).mean(), 2),
                'LED_2_Prob': round((daily['p_led_2'] > 0.5).mean(), 2),
                'USB_Prob': round((daily['p_usb'] > 0.5).mean(), 2)
            }
        
        # Analyze each hour of the day
        hourly_probs = {}
        for hour in range(24):
            hour_data = df[df['timestamp'].dt.hour == hour]
            if len(hour_data) > 0:
                hourly_probs[f'hour_{hour:02d}'] = get_probs(hour_data)
            else:
                hourly_probs[f'hour_{hour:02d}'] = {
                    'LED_1_Prob': 0.0,
                    'LED_2_Prob': 0.0,
                    'USB_Prob': 0.0
                }
        
        # Find peak hours for each appliance
        peak_hours = {}
        for appliance in ['LED_1', 'LED_2', 'USB']:
            max_prob = 0.0
            peak_hour = -1
            for hour in range(24):
                prob = hourly_probs[f'hour_{hour:02d}'][f'{appliance}_Prob']
                if prob > max_prob:
                    max_prob = prob
                    peak_hour = hour
            peak_hours[appliance] = {
                'hour': peak_hour,
                'probability': max_prob
            }
        
        # 3. Extract Daily Event Probability (occasional_use in RAMP)
        daily_all = df.groupby('date_only')[['p_led_1', 'p_led_2', 'p_usb']].max()
        daily_event_probs = {
            'LED_1_Prob': round((daily_all['p_led_1'] > 0.5).mean(), 2),
            'LED_2_Prob': round((daily_all['p_led_2'] > 0.5).mean(), 2),
            'USB_Prob': round((daily_all['p_usb'] > 0.5).mean(), 2)
        }
        
        # 3. Calculate RAMP-specific parameters for each appliance
        def calculate_ramp_params(power_series, col_name, daily_threshold=0.0):
            INTERVAL_MINUTES = 5
            df_temp = pd.DataFrame({'timestamp': df['timestamp'], 'date_only': df['date_only'], 'power': power_series, 'hour': df['timestamp'].dt.hour})
            df_temp['active'] = df_temp['power'] > daily_threshold
            
            daily_minutes = []
            for date in df_temp['date_only'].unique():
                day_data = df_temp[df_temp['date_only'] == date]
                if day_data['active'].any():
                    daily_minutes.append(day_data['active'].sum() * INTERVAL_MINUTES)
            
            daily_minutes = np.array(daily_minutes)
            func_time = round(daily_minutes.mean(), 1) if len(daily_minutes) > 0 else 0.0
            
            usage_periods = []
            for date in df_temp['date_only'].unique():
                day_active = df_temp[df_temp['date_only'] == date]['active'].values
                if day_active.any():
                    day_active_padded = np.concatenate(([False], day_active, [False]))
                    changes = np.diff(day_active_padded.astype(int))
                    starts = np.where(changes == 1)[0]
                    ends = np.where(changes == -1)[0]
                    for start, end in zip(starts, ends):
                        usage_periods.append((end - start) * INTERVAL_MINUTES)
            
            func_cycle = np.median(usage_periods) if usage_periods else 5.0
            time_fraction_random_variability = round(daily_minutes.std() / daily_minutes.mean(), 2) if (func_time > 0 and len(daily_minutes) > 1) else 0.0
            
            windows = []
            in_window = False
            window_start = None
            
            hour_probs = []
            for hour in range(24):
                hour_data = df[df['timestamp'].dt.hour == hour]
                if len(hour_data) > 0:
                    hour_probs.append((hour_data.groupby('date_only')[col_name].max() > daily_threshold).mean())
                else:
                    hour_probs.append(0)
            
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
            
            num_windows = len(windows)
            if num_windows > 0:
                window_sizes = [w[1] - w[0] for w in windows]
                random_var_w = round(np.std(window_sizes) / np.mean(window_sizes), 2) if (len(window_sizes) > 1 and sum(window_sizes) > 0) else 0.0
            else:
                random_var_w = 0.0
            
            ramp_result = {
                'num_windows': num_windows if num_windows > 0 else 1,
                'func_time': func_time, 'func_cycle': func_cycle,
                'time_fraction_random_variability': time_fraction_random_variability, 'random_var_w': random_var_w
            }
            windows_to_add = windows if windows else [[0, 24*60]]
            for idx, window in enumerate(windows_to_add, start=1):
                ramp_result[f'window_{idx}'] = window
            return ramp_result
        
        ramp_params = {app: calculate_ramp_params(df[col], col) for app, col in [('LED_1', 'p_led_1'), ('LED_2', 'p_led_2'), ('USB', 'p_usb')]}

        # 5. Calculate Power Variation
        def calculate_power_variation(power_series, col_name, threshold=0.5):
            active_power = power_series[power_series > threshold]
            if len(active_power) == 0:
                return {k: 0.0 for k in ['mean_power_W', 'std_power_W', 'coeff_variation', 'min_power_W', 'max_power_W', 'range_power_W', 'median_power_W', 'q25_power_W', 'q75_power_W']}
            
            mean_power, std_power = active_power.mean(), active_power.std()
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
        
        power_variation = {app: calculate_power_variation(df[col], col) for app, col in [('LED_1', 'p_led_1'), ('LED_2', 'p_led_2'), ('USB', 'p_usb')]}
        thermal_p_var = {app: power_variation[app]['coeff_variation'] for app in ['LED_1', 'LED_2', 'USB']}

        # 6. Calculate TIER 2: Structural Profiling & Resilience Metrics
        def calculate_structural_metrics(df, threshold=0.5):
            """Calculate structural profiling and resilience metrics for total system."""
            total_power = df['p_total']
            
            # Modal Peak Hour: hour with highest median power (system-wide)
            hourly_medians = df.groupby(df['timestamp'].dt.hour)['p_total'].median()
            modal_peak_hour = int(hourly_medians.idxmax()) if len(hourly_medians) > 0 else 0
            
            # Base Load: 10th percentile of non-zero power (system idle but on)
            active_periods = total_power[total_power > threshold]
            if len(active_periods) > 0:
                base_load_W = round(active_periods.quantile(0.1), 2)
            else:
                base_load_W = 0.0
            
            # MRSD (Mean Relative Standard Deviation) - Chaos Index
            # Calculate coefficient of variation for each day, then take mean
            daily_cv_list = []
            for date in df['date_only'].unique():
                day_power = df[df['date_only'] == date]['p_total']
                day_mean = day_power.mean()
                day_std = day_power.std()
                if day_mean > 0:
                    daily_cv_list.append(day_std / day_mean)
            
            mrsd_chaos_index = round(np.mean(daily_cv_list), 3) if daily_cv_list else 0.0
            
            # Relative Mean Power by time-of-day (morning, daytime, evening, night)
            # Morning: 06:00-11:59, Daytime: 12:00-17:59, Evening: 18:00-23:59, Night: 00:00-05:59
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
        
        structural_metrics = calculate_structural_metrics(df)

        # 7. Calculate RELIABILITY METRICS: Blackout Frequency, Climatic vs Behavioral Rates
        def calculate_reliability_metrics(df, threshold=0.5):
            """Calculate blackout and reliability metrics."""
            # Identify blackouts: gaps in timestamp data (data logger stopped recording)
            df_copy = df.copy()
            df_copy['time_diff_minutes'] = df_copy['timestamp'].diff().dt.total_seconds() / 60
            
            # Define blackout as a gap > 7 minutes (expected interval is 5 min)
            EXPECTED_INTERVAL = 5
            BLACKOUT_THRESHOLD = 7
            df_copy['is_blackout'] = df_copy['time_diff_minutes'] > BLACKOUT_THRESHOLD
            
            # Group consecutive blackouts
            df_copy['blackout_block'] = (df_copy['is_blackout'] != df_copy['is_blackout'].shift()).cumsum()
            bo_blocks = df_copy[df_copy['is_blackout'] == True].groupby('blackout_block')
            
            total_bo_events = bo_blocks.ngroups
            
            # Mean Outage Duration (in minutes)
            mean_outage_duration = 0.0
            if total_bo_events > 0:
                outage_durations = []
                for _, group in bo_blocks:
                    duration = group['time_diff_minutes'].iloc[0]  # Duration of the gap
                    outage_durations.append(duration)
                mean_outage_duration = round(np.mean(outage_durations), 1)
            
            # Reliability Index: % of time with data (system operational)
            total_time_minutes = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60
            if total_time_minutes > 0:
                ri_percent = ((total_time_minutes - (bo_blocks.size().sum() * EXPECTED_INTERVAL if total_bo_events > 0 else 0)) / total_time_minutes) * 100
            else:
                ri_percent = 0.0
            
            # Climatic vs Behavioral Blackout Rate
            climatic_events = 0
            df_copy['hour'] = df_copy['timestamp'].dt.hour
            
            for _, group in bo_blocks:
                blackout_start = group['timestamp'].min()
                # Look back 24 hours before blackout
                lookback_start = blackout_start - pd.Timedelta(hours=24)
                prev_data = df[(df['timestamp'] >= lookback_start) & (df['timestamp'] < blackout_start)]
                
                if len(prev_data) > 0:
                    # Check if sufficient sun during peak hours (10:00-15:00)
                    sun_hours = prev_data[(prev_data['hour'] >= 10) & (prev_data['hour'] <= 15)]
                    if len(sun_hours) > 0 and sun_hours['v_pv'].mean() < 15.0:
                        # Low PV voltage = climatic failure
                        climatic_events += 1
            
            behavioral_events = total_bo_events - climatic_events
            
            # Calculate rates as events per 100 days
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
        
        reliability_metrics = calculate_reliability_metrics(df)

        # Pack final params
        params = {
            'hardware': hardware,
            'daily_event_probs': daily_event_probs,
            'hourly_probs': hourly_probs,
            'peak_hours': peak_hours,
            'power_variation': power_variation,
            'thermal_p_var': thermal_p_var,
            'ramp_params': ramp_params,
            'structural_metrics': structural_metrics,
            'reliability_metrics': reliability_metrics
        }
        
        user_id = filename.stem.split('_')[-1]
        
        # Print extracted parameters to console
        print(f"\n{'='*70}")
        print(f"USER {user_id} - EXTRACTED PARAMETERS")
        print(f"{'='*70}")
        
        print(f"\n📱 HARDWARE (Median Wattage when ON):")
        for appliance, wattage in hardware.items():
            print(f"   {appliance.replace('_W', '').upper()}: {wattage} W")
        
        print(f"\n📊 DAILY EVENT PROBABILITIES (Probability of use per day):")
        for appliance, prob in daily_event_probs.items():
            print(f"   {appliance.replace('_Prob', '').upper()}: {prob*100:.1f}%")
        
        print(f"\n⏰ PEAK HOURS:")
        for appliance, peak_info in peak_hours.items():
            hour = peak_info['hour']
            prob = peak_info['probability']
            print(f"   {appliance}: Hour {hour:02d}:00 ({prob*100:.1f}% probability)")
        
        print(f"\n⚡ POWER VARIATION (Active power statistics):")
        for appliance, stats in power_variation.items():
            print(f"   {appliance}:")
            print(f"      Mean: {stats['mean_power_W']:.2f} W | Std: {stats['std_power_W']:.2f} W | CV: {stats['coeff_variation']:.2f}")
            print(f"      Range: {stats['min_power_W']:.2f} - {stats['max_power_W']:.2f} W | Median: {stats['median_power_W']:.2f} W")
        
        print(f"\n🔄 RAMP PARAMETERS:")
        for appliance, ramp_data in ramp_params.items():
            print(f"   {appliance}:")
            print(f"      Windows: {ramp_data['num_windows']} | Func Time: {ramp_data['func_time']:.1f} min | Func Cycle: {ramp_data['func_cycle']:.1f} min")
            print(f"      Time Variability: {ramp_data['time_fraction_random_variability']:.2f} | Window Variability: {ramp_data['random_var_w']:.2f}")
            for window_idx in range(1, ramp_data['num_windows'] + 1):
                window = ramp_data[f'window_{window_idx}']
                print(f"      Window {window_idx}: {window[0]:.0f} - {window[1]:.0f} minutes")
        
        print(f"\n📊 TIER 2: STRUCTURAL PROFILING & RESILIENCE METRICS:")
        print(f"   Modal Peak Hour: {structural_metrics['modal_peak_hour']:02d}:00")
        print(f"   Base Load: {structural_metrics['base_load_W']:.2f} W")
        print(f"   MRSD Chaos Index: {structural_metrics['mrsd_chaos_index']:.3f}")
        print(f"   Overall Mean Power: {structural_metrics['overall_mean_power_W']:.2f} W")
        print(f"   Relative Mean Power by Time-of-Day:")
        for period, rel_power in structural_metrics['relative_mean_power'].items():
            print(f"      {period.capitalize()}: {rel_power:.3f}x overall mean")
        
        print(f"\n🔋 RELIABILITY METRICS: BLACKOUT ANALYSIS:")
        print(f"   Blackout Frequency: {reliability_metrics['bo_freq_events']} events")
        print(f"   Mean Outage Duration: {reliability_metrics['mean_outage_duration_min']:.1f} minutes")
        print(f"   Reliability Index: {reliability_metrics['ri_percent']:.2f}%")
        print(f"   Climatic Blackouts: {reliability_metrics['climatic_blackout_events']} events ({reliability_metrics['cbr_events_per_100days']:.2f} per 100 days)")
        print(f"   Behavioral Blackouts: {reliability_metrics['behavioral_blackout_events']} events ({reliability_metrics['bbr_events_per_100days']:.2f} per 100 days)")
        
        print(f"\n{'='*70}\n")
        
        # Save JSON
        output_json = OUTPUT_DIR / f"empirical_parameters_user_{user_id}.json"
        with open(output_json, 'w') as f:
            json.dump(params, f, indent=4)
        
        # Save Hourly Matrix
        hourly_matrix_data = {'Hour': list(range(24))}
        for appliance in ['LED_1', 'LED_2', 'USB']:
            hourly_matrix_data[appliance] = [hourly_probs[f'hour_{hour:02d}'][f'{appliance}_Prob'] for hour in range(24)]
        hourly_matrix_df = pd.DataFrame(hourly_matrix_data)
        output_hourly = OUTPUT_DIR / f"hourly_probabilities_user_{user_id}.csv"
        hourly_matrix_df.to_csv(output_hourly, index=False)
        
        print(f"✓ User {user_id}: saved to {output_json.name}")
        
        return {'user_id': user_id, 'file': filename.name, 'params': params}
    
    except Exception as e:
        print(f"✗ Error processing {filename.name}: {e}")
        return None


def batch_process(input_pattern=None):
    if not INPUT_DIR.exists():
        print(f"Error: Input directory not found: {INPUT_DIR}")
        sys.exit(1)
    
    csv_files = list(INPUT_DIR.glob(input_pattern)) if input_pattern else list(INPUT_DIR.glob("*.csv"))
    if not csv_files:
        print("No CSV files found!")
        sys.exit(1)
        
    print(f"Found {len(csv_files)} file(s) to process\n")
    
    results = [extract_parameters(f) for f in sorted(csv_files)]
    results = [r for r in results if r]
    
    if results:
        summary_data = []
        for result in results:
            row = {
                'user_id': result['user_id'],
                'file': result['file'],
                'led_1_W': result['params']['hardware']['led_1_W'],
                'led_2_W': result['params']['hardware']['led_2_W'],
                'usb_W': result['params']['hardware']['usb_W'],
                'thermal_p_var_LED_1': result['params']['thermal_p_var']['LED_1'],
                'LED_1_daily_prob': result['params']['daily_event_probs']['LED_1_Prob'],
                'LED_1_peak_hour': result['params']['peak_hours']['LED_1']['hour'],
                'LED_1_peak_prob': result['params']['peak_hours']['LED_1']['probability'],
                'modal_peak_hour': result['params']['structural_metrics']['modal_peak_hour'],
                'base_load_W': result['params']['structural_metrics']['base_load_W'],
                'mrsd_chaos_index': result['params']['structural_metrics']['mrsd_chaos_index'],
                'overall_mean_power_W': result['params']['structural_metrics']['overall_mean_power_W'],
                'relative_mean_power_morning': result['params']['structural_metrics']['relative_mean_power']['morning'],
                'relative_mean_power_daytime': result['params']['structural_metrics']['relative_mean_power']['daytime'],
                'relative_mean_power_evening': result['params']['structural_metrics']['relative_mean_power']['evening'],
                'relative_mean_power_night': result['params']['structural_metrics']['relative_mean_power']['night'],
                'bo_freq_events': result['params']['reliability_metrics']['bo_freq_events'],
                'mean_outage_duration_min': result['params']['reliability_metrics']['mean_outage_duration_min'],
                'ri_percent': result['params']['reliability_metrics']['ri_percent'],
                'climatic_blackout_events': result['params']['reliability_metrics']['climatic_blackout_events'],
                'behavioral_blackout_events': result['params']['reliability_metrics']['behavioral_blackout_events'],
                'cbr_events_per_100days': result['params']['reliability_metrics']['cbr_events_per_100days'],
                'bbr_events_per_100days': result['params']['reliability_metrics']['bbr_events_per_100days'],
            }
            # (Truncated other appliance appending for brevity)
            summary_data.append(row)
        
        summary_df = pd.DataFrame(summary_data)
        summary_csv = OUTPUT_DIR / "empirical_parameters_summary.csv"
        summary_df.to_csv(summary_csv, index=False)
        print(f"\n✓ Summary saved to: {summary_csv.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract energy parameters from timeseries CSV files")
    parser.add_argument("--user", type=str, help="Process specific user (e.g., '74')")
    parser.add_argument("--pattern", type=str, help="Glob pattern to filter files (e.g., 'tpdin_user_*.csv')")
    
    args = parser.parse_args()
    pattern = f"*_user_{args.user}.csv" if args.user else args.pattern
    batch_process(input_pattern=pattern)