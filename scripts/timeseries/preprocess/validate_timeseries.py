"""
Validate calibrated timeseries data WITHOUT removing empty rows.

This script:
1. Validates timestamps are correctly calibrated
2. Analyzes PV generation patterns to confirm calibration
3. KEEPS all rows including empty ones (they represent blackouts)
4. Reports data quality and gaps

Usage:
    python validate_timeseries.py --input tpdin_user_96_calibrated.csv --type tpdin
"""

import pandas as pd
import numpy as np
import argparse
from pathlib import Path

def get_data_columns(datalogger_type):
    """Get measurement column names by datalogger type."""
    if datalogger_type == 'tpdin':
        return ['v_pv', 'v_usb', 'v_led_1', 'v_led_2', 'c_usb', 'c_led_1', 'c_led_2']
    elif datalogger_type == 'old':
        return ['v_pv', 'v_usb', 'v_led', 'c_usb', 'c_led']
    elif datalogger_type == 'blue':
        return ['v_pv', 'v_cons', 'c_cons']
    else:
        raise ValueError(f"Unknown datalogger type: {datalogger_type}")

def detect_datalogger_type(df):
    """Auto-detect datalogger type from columns."""
    cols = [c.lower() for c in df.columns]
    
    if 'c_cons' in cols:
        return 'blue'
    elif 'c_led_1' in cols and 'c_led_2' in cols:
        return 'tpdin'
    elif 'c_led' in cols and 'c_led_1' not in cols:
        return 'old'
    else:
        raise ValueError("Cannot determine datalogger type from columns")

def has_measurement_data(row, data_cols):
    """Check if a row has any actual measurement data."""
    for col in data_cols:
        if col in row.index:
            val = row[col]
            if pd.notna(val) and str(val).strip() != '' and float(val) != 0:
                return True
    return False

def count_empty_rows(df, data_cols):
    """Count rows with no measurements (blackout periods)."""
    empty_rows = ~df.apply(lambda row: has_measurement_data(row, data_cols), axis=1)
    return empty_rows.sum()

def analyze_pv_patterns(df):
    """Analyze PV generation patterns to validate timestamp calibration."""
    df_temp = df.copy()
    df_temp['corrected_timestamp'] = pd.to_datetime(df_temp['corrected_timestamp'], format='mixed', errors='coerce')
    df_temp['hour'] = df_temp['corrected_timestamp'].dt.hour
    df_temp['date'] = df_temp['corrected_timestamp'].dt.date
    
    # Check daytime hours (6am-6pm)
    daytime = df_temp[(df_temp['hour'] >= 6) & (df_temp['hour'] < 18)]
    
    if len(daytime) == 0:
        return {
            'daytime_records': 0,
            'daytime_with_pv': 0,
            'pv_percentage': 0,
            'days_with_sun': 0,
            'avg_max_pv': 0,
            'max_pv': 0,
            'hour_pv_consistency': 'N/A',
            'night_pv_anomalies': 0
        }
    
    # Count records with PV voltage > 2V during daytime
    pv_records = (daytime['v_pv'] > 2).sum()
    
    # Daily statistics
    daily_pv = daytime.groupby('date')['v_pv'].max()
    days_with_sun = (daily_pv > 2).sum()
    
    # Hour-PV consistency check
    hourly_pv = daytime.groupby('hour')['v_pv'].agg(['mean', 'max', 'count'])
    pct_sun_by_hour = (daytime[daytime['v_pv'] > 2].groupby('hour').size() / daytime.groupby('hour').size() * 100).fillna(0)
    
    # Check if PV increases from morning to noon and decreases afternoon
    morning_hours = hourly_pv.loc[6:11, 'mean'].mean() if len(hourly_pv.loc[6:11]) > 0 else 0
    noon_hours = hourly_pv.loc[12:15, 'mean'].mean() if len(hourly_pv.loc[12:15]) > 0 else 0
    afternoon_hours = hourly_pv.loc[16:17, 'mean'].mean() if len(hourly_pv.loc[16:17]) > 0 else 0
    
    # Realistic pattern: noon > morning, afternoon lower
    if noon_hours > morning_hours * 0.8 and (afternoon_hours == 0 or afternoon_hours < noon_hours * 1.2):
        consistency = "Good"
    elif noon_hours > morning_hours * 0.5:
        consistency = "Fair"
    else:
        consistency = "Poor"
    
    # Night PV anomalies (should be near 0 between 6pm-6am)
    nighttime = df_temp[(df_temp['hour'] < 6) | (df_temp['hour'] >= 18)]
    night_anomalies = (nighttime['v_pv'] > 5).sum()  # Unexpected high PV at night
    
    return {
        'daytime_records': len(daytime),
        'daytime_with_pv': pv_records,
        'pv_percentage': round(100 * pv_records / len(daytime), 1) if len(daytime) > 0 else 0,
        'days_with_sun': days_with_sun,
        'avg_max_pv': round(daily_pv.mean(), 2),
        'max_pv': round(daily_pv.max(), 2),
        'hour_pv_consistency': consistency,
        'night_pv_anomalies': night_anomalies
    }

