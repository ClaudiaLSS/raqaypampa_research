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
        # Probability that device is used at least once during the day
        daily_all = df.groupby('date_only')[['p_led_1', 'p_led_2', 'p_usb']].max()
        daily_event_probs = {
            'LED_1_Prob': round((daily_all['p_led_1'] > 0.5).mean(), 2),
            'LED_2_Prob': round((daily_all['p_led_2'] > 0.5).mean(), 2),
            'USB_Prob': round((daily_all['p_usb'] > 0.5).mean(), 2)
        }
        
        # 4. Calculate RAMP-specific parameters for each appliance
        def calculate_ramp_params(power_series, col_name, daily_threshold=0.0):
            """
            Calculate RAMP parameters: num_windows, windows, func_time,
            time_fraction_random_variability, random_var_w
            
            Args:
                power_series: The power data series
                col_name: Original column name in df (e.g., 'p_led_1')
                daily_threshold: Threshold for active detection (0 = any power > 0)
            """
            # Add hour and minute to dataframe for this calculation
            df_temp = pd.DataFrame({
                'timestamp': df['timestamp'],
                'date_only': df['date_only'],
                'power': power_series,
                'hour': df['timestamp'].dt.hour,
                'minute': df['timestamp'].dt.minute
            })
            
            # Find active periods (power > threshold)
            df_temp['active'] = df_temp['power'] > daily_threshold
            
            # Calculate daily functioning time (minutes per day)
            # Data is in 5-minute intervals, so multiply by 5
            INTERVAL_MINUTES = 5
            daily_minutes = []
            for date in df_temp['date_only'].unique():
                day_data = df_temp[df_temp['date_only'] == date]
                if day_data['active'].any():
                    # Count active 5-minute intervals and convert to actual minutes
                    active_intervals = day_data['active'].sum()
                    active_minutes = active_intervals * INTERVAL_MINUTES
                    daily_minutes.append(active_minutes)
            
            daily_minutes = np.array(daily_minutes)
            
            # Average functioning time (in minutes per day)
            func_time = round(daily_minutes.mean(), 1) if len(daily_minutes) > 0 else 0.0
            
            # Find shortest contiguous usage period to set as func_cycle
            # This identifies the minimum duration the appliance stays on
            usage_periods = []  # Will store duration of each contiguous "on" period
            
            for date in df_temp['date_only'].unique():
                day_data = df_temp[df_temp['date_only'] == date]
                day_active = day_data['active'].values
                
                # Find contiguous blocks of True values
                if day_active.any():
                    # Add a False at the start and end to simplify edge detection
                    day_active_padded = np.concatenate(([False], day_active, [False]))
                    changes = np.diff(day_active_padded.astype(int))
                    
                    # starts[i] is where a True block starts, ends[i] is where it ends
                    starts = np.where(changes == 1)[0]
                    ends = np.where(changes == -1)[0]
                    
                    # Duration of each contiguous period (in intervals, multiply by 5 min)
                    for start, end in zip(starts, ends):
                        period_duration = (end - start) * INTERVAL_MINUTES
                        usage_periods.append(period_duration)
            
            # Find 5th percentile usage period as func_cycle (much smaller, more robust)
            # This gives a realistic minimum usage duration while being very RAMP-compatible
            if usage_periods:
                func_cycle = np.percentile(usage_periods, 5)
            else:
                func_cycle = 5.0  # Default to 5 minutes if no data
            
            # Time fraction random variability (coefficient of variation)
            if func_time > 0 and len(daily_minutes) > 1:
                time_fraction_random_variability = round(daily_minutes.std() / daily_minutes.mean(), 2)
            else:
                time_fraction_random_variability = 0.0
            
            # Print daily usage breakdown for inspection
            print(f"\n    Daily usage breakdown for {col_name}:")
            print(f"      Mean: {func_time:.1f} min/day")
            print(f"      Std Dev: {daily_minutes.std():.1f} min")
            print(f"      Min: {daily_minutes.min():.1f} min")
            print(f"      Max: {daily_minutes.max():.1f} min")
            print(f"      Variability (CV): {time_fraction_random_variability:.2f}")
            print(f"      Sample size: {len(daily_minutes)} days")
            print(f"      5th percentile usage period (func_cycle): {func_cycle:.1f} min")
            print(f"      Longest usage period: {max(usage_periods):.1f} min" if usage_periods else "      No usage periods found")
            print(f"      Total usage periods detected: {len(usage_periods)}")
            
            # Show distribution in bins
            if len(daily_minutes) > 0:
                bins = [0, 30, 60, 120, 240, 480, 1440]
                bin_labels = ['0-30', '30-60', '60-120', '120-240', '240-480', '480+']
                hist, _ = np.histogram(daily_minutes, bins=bins)
                print(f"      Distribution (minutes/day):")
                for label, count in zip(bin_labels, hist):
                    pct = 100 * count / len(daily_minutes)
                    print(f"        {label:>8} min: {count:3d} days ({pct:5.1f}%)")
            
            # Detect usage windows from hourly probabilities
            # A window is a contiguous set of hours where probability > 0.1
            windows = []
            in_window = False
            window_start = None
            
            hour_probs = []
            for hour in range(24):
                # Use the original column name from df
                hour_data = df[df['timestamp'].dt.hour == hour]
                if len(hour_data) > 0:
                    daily_hour = hour_data.groupby('date_only')[col_name].max()
                    hour_prob = (daily_hour > daily_threshold).mean()
                else:
                    hour_prob = 0
                hour_probs.append(hour_prob)
            
            for hour in range(24):
                if hour_probs[hour] > 0.1:  # Threshold for window detection
                    if not in_window:
                        window_start = hour * 60  # Convert to minutes
                        in_window = True
                elif in_window:
                    window_end = hour * 60  # End of previous hour
                    windows.append([window_start, window_end])
                    in_window = False
            
            # Close last window if still open
            if in_window:
                windows.append([window_start, 24 * 60])
            
            num_windows = len(windows)
            
            # Random variability in window size (std of window sizes / mean window size)
            if num_windows > 0:
                window_sizes = [w[1] - w[0] for w in windows]
                if len(window_sizes) > 1 and sum(window_sizes) > 0:
                    random_var_w = round(np.std(window_sizes) / np.mean(window_sizes), 2)
                else:
                    random_var_w = 0.0
            else:
                random_var_w = 0.0
            
            # Create RAMP-style window naming: window_1, window_2, etc.
            ramp_result = {
                'num_windows': num_windows if num_windows > 0 else 1,
                'func_time': func_time,
                'func_cycle': func_cycle,
                'time_fraction_random_variability': time_fraction_random_variability,
                'random_var_w': random_var_w
            }
            
            # Add individual windows with RAMP naming convention
            windows_to_add = windows if windows else [[0, 24*60]]
            for idx, window in enumerate(windows_to_add, start=1):
                ramp_result[f'window_{idx}'] = window
            
            return ramp_result
        
        # Calculate parameters for each appliance
        ramp_params = {}
        for appliance, col_name in [('LED_1', 'p_led_1'), 
                                     ('LED_2', 'p_led_2'), 
                                     ('USB', 'p_usb')]:
            ramp_params[appliance] = calculate_ramp_params(df[col_name], col_name)

        params = {
            'hardware': hardware,
            'daily_event_probs': daily_event_probs,
            'hourly_probs': hourly_probs,
            'peak_hours': peak_hours,
            'ramp_params': ramp_params
        }
        
        # Extract user ID from filename (e.g., "tpdin_user_74.csv" -> "74")
        user_id = filename.stem.split('_')[-1]
        
        # Save to individual JSON file
        output_json = OUTPUT_DIR / f"empirical_parameters_user_{user_id}.json"
        with open(output_json, 'w') as f:
            json.dump(params, f, indent=4)
        
        # Create hourly probability matrix (for easy analysis)
        hourly_matrix_data = {
            'Hour': list(range(24))
        }
        for appliance in ['LED_1', 'LED_2', 'USB']:
            hourly_matrix_data[appliance] = [
                hourly_probs[f'hour_{hour:02d}'][f'{appliance}_Prob']
                for hour in range(24)
            ]
        
        hourly_matrix_df = pd.DataFrame(hourly_matrix_data)
        output_hourly = OUTPUT_DIR / f"hourly_probabilities_user_{user_id}.csv"
        hourly_matrix_df.to_csv(output_hourly, index=False)
        
        print(f"✓ User {user_id}: saved to {output_json.name}")
        print(f"✓ Hourly matrix: saved to {output_hourly.name}")
        print("\nHourly Probabilities Matrix:")
        print(hourly_matrix_df.to_string(index=False))
        print()
        
        return {
            'user_id': user_id,
            'file': filename.name,
            'params': params
        }
    
    except Exception as e:
        print(f"✗ Error processing {filename.name}: {e}")
        return None


