"""
run_community.py
================
Single-run whole-community simulation: simulate every Energy Behaviour
Profile at its OWN household count in one process, instead of four
uniform-count invocations of run_simulation.py.

This is a thin driver. It imports and reuses run_simulation.py's engine
unchanged - simulate_year() (with all its seasonal logic, including
Profile 4's inversion), the per-household seeding scheme, save_results()
and compute_summary(). The only thing it changes is that the household
count varies per profile, driven by --counts, rather than being one
uniform --n_households for all.

Because it writes the SAME per-household output files as run_simulation.py
(profile_<pid>_minute.parquet|csv and profile_<pid>_minute_aggregated.csv),
build_community.py and validate_community.py consume its output with no
changes. Per-household resolution is preserved, so the coincidence factor
is still computable (a true single RAMP UseCase that returns only the
summed aggregate would lose that - see note at the bottom of this file).

Optionally, the homogeneous Model A community can be simulated in the SAME
run by pointing --homogeneous_json at the averaged-profile parameters and
giving it the total community size, so one command produces everything
needed for the A/B community comparison.

Usage
-----
    # heterogeneous mix only, in one run:
    python run_community.py --params_dir parameters \
        --counts 1=28,2=11,3=14,4=12 --output_dir sim_community

    # heterogeneous mix AND Model A (homogeneous), one run:
    python run_community.py --params_dir parameters \
        --counts 1=28,2=11,3=14,4=12 \
        --homogeneous_json parameters/profile_A_params.json \
        --homogeneous_pid 99 --homogeneous_n 65 \
        --output_dir sim_community

    # one season / month, same passthrough flags as run_simulation.py:
    python run_community.py --counts 1=28,2=11,3=14,4=12 --season harvesting
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

# Reuse the simulation engine unchanged - identical seasonal behaviour.
from run_simulation import (
    RAMP_AVAILABLE,
    logger,
    load_profiles,
    simulate_year,
    save_results,
    compute_summary,
    season_of,
    VALID_SEASONS,
)


def parse_counts(spec: str) -> list[tuple[str, int]]:
    """Parse '1=28,2=11,3=14,4=12' -> [('1',28),('2',11),('3',14),('4',12)]."""
    members = []
    for part in spec.split(","):
        pid, _, cnt = part.partition("=")
        pid, cnt = pid.strip(), cnt.strip()
        if not pid or not cnt:
            raise argparse.ArgumentTypeError(
                f"bad --counts entry '{part}'; expected 'pid=count'")
        members.append((pid, int(cnt)))
    return members


def build_plan(args) -> list[tuple[str, dict, int]]:
    """
    Resolve the requested (profile_id, profile_dict, count) simulation plan
    from the combined bundle plus an optional standalone Model A JSON.
    """
    profiles = load_profiles(Path(args.params_dir), None)  # combined bundle
    plan: list[tuple[str, dict, int]] = []

    for pid, count in args.counts:
        if pid not in profiles:
            raise SystemExit(
                f"[-] Profile id '{pid}' from --counts not found in the "
                f"combined bundle (have: {sorted(profiles)}). Check "
                f"--params_dir / all_profiles_params.json.")
        plan.append((str(pid), profiles[pid], count))

    if args.homogeneous_json is not None:
        homo = load_profiles(Path(args.params_dir), Path(args.homogeneous_json))
        # load_profiles keys by the JSON's own profile_id; take the single entry
        (_key, homo_profile), = homo.items()
        homo_pid = str(args.homogeneous_pid or _key)
        homo_n = args.homogeneous_n or sum(c for _, c in args.counts)
        plan.append((homo_pid, homo_profile, homo_n))

    return plan


def main():
    ap = argparse.ArgumentParser(
        description="Single-run whole-community RAMP simulation at per-profile "
                    "household counts (reuses run_simulation.py's engine).")
    ap.add_argument("--params_dir", default="parameters",
                    help="Directory with all_profiles_params.json.")
    ap.add_argument("--output_dir", default="sim_community",
                    help="Output directory (shared by all profiles this run).")
    ap.add_argument("--counts", type=parse_counts, required=True,
                    help="Per-profile household counts, e.g. '1=28,2=11,3=14,4=12'.")
    ap.add_argument("--homogeneous_json", type=Path, default=None,
                    help="Optional Model A (averaged) profile JSON to simulate "
                         "in the same run as the homogeneous community.")
    ap.add_argument("--homogeneous_pid", type=str, default=None,
                    help="Profile id to store Model A under (int-castable, e.g. 99). "
                         "Defaults to the id inside the JSON.")
    ap.add_argument("--homogeneous_n", type=int, default=None,
                    help="Model A household count = total community size "
                         "(defaults to the sum of --counts).")
    ap.add_argument("--year", type=int, default=2024)
    ap.add_argument("--season", default=None, choices=sorted(VALID_SEASONS),
                    help="Simulate only this season (same semantics as run_simulation.py).")
    ap.add_argument("--month", type=int, default=None, choices=range(1, 13), metavar="1-12",
                    help="Simulate only this month (same semantics as run_simulation.py).")
    ap.add_argument("--seed", type=int, default=42,
                    help="Global seed; per-household seed matches run_simulation.py "
                         "(seed + int(pid)*1000 + hh_id) for reproducible parity.")
    ap.add_argument("--allow_fallback", action="store_true",
                    help="Permit the non-RAMP fallback simulator (not for publication).")
    args = ap.parse_args()

    if not RAMP_AVAILABLE and not args.allow_fallback:
        raise SystemExit(
            "[-] rampdemand is not installed and --allow_fallback was not passed. "
            "Install RAMP before a publication run (see run_simulation.py).")

    # month implies a season; validate consistency exactly like run_simulation.py
    month_season = season_of(date(args.year, args.month, 1)) if args.month else None
    if args.month and args.season and month_season != args.season:
        raise SystemExit(
            f"[-] --month {args.month} falls in season '{month_season}', which "
            f"doesn't match --season {args.season}.")
    effective_season = args.season or month_season

    plan = build_plan(args)

    logger.info("=" * 64)
    logger.info("RAMP Whole-Community Simulation (single run) - Raqaypampa")
    logger.info("=" * 64)
    logger.info("Year            : %s", args.year)
    logger.info("Season/month    : %s", effective_season or "(full year)")
    logger.info("Output dir      : %s", Path(args.output_dir).resolve())
    logger.info("Plan            :")
    for pid, prof, count in plan:
        logger.info("    profile %-3s x %-4d  (%s)", pid, count,
                    prof.get("profile_name", "?"))
    total_hh = sum(c for _, _, c in plan)
    logger.info("Total households : %d", total_hh)

    results: dict[str, pd.DataFrame] = {}

    for pid, profile, count in plan:
        # Mirror run_simulation.py's pre-resolved-season guard.
        pre_season = profile.get("season")
        if pre_season and effective_season and pre_season != effective_season:
            raise SystemExit(
                f"[-] Profile {pid}'s JSON is pre-resolved for season "
                f"'{pre_season}' but this run resolves to '{effective_season}'. "
                f"Re-extract or drop --season/--month.")

        logger.info("Simulating profile %s: %s (%d households)",
                    pid, profile.get("profile_name", "?"), count)
        hh_dfs: list[pd.DataFrame] = []
        for hh_id in range(count):
            hh_seed = args.seed + int(pid) * 1000 + hh_id  # parity with run_simulation.py
            hh_df = simulate_year(
                profile, args.year, hh_id, hh_seed,
                only_season=args.season, only_month=args.month,
            )
            hh_dfs.append(hh_df)
        results[str(pid)] = pd.concat(hh_dfs, ignore_index=True)
        logger.info("  done - mean power %.3f W", results[str(pid)]["power_w"].mean())

    logger.info("Saving results (same file layout as run_simulation.py)...")
    save_results(results, Path(args.output_dir))

    logger.info("=" * 64)
    for pid, stats in compute_summary(results).items():
        o = stats["overall"]
        logger.info("Profile %s  mean=%.3f W  peak=%.1f W  total=%.0f Wh/yr",
                    pid, o["mean_power_w"], o["peak_power_w"], o["total_energy_wh"])

    logger.info("Done. Next:")
    logger.info("  python build_community.py --sim_dir %s --counts %s%s",
                args.output_dir,
                ",".join(f"{p}={c}" for p, c in args.counts),
                (f" --homogeneous_pid {args.homogeneous_pid} "
                 f"--homogeneous_n {args.homogeneous_n or total_hh}"
                 if args.homogeneous_json else ""))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Note on the alternative "true single UseCase" approach
# ---------------------------------------------------------------------------
# RAMP can hold all four profiles as separate User types in ONE UseCase
# (each with its own num_users) and sum them internally in a single
# generate_daily_load_profiles() call. That is the most literal "single
# run", but generate_daily_load_profiles() returns only the SUMMED community
# curve - individual household load profiles are not recovered - so the
# coincidence factor (community peak / sum of individual household peaks)
# and any per-household diversity diagnostics become impossible to compute
# downstream. This driver deliberately keeps per-household resolution (one
# simulate_year() call per household, results concatenated) so build_community.py
# can still compute those aggregate-vs-individual metrics. It is a single
# *command*/process; it is not collapsed into a single RAMP call, on purpose.