def identify_gaps(df):
    """Identify data gaps larger than 1 hour."""
    df_sorted = df.copy()
    df_sorted['corrected_timestamp'] = pd.to_datetime(df_sorted['corrected_timestamp'], format='mixed', errors='coerce')
    df_sorted = df_sorted.sort_values('corrected_timestamp').reset_index(drop=True)
    df_sorted['time_diff'] = df_sorted['corrected_timestamp'].diff().dt.total_seconds() / 60
    
    gaps = df_sorted[df_sorted['time_diff'] > 60]
    return gaps

def check_time_step_consistency(df):
    """Analyze time_step_min column consistency."""
    if 'time_step_min' not in df.columns:
        return {'status': 'Column not found', 'expected_5min': 0, 'anomalies': 0}
    
    time_steps = df['time_step_min'].dropna()
    
    if len(time_steps) == 0:
        return {'status': 'All empty', 'expected_5min': 0, 'anomalies': 0}
    
    # Check for expected 5-minute steps
    expected_5min = (time_steps == 5.0).sum()
    anomalies = ((time_steps < 4.5) | (time_steps > 5.5)).sum()  # Flag unusual steps
    
    return {
        'status': 'Present',
        'total_records': len(time_steps),
        'expected_5min': expected_5min,
        'expected_pct': round(100 * expected_5min / len(time_steps), 1) if len(time_steps) > 0 else 0,
        'anomalies': anomalies,
        'mean': round(time_steps.mean(), 3),
        'min': round(time_steps.min(), 3),
        'max': round(time_steps.max(), 3)
    }

def check_measurement_ranges(df, data_cols):
    """Check voltage and current measurements for realistic ranges.
    
    Only checks columns that are relevant for this datalogger type.
    """
    issues = {
        'extreme_pv': 0,
        'extreme_usb': 0,
        'extreme_led': 0,
        'extreme_current': 0,
        'negative_values': 0
    }
    
    # Check PV voltage (typical range 0-25V for solar panels) - all types have this
    if 'v_pv' in data_cols and 'v_pv' in df.columns:
        issues['extreme_pv'] = ((df['v_pv'] > 25) | (df['v_pv'] < -1)).sum()
    
    # Check USB voltage (should be around 5V, allow 4-6V tolerance) - TPDIN and OLD only
    if 'v_usb' in data_cols and 'v_usb' in df.columns:
        issues['extreme_usb'] = ((df['v_usb'] > 6) | ((df['v_usb'] < 3) & (df['v_usb'] > 0))).sum()
    
    # Check LED voltages (should be around 3.3V or similar) - TPDIN and OLD only
    if any('v_led' in col for col in data_cols):
        led_cols = [c for c in df.columns if 'v_led' in c and c in data_cols]
        for col in led_cols:
            issues['extreme_led'] += ((df[col] > 5) | ((df[col] < 2) & (df[col] > 0))).sum()
    
    # Check currents (should be positive) - all types
    current_cols = [c for c in data_cols if c.startswith('c_')]
    for col in current_cols:
        if col in df.columns:
            issues['negative_values'] += (df[col] < 0).sum()
            issues['extreme_current'] += (df[col] > 5).sum()  # > 5A is unusual
    
    return issues

