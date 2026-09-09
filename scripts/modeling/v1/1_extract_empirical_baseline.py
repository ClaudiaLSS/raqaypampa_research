"""
Main extraction pipeline for empirical baseline metrics.
Auto-detects datalogger type (OLD, BLUE or TPDIN) and routes to appropriate extractor.
Auto-classifies household profile and extracts anthropological time windows for RAMP analysis.
"""
import pandas as pd
import json
import argparse
from pathlib import Path
import sys
import numpy as np
import re
import traceback

from tpdin_extractor import TPDINExtractor
from old_extractor import OldExtractor
from blue_extractor import BlueExtractor

# Define directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def convert_numpy_types(obj):
    """Recursively convert numpy/pandas types to Python native types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    else:
        return obj


def parse_anthropological_windows_from_markdown(markdown_path):
    """
    Extract anthropological time windows from the end of a profile markdown file.
    
    Expects a section like:
    ## Anthropological Windows
    - Morning: [240, 540]
    - Afternoon: [540, 900]
    - Evening: [900, 1260]
    - Night: [1260, 1440]
    
    Returns a dictionary mapping period names to (start_minute, end_minute) tuples.
    """
    if not Path(markdown_path).exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
    
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    anthropological_windows = {}
    
    # Pattern: "- {Period}: [{start}, {end}]" within an Anthropological Windows section
    window_pattern = r'-\s+([A-Za-z\s]+):\s*\[(\d+),\s*(\d+)\]'
    
    # Find all time windows
    windows = re.finditer(window_pattern, content)
    
    for window_match in windows:
        period_name = window_match.group(1).strip()
        start_minute = int(window_match.group(2))
        end_minute = int(window_match.group(3))
        anthropological_windows[period_name] = (start_minute, end_minute)
    
    if not anthropological_windows:
        raise ValueError(f"No anthropological windows found in {markdown_path}")
    
    print(f"\n✓ Parsed {len(anthropological_windows)} anthropological time windows from {Path(markdown_path).name}:")
    for period, (start, end) in sorted(anthropological_windows.items()):
        print(f"  - {period}: [{start}, {end}] minutes")
    
    return anthropological_windows


def classify_profile(chaos_index, stacking_index, safety_lights_prob):
    """
    Classify the household profile based on empirical metrics.
    
    Profiles:
    - Profile 4: System Breakers (Nomads/Split-Households) - extreme chaos
    - Profile 3: Extended Hub (Dense Multi-Generational Families) - high device stacking
    - Profile 2: Isolated Elder (Unipersonal/Elderly) - low stacking, high safety lights
    - Profile 1: Agricultural Core (Default) - baseline households
    
    Args:
        chaos_index: MRSD chaos index from structural metrics
        stacking_index: Appliance stacking index percentage (or None if not computed)
        safety_lights_prob: Safety lights probability (midnight-4am)
    
    Returns:
        str: Profile markdown filename
    """
    # Safely handle None stacking index (single appliance systems)
    stacking = stacking_index
    if stacking is None:
        stacking = 0.0
    
    # 1. Isolate the Nomads / Split-Households (Profile 4)
    # The defining signature is extreme temporal absence and chaotic returns.
    if chaos_index >= 2.00:
        return 'profile_4_system_breakers.md'
    
    # 2. Isolate the Dense Multi-Generational Families (Profile 3)
    # Defined by severe simultaneous device usage (Stacking > 25%) and heavy baselines.
    elif stacking >= 25.0:
        return 'profile_3_extended_hub.md'
    
    # 3. Isolate the Unipersonal / Elderly Households (Profile 2)
    # Defined by a physical inability to stack appliances (< 15%), but strong reliance on safety lights.
    elif stacking <= 15.0 and safety_lights_prob >= 0.70:
        return 'profile_2_isolated_elder.md'
    
    # 4. Default to Agricultural Core (Profile 1)
    else:
        return 'profile_1_agricultural_core.md'


def compute_led_time_of_day_probs(hourly_probs, datalogger_type):
    """Compute LED probabilities for specific time windows (morning 4-8, night 18-21)."""
    led_tod_probs = {}
    
    if datalogger_type == 'blue':
        return led_tod_probs  # No LEDs in BLUE
    
    # Define LED appliances based on datalogger type
    if datalogger_type == 'tpdin':
        led_appliances = ['LED_1', 'LED_2']
    else:  # old
        led_appliances = ['LED']
    
    # Define time windows
    morning_hours = list(range(4, 8))  # 4:00-7:59 (4-8)
    night_hours = list(range(18, 21))  # 18:00-20:59 (18-21)
    
    for led in led_appliances:
        morning_probs = []
        night_probs = []
        
        # Collect morning probabilities
        for hour in morning_hours:
            hour_key = f'hour_{hour:02d}'
            if hour_key in hourly_probs:
                prob_key = f'{led}_Prob'
                if prob_key in hourly_probs[hour_key]:
                    morning_probs.append(hourly_probs[hour_key][prob_key])
        
        # Collect night probabilities
        for hour in night_hours:
            hour_key = f'hour_{hour:02d}'
            if hour_key in hourly_probs:
                prob_key = f'{led}_Prob'
                if prob_key in hourly_probs[hour_key]:
                    night_probs.append(hourly_probs[hour_key][prob_key])
        
        # Compute averages for the time windows
        if morning_probs:
            led_tod_probs[f'{led}_morning_prob'] = np.mean(morning_probs)
        if night_probs:
            led_tod_probs[f'{led}_night_prob'] = np.mean(night_probs)
    
    return led_tod_probs


def detect_datalogger_type(filename):
    """Auto-detect datalogger type from filename or column structure."""
    filename_str = str(filename).lower()
    
    if 'blue' in filename_str:
        return 'blue'
    elif 'tpdin' in filename_str:
        return 'tpdin'
    elif 'old' in filename_str:
        return 'old'
    else:
        # Fallback: check columns
        df_sample = pd.read_csv(filename, nrows=1)
        if 'c_cons' in df_sample.columns:
            return 'blue'
        elif 'c_led_1' in df_sample.columns and 'c_led_2' in df_sample.columns:
            return 'tpdin'
        elif 'c_led' in df_sample.columns:
            return 'old'
        else:
            raise ValueError(f"Cannot determine datalogger type for {filename}")


def extract_parameters(filename):
    """Extract all parameters from a single CSV file.
    
    Args:
        filename: Path to the CSV file
    
    The function auto-classifies the household profile based on empirical metrics,
    loads the corresponding markdown profile, and extracts anthropological time windows
    for RAMP parameter extraction.
    """
    print(f"Extracting parameters from {filename.name}...")
    
    try:
        # Detect type and instantiate correct extractor
        datalogger_type = detect_datalogger_type(filename)
        
        if datalogger_type == 'tpdin':
            extractor = TPDINExtractor()
            appliance_count = 3
        elif datalogger_type == 'old':
            extractor = OldExtractor()
            appliance_count = 2
        else:  # blue
            extractor = BlueExtractor()
            appliance_count = 1
        
        # Preprocess
        df = extractor.preprocess(filename)
        
        # Detect power anomalies
        anomaly_report = extractor.detect_power_anomalies(df)
        
        # Extract all metrics
        hardware = extractor.extract_hardware(df)
        
        hourly_data = extractor.extract_hourly_probs(df)
        hourly_probs = hourly_data['hourly_probs']
        peak_hours = hourly_data['peak_hours']
        daily_event_probs = hourly_data['daily_event_probs']
        
        ramp_params = extractor.extract_ramp_params(df)
        
        power_data = extractor.extract_power_variation(df)
        power_variation = power_data['power_variation']
        thermal_p_var = power_data['thermal_p_var']
        
        structural_metrics = extractor.extract_structural_metrics(df)
        reliability_metrics = extractor.extract_reliability_metrics(df)
        
        # Extract stacking index using known hardware specifications for datalogger type
        stacking_metrics = extractor.extract_stacking_index(df, datalogger_type)
        
        # Auto-classify profile and load anthropological time windows
        profile_md_filename = classify_profile(
            structural_metrics['mrsd_chaos_index'],
            stacking_metrics['stacking_index'],
            structural_metrics['safety_lights_probability']
        )
        profile_md_path = PROJECT_ROOT / "data" / "clean" / "profiles" / profile_md_filename
        
        anthropological_windows = None
        if profile_md_path.exists():
            try:
                anthropological_windows = parse_anthropological_windows_from_markdown(profile_md_path)
                print(f"✓ Auto-classified profile: {profile_md_filename}")
            except Exception as e:
                print(f"[!] Could not parse anthropological windows from {profile_md_filename}: {e}")
        else:
            print(f"[!] Auto-classified profile not found: {profile_md_filename}")
        
        # Extract RAMP parameters by period using anthropological windows
        if anthropological_windows:
            ramp_params_by_period = extractor.extract_ramp_params_by_period(df, anthropological_windows)
        else:
            # Fallback to old hardcoded periods if anthropological windows not found
            ramp_params_by_period = extractor.extract_ramp_params_by_period(df)
        
        # Compute LED time-of-day probabilities (morning 4-8, night 18-21)
        led_time_of_day_probs = compute_led_time_of_day_probs(hourly_probs, datalogger_type)
        
        # Pack all parameters
        params = {
            'datalogger_type': datalogger_type,
            'anomaly_report': anomaly_report,
            'hardware': hardware,
            'daily_event_probs': daily_event_probs,
            'hourly_probs': hourly_probs,
            'peak_hours': peak_hours,
            'led_time_of_day_probs': led_time_of_day_probs,
            'power_variation': power_variation,
            'thermal_p_var': thermal_p_var,
            'ramp_params': ramp_params,
            'structural_metrics': structural_metrics,
            'stacking_metrics': stacking_metrics,
            'reliability_metrics': reliability_metrics
        }
        
        user_id = filename.stem.split('_')[-1]
        
        # Print extracted parameters to console
        print(f"\n{'='*70}")
        print(f"USER {user_id} ({datalogger_type.upper()}) - EXTRACTED PARAMETERS")
        print(f"{'='*70}")

        # --- Print the Anthropological Time Windows Used ---
        print(f"\n🕒 ANTHROPOLOGICAL WINDOWS (Time periods used for activity extraction):")
        if anthropological_windows:
            for period, (start_min, end_min) in anthropological_windows.items():
                print(f"   - {period}: [{start_min}, {end_min}] minutes")
        else:
            print("   - Using Legacy Hardcoded Hourly Periods (Morning, Daytime, Evening, Night)")
        # -------------------------------------------
        
        # Print anomaly report prominently
        if anomaly_report['anomaly_count'] > 0:
            print(f"\n⚠️  DATA QUALITY WARNING:")
            print(f"   {anomaly_report['status']}")
            print(f"   Max reading: {anomaly_report['max_power_reading']}W (threshold: {anomaly_report['anomaly_threshold']}W)")
            if 'top_anomalies' in anomaly_report and anomaly_report['top_anomalies']:
                print(f"   Top anomalies:")
                for timestamp, power in anomaly_report['top_anomalies'][:3]:
                    print(f"      {timestamp}: {power:.2f}W")
        else:
            print(f"\n✓ DATA QUALITY: {anomaly_report['status']}")
        
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
        
        if led_time_of_day_probs:
            print(f"\n🌅 LED TIME-OF-DAY PROBABILITIES:")
            for led_key, prob in led_time_of_day_probs.items():
                if 'morning' in led_key:
                    led_name = led_key.split('_')[0]
                    print(f"   {led_name} Morning (04:00-07:59): {prob*100:.1f}%")
            for led_key, prob in led_time_of_day_probs.items():
                if 'night' in led_key:
                    led_name = led_key.split('_')[0]
                    print(f"   {led_name} Night (18:00-20:59): {prob*100:.1f}%")
        
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
            # Only print stored window examples (usually first 10)
            window_idx = 1
            while f'window_{window_idx}' in ramp_data:
                window = ramp_data[f'window_{window_idx}']
                print(f"      Window {window_idx}: {window[0]:.0f} - {window[1]:.0f} minutes")
                window_idx += 1
        
        print(f"\n📊 TIER 2: STRUCTURAL PROFILING & RESILIENCE METRICS:")
        print(f"   Modal Peak Hour: {structural_metrics['modal_peak_hour']:02d}:00")
        print(f"   Safety Lights Probability (midnight-4am): {structural_metrics['safety_lights_probability']*100:.1f}%")
        print(f"   MRSD Chaos Index: {structural_metrics['mrsd_chaos_index']:.3f}")
        print(f"   Overall Mean Power: {structural_metrics['overall_mean_power_W']:.2f} W")
        print(f"   Relative Mean Power by Time-of-Day:")
        for period, rel_power in structural_metrics['relative_mean_power'].items():
            print(f"      {period.capitalize()}: {rel_power:.3f}x overall mean")
        
        print(f"\n🔌 APPLIANCE STACKING INDEX (Simultaneous Multi-Device Usage):")
        print(f"   Devices: {stacking_metrics['appliance_names']}")
        print(f"   Stacking Threshold: {stacking_metrics['stacking_threshold_W']}W")
        if stacking_metrics['stacking_index'] is not None:
            print(f"   Stacking Index: {stacking_metrics['stacking_index']:.1f}% of active time")
            if stacking_metrics['total_active_rows'] > 0:
                print(f"   Events: {stacking_metrics['stacking_events_count']} out of {stacking_metrics['total_active_rows']} active measurements")
                print(f"   Interpretation: {stacking_metrics['stacking_interpretation']}")
            else:
                print(f"   Events: No device activity recorded")
        else:
            print(f"   Stacking Index: Not computed (single appliance system)")
        
        print(f"\n🔋 RELIABILITY METRICS: BLACKOUT ANALYSIS:")
        print(f"   Measurement Duration: {reliability_metrics['num_measurement_days']} days")
        print(f"   Blackout Frequency: {reliability_metrics['bo_freq_events']} events ({reliability_metrics['bo_freq_events_per_100days']:.2f} per 100 days)")
        print(f"   Mean Outage Duration: {reliability_metrics['mean_outage_duration_min']:.1f} minutes")
        print(f"   Reliability Index: {reliability_metrics['ri_percent']:.2f}%")
        print(f"   Climatic Blackouts: {reliability_metrics['climatic_blackout_events']} events ({reliability_metrics['cbr_events_per_100days']:.2f} per 100 days)")
        print(f"   Behavioral Blackouts: {reliability_metrics['behavioral_blackout_events']} events ({reliability_metrics['bbr_events_per_100days']:.2f} per 100 days)")
        
        print(f"\n{'='*70}\n")
        
        # Save JSON - convert numpy types to native Python types first
        params_serializable = convert_numpy_types(params)
        output_json = OUTPUT_DIR / f"empirical_parameters_user_{user_id}.json"
        with open(output_json, 'w') as f:
            json.dump(params_serializable, f, indent=4)
        
        # Save Hourly Matrix
        if datalogger_type == 'tpdin':
            hourly_matrix_data = {'Hour': list(range(24))}
            for appliance in ['LED_1', 'LED_2', 'USB']:
                hourly_matrix_data[appliance] = [hourly_probs[f'hour_{hour:02d}'][f'{appliance}_Prob'] for hour in range(24)]
        elif datalogger_type == 'old':
            hourly_matrix_data = {'Hour': list(range(24))}
            for appliance in ['LED', 'USB']:
                hourly_matrix_data[appliance] = [hourly_probs[f'hour_{hour:02d}'][f'{appliance}_Prob'] for hour in range(24)]
        else:  # blue
            hourly_matrix_data = {'Hour': list(range(24))}
            hourly_matrix_data['CONS'] = [hourly_probs[f'hour_{hour:02d}']['CONS_Prob'] for hour in range(24)]
        
        hourly_matrix_df = pd.DataFrame(hourly_matrix_data)
        output_hourly = OUTPUT_DIR / f"hourly_probabilities_user_{user_id}.csv"
        hourly_matrix_df.to_csv(output_hourly, index=False)
        
        # Save RAMP parameters by period (new method)
        ramp_by_period_serializable = convert_numpy_types(ramp_params_by_period)
        output_ramp_period_json = OUTPUT_DIR / f"ramp_parameters_by_period_user_{user_id}.json"
        with open(output_ramp_period_json, 'w') as f:
            json.dump(ramp_by_period_serializable, f, indent=4)
        
        print(f"✓ User {user_id}: saved to {output_json.name}")
        print(f"✓ User {user_id}: period-based RAMP saved to {output_ramp_period_json.name}")
        
        return {'user_id': user_id, 'file': filename.name, 'params': params, 'datalogger_type': datalogger_type, 'anomaly_report': anomaly_report}
    
    except Exception as e:
        print(f"✗ Error processing {filename.name}: {e}")
        import traceback
        traceback.print_exc()
        return None


def batch_process(input_pattern=None):
    """Batch process all matching CSV files.
    
    Args:
        input_pattern: Glob pattern to filter files
    """
    if not INPUT_DIR.exists():
        print(f"Error: Input directory not found: {INPUT_DIR}")
        sys.exit(1)
    
    csv_files = list(INPUT_DIR.glob(input_pattern)) if input_pattern else list(INPUT_DIR.glob("*.csv"))
    
    # Filter to only include OLD and TPDIN datalogger files (exclude BLUE)
    # BLUE users are excluded from analysis due to single-appliance limitation
    datalogger_files = [f for f in csv_files if any(dtype in f.name for dtype in ['old_', 'tpdin_'])]
    
    if not datalogger_files:
        print("No OLD or TPDIN datalogger CSV files found!")
        sys.exit(1)
        
    print(f"Found {len(datalogger_files)} datalogger file(s) to process (BLUE users excluded)\n")
    
    results = [extract_parameters(f) for f in sorted(datalogger_files)]
    results = [r for r in results if r]
    
    if results:
        summary_data = []
        for result in results:
            row = {
                'user_id': result['user_id'],
                'file': result['file'],
                'datalogger_type': result['datalogger_type'],
                'anomaly_count': result['anomaly_report']['anomaly_count'],
                'anomaly_percentage': result['anomaly_report']['anomaly_percentage'],
                'max_power_reading_W': result['anomaly_report'].get('max_power_reading', 0),
                'anomaly_threshold_W': result['anomaly_report'].get('anomaly_threshold', 0),
                'modal_peak_hour': result['params']['structural_metrics']['modal_peak_hour'],
                'safety_lights_probability': result['params']['structural_metrics']['safety_lights_probability'],
                'mrsd_chaos_index': result['params']['structural_metrics']['mrsd_chaos_index'],
                'overall_mean_power_W': result['params']['structural_metrics']['overall_mean_power_W'],
                'relative_mean_power_morning': result['params']['structural_metrics']['relative_mean_power']['morning'],
                'relative_mean_power_daytime': result['params']['structural_metrics']['relative_mean_power']['daytime'],
                'relative_mean_power_evening': result['params']['structural_metrics']['relative_mean_power']['evening'],
                'relative_mean_power_night': result['params']['structural_metrics']['relative_mean_power']['night'],
                'stacking_index': result['params']['stacking_metrics']['stacking_index'],
                'stacking_threshold_W': result['params']['stacking_metrics']['stacking_threshold_W'],
                'stacking_events_count': result['params']['stacking_metrics']['stacking_events_count'],
                'stacking_total_active_rows': result['params']['stacking_metrics']['total_active_rows'],
                'num_measurement_days': result['params']['reliability_metrics']['num_measurement_days'],
                'bo_freq_events': result['params']['reliability_metrics']['bo_freq_events'],
                'bo_freq_events_per_100days': result['params']['reliability_metrics']['bo_freq_events_per_100days'],
                'mean_outage_duration_min': result['params']['reliability_metrics']['mean_outage_duration_min'],
                'ri_percent': result['params']['reliability_metrics']['ri_percent'],
                'climatic_blackout_events': result['params']['reliability_metrics']['climatic_blackout_events'],
                'behavioral_blackout_events': result['params']['reliability_metrics']['behavioral_blackout_events'],
                'cbr_events_per_100days': result['params']['reliability_metrics']['cbr_events_per_100days'],
                'bbr_events_per_100days': result['params']['reliability_metrics']['bbr_events_per_100days'],
            }
            
            # Add appliance-specific columns based on datalogger type
            hardware = result['params']['hardware']
            for app, wattage in hardware.items():
                row[f'hardware_{app}'] = wattage
            
            daily_probs = result['params']['daily_event_probs']
            for app, prob in daily_probs.items():
                row[f'daily_prob_{app}'] = prob
            
            peak = result['params']['peak_hours']
            for app, info in peak.items():
                row[f'peak_hour_{app}'] = info['hour']
                row[f'peak_prob_{app}'] = info['probability']
            
            thermal = result['params']['thermal_p_var']
            for app, cv in thermal.items():
                row[f'thermal_cv_{app}'] = cv
            
            # Add LED time-of-day probabilities
            led_tod = result['params']['led_time_of_day_probs']
            for led_key, prob in led_tod.items():
                row[f'led_tod_{led_key}'] = prob
            
            # Only include users with computed stacking index (exclude BLUE)
            if result['datalogger_type'] != 'blue':
                summary_data.append(row)
        
        summary_df = pd.DataFrame(summary_data)
        summary_csv = OUTPUT_DIR / "empirical_parameters_summary.csv"
        summary_df.to_csv(summary_csv, index=False)
        print(f"\n✓ Summary saved to: {summary_csv.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract energy parameters from timeseries CSV files (OLD, TPDIN, and BLUE)")
    parser.add_argument("--user", type=str, help="Process specific user (e.g., '74')")
    parser.add_argument("--pattern", type=str, help="Glob pattern to filter files (e.g., '*_user_*.csv')")
    parser.add_argument("--type", type=str, choices=['old', 'tpdin', 'blue'], help="Filter by datalogger type")
    
    args = parser.parse_args()
    
    # Build pattern
    patterns = []
    if args.user:
        patterns.append(f"*_user_{args.user}.csv")
    if args.type:
        patterns.append(f"{args.type}_user_*.csv")
    if args.pattern:
        patterns.append(args.pattern)
    
    if patterns:
        # Use first pattern that matches files
        for pattern in patterns:
            if list(INPUT_DIR.glob(pattern)):
                batch_process(input_pattern=pattern)
                break
    else:
        batch_process()
