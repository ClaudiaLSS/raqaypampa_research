"""
Temporal-dynamics analysis for paper Section 5.1.

Two claims this supports:
  (1) P1 households are annually stable  -> expect ~0 absence days, no multi-day runs.
  (2) P4/P3 mobile households show absence -> characterise runs and where they fall,
      to test convergence against interview-documented absence windows.

Handles three logger formats automatically:
  - TPDIN : v_led_1,v_led_2,v_usb + c_led_1,c_led_2,c_usb   (p = LED1+LED2+USB)
  - OLD   : v_led_1,v_usb + c_led,c_usb                     (p = LED+USB)
  - BLUE  : v_led_1,c_cons                                  (p = v_led_1 * c_cons)

Sampling step is INFERRED from each file (do not assume 5 min).

Usage:
    python temporal_dynamics.py --user 72
    python temporal_dynamics.py --user 23 --low-frac 0.05 --min-run 3

Run every user with the SAME --low-frac and --min-run so the rule is uniform.
"""

import sys
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# --- resolved relative to the project root, regardless of the caller's cwd ---
PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = PROJECT_ROOT / "data" / "clean" / "timeseries"


def load_user_data(user_id):
    """Load one logger file (auto-detect prefix/format) and build p_total [W]."""
    data_file, logger_type = None, "UNKNOWN"
    for prefix in ["tpdin", "blue", "old"]:
        f = INPUT_DIR / f"{prefix}_user_{user_id}.csv"
        if f.exists():
            data_file, logger_type = f, prefix.upper()
            break
    if data_file is None:
        print(f"[-] No data file for user {user_id} in {INPUT_DIR} "
              f"(looked for tpdin_/blue_/old_ prefixes)")
        sys.exit(1)

    df = pd.read_csv(data_file)
    df['timestamp'] = pd.to_datetime(df['corrected_timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)

    zero = pd.Series(0.0, index=df.index)

    # --- format-aware power model ---
    if 'c_cons' in df.columns:
        # BLUE: single consumption-current channel; v_led_1 used as bus voltage
        v_bus = df.get('v_led_1', df.get('v_pv', zero))
        c_cons = df.get('c_cons', zero)
        df['p_total'] = (v_bus * c_cons).clip(lower=0)
        power_model = "BLUE (v_led_1 * c_cons)"
    else:
        # TPDIN / OLD: sum of LED (+ LED2) + USB channels
        v_usb   = df.get('v_usb', zero)
        c_usb   = df.get('c_usb', zero)
        v_led_1 = df.get('v_led_1', df.get('v_led', zero))
        c_led_1 = df.get('c_led_1', df.get('c_led', zero))   # OLD uses c_led
        v_led_2 = df.get('v_led_2', zero)
        c_led_2 = df.get('c_led_2', zero)

        p_led_1 = (v_led_1 * c_led_1).clip(lower=0)
        p_led_2 = (v_led_2 * c_led_2).clip(lower=0)
        p_usb   = (v_usb   * c_usb  ).clip(lower=0)
        df['p_total'] = p_led_1 + p_led_2 + p_usb
        power_model = "TPDIN/OLD (LED[+LED2]+USB)"

    print(f"Loaded {len(df):,} rows from {data_file.name} ({logger_type})")
    print(f"  Power model : {power_model}")
    print(f"  Date range  : {df['timestamp'].min()} -> {df['timestamp'].max()}")
    print(f"  Span        : {(df['timestamp'].max() - df['timestamp'].min()).days + 1} days")
    return df


def analyze_temporal_dynamics(df, user_id, low_frac=0.05, min_run_days=3):
    """Absence-run analysis on daily energy, with inferred sampling step."""
    print("\n" + "=" * 80)
    print(f"TEMPORAL DYNAMICS (Section 5.1) - User {user_id}")
    print("=" * 80)

    ts = df.set_index('timestamp')['p_total'].sort_index()

    # --- infer sampling step (median gap between samples), in minutes ---
    step_min = ts.index.to_series().diff().dt.total_seconds().median() / 60.0
    print(f"  Inferred sample step : {step_min:.2f} min")
    if not (0.5 <= step_min <= 60):
        print("  [!] Unusual step - check the file before trusting energy numbers.")

    # --- daily energy Wh/day = sum(power_W) * step_hours ---
    daily = ts.resample('D').apply(lambda s: s.sum() * (step_min / 60.0)).rename('Wh').to_frame()

    # --- keep only days that are >=70% sample-complete (format-agnostic) ---
    counts = ts.resample('D').count()
    expected = (24 * 60) / step_min
    valid_idx = counts[counts >= 0.7 * expected].index
    daily = daily[daily.index.isin(valid_idx)]
    daily['month'] = daily.index.month
    print(f"  Expected samples/full day : {expected:.0f}")
    print(f"  Valid days (>=70% complete): {len(daily)}")
    if len(daily) == 0:
        print("  [!] No valid days after completeness filter - aborting.")
        return daily, []

    # --- monthly stability table ---
    monthly = daily.groupby('month')['Wh'].agg(['mean', 'std', 'count'])
    monthly['cv'] = monthly['std'] / monthly['mean']
    print("\n  Monthly daily-energy (Wh/day):")
    print(monthly.round(2).to_string())
    if len(monthly) >= 2 and monthly['mean'].max() > 0:
        ratio = monthly['mean'].min() / monthly['mean'].max()
        print(f"\n  Lowest/highest month-mean ratio = {ratio:.2f} "
              f"(NOTE: energy magnitude is generation-confounded; "
              f"presence is the absence-run result below)")

    # --- low-usage flag (uniform stated rule) ---
    active_median = daily.loc[daily['Wh'] > 0, 'Wh'].median()
    thresh = low_frac * active_median
    daily['low'] = daily['Wh'] < thresh
    print(f"\n  Active-day median Wh        : {active_median:.2f}")
    print(f"  Low threshold ({int(low_frac*100)}% of median): {thresh:.2f} Wh")
    print(f"  Low-usage days              : {int(daily['low'].sum())} / {len(daily)} "
          f"({100*daily['low'].mean():.1f}%)")

    # --- contiguous low-usage runs (absence proxy; isolated low days excluded) ---
    runs = []
    start, length = None, 0
    for d, is_low in zip(daily.index, daily['low']):
        if is_low:
            start, length = (d, 1) if start is None else (start, length + 1)
        else:
            if start is not None and length >= min_run_days:
                runs.append((start, length))
            start, length = None, 0
    if start is not None and length >= min_run_days:
        runs.append((start, length))

    print(f"\n  Absence runs (>= {min_run_days} contiguous low days): {len(runs)}")
    if runs:
        lengths = [r[1] for r in runs]
        print(f"    Run lengths (d) : {sorted(lengths, reverse=True)}")
        print(f"    Median run (d)  : {np.median(lengths):.0f}")
        print(f"    Days in runs    : {sum(lengths)} ({100*sum(lengths)/len(daily):.1f}% of valid)")
        print("    Run start dates :")
        for s, l in runs:
            print(f"      {s.date()}  ({l} d)")

        # where do absent days fall (by month) + Dec-Feb window (for user 23)
        run_months = []
        for s, l in runs:
            run_months.extend(pd.date_range(s, periods=l, freq='D').month.tolist())
        rm = pd.Series(run_months)
        print("\n    Absent days by month:")
        for m in range(1, 13):
            n = int((rm == m).sum())
            if n:
                print(f"      month {m:2d}: {n:3d}")
        dec_feb = int(rm.isin([12, 1, 2]).sum())
        print(f"    Dec-Feb window  : {dec_feb}/{len(rm)} ({100*dec_feb/len(rm):.0f}%)")

    # periodicity of run onsets (for user 64's ~2-week alternation)
    if len(runs) >= 2:
        starts = [pd.Timestamp(r[0]) for r in runs]
        gaps = [(starts[i+1] - starts[i]).days for i in range(len(starts)-1)]
        print(f"\n    Gaps between run starts (d): {gaps}")
        print(f"    Median gap (d)  : {np.median(gaps):.0f}  (~14 => two-week alternation)")

    return daily, runs


def main():
    ap = argparse.ArgumentParser(description="Temporal-dynamics analysis (Section 5.1)")
    ap.add_argument('--user', type=int, required=True)
    ap.add_argument('--low-frac', type=float, default=0.05,
                    help="low-usage threshold as fraction of active-day median (default 0.05)")
    ap.add_argument('--min-run', type=int, default=3,
                    help="min contiguous low days to count as an absence run (default 3)")
    args = ap.parse_args()

    df = load_user_data(args.user)
    analyze_temporal_dynamics(df, args.user,
                              low_frac=args.low_frac, min_run_days=args.min_run)


if __name__ == '__main__':
    main()