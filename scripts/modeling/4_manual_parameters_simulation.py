"""
Script to manually set RAMP parameters and simulate load profiles.
Allows easy parameter tweaking and comparison with real data.

Parameters:
    thermal_p_var: Power variability (Coefficient of Variation) for thermal dynamics
                   Set at appliance level (applies to all periods) or per-period level

Usage:
    # Run with default parameters from config file
    python 4_manual_parameters_simulation.py --user 74 --days 5 --config manual_params.json
    
    # Override individual parameters via CLI
    python 4_manual_parameters_simulation.py --user 74 --days 5 \\
        --occasional-use LED_1_evening_school_cooking:0.95 \\
        --thermal-p-var LED_1:0.15
"""

import json
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Suppress RAMP warnings
warnings.filterwarnings('ignore')

try:
    from ramp import UseCase, User, Appliance
except ImportError:
    print("Error: RAMP library not found.")
    print("  Install with: pip install rampdemand")
    sys.exit(1)

# Define paths matching the project structure
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR_REAL = PROJECT_ROOT / "data" / "clean" / "timeseries"
OUTPUT_DIR = SCRIPT_DIR / "output"
FIGURES_DIR = PROJECT_ROOT / "results" / "timeseries" / "figures"
PARAMS_DIR = SCRIPT_DIR / "manual_parameters"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
PARAMS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# Default Parameter Templates for All 12 Appliance-Period Combinations
# ============================================================================

DEFAULT_PARAMETERS = {
    "LED_1": {
        "power_W": 2.56,
        "thermal_p_var": 0.10,  # Power variability (CV) for thermal dynamics
        "periods": {
            "morning_prep": {
                "occasional_use": 0.39,
                "avg_minutes": 35.4,
                "std_minutes": 63.2,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.10,  # Power variability (CV) for this period
                "windows": [[240, 600]],  # 4-10h (optional: defaults shown)
            },
            "daytime": {
                "occasional_use": 0.10,
                "avg_minutes": 5.8,
                "std_minutes": 25.8,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.10,
                "windows": [[600, 1020]],  # 10-17h
            },
            "evening_school_cooking": {
                "occasional_use": 0.99,
                "avg_minutes": 105.6,
                "std_minutes": 61.7,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.10,
                "windows": [[1020, 1440]],  # 17-24h
            },
            "night_security": {
                "occasional_use": 0.13,
                "avg_minutes": 3.0,
                "std_minutes": 19.1,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.10,
                "windows": [[0, 240]],  # 0-4h
            },
        },
    },
    "LED_2": {
        "power_W": 2.60,
        "thermal_p_var": 0.12,  # Power variability (CV) for thermal dynamics
        "periods": {
            "morning_prep": {
                "occasional_use": 0.48,
                "avg_minutes": 59.8,
                "std_minutes": 81.5,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.12,
                "windows": [[240, 600]],
            },
            "daytime": {
                "occasional_use": 0.15,
                "avg_minutes": 14.7,
                "std_minutes": 53.8,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.12,
                "windows": [[600, 1020]],
            },
            "evening_school_cooking": {
                "occasional_use": 0.98,
                "avg_minutes": 118.0,
                "std_minutes": 63.5,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.12,
                "windows": [[1020, 1440]],
            },
            "night_security": {
                "occasional_use": 0.18,
                "avg_minutes": 9.6,
                "std_minutes": 30.1,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.12,
                "windows": [[0, 240]],
            },
        },
    },
    "USB": {
        "power_W": 1.88,
        "thermal_p_var": 0.15,  # Power variability (CV) for thermal dynamics
        "periods": {
            "morning_prep": {
                "occasional_use": 0.79,
                "avg_minutes": 95.9,
                "std_minutes": 89.7,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.15,
                "windows": [[240, 600]],
            },
            "daytime": {
                "occasional_use": 0.78,
                "avg_minutes": 166.8,
                "std_minutes": 121.7,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.15,
                "windows": [[600, 1020]],
            },
            "evening_school_cooking": {
                "occasional_use": 0.77,
                "avg_minutes": 93.1,
                "std_minutes": 83.2,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.15,
                "windows": [[1020, 1440]],
            },
            "night_security": {
                "occasional_use": 0.46,
                "avg_minutes": 92.4,
                "std_minutes": 109.5,
                "rand_var": 0.30,
                "func_cycle": 5,
                "thermal_p_var": 0.15,
                "windows": [[0, 240]],
            },
        },
    },
}

