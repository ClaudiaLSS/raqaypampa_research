"""
Script to explore seasonality patterns in measured load curves using Raqaypampa's rain-driven agricultural calendar.

RAIN-DRIVEN AGRICULTURE AND FOOD SECURITY:
Raqaypampa's economy is fundamentally driven by rain-fed agriculture (secano) spread across different
ecological altitudes. This reliance on rainfall creates a strict calendar that governs not only farming
and livestock management, but also the community's cultural, musical, social, and spiritual life.
Food security and community traditions are entirely dependent on this seasonal rhythm.

AGRICULTURAL AND LIVESTOCK CYCLES:
The calendar is directly tied to the arrival and patterns of the rains:

    PLANTING SEASON (October-January):
        Core Period: October-November (potatoes, maize; staple crops)
        Extension: January (wheat sowing)
        Cultural Marker: Mama Rosario festival (October) signals seasonal beginning
        Labor Demands: INTENSE and HOME-BASED
          - High labor demands; families must stay home to tend crops
          - Livestock management: actively controlled and shepherded to protect newly sown fields
          - Cannot migrate; animals must be watched during vulnerable early growth
        Energy Impact: MODERATE-HIGH (field work, animal tending, household presence)
        Musical Life: K'ullu Charangos (November-January)

    GROWING PERIOD (February-April):
        Characteristics: Entire rainy season with constant labor and crop care
        Cultural Events:
          - Carnival (Feb-Mar): rituals (qhupuyus) thanking Pachamama for growing crops
          - Harvesting begins in March, continues throughout the season
        Labor Demands: HIGH and CONTINUOUS
          - Constant attention required for crop care and protection
          - Peak labor intensity beginning as harvest approaches
          - Families remain home for active agricultural work
        Energy Impact: HIGH (ongoing field work, intensive crop care, harvest preparation)
        Musical Life: Tabla Charango & Much'a Flauta (Feb-April, rainy season instruments)

    MAIN HARVESTING SEASON (May-June):
        Climax Period: May-June 24 (San Juan festival)
        Critical Transition: June 24 marks END OF HARVEST and START OF ANDEAN NEW YEAR
        Cultural Significance:
          - San Juan (June 24): Ends harvest period; community celebration of completion
          - Chhalaku: Traditional barter system (high-altitude products ↔ valley goods)
          - Time for spiritual thanksgiving and community cohesion
        Labor Demands: VERY HIGH - PEAK INTENSITY
          - Heavy, intensive harvesting work across entire community
          - Highest physical labor demands of entire year
          - All family members mobilized for harvest completion
        Energy Impact: VERY HIGH (intensive harvesting, processing, food preservation)
        Musical Life: Laquitas with drums begin (June 24 - July, marking new year)

    LIVESTOCK FREE-GRAZING & MIGRATION PERIOD (Late June through September):
        Critical Transition Date: June 24 (San Juan)
        Free-Grazing Period: June 24 - October (full 4+ months)
        Communal Pasture: Entire territory becomes immense communal pasture
        Grazing System:
          - Animals (sheep, goats, cattle) released to graze freely on crop stubble (rastrojos)
          - Minimal shepherding required; animals mostly unsupervised
          - Natural landscape management through animal grazing
        Migration & Income Supplementation:
          - Temporary migration to regions like Chapare for supplementary income
          - SHORT trips after planting (early Oct); LONGER trips after harvest (Jul-Aug)
          - Families may be absent for extended periods (weeks to months)
          - Economic necessity alongside agricultural cycle
        Labor Demands: LOW - minimal active field work
          - No crops being tended; stubble provides pasture
          - Households often empty due to migration
          - Reduced domestic energy use from household absence
        Energy Impact: LOW (minimal field work, likely household absence, intermittent occupation)
        Musical Life: Lechewayos (late July-October), marking transition away from harvest

CULTURAL, SPIRITUAL, AND MUSICAL SYNCHRONIZATION:
Social and spiritual events are deeply synchronized with agricultural milestones:
  - Mama Rosario (October): Beginning of planting; community gathering and planning
  - Carnival (Feb-Mar): Thanksgiving to Pachamama; qhupuyus rituals during crop growth
  - San Juan (June 24): New Year marker; harvest completion; chhalaku barter exchange

Musical instruments are strictly regulated by season (indicator of cultural time):
  - Laquitas with drums: San Juan (June 24) through July
  - Lechewayos: Late July through October (transition to next planting cycle)
  - K'ullu Charangos: November through January (planting season)
  - Tabla Charango & Much'a Flauta: February-April (rainy season, exclusive use)

SOCIAL DYNAMICS, MIGRATION, AND EDUCATION DISCONNECTS:
The seasonal calendar reveals critical tensions with external systems:
  - Formal education fails to accommodate seasonal agricultural work
  - Teachers disconnect from community's seasonal, productive, and festive activities
  - State fiscal year deadlines are insensitive to local agricultural calendar
  - Government agricultural support programs poorly timed relative to actual cycles
  - Youth migration pressures inadvertently encouraged by educational system

CLIMATE CHANGE AND DISRUPTION:
The delicate seasonal balance is now under severe threat:
  - Traditional weather prediction (bio-indicators: plants, animals, stars) increasingly unreliable
  - Climate behaving erratically; traditional knowledge less predictive
  - Experiencing: shorter, more delayed rainy seasons; prolonged droughts
  - Impacts: disrupted planting calendar, soil erosion, reduced pasture availability
  - Food security directly threatened by climate unpredictability

Input: Real measured data from data/clean/timeseries/
Output: Seasonality analysis plots and statistics based on Raqaypampa's rain-driven agricultural calendar

Usage:
    python explore_seasonality.py --user 74                      # Full analysis
    python explore_seasonality.py --user 74 --season planting    # Planting season (Oct-Jan)
    python explore_seasonality.py --user 74 --season growing     # Growing period (Feb-Apr)
    python explore_seasonality.py --user 74 --season harvesting  # Main harvest (May-Jun 24)
    python explore_seasonality.py --user 74 --season grazing     # Free grazing & migration (Jun 24-Oct)
    python explore_seasonality.py --user 74 --month 7            # July only
    python explore_seasonality.py --user 74 --no-plots           # Statistics only
"""

