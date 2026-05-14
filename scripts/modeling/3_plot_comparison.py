import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
import sys
import matplotlib.dates as mdates

# Define paths matching the project structure
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR_REAL = PROJECT_ROOT / "data" / "clean" / "timeseries"
INPUT_DIR_SIM = SCRIPT_DIR / "output"
FIGURES_DIR = PROJECT_ROOT / "results" / "timeseries" / "figures"

# Ensure Figures directory exists
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def load_and_prep_data(user_id, sim_model="period"):
    """Loads both real and simulated data and preps time bins.
    
    Args:
        user_id: User ID to load
        sim_model: "period" (default) or "daily" to specify which simulation to use
    """
    print(f"Loading data for User {user_id}...")
    
    # 1. Load Real Data
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

    # 2. Load Simulated Data
    # Try period-based model first, fall back to daily, then fallback to old format
    sim_file = INPUT_DIR_SIM / f"simulated_profile_user_{user_id}_{sim_model}.csv"
    if not sim_file.exists():
        print(f"Warning: {sim_file.name} not found, trying alternative...")
        # Fallback: try the other model type
        alt_model = "daily" if sim_model == "period" else "period"
        sim_file = INPUT_DIR_SIM / f"simulated_profile_user_{user_id}_{alt_model}.csv"
        if not sim_file.exists():
            # Last resort: try old format without model type
            sim_file = INPUT_DIR_SIM / f"simulated_profile_user_{user_id}.csv"
            if not sim_file.exists():
                print(f"Error: No simulated data file found for user {user_id}")
                print(f"Tried: simulated_profile_user_{user_id}_{sim_model}.csv")
                print(f"Tried: simulated_profile_user_{user_id}_{alt_model}.csv")
                print(f"Tried: simulated_profile_user_{user_id}.csv")
                print("Run 2_run_simulations.py first!")
                sys.exit(1)
            print(f"Using old format: {sim_file.name}")
        else:
            print(f"Using {alt_model} model: {sim_file.name}")
    else:
        print(f"Using {sim_model} model: {sim_file.name}")
        
    df_sim = pd.read_csv(sim_file)
    df_sim['timestamp'] = pd.to_datetime(df_sim['DateTime'])
    df_sim['p_total'] = df_sim['Total Load [W]']
    df_sim['date_only'] = df_sim['timestamp'].dt.date
    df_sim['time_decimal'] = df_sim['timestamp'].dt.hour + df_sim['timestamp'].dt.minute / 60.0

    # 3. Create standardized time bins (15-minute intervals) for smooth averaging
    bins = np.arange(0, 24.25, 0.25)
    df_real['time_bin'] = pd.cut(df_real['time_decimal'], bins, labels=bins[:-1])
    df_sim['time_bin'] = pd.cut(df_sim['time_decimal'], bins, labels=bins[:-1])

    return df_real, df_sim

def plot_averages(df_real, df_sim, user_id):
    """Plot 1: The Daily Average Comparison"""
    real_curve = df_real.groupby('time_bin', observed=True)['p_total'].mean().reset_index()
    sim_curve = df_sim.groupby('time_bin', observed=True)['p_total'].mean().reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(real_curve['time_bin'].astype(float), real_curve['p_total'], 
             label='Real Measured Load', color='black', linewidth=3)
    plt.plot(sim_curve['time_bin'].astype(float), sim_curve['p_total'], 
             label='RAMP Simulation', color='blue', linestyle='--', linewidth=2.5)

    plt.title(f'Average Daily Load Profile Comparison - User {user_id}', fontsize=14, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('Average Power (W)', fontsize=12)
    plt.xticks(np.arange(0, 25, 2))
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    out_path = FIGURES_DIR / f"val_average_user_{user_id}.png"
    plt.savefig(out_path, dpi=300)
    print(f"✓ Saved Average Plot: {out_path.name}")
    plt.close()

def plot_shadows(df_real, df_sim, user_id):
    """Plot 2: The Variance/Shadow Comparison (Side-by-Side)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
    
    # Real Shadow
    for date in df_real['date_only'].unique():
        day_data = df_real[df_real['date_only'] == date]
        ax1.plot(day_data['time_decimal'], day_data['p_total'], color='gray', alpha=0.1, linewidth=1)
    real_mean = df_real.groupby('time_bin', observed=True)['p_total'].mean()
    ax1.plot(real_mean.index.astype(float), real_mean.values, color='black', linewidth=2, label='Mean')
    
    ax1.set_title('Real Data: Variance & Spread', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Hour of the Day')
    ax1.set_ylabel('Power (W)')
    ax1.set_xticks(np.arange(0, 25, 4))
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(bottom=0)

    # Sim Shadow
    for date in df_sim['date_only'].unique()[:len(df_real['date_only'].unique())]: # Match number of days
        day_data = df_sim[df_sim['date_only'] == date]
        ax2.plot(day_data['time_decimal'], day_data['p_total'], color='lightblue', alpha=0.1, linewidth=1)
    sim_mean = df_sim.groupby('time_bin', observed=True)['p_total'].mean()
    ax2.plot(sim_mean.index.astype(float), sim_mean.values, color='blue', linewidth=2, label='Mean')

    ax2.set_title('RAMP Simulation: Variance & Spread', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Hour of the Day')
    ax2.set_xticks(np.arange(0, 25, 4))
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = FIGURES_DIR / f"val_variance_user_{user_id}.png"
    plt.savefig(out_path, dpi=300)
    print(f"✓ Saved Variance Plot: {out_path.name}")
    plt.close()

def plot_specific_days(df_real, df_sim, user_id):
    """Plot 3: Single Day Spikes (3 random days stacked)"""
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, sharey=True)
    
    # Pick 3 random days from both datasets
    real_days = np.random.choice(df_real['date_only'].unique(), 3, replace=False)
    sim_days = np.random.choice(df_sim['date_only'].unique(), 3, replace=False)

    for i in range(3):
        # Real
        r_data = df_real[df_real['date_only'] == real_days[i]]
        axes[i].plot(r_data['time_decimal'], r_data['p_total'], color='black', label='Real Day' if i==0 else "")
        
        # Sim
        s_data = df_sim[df_sim['date_only'] == sim_days[i]]
        axes[i].plot(s_data['time_decimal'], s_data['p_total'], color='blue', alpha=0.7, label='Simulated Day' if i==0 else "")
        
        axes[i].set_ylabel('Power (W)')
        axes[i].grid(True, alpha=0.4)
        if i == 0:
            axes[i].legend(loc='upper right')

    axes[2].set_xlabel('Hour of the Day', fontsize=12)
    axes[2].set_xticks(np.arange(0, 25, 2))
    plt.suptitle(f'Intermittent Spike Behavior (3 Random Days) - User {user_id}', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    out_path = FIGURES_DIR / f"val_specific_days_user_{user_id}.png"
    plt.savefig(out_path, dpi=300)
    print(f"✓ Saved Specific Days Plot: {out_path.name}")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot validation comparisons")
    parser.add_argument("--user", type=str, required=True, help="User ID (e.g., '74')")
    parser.add_argument("--model", type=str, default="period", choices=["period", "daily"],
                        help="Which simulation model to compare: 'period' (default) or 'daily'")
    args = parser.parse_args()
    
    df_real, df_sim = load_and_prep_data(args.user, sim_model=args.model)
    plot_averages(df_real, df_sim, args.user)
    plot_shadows(df_real, df_sim, args.user)
    plot_specific_days(df_real, df_sim, args.user)
    
    print("\nAll validation plots generated successfully!")