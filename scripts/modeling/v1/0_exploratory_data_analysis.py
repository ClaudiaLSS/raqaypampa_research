"""
Exploratory Data Analysis: Comprehensive Sociotechnical Profiling
Analyzes raw timeseries data to discover natural clustering across 8 key metrics:
Peak, Peak Hour, Night Safety, Chaos, Relative Power, Mean Power, Stacking, and Reliability.
Outputs descriptive statistics and raw distribution plots.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import sys

# Set academic plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.2)

# Define paths
SCRIPT_DIR = Path(__file__).parent if '__file__' in globals() else Path().absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"
PLOTS_DIR = SCRIPT_DIR / "output" / "plots"

# Ensure output directory exists
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Import your extractors
sys.path.append(str(SCRIPT_DIR))
from tpdin_extractor import TPDINExtractor
from old_extractor import OldExtractor

def detect_datalogger_type(filename):
    """Simple detector based on filename."""
    name = str(filename).lower()
    if 'tpdin' in name: return 'tpdin'
    if 'old' in name: return 'old'
    return 'unknown'

def main():
    print(f"Scanning raw timeseries data in: {INPUT_DIR.name}/...")

    # 1. Process raw files to generate the structural metrics on the fly
    summary_data = []
    raw_files = [f for f in INPUT_DIR.glob("*.csv") if 'blue' not in f.name.lower()]

    if not raw_files:
        print("No valid datalogger files found.")
        return

    for file in raw_files:
        dtype = detect_datalogger_type(file)
        if dtype == 'unknown': continue
            
        extractor = TPDINExtractor() if dtype == 'tpdin' else OldExtractor()
        
        try:
            # Preprocess
            df = extractor.preprocess(file)
            
            # Extract metrics from the 3 core base_extractor functions
            struct_metrics = extractor.extract_structural_metrics(df)
            stacking_metrics = extractor.extract_stacking_index(df, dtype)
            rel_metrics = extractor.extract_reliability_metrics(df)
            
            # Absolute Peak Power Calculation (Max wattage observed)
            peak_power_W = df['p_total'].max()
            
            # Flatten the nested dictionaries into a clean, single-level row
            metrics = {
                'user_id': file.stem.split('_')[-1],
                'datalogger_type': dtype,
                'peak_power_W': peak_power_W,
                'modal_peak_hour': struct_metrics['modal_peak_hour'],
                'safety_lights_probability': struct_metrics['safety_lights_probability'],
                'mrsd_chaos_index': struct_metrics['mrsd_chaos_index'],
                'rel_power_evening': struct_metrics['relative_mean_power']['evening'],
                'overall_mean_power_W': struct_metrics['overall_mean_power_W'],
                'stacking_index': stacking_metrics['stacking_index'] if stacking_metrics['stacking_index'] is not None else 0.0,
                'reliability_index_percent': rel_metrics['ri_percent'],
                'blackout_freq_100d': rel_metrics['bo_freq_events_per_100days']
            }
            summary_data.append(metrics)
            
        except Exception as e:
            print(f"Skipping {file.name} due to error: {e}")

    df_summary = pd.DataFrame(summary_data)
    n_users = len(df_summary)
    print(f"Successfully generated comprehensive metrics for {n_users} users!\n")
    
    # ---------------------------------------------------------
    # PRINT THE STATISTICAL OUTPUTS TO HELP YOU DEFINE THRESHOLDS
    # ---------------------------------------------------------
    print("==========================================================")
    print("EMPIRICAL DISTRIBUTION STATISTICS (Use these for thresholds)")
    print("==========================================================")
    
    metrics_to_analyze = [
        'peak_power_W',
        'modal_peak_hour',
        'safety_lights_probability', 
        'mrsd_chaos_index', 
        'rel_power_evening',
        'overall_mean_power_W',
        'stacking_index',
        'reliability_index_percent',
        'blackout_freq_100d'
    ]
    
    for metric in metrics_to_analyze:
        print(f"\n--- {metric.upper()} ---")
        print(f"Min:    {df_summary[metric].min():.2f}")
        print(f"25th %: {df_summary[metric].quantile(0.25):.2f}")
        print(f"Median: {df_summary[metric].median():.2f}")
        print(f"75th %: {df_summary[metric].quantile(0.75):.2f}")
        print(f"90th %: {df_summary[metric].quantile(0.90):.2f}")
        print(f"Max:    {df_summary[metric].max():.2f}")
    
    print("\n==========================================================")
    print("Generating and saving unclassified exploratory plots...")

    # ---------------------------------------------------------
    # Plot 1: Absolute Peak Power Distribution
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df_summary['peak_power_W'], bins=20, kde=True, color='darkred')
    plt.title(f'Distribution of Absolute Peak Power (Maximum Wattage) [N={n_users}]')
    plt.xlabel('Peak Power (W)')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '1_peak_power_distribution.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 2: Modal Peak Hour Count
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df_summary, x='modal_peak_hour', palette='viridis')
    plt.title(f'Modal Peak Hour of Usage [N={n_users}]')
    plt.xlabel('Hour of Day (24h)')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '2_peak_hour_distribution.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 3: Night Safety Lights Probability
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df_summary['safety_lights_probability'], bins=20, kde=True, color='orange')
    plt.title(f'Overnight Safety Light Probability (Midnight - 4AM) [N={n_users}]')
    plt.xlabel('Probability of Lights ON')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '3_safety_lights_distribution.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 4: MRSD Chaos Index
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df_summary['mrsd_chaos_index'], bins=20, kde=True, color='purple')
    plt.title(f'Distribution of Routine Chaos (MRSD Index) [N={n_users}]')
    plt.xlabel('MRSD Chaos Index')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '4_chaos_index_distribution.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 5: Relative Mean Power (Evening Stress)
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df_summary['rel_power_evening'], bins=20, kde=True, color='navy')
    plt.title(f'Evening Load Intensity (Multiplier of 24h Average) [N={n_users}]')
    plt.xlabel('Relative Evening Power')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '5_relative_evening_power.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 6: Overall Mean Power (Base Load)
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df_summary['overall_mean_power_W'], bins=20, kde=True, color='teal')
    plt.title(f'Base Load Distribution (Overall Mean Power) [N={n_users}]')
    plt.xlabel('Mean Power (W)')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '6_base_load_distribution.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 7: Appliance Stacking Index
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df_summary['stacking_index'], bins=20, kde=True, color='crimson')
    plt.title(f'Distribution of Appliance Stacking (Simultaneous Use) [N={n_users}]')
    plt.xlabel('Stacking Index (% of active time)')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '7_stacking_distribution.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # Plot 8: System Reliability vs. Blackout Frequency
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=df_summary, 
        x='blackout_freq_100d', 
        y='reliability_index_percent', 
        hue='overall_mean_power_W', 
        size='overall_mean_power_W',
        sizes=(50, 400),
        alpha=0.8,
        palette='magma'
    )
    plt.title(f'System Reliability vs. Blackout Frequency [N={n_users}]')
    plt.xlabel('Blackout Events (per 100 days)')
    plt.ylabel('Reliability Index (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Mean Power (W)")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '8_reliability_scatter.png', dpi=300)
    plt.close()

    print(f"✓ All 8 exploratory plots saved successfully to: {PLOTS_DIR}")

if __name__ == "__main__":
    main()