def check_timestamp_continuity(df):
    """Check if timestamps are monotonically increasing."""
    if 'corrected_timestamp' not in df.columns:
        return {'status': 'Column not found', 'regressions': 0}
    
    df_temp = df.copy()
    df_temp['corrected_timestamp'] = pd.to_datetime(df_temp['corrected_timestamp'], format='mixed', errors='coerce')
    
    # Check for backwards jumps
    ts_diff = df_temp['corrected_timestamp'].diff()
    regressions = (ts_diff < pd.Timedelta(0)).sum()
    
    # Check for huge forward jumps (> 1 week)
    huge_jumps = (ts_diff > pd.Timedelta(days=7)).sum()
    
    return {
        'status': 'OK' if regressions == 0 else 'ISSUES',
        'regressions': regressions,
        'huge_jumps': huge_jumps
    }

def analyze_blackout_patterns(df, data_cols):
    """Analyze blackout patterns to identify realistic outages."""
    df_temp = df.copy()
    df_temp['corrected_timestamp'] = pd.to_datetime(df_temp['corrected_timestamp'], format='mixed', errors='coerce')
    df_temp['has_data'] = df_temp.apply(lambda row: has_measurement_data(row, data_cols), axis=1)
    
    # Identify blackout periods
    df_temp['blackout_group'] = (df_temp['has_data'] != df_temp['has_data'].shift()).cumsum()
    blackout_periods = df_temp[~df_temp['has_data']].groupby('blackout_group').agg({
        'corrected_timestamp': ['min', 'max', 'count']
    })
    
    if len(blackout_periods) == 0:
        return {
            'total_blackouts': 0,
            'avg_blackout_duration_min': 0,
            'max_blackout_duration_min': 0,
            'anomalous_blackouts': 0
        }
    
    blackout_periods.columns = ['start', 'end', 'count']
    blackout_periods['duration_min'] = (blackout_periods['end'] - blackout_periods['start']).dt.total_seconds() / 60
    
    # Flag anomalous blackouts (> 7 days at a time, which is suspicious)
    anomalous = (blackout_periods['duration_min'] > 7 * 24 * 60).sum()
    
    return {
        'total_blackouts': len(blackout_periods),
        'avg_blackout_duration_min': round(blackout_periods['duration_min'].mean(), 1),
        'max_blackout_duration_min': round(blackout_periods['duration_min'].max(), 1),
        'anomalous_blackouts': anomalous
    }