# Default time windows for each period (in minutes from midnight)
# These can be overridden in the JSON config
DEFAULT_PERIOD_WINDOWS = {
    "morning_prep": [[240, 600]],  # 4:00-10:00 (4-10h)
    "daytime": [[600, 1020]],  # 10:00-17:00 (10-17h)
    "evening_school_cooking": [[1020, 1440]],  # 17:00-24:00 (17-24h)
    "night_security": [[0, 240]],  # 00:00-04:00 (0-4h)
}


# ============================================================================
# Functions
# ============================================================================

def create_example_config():
    """Create an example manual parameters config file."""
    config_file = PARAMS_DIR / "manual_params_example.json"
    
    with open(config_file, 'w') as f:
        json.dump(DEFAULT_PARAMETERS, f, indent=2)
    
    print(f"✓ Example config created: {config_file}")
    print("  Edit this file to manually adjust parameters, then run:")
    print(f"  python 4_manual_parameters_simulation.py --user 74 --days 5 --config {config_file}")


def load_config(config_file=None):
    """Load configuration from JSON file or use defaults."""
    if config_file:
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"Error: Config file not found: {config_path}")
            sys.exit(1)
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"✓ Loaded config from: {config_path}")
        return config
    else:
        print("✓ Using default parameters")
        return DEFAULT_PARAMETERS


def apply_cli_overrides(config, overrides):
    """Apply command-line parameter overrides to config.
    
    Overrides format: 
        - Period-specific: "LED_1_evening_school_cooking:occasional_use:0.95"
        - Appliance-level: "LED_1:thermal_p_var:0.15"
    """
    if not overrides:
        return config
    
    for override in overrides:
        parts = override.split(':')
        if len(parts) == 3:
            appliance_period, param_name, value = parts
            
            # Check if this is an appliance-level parameter
            if appliance_period in config:
                # Appliance-level parameter (e.g., thermal_p_var)
                try:
                    value = float(value)
                    config[appliance_period][param_name] = value
                    print(f"  Override: {appliance_period}.{param_name} = {value}")
                except ValueError:
                    print(f"  Warning: Could not parse value '{value}' as float")
            else:
                # Period-specific parameter
                # Parse appliance name and period
                tokens = appliance_period.split('_')
                appliance = f"{tokens[0]}_{tokens[1]}"  # e.g., "LED_1"
                period = '_'.join(tokens[2:])  # e.g., "evening_school_cooking"
                
                if appliance in config and period in config[appliance].get("periods", {}):
                    try:
                        value = float(value)
                        config[appliance]["periods"][period][param_name] = value
                        print(f"  Override: {appliance}[{period}].{param_name} = {value}")
                    except ValueError:
                        print(f"  Warning: Could not parse value '{value}' as float")
                else:
                    print(f"  Warning: Could not find {appliance_period} in config")
    
    return config


def run_ramp_simulation(config, days, seed=42):
    """Create and run RAMP simulation with given parameters."""
    print(f"\nCreating RAMP use case with manual parameters...")
    
    use_case = UseCase()
    user = User()
    
    # Create appliances from config
    appliance_count = 0
    for appliance_name, appliance_config in config.items():
        power = appliance_config["power_W"]
        
        for period_name, period_config in appliance_config["periods"].items():
            appliance_period_name = f"{appliance_name}_{period_name}"
            occasional_use = period_config["occasional_use"]
            avg_minutes = period_config["avg_minutes"]
            std_minutes = period_config["std_minutes"]
            rand_var = period_config["rand_var"]
            
            # Get windows from config, or use defaults
            windows = period_config.get("windows", DEFAULT_PERIOD_WINDOWS.get(period_name))
            if not windows:
                print(f"  Warning: No windows found for {period_name}, using default")
                windows = DEFAULT_PERIOD_WINDOWS.get(period_name, [[0, 1440]])
            
            # Get thermal power variability from config (for post-processing, not RAMP)
            thermal_p_var = period_config.get("thermal_p_var", appliance_config.get("thermal_p_var", 0.0))
            
            # Create appliance
            app = Appliance(
                name=appliance_period_name,
                user=user,
                power=power,
                number=1
            )
            
            # Set occasional use (probability of being used that day)
            app.occasional_use = occasional_use
            
            # Set functioning time (average minutes per day in this period)
            app.func_time = int(np.round(avg_minutes))
            
            # Set functioning cycle (resolution of power ramps)
            func_cycle = period_config.get("func_cycle", 5)  # default to 5 if not specified
            app.func_cycle = func_cycle
            
            # Set variability parameters FIRST
            app.time_fraction_random_variability = rand_var  # Time of use variation
            app.random_var_w = 0.35  # Window timing variability (NOT power variability)
            
            # Set windows for this period (after variability)
            app.num_windows = len(windows)
            for i, (window_start, window_end) in enumerate(windows, start=1):
                setattr(app, f'window_{i}', [window_start, window_end])
            
            user.add_appliance(app)
            appliance_count += 1
    
    # Add user to use case
    use_case.add_user(user)
    
    print(f"✓ Created {appliance_count} appliances (3 devices × 4 periods)")
    
    # Run simulation
    print(f"\nRunning simulation for {days} days...")
    use_case.initialize(num_days=days)
    profile = use_case.generate_daily_load_profiles(flat=True)
    
    return profile


