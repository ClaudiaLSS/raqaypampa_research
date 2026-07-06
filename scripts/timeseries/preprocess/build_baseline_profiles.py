"""
build_baseline_profiles.py
===========================
Pre-processes raw datalogger files (both 'old' and 'tpdin' formats) into a
single empirical baseline load curve per user profile, to be used as the
ground truth for RAMP validation (validate_simulation.py).

Why this exists
----------------
validate_simulation.py compares one simulated profile against one real
user. But your real dataloggers come in two native resolutions (tpdin =
5-min steps, old = 10-min steps) and you often want to combine SEVERAL
real users into one representative "baseline" curve per profile, over a
specific time window (a whole year, a single month, a season...). This
script does that combination step once, up front, so validate_simulation.py
(or any other analysis) can just read one clean CSV per profile.

What it does
------------
1. Reads a JSON config telling it, per profile: which raw files to use and
   what time period to use as the baseline (full year / specific months /
   an explicit date range).
2. For each raw file, auto-detects its format (old vs tpdin) from the
   filename (overridable), reconstructs total power from the v_*/c_*
   channels, and snaps its (possibly jittery) timestamps onto a clean
   regular grid at the file's OWN native resolution.
3. Per profile, finds the finest (smallest) native resolution among the
   files assigned to it -- e.g. if a profile mixes tpdin (5 min) and old
   (10 min) files, the target grid is 5 min, per your instruction to keep
   the highest available resolution. Coarser files are upsampled onto that
   finer grid via time-based linear interpolation, but ONLY within a
   single native interval -- the script never fabricates data across a
   real gap bigger than one native step.
4. Averages across all users assigned to a profile, row-wise, at each grid
   timestamp (skipping users with missing data at that timestamp rather
   than treating missing as zero), producing one representative curve.
5. Writes one CSV per profile: baseline_profile_<id>.csv with columns
    timestamp, power_w, n_users_contributing.

By default, the script aligns all timestamps on a synthetic calendar year
so curves from different real years still line up by month/day/time.
Pass --align_by timestamp to keep the original year-specific behavior.

Config file format (JSON)
--------------------------
{
  "raw_dir": "data/clean/timeseries",
  "output_dir": "baseline_results",
  "profiles": {
    "1": {
      "files": ["tpdin_user_74.csv", "tpdin_user_82.csv"],
      "period": {"type": "full_year", "year": 2024}
    },
    "2": {
      "files": ["old_user_12.csv"],
      "period": {"type": "months", "year": 2024, "months": [3, 4]}
    },
    "3": {
      "files": ["tpdin_user_55.csv", "old_user_60.csv"],
      "period": {"type": "date_range", "start": "2024-01-01", "end": "2024-01-31"}
    },
    "4": {
      "files": ["tpdin_user_99.csv"],
      "period": {"type": "full_year", "year": 2024}
    }
  }
}

period.type options:
  "full_year"    -> requires "year" (int); a plain Jan-Dec calendar year.
  "months"       -> requires "year" (int) and "months" (ORDERED list of 1-12).
                    The list is read in the order given, not sorted: if a
                    later month is smaller than the one before it, the year
                    is assumed to roll over. E.g. {"year": 2024, "months":
                    [10, 11, 12, 1]} means Oct-Dec 2024 + Jan 2025 (a
                    planting season spanning a year boundary).
  "date_range"   -> requires "start" and "end" ("YYYY-MM-DD" strings,
                    inclusive). The most flexible option -- use this for
                    any period that isn't a clean calendar year or a short
                    list of months, e.g. a full "agricultural year" like
                    2024-10-01 to 2025-09-30.

Usage
-----
    # Generate an example config to edit, then exit
    python build_baseline_profiles.py --write_example_config baseline_config.json

    # Run using a config file
    python build_baseline_profiles.py --config baseline_config.json

    # Override raw/output dirs from the CLI (takes precedence over the config file)
    python build_baseline_profiles.py --config baseline_config.json \
        --raw_dir data/clean/timeseries --output_dir baseline_results
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Format detection & native resolution
# ---------------------------------------------------------------------------

ANCHOR_YEAR = 2000
NATIVE_STEP_MINUTES = {"old": 10, "tpdin": 5}


def detect_format(filename: str) -> str:
    """Infer 'old' vs 'tpdin' from the filename. Raise if ambiguous."""
    name = filename.lower()
    if "tpdin" in name:
        return "tpdin"
    if "old" in name:
        return "old"
    raise ValueError(
        f"Could not infer datalogger format ('old' or 'tpdin') from filename "
        f"'{filename}'. Rename the file to include 'old' or 'tpdin', or add "
        f"an explicit \"format\": \"old\"/\"tpdin\" field for this file in "
        f"the config."
    )


def _month_day_time_key(ts: pd.Timestamp) -> tuple[int, int, int, int, int, int]:
    return (ts.month, ts.day, ts.hour, ts.minute, ts.second, ts.microsecond)


def _anchor_timestamp(ts: pd.Timestamp, year: int) -> pd.Timestamp:
    return ts.replace(year=year)


def _build_month_year_map(months: list[int], base_year: int) -> dict[int, int]:
    month_year_map: dict[int, int] = {}
    current_year = base_year
    prev_month = None
    for month in months:
        if prev_month is not None and month < prev_month:
            current_year += 1
        month_year_map.setdefault(month, current_year)
        prev_month = month
    return month_year_map


def normalize_timestamp_for_alignment(ts: pd.Timestamp, period_cfg: dict, align_by: str) -> pd.Timestamp:
    if align_by == "timestamp":
        return ts

    ptype = period_cfg.get("type")

    if ptype == "full_year":
        return _anchor_timestamp(ts, ANCHOR_YEAR)

    if ptype == "months":
        month_year_map = _build_month_year_map(period_cfg["months"], ANCHOR_YEAR)
        return _anchor_timestamp(ts, month_year_map.get(ts.month, ANCHOR_YEAR))

    if ptype == "date_range":
        start = pd.Timestamp(period_cfg["start"])
        end = pd.Timestamp(period_cfg["end"])
        crosses_year = _month_day_time_key(end) < _month_day_time_key(start)
        year = ANCHOR_YEAR + 1 if crosses_year and _month_day_time_key(ts) < _month_day_time_key(start) else ANCHOR_YEAR
        return _anchor_timestamp(ts, year)

    raise ValueError(f"Unsupported period.type '{ptype}' for timestamp normalization.")


# ---------------------------------------------------------------------------
# Power reconstruction (mirrors validate_simulation.py's logic)
# ---------------------------------------------------------------------------

def reconstruct_power(df: pd.DataFrame) -> pd.Series:
    """
    Reconstruct total power (W) from raw voltage/current channels.
    Handles both the tpdin format (v_led_1/c_led_1, v_led_2/c_led_2,
    v_usb/c_usb) and the old single-LED format (v_led/c_led), defaulting
    any missing channel to zero.
    """
    zero = pd.Series(0.0, index=df.index)

    v_usb   = df.get("v_usb",   zero)
    c_usb   = df.get("c_usb",   zero)
    v_led_1 = df.get("v_led_1", df.get("v_led", zero))
    c_led_1 = df.get("c_led_1", df.get("c_led", zero))
    v_led_2 = df.get("v_led_2", zero)
    c_led_2 = df.get("c_led_2", zero)

    p_led_1 = (v_led_1 * c_led_1).clip(lower=0)
    p_led_2 = (v_led_2 * c_led_2).clip(lower=0)
    p_usb   = (v_usb   * c_usb).clip(lower=0)

    return p_led_1 + p_led_2 + p_usb


# ---------------------------------------------------------------------------
# Period parsing
# ---------------------------------------------------------------------------

def parse_period(period_cfg: dict, align_by: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    """
    Turn a period config block into an inclusive (start, end) timestamp
    range covering the whole end day (i.e. end is set to 23:59:59 of the
    last day) so date_range-based grids include every timestep of the
    final day.

    For "months", the list is treated as an ORDERED sequence (not sorted)
    starting in "year". Whenever a month value is smaller than the one
    before it in the list, the year is assumed to have rolled over -- this
    lets you express a season that crosses a calendar year boundary, e.g.
    a planting season of Oct-Jan as {"year": 2024, "months": [10, 11, 12, 1]}
    which resolves to Oct-Dec 2024 + Jan 2025.
    """
    ptype = period_cfg.get("type")

    if ptype == "full_year":
        year = period_cfg["year"]
        if align_by == "timestamp":
            start = pd.Timestamp(year=year, month=1, day=1)
            end = pd.Timestamp(year=year, month=12, day=31, hour=23, minute=59, second=59)
        else:
            start = pd.Timestamp(year=ANCHOR_YEAR, month=1, day=1)
            end = pd.Timestamp(year=ANCHOR_YEAR, month=12, day=31, hour=23, minute=59, second=59)

    elif ptype == "months":
        months = period_cfg["months"]
        if not months:
            raise ValueError("period.months is empty.")

        # Build (year, month) pairs in LIST ORDER, rolling the year forward
        # whenever the month value drops below the previous one (wraparound).
        year_month_pairs = []
        current_year = period_cfg.get("year", ANCHOR_YEAR) if align_by == "timestamp" else ANCHOR_YEAR
        prev_month = None
        for m in months:
            if prev_month is not None and m < prev_month:
                current_year += 1
            year_month_pairs.append((current_year, m))
            prev_month = m

        first_year, first_month = year_month_pairs[0]
        last_year, last_month = year_month_pairs[-1]
        start = pd.Timestamp(year=first_year, month=first_month, day=1)
        end = (pd.Timestamp(year=last_year, month=last_month, day=1) + pd.offsets.MonthEnd(1))
        end = end.replace(hour=23, minute=59, second=59)

        # Contiguity check: does the (possibly wrapping) month sequence form
        # an unbroken run, e.g. [10, 11, 12, 1] rather than [10, 12, 1]?
        expected_month = first_month
        is_contiguous = True
        for m in months:
            if m != expected_month:
                is_contiguous = False
                break
            expected_month = expected_month + 1 if expected_month < 12 else 1
        if not is_contiguous:
            print(
                f"[!] Warning: period.months={months} is not a contiguous run "
                f"(in the order given). The date grid will span {start.date()} "
                f"to {end.date()}, but only the listed months' rows will "
                f"actually be included -- double check this is what you intend."
            )
        if year_month_pairs[-1][0] > year_month_pairs[0][0]:
            print(
                f"[*] Note: period.months spans a year boundary: "
                f"{year_month_pairs[0]} to {year_month_pairs[-1]} "
                f"(i.e. {start.date()} to {end.date()})."
            )

    elif ptype == "date_range":
        start = pd.Timestamp(period_cfg["start"])
        end = pd.Timestamp(period_cfg["end"]).replace(hour=23, minute=59, second=59)
        if align_by != "timestamp":
            year_span = end.year - start.year
            start = _anchor_timestamp(start, ANCHOR_YEAR)
            end = _anchor_timestamp(end, ANCHOR_YEAR + year_span)

    else:
        raise ValueError(
            f"Unknown period.type '{ptype}'. Expected 'full_year', 'months', "
            f"or 'date_range'."
        )


    if end <= start:
        raise ValueError(f"Period end ({end}) is not after start ({start}).")

    return start, end


# ---------------------------------------------------------------------------
# Per-file loading and gridding
# ---------------------------------------------------------------------------

def load_and_grid_file(
    file_path: Path,
    fmt: str,
    native_step_min: int,
    target_step_min: int,
    full_range: pd.DatetimeIndex,
    period_cfg: dict,
    align_by: str,
) -> pd.Series:
    """
    Load one raw file, reconstruct power, snap it onto its native-resolution
    grid, then (if needed) upsample onto the profile's target grid, and
    finally reindex onto the shared full_range so it can be averaged
    column-wise against other users.

    Returns a pd.Series indexed by full_range, with NaN wherever this file
    has no (or out-of-period) data.
    """
    print(f"    - {file_path.name} (format={fmt}, native step={native_step_min} min)")

    df = pd.read_csv(file_path)
    n_raw = len(df)

    ts_col = "corrected_timestamp" if "corrected_timestamp" in df.columns else "timestamp"
    df["timestamp"] = pd.to_datetime(df[ts_col], errors="coerce")
    n_bad = df["timestamp"].isna().sum()
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    if n_bad > 0:
        print(f"      [!] Dropped {n_bad}/{n_raw} rows with unparseable timestamps.")

    if align_by != "timestamp":
        df["timestamp"] = df["timestamp"].map(
            lambda ts: normalize_timestamp_for_alignment(ts, period_cfg, align_by)
        )
        df = df.sort_values("timestamp")

    df["p_total"] = reconstruct_power(df)
    df = df.set_index("timestamp")[["p_total"]]

    # 1. Snap onto this file's own native grid (handles jitter/duplicates).
    native_series = df["p_total"].resample(f"{native_step_min}min").mean()

    # 2. Restrict to the requested period BEFORE upsampling, so we don't
    #    interpolate across the period boundary using out-of-period data.
    start, end = parse_period(period_cfg, align_by)
    native_series = native_series[(native_series.index >= start) & (native_series.index <= end)]
    if period_cfg.get("type") == "months":
        native_series = native_series[native_series.index.month.isin(period_cfg["months"])]

    if native_series.dropna().empty:
        print(f"      [!] Warning: no data for {file_path.name} within the requested period.")
        return pd.Series(np.nan, index=full_range)

    # 3. Upsample to the profile's target grid if this file's native
    #    resolution is coarser than the target. Only interpolate within a
    #    single native interval, so we never fabricate values across a
    #    real gap in the data.
    if native_step_min > target_step_min:
        limit_steps = max(1, native_step_min // target_step_min - 1)
        target_index_for_file = pd.date_range(
            native_series.index.min(), native_series.index.max(), freq=f"{target_step_min}min"
        )
        fine_series = native_series.reindex(
            native_series.index.union(target_index_for_file)
        ).interpolate(method="time", limit=limit_steps, limit_area="inside")
        fine_series = fine_series.reindex(target_index_for_file)
        print(
            f"      Upsampled from {native_step_min} min to {target_step_min} min "
            f"(linear interpolation, max gap filled = {limit_steps} step(s))."
        )
    else:
        fine_series = native_series

    # 4. Reindex onto the shared full_range so every file/user lines up on
    #    exactly the same timestamps for averaging.
    aligned = fine_series.reindex(full_range)
    n_missing = aligned.isna().sum()
    coverage = 1 - (n_missing / len(full_range))
    print(f"      Coverage of requested period: {coverage:.1%} ({len(full_range) - n_missing}/{len(full_range)} steps)")

    return aligned


# ---------------------------------------------------------------------------
# Per-profile baseline construction
# ---------------------------------------------------------------------------

def build_baseline_for_profile(
    profile_id: str,
    profile_cfg: dict,
    raw_dir: Path,
    output_dir: Path,
    align_by: str,
) -> None:
    print(f"\n[*] Building baseline for Profile {profile_id}...")

    files = profile_cfg["files"]
    period_cfg = profile_cfg["period"]
    if not files:
        print(f"[-] Profile {profile_id}: no files listed, skipping.")
        return

    # Resolve format + native step per file (config can override auto-detection
    # with an explicit {"file": "...", "format": "old"} entry; plain filename
    # strings use auto-detection).
    resolved_files = []
    for entry in files:
        if isinstance(entry, dict):
            fname = entry["file"]
            fmt = entry.get("format") or detect_format(fname)
        else:
            fname = entry
            fmt = detect_format(fname)
        resolved_files.append((fname, fmt))

    native_steps = [NATIVE_STEP_MINUTES[fmt] for _, fmt in resolved_files]
    target_step_min = min(native_steps)
    print(
        f"[*] Files: {[f for f, _ in resolved_files]}"
        f" -> native steps {native_steps} min -> target grid = {target_step_min} min"
    )

    start, end = parse_period(period_cfg, align_by)
    full_range = pd.date_range(start, end, freq=f"{target_step_min}min")
    if period_cfg.get("type") == "months":
        full_range = full_range[full_range.month.isin(period_cfg["months"])]
    print(f"[*] Baseline period: {start.date()} to {end.date()} ({len(full_range)} grid steps)")

    per_user_series = {}
    for fname, fmt in resolved_files:
        file_path = raw_dir / fname
        if not file_path.exists():
            print(f"[-] Error: file not found: {file_path}. Skipping this file.")
            continue
        native_step_min = NATIVE_STEP_MINUTES[fmt]
        series = load_and_grid_file(
            file_path, fmt, native_step_min, target_step_min, full_range, period_cfg, align_by
        )
        per_user_series[fname] = series

    if not per_user_series:
        print(f"[-] Profile {profile_id}: no usable files loaded, skipping output.")
        return

    combined = pd.DataFrame(per_user_series)
    baseline_power = combined.mean(axis=1, skipna=True)
    n_users_contributing = combined.notna().sum(axis=1)

    out_df = pd.DataFrame({
        "timestamp": full_range,
        "power_w": baseline_power.values,
        "n_users_contributing": n_users_contributing.values,
    })

    n_total_users = len(per_user_series)
    fully_missing = (n_users_contributing == 0).sum()
    if fully_missing > 0:
        print(
            f"[!] Warning: {fully_missing}/{len(full_range)} grid steps have NO "
            f"contributing users (all files missing data there). power_w will be "
            f"NaN for those rows."
        )
    partial = ((n_users_contributing > 0) & (n_users_contributing < n_total_users)).sum()
    if partial > 0:
        print(
            f"[*] Note: {partial}/{len(full_range)} grid steps are averaged over "
            f"fewer than all {n_total_users} assigned users (partial coverage)."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"baseline_profile_{profile_id}.csv"
    out_df.to_csv(out_path, index=False)

    valid = baseline_power.dropna()
    print(
        f"[+] Saved: {out_path} | mean={valid.mean():.2f} W  "
        f"peak={valid.max():.2f} W  n_users={n_total_users}  "
        f"resolution={target_step_min} min"
    )


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

EXAMPLE_CONFIG = {
    "raw_dir": "data/clean/timeseries",
    "output_dir": "baseline_results",
    "align_by": "month_day",
    "profiles": {
        "1": {
            "files": ["tpdin_user_74.csv", "tpdin_user_82.csv"],
            "period": {"type": "full_year", "year": 2024},
        },
        "2": {
            "files": ["old_user_12.csv"],
            "period": {"type": "months", "year": 2024, "months": [3, 4]},
        },
        "3": {
            "files": ["tpdin_user_55.csv", "old_user_60.csv"],
            "period": {"type": "date_range", "start": "2024-01-01", "end": "2024-01-31"},
        },
        "4": {
            "files": ["tpdin_user_99.csv"],
            "period": {"type": "full_year", "year": 2024},
        },
    },
}


def write_example_config(path: Path) -> None:
    with open(path, "w") as f:
        json.dump(EXAMPLE_CONFIG, f, indent=2)
    print(f"[+] Example config written to: {path}")
    print("    Edit it with your actual filenames and baseline periods, then run:")
    print(f"    python build_baseline_profiles.py --config {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Build empirical baseline load curves per profile from raw datalogger files."
    )
    ap.add_argument("--config", type=str, default=None,
                     help="Path to the JSON config file (see module docstring for format).")
    ap.add_argument("--write_example_config", type=str, default=None, metavar="PATH",
                     help="Write an example config to PATH and exit, without running anything.")
    ap.add_argument("--raw_dir", type=str, default=None,
                     help="Override the config's raw_dir.")
    ap.add_argument("--output_dir", type=str, default=None,
                     help="Override the config's output_dir.")
    ap.add_argument("--align_by", type=str, choices=["timestamp", "month_day"], default=None,
                     help="Alignment mode: 'timestamp' keeps original years; 'month_day' aligns across years on a synthetic calendar.")
    ap.add_argument("--profiles", type=str, nargs="+", default=None,
                     help="Only build baselines for these profile IDs (default: all in config).")
    args = ap.parse_args()

    if args.write_example_config:
        write_example_config(Path(args.write_example_config))
        return

    if not args.config:
        print("[-] Error: --config is required (or use --write_example_config to get started).")
        sys.exit(1)

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"[-] Error: config file not found: {config_path}")
        print("    Use --write_example_config to generate a starting template.")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    raw_dir = Path(args.raw_dir or config.get("raw_dir", "data/clean/timeseries"))
    output_dir = Path(args.output_dir or config.get("output_dir", "baseline_results"))
    align_by = args.align_by or config.get("align_by", "month_day")
    if align_by not in {"timestamp", "month_day"}:
        print(f"[-] Error: invalid align_by '{align_by}'. Expected 'timestamp' or 'month_day'.")
        sys.exit(1)

    profiles_cfg = config["profiles"]
    profile_ids = args.profiles or list(profiles_cfg.keys())

    print("=" * 64)
    print("Building Empirical Baseline Profiles - Raqaypampa")
    print("=" * 64)
    print(f"Raw dir     : {raw_dir.resolve()}")
    print(f"Output dir  : {output_dir.resolve()}")
    print(f"Align mode  : {align_by}")
    print(f"Profiles    : {profile_ids}")

    for pid in profile_ids:
        if pid not in profiles_cfg:
            print(f"[-] Warning: profile '{pid}' not found in config, skipping.")
            continue
        build_baseline_for_profile(pid, profiles_cfg[pid], raw_dir, output_dir, align_by)

    print("\n[+] Done.")


if __name__ == "__main__":
    main()