import sys
import json
import argparse
import warnings
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats

# Suppress warnings
warnings.filterwarnings('ignore')

# Define paths matching project structure
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"
OUTPUT_DIR = SCRIPT_DIR / "output"
FIGURES_DIR = PROJECT_ROOT / "results" / "timeseries" / "figures"

# Ensure output directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_user_data(user_id):
    """Load measured data for a specific user."""
    data_file = INPUT_DIR / f"tpdin_user_{user_id}.csv"
    
    if not data_file.exists():
        print(f"Error: Data file not found: {data_file}")
        sys.exit(1)
    
    df = pd.read_csv(data_file)
    df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    
    # Calculate total power
    df['p_total'] = (df['v_led_1'] * df['c_led_1']).clip(lower=0) + \
                    (df['v_led_2'] * df['c_led_2']).clip(lower=0) + \
                    (df['v_usb'] * df['c_usb']).clip(lower=0)
    
    # Extract temporal features
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['month_name'] = df['timestamp'].dt.strftime('%B')
    df['day'] = df['timestamp'].dt.day
    df['weekday'] = df['timestamp'].dt.dayofweek
    df['weekday_name'] = df['timestamp'].dt.day_name()
    df['week'] = df['timestamp'].dt.isocalendar().week
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['date'] = df['timestamp'].dt.date
    df['time_decimal'] = df['hour'] + df['minute'] / 60.0
    
    print(f"✓ Loaded {len(df)} measurements from {data_file}")
    print(f"  Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"  Total days: {(df['timestamp'].max() - df['timestamp'].min()).days + 1}")
    
    return df


def compute_seasonality_statistics(df):
    """Compute seasonality statistics."""
    print("\n" + "="*80)
    print("SEASONALITY STATISTICS")
    print("="*80)
    
    # Monthly statistics
    print("\nMonthly Load Statistics:")
    print("-" * 80)
    monthly_stats = df.groupby('month_name')['p_total'].agg([
        ('Mean [W]', 'mean'),
        ('Std [W]', 'std'),
        ('Min [W]', 'min'),
        ('Max [W]', 'max'),
        ('Active Min', lambda x: (x > 0.1).sum()),  # Count of active 5-minute periods
    ])
    
    # Reorder by month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_stats = monthly_stats.reindex([m for m in month_order if m in monthly_stats.index])
    print(monthly_stats.to_string())
    
    # Weekly statistics
    print("\n\nWeekly Load Statistics:")
    print("-" * 80)
    weekly_stats = df.groupby('weekday_name')['p_total'].agg([
        ('Mean [W]', 'mean'),
        ('Std [W]', 'std'),
        ('Min [W]', 'min'),
        ('Max [W]', 'max'),
    ])
    
    # Reorder by weekday
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_stats = weekly_stats.reindex([d for d in weekday_order if d in weekly_stats.index])
    print(weekly_stats.to_string())
    
    # Hourly statistics
    print("\n\nHourly Load Statistics (Top 10 Hours):")
    print("-" * 80)
    hourly_stats = df.groupby('hour')['p_total'].agg([
        ('Mean [W]', 'mean'),
        ('Std [W]', 'std'),
        ('Min [W]', 'min'),
        ('Max [W]', 'max'),
    ]).sort_values('Mean [W]', ascending=False)
    print(hourly_stats.head(10).to_string())
    
    return monthly_stats, weekly_stats, hourly_stats


def add_raqaypampa_seasons(df):
    """Add Raqaypampa agricultural season labels based on month and date.
    
    Season boundaries synchronized to actual agricultural and cultural calendar:
    
        Planting (Oct 1 - Jan 31): 
            Oct-Nov: Core planting (potatoes, maize); Mama Rosario festival signals start
            Dec-Jan: Continued planting; wheat sowing in January
            Characteristics: Families home, livestock controlled, intense labor
            K'ullu Charangos played (Nov-Jan)
    
        Growing (Feb 1 - Apr 30): 
            Feb-Mar: Rainy season, crop care, Carnival rituals
            Apr: Continued harvest preparation
            Characteristics: Constant labor, high intensity, harvesting begins in March
            Tabla Charango & Much'a Flauta (rainy season instruments, Feb-Apr)
    
        Harvesting (May 1 - Jun 24): 
            May: Heavy harvesting work
            Jun 1-24: Harvest completion; San Juan (Jun 24) marks end and Andean New Year start
            Characteristics: Peak labor intensity, community-wide effort, chhalaku barter
            Laquitas with drums begin at June 24
    
        Grazing / Free-Grazing & Migration (Jun 24 - Oct 31):
            Jun 24: Critical transition - San Juan, animals released to communal pasture
            Jul-Sep: Extended free-grazing on rastrojos, migration for supplementary income
            Oct: Migration ends; grazing period ends; preparation for next planting
            Characteristics: Minimal field labor, household absence common, low energy use
            Lechewayos (late Jul-Oct); Laquitas early (Jun 24-Jul)
    """
    def month_day_to_season(row):
        month = row['month']
        day = row['day']
        
        # Critical boundary: June 24 (San Juan) marks transition to free-grazing period
        if month in [10, 11, 12, 1]:
            return 'Planting'
        elif month in [2, 3, 4]:
            return 'Growing'
        elif month == 5:
            return 'Harvesting'
        elif month == 6:
            # Before June 24: Harvesting; On/After June 24: Grazing (free-grazing & migration)
            return 'Harvesting' if day < 24 else 'Grazing'
        elif month in [7, 8, 9, 10]:
            return 'Grazing'
    
    df['raq_season'] = df.apply(month_day_to_season, axis=1)
    return df


def compute_raqaypampa_season_statistics(df):
    """Analyze load patterns across Raqaypampa's rain-driven agricultural seasons.
    
    This analysis reflects the actual work cycles, livestock management, migration patterns,
    cultural events, and food security dynamics that govern Raqaypampa's life.
    
    Key insights:
    - Planting season: Families must stay home to tend crops and control livestock
    - Growing period: Constant rainy-season labor for crop care and harvesting prep
    - Harvesting peak: Community-wide intensive labor until June 24 (San Juan)
    - Free-grazing: Animals released to communal pasture; families often migrate for income
    - Climate threat: Erratic rainfall disrupts traditional weather prediction methods
    """
    print("\n" + "="*80)
    print("RAQAYPAMPA RAIN-DRIVEN AGRICULTURAL SEASON ANALYSIS")
    print("="*80)
    print("\nSeason Definitions (synchronized to rain cycle and agricultural calendar):")
    print("  Planting (Oct-Jan):")
    print("    Oct-Nov: Core planting (potatoes, maize); Mama Rosario festival begins season")
    print("    Dec-Jan: Continued planting; wheat sowing in January")
    print("    Characteristics: Families HOME; livestock CONTROLLED; intense labor; cannot migrate")
    print("    Instruments: K'ullu Charangos (Nov-Jan)")
    print()
    print("  Growing (Feb-Apr):")
    print("    Feb-Mar: Rainy season crop care; Carnival rituals (qhupuyus) honoring Pachamama")
    print("    Apr: Harvest preparation continues")
    print("    Characteristics: Constant labor; rainy season; HIGH intensity; families home")
    print("    Instruments: Tabla Charango & Much'a Flauta (rainy season exclusive, Feb-Apr)")
    print()
    print("  Harvesting (May - Jun 24):")
    print("    May-Jun 23: Heavy, intensive harvesting across entire community")
    print("    Jun 24: SAN JUAN - CRITICAL TRANSITION")
    print("      - Ends harvest period and agricultural year")
    print("      - Marks Andean New Year beginning")
    print("      - Chhalaku: traditional barter of high-altitude/valley products")
    print("    Characteristics: PEAK labor intensity; community-wide mobilization; food preservation")
    print("    Instruments: Laquitas with drums BEGIN at San Juan (Jun 24)")
    print()
    print("  Free-Grazing & Migration (Jun 24 - Oct 31):")
    print("    (referred to as 'Grazing' season in analysis outputs)")
    print("    Jun 24 - Oct: Territory becomes COMMUNAL PASTURE")
    print("      - Animals released to graze freely on crop stubble (rastrojos)")
    print("      - Minimal shepherding; natural landscape management")
    print("    Migration for supplementary income:")
    print("      - SHORT trips: October (after planting setup)")
    print("      - LONGER trips: July-August (after harvest, extended absence possible)")
    print("      - Destination: Chapare region and other income-earning areas")
    print("    Characteristics: Minimal field labor; LIKELY household ABSENCE; low energy use")
    print("    Instruments: Lechewayos (late Jul-Oct); Laquitas early (Jun 24 - Jul)")
    print()
    print("Climate Change Impacts:")
    print("  - Shorter, more delayed rainy seasons disrupting traditional calendar")
    print("  - Prolonged droughts affecting crop and pasture availability")
    print("  - Erratic weather undermining traditional bio-indicator weather prediction")
    print("  - Food security threatened by increased unpredictability")
    
    # Define season order and colors for consistent visualization
    season_order = ['Planting', 'Growing', 'Harvesting', 'Grazing']
    season_colors = {
        'Planting': '#3498db',      # Blue
        'Growing': '#2ecc71',       # Green
        'Harvesting': '#e74c3c',    # Red
        'Grazing': '#f39c12'        # Orange
    }
    
    # Overall statistics by season
    print("\nLoad Statistics by Raqaypampa Season:")
    print("-" * 80)
    season_stats = df.groupby('raq_season')['p_total'].agg([
        ('Mean [W]', 'mean'),
        ('Median [W]', 'median'),
        ('Std [W]', 'std'),
        ('Min [W]', 'min'),
        ('Max [W]', 'max'),
        ('Active Days', lambda x: (x > 0.1).sum() / 288),  # 288 = 5-min intervals per day
    ])
    season_stats = season_stats.reindex([s for s in season_order if s in season_stats.index])
    print(season_stats.to_string())
    
    # Daily activity patterns by season
    print("\n\nDaily Activity Intensity by Season (Active Minutes per Day):")
    print("-" * 80)
    df_daily = df.groupby(['date', 'raq_season']).apply(
        lambda x: ((x['p_total'] > 0.1).sum() * 5)  # Convert to minutes
    ).reset_index()
    df_daily.columns = ['date', 'raq_season', 'active_minutes']
    
    activity_stats = df_daily.groupby('raq_season')['active_minutes'].agg([
        ('Mean [min/day]', 'mean'),
        ('Median [min/day]', 'median'),
        ('Std [min/day]', 'std'),
        ('Min [min/day]', 'min'),
        ('Max [min/day]', 'max'),
    ])
    activity_stats = activity_stats.reindex([s for s in season_order if s in activity_stats.index])
    print(activity_stats.to_string())
    
    # Peak load times by season
    print("\n\nPeak Load Hours by Season:")
    print("-" * 80)
    for season in season_order:
        season_data = df[df['raq_season'] == season]
        if len(season_data) > 0:
            peak_hour = season_data.groupby('hour')['p_total'].mean().idxmax()
            peak_val = season_data.groupby('hour')['p_total'].mean().max()
            print(f"  {season:12s}: Hour {peak_hour:02d}:00 (avg {peak_val:.2f} W)")
    
    # Migration indicator by season
    print("\n\nMigration Indicator - Low Activity Days (< 60 min/day):")
    print("-" * 80)
    low_activity = df_daily.groupby('raq_season').apply(
        lambda x: (x['active_minutes'] < 60).sum()
    )
    total_days = df_daily.groupby('raq_season').size()
    low_activity_pct = (low_activity / total_days * 100).round(1)
    
    for season in season_order:
        if season in low_activity.index:
            pct = low_activity_pct[season]
            print(f"  {season:12s}: {low_activity[season]:3d} low-activity days ({pct:5.1f}% of total)")
    
    print("\n  Note: High percentages in Grazing season (Jun 24-Oct) suggest free-grazing livestock period")
    print("        and migration for supplementary income - families often absent, minimal field labor.")
    
    return df


def plot_monthly_patterns(df, user_id):
    """Plot monthly load patterns."""
    print("\nGenerating monthly patterns plot...")
    
    # Prepare data by month
    bins = np.arange(0, 24.25, 0.25)
    df['time_bin'] = pd.cut(df['time_decimal'], bins, labels=bins[:-1])
    
    # Get hourly profiles for each month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    available_months = [m for m in month_order if m in df['month_name'].unique()]
    
    fig, axes = plt.subplots(3, 4, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, month_name in enumerate(available_months):
        ax = axes[idx]
        month_data = df[df['month_name'] == month_name]
        
        if len(month_data) > 0:
            hourly = month_data.groupby('time_bin', observed=True)['p_total'].mean()
            time_values = bins[:-1].astype(float)
            
            ax.plot(time_values[:len(hourly)], hourly.values, 
                   linewidth=2.5, color='steelblue', marker='o', markersize=4)
            ax.fill_between(time_values[:len(hourly)], hourly.values, alpha=0.3, color='steelblue')
            
            ax.set_title(f'{month_name}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=10)
            ax.set_ylabel('Power (W)', fontsize=10)
            ax.set_xticks(np.arange(0, 25, 4))
            ax.grid(True, linestyle=':', alpha=0.6)
    
    # Hide unused subplots
    for idx in range(len(available_months), len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle(f'Monthly Load Patterns - User {user_id}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"seasonality_monthly_patterns_user_{user_id}.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_monthly_heatmap(df, user_id):
    """Plot hour-by-month heatmap."""
    print("\nGenerating monthly heatmap...")
    
    # Create hour x month pivot
    bins = np.arange(0, 24.25, 0.25)
    df['time_bin'] = pd.cut(df['time_decimal'], bins, labels=bins[:-1])
    
    # Aggregate by hour and month
    hourly_monthly = df.groupby(['hour', 'month_name'])['p_total'].mean().reset_index()
    
    # Pivot to create heatmap
    heatmap_data = hourly_monthly.pivot(index='hour', columns='month_name', values='p_total')
    
    # Reorder columns by month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    heatmap_data = heatmap_data[[m for m in month_order if m in heatmap_data.columns]]
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='YlOrRd', cbar_kws={'label': 'Power (W)'}, ax=ax)
    
    ax.set_title(f'Hourly Load by Month - User {user_id}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Hour of Day', fontsize=12)
    
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"seasonality_monthly_heatmap_user_{user_id}.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_weekly_patterns(df, user_id):
    """Plot weekly load patterns by day of week."""
    print("\nGenerating weekly patterns plot...")
    
    bins = np.arange(0, 24.25, 0.25)
    df['time_bin'] = pd.cut(df['time_decimal'], bins, labels=bins[:-1])
    
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    available_days = [d for d in weekday_order if d in df['weekday_name'].unique()]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(available_days)))
    
    for idx, day_name in enumerate(available_days):
        ax = axes[idx]
        day_data = df[df['weekday_name'] == day_name]
        
        if len(day_data) > 0:
            hourly = day_data.groupby('time_bin', observed=True)['p_total'].mean()
            time_values = bins[:-1].astype(float)
            
            ax.plot(time_values[:len(hourly)], hourly.values, 
                   linewidth=2.5, color=colors[idx], marker='o', markersize=4)
            ax.fill_between(time_values[:len(hourly)], hourly.values, alpha=0.3, color=colors[idx])
            
            ax.set_title(f'{day_name}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=10)
            ax.set_ylabel('Power (W)', fontsize=10)
            ax.set_xticks(np.arange(0, 25, 4))
            ax.grid(True, linestyle=':', alpha=0.6)
    
    # Hide unused subplots
    for idx in range(len(available_days), len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle(f'Weekly Load Patterns - User {user_id}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"seasonality_weekly_patterns_user_{user_id}.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_monthly_comparison(df, user_id):
    """Plot comparison of average load across months."""
    print("\nGenerating monthly comparison plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Monthly mean power
    monthly_mean = df.groupby('month_name')['p_total'].mean()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_mean = monthly_mean.reindex([m for m in month_order if m in monthly_mean.index])
    
    axes[0].bar(range(len(monthly_mean)), monthly_mean.values, color='steelblue', alpha=0.7, edgecolor='black')
    axes[0].set_xticks(range(len(monthly_mean)))
    axes[0].set_xticklabels([m[:3] for m in monthly_mean.index], rotation=0)
    axes[0].set_title('Average Power by Month', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Power (W)', fontsize=11)
    axes[0].grid(True, axis='y', linestyle=':', alpha=0.6)
    
    # Monthly variability (std dev)
    monthly_std = df.groupby('month_name')['p_total'].std()
    monthly_std = monthly_std.reindex([m for m in month_order if m in monthly_std.index])
    
    axes[1].bar(range(len(monthly_std)), monthly_std.values, color='coral', alpha=0.7, edgecolor='black')
    axes[1].set_xticks(range(len(monthly_std)))
    axes[1].set_xticklabels([m[:3] for m in monthly_std.index], rotation=0)
    axes[1].set_title('Load Variability by Month (Std Dev)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Std Dev (W)', fontsize=11)
    axes[1].grid(True, axis='y', linestyle=':', alpha=0.6)
    
    plt.suptitle(f'Seasonal Comparison - User {user_id}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"seasonality_monthly_comparison_user_{user_id}.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def compute_rainy_dry_season_statistics(df):
    """Analyze load patterns differences between rainy and dry seasons.
    
    Rainy Season (Nov-Mar): Planting, land preparation, intensive agricultural work
    Dry Season (Apr-Oct): Harvesting, less rainfall, potential migration periods
    """
    print("\n" + "="*80)
    print("RAINY vs DRY SEASON ANALYSIS")
    print("="*80)
    print("\nSeason Definition:")
    print("  Rainy Season (Nov-Mar): Planting, land preparation, intensive work")
    print("  Dry Season (Apr-Oct): Harvesting, less rainfall, potential migration")
    
    # Define seasons
    df['rain_season'] = df['month'].isin([11, 12, 1, 2, 3]).map({True: 'Rainy', False: 'Dry'})
    
    # Overall statistics
    print("\nOverall Load Comparison:")
    print("-" * 80)
    season_stats = df.groupby('rain_season')['p_total'].agg([
        ('Mean [W]', 'mean'),
        ('Median [W]', 'median'),
        ('Std [W]', 'std'),
        ('Min [W]', 'min'),
        ('Max [W]', 'max'),
        ('Active Days', lambda x: (x > 0.1).sum() / 288),  # 288 = 5-min intervals per day
    ])
    print(season_stats.to_string())
    
    # Daily activity patterns
    print("\n\nDaily Activity Intensity (Active Minutes per Day):")
    print("-" * 80)
    df_daily = df.groupby(['date', 'rain_season']).apply(
        lambda x: ((x['p_total'] > 0.1).sum() * 5)  # Convert to minutes
    ).reset_index()
    df_daily.columns = ['date', 'rain_season', 'active_minutes']
    
    activity_stats = df_daily.groupby('rain_season')['active_minutes'].agg([
        ('Mean [min/day]', 'mean'),
        ('Median [min/day]', 'median'),
        ('Std [min/day]', 'std'),
        ('Min [min/day]', 'min'),
        ('Max [min/day]', 'max'),
    ])
    print(activity_stats.to_string())
    
    # Peak load times
    print("\n\nPeak Load Hours (when most active):")
    print("-" * 80)
    rainy_peak = df[df['rain_season'] == 'Rainy'].groupby('hour')['p_total'].mean().idxmax()
    dry_peak = df[df['rain_season'] == 'Dry'].groupby('hour')['p_total'].mean().idxmax()
    rainy_peak_val = df[df['rain_season'] == 'Rainy'].groupby('hour')['p_total'].mean().max()
    dry_peak_val = df[df['rain_season'] == 'Dry'].groupby('hour')['p_total'].mean().max()
    
    print(f"  Rainy Season: Hour {rainy_peak:02d}:00 (avg {rainy_peak_val:.2f} W)")
    print(f"  Dry Season:   Hour {dry_peak:02d}:00 (avg {dry_peak_val:.2f} W)")
    
    # Migration indicator: Days with very low activity
    print("\n\nMigration Indicator - Low Activity Days (< 60 min/day):")
    print("-" * 80)
    low_activity = df_daily.groupby('rain_season').apply(
        lambda x: (x['active_minutes'] < 60).sum()
    )
    total_days = df_daily.groupby('rain_season').size()
    low_activity_pct = (low_activity / total_days * 100).round(1)
    
    for season in ['Rainy', 'Dry']:
        if season in low_activity.index:
            print(f"  {season:5s} Season: {low_activity[season]:3d} low-activity days " +
                  f"({low_activity_pct[season]:5.1f}% of total)")
    
    return df


def plot_raqaypampa_season_comparison(df, user_id):
    """Compare load profiles across Raqaypampa's rain-driven agricultural seasons.
    
    Analyzes household energy patterns (measured lighting and appliance use) in relation
    to Raqaypampa's agricultural calendar:
    - Planting (Oct-Jan): Families home, livestock control, intense labor
    - Growing (Feb-Apr): Constant rainy season crop care, high activity
    - Harvesting (May-Jun 24): Peak community-wide harvesting work
    - Grazing (Jun 24-Oct): Free-grazing animals, migration for supplementary income, low labor
    """
    print("\nGenerating Raqaypampa rain-driven agricultural season comparison plot...")
    
    season_colors = {
        'Planting': '#3498db',      # Blue
        'Growing': '#2ecc71',       # Green
        'Harvesting': '#e74c3c',    # Red
        'Grazing': '#f39c12'        # Orange
    }
    season_order = ['Planting', 'Growing', 'Harvesting', 'Grazing']
    
    bins = np.arange(0, 24.25, 0.25)
    df['time_bin'] = pd.cut(df['time_decimal'], bins, labels=bins[:-1])
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    time_values = bins[:-1].astype(float)
    
    # Plot 1: Hourly profiles by season
    ax = axes[0, 0]
    for season in season_order:
        season_data = df[df['raq_season'] == season]
        if len(season_data) > 0:
            hourly = season_data.groupby('time_bin', observed=True)['p_total'].mean()
            ax.plot(time_values[:len(hourly)], hourly.values, 
                   linewidth=2.5, color=season_colors[season], marker='o', markersize=3,
                   label=season, alpha=0.8)
    
    ax.set_title('Average Hourly Load by Agricultural Season', fontsize=12, fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=11)
    ax.set_ylabel('Power (W)', fontsize=11)
    ax.set_xticks(np.arange(0, 25, 4))
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(fontsize=9, loc='upper left')
    
    # Plot 2: Daily activity distribution by season
    ax = axes[0, 1]
    df_daily = df.groupby(['date', 'raq_season']).apply(
        lambda x: ((x['p_total'] > 0.1).sum() * 5)
    ).reset_index()
    df_daily.columns = ['date', 'raq_season', 'active_minutes']
    
    activity_data = [df_daily[df_daily['raq_season'] == s]['active_minutes'].values 
                     for s in season_order if s in df_daily['raq_season'].unique()]
    activity_labels = [s for s in season_order if s in df_daily['raq_season'].unique()]
    activity_colors = [season_colors[s] for s in activity_labels]
    
    ax.hist(activity_data, bins=30, label=activity_labels, color=activity_colors, 
           alpha=0.7, edgecolor='black')
    ax.set_title('Distribution of Daily Activity Intensity', fontsize=12, fontweight='bold')
    ax.set_xlabel('Active Minutes per Day', fontsize=11)
    ax.set_ylabel('Frequency (# of days)', fontsize=11)
    ax.grid(True, axis='y', linestyle=':', alpha=0.6)
    ax.legend(fontsize=9)
    
    # Plot 3: Monthly bars colored by season
    ax = axes[1, 0]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_nums = list(range(1, 13))
    monthly_means = [df[df['month'] == m]['p_total'].mean() if len(df[df['month'] == m]) > 0 else 0 
                     for m in month_nums]
    month_seasons = []
    for m in month_nums:
        if m in [10, 11, 12, 1]:
            month_seasons.append('Planting')
        elif m in [2, 3, 4]:
            month_seasons.append('Growing')
        elif m in [5, 6]:
            month_seasons.append('Harvesting')
        elif m in [7, 8, 9]:
            month_seasons.append('Grazing')
    
    colors_by_month = [season_colors[s] for s in month_seasons]
    x = np.arange(len(months))
    
    ax.bar(x, monthly_means, color=colors_by_month, alpha=0.8, edgecolor='black')
    ax.set_title('Average Load by Month (Colored by Season)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Power (W)', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    ax.grid(True, axis='y', linestyle=':', alpha=0.6)
    
    # Plot 4: Migration indicator by season
    ax = axes[1, 1]
    low_activity = df_daily.groupby('raq_season').apply(
        lambda x: (x['active_minutes'] < 60).sum() / len(x) * 100
    )
    
    seasons_data = [low_activity.get(s, 0) for s in season_order]
    colors_bar = [season_colors[s] for s in season_order]
    
    bars = ax.bar(season_order, seasons_data, color=colors_bar, alpha=0.8, 
                 edgecolor='black', width=0.6)
    ax.set_title('Migration Indicator: Low Activity Days\n(< 60 min/day, typically Jun 24-Oct free-grazing period)', 
                fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage of Days (%)', fontsize=11)
    ax.grid(True, axis='y', linestyle=':', alpha=0.6)
    
    # Add value labels on bars
    for bar, val in zip(bars, seasons_data):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.suptitle(f'Raqaypampa Rain-Driven Agricultural Seasons: Impact on Household Energy Use and Work Patterns - User {user_id}', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"seasonality_raqaypampa_seasons_user_{user_id}.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def plot_rainy_dry_comparison(df, user_id):
    """Compare load profiles between rainy and dry seasons (legacy function)."""
    pass  # Function kept for backward compatibility, superseded by plot_raqaypampa_season_comparison()


def plot_raqaypampa_season_variability(df, user_id):
    """Analyze day-to-day variability across Raqaypampa's agricultural seasons."""
    print("\nGenerating rainy/dry season variability plot...")
    
    df_daily = df.groupby(['date', 'raq_season']).apply(
        lambda x: ((x['p_total'] > 0.1).sum() * 5)
    ).reset_index()
    df_daily.columns = ['date', 'raq_season', 'active_minutes']
    
    # Time series of daily activity
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    # Full time series
    ax = axes[0]
    season_colors = {
        'Planting': '#3498db',
        'Growing': '#2ecc71',
        'Harvesting': '#e74c3c',
        'Grazing': '#f39c12'
    }
    season_order = ['Planting', 'Growing', 'Harvesting', 'Grazing']
    
    for season in season_order:
        season_data = df_daily[df_daily['raq_season'] == season].set_index('date')
        if len(season_data) > 0:
            ax.scatter(season_data.index, season_data['active_minutes'], 
                      color=season_colors[season], s=30, alpha=0.6, label=season)
    
    # Add rolling average
    all_dates = sorted(df_daily['date'].unique())
    all_data = df_daily.set_index('date').loc[all_dates]
    rolling_avg = all_data['active_minutes'].rolling(window=7, center=True).mean()
    ax.plot(rolling_avg.index, rolling_avg.values, color='black', linewidth=2, alpha=0.5, label='7-day Moving Avg')
    
    ax.axhline(y=60, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Migration Threshold (60 min)')
    ax.set_title('Daily Activity Over Time by Raqaypampa Agricultural Season', fontsize=12, fontweight='bold')
    ax.set_ylabel('Active Minutes per Day', fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(fontsize=10, loc='upper left')
    
    # Box plot comparison
    ax = axes[1]
    activity_data = [df_daily[df_daily['raq_season'] == s]['active_minutes'].values 
                     for s in season_order if s in df_daily['raq_season'].unique()]
    activity_labels = [s for s in season_order if s in df_daily['raq_season'].unique()]
    
    bp = ax.boxplot(activity_data, labels=activity_labels, patch_artist=True, showmeans=True)
    
    # Color boxes
    for patch, season in zip(bp['boxes'], activity_labels):
        patch.set_facecolor(season_colors[season])
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Active Minutes per Day', fontsize=11)
    ax.set_title('Activity Level Distribution by Season', fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', linestyle=':', alpha=0.6)
    
    plt.suptitle(f'Raqaypampa Seasonal Variability in Work Patterns - User {user_id}', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig_file = FIGURES_DIR / f"seasonality_raqaypampa_variability_user_{user_id}.png"
    plt.savefig(fig_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {fig_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Explore seasonality patterns using Raqaypampa\'s agricultural calendar',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python explore_seasonality.py --user 74                          # Full analysis
  python explore_seasonality.py --user 74 --season planting        # Planting season (Oct-Jan)
  python explore_seasonality.py --user 74 --season growing         # Growing/harvest begins (Feb-Apr)
  python explore_seasonality.py --user 74 --season harvesting      # Main harvest (May-Jun)
  python explore_seasonality.py --user 74 --season grazing         # Free grazing & migration (Jul-Sep)
  python explore_seasonality.py --user 74 --month 7                # July only
  python explore_seasonality.py --user 74 --no-plots               # Statistics only
        """
    )
    
    parser.add_argument('--user', type=int, required=True, help='User ID')
    parser.add_argument('--month', type=int, help='Filter to specific month (1-12)')
    parser.add_argument('--season', choices=['planting', 'growing', 'harvesting', 'grazing'], 
                       help='Filter to specific agricultural season')
    parser.add_argument('--no-plots', action='store_true', help='Skip plot generation (stats only)')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("SEASONALITY ANALYSIS - RAQAYPAMPA AGRICULTURAL CALENDAR")
    print("="*80)
    
    # Load data
    df = load_user_data(args.user)
    
    # Add Raqaypampa agricultural seasons
    df = add_raqaypampa_seasons(df)
    
    # Filter by month if specified
    if args.month:
        df = df[df['month'] == args.month]
        print(f"\nFiltered to month {args.month} ({df['month_name'].iloc[0]})")
        print(f"Remaining measurements: {len(df)}")
    
    # Filter by season if specified
    season_descriptions = {
        'planting': 'Planting (Oct-Jan): Intensive labor, livestock control, families home',
        'growing': 'Growing (Feb-Apr): Constant crop care, harvest preparation, high labor',
        'harvesting': 'Harvesting (May-Jun): Heavy harvesting work, peak labor demands',
        'grazing': 'Grazing (Jul-Sep): Free-grazing animals, migration possible, low labor'
    }
    season_map = {
        'planting': 'Planting',
        'growing': 'Growing',
        'harvesting': 'Harvesting',
        'grazing': 'Grazing'
    }
    
    if args.season:
        season_name = season_map[args.season]
        df = df[df['raq_season'] == season_name]
        print(f"\nFiltered to {season_descriptions[args.season]}")
        print(f"Remaining measurements: {len(df)}")
    
    # Compute statistics
    compute_seasonality_statistics(df)
    
    # Raqaypampa season analysis
    df = compute_raqaypampa_season_statistics(df)
    
    # Generate plots
    if not args.no_plots:
        print("\n" + "="*80)
        print("GENERATING PLOTS")
        print("="*80)
        
        plot_monthly_patterns(df, args.user)
        plot_monthly_heatmap(df, args.user)
        plot_weekly_patterns(df, args.user)
        plot_monthly_comparison(df, args.user)
        plot_raqaypampa_season_comparison(df, args.user)
        plot_raqaypampa_season_variability(df, args.user)
        
        print(f"\n✓ All plots saved to: {FIGURES_DIR}")


if __name__ == '__main__':
    main()
