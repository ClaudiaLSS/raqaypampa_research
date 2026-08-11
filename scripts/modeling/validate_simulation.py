"""
validate_simulation.py
======================
Validates RAMP-simulated load profiles against empirical baseline profiles
(built by build_baseline_profiles.py) for the Raqaypampa profiles.

  Simulated (per profile):  simulation_results/profile_<pid>_minute.csv/parquet
                             (per household; averaged -> representative household)

  Baseline  (per profile):  baseline_results/baseline_profile_<id>.csv
                             columns: timestamp, power_w, n_users_contributing

Metrics
-------
Tier 1 (Error):        RMSE, LCSS score, MPDADA ratio
LDC (Duration-sorted):  LDC-RMSE (Tier 1's RMSE, computed on the duration-sorted
                       curve instead of the chronological one), P95 power (W)
Tier 2 (Structure):    Modal peak hour, average-curve peak, absolute max power,
                       MRSD chaos index
Tier 2 (Energy/Var):   Overall mean power, daily energy (Wh), base load 00-04h
Tier 2 (Macro windows):Morning / Daytime / Evening / Night mean loads

Plots
-----
1. Shadow + mean:  all daily curves faint, mean curve bold (real | sim panels)
2. Overlaid means: real vs sim average curves on one axis
3. Random week:    a continuous 7-day slice, real over sim
4. Load Duration Curve: real and sim daily curves, each sorted descending
   independently, plotted against fraction of day at or above that power
   level -- discards timing to isolate demand-level distribution fit

Usage
-----
    # validate simulated profile 1 against baseline profile 1, whole overlap
    python validate_simulation.py --baseline 1 --profile 1

    # only January, February, March
    python validate_simulation.py --baseline 1 --profile 1 --months 1 2 3
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Paths (overridable from the CLI)
# ---------------------------------------------------------------------------

DEFAULT_BASELINE_DIR = Path("..") / ".." / "data" / "clean" / "timeseries" / "baseline_results"
DEFAULT_SIM_DIR       = Path("simulation_results")

# Expected real-data sampling intervals (minutes). Used only to sanity-check
# the inferred interval_hours in calculate_structural_metrics; a real value
# far outside this set usually means the datalogger has gaps/drops that are
# silently inflating the median diff, which would quietly distort
# daily_energy_wh for the real side.
EXPECTED_REAL_INTERVALS_MIN = (5, 10)


def ensure_output_dirs(sim_dir: Path) -> tuple[Path, Path]:
    """Create and return (figures_dir, metrics_dir) under the sim output dir."""
    figures_dir = sim_dir / "figures"
    metrics_dir = sim_dir / "metrics"
    figures_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    return figures_dir, metrics_dir


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_real_baseline(baseline_profile_id: str, baseline_dir: Path) -> pd.DataFrame:
    """
    Load a pre-built empirical baseline (from build_baseline_profiles.py)
    as the "real" comparison series, instead of a single raw user file.

    Expects baseline_dir/baseline_profile_<id>.csv with columns:
        timestamp, power_w, n_users_contributing

    Rows where power_w is NaN (no contributing user had data at that
    timestamp) are dropped, with a warning, since they'd otherwise show
    up as spurious zero-load minutes.
    """
    print(f"\n[*] Loading empirical baseline for profile: {baseline_profile_id}")

    baseline_file = baseline_dir / f"baseline_profile_{baseline_profile_id}.csv"
    if not baseline_file.exists():
        print(f"[-] Error: baseline file not found: {baseline_file}")
        print("    Run build_baseline_profiles.py first to generate it.")
        sys.exit(1)

    df = pd.read_csv(baseline_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    n_total = len(df)
    n_nan = df["power_w"].isna().sum()
    df = df.dropna(subset=["power_w"])
    if n_nan > 0:
        print(
            f"[!] Warning: {n_nan}/{n_total} baseline rows ({n_nan / n_total:.1%}) had no "
            f"contributing users and were dropped."
        )

    if "n_users_contributing" in df.columns:
        avg_n_users = df["n_users_contributing"].mean()
        min_n_users = df["n_users_contributing"].min()
        print(
            f"[*] Baseline coverage: {avg_n_users:.1f} users/step on average "
            f"(min {min_n_users} at any single step)."
        )
        if min_n_users == 0:
            print(
                "[!] Warning: some retained rows have n_users_contributing == 0 despite "
                "a non-NaN power_w; check build_baseline_profiles.py output for consistency."
            )

    df["p_total"]      = df["power_w"]
    df["date_only"]    = df["timestamp"].dt.date
    df["time_decimal"] = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60.0

    print(
        f"[*] Loaded baseline: {len(df)} rows, "
        f"{df['date_only'].nunique()} days, mean={df['p_total'].mean():.2f} W"
    )
    return df[["timestamp", "p_total", "date_only", "time_decimal"]]


def load_sim_minute_average(profile_id: str, sim_dir: Path) -> tuple[pd.DataFrame, str]:
    """
    Default / explicit per-household path: always read the minute-level
    per-household file and average across households, producing one
    representative household's load curve - the correct comparison
    point for a single real user.
    """
    profile_name = f"PROFILE_{profile_id}"
    minute_parquet = sim_dir / f"profile_{profile_id}_minute.parquet"
    minute_csv     = sim_dir / f"profile_{profile_id}_minute.csv"

    src = None
    if minute_parquet.exists():
        src = minute_parquet
    elif minute_csv.exists():
        src = minute_csv
    else:
        print(f"[-] Error: per-household minute file not found for profile {profile_id}.")
        print(f"    Looked for: {minute_parquet.name}, {minute_csv.name}")
        print("    Run run_simulation.py first.")
        sys.exit(1)

    print(f"[*] Found simulated data: {src.name}  (per-household -> averaged to representative household)")
    df = pd.read_parquet(src) if src.suffix == ".parquet" else pd.read_csv(src)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    n_households = df["household_id"].nunique() if "household_id" in df.columns else None
    if n_households is not None:
        print(f"[*] Averaging across {n_households} simulated households at each minute.")

    df = df.groupby("timestamp", as_index=False)["power_w"].mean()

    df["p_total"]      = df["power_w"]
    df["date_only"]    = df["timestamp"].dt.date
    df["time_decimal"] = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60.0
    return df[["timestamp", "p_total", "date_only", "time_decimal"]], profile_name


def apply_time_filters(
    df_real: pd.DataFrame,
    df_sim: pd.DataFrame,
    target_months: list[int] | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply optional calendar-month filtering, mirroring the first engine."""
    if target_months is not None:
        print(f"[*] Limiting validation strictly to months: {target_months}")
        df_real = df_real[df_real["timestamp"].dt.month.isin(target_months)]
        df_sim  = df_sim[df_sim["timestamp"].dt.month.isin(target_months)]
        if df_real.empty or df_sim.empty:
            print("[-] Warning: missing data for selected months.")

    print(f"[+] Real data active: {df_real['date_only'].nunique()} days")
    print(f"[+] Sim data active:  {df_sim['date_only'].nunique()} days")

    if df_real.empty or df_sim.empty:
        print("[-] Cannot proceed: datasets are empty after filtering.")
        sys.exit(1)

    # Standardized 15-minute bins for smooth averaging (same as first engine)
    bins = np.arange(0, 24.25, 0.25)
    df_real = df_real.copy()
    df_sim  = df_sim.copy()
    df_real["time_bin"] = pd.cut(df_real["time_decimal"], bins, labels=bins[:-1])
    df_sim["time_bin"]  = pd.cut(df_sim["time_decimal"],  bins, labels=bins[:-1])

    return df_real, df_sim


