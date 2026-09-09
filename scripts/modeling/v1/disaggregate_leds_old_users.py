"""
Script 3: NILM Disaggregation of LED1 and LED2 for OLD Users (NumPy-only version)
==================================================================================

This simplified version uses only NumPy (no sklearn/pandas dependencies).
Uses power-based thresholding to disaggregate LED1 and LED2.
"""

import numpy as np
from pathlib import Path
import json
import csv
from collections import defaultdict

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Nominal power values for OLD user LEDs
LED1_NOMINAL = 2.0  # Watts
LED2_NOMINAL = 3.0  # Watts

# OLD user IDs
OLD_USER_IDS = [63, 64, 69, 72, 83, 84]

def read_csv_simple(filepath):
    """Read CSV file with basic Python (no pandas)"""
    data = {'headers': None, 'rows': []}
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                data['headers'] = row
            else:
                data['rows'].append(row)
    return data

def calculate_led_power(v_led, c_led):
    """Calculate LED power: P = V * I"""
    power = v_led * np.abs(c_led)
    power[power < 0.1] = 0  # Threshold out noise
    return power

def disaggregate_by_power_thresholds(led_power):
    """
    Disaggregate LED states using power thresholds.
    
    States:
    - 0W-0.5W: Both OFF
    - 0.5W-2.5W: LED1 only
    - 2.5W-3.5W: LED2 only
    - 3.5W-5.5W: Both ON
    """
    led1_on = np.zeros_like(led_power, dtype=int)
    led2_on = np.zeros_like(led_power, dtype=int)
    state = np.zeros_like(led_power, dtype=int)
    
    # Classify based on power ranges
    for i, p in enumerate(led_power):
        if p < 0.5:
            state[i] = 0  # Both OFF
            led1_on[i] = 0
            led2_on[i] = 0
        elif p < 2.5:
            state[i] = 1  # LED1 only
            led1_on[i] = 1
            led2_on[i] = 0
        elif p < 3.5:
            state[i] = 2  # LED2 only
            led1_on[i] = 0
            led2_on[i] = 1
        else:  # p >= 3.5
            state[i] = 3  # Both ON
            led1_on[i] = 1
            led2_on[i] = 1
    
    return led1_on, led2_on, state

