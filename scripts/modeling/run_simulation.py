"""
run_simulation.py
=================
Builds and runs RAMP models for all Raqaypampa household profiles,
respecting seasonal variability over a full calendar year.

How it works
------------
1. Loads the JSON parameter files produced by extract_parameters.py.
2. Groups the simulation year into contiguous season blocks.
3. For each (profile, season) pair, builds ONE RAMP User/UseCase with
   seasonal parameter overrides applied, then calls
   generate_daily_load_profiles() once per day within that block.
4. Concatenates results (vectorized, no per-minute Python dict loop)
   and writes Parquet + CSV outputs.

Seasonal logic per profile (as documented in the markdowns)
------------------------------------------------------------
Profile 1 - Agricultural Core:
    Baseline = Planting (Oct-Jan) + Harvesting (May-Jun)
    Reduced  = Growing (Feb-Apr) + Free Grazing (Jul-Sep)
    -> occasional_use down on VAs 1,2,3,5,6,7; func_time down on VA9

Profile 2 - Isolated Elderly:
    No occupancy-driven seasonal change (Rule 18: sedentary anchor).
    Only VA9 func_time increases during Growing + Harvesting (family visits).

Profile 3 - Extended Hub:
    Same pattern as Profile 1.
    Reduced = Growing (Feb-Apr) + Free Grazing (Jul-Sep)

Profile 4 - System Breakers:
    INVERTED: baseline is Growing + Free Grazing (household mostly absent).
    Activity INCREASES during Planting + Harvesting.

Usage
-----
    pip install rampdemand
    python run_simulation.py
    python run_simulation.py --profile_json parameters/profile_1_params.json
    python run_simulation.py --params_dir parameters --output_dir simulation_results --year 2024 --n_households 10

Dependencies
------------
    rampdemand   (pip install rampdemand)
    pandas
    pyarrow         (for Parquet output)
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import warnings
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from ramp import UseCase, User, Appliance
    RAMP_AVAILABLE = True
except ImportError:
    RAMP_AVAILABLE = False
    warnings.warn(
        "ramp-mobility is not installed. Install it with:\n"
        "    pip install ramp-mobility\n"
        "Falling back to a lightweight stochastic simulator for testing. "
        "Results from the fallback simulator are NOT validated against RAMP's "
        "engine and should never be used for publication figures.",
        stacklevel=2,
    )

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("ramp_sim")


# ---------------------------------------------------------------------------
# Season calendar (mirrors extract_parameters.py)
# ---------------------------------------------------------------------------

SEASON_MONTHS: dict[str, list[int]] = {
    "planting":     [10, 11, 12, 1],
    "growing":      [2, 3, 4],
    "harvesting":   [5, 6],
    "free_grazing": [7, 8, 9],
}
MONTH_TO_SEASON: dict[int, str] = {
    m: s for s, months in SEASON_MONTHS.items() for m in months
}


def season_of(d: date) -> str:
    return MONTH_TO_SEASON[d.month]


@dataclass(frozen=True)
class SeasonBlock:
    """A contiguous run of calendar days that all fall in the same season."""
    season: str
    start_date: date
    n_days: int


def season_blocks_for_year(year: int) -> list[SeasonBlock]:
    """
    Walk the calendar year day by day and group it into contiguous
    same-season blocks. This lets us build the RAMP User/UseCase once
    per block instead of once per day.
    """
    start = date(year, 1, 1)
    n_days = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365

    blocks: list[SeasonBlock] = []
    block_start = start
    block_season = season_of(start)
    block_len = 1

    for day_offset in range(1, n_days):
        current_date = start + timedelta(days=day_offset)
        s = season_of(current_date)
        if s == block_season:
            block_len += 1
        else:
            blocks.append(SeasonBlock(block_season, block_start, block_len))
            block_start = current_date
            block_season = s
            block_len = 1
    blocks.append(SeasonBlock(block_season, block_start, block_len))
    return blocks


# ---------------------------------------------------------------------------
# Parameter helpers
# ---------------------------------------------------------------------------

def resolve_va_params(va: dict, season: str) -> dict:
    """
    Return a copy of the VA parameter dict with seasonal overrides applied.
    The baseline values are used unchanged when no override exists for
    the current season. All fields present on the VA (not just a fixed
    subset) are carried through, since the RAMP Appliance object on some
    installed versions accepts extra optional attributes such as `flat`,
    `time_fraction_random_variability`, and `random_var_w`.
    """
    resolved = {k: v for k, v in va.items() if k != "seasonal_overrides"}
    overrides = va.get("seasonal_overrides", {}).get(season, {})
    resolved.update(overrides)
    return resolved


# ---------------------------------------------------------------------------
# RAMP-based simulation (one User/UseCase built per profile+season block)
# ---------------------------------------------------------------------------

def build_ramp_user(profile: dict, season: str, user_name: str) -> "User":
    """
    Construct a RAMP User with appliances resolved for the given season.

    Mirrors the construction pattern confirmed to work on the installed
    RAMP version: only a few "core" parameters go into Appliance.__init__
    (user, name, power, number, func_time, func_cycle, and optionally
    flat); everything else (num_windows, occasional_use,
    time_fraction_random_variability, random_var_w, window_1, window_2,
    ...) is set as an attribute on the Appliance instance AFTER
    construction, then the appliance is registered via
    user.add_appliance(appliance).
    """
    user = User(user_name=user_name, num_users=1)

    for va in profile["appliances"]:
        p = resolve_va_params(va, season)

        # occasional_use=0 means the appliance never fires this season -
        # skip it, but log it so the methodology section can account for it.
        if p["occasional_use"] == 0:
            logger.info(
                "Skipping appliance '%s' for %s / %s: occasional_use=0",
                p["name"], user_name, season,
            )
            continue

        windows = p["windows"]

        app_kwargs = {
            "user":       user,
            "name":       p["name"],
            "power":      float(p["power"]),
            "number":     1,
            "func_time":  int(round(p["func_time"])),
            "func_cycle": int(round(p["func_cycle"])),
        }
        if "flat" in p:
            app_kwargs["flat"] = p["flat"]

        appliance = Appliance(**app_kwargs)

        appliance.num_windows = len(windows) if windows else 1
        appliance.occasional_use = float(p["occasional_use"])
        appliance.time_fraction_random_variability = float(p.get("time_fraction_random_variability", 0.0))
        appliance.random_var_w = float(p.get("random_var_w", 0.0))

        # Windows are [start_minute, end_minute] pairs (0-1440).
        for i, window in enumerate(windows, start=1):
            setattr(appliance, f"window_{i}", [int(v) for v in window])

        user.add_appliance(appliance)

    return user


def simulate_block_ramp(
    profile: dict,
    block: SeasonBlock,
    profile_id: str,
    household_id: int,
    hh_seed: int,
) -> np.ndarray:
    """
    Simulate every day in a season block with ONE RAMP User/UseCase
    (built once per block, not once per day).

    Matches the API confirmed to work on the installed RAMP version:
    UseCase() takes no construction-time date range; instead you call
    use_case.initialize(num_days=N) to set how many days to simulate,
    then use_case.generate_daily_load_profiles(flat=True) runs all N
    days in one call and returns a flat 1-D numpy array of length
    N * 1440.

    Returns an array of shape (block.n_days, 1440) in watts.
    """
    # Seed numpy's global RNG deterministically, derived from the
    # household seed plus the block start, so re-running the script
    # reproduces results exactly. RAMP draws from this global generator
    # internally, so seeding only a local rng object does not make RAMP
    # runs reproducible.
    block_seed = hh_seed * 100_003 + block.start_date.toordinal()
    np.random.seed(block_seed % (2**32 - 1))
    random.seed(block_seed)

    use_case = UseCase()
    user = build_ramp_user(profile, block.season, user_name=f"P{profile_id}_H{household_id}")
    use_case.add_user(user)

    use_case.initialize(num_days=block.n_days)
    load = use_case.generate_daily_load_profiles(flat=True)
    arr = np.asarray(load, dtype=float).reshape(-1)

    expected_len = block.n_days * 1440
    if arr.size != expected_len:
        raise RuntimeError(
            f"Unexpected RAMP output length for block {block.season} "
            f"starting {block.start_date}: got {arr.size}, expected {expected_len}. "
            "Check `ramp.UseCase.generate_daily_load_profiles` / "
            "`ramp.UseCase.initialize` in your installed version's docs."
        )

    return arr.reshape(block.n_days, 1440)


# ---------------------------------------------------------------------------
# Fallback lightweight stochastic simulator (when RAMP is not installed)
# ---------------------------------------------------------------------------

def _appliance_load(p: dict, rng: np.random.Generator) -> np.ndarray:
    """Stochastic minute-level load for one VA using RAMP-like logic."""
    load = np.zeros(1440)
    if rng.random() > p["occasional_use"]:
        return load

    power      = p["power"]
    func_time  = int(p["func_time"])
    func_cycle = max(1, int(p["func_cycle"]))

    for window in p["windows"]:
        w_start, w_end = window
        if w_end <= w_start:
            w_end += 1440  # overnight window

        w_dur = w_end - w_start
        if w_dur <= 0:
            continue

        n_cycles = max(1, func_time // func_cycle)
        cycle_len = min(func_cycle, max(1, w_dur // n_cycles))

        for _ in range(n_cycles):
            latest_start = max(w_start, w_end - cycle_len)
            t_start = int(rng.integers(w_start, latest_start + 1)) if latest_start > w_start else w_start
            for t in range(cycle_len):
                load[(t_start + t) % 1440] += power

    return load


def simulate_block_fallback(
    profile: dict,
    block: SeasonBlock,
    rng: np.random.Generator,
) -> np.ndarray:
    daily_arrays = []
    for _ in range(block.n_days):
        load = np.zeros(1440)
        for va in profile["appliances"]:
            p = resolve_va_params(va, block.season)
            load += _appliance_load(p, rng)
        daily_arrays.append(load)
    return np.vstack(daily_arrays)


# ---------------------------------------------------------------------------
# Year simulation
# ---------------------------------------------------------------------------

def simulate_year(
    profile: dict,
    year: int,
    household_id: int,
    hh_seed: int,
) -> pd.DataFrame:
    """
    Simulate every day of `year` for a single household, building the
    RAMP User/UseCase once per season block rather than once per day.
    Returns a minute-level DataFrame built via vectorized array ops
    (no per-minute Python dict appends).
    """
    profile_id = str(profile["profile_id"])
    blocks = season_blocks_for_year(year)
    rng = np.random.default_rng(hh_seed)  # only used by the fallback path

    chunks: list[pd.DataFrame] = []

    for block in blocks:
        if RAMP_AVAILABLE:
            arr = simulate_block_ramp(profile, block, profile_id, household_id, hh_seed)
        else:
            arr = simulate_block_fallback(profile, block, rng)

        n_days, n_minutes = arr.shape
        timestamps = pd.date_range(
            start=block.start_date, periods=n_days * n_minutes, freq="min"
        )
        chunk = pd.DataFrame({
            "timestamp":    timestamps,
            "power_w":      arr.reshape(-1).astype("float32"),
            "profile_id":   profile_id,
            "household_id": household_id,
            "season":       block.season,
        })
        chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)
    df["profile_id"]   = df["profile_id"].astype("category")
    df["household_id"] = df["household_id"].astype("int16")
    df["season"]       = df["season"].astype("category")
    return df


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def aggregate_hourly(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hour_ts"] = df["timestamp"].dt.floor("h")
    return (
        df.groupby(["profile_id", "household_id", "hour_ts", "season"], sort=False, observed=True)
          .agg(power_w=("power_w", "mean"))
          .reset_index()
          .rename(columns={"hour_ts": "timestamp"})
    )


def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = df["timestamp"].dt.date
    agg = (
        df.groupby(["profile_id", "household_id", "date", "season"], sort=False, observed=True)
          .agg(
              mean_power_w   =("power_w", "mean"),
              peak_power_w   =("power_w", "max"),
              total_energy_wh=("power_w", lambda x: x.sum() / 60),  # W*min -> Wh
          )
          .reset_index()
    )
    return agg


def compute_summary(results: dict[str, pd.DataFrame]) -> dict:
    summary = {}
    for pid, df in results.items():
        df = df.copy()
        df["hour"] = df["timestamp"].dt.hour
        by_hour = df.groupby("hour")["power_w"].mean().to_dict()
        by_season = (
            df.groupby("season", observed=True)["power_w"]
              .agg(mean="mean", std="std")
              .rename(columns={"mean": "mean_power_w", "std": "std_power_w"})
              .to_dict(orient="index")
        )
        summary[pid] = {
            "n_households": int(df["household_id"].nunique()),
            "n_days":       int(df["timestamp"].dt.date.nunique()),
            "overall": {
                "mean_power_w":    float(df["power_w"].mean()),
                "peak_power_w":    float(df["power_w"].max()),
                "std_power_w":     float(df["power_w"].std()),
                "total_energy_wh": float(df["power_w"].sum() / 60),
            },
            "by_season": {s: {k: float(v) for k, v in vals.items()}
                          for s, vals in by_season.items()},
            "mean_load_curve_by_hour": {int(h): float(v) for h, v in by_hour.items()},
        }
    return summary


# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------

def _parquet_engine_available() -> bool:
    """
    Probe whether pandas can actually write Parquet in this environment.
    Mixed conda/pip installs can leave a partially-broken pyarrow on the
    path (importable but raising AttributeError on internal symbols),
    which only surfaces the first time to_parquet() is called - often
    after an hours-long simulation has already finished. Checking once,
    up front, lets us fall back to CSV instead of losing the whole run.
    """
    try:
        import pyarrow.parquet  # noqa: F401
        return True
    except Exception as exc:
        logger.warning(
            "Parquet engine (pyarrow) is not usable in this environment (%s: %s). "
            "Falling back to CSV-only output so this run's results are not lost. "
            "Fix your pyarrow install (e.g. `pip uninstall pyarrow && conda install "
            "-c conda-forge pyarrow`) to get Parquet output on the next run.",
            type(exc).__name__, exc,
        )
        return False


def save_results(results: dict[str, pd.DataFrame], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    use_parquet = _parquet_engine_available()

    all_hourly: list[pd.DataFrame] = []
    all_daily:  list[pd.DataFrame] = []

    for pid, df in results.items():
        if use_parquet:
            minute_path = output_dir / f"profile_{pid}_minute.parquet"
            try:
                df.to_parquet(minute_path, index=False)
                logger.info("Saved: %s", minute_path)
            except Exception as exc:
                logger.warning(
                    "Parquet write failed for profile %s (%s); falling back to CSV.",
                    pid, exc,
                )
                use_parquet = False

        if not use_parquet:
            minute_path = output_dir / f"profile_{pid}_minute.csv"
            df.to_csv(minute_path, index=False)
            logger.info("Saved: %s", minute_path)

        # Simplified minute-level CSV: timestamp + power_w only, summed
        # across all households in this profile (i.e. the aggregate load
        # of the profile's household group at each minute of the year).
        agg_minute_path = output_dir / f"profile_{pid}_minute_aggregated.csv"
        agg_minute_df = (
            df.groupby("timestamp", as_index=False, sort=True)["power_w"]
              .sum()
        )
        agg_minute_df.to_csv(agg_minute_path, index=False)
        logger.info("Saved: %s", agg_minute_path)

        hourly_df_pid = aggregate_hourly(df)
        daily_df_pid  = aggregate_daily(df)
        all_hourly.append(hourly_df_pid)
        all_daily.append(daily_df_pid)

        # Per-profile standalone CSVs (hourly + daily), independent of
        # the combined all_profiles_* files below.
        daily_path_pid = output_dir / f"profile_{pid}_daily.csv"
        daily_df_pid.to_csv(daily_path_pid, index=False)
        logger.info("Saved: %s", daily_path_pid)

        hourly_path_pid = output_dir / f"profile_{pid}_hourly.csv"
        hourly_df_pid.to_csv(hourly_path_pid, index=False)
        logger.info("Saved: %s", hourly_path_pid)

    hourly_df = pd.concat(all_hourly, ignore_index=True)
    daily_df  = pd.concat(all_daily,  ignore_index=True)

    if use_parquet:
        try:
            hourly_df.to_parquet(output_dir / "all_profiles_hourly.parquet", index=False)
            daily_df.to_parquet( output_dir / "all_profiles_daily.parquet",  index=False)
            logger.info("Saved: %s", output_dir / "all_profiles_hourly.parquet")
            logger.info("Saved: %s", output_dir / "all_profiles_daily.parquet")
        except Exception as exc:
            logger.warning("Parquet write failed for combined files (%s); falling back to CSV.", exc)
            use_parquet = False

    if not use_parquet:
        hourly_df.to_csv(output_dir / "all_profiles_hourly.csv", index=False)
        logger.info("Saved: %s", output_dir / "all_profiles_hourly.csv")

    daily_df.to_csv(output_dir / "all_profiles_daily.csv", index=False)
    logger.info("Saved: %s", output_dir / "all_profiles_daily.csv")

    summary = compute_summary(results)
    summary_path = output_dir / "simulation_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    logger.info("Saved: %s", summary_path)


def load_profiles(params_dir: Path, profile_json: Path | None) -> dict[str, dict]:
    """Load either the combined bundle or a standalone single-profile JSON."""
    if profile_json is not None:
        if not profile_json.exists():
            raise FileNotFoundError(f"Parameter file not found: {profile_json}")
        with open(profile_json) as f:
            profile = json.load(f)

        profile_id = profile.get("profile_id")
        if profile_id is None:
            raise KeyError(f"profile_id missing in {profile_json}")

        return {str(profile_id): profile}

    combined_path = params_dir / "all_profiles_params.json"
    if not combined_path.exists():
        raise FileNotFoundError(
            f"Parameter file not found: {combined_path}\n"
            "Run extract_parameters.py first or pass --profile_json."
        )
    with open(combined_path) as f:
        combined = json.load(f)
    return combined["profiles"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Run full-year RAMP energy demand simulation for Raqaypampa profiles."
    )
    ap.add_argument("--params_dir",   default="parameters",
                     help="Directory with JSON files from extract_parameters.py")
    ap.add_argument("--output_dir",   default="simulation_results",
                     help="Directory for output files")
    ap.add_argument("--profile_json", type=Path, default=None,
                     help="Optional path to a single profile JSON file")
    ap.add_argument("--year",         type=int, default=2024,
                     help="Simulation year (default: 2024)")
    ap.add_argument("--n_households", type=int, default=10,
                     help="Number of households to simulate per profile (default: 10)")
    ap.add_argument("--seed",         type=int, default=42,
                     help="Global random seed (default: 42)")
    ap.add_argument("--allow_fallback", action="store_true",
                     help="Allow the script to run with the non-RAMP fallback "
                          "simulator if rampdemand is not installed. By default "
                          "the script refuses to run without RAMP, since fallback "
                          "results are not validated and should not be used for "
                          "publication figures.")
    args = ap.parse_args()

    params_dir = Path(args.params_dir)
    output_dir = Path(args.output_dir)

    if not RAMP_AVAILABLE and not args.allow_fallback:
        raise RuntimeError(
            "rampdemand is not installed and --allow_fallback was not passed. "
            "Install it with `pip install rampdemand` (or `pip install "
            "ramp-mobility`, depending on the package name on your system) "
            "before running a simulation intended for publication results. "
            "Pass --allow_fallback explicitly if you really want the "
            "lightweight stochastic stand-in (e.g. for a quick local smoke test)."
        )

    logger.info("=" * 64)
    logger.info("RAMP Energy Demand Simulation - Raqaypampa")
    logger.info("=" * 64)
    logger.info("Year                : %s", args.year)
    logger.info("Households/profile  : %s", args.n_households)
    logger.info("Random seed         : %s", args.seed)
    logger.info("RAMP available      : %s", RAMP_AVAILABLE)
    logger.info("Params dir          : %s", params_dir.resolve())
    logger.info("Output dir          : %s", output_dir.resolve())

    profiles = load_profiles(params_dir, args.profile_json)
    logger.info("Profiles loaded: %s", list(profiles.keys()))

    results: dict[str, pd.DataFrame] = {}

    for pid, profile in profiles.items():
        logger.info("Simulating Profile %s: %s", pid, profile["profile_name"])
        hh_dfs: list[pd.DataFrame] = []

        for hh_id in range(args.n_households):
            # Per-household seed so results are reproducible but independent.
            hh_seed = args.seed + int(pid) * 1000 + hh_id
            logger.info("  Household %3d/%d (seed=%d)", hh_id + 1, args.n_households, hh_seed)
            hh_df = simulate_year(profile, args.year, hh_id, hh_seed)
            hh_dfs.append(hh_df)

        profile_df = pd.concat(hh_dfs, ignore_index=True)
        results[pid] = profile_df
        mean_pw = profile_df["power_w"].mean()
        logger.info("  Completed %d households - mean power: %.3f W", args.n_households, mean_pw)

    logger.info("Saving results...")
    save_results(results, output_dir)

    logger.info("=" * 64)
    logger.info("Summary")
    logger.info("=" * 64)
    summary = compute_summary(results)
    for pid, stats in summary.items():
        o = stats["overall"]
        logger.info(
            "Profile %s  mean=%.3f W  peak=%.1f W  total=%.0f Wh/year",
            pid, o["mean_power_w"], o["peak_power_w"], o["total_energy_wh"],
        )
        for season, sv in stats["by_season"].items():
            logger.info("    %-14s %.3f W", season, sv["mean_power_w"])

    logger.info("Done.")


if __name__ == "__main__":
    main()