def validate_timeseries(input_file, datalogger_type=None):
    """
    Validate timeseries data. Keeps all rows including empty ones.
    
    Args:
        input_file: Path to CSV file
        datalogger_type: 'tpdin', 'old', or 'blue' (auto-detected if None)
    
    Returns:
        dict with validation statistics
    """
    print(f"Reading {input_file.name}...")
    df = pd.read_csv(input_file)
    
    total_rows = len(df)
    print(f"  Total rows: {total_rows:,}")
    
    # Auto-detect type if not provided
    if datalogger_type is None:
        datalogger_type = detect_datalogger_type(df)
    
    data_cols = get_data_columns(datalogger_type)
    print(f"  Datalogger type: {datalogger_type.upper()}")
    
    # Count empty vs full rows
    print(f"\n{'─'*70}")
    print("Data Completeness:")
    print(f"{'─'*70}")
    
    empty_count = count_empty_rows(df, data_cols)
    full_count = total_rows - empty_count
    
    print(f"  Rows with measurements: {full_count:,} ({100*full_count/total_rows:.1f}%)")
    print(f"  Rows with no data (blackouts): {empty_count:,} ({100*empty_count/total_rows:.1f}%)")
    
    # PV Pattern Analysis
    print(f"\n{'─'*70}")
    print("PV Generation Analysis (Timestamp Validation):")
    print(f"{'─'*70}")
    
    pv_stats = analyze_pv_patterns(df)
    print(f"  Daytime records (6am-6pm): {pv_stats['daytime_records']:,}")
    print(f"  Records with PV > 2V: {pv_stats['daytime_with_pv']:,} ({pv_stats['pv_percentage']:.1f}%)")
    print(f"  Days with sun detected: {pv_stats['days_with_sun']}")
    print(f"  Avg max daily PV: {pv_stats['avg_max_pv']} V")
    print(f"  Peak PV voltage: {pv_stats['max_pv']} V")
    print(f"  Hour-PV Consistency: {pv_stats['hour_pv_consistency']}")
    if pv_stats['night_pv_anomalies'] > 0:
        print(f"  ⚠️  Night PV anomalies: {pv_stats['night_pv_anomalies']} (unexpected high PV after 6pm/before 6am)")
    
    # Timestamp Analysis
    print(f"\n{'─'*70}")
    print("Timestamp Validation:")
    print(f"{'─'*70}")
    
    df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'], format='mixed', errors='coerce')
    date_start = df['corrected_timestamp'].min()
    date_end = df['corrected_timestamp'].max()
    date_range = date_end - date_start
    
    print(f"  Start: {date_start}")
    print(f"  End: {date_end}")
    print(f"  Duration: {date_range.days} days, {date_range.seconds//3600} hours")
    
    # Gap Analysis
    print(f"\n{'─'*70}")
    print("Data Gaps (> 60 minutes):")
    print(f"{'─'*70}")
    
    gaps = identify_gaps(df)
    
    if len(gaps) > 0:
        print(f"  Found: {len(gaps)} gaps")
        for idx, (i, row) in enumerate(gaps.head(5).iterrows()):
            gap_min = row['time_diff']
            ts = row['corrected_timestamp']
            hours = gap_min / 60
            days = hours / 24
            if days >= 1:
                print(f"    • {gap_min:.0f} min ({days:.1f} days) at {ts}")
            elif hours >= 1:
                print(f"    • {gap_min:.0f} min ({hours:.1f} hours) at {ts}")
            else:
                print(f"    • {gap_min:.0f} min at {ts}")
        if len(gaps) > 5:
            print(f"    ... and {len(gaps) - 5} more")
    else:
        print(f"  ✓ No gaps > 60 minutes detected")
    
    # Time Step Consistency Check
    print(f"\n{'─'*70}")
    print("Time Step Consistency:")
    print(f"{'─'*70}")
    
    time_step_check = check_time_step_consistency(df)
    if time_step_check['status'] == 'Present':
        print(f"  Expected 5-min steps: {time_step_check['expected_5min']:,} ({time_step_check['expected_pct']:.1f}%)")
        if time_step_check['anomalies'] > 0:
            print(f"  ⚠️  Anomalous steps: {time_step_check['anomalies']}")
        print(f"  Range: {time_step_check['min']} - {time_step_check['max']} min (mean: {time_step_check['mean']})")
    else:
        print(f"  {time_step_check['status']}")
    
    # Timestamp Continuity Check
    print(f"\n{'─'*70}")
    print("Timestamp Continuity:")
    print(f"{'─'*70}")
    
    continuity_check = check_timestamp_continuity(df)
    if continuity_check['regressions'] > 0:
        print(f"  ⚠️  ISSUE: {continuity_check['regressions']} timestamp regressions (backward jumps)")
    else:
        print(f"  ✓ All timestamps move forward chronologically")
    
    if continuity_check['huge_jumps'] > 0:
        print(f"  ⚠️  WARNING: {continuity_check['huge_jumps']} huge forward jumps (> 7 days)")
    
    # Measurement Ranges Check
    print(f"\n{'─'*70}")
    print("Measurement Ranges (Sanity Check):")
    print(f"{'─'*70}")
    
    range_check = check_measurement_ranges(df, data_cols)
    issues_found = False
    if range_check['extreme_pv'] > 0:
        print(f"  ⚠️  Extreme PV values: {range_check['extreme_pv']}")
        issues_found = True
    if range_check['extreme_usb'] > 0:
        print(f"  ⚠️  Extreme USB voltage: {range_check['extreme_usb']}")
        issues_found = True
    if range_check['extreme_led'] > 0:
        print(f"  ⚠️  Extreme LED voltage: {range_check['extreme_led']}")
        issues_found = True
    if range_check['extreme_current'] > 0:
        print(f"  ⚠️  High currents (>5A): {range_check['extreme_current']}")
        issues_found = True
    if range_check['negative_values'] > 0:
        print(f"  ⚠️  Negative current values: {range_check['negative_values']}")
        issues_found = True
    if not issues_found:
        print(f"  ✓ All measurements within reasonable ranges")
    
    # Blackout Pattern Analysis
    print(f"\n{'─'*70}")
    print("Blackout Pattern Analysis:")
    print(f"{'─'*70}")
    
    blackout_check = analyze_blackout_patterns(df, data_cols)
    if blackout_check['total_blackouts'] > 0:
        print(f"  Total blackout periods: {blackout_check['total_blackouts']}")
        print(f"  Avg duration: {blackout_check['avg_blackout_duration_min']:.0f} min")
        print(f"  Max duration: {blackout_check['max_blackout_duration_min']:.0f} min")
        if blackout_check['anomalous_blackouts'] > 0:
            print(f"  ⚠️  Anomalous blackouts (>7 days): {blackout_check['anomalous_blackouts']}")
    else:
        print(f"  No blackout periods detected")
    
    # Quality Assessment
    print(f"\n{'─'*70}")
    print("Calibration Quality Assessment:")
    print(f"{'─'*70}")
    
    if pv_stats['pv_percentage'] < 5:
        print(f"  ⚠️  CRITICAL: Very low PV during daytime ({pv_stats['pv_percentage']:.1f}%)")
        print(f"     → Timestamps may be incorrectly calibrated")
        quality = "POOR"
    elif pv_stats['pv_percentage'] < 30:
        print(f"  ⚠️  WARNING: Low PV during daytime ({pv_stats['pv_percentage']:.1f}%)")
        print(f"     → Possible calibration issues or cloudy climate")
        quality = "FAIR"
    else:
        print(f"  ✓ Good PV pattern: {pv_stats['pv_percentage']:.1f}% of daytime hours have sun")
        print(f"    Timestamps appear correctly calibrated")
        quality = "GOOD"
    
    return {
        'input_file': input_file.name,
        'total_rows': total_rows,
        'full_rows': full_count,
        'empty_rows': empty_count,
        'datalogger_type': datalogger_type,
        'pv_stats': pv_stats,
        'date_start': str(date_start),
        'date_end': str(date_end),
        'num_gaps': len(gaps),
        'time_step_check': time_step_check,
        'continuity_check': continuity_check,
        'range_check': range_check,
        'blackout_check': blackout_check,
        'quality': quality
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate calibrated timeseries data (keeps all rows including blackouts)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_timeseries.py --input tpdin_user_96_calibrated.csv
  python validate_timeseries.py --input data/clean/timeseries/tpdin_user_96_calibrated.csv --type tpdin
        """
    )
    
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--type", type=str, choices=['old', 'tpdin', 'blue'], 
                        help="Datalogger type (auto-detect if not specified)")
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    
    if not input_file.is_absolute():
        # Try from default directory
        input_file = Path("/home/claudia/Documents/raqaypampa_research/data/clean/timeseries") / input_file
    
    if not input_file.exists():
        print(f"❌ Error: File not found: {input_file}")
        exit(1)
    
    # Run validation
    print(f"\n{'='*70}")
    print("TIMESERIES CALIBRATION VALIDATION")
    print(f"{'='*70}\n")
    
    stats = validate_timeseries(input_file, args.type)
    
    print(f"\n{'='*70}")
    print("✓ SUMMARY")
    print(f"{'='*70}")
    print(f"  File: {stats['input_file']}")
    print(f"  Total rows: {stats['total_rows']:,}")
    print(f"    • With data: {stats['full_rows']:,}")
    print(f"    • Blackout (empty): {stats['empty_rows']:,}")
    print(f"  Data period: {stats['date_start']} to {stats['date_end']}")
    print(f"  Data gaps: {stats['num_gaps']} gaps > 60 min")
    print(f"  Calibration Quality: {stats['quality']}")
    print(f"  PV pattern: {stats['pv_stats']['pv_percentage']:.1f}% daytime with sun")
    print(f"{'='*70}\n")