def save_simulation_results(profile, user_id, config_name="manual"):
    """Save simulated load profile to CSV."""
    # profile is a numpy array with 1-minute resolution
    timestamps = []
    power_values = []
    start_date = datetime(2026, 5, 12)
    
    total_minutes = profile.shape[0]
    for minute_idx in range(total_minutes):
        timestamp = start_date + timedelta(minutes=minute_idx)
        timestamps.append(timestamp)
        power_values.append(profile[minute_idx])
    
    df = pd.DataFrame({
        'DateTime': timestamps,
        'Total Load [W]': power_values,
    })
    
    output_file = OUTPUT_DIR / f"simulated_profile_user_{user_id}_{config_name}.csv"
    df.to_csv(output_file, index=False)
    print(f"✓ Simulated profile saved to: {output_file}")
    
    return df


def load_real_data(user_id):
    """Load real measured data."""
    real_file = INPUT_DIR_REAL / f"tpdin_user_{user_id}.csv"
    if not real_file.exists():
        print(f"Error: Real data file not found: {real_file}")
        sys.exit(1)
    
    df_real = pd.read_csv(real_file)
    df_real['timestamp'] = pd.to_datetime(df_real['corrected_timestamp'], errors='coerce')
    df_real = df_real.dropna(subset=['timestamp'])
    
    # Calculate total real power
    df_real['p_total'] = (df_real['v_led_1'] * df_real['c_led_1']).clip(lower=0) + \
                         (df_real['v_led_2'] * df_real['c_led_2']).clip(lower=0) + \
                         (df_real['v_usb'] * df_real['c_usb']).clip(lower=0)
    
    df_real['date_only'] = df_real['timestamp'].dt.date
    df_real['time_decimal'] = df_real['timestamp'].dt.hour + df_real['timestamp'].dt.minute / 60.0
    
    return df_real


