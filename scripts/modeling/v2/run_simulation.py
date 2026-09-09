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

Two independent seasonal mechanisms
-----------------------------------
1. Per-VA `seasonal_overrides` - a frequency/duration change on days the
   household is home. Applied by resolve_va_params().
2. The household-level occupancy mask (`prob_home`) - one presence draw per
   household per day that switches EVERY VA of that household off together.
   Applied by resolve_occupancy() -> RAMP's `User.prob_home`.
They compose multiplicatively: P(VA runs on a day) = prob_home * occasional_use.

Seasonal logic per profile (as documented in the markdowns' §6)
---------------------------------------------------------------
Profile 1 - Agricultural Core:
    Baseline = Planting (Oct-Jan) + Harvesting (May-Jun)
    Reduced  = Growing (Feb-Apr) + Free Grazing (Jul-Sep)
    -> occasional_use down on VAs 1,2,3,5,6,7; func_time down on VA9
    Occupancy mask OFF (prob_home: null) - the partial absence is already
    carried by those per-VA floors; a mask would double-count it.

Profile 2 - Isolated Elderly:
    No occupancy-driven seasonal change (R-A: the sedentary anchor).
    Only VA9 func_time increases during Growing + Harvesting (family visits).
    Occupancy mask OFF (prob_home: null) - continuous 365-day occupancy is a
    finding here, not a missing value.

Profile 3 - Extended Hub:
    Provisional per-VA override set for Growing + Free Grazing (§5).
    Occupancy mask ON: prob_home 0.96, dropping to 0.78 in Free Grazing
    (Jul-Sep migration window). This is the profile's primary seasonal effect.

Profile 4 - System Breakers:
    INVERTED: baseline is Planting + Harvesting; occasional_use is reduced
    during Growing + Free Grazing.
    Occupancy mask ON and dominant: prob_home 0.69 / 0.61 / 0.61 / 0.78 for
    planting / growing / harvesting / free grazing (annual 0.68), which
    inverts the community's seasonal shape - presence is LOWEST in growing
    and harvesting.

The occupancy mask requires the local RAMP fork (RAMP_main), which adds
`User.prob_home`; it is not in upstream rampdemand 0.5.2. A profile with
`prob_home: null` runs on either build.

Usage
-----
    pip install -e /path/to/RAMP_main      # the fork; see Dependencies
    python run_simulation.py
    python run_simulation.py --profile_json parameters/profile_1_params.json
    python run_simulation.py --params_dir parameters --output_dir simulation_results --year 2024 --n_households 10

Dependencies
------------
    rampdemand   - installed from the local RAMP fork (`pip install -e
                   /path/to/RAMP_main`), which adds `User.prob_home` for the
                   occupancy mask. Upstream `pip install rampdemand` works
                   only for profiles whose §6 sets `prob_home: null`;
                   Profiles 3 and 4 will raise a clear error on it.
    pandas
    pyarrow         (for Parquet output)
"""

from __future__ import annotations

import argparse
import calendar
import inspect
import json
import logging
import random
import warnings
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from season_resolve import (
    VALID_SEASONS,
    SEASON_MONTHS,
    MONTH_TO_SEASON,
    resolve_va_params,
    resolve_occupancy,
    rescale_occasional_use,
)

try:
    from ramp import UseCase, User, Appliance
    RAMP_AVAILABLE = True
    # The household-level occupancy mask (User.prob_home) is NOT in upstream
    # RAMP 0.5.2 - it comes from the local fork (see its FORK_NOTES.md §1).
    # Detect it rather than assume it: `pip install rampdemand`, which this
    # module's own usage notes suggest, yields an upstream build where passing
    # prob_home= raises a bare TypeError from deep inside __init__. Profiles
    # that don't ask for a mask keep working on either build.
    PROB_HOME_SUPPORTED = "prob_home" in inspect.signature(User.__init__).parameters
except ImportError:
    RAMP_AVAILABLE = False
    PROB_HOME_SUPPORTED = False
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
# Season calendar (imported from season_resolve.py - shared with
# extract_parameters.py so the two scripts can't define seasons differently)
# ---------------------------------------------------------------------------

def season_of(d: date) -> str:
    return MONTH_TO_SEASON[d.month]


@dataclass(frozen=True)
class SeasonBlock:
    """A contiguous run of calendar days that all fall in the same season."""
    season: str
    start_date: date
    n_days: int


def season_blocks_for_year(year: int, only_season: str | None = None) -> list[SeasonBlock]:
    """
    Walk the calendar year day by day and group it into contiguous
    same-season blocks. This lets us build the RAMP User/UseCase once
    per block instead of once per day.

    If `only_season` is given, blocks for every other season are dropped
    entirely (not simulated) - the returned blocks still carry their real
    calendar dates, so a season-restricted run's timestamps land on the
    correct days of the year rather than being remapped to start at
    Jan 1st.
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

    if only_season is not None:
        blocks = [b for b in blocks if b.season == only_season]
    return blocks


def month_block(year: int, month: int) -> SeasonBlock:
    """
    Return a single SeasonBlock covering every day of `month` in `year`.

    A calendar month always falls entirely within one season - SEASON_MONTHS
    groups whole months, never splits one - so this is a plain date-range
    lookup, not a filtered walk like season_blocks_for_year. The returned
    block's `.season` is that month's real season, so the existing
    per-block plumbing (build_ramp_users -> resolve_va_params and
    resolve_occupancy) picks up the correct seasonal overrides and the
    correct seasonal `prob_home` automatically, with no extra wiring needed
    beyond simulate_year choosing this block instead of the full year's.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"month must be between 1 and 12, got {month}")
    start = date(year, month, 1)
    n_days = calendar.monthrange(year, month)[1]
    return SeasonBlock(season_of(start), start, n_days)

    return blocks


# ---------------------------------------------------------------------------
# RAMP-based simulation (one User/UseCase built per profile+season block)
# ---------------------------------------------------------------------------

# Tracks which (profile_id, season) pairs have already had their occupancy
# setting logged. build_ramp_users runs once per household per season block, so
# without this the mask line would repeat n_households x n_blocks times.
_OCCUPANCY_LOGGED: set[tuple[str, str]] = set()


def _log_occupancy_once(profile: dict, season: str, occupancy: dict, note: str = "") -> None:
    """Log a profile+season's occupancy setting the first time it's built."""
    key = (str(profile.get("profile_id")), season)
    if key in _OCCUPANCY_LOGGED:
        return
    _OCCUPANCY_LOGGED.add(key)

    prob_home = occupancy["prob_home"]
    if prob_home is None:
        logger.info(
            "Profile %s / %-12s occupancy mask OFF (prob_home=null)",
            key[0], season,
        )
        return
    logger.info(
        "Profile %s / %-12s occupancy mask ON: prob_home=%.2f "
        "(~%.0f%% of days absent), occasional_use read as %s%s",
        key[0], season, prob_home, (1.0 - prob_home) * 100,
        occupancy["occasional_use_basis"], note,
    )


def build_ramp_users(profile: dict, season: str, user_name: str) -> list["User"]:
    """
    Construct the RAMP User(s) representing ONE household of this profile,
    with appliances resolved for the given season.

    Returns a LIST because the occupancy mask can require two users for a
    single physical household - see "Occupancy" below. Callers must add every
    returned user to the UseCase.

    Registration pattern: a single `user.add_appliance(**kwargs)` call,
    with both the "core" Appliance kwargs (power, func_time, ...) and the
    window kwargs (window_1, window_2, random_var_w) passed together.
    `add_appliance` internally splits them, builds the Appliance, calls
    its `.windows()` method, and appends it to `user.App_list` - this is
    RAMP's documented, actively-maintained entry point (RAMP CHANGELOG
    0.5.2: an older back-compat `Appliance`-on-`User` pattern is now
    deprecated in favor of exactly this). Verified directly against the
    installed RAMP version (0.5.0).

    The previous version of this function built an `Appliance` object by
    hand and then called `user.add_appliance(appliance)`, passing the
    already-built object as a positional argument. `add_appliance` does
    NOT accept a pre-built Appliance - passing one positionally is
    silently accepted as a garbage value for its first kwarg (`number`),
    and the real appliance is never registered: `user.App_list` stays
    empty and no error is raised.

    Seasonal overrides: `resolve_va_params` (season_resolve.py) applies
    any `seasonal_overrides[season]` found on a VA, falling back to
    baseline where none exists for that season. Every profile now carries
    some (Profile 1's §6 states explicit per-VA seasonal deltas; Profiles
    2-4 carry provisional sets flagged in their own §5 as sensitivity
    variants rather than re-derived findings).

    Occupancy: `resolve_occupancy` (season_resolve.py) reads the profile's
    §6 `yaml occupancy` block and returns this season's `prob_home`, which
    is passed straight to `User(prob_home=...)`. RAMP then makes ONE
    presence draw per household per day and gates every appliance of that
    user together, so an absent household produces exactly zero load that
    day - the household-level structural-absence mechanism Profiles 3 and
    4 name in their §6 as their primary seasonal effect. `prob_home=None`
    (Profiles 1 and 2) disables the draw entirely and consumes no random
    number, leaving those profiles' output bit-identical to a pre-feature
    run.

    Two subtleties the mask forces, both handled here:

    1. `occasional_use` becomes present-conditional once the mask is on:
       `P(VA runs) = prob_home * occasional_use`. Profiles declaring
       `occasional_use_basis: all_days` get each value divided by
       `prob_home` (capped at 1.0) to hold the mean load curve fixed;
       under the default `present_conditional` the authored values are
       already on the right basis and pass through untouched.
    2. RAMP's mask gates *every* appliance of the user, including ones
       declared `flat` (a fridge would keep running while the household is
       away). Any `flat: true` VA is therefore moved onto a SECOND, unmasked
       User representing the same physical household - which is why this
       function returns a list. No current profile uses `flat`, so this
       path is inert today; it exists so that adding one later can't
       silently switch a continuous load off.
    """
    occupancy = resolve_occupancy(profile, season)
    prob_home = occupancy["prob_home"]
    basis = occupancy["occasional_use_basis"]

    if prob_home is not None and not PROB_HOME_SUPPORTED:
        raise RuntimeError(
            f"Profile {profile.get('profile_id')} requests an occupancy mask "
            f"(prob_home={prob_home} for season '{season}'), but the installed RAMP "
            f"has no 'prob_home' parameter on User. The mask is a local-fork feature, "
            f"not part of upstream rampdemand 0.5.2 - install the fork at "
            f"RAMP_main (`pip install -e /path/to/RAMP_main`), or set 'prob_home: null' "
            f"in that profile's §6 occupancy block to simulate it without absence."
        )

    # Appliances of THIS household that the presence draw should gate (the
    # default) vs. ones that must keep running while the household is away.
    masked_kwargs: list[dict] = []
    always_on_kwargs: list[dict] = []
    capped: list[str] = []

    for va in profile["appliances"]:
        if va.get("retired"):
            continue

        p = resolve_va_params(va, season)

        # occasional_use=0 means the appliance never fires this season -
        # skip it, but log it so the methodology section can account for it.
        # (RAMP 0.5.2 also ignores appliances with func_time or randomly
        # allocated time of use == 0 internally; this explicit skip is kept
        # for occasional_use specifically and for the log line.)
        if p["occasional_use"] == 0:
            logger.info(
                "Skipping appliance '%s' for %s / %s: occasional_use=0",
                p["name"], user_name, season,
            )
            continue

        num_windows = p.get("num_windows", 1)

        # Under `all_days`, convert "fraction of all days" to the "fraction of
        # HOME days" RAMP reads once the mask is active. A no-op under the
        # default `present_conditional`, and whenever prob_home is None.
        occasional_use, was_capped = rescale_occasional_use(
            p["occasional_use"], prob_home, basis
        )
        if was_capped:
            capped.append(p["name"])

        app_kwargs = {
            "name":       p["name"],
            "power":      float(p["power"]),
            "number":     int(p.get("number", 1)),  # falls back to 1 if not in JSON - see run_simulation.py review notes
            "num_windows": num_windows,
            "func_time":  int(round(p["func_time"])),
            "func_cycle": int(round(p["func_cycle"])),
            "occasional_use": occasional_use,
            "time_fraction_random_variability": float(p.get("time_fraction_random_variability", 0.0)),
            "random_var_w": float(p.get("random_var_w", 0.0)),
        }
        if "thermal_p_var" in p:
            app_kwargs["thermal_p_var"] = float(p["thermal_p_var"])
        if "flat" in p:
            app_kwargs["flat"] = p["flat"]

        for i in range(1, num_windows + 1):
            key = f"window_{i}"
            if key not in p:
                raise KeyError(
                    f"Appliance '{p['name']}' declares num_windows={num_windows} "
                    f"but has no '{key}' value - check the source markdown's YAML block."
                )
            app_kwargs[key] = [int(v) for v in p[key]]

        # A `flat` load is a continuous one, so it must survive the household's
        # absence rather than be switched off with the rest (RAMP's mask gates
        # every appliance of a masked user indiscriminately).
        if prob_home is not None and p.get("flat"):
            always_on_kwargs.append(app_kwargs)
        else:
            masked_kwargs.append(app_kwargs)

    if capped:
        logger.warning(
            "Profile %s / %s: occasional_use hit the 1.0 cap when rescaling to "
            "the present-conditional basis for %s. prob_home=%.2f is too low to "
            "preserve those VAs' mean usage - their mean load is reduced, not held "
            "fixed. Lower the authored occasional_use or raise prob_home.",
            profile.get("profile_id"), season, ", ".join(capped), prob_home,
        )

    note = ""
    if always_on_kwargs:
        note = (
            f", {len(always_on_kwargs)} flat appliance(s) held on a separate "
            f"unmasked user"
        )
    _log_occupancy_once(profile, season, occupancy, note)

    # The masked user is always created, even with no appliances, so that a
    # season in which every VA is skipped keeps the same UseCase shape (exactly
    # one user per household) that it had before the mask existed.
    user_kwargs = {"user_name": user_name, "num_users": 1}
    if prob_home is not None:
        user_kwargs["prob_home"] = prob_home
    masked_user = User(**user_kwargs)
    for app_kwargs in masked_kwargs:
        masked_user.add_appliance(**app_kwargs)  # single call: builds + registers

    users = [masked_user]

    if always_on_kwargs:
        always_on_user = User(user_name=f"{user_name}_always_on", num_users=1)
        for app_kwargs in always_on_kwargs:
            always_on_user.add_appliance(**app_kwargs)
        users.append(always_on_user)

    return users


def simulate_block_ramp(
    profile: dict,
    block: SeasonBlock,
    profile_id: str,
    household_id: int,
    hh_seed: int,
) -> np.ndarray:
    """
    Simulate every day in a season block with ONE RAMP UseCase, built once
    per block rather than once per day.

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
    # Usually one user per household; two when the occupancy mask is on and the
    # profile has a `flat` appliance that must keep running while away.
    for user in build_ramp_users(
        profile, block.season, user_name=f"P{profile_id}_H{household_id}"
    ):
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
    num_windows = p.get("num_windows", 1)
    windows = [p[f"window_{i}"] for i in range(1, num_windows + 1)]

    for window in windows:
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
    """
    Stand-in for simulate_block_ramp when RAMP isn't installed. Mirrors the
    occupancy mask's structure - one presence draw per day, gating every
    non-`flat` VA together - so a fallback run is at least structurally
    comparable to a real one. It is still not validated against RAMP's engine
    and must not be used for publication figures.
    """
    occupancy = resolve_occupancy(profile, block.season)
    prob_home = occupancy["prob_home"]
    basis = occupancy["occasional_use_basis"]

    daily_arrays = []
    for _ in range(block.n_days):
        # One draw per household per day, shared by every appliance - the
        # whole point of the mask being household-level rather than per-VA.
        present = prob_home is None or rng.random() < prob_home

        load = np.zeros(1440)
        for va in profile["appliances"]:
            if va.get("retired"):
                continue
            p = resolve_va_params(va, block.season)
            if not present and not p.get("flat"):
                continue
            p = dict(p)
            p["occasional_use"], _ = rescale_occasional_use(
                p["occasional_use"], prob_home, basis
            )
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
    only_season: str | None = None,
    only_month: int | None = None,
) -> pd.DataFrame:
    """
    Simulate every day of `year` for a single household, building the
    RAMP User/UseCase once per season block rather than once per day.
    Returns a minute-level DataFrame built via vectorized array ops
    (no per-minute Python dict appends).

    If `only_season` is given, only that season's blocks are simulated -
    the output covers that season's real calendar days (e.g. Feb-Apr for
    "growing"), not a relabeled Jan-1-start range. Useful for a quick,
    much shorter run when checking one season's behavior specifically,
    without paying for the other three.

    If `only_month` is given (1-12), only that single calendar month is
    simulated, via month_block() rather than season_blocks_for_year().
    Since a month always falls entirely within one season, its seasonal
    overrides still apply automatically. If `only_season` is also given,
    it must match the month's real season (checked here, not just at the
    CLI layer, so a direct function call gets the same protection).
    """
    profile_id = str(profile["profile_id"])

    if only_month is not None:
        blocks = [month_block(year, only_month)]
        if only_season is not None and blocks[0].season != only_season:
            raise ValueError(
                f"--month {only_month} falls in season '{blocks[0].season}', "
                f"which doesn't match --season {only_season}. Pass only one "
                f"of the two, or make them consistent."
            )
    else:
        blocks = season_blocks_for_year(year, only_season=only_season)

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
    ap.add_argument("--season", default=None, choices=sorted(VALID_SEASONS),
                     help="If given, simulate only this one season's calendar days "
                          "instead of the full year (much faster for a focused check). "
                          "Output still carries that season's real dates. If the loaded "
                          "JSON was itself produced by extract_parameters.py --season, "
                          "this must match it (or be omitted). Mutually exclusive with "
                          "--month, unless they name the same season.")
    ap.add_argument("--month", type=int, default=None, choices=range(1, 13),
                     metavar="1-12",
                     help="If given, simulate only this one calendar month instead of "
                          "the full year - finer-grained than --season. A month always "
                          "falls within one season, so that season's overrides (if any) "
                          "still apply automatically; e.g. --month 3 (March) uses the "
                          "'growing' season's values for Profile 1. If --season is also "
                          "given it must match the month's real season.")
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
            "Install the local fork with `pip install -e /path/to/RAMP_main` "
            "before running a simulation intended for publication results - the "
            "fork is what provides the occupancy mask (User.prob_home) that "
            "Profiles 3 and 4 require. Pass --allow_fallback explicitly if you "
            "really want the lightweight stochastic stand-in (e.g. for a quick "
            "local smoke test)."
        )

    # --month implies a season (a month is always fully inside one season);
    # resolve that once up front so both the logging line and the
    # pre-flattened-JSON check below can treat --season/--month uniformly.
    month_implied_season = season_of(date(args.year, args.month, 1)) if args.month else None
    if args.month and args.season and month_implied_season != args.season:
        raise ValueError(
            f"--month {args.month} falls in season '{month_implied_season}', "
            f"which doesn't match --season {args.season}. Pass only one of "
            f"the two, or make them consistent."
        )
    effective_season = args.season or month_implied_season

    logger.info("=" * 64)
    logger.info("RAMP Energy Demand Simulation - Raqaypampa")
    logger.info("=" * 64)
    logger.info("Year                : %s", args.year)
    logger.info("Month filter        : %s", args.month or "(none)")
    logger.info("Season filter       : %s", effective_season or "(none - full year)")
    logger.info("Households/profile  : %s", args.n_households)
    logger.info("Random seed         : %s", args.seed)
    logger.info("RAMP available      : %s", RAMP_AVAILABLE)
    logger.info("Params dir          : %s", params_dir.resolve())
    logger.info("Output dir          : %s", output_dir.resolve())

    profiles = load_profiles(params_dir, args.profile_json)
    logger.info("Profiles loaded: %s", list(profiles.keys()))

    for pid, profile in profiles.items():
        pre_season = profile.get("season")
        if pre_season and effective_season and pre_season != effective_season:
            raise ValueError(
                f"Profile {pid}'s JSON was pre-resolved for season "
                f"'{pre_season}' (by extract_parameters.py --season), but "
                f"this run resolves to season '{effective_season}' "
                f"(from --season and/or --month). These must match - "
                f"re-extract with the right --season, or omit --season/"
                f"--month here to use the JSON's own resolved values."
            )
        if pre_season and not effective_season:
            logger.info(
                "Profile %s's JSON is pre-resolved for season '%s' - "
                "simulating the full year with these season-%s values "
                "applied uniformly (not varying by calendar season).",
                pid, pre_season, pre_season,
            )

    results: dict[str, pd.DataFrame] = {}

    for pid, profile in profiles.items():
        logger.info("Simulating Profile %s: %s", pid, profile["profile_name"])
        hh_dfs: list[pd.DataFrame] = []

        for hh_id in range(args.n_households):
            # Per-household seed so results are reproducible but independent.
            hh_seed = args.seed + int(pid) * 1000 + hh_id
            logger.info("  Household %3d/%d (seed=%d)", hh_id + 1, args.n_households, hh_seed)
            hh_df = simulate_year(
                profile, args.year, hh_id, hh_seed,
                only_season=args.season, only_month=args.month,
            )
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