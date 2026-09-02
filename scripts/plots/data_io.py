"""
The single seam between the manuscript figures and the results on disk.

This is the ONLY file to edit when paths, runs or the validation window
change. Every figure script consumes one of two long-format tables and
nothing else, so nothing downstream needs to know where the data came from.

SCHEMA CONTRACT
---------------
load_profile_minutes()  -> Fig. 4, Fig. 5
    profile    int, 1-4
    series     "measured" | "socio_technical"
    day        one value per calendar day (grouping key only; the measured
               and simulated runs are stamped in different years, which is
               fine because days are never compared across series)
    time_min   int, 0-1439, minute-of-day at the start of the bin
    power_w    float, mean power over the bin

load_community_minutes()  -> Fig. 6, Fig. 7
    series     "heterogeneous" | "homogeneous"
    day, time_min, power_w   as above

RESAMPLING
----------
Both loaders resample onto a common bin (default 15 min, matching
`calculate_ldc_metrics` in scripts/modeling/validate_simulation.py) because
the sources do not share a sampling rate:

    measured baselines   P1/P4 at 5 min, P2/P3 at 10 min
    simulated runs       1 min

Plotting them unharmonised would make the simulated LDC sit above the
measured one at the top end purely as a sampling artefact. Do not remove
the resampling step to "keep more detail".

KNOWN CAVEATS
-------------
* The community aggregates were rebuilt on 2026-08-31 with
  build_community.py --sim_dir sim_community --counts 1=28,2=11,3=14,4=12
  --homogeneous_pid 0 --homogeneous_n 65, so they now agree with the
  current sim_community/ per-profile runs. If the profile parameter JSONs
  change, re-run run_community.py and then build_community.py again —
  otherwise Fig. 6/7 would describe an older parameterisation than
  Fig. 4/5 do.
* Measured pools are small: 2 households for P1/P3/P4 and 1 for P2. Pass
  the counts to the figures via N_HOUSEHOLDS so the panels state them.
* SIM_DIR points at simulation_results/, whose per-profile runs contain
  exactly ONE household each. profile_<pid>_minute_aggregated.csv is the
  SUM across a profile's households, so with one household it equals that
  household — correctly comparable to the measured representative
  baseline. Never re-point Fig. 4/5 at sim_community/: the same filenames
  there sum 11-28 households and the curves would be that many times too
  high. Check simulation_summary.json's n_households before switching.
"""

from pathlib import Path

import pandas as pd

# --- Where things live ----------------------------------------------------
REPO = Path(__file__).resolve().parents[2]

MEASURED_DIR = REPO / "data/clean/timeseries/baseline_results"
SIM_DIR = REPO / "scripts/modeling/simulation_results"
COMMUNITY_DIR = REPO / "scripts/modeling/community_results"

MEASURED_FILE = "baseline_profile_{profile}.csv"
SIM_FILE = "profile_{profile}_minute_aggregated.csv"
HETEROGENEOUS_FILE = "community_heterogeneous_minute.csv"
HOMOGENEOUS_FILE = "community_homogeneous_minute.csv"

# --- Validation window ----------------------------------------------------
# Fig. 4 and Fig. 5 are May panels. Fig. 6 and Fig. 7 use the full year by
# default; pass month=5 to restrict them too.
VALIDATION_MONTH = 5
BIN_MINUTES = 15

# Households behind each measured baseline, for the panel annotations.
# Update alongside build_baseline_profiles.py.
N_HOUSEHOLDS = {1: 2, 2: 1, 3: 2, 4: 2}


def _load_series(path, series, month=None, bin_minutes=BIN_MINUTES):
    """Read one timestamp/power_w CSV into the canonical long format."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"missing input {path}\n"
            f"  Check the paths at the top of data_io.py, or run the "
            f"simulation/baseline step that produces this file."
        )

    df = pd.read_csv(path, usecols=["timestamp", "power_w"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if month is not None:
        df = df[df["timestamp"].dt.month == month]
        if df.empty:
            raise ValueError(f"{path.name} has no data for month {month}")

    df = (
        df.set_index("timestamp")["power_w"]
        .resample(f"{bin_minutes}min")
        .mean()
        .dropna()
        .reset_index()
    )

    df["series"] = series
    df["day"] = df["timestamp"].dt.normalize()
    df["time_min"] = df["timestamp"].dt.hour * 60 + df["timestamp"].dt.minute
    return df[["series", "day", "time_min", "power_w"]]


def load_profile_minutes(
    profiles=(1, 2, 3, 4),
    month=VALIDATION_MONTH,
    bin_minutes=BIN_MINUTES,
):
    """Measured and Socio-Technical simulated power, per profile. Fig. 4, 5."""
    frames = []
    for profile in profiles:
        measured = _load_series(
            MEASURED_DIR / MEASURED_FILE.format(profile=profile),
            "measured", month=month, bin_minutes=bin_minutes,
        )
        simulated = _load_series(
            SIM_DIR / SIM_FILE.format(profile=profile),
            "socio_technical", month=month, bin_minutes=bin_minutes,
        )
        for frame in (measured, simulated):
            frame["profile"] = profile
            frames.append(frame)

    out = pd.concat(frames, ignore_index=True)
    return out[["profile", "series", "day", "time_min", "power_w"]]


def load_community_minutes(month=None, bin_minutes=BIN_MINUTES):
    """Heterogeneous reference and homogeneous Model aggregates. Fig. 6, 7."""
    frames = [
        _load_series(
            COMMUNITY_DIR / HETEROGENEOUS_FILE,
            "heterogeneous", month=month, bin_minutes=bin_minutes,
        ),
        _load_series(
            COMMUNITY_DIR / HOMOGENEOUS_FILE,
            "homogeneous", month=month, bin_minutes=bin_minutes,
        ),
    ]
    return pd.concat(frames, ignore_index=True)
