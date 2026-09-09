"""
Diagnostic script to analyze RAMP output and understand power behavior patterns.
Identifies exact power transitions, window boundaries, and anomalies.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"

def analyze_ramp_output(user_id, config_name="manual"):
    """Analyze simulated load profile for patterns."""
    
    profile_file = OUTPUT_DIR / f"simulated_profile_user_{user_id}_{config_name}.csv"
    
    if not profile_file.exists():
        print(f"Error: Profile file not found: {profile_file}")
        sys.exit(1)
    
    df = pd.read_csv(profile_file)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute
    df['Time_str'] = df['DateTime'].dt.strftime('%H:%M:%S')
    
    print("\n" + "="*80)
    print("RAMP OUTPUT DIAGNOSTIC ANALYSIS")
    print("="*80)
    
    # 1. Analyze power transitions
    print("\n1. POWER TRANSITION ANALYSIS")
    print("-" * 80)
    
    df['Power_Diff'] = df['Total Load [W]'].diff()
    df['Power_Changed'] = (df['Power_Diff'].abs() > 0.0001)
    
    transitions = df[df['Power_Changed']].copy()
    print(f"Total rows: {len(df)}")
    print(f"Rows with power changes: {len(transitions)}")
    print(f"Percentage of changes: {len(transitions)/len(df)*100:.2f}%\n")
    
    # 2. Look for the 0.001 W pattern
    print("2. GHOST POWER ANALYSIS (0.001 W pattern)")
    print("-" * 80)
    
    ghost_power = df[(df['Total Load [W]'] > 0.0001) & (df['Total Load [W]'] < 0.002)]
    print(f"Rows with power between 0.0001-0.002 W: {len(ghost_power)}")
    
    if len(ghost_power) > 0:
        print("\nSample of ghost power occurrences:")
        print(ghost_power[['Time_str', 'Total Load [W]', 'Hour', 'Minute']].head(20).to_string())
        
        # Check if they occur at specific times
        ghost_hours = ghost_power['Hour'].value_counts().sort_index()
        print(f"\nGhost power by hour:")
        print(ghost_hours)
        
        ghost_minutes = ghost_power['Minute'].value_counts().sort_index()
        print(f"\nGhost power by minute:")
        print(ghost_minutes)
    
    # 3. Analyze power levels when "ON"
    print("\n3. ACTIVE POWER LEVELS (when device is ON)")
    print("-" * 80)
    
    active_power = df[df['Total Load [W]'] > 0.1]  # Excluding ghost power
    print(f"Rows with power > 0.1 W: {len(active_power)}")
    
    if len(active_power) > 0:
        print(f"\nActive power statistics:")
        print(f"  Min: {active_power['Total Load [W]'].min():.3f} W")
        print(f"  Max: {active_power['Total Load [W]'].max():.3f} W")
        print(f"  Mean: {active_power['Total Load [W]'].mean():.3f} W")
        print(f"  Std Dev: {active_power['Total Load [W]'].std():.3f} W")
        print(f"  Median: {active_power['Total Load [W]'].median():.3f} W")
        
        # Check power distribution
        print(f"\nActive power distribution:")
        bins = [0.1, 1, 2, 3, 4, 5, 10, 100]
        for i in range(len(bins)-1):
            count = len(active_power[(active_power['Total Load [W]'] >= bins[i]) & 
                                     (active_power['Total Load [W]'] < bins[i+1])])
            pct = count / len(active_power) * 100
            print(f"  {bins[i]:.1f}-{bins[i+1]:.1f} W: {count:5d} rows ({pct:5.1f}%)")
    
    # 4. Analyze ON/OFF patterns by hour
    print("\n4. HOURLY ON/OFF PATTERNS")
    print("-" * 80)
    
    hourly_active = df[df['Total Load [W]'] > 0.1].groupby('Hour').size()
    hourly_total = df.groupby('Hour').size()
    
    print(f"{'Hour':<6} {'Active Min':<12} {'Total Min':<12} {'% Active':<10}")
    print("-" * 40)
    for hour in range(24):
        active_min = hourly_active.get(hour, 0)
        total_min = hourly_total.get(hour, 0)
        pct_active = (active_min / total_min * 100) if total_min > 0 else 0
        print(f"{hour:<6} {active_min:<12} {total_min:<12} {pct_active:<10.1f}%")
    
    # 5. Identify activation windows
    print("\n5. ACTIVATION WINDOWS (continuous ON periods)")
    print("-" * 80)
    
    # Mark ON/OFF states
    threshold = 0.1  # Anything > 0.1W is considered ON
    df['State'] = (df['Total Load [W]'] > threshold).astype(int)
    df['State_Change'] = df['State'].diff().fillna(0)
    
    window_starts = df[df['State_Change'] == 1].copy()
    window_ends = df[df['State_Change'] == -1].copy()
    
    print(f"Number of ON→OFF transitions: {len(window_starts)}")
    print(f"Number of OFF→ON transitions: {len(window_ends)}")
    
    if len(window_starts) > 0:
        print(f"\nFirst 10 window activations:")
        for i, row in window_starts.head(10).iterrows():
            end_row = None
            if i + 1 < len(df):
                # Find the next OFF transition
                next_off = df[df.index > i][df['State_Change'] == -1]
                if len(next_off) > 0:
                    end_row = next_off.iloc[0]
            
            duration = "?"
            if end_row is not None:
                duration = f"{(end_row.name - i) // 60} min" if (end_row.name - i) > 0 else "1 min"
            
            print(f"  {row['Time_str']} - {row['Total Load [W]']:.3f}W ({duration})")
    
    # 6. Check if 0.001W appears at EXACT window boundaries
    print("\n6. 0.001W AT WINDOW BOUNDARIES")
    print("-" * 80)
    
    ghost_and_transitions = df[(df['Total Load [W]'].between(0.0001, 0.002)) & 
                                (df['Power_Changed'] == True)]
    
    if len(ghost_and_transitions) > 0:
        print(f"Ghost power occurrences that are transitions: {len(ghost_and_transitions)}")
        print("\nFirst 10 examples:")
        print(ghost_and_transitions[['Time_str', 'Total Load [W]', 'Power_Diff']].head(10).to_string())
        print("\n→ This suggests 0.001W may be RAMP's initialization pulse at window start")
    else:
        print("No 0.001W values found at transitions")
        print("→ 0.001W may be occurring within active periods (noise)")
    
    # 7. Daily summary
    print("\n7. DAILY SUMMARY")
    print("-" * 80)
    
    df['Date'] = df['DateTime'].dt.date
    daily_stats = []
    
    for date in df['Date'].unique()[:7]:  # First 7 days
        day_data = df[df['Date'] == date]
        active_data = day_data[day_data['Total Load [W]'] > 0.1]
        
        total_active_min = len(active_data)
        mean_power = active_data['Total Load [W]'].mean() if len(active_data) > 0 else 0
        max_power = active_data['Total Load [W]'].max() if len(active_data) > 0 else 0
        
        daily_stats.append({
            'Date': date,
            'Active Minutes': total_active_min,
            'Mean Power (W)': mean_power,
            'Max Power (W)': max_power
        })
    
    daily_df = pd.DataFrame(daily_stats)
    print(daily_df.to_string(index=False))
    
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    print("""
If 0.001W appears at exact window boundaries:
  → This is likely RAMP's internal marker for window activation
  → It's NOT real power and can be filtered out (keep only > 0.01W)
  → It doesn't affect average power calculations significantly

If 0.001W appears randomly throughout:
  → Could be RAMP's numerical noise floor
  → Could be related to thermal_p_var if values are very small
  → Filtering to > 0.01W or > 0.1W recommended for analysis

If power variability is too high/low:
  → Check that thermal_p_var values are reasonable (0.1-0.2 typical)
  → Verify func_time matches expected daily usage
  → Check window sizes and occasional_use probabilities
    """)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze RAMP simulation output")
    parser.add_argument('--user', type=int, default=74, help='User ID')
    parser.add_argument('--config', type=str, default="manual", help='Config name')
    
    args = parser.parse_args()
    
    analyze_ramp_output(args.user, args.config)
