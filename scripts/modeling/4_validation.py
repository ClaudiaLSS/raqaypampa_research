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
OUTPUT_DIR = SCRIPT_DIR / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
METRICS_DIR = OUTPUT_DIR / "metrics"

# Ensure output directories exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR.mkdir(parents=True, exist_ok=True)

def load_and_prep_data(user_id, sim_model="period", num_days=None):
    """Loads both real and simulated data and preps time bins.
    
    Args:
        user_id: User ID to load
        sim_model: "period" (default) or "daily" to specify which simulation to use
        num_days: Limit to first N days of data (None = use all available data)
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

    # 2. Load Simulated Data - Try plain filename first (new format), then model-specific (old format)
    sim_file = INPUT_DIR_SIM / f"simulated_profile_user_{user_id}.csv"
    if not sim_file.exists():
        print(f"Warning: {sim_file.name} not found, trying model-specific names...")
        alt_model = "daily" if sim_model == "period" else "period"
        sim_file = INPUT_DIR_SIM / f"simulated_profile_user_{user_id}_{alt_model}.csv"
        if not sim_file.exists():
            sim_file = INPUT_DIR_SIM / f"simulated_profile_user_{user_id}_{sim_model}.csv"
            if not sim_file.exists():
                print(f"Error: No simulated data file found for user {user_id}")
                print(f"Tried: simulated_profile_user_{user_id}.csv")
                print(f"Tried: simulated_profile_user_{user_id}_{alt_model}.csv")
                print(f"Tried: simulated_profile_user_{user_id}_{sim_model}.csv")
                sys.exit(1)
            print(f"Using old format: {sim_file.name}")
        else:
            print(f"Using {alt_model} model: {sim_file.name}")
    else:
        print(f"Using new format: {sim_file.name}")
        
    df_sim = pd.read_csv(sim_file)
    df_sim['timestamp'] = pd.to_datetime(df_sim['DateTime'])
    df_sim['p_total'] = df_sim['Total Load [W]']
    df_sim['date_only'] = df_sim['timestamp'].dt.date
    df_sim['time_decimal'] = df_sim['timestamp'].dt.hour + df_sim['timestamp'].dt.minute / 60.0

    # 4. Limit to first N days if specified
    if num_days is not None and num_days > 0:
        print(f"\nLimiting data to first {num_days} days...")
        real_days = sorted(df_real['date_only'].unique())[:num_days]
        sim_days = sorted(df_sim['date_only'].unique())[:num_days]
        
        df_real = df_real[df_real['date_only'].isin(real_days)]
        df_sim = df_sim[df_sim['date_only'].isin(sim_days)]
        
        print(f"Real data: {len(real_days)} days ({df_real.shape[0]} rows)")
        print(f"Simulated data: {len(sim_days)} days ({df_sim.shape[0]} rows)")

    # 5. Create standardized time bins (15-minute intervals) for smooth averaging
    bins = np.arange(0, 24.25, 0.25)
    df_real['time_bin'] = pd.cut(df_real['time_decimal'], bins, labels=bins[:-1])
    df_sim['time_bin'] = pd.cut(df_sim['time_decimal'], bins, labels=bins[:-1])

    return df_real, df_sim

def plot_averages(df_real, df_sim, user_id):
    """Plot 1: The Daily Average Comparison"""
    # Group by time_bin to get average power at each hour across all days
    real_curve = df_real.groupby('time_bin', observed=True)['p_total'].mean().reset_index()
    sim_curve = df_sim.groupby('time_bin', observed=True)['p_total'].mean().reset_index()
    
    # Debug info
    print(f"\nDebug - plot_averages:")
    print(f"  Real data: {df_real.shape[0]} rows, {df_real['date_only'].nunique()} unique days")
    print(f"  Real time bins with data: {len(real_curve)} bins")
    print(f"  Real data range: {df_real['p_total'].min():.2f}W - {df_real['p_total'].max():.2f}W")
    print(f"  Real daily avg curve range: {real_curve['p_total'].min():.2f}W - {real_curve['p_total'].max():.2f}W")
    print(f"  Sim data: {df_sim.shape[0]} rows, {df_sim['date_only'].nunique()} unique days")
    print(f"  Sim time bins with data: {len(sim_curve)} bins")
    print(f"  Sim data range: {df_sim['p_total'].min():.2f}W - {df_sim['p_total'].max():.2f}W")
    print(f"  Sim daily avg curve range: {sim_curve['p_total'].min():.2f}W - {sim_curve['p_total'].max():.2f}W")

    plt.figure(figsize=(12, 6))
    plt.plot(real_curve['time_bin'].astype(float), real_curve['p_total'], 
             label='Real Measured Load', color='black', linewidth=3, marker='o', markersize=4)
    plt.plot(sim_curve['time_bin'].astype(float), sim_curve['p_total'], 
             label='RAMP Simulation', color='blue', linestyle='--', linewidth=2.5, marker='s', markersize=4)

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
    for date in df_sim['date_only'].unique()[:len(df_real['date_only'].unique())]:
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
    
    real_days = np.random.choice(df_real['date_only'].unique(), 3, replace=False)
    sim_days = np.random.choice(df_sim['date_only'].unique(), min(3, len(df_sim['date_only'].unique())), replace=False)
    
    # Debug info
    print(f"\nDebug - plot_specific_days:")
    print(f"  Real unique dates: {df_real['date_only'].nunique()}")
    print(f"  Sim unique dates: {df_sim['date_only'].nunique()}")
    print(f"  Real days selected: {real_days}")
    print(f"  Sim days selected: {sim_days}")
    print(f"  Sim days available: {len(sim_days)}")
    
    # Check data for each day
    for i, sim_day in enumerate(sim_days):
        sim_day_data = df_sim[df_sim['date_only'] == sim_day]
        print(f"  Sim day {i} ({sim_day}): {len(sim_day_data)} rows")

    for i in range(3):
        r_data = df_real[df_real['date_only'] == real_days[i]]
        axes[i].plot(r_data['time_decimal'], r_data['p_total'], color='black', label='Real Day' if i==0 else "")
        
        if i < len(sim_days):
            s_data = df_sim[df_sim['date_only'] == sim_days[i]]
            if len(s_data) > 0:
                axes[i].plot(s_data['time_decimal'], s_data['p_total'], color='blue', alpha=0.7, label='Simulated Day' if i==0 else "")
            else:
                axes[i].text(12, 3, f"No sim data for {sim_days[i]}", ha='center', fontsize=10, color='red')
        else:
            axes[i].text(12, 3, "No simulated day available", ha='center', fontsize=10, color='red')
        
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


def calculate_structural_metrics(df):
    """Extracts Tier 2 structural profiling and resilience metrics from a dataframe."""
    # 1. Modal Peak Hour
    daily_peak_idx = df.groupby('date_only')['p_total'].idxmax()
    peak_hours_series = df.loc[daily_peak_idx.dropna(), 'timestamp'].dt.hour
    modal_peak_hour = int(peak_hours_series.mode()[0]) if not peak_hours_series.empty else 0
    
    # 2. Base Load (Minimum Value / Safety Baseline during 00:00 - 04:00)
    night_data = df[(df['timestamp'].dt.hour >= 0) & (df['timestamp'].dt.hour < 4)]
    daily_night_min = night_data.groupby('date_only')['p_total'].min()
    base_load_W = round(daily_night_min.median(), 2) if not daily_night_min.empty else 0.0
    
    # 3. MRSD (Mean Relative Standard Deviation of Daily Energy -> Chaos Metric)
    # Dynamically calculate logging interval in hours to ensure Wh mapping parity
    interval_hours = df['timestamp'].diff().median().total_seconds() / 3600.0
    if pd.isna(interval_hours) or interval_hours == 0:
        interval_hours = 5.0 / 60.0  # Fallback to 5 mins default
        
    daily_energy_Wh = df.groupby('date_only')['p_total'].sum() * interval_hours
    mean_daily_Wh = daily_energy_Wh.mean()
    std_daily_Wh = daily_energy_Wh.std()
    mrsd = round(std_daily_Wh / mean_daily_Wh, 3) if mean_daily_Wh > 0 else 0.0
    
    # 4. Relative Mean Power (Time-Blocked Macro-Windows)
    time_periods = {
        'morning': (4, 10),
        'daytime': (10, 17),
        'evening': (17, 24),
        'night': (0, 4)
    }
    relative_mean_power = {}
    for name, (start_h, end_h) in time_periods.items():
        p_data = df[(df['timestamp'].dt.hour >= start_h) & (df['timestamp'].dt.hour < end_h)]
        relative_mean_power[name] = round(p_data['p_total'].mean(), 2) if len(p_data) > 0 else 0.0
        
    return modal_peak_hour, base_load_W, mrsd, relative_mean_power


def calculate_validation_metrics(df_real, df_sim, user_id, epsilon_watts=2.0):
    """Calculates Dual-Tier validation metrics (Time-Series alignment & Structural profiling)."""
    print("Calculating validation metrics...")
    
    # =====================================================================
    # TIER 1 VALIDATION: TIME-SERIES ALIGNMENT
    # =====================================================================
    real_profile = df_real.groupby('time_bin', observed=True)['p_total'].mean().fillna(0).values
    sim_profile = df_sim.groupby('time_bin', observed=True)['p_total'].mean().fillna(0).values

    # RMSE
    rmse = np.sqrt(np.mean((real_profile - sim_profile) ** 2))
    
    # MPDADA
    real_peak = np.max(real_profile)
    sim_peak = np.max(sim_profile)
    real_daily_avg = np.mean(real_profile)
    mpdada = abs(sim_peak - real_peak) / real_daily_avg if real_daily_avg > 0 else 0

    # LCSS
    n, m = len(real_profile), len(sim_profile)
    dp = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if abs(real_profile[i-1] - sim_profile[j-1]) <= epsilon_watts:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    lcss_score = dp[n][m] / max(n, m)

    # =====================================================================
    # TIER 2 VALIDATION: STRUCTURAL PROFILING & RESILIENCE INDICATORS
    # =====================================================================
    r_peak_hr, r_base, r_mrsd, r_rmp = calculate_structural_metrics(df_real)
    s_peak_hr, s_base, s_mrsd, s_rmp = calculate_structural_metrics(df_sim)

    # Compile Dual-Tier Results for comparison format (Real vs Simulated in rows)
    metrics_list = [
        {"User_ID": user_id, "Metric": "RMSE (Watts)", "Real": "—", "Simulated": round(rmse, 3), "Deviation": "—"},
        {"User_ID": user_id, "Metric": "MPDADA Ratio", "Real": "—", "Simulated": round(mpdada, 3), "Deviation": "—"},
        {"User_ID": user_id, "Metric": "LCSS Score", "Real": "—", "Simulated": round(lcss_score, 3), "Deviation": "—"},
        {"User_ID": user_id, "Metric": "Modal Peak Hour", "Real": f"{r_peak_hr:02d}:00", "Simulated": f"{s_peak_hr:02d}:00", "Deviation": f"{abs(r_peak_hr - s_peak_hr)}h"},
        {"User_ID": user_id, "Metric": "Base Load (W)", "Real": round(r_base, 2), "Simulated": round(s_base, 2), "Deviation": f"{abs(r_base - s_base):.2f}W ({abs(r_base - s_base) / (r_base if r_base > 0 else 1) * 100:.1f}%)"},
        {"User_ID": user_id, "Metric": "MRSD Chaos Index", "Real": round(r_mrsd, 3), "Simulated": round(s_mrsd, 3), "Deviation": f"{abs(r_mrsd - s_mrsd):.3f} ({abs(r_mrsd - s_mrsd) / (r_mrsd if r_mrsd > 0 else 1) * 100:.1f}%)"},
        {"User_ID": user_id, "Metric": "RMP Morning (W)", "Real": round(r_rmp['morning'], 2), "Simulated": round(s_rmp['morning'], 2), "Deviation": f"{abs(r_rmp['morning'] - s_rmp['morning']):.2f}W ({abs(r_rmp['morning'] - s_rmp['morning']) / (r_rmp['morning'] if r_rmp['morning'] > 0 else 1) * 100:.1f}%)"},
        {"User_ID": user_id, "Metric": "RMP Daytime (W)", "Real": round(r_rmp['daytime'], 2), "Simulated": round(s_rmp['daytime'], 2), "Deviation": f"{abs(r_rmp['daytime'] - s_rmp['daytime']):.2f}W ({abs(r_rmp['daytime'] - s_rmp['daytime']) / (r_rmp['daytime'] if r_rmp['daytime'] > 0 else 1) * 100:.1f}%)"},
        {"User_ID": user_id, "Metric": "RMP Evening (W)", "Real": round(r_rmp['evening'], 2), "Simulated": round(s_rmp['evening'], 2), "Deviation": f"{abs(r_rmp['evening'] - s_rmp['evening']):.2f}W ({abs(r_rmp['evening'] - s_rmp['evening']) / (r_rmp['evening'] if r_rmp['evening'] > 0 else 1) * 100:.1f}%)"},
        {"User_ID": user_id, "Metric": "RMP Night (W)", "Real": round(r_rmp['night'], 2), "Simulated": round(s_rmp['night'], 2), "Deviation": f"{abs(r_rmp['night'] - s_rmp['night']):.2f}W ({abs(r_rmp['night'] - s_rmp['night']) / (r_rmp['night'] if r_rmp['night'] > 0 else 1) * 100:.1f}%)"}
    ]
    
    # Save to CSV - Always write fresh (not append) to avoid format conflicts
    metrics_file = METRICS_DIR / "validation_metrics.csv"
    
    df_results = pd.DataFrame(metrics_list)
    # Write with header, don't append to avoid format mixing
    df_results.to_csv(metrics_file, mode='w', header=True, index=False)
        
    print("\n" + "="*70)
    print(f"DUAL-TIER PERFORMANCE SUMMARY (USER {user_id})")
    print("="*70)
    print(f"  TIER 1 (Error Metrics) -> RMSE: {rmse:.3f}W | LCSS: {lcss_score:.3f} | MPDADA: {mpdada:.3f}")
    print(f"\n  TIER 2 COMPARISON (Real vs Simulated with Deviation):")
    print(f"    Chaos/MRSD:    Real: {r_mrsd:<6} | Sim: {s_mrsd:<6} | Δ: {abs(r_mrsd - s_mrsd):.3f} ({abs(r_mrsd - s_mrsd)/(r_mrsd if r_mrsd > 0 else 1)*100:.1f}%)")
    print(f"    Base Load:     Real: {r_base:<5}W | Sim: {s_base:<5}W | Δ: {abs(r_base - s_base):.2f}W ({abs(r_base - s_base)/(r_base if r_base > 0 else 1)*100:.1f}%)")
    print(f"    Peak Hour:     Real: {r_peak_hr:02d}:00  | Sim: {s_peak_hr:02d}:00 | Δ: {abs(r_peak_hr - s_peak_hr)}h")
    print(f"\n  Relative Mean Power (Real vs Sim with Deviation):")
    print(f"    Morning: {r_rmp['morning']:<5}W | {s_rmp['morning']:<5}W | Δ {abs(r_rmp['morning']-s_rmp['morning']):.2f}W ({abs(r_rmp['morning']-s_rmp['morning'])/(r_rmp['morning'] if r_rmp['morning'] > 0 else 1)*100:.1f}%)")
    print(f"    Daytime: {r_rmp['daytime']:<5}W | {s_rmp['daytime']:<5}W | Δ {abs(r_rmp['daytime']-s_rmp['daytime']):.2f}W ({abs(r_rmp['daytime']-s_rmp['daytime'])/(r_rmp['daytime'] if r_rmp['daytime'] > 0 else 1)*100:.1f}%)")
    print(f"    Evening: {r_rmp['evening']:<5}W | {s_rmp['evening']:<5}W | Δ {abs(r_rmp['evening']-s_rmp['evening']):.2f}W ({abs(r_rmp['evening']-s_rmp['evening'])/(r_rmp['evening'] if r_rmp['evening'] > 0 else 1)*100:.1f}%)")
    print(f"    Night:   {r_rmp['night']:<5}W | {s_rmp['night']:<5}W | Δ {abs(r_rmp['night']-s_rmp['night']):.2f}W ({abs(r_rmp['night']-s_rmp['night'])/(r_rmp['night'] if r_rmp['night'] > 0 else 1)*100:.1f}%)")
    print("="*70 + "\n")
    
    return metrics_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot validation comparisons and calculate metrics")
    parser.add_argument("--user", type=str, required=True, help="User ID (e.g., '74')")
    parser.add_argument("--model", type=str, default="period", choices=["period", "daily"],
                        help="Which simulation model to compare: 'period' (default) or 'daily'")
    parser.add_argument("--days", type=int, default=None,
                        help="Limit validation to first N days of data (default: use all available days)")
    args = parser.parse_args()
    
    df_real, df_sim = load_and_prep_data(args.user, sim_model=args.model, num_days=args.days)
    
    # Generate visual plots
    plot_averages(df_real, df_sim, args.user)
    plot_shadows(df_real, df_sim, args.user)
    plot_specific_days(df_real, df_sim, args.user)
    
    # Generate mathematical validation
    metrics = calculate_validation_metrics(df_real, df_sim, args.user, epsilon_watts=2.0)
    
    print("All validation plots and metrics generated successfully!")