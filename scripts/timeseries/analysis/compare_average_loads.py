"""
Multi-User Average Load Curve Comparator

Dynamically loads timeseries data across any hardware logger type (TPDIN, BLUE, OLD).
Calculates the 15-minute binned average load curve for each user.
Overlays multiple users on a single plot for comparative structural analysis.

Usage:
    # Compare two users using all available data
    python compare_average_loads.py --users 74 82

    # Compare five users, but strictly limit the average to the first 30 days of data
    python compare_average_loads.py --users 74 82 12 5 101 --days 30
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define paths matching project structure
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"
FIGURES_DIR = PROJECT_ROOT / "results" / "timeseries" / "figures"

# Ensure output directories exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_user_data(user_id):
    """Load measured data dynamically for TPDIN, BLUE, or OLD loggers."""
    
    # 1. Auto-detect the correct hardware logger file
    possible_prefixes = ["tpdin", "blue", "old"]
    data_file = None
    logger_type = "UNKNOWN"
    
    for prefix in possible_prefixes:
        temp_file = INPUT_DIR / f"{prefix}_user_{user_id}.csv"
        if temp_file.exists():
            data_file = temp_file
            logger_type = prefix.upper()
            break
            
    if data_file is None:
        print(f"[-] Warning: Data file not found for User {user_id}. Skipping.")
        return None, None
    
    df = pd.read_csv(data_file)
    df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    
    # 2. Safely calculate total power (Hardware Agnostic)
    zero_series = pd.Series(0.0, index=df.index)
    v_usb = df.get('v_usb', zero_series)
    c_usb = df.get('c_usb', zero_series)
    v_led_1 = df.get('v_led_1', df.get('v_led', zero_series))
    c_led_1 = df.get('c_led_1', df.get('c_led', zero_series))
    v_led_2 = df.get('v_led_2', zero_series)
    c_led_2 = df.get('c_led_2', zero_series)
    
    p_led_1 = (v_led_1 * c_led_1).clip(lower=0)
    p_led_2 = (v_led_2 * c_led_2).clip(lower=0)
    p_usb = (v_usb * c_usb).clip(lower=0)
    
    df['p_total'] = p_led_1 + p_led_2 + p_usb
    
    # 3. Extract temporal features
    df['date_only'] = df['timestamp'].dt.date
    df['time_decimal'] = df['timestamp'].dt.hour + df['timestamp'].dt.minute / 60.0
    
    print(f"[+] Loaded User {user_id} ({logger_type} logger) - {len(df)} rows.")
    return df, logger_type


def process_average_curve(df, num_days=None):
    """Filters by days and calculates the 15-minute binned average."""
    
    if df is None or df.empty:
        return None
        
    # Filter to first N days if requested
    if num_days is not None and num_days > 0:
        unique_dates = sorted(df['date_only'].unique())
        if len(unique_dates) > num_days:
            active_dates = unique_dates[:num_days]
            df = df[df['date_only'].isin(active_dates)]
            print(f"    -> Filtered to first {num_days} days.")
        else:
            print(f"    -> Note: Requested {num_days} days, but only {len(unique_dates)} days available.")
            
    # Create standardized time bins (15-minute intervals) for smooth averaging
    bins = np.arange(0, 24.25, 0.25)
    df['time_bin'] = pd.cut(df['time_decimal'], bins, labels=bins[:-1])
    
    # Calculate the mean power for each 15-minute block
    avg_profile = df.groupby('time_bin', observed=True)['p_total'].mean().fillna(0)
    
    return avg_profile


def plot_comparative_curves(user_profiles, num_days):
    """Generates a single plot overlaying all successfully processed users."""
    
    if not user_profiles:
        print("[-] No valid user data to plot. Exiting.")
        sys.exit(1)
        
    print("\n[*] Generating comparative plot...")
    plt.figure(figsize=(12, 6))
    
    # Generate a dynamic color palette based on how many users are selected
    colors = plt.cm.tab10(np.linspace(0, 1, len(user_profiles)))
    
    max_power = 0
    
    # FIXED: Correctly unpack the dictionary key (user_id) and the tuple value (label, profile)
    for idx, (user_id, (label, profile)) in enumerate(user_profiles.items()):
        time_values = profile.index.astype(float)
        power_values = profile.values
        
        # Track max power to set Y-axis limit cleanly
        if max(power_values) > max_power:
            max_power = max(power_values)
            
        plt.plot(time_values, power_values, linewidth=2.5, color=colors[idx], label=label)
        # Add a light fill under the curve to make it look nicer
        plt.fill_between(time_values, power_values, alpha=0.05, color=colors[idx])

    # Dynamic Title
    day_text = f" (First {num_days} Days)" if num_days else " (All Available Data)"
    plt.title(f'Comparative Average Daily Load Curves{day_text}', fontsize=14, fontweight='bold')
    
    # Formatting
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('Average Power Demand (W)', fontsize=12)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlim(0, 24)
    
    # Give a little headroom above the highest peak
    plt.ylim(0, max_power * 1.2)
    
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
    plt.tight_layout()
    
    # Generate dynamic filename based on users included
    user_str = "_".join([str(u) for u in user_profiles.keys()])
    if len(user_str) > 30: 
        user_str = f"{len(user_profiles)}_users" # Prevent massive filenames if comparing 20+ users
        
    fig_file = FIGURES_DIR / f"comparison_load_curves_U{user_str}.png"
    plt.savefig(fig_file, dpi=200, bbox_inches='tight')
    print(f"✓ Saved plot successfully to: {fig_file.name}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Compare Average Load Curves Across Multiple Users")
    
    # nargs='+' allows accepting a list of inputs: --users 74 82 12
    parser.add_argument("--users", type=int, nargs='+', required=True, 
                        help="List of User IDs to compare separated by spaces (e.g., --users 74 82 12)")
    parser.add_argument("--days", type=int, default=None, 
                        help="Limit average calculation to the first N days of available data")
                        
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print(" MULTI-USER LOAD COMPARATOR")
    print("="*70)
    
    user_profiles = {}
    
    # Process each user
    for user_id in args.users:
        df, logger_type = load_user_data(user_id)
        
        if df is not None:
            avg_profile = process_average_curve(df, num_days=args.days)
            if avg_profile is not None:
                # Save it in a dictionary with a clean label for the legend
                label = f"User {user_id} ({logger_type})"
                user_profiles[user_id] = (label, avg_profile)
                
    # Generate the final plot
    plot_comparative_curves(user_profiles, num_days=args.days)


if __name__ == "__main__":
    main()