def plot_sample_daily_curves(df_real, df_sim, user_id, config_name="manual", num_days=7):
    """Generate plot showing 7 random daily curves with average overlay."""
    print(f"\nGenerating sample daily curves plot (random {num_days} days)...")
    
    # Prepare time bins
    bins = np.arange(0, 24.25, 0.25)
    
    # Process real data - July only
    df_real['time_bin'] = pd.cut(df_real['time_decimal'], bins, labels=bins[:-1])
    df_real_jul = df_real[pd.to_datetime(df_real['date_only']).dt.month == 7]
    real_by_date = df_real_jul.groupby('date_only')
    real_daily_curves = []
    real_dates = []
    for date, group in real_by_date:
        daily_curve = group.groupby('time_bin', observed=True)['p_total'].mean()
        if len(daily_curve) > 10:  # Filter out incomplete days
            real_daily_curves.append(daily_curve)
            real_dates.append(date)
    
    # Randomly select num_days from real data
    if len(real_daily_curves) > num_days:
        indices = np.random.choice(len(real_daily_curves), num_days, replace=False)
        real_sample = [real_daily_curves[i] for i in sorted(indices)]
    else:
        real_sample = real_daily_curves
    
    # Process simulated data
    df_sim['timestamp'] = pd.to_datetime(df_sim['DateTime'])
    df_sim['date_only'] = df_sim['timestamp'].dt.date
    df_sim['time_decimal'] = df_sim['timestamp'].dt.hour + df_sim['timestamp'].dt.minute / 60.0
    df_sim['time_bin'] = pd.cut(df_sim['time_decimal'], bins, labels=bins[:-1])
    sim_by_date = df_sim.groupby('date_only')
    sim_daily_curves = []
    for date, group in sim_by_date:
        daily_curve = group.groupby('time_bin', observed=True)['Total Load [W]'].mean()
        if len(daily_curve) > 10:
            sim_daily_curves.append(daily_curve)
    
    # Randomly select num_days from simulated data
    if len(sim_daily_curves) > num_days:
        indices = np.random.choice(len(sim_daily_curves), num_days, replace=False)
        sim_sample = [sim_daily_curves[i] for i in sorted(indices)]
    else:
        sim_sample = sim_daily_curves
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot real data sample
    time_values = bins[:-1].astype(float)
    colors = plt.cm.Greys(np.linspace(0.3, 0.7, len(real_sample)))
    for i, curve in enumerate(real_sample):
        ax1.plot(time_values[:len(curve)], curve.values, 
                color=colors[i], alpha=0.7, linewidth=2, label=f'Day {i+1}')
    
    ax1.set_title(f'Real Data (July Only) - {num_days} Random Days', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Hour of the Day', fontsize=11)
    ax1.set_ylabel('Power (W)', fontsize=11)
    ax1.set_xticks(np.arange(0, 25, 2))
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(fontsize=9, loc='upper left')
    
    # Plot simulated data sample
    colors = plt.cm.Blues(np.linspace(0.3, 0.7, len(sim_sample)))
    for i, curve in enumerate(sim_sample):
        ax2.plot(time_values[:len(curve)], curve.values, 
                color=colors[i], alpha=0.7, linewidth=2, label=f'Day {i+1}')
    
    ax2.set_title(f'RAMP Simulation - {num_days} Random Days', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Hour of the Day', fontsize=11)
    ax2.set_ylabel('Power (W)', fontsize=11)
    ax2.set_xticks(np.arange(0, 25, 2))
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(fontsize=9, loc='upper left')
    
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"comparison_manual_user_{user_id}_sample_daily_curves.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_daily_curves_cloud(df_real, df_sim, user_id, config_name="manual"):
    """Generate plot showing all daily curves as a cloud with average overlay."""
    print(f"\nGenerating daily curves cloud plot...")
    
    # Prepare time bins
    bins = np.arange(0, 24.25, 0.25)
    
    # Process real data - July only
    df_real['time_bin'] = pd.cut(df_real['time_decimal'], bins, labels=bins[:-1])
    df_real_jul = df_real[pd.to_datetime(df_real['date_only']).dt.month == 7]
    real_by_date = df_real_jul.groupby('date_only')
    real_daily_curves = []
    for date, group in real_by_date:
        daily_curve = group.groupby('time_bin', observed=True)['p_total'].mean()
        if len(daily_curve) > 10:  # Filter out incomplete days
            real_daily_curves.append(daily_curve)
    
    # Process simulated data (group by 24-hour periods)
    df_sim['timestamp'] = pd.to_datetime(df_sim['DateTime'])
    df_sim['date_only'] = df_sim['timestamp'].dt.date
    df_sim['time_decimal'] = df_sim['timestamp'].dt.hour + df_sim['timestamp'].dt.minute / 60.0
    df_sim['time_bin'] = pd.cut(df_sim['time_decimal'], bins, labels=bins[:-1])
    sim_by_date = df_sim.groupby('date_only')
    sim_daily_curves = []
    for date, group in sim_by_date:
        daily_curve = group.groupby('time_bin', observed=True)['Total Load [W]'].mean()
        if len(daily_curve) > 10:
            sim_daily_curves.append(daily_curve)
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot real data cloud
    time_values = bins[:-1].astype(float)
    for curve in real_daily_curves:
        ax1.plot(time_values[:len(curve)], curve.values, 
                color='gray', alpha=0.15, linewidth=1)
    
    # Calculate real average directly from July data only (not from daily curves)
    real_avg_direct = df_real_jul.groupby('time_bin', observed=True)['p_total'].mean()
    ax1.plot(time_values[:len(real_avg_direct)], real_avg_direct.values, 
            color='black', linewidth=3, label='Average', zorder=10)
    
    ax1.set_title(f'Real Data (July Only) - All Daily Curves + Average', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Hour of the Day', fontsize=11)
    ax1.set_ylabel('Power (W)', fontsize=11)
    ax1.set_xticks(np.arange(0, 25, 2))
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(fontsize=10)
    
    # Plot simulated data cloud
    for curve in sim_daily_curves:
        ax2.plot(time_values[:len(curve)], curve.values, 
                color='blue', alpha=0.15, linewidth=1)
    
    # Calculate simulated average directly from all data (not from daily curves)
    sim_avg_direct = df_sim.groupby('time_bin', observed=True)['Total Load [W]'].mean()
    ax2.plot(time_values[:len(sim_avg_direct)], sim_avg_direct.values, 
            color='darkblue', linewidth=3, label='Average', zorder=10)
    
    ax2.set_title(f'RAMP Simulation - All Daily Curves + Average', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Hour of the Day', fontsize=11)
    ax2.set_ylabel('Power (W)', fontsize=11)
    ax2.set_xticks(np.arange(0, 25, 2))
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"comparison_manual_user_{user_id}_daily_curves_cloud.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_comparison(df_real, df_sim, user_id, config_name="manual"):
    """Generate comparison plots between real and simulated data."""
    print(f"\nGenerating comparison plots...")
    
    # Prepare time bins for smoothing
    bins = np.arange(0, 24.25, 0.25)
    
    df_real['time_bin'] = pd.cut(df_real['time_decimal'], bins, labels=bins[:-1])
    df_real_jul = df_real[pd.to_datetime(df_real['date_only']).dt.month == 7]
    df_sim['timestamp'] = pd.to_datetime(df_sim['DateTime'])
    df_sim['time_decimal'] = df_sim['timestamp'].dt.hour + df_sim['timestamp'].dt.minute / 60.0
    df_sim['time_bin'] = pd.cut(df_sim['time_decimal'], bins, labels=bins[:-1])
    
    # Plot 1: Average Daily Profile
    real_curve = df_real_jul.groupby('time_bin', observed=True)['p_total'].mean().reset_index()
    sim_curve = df_sim.groupby('time_bin', observed=True)['Total Load [W]'].mean().reset_index()
    
    plt.figure(figsize=(12, 5))
    plt.plot(real_curve['time_bin'].astype(float), real_curve['p_total'], 
             label='Real Measured Load', color='black', linewidth=3, marker='o')
    plt.plot(sim_curve['time_bin'].astype(float), sim_curve['Total Load [W]'], 
             label='RAMP Simulation (Manual Params)', color='blue', linestyle='--', 
             linewidth=2.5, marker='s', alpha=0.8)
    
    plt.title(f'Average Daily Load Profile - User {user_id} (Manual Parameters)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('Average Power (W)', fontsize=12)
    plt.xticks(np.arange(0, 25, 2))
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11, loc='upper left')
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"comparison_manual_user_{user_id}_avg_profile.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()
    
    # Plot 2: Variability/Spread
    real_std = df_real_jul.groupby('time_bin', observed=True)['p_total'].std().reset_index()
    sim_std = df_sim.groupby('time_bin', observed=True)['Total Load [W]'].std().reset_index()
    
    plt.figure(figsize=(12, 5))
    plt.plot(real_std['time_bin'].astype(float), real_std['p_total'], 
             label='Real Data Std Dev', color='darkred', linewidth=3, marker='o')
    plt.plot(sim_std['time_bin'].astype(float), sim_std['Total Load [W]'], 
             label='Simulation Std Dev', color='darkblue', linestyle='--', 
             linewidth=2.5, marker='s', alpha=0.8)
    
    plt.title(f'Load Variability by Hour - User {user_id} (Manual Parameters)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('Standard Deviation (W)', fontsize=12)
    plt.xticks(np.arange(0, 25, 2))
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"comparison_manual_user_{user_id}_variability.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()
    
    # Plot 3: Statistical Comparison Table
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Calculate statistics
    real_mean = df_real_jul['p_total'].mean()
    real_max = df_real_jul['p_total'].max()
    real_std = df_real_jul['p_total'].std()
    
    sim_mean = df_sim['Total Load [W]'].mean()
    sim_max = df_sim['Total Load [W]'].max()
    sim_std = df_sim['Total Load [W]'].std()
    
    stats_data = [
        ['Metric', 'Real Data', 'Simulation', 'Difference'],
        ['Mean Power (W)', f'{real_mean:.2f}', f'{sim_mean:.2f}', 
         f'{abs(real_mean - sim_mean):.2f} ({abs(real_mean - sim_mean)/real_mean*100:.1f}%)'],
        ['Max Power (W)', f'{real_max:.2f}', f'{sim_max:.2f}', 
         f'{abs(real_max - sim_max):.2f} ({abs(real_max - sim_max)/real_max*100:.1f}%)'],
        ['Std Dev (W)', f'{real_std:.2f}', f'{sim_std:.2f}', 
         f'{abs(real_std - sim_std):.2f} ({abs(real_std - sim_std)/real_std*100:.1f}%)'],
    ]
    
    table = ax.table(cellText=stats_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.25, 0.25, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title(f'Load Statistics Comparison - User {user_id}', 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"comparison_manual_user_{user_id}_statistics.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_three_random_daily_curves(df_real, df_sim, user_id, config_name="manual"):
    """Generate plot showing 3 random daily load curves side by side."""
    print(f"\nGenerating 3 random daily curves plot...")
    
    # Prepare time bins
    bins = np.arange(0, 24.25, 0.25)
    
    # Process real data - July only
    df_real['time_bin'] = pd.cut(df_real['time_decimal'], bins, labels=bins[:-1])
    df_real_jul = df_real[pd.to_datetime(df_real['date_only']).dt.month == 7]
    real_by_date = df_real_jul.groupby('date_only')
    real_daily_curves = []
    real_dates = []
    for date, group in real_by_date:
        daily_curve = group.groupby('time_bin', observed=True)['p_total'].mean()
        if len(daily_curve) > 10:  # Filter out incomplete days
            real_daily_curves.append(daily_curve)
            real_dates.append(date)
    
    # Randomly select 3 from real data
    num_days = min(3, len(real_daily_curves))
    if len(real_daily_curves) > num_days:
        indices = np.random.choice(len(real_daily_curves), num_days, replace=False)
        real_sample = [real_daily_curves[i] for i in sorted(indices)]
    else:
        real_sample = real_daily_curves
    
    # Process simulated data
    df_sim['timestamp'] = pd.to_datetime(df_sim['DateTime'])
    df_sim['date_only'] = df_sim['timestamp'].dt.date
    df_sim['time_decimal'] = df_sim['timestamp'].dt.hour + df_sim['timestamp'].dt.minute / 60.0
    df_sim['time_bin'] = pd.cut(df_sim['time_decimal'], bins, labels=bins[:-1])
    sim_by_date = df_sim.groupby('date_only')
    sim_daily_curves = []
    for date, group in sim_by_date:
        daily_curve = group.groupby('time_bin', observed=True)['Total Load [W]'].mean()
        if len(daily_curve) > 10:
            sim_daily_curves.append(daily_curve)
    
    # Randomly select 3 from simulated data
    num_days = min(3, len(sim_daily_curves))
    if len(sim_daily_curves) > num_days:
        indices = np.random.choice(len(sim_daily_curves), num_days, replace=False)
        sim_sample = [sim_daily_curves[i] for i in sorted(indices)]
    else:
        sim_sample = sim_daily_curves
    
    # Create figure with 3 subplots (one for each day)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    time_values = bins[:-1].astype(float)
    
    for i in range(min(len(real_sample), len(sim_sample))):
        ax = axes[i]
        
        # Plot real and simulated curves
        ax.plot(time_values[:len(real_sample[i])], real_sample[i].values, 
                color='black', linewidth=2.5, label='Real Data', marker='o', markersize=4, alpha=0.8)
        ax.plot(time_values[:len(sim_sample[i])], sim_sample[i].values, 
                color='blue', linewidth=2.5, label='RAMP Simulation', marker='s', markersize=4, 
                linestyle='--', alpha=0.8)
        
        ax.set_title(f'Day {i+1}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Hour of the Day', fontsize=10)
        ax.set_ylabel('Power (W)', fontsize=10)
        ax.set_xticks(np.arange(0, 25, 4))
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(fontsize=9, loc='upper left')
    
    plt.suptitle(f'3 Random Daily Load Curves (July Only) - User {user_id} (Real vs Simulation)', 
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"comparison_manual_user_{user_id}_3random_daily_curves.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def print_config_summary(config):
    """Print a summary of the configuration parameters."""
    print("\n" + "="*80)
    print("RAMP PARAMETER CONFIGURATION")
    print("="*80)
    
    for appliance, app_config in config.items():
        power = app_config["power_W"]
        thermal_p_var = app_config.get("thermal_p_var", "N/A")
        print(f"\n{appliance} (Power: {power}W, Thermal_P_Var: {thermal_p_var})")
        print("-" * 80)
        
        for period, period_config in app_config["periods"].items():
            period_thermal_p_var = period_config.get("thermal_p_var", thermal_p_var)
            print(f"  {period:30s} | Prob: {period_config['occasional_use']:.2f}  "
                  f"Avg: {period_config['avg_minutes']:6.1f} min  "
                  f"Std: {period_config['std_minutes']:6.1f} min  "
                  f"Time_CV: {period_config['rand_var']:.2f}  "
                  f"Power_CV: {period_thermal_p_var}")


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Manually set RAMP parameters and simulate vs real data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default parameters
  python 4_manual_parameters_simulation.py --user 74 --days 5
  
  # Run with custom config file
  python 4_manual_parameters_simulation.py --user 74 --days 5 --config manual_params.json
  
  # Override specific parameters
  python 4_manual_parameters_simulation.py --user 74 --days 5 \\
    --occasional-use LED_1_evening_school_cooking:0.95 \\
    --thermal-p-var LED_1:0.15
    
  # Appliance-level thermal_p_var applies to all periods:
    --thermal-p-var LED_1:0.15
    
  # Period-specific thermal_p_var:
    --thermal-p-var LED_1_evening_school_cooking:thermal_p_var:0.20
        """)
    
    parser.add_argument('--user', type=int, required=False, help='User ID')
    parser.add_argument('--days', type=int, default=5, help='Number of days to simulate (default: 5)')
    parser.add_argument('--config', type=str, help='Path to custom config JSON file')
    parser.add_argument('--occasional-use', action='append', dest='overrides',
                       help='Override parameters (format: APPLIANCE_PERIOD:param:value)')
    parser.add_argument('--thermal-p-var', action='append', dest='overrides',
                       help='Override thermal_p_var (power variability): APPLIANCE:value OR APPLIANCE_PERIOD:thermal_p_var:value')
    parser.add_argument('--create-example', action='store_true', 
                       help='Create example config file and exit')
    
    args = parser.parse_args()
    
    # Create example config if requested
    if args.create_example:
        create_example_config()
        return
    
    # Check that user is provided if not creating example
    if args.user is None:
        print("Error: --user is required (unless using --create-example)")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("MANUAL PARAMETER RAMP SIMULATION")
    print("="*80)
    
    # Load configuration
    print(f"DEBUG: args.config = {args.config}")
    config = load_config(args.config)
    print(f"DEBUG: Loaded config has {sum(len(v.get('periods', {})) for v in config.values())} total periods")
    
    # Apply CLI overrides
    if args.overrides:
        config = apply_cli_overrides(config, args.overrides)
    
    # Print parameter summary
    print_config_summary(config)
    
    # Run RAMP simulation
    profile = run_ramp_simulation(config, days=args.days)
    
    # Save results
    df_sim = save_simulation_results(profile, args.user, config_name="manual")
    
    # Load real data and generate plots
    print(f"\nLoading real data for User {args.user}...")
    df_real = load_real_data(args.user)
    print(f"✓ Loaded {len(df_real)} measurements from {df_real['date_only'].nunique()} days")
    
    # Generate comparison plots
    plot_comparison(df_real, df_sim, args.user, config_name="manual")
    
    # Generate sample daily curves plot (7 random days)
    plot_sample_daily_curves(df_real, df_sim, args.user, config_name="manual", num_days=7)
    
    # Generate 3 random daily curves plot
    plot_three_random_daily_curves(df_real, df_sim, args.user, config_name="manual")
    
    # Generate daily curves cloud plot
    plot_daily_curves_cloud(df_real, df_sim, args.user, config_name="manual")
    
    print("\n" + "="*80)
    print("✓ SIMULATION COMPLETE")
    print("="*80)
    print(f"\nOutputs saved to:")
    print(f"  Simulation: {OUTPUT_DIR}")
    print(f"  Figures: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