# ---------------------------------------------------------------------------
# Plots (identical style to the first approach)
# ---------------------------------------------------------------------------

def plot_shadows_and_average(df_real, df_sim, real_label, profile_name, figures_dir):
    """Plot 1: all daily curves (faint) overlaid with the mean curve (bold)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    for d in df_real["date_only"].unique():
        day = df_real[df_real["date_only"] == d]
        ax1.plot(day["time_decimal"], day["p_total"], color="gray", alpha=0.08, linewidth=1)
    real_mean = df_real.groupby("time_bin", observed=True)["p_total"].mean()
    ax1.plot(real_mean.index.astype(float), real_mean.values,
             color="black", linewidth=3.5, label="Real Average Load")
    ax1.set_title(f"Real Measured Data ({real_label})\nDaily Variance vs Average",
                  fontsize=14, fontweight="bold")
    ax1.set_xlabel("Hour of the Day", fontsize=12)
    ax1.set_ylabel("Power Demand (W)", fontsize=12)
    ax1.set_xticks(np.arange(0, 25, 3))
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=11)
    ax1.set_ylim(bottom=0)

    for d in df_sim["date_only"].unique():
        day = df_sim[df_sim["date_only"] == d]
        ax2.plot(day["time_decimal"], day["p_total"], color="cornflowerblue", alpha=0.08, linewidth=1)
    sim_mean = df_sim.groupby("time_bin", observed=True)["p_total"].mean()
    ax2.plot(sim_mean.index.astype(float), sim_mean.values,
             color="darkblue", linewidth=3.5, label="Simulated Average Load")
    ax2.set_title(f"RAMP Simulation ({profile_name})\nDaily Variance vs Average",
                  fontsize=14, fontweight="bold")
    ax2.set_xlabel("Hour of the Day", fontsize=12)
    ax2.set_xticks(np.arange(0, 25, 3))
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=11)

    plt.tight_layout()
    out = figures_dir / f"val_shadows_mean_{real_label}_{profile_name.lower()}.png"
    plt.savefig(out, dpi=300)
    print(f"[+] Saved shadow plot: {out.name}")
    plt.close()


def plot_overlaid_averages(df_real, df_sim, real_label, profile_name, figures_dir):
    """Plot 2: real vs sim average curves overlaid on one axis."""
    plt.figure(figsize=(10, 6))
    real_mean = df_real.groupby("time_bin", observed=True)["p_total"].mean()
    sim_mean  = df_sim.groupby("time_bin", observed=True)["p_total"].mean()

    plt.plot(real_mean.index.astype(float), real_mean.values,
             color="black", linewidth=3, label="Measured Average Load")
    plt.plot(sim_mean.index.astype(float), sim_mean.values,
             color="darkblue", linewidth=3, linestyle="--", label="Simulated Average Load")

    plt.title(f"Overlay: Measured vs Simulated Average Load\n{real_label} | {profile_name}",
              fontsize=14, fontweight="bold")
    plt.xlabel("Hour of the Day", fontsize=12)
    plt.ylabel("Power Demand (W)", fontsize=12)
    plt.xticks(np.arange(0, 25, 3))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left", fontsize=12)
    plt.ylim(bottom=0)

    plt.tight_layout()
    out = figures_dir / f"val_overlay_mean_{real_label}_{profile_name.lower()}.png"
    plt.savefig(out, dpi=300)
    print(f"[+] Saved overlaid average plot: {out.name}")
    plt.close()


def plot_random_week(df_real, df_sim, real_label, profile_name, figures_dir, seed=None):
    """Plot 3: a continuous 7-day slice, real over sim."""
    if seed is not None:
        random.seed(seed)

    real_dates = sorted(df_real["date_only"].unique())
    sim_dates  = sorted(df_sim["date_only"].unique())

    if len(real_dates) < 7 or len(sim_dates) < 7:
        print("[-] Not enough days to plot a full week. Skipping weekly plot.")
        return

    r_start = random.randint(0, len(real_dates) - 8)
    s_start = random.randint(0, len(sim_dates) - 8)

    real_week = df_real[df_real["date_only"].isin(real_dates[r_start:r_start + 7])].copy()
    sim_week  = df_sim[df_sim["date_only"].isin(sim_dates[s_start:s_start + 7])].copy()

    real_week["hour_continuous"] = (
        (real_week["timestamp"] - real_week["timestamp"].min()).dt.total_seconds() / 3600.0
    )
    sim_week["hour_continuous"] = (
        (sim_week["timestamp"] - sim_week["timestamp"].min()).dt.total_seconds() / 3600.0
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True, sharey=True)
    ax1.plot(real_week["hour_continuous"], real_week["p_total"], color="black", linewidth=1.5)
    ax1.set_title(f"Real Measured Load: Continuous Random Week ({real_label})", fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylabel("Power (W)")

    ax2.plot(sim_week["hour_continuous"], sim_week["p_total"], color="blue", linewidth=1.5)
    ax2.set_title(f"RAMP Simulated Load: Continuous Random Week ({profile_name})", fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel("Hours (7 Days = 168 Hours)")
    ax2.set_ylabel("Power (W)")
    ax2.set_xticks(np.arange(0, 169, 24))

    plt.tight_layout()
    out = figures_dir / f"val_random_week_{real_label}_{profile_name.lower()}.png"
    plt.savefig(out, dpi=300)
    print(f"[+] Saved week plot: {out.name}")
    plt.close()


def plot_load_duration_curve(df_real, df_sim, real_label, profile_name, figures_dir):
    """
    Plot 4: Load Duration Curve (LDC).

    Takes the same 15-minute-binned representative daily curve used for
    Tier 1 (real_profile / sim_profile in calculate_validation_metrics),
    sorts each independently in descending order, and plots power (W)
    against the fraction of the day at or above that level. Unlike the
    chronological overlay (Plot 2), timing is discarded entirely here --
    this isolates whether the model reproduces the overall *distribution*
    of demand levels a household sits at, independent of when each level
    occurs during the day.

    Because each series is sorted independently, the two curves are not
    directly comparable minute-by-minute (see calculate_ldc_metrics for the
    LDC-RMSE statistic, which quantifies that comparison numerically).
    """
    real_profile = df_real.groupby("time_bin", observed=True)["p_total"].mean().fillna(0).values
    sim_profile  = df_sim.groupby("time_bin", observed=True)["p_total"].mean().fillna(0).values

    real_sorted = np.sort(real_profile)[::-1]
    sim_sorted  = np.sort(sim_profile)[::-1]

    pct_real = np.linspace(0, 100, len(real_sorted)) if len(real_sorted) else np.array([])
    pct_sim  = np.linspace(0, 100, len(sim_sorted))  if len(sim_sorted)  else np.array([])

    plt.figure(figsize=(10, 6))
    plt.plot(pct_real, real_sorted, color="black", linewidth=3, label="Measured Load Duration Curve")
    plt.plot(pct_sim, sim_sorted, color="darkblue", linewidth=3, linestyle="--",
             label="Simulated Load Duration Curve")

    plt.title(f"Load Duration Curve: Measured vs Simulated\n{real_label} | {profile_name}",
              fontsize=14, fontweight="bold")
    plt.xlabel("Fraction of Day at or Above Power Level (%)", fontsize=12)
    plt.ylabel("Power Demand (W)", fontsize=12)
    plt.xticks(np.arange(0, 101, 10))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper right", fontsize=12)
    plt.ylim(bottom=0)

    plt.tight_layout()
    out = figures_dir / f"val_ldc_{real_label}_{profile_name.lower()}.png"
    plt.savefig(out, dpi=300)
    print(f"[+] Saved LDC plot: {out.name}")
    plt.close()


# ---------------------------------------------------------------------------
# Metrics (identical formulas to the first approach)
# ---------------------------------------------------------------------------

def _infer_interval_hours(df: pd.DataFrame, label: str) -> float:
    """
    Infer the sampling interval (in hours) from the median timestamp
    diff, with a sanity check against EXPECTED_REAL_INTERVALS_MIN.

    A real-world datalogger with dropped/offline periods can have a
    median diff that jumps far above its true sampling interval (e.g.
    if enough gaps exist that "5 minutes" stops being the modal/median
    diff). That would silently inflate/deflate daily_energy_wh without
    raising an error, so we print a loud warning instead of failing
    silently.
    """
    interval_hours = df["timestamp"].diff().median().total_seconds() / 3600.0
    if pd.isna(interval_hours) or interval_hours <= 0:
        print(f"[!] Warning: could not infer a sampling interval for {label}; defaulting to 5 min.")
        return 5.0 / 60.0

    interval_min = interval_hours * 60.0
    closest = min(EXPECTED_REAL_INTERVALS_MIN, key=lambda m: abs(m - interval_min))
    if abs(closest - interval_min) > 0.5:  # more than 30s off the nearest expected interval
        print(
            f"[!] Warning: inferred sampling interval for {label} is {interval_min:.2f} min, "
            f"which doesn't closely match any expected interval {EXPECTED_REAL_INTERVALS_MIN}. "
            "This usually means there are gaps or irregular logging in this dataset, which can "
            "distort daily energy (Wh) figures for this series. Consider inspecting the raw "
            "timestamps for large gaps before trusting the energy metrics below."
        )
    return interval_hours


def calculate_structural_metrics(df: pd.DataFrame, label: str = "series") -> dict:
    """Tier 2 structural metrics, returning means and standard deviations."""
    daily_peak_idx = df.groupby("date_only")["p_total"].idxmax()
    peak_hours = df.loc[daily_peak_idx.dropna(), "timestamp"].dt.hour
    modal_peak_hour = int(peak_hours.mode()[0]) if not peak_hours.empty else 0

    night = df[(df["timestamp"].dt.hour >= 0) & (df["timestamp"].dt.hour < 4)]
    daily_night_mean = night.groupby("date_only")["p_total"].mean()
    base_mean = daily_night_mean.mean() if not daily_night_mean.empty else 0.0
    base_std  = daily_night_mean.std()  if not daily_night_mean.empty else 0.0

    interval_hours = _infer_interval_hours(df, label)

    daily_energy_wh = df.groupby("date_only")["p_total"].sum() * interval_hours
    wh_mean = daily_energy_wh.mean()
    wh_std  = daily_energy_wh.std()
    mrsd = (wh_std / wh_mean) if wh_mean > 0 else 0.0

    daily_mean_power = df.groupby("date_only")["p_total"].mean()
    overall_mean = daily_mean_power.mean() if not daily_mean_power.empty else 0.0
    overall_std  = daily_mean_power.std()  if not daily_mean_power.empty else 0.0

    periods = {"morning": (4, 10), "daytime": (10, 17), "evening": (17, 24), "night": (0, 4)}
    rmp = {}
    for name, (s_h, e_h) in periods.items():
        p = df[(df["timestamp"].dt.hour >= s_h) & (df["timestamp"].dt.hour < e_h)]
        dm = p.groupby("date_only")["p_total"].mean()
        rmp[f"{name}_mean"] = dm.mean() if not dm.empty else 0.0
        rmp[f"{name}_std"]  = dm.std()  if not dm.empty else 0.0

    return {
        "modal_peak": modal_peak_hour,
        "base_mean": base_mean, "base_std": base_std,
        "mrsd": mrsd, "wh_mean": wh_mean, "wh_std": wh_std,
        "overall_p_mean": overall_mean, "overall_p_std": overall_std,
        "rmp": rmp,
    }


def _lcss(real_profile: np.ndarray, sim_profile: np.ndarray, epsilon: float) -> float:
    """Longest Common Sub-Sequence score, normalized to [0, 1]."""
    n, m = len(real_profile), len(sim_profile)
    dp = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if abs(real_profile[i - 1] - sim_profile[j - 1]) <= epsilon:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m] / max(n, m) if max(n, m) > 0 else 0.0


def calculate_ldc_metrics(real_profile: np.ndarray, sim_profile: np.ndarray) -> dict:
    """
    LDC (Load Duration Curve) metrics, computed on the same 15-minute-binned
    representative daily curve as Tier 1, but sorted descending on each
    series independently before comparison.

    - ldc_rmse: same statistic as Tier 1's RMSE, computed on the
      duration-sorted curve instead of the chronological one. Comparing
      this against Tier 1 RMSE separates how much of a profile's error is
      attributable to *when* demand occurs (chronological RMSE) versus how
      well the model reproduces the *distribution* of demand levels
      regardless of timing (LDC-RMSE).
    - p95_real / p95_sim: the power level exceeded only 5% of the day for
      each series -- the quantity most directly relevant to sizing
      decisions (inverter rating, peak dispatch capacity), reported
      separately from the aggregate curve-fit statistic above.
    """
    real_sorted = np.sort(real_profile)[::-1]
    sim_sorted  = np.sort(sim_profile)[::-1]

    ldc_rmse = float(np.sqrt(np.mean((real_sorted - sim_sorted) ** 2))) if len(real_sorted) else 0.0
    p95_real = float(np.percentile(real_profile, 95)) if len(real_profile) else 0.0
    p95_sim  = float(np.percentile(sim_profile, 95))  if len(sim_profile)  else 0.0

    return {"ldc_rmse": ldc_rmse, "p95_real": p95_real, "p95_sim": p95_sim}


def calculate_validation_metrics(
    df_real, df_sim, real_label, profile_name, metrics_dir, epsilon_watts=0.5
) -> pd.DataFrame:
    """Dual-tier validation metrics, formatted into a table and saved as CSV."""
    print("\n[*] Calculating dual-tier validation metrics...")

    # TIER 1 — time-series alignment on the daily average profile
    real_profile = df_real.groupby("time_bin", observed=True)["p_total"].mean().fillna(0).values
    sim_profile  = df_sim.groupby("time_bin", observed=True)["p_total"].mean().fillna(0).values

    real_avg_peak = float(np.max(real_profile)) if len(real_profile) else 0.0
    sim_avg_peak  = float(np.max(sim_profile))  if len(sim_profile)  else 0.0
    real_abs_peak = float(df_real["p_total"].max())
    sim_abs_peak  = float(df_sim["p_total"].max())

    rmse = float(np.sqrt(np.mean((real_profile - sim_profile) ** 2)))
    mpdada = (
        abs(np.max(sim_profile) - np.max(real_profile)) / np.mean(real_profile)
        if np.mean(real_profile) > 0 else 0.0
    )
    lcss_score = _lcss(real_profile, sim_profile, epsilon_watts)

    # LDC — duration-sorted complement to Tier 1 (see calculate_ldc_metrics docstring)
    ldc = calculate_ldc_metrics(real_profile, sim_profile)

    # TIER 2 — structural profiling
    r = calculate_structural_metrics(df_real, label="real")
    s = calculate_structural_metrics(df_sim, label="simulated")

    def fmt_err(real_val, sim_val, unit="W"):
        abs_err = abs(real_val - sim_val)
        rel_err = (abs_err / real_val * 100) if real_val > 0 else 0.0
        return f"{abs_err:.2f} {unit} ({rel_err:.1f}%)"

    def fmt_mrsd_err():
        diff = abs(r["mrsd"] - s["mrsd"])
        rel = (diff / r["mrsd"] * 100) if r["mrsd"] > 0 else 0.0
        return f"{diff:.3f} ({rel:.1f}%)"

    rows = [
        {"Metric Group": "Tier 1: Error", "Metric": "RMSE (Watts)",
         "Real (Mean ± Std)": "—", "Sim (Mean ± Std)": f"{rmse:.3f}", "Mean Abs Error": "—"},
        {"Metric Group": "Tier 1: Error", "Metric": "LCSS Score",
         "Real (Mean ± Std)": "—", "Sim (Mean ± Std)": f"{lcss_score:.3f}", "Mean Abs Error": "—"},
        {"Metric Group": "Tier 1: Error", "Metric": "MPDADA Ratio",
         "Real (Mean ± Std)": "—", "Sim (Mean ± Std)": f"{mpdada:.3f}", "Mean Abs Error": "—"},

        {"Metric Group": "LDC: Duration-Sorted", "Metric": "LDC-RMSE (Watts)",
         "Real (Mean ± Std)": "—", "Sim (Mean ± Std)": f"{ldc['ldc_rmse']:.3f}", "Mean Abs Error": "—"},
        {"Metric Group": "LDC: Duration-Sorted", "Metric": "P95 Power (W)",
         "Real (Mean ± Std)": f"{ldc['p95_real']:.2f}", "Sim (Mean ± Std)": f"{ldc['p95_sim']:.2f}",
         "Mean Abs Error": fmt_err(ldc['p95_real'], ldc['p95_sim'], "W")},

        {"Metric Group": "Tier 2: Structure", "Metric": "Modal Peak Hour",
         "Real (Mean ± Std)": f"{r['modal_peak']:02d}:00",
         "Sim (Mean ± Std)": f"{s['modal_peak']:02d}:00",
         "Mean Abs Error": f"{abs(r['modal_peak'] - s['modal_peak'])} hrs"},
        {"Metric Group": "Tier 2: Structure", "Metric": "Average Curve Peak (W)",
         "Real (Mean ± Std)": f"{real_avg_peak:.2f}", "Sim (Mean ± Std)": f"{sim_avg_peak:.2f}",
         "Mean Abs Error": fmt_err(real_avg_peak, sim_avg_peak, "W")},
        {"Metric Group": "Tier 2: Structure", "Metric": "Absolute Max Power (W)",
         "Real (Mean ± Std)": f"{real_abs_peak:.2f}", "Sim (Mean ± Std)": f"{sim_abs_peak:.2f}",
         "Mean Abs Error": fmt_err(real_abs_peak, sim_abs_peak, "W")},
        {"Metric Group": "Tier 2: Structure", "Metric": "MRSD (Chaos Index)",
         "Real (Mean ± Std)": f"{r['mrsd']:.3f}", "Sim (Mean ± Std)": f"{s['mrsd']:.3f}",
         "Mean Abs Error": fmt_mrsd_err()},

        {"Metric Group": "Tier 2: Energy & Variance", "Metric": "Overall Mean Power (W)",
         "Real (Mean ± Std)": f"{r['overall_p_mean']:.2f} ± {r['overall_p_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['overall_p_mean']:.2f} ± {s['overall_p_std']:.2f}",
         "Mean Abs Error": fmt_err(r['overall_p_mean'], s['overall_p_mean'], "W")},
        {"Metric Group": "Tier 2: Energy & Variance", "Metric": "Daily Energy (Wh)",
         "Real (Mean ± Std)": f"{r['wh_mean']:.2f} ± {r['wh_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['wh_mean']:.2f} ± {s['wh_std']:.2f}",
         "Mean Abs Error": fmt_err(r['wh_mean'], s['wh_mean'], "Wh")},
        {"Metric Group": "Tier 2: Energy & Variance", "Metric": "Base Load (W) [00:00-04:00]",
         "Real (Mean ± Std)": f"{r['base_mean']:.2f} ± {r['base_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['base_mean']:.2f} ± {s['base_std']:.2f}",
         "Mean Abs Error": fmt_err(r['base_mean'], s['base_mean'], "W")},

        {"Metric Group": "Tier 2: Macro Windows", "Metric": "Morning Load (W) [04:00-10:00]",
         "Real (Mean ± Std)": f"{r['rmp']['morning_mean']:.2f} ± {r['rmp']['morning_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['rmp']['morning_mean']:.2f} ± {s['rmp']['morning_std']:.2f}",
         "Mean Abs Error": fmt_err(r['rmp']['morning_mean'], s['rmp']['morning_mean'], "W")},
        {"Metric Group": "Tier 2: Macro Windows", "Metric": "Daytime Load (W) [10:00-17:00]",
         "Real (Mean ± Std)": f"{r['rmp']['daytime_mean']:.2f} ± {r['rmp']['daytime_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['rmp']['daytime_mean']:.2f} ± {s['rmp']['daytime_std']:.2f}",
         "Mean Abs Error": fmt_err(r['rmp']['daytime_mean'], s['rmp']['daytime_mean'], "W")},
        {"Metric Group": "Tier 2: Macro Windows", "Metric": "Evening Peak (W) [17:00-24:00]",
         "Real (Mean ± Std)": f"{r['rmp']['evening_mean']:.2f} ± {r['rmp']['evening_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['rmp']['evening_mean']:.2f} ± {s['rmp']['evening_std']:.2f}",
         "Mean Abs Error": fmt_err(r['rmp']['evening_mean'], s['rmp']['evening_mean'], "W")},
        {"Metric Group": "Tier 2: Macro Windows", "Metric": "Night Load (W) [00:00-04:00]",
         "Real (Mean ± Std)": f"{r['rmp']['night_mean']:.2f} ± {r['rmp']['night_std']:.2f}",
         "Sim (Mean ± Std)": f"{s['rmp']['night_mean']:.2f} ± {s['rmp']['night_std']:.2f}",
         "Mean Abs Error": fmt_err(r['rmp']['night_mean'], s['rmp']['night_mean'], "W")},
    ]

    df_results = pd.DataFrame(rows)
    metrics_file = metrics_dir / f"validation_{real_label}_{profile_name.lower()}.csv"
    df_results.to_csv(metrics_file, index=False)

    print("\n" + "=" * 105)
    print(f" VALIDATION RESULTS: {real_label} vs {profile_name}")
    print("=" * 105)
    print(df_results[["Metric", "Real (Mean ± Std)", "Sim (Mean ± Std)", "Mean Abs Error"]]
          .to_string(index=False))
    print("=" * 105 + "\n")
    print(f"[+] Saved metrics table: {metrics_file.name}")

    return df_results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Validate a RAMP-simulated profile against an empirical baseline profile."
    )
    ap.add_argument("--baseline", type=str, required=True,
                    help="Baseline profile id to validate against (e.g. '1'), "
                         "from baseline_results/baseline_profile_<id>.csv")
    ap.add_argument("--profile", type=str, required=True,
                    help="Simulated profile id to validate (e.g. '1')")
    ap.add_argument("--months", type=int, nargs="+", choices=range(1, 13), default=None,
                    help="Limit validation to specific months (e.g. --months 1 2 3). "
                         "Default: use the full overlap between datasets.")
    args = ap.parse_args()

    figures_dir, metrics_dir = ensure_output_dirs(DEFAULT_SIM_DIR)

    df_real = load_real_baseline(args.baseline, DEFAULT_BASELINE_DIR)
    real_label = f"baseline_p{args.baseline}"

    df_sim, profile_name = load_sim_minute_average(args.profile, DEFAULT_SIM_DIR)

    # Filter
    df_real, df_sim = apply_time_filters(df_real, df_sim, args.months)

    # Plots
    plot_shadows_and_average(df_real, df_sim, real_label, profile_name, figures_dir)
    plot_overlaid_averages(df_real, df_sim, real_label, profile_name, figures_dir)
    plot_random_week(df_real, df_sim, real_label, profile_name, figures_dir)
    plot_load_duration_curve(df_real, df_sim, real_label, profile_name, figures_dir)

    # Metrics
    calculate_validation_metrics(df_real, df_sim, real_label, profile_name, metrics_dir)

    print("[+] Validation complete!")


if __name__ == "__main__":
    main()