def process_old_user(user_id):
    """Main processing pipeline for a single OLD user."""
    print(f"\n{'='*70}")
    print(f"Processing OLD User {user_id}")
    print(f"{'='*70}")
    
    # Load CSV
    csv_file = DATA_DIR / f"old_user_{user_id}.csv"
    if not csv_file.exists():
        print(f"[-] File not found: {csv_file}")
        return None
    
    print(f"[*] Loading {csv_file.name}...")
    data = read_csv_simple(csv_file)
    
    # Find column indices
    headers = data['headers']
    try:
        v_led_idx = headers.index('v_led_1')
        c_led_idx = headers.index('c_led')
        time_idx = headers.index('corrected_timestamp')
    except ValueError as e:
        print(f"[-] Column not found: {e}")
        return None
    
    # Parse data (skip rows with missing values)
    n_rows = len(data['rows'])
    print(f"    Total rows: {n_rows}")
    
    v_led_list, c_led_list, timestamps = [], [], []
    for row in data['rows']:
        try:
            v = float(row[v_led_idx])
            c = float(row[c_led_idx])
            ts = row[time_idx]
            if v and c and ts:  # Skip empty values
                v_led_list.append(v)
                c_led_list.append(c)
                timestamps.append(ts)
        except (ValueError, IndexError):
            continue
    
    v_led = np.array(v_led_list)
    c_led = np.array(c_led_list)
    print(f"    Valid rows: {len(v_led)}")
    
    # Calculate LED power
    print("[*] Calculating LED power...")
    led_power = calculate_led_power(v_led, c_led)
    
    print(f"    LED Power stats:")
    print(f"      Mean: {np.mean(led_power):.3f}W")
    print(f"      Max:  {np.max(led_power):.3f}W")
    print(f"      Std:  {np.std(led_power):.3f}W")
    
    # Disaggregate
    print("[*] Disaggregating LED states...")
    led1_on, led2_on, state = disaggregate_by_power_thresholds(led_power)
    
    # Extract date and hour from timestamp
    dates = []
    hours = []
    for ts_str in timestamps:
        try:
            # Parse "2023-04-26 14:24:57" format
            date_part = ts_str.split(' ')[0]
            time_part = ts_str.split(' ')[1]
            hour = int(time_part.split(':')[0])
            dates.append(date_part)
            hours.append(hour)
        except:
            dates.append("unknown")
            hours.append(-1)
    
    hours = np.array(hours)
    
    # =====================================================================
    # HOURLY PROBABILITIES
    # =====================================================================
    print("[*] Computing HOURLY probabilities...")
    hourly_probs = defaultdict(lambda: {'led1': [], 'led2': [], 'both': [], 'power': []})
    
    for h, l1, l2, p in zip(hours, led1_on, led2_on, led_power):
        if h >= 0:
            hourly_probs[h]['led1'].append(l1)
            hourly_probs[h]['led2'].append(l2)
            hourly_probs[h]['both'].append(l1 * l2)
            hourly_probs[h]['power'].append(p)
    
    hourly_table = []
    for h in sorted(hourly_probs.keys()):
        data = hourly_probs[h]
        hourly_table.append({
            'hour': h,
            'LED1_Prob': np.mean(data['led1']) if data['led1'] else 0,
            'LED2_Prob': np.mean(data['led2']) if data['led2'] else 0,
            'Both_ON_Prob': np.mean(data['both']) if data['both'] else 0,
            'Power_Mean': np.mean(data['power']) if data['power'] else 0,
            'Power_Max': np.max(data['power']) if data['power'] else 0,
            'Samples': len(data['led1'])
        })
    
    # =====================================================================
    # DAILY PROBABILITIES
    # =====================================================================
    print("[*] Computing DAILY probabilities...")
    daily_probs = defaultdict(lambda: {'led1': [], 'led2': [], 'both': []})
    
    for d, l1, l2 in zip(dates, led1_on, led2_on):
        if d != "unknown":
            daily_probs[d]['led1'].append(l1)
            daily_probs[d]['led2'].append(l2)
            daily_probs[d]['both'].append(l1 * l2)
    
    daily_table = []
    for d in sorted(daily_probs.keys()):
        data = daily_probs[d]
        daily_table.append({
            'date': d,
            'LED1_Prob': np.mean(data['led1']) if data['led1'] else 0,
            'LED2_Prob': np.mean(data['led2']) if data['led2'] else 0,
            'Stacking_Prob': np.mean(data['both']) if data['both'] else 0
        })
    
    # =====================================================================
    # SUMMARY STATISTICS
    # =====================================================================
    print("\n[+] SUMMARY STATISTICS:")
    led1_overall = np.mean(led1_on)
    led2_overall = np.mean(led2_on)
    both_overall = np.mean(led1_on * led2_on)
    
    print(f"\n    Overall Probabilities:")
    print(f"      LED1 ON: {led1_overall:.1%}")
    print(f"      LED2 ON: {led2_overall:.1%}")
    print(f"      Both ON: {both_overall:.1%}")
    
    state_dist = np.bincount(state, minlength=4) / len(state)
    print(f"\n    State Distribution:")
    print(f"      Both OFF:    {state_dist[0]:.1%}")
    print(f"      LED1 only:   {state_dist[1]:.1%}")
    print(f"      LED2 only:   {state_dist[2]:.1%}")
    print(f"      Both ON:     {state_dist[3]:.1%}")
    
    days_used = sum(1 for d in daily_table if d['LED1_Prob'] > 0.01 or d['LED2_Prob'] > 0.01)
    print(f"\n    Usage Patterns:")
    print(f"      Days used: {days_used} / {len(daily_table)}")
    print(f"      Avg daily stacking: {np.mean([d['Stacking_Prob'] for d in daily_table]):.1%}")
    
    # =====================================================================
    # SAVE OUTPUTS
    # =====================================================================
    print("\n[*] Saving outputs...")
    
    # Hourly CSV
    hourly_out = OUTPUT_DIR / f"led_disaggregation_hourly_user_{user_id}.csv"
    with open(hourly_out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['hour', 'LED1_Prob', 'LED2_Prob', 'Both_ON_Prob', 'Power_Mean', 'Power_Max', 'Samples'])
        writer.writeheader()
        writer.writerows(hourly_table)
    print(f"    ✓ {hourly_out.name}")
    
    # Daily CSV
    daily_out = OUTPUT_DIR / f"led_disaggregation_daily_user_{user_id}.csv"
    with open(daily_out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'LED1_Prob', 'LED2_Prob', 'Stacking_Prob'])
        writer.writeheader()
        writer.writerows(daily_table)
    print(f"    ✓ {daily_out.name}")
    
    # Summary JSON
    summary = {
        "user_id": user_id,
        "measurement_period_days": len(daily_table),
        "led1_nominal_power": LED1_NOMINAL,
        "led2_nominal_power": LED2_NOMINAL,
        "overall_probabilities": {
            "led1_on": float(led1_overall),
            "led2_on": float(led2_overall),
            "both_on": float(both_overall)
        },
        "state_distribution": {
            "both_off": float(state_dist[0]),
            "led1_only": float(state_dist[1]),
            "led2_only": float(state_dist[2]),
            "both_on": float(state_dist[3])
        },
        "daily_usage": {
            "days_used": days_used,
            "total_days": len(daily_table),
            "avg_stacking_prob": float(np.mean([d['Stacking_Prob'] for d in daily_table]))
        }
    }
    
    summary_out = OUTPUT_DIR / f"led_disaggregation_summary_user_{user_id}.json"
    with open(summary_out, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"    ✓ {summary_out.name}")
    
    return summary

def main():
    print("\n" + "="*70)
    print("NILM DISAGGREGATION OF LED1 & LED2 FOR OLD USERS")
    print("="*70)
    
    all_summaries = {}
    
    for user_id in OLD_USER_IDS:
        summary = process_old_user(user_id)
        if summary:
            all_summaries[f"user_{user_id}"] = summary
    
    # Save consolidated summary
    consolidated_out = OUTPUT_DIR / "led_disaggregation_all_users_summary.json"
    with open(consolidated_out, 'w') as f:
        json.dump(all_summaries, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[+] Disaggregation complete!")
    print(f"    All outputs saved to: {OUTPUT_DIR}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