def batch_process(input_pattern=None):
    """Process all CSV files in INPUT_DIR.
    
    Args:
        input_pattern: Optional glob pattern to filter files (e.g., "tpdin_user_74.csv")
    """
    if not INPUT_DIR.exists():
        print(f"Error: Input directory not found: {INPUT_DIR}")
        sys.exit(1)
    
    # Find CSV files
    if input_pattern:
        csv_files = list(INPUT_DIR.glob(input_pattern))
        print(f"\nSearching for pattern: {input_pattern}")
    else:
        csv_files = list(INPUT_DIR.glob("*.csv"))
        print(f"\nProcessing all CSV files from: {INPUT_DIR}")
    
    if not csv_files:
        print("No CSV files found!")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} file(s) to process\n")
    
    # Process each file
    results = []
    for csv_file in sorted(csv_files):
        result = extract_parameters(csv_file)
        if result:
            results.append(result)
    
    # Create summary CSV
    if results:
        summary_data = []
        for result in results:
            row = {
                'user_id': result['user_id'],
                'file': result['file'],
                'led_1_W': result['params']['hardware']['led_1_W'],
                'led_2_W': result['params']['hardware']['led_2_W'],
                'usb_W': result['params']['hardware']['usb_W'],
                'LED_1_daily_prob': result['params']['daily_event_probs']['LED_1_Prob'],
                'LED_2_daily_prob': result['params']['daily_event_probs']['LED_2_Prob'],
                'USB_daily_prob': result['params']['daily_event_probs']['USB_Prob'],
                'LED_1_peak_hour': result['params']['peak_hours']['LED_1']['hour'],
                'LED_1_peak_prob': result['params']['peak_hours']['LED_1']['probability'],
                'LED_2_peak_hour': result['params']['peak_hours']['LED_2']['hour'],
                'LED_2_peak_prob': result['params']['peak_hours']['LED_2']['probability'],
                'USB_peak_hour': result['params']['peak_hours']['USB']['hour'],
                'USB_peak_prob': result['params']['peak_hours']['USB']['probability'],
            }
            
            # Add hourly probabilities
            for hour, probs in result['params']['hourly_probs'].items():
                row[f'{hour}_LED_1'] = probs['LED_1_Prob']
                row[f'{hour}_LED_2'] = probs['LED_2_Prob']
                row[f'{hour}_USB'] = probs['USB_Prob']
            
            summary_data.append(row)
        
        summary_df = pd.DataFrame(summary_data)
        summary_csv = OUTPUT_DIR / "empirical_parameters_summary.csv"
        summary_df.to_csv(summary_csv, index=False)
        
        print(f"\n✓ Summary saved to: {summary_csv.name}")
        print(f"\nProcessed {len(results)} file(s) successfully")
        print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract energy parameters from timeseries CSV files"
    )
    parser.add_argument(
        "--user",
        type=str,
        help="Process specific user (e.g., '74')"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        help="Glob pattern to filter files (e.g., 'tpdin_user_*.csv')"
    )
    
    args = parser.parse_args()
    
    if args.user:
        # Process specific user
        pattern = f"*_user_{args.user}.csv"
        batch_process(input_pattern=pattern)
    elif args.pattern:
        # Process with custom pattern
        batch_process(input_pattern=args.pattern)
    else:
        # Process all files
        batch_process()