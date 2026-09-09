"""
build_community.py
==================
Assemble whole-community load curves from the per-profile RAMP outputs
produced by run_simulation.py, so a community can be carried into
validation alongside the existing per-profile (representative-household)
comparison in validate_simulation.py.

Two communities are built, both over the SAME simulated calendar so their
minute-level series are directly comparable:

  * Heterogeneous (Model B):  the demographic mix of Energy Behaviour
    Profiles in their real classified proportions. Built by summing the
    per-household minute series across all four profiles, taking the first
    k_p distinct households of each profile p (k_p = that profile's
    community count).

  * Homogeneous (Model A):  N_total households that all share the single
    averaged representative parametrisation - i.e. the standard baseline
    scaled to the whole community. Built by summing the first N_total
    households of the Model A per-household run.

Because each household is an independent stochastic RAMP realisation (see
run_simulation.py's per-household seeding), summing them reproduces real
diversity / coincidence effects rather than stamping one clone N times.
The difference in the *coincidence factor* between the two communities is
the headline planning quantity this script exists to expose.

An OPTIONAL empirical reference community can also be composed from the
measured per-profile baselines used by validate_simulation.py. It is a
*composed* reference (mix-weighted sum of each profile's representative
daily curve), NOT an independently metered community total - see the
caveat in build_empirical_reference_daily(). Its purpose is a consistency
check on the heterogeneous community, since a true 65-household aggregate
was never metered; per-profile validation against telemetry remains the
primary empirical anchor and is unchanged (validate_simulation.py).

Inputs (from run_simulation.py, one run per profile into --sim_dir)
------------------------------------------------------------------
    profile_<pid>_minute.parquet|csv   cols: timestamp, power_w,
                                        profile_id, household_id, season

Outputs (into --out_dir)
------------------------
    community_heterogeneous_minute.csv   cols: timestamp, power_w
    community_homogeneous_minute.csv     cols: timestamp, power_w   (if Model A given)
    community_coincidence.csv            per-day coincidence factor, both communities
    community_empirical_daily.csv        (optional) time_decimal, power_w

Usage
-----
    # 1) run run_simulation.py ONCE PER PROFILE at the mix counts, same out dir:
    #    python run_simulation.py --profile_json parameters/profile_1_params.json \
    #        --n_households 28 --output_dir sim_community
    #    ... profiles 2 (11), 3 (14), 4 (12) ...
    #    # Model A (single averaged profile) scaled to the whole community:
    #    python run_simulation.py --profile_json parameters/profile_A_params.json \
    #        --n_households 65 --output_dir sim_community
    #
    # 2) assemble the communities:
    #    python build_community.py --sim_dir sim_community \
    #        --counts 1=28,2=11,3=14,4=12 \
    #        --homogeneous_pid 99 --homogeneous_n 65 \
    #        --out_dir community_results
    #
    #    # add a composed empirical reference for a consistency check:
    #    python build_community.py ... --with_empirical \
    #        --baseline_dir ../../data/clean/timeseries/baseline_results
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Loading per-household simulated minute data
# ---------------------------------------------------------------------------

def load_profile_households(pid: str, sim_dir: Path) -> pd.DataFrame:
    """
    Load the per-household minute file for a profile, preferring Parquet.
    Returns a long DataFrame with at least: timestamp, power_w, household_id.
    """
    pq = sim_dir / f"profile_{pid}_minute.parquet"
    csv = sim_dir / f"profile_{pid}_minute.csv"
    if pq.exists():
        df = pd.read_parquet(pq)
    elif csv.exists():
        df = pd.read_csv(csv)
    else:
        raise SystemExit(
            f"[-] Per-household minute file not found for profile {pid} in {sim_dir}.\n"
            f"    Looked for: {pq.name}, {csv.name}\n"
            f"    Run run_simulation.py for this profile first."
        )
    if "household_id" not in df.columns:
        raise SystemExit(
            f"[-] {pq.name if pq.exists() else csv.name} has no 'household_id' column; "
            f"cannot compose a community from it."
        )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ---------------------------------------------------------------------------
# Community assembly
# ---------------------------------------------------------------------------

def assemble_community(members: list[tuple[str, int]], sim_dir: Path
                       ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Sum minute-level load across the requested households.

    members: list of (profile_id, count). For the heterogeneous community
    this is all four profiles at their mix counts; for the homogeneous
    community it is a single (model_a_pid, N_total) entry.

    Takes the FIRST `count` distinct household_ids of each profile (they
    are already independent stochastic draws, so any deterministic subset
    is a valid sample and keeps the run reproducible). Errors out if a
    profile was simulated with fewer households than requested.

    Returns:
      community_df : DataFrame [timestamp, power_w]  (aggregate load)
      kept_long    : DataFrame [timestamp, power_w, uid]  (each contributing
                     household, with a globally-unique uid so peaks never
                     collide across profiles - needed for coincidence factor)
    """
    community: pd.Series | None = None
    kept_frames: list[pd.DataFrame] = []

    for pid, k in members:
        hh = load_profile_households(pid, sim_dir)
        avail = sorted(hh["household_id"].unique())
        if len(avail) < k:
            raise SystemExit(
                f"[-] Profile {pid}: need {k} households but only {len(avail)} "
                f"were simulated. Re-run run_simulation.py for profile {pid} "
                f"with --n_households >= {k}."
            )
        keep = set(avail[:k])
        sub = hh[hh["household_id"].isin(keep)].copy()
        sub["uid"] = f"P{pid}_" + sub["household_id"].astype(str)
        kept_frames.append(sub[["timestamp", "power_w", "uid"]])

        psum = sub.groupby("timestamp")["power_w"].sum()
        community = psum if community is None else community.add(psum, fill_value=0.0)
        print(f"[*] Profile {pid}: added {k} households "
              f"(mean {sub.groupby('uid')['power_w'].mean().mean():.2f} W/household).")

    community_df = community.rename("power_w").reset_index()
    community_df = community_df.sort_values("timestamp").reset_index(drop=True)
    kept_long = pd.concat(kept_frames, ignore_index=True)
    return community_df, kept_long


def coincidence_table(community_df: pd.DataFrame, kept_long: pd.DataFrame,
                      label: str) -> pd.DataFrame:
    """
    Per-day coincidence factor = community coincident peak / sum of the
    individual household peaks that day.

    A homogeneous community (all households sharing the same time windows)
    peaks close to synchronously, giving a HIGH coincidence factor and a
    tall aggregate peak. A heterogeneous community staggers peaks across
    profiles, giving a LOWER coincidence factor and a broader, lower peak.
    The gap between the two is the diversity that a single-profile model
    cannot see, and it drives inverter / peak-dispatch sizing.
    """
    c = community_df.copy()
    c["date"] = pd.to_datetime(c["timestamp"]).dt.date
    comm_peak = c.groupby("date")["power_w"].max()

    k = kept_long.copy()
    k["date"] = pd.to_datetime(k["timestamp"]).dt.date
    hh_peak = k.groupby(["date", "uid"])["power_w"].max()
    sum_indiv = hh_peak.groupby("date").sum()

    cf = (comm_peak / sum_indiv.replace(0, np.nan)).rename("coincidence_factor")
    out = pd.concat(
        [comm_peak.rename("community_peak_w"),
         sum_indiv.rename("sum_individual_peaks_w"),
         cf], axis=1
    ).reset_index()
    out.insert(0, "community", label)
    return out


# ---------------------------------------------------------------------------
# Optional composed empirical reference (consistency check only)
# ---------------------------------------------------------------------------

def build_empirical_reference_daily(members: list[tuple[str, int]],
                                    baseline_dir: Path) -> pd.DataFrame | None:
    """
    Compose a representative-daily-curve empirical community as the
    mix-weighted sum of each profile's measured baseline:

        community_real(t_of_day) = sum_p  k_p * baseline_p(t_of_day)

    where baseline_p is the representative-household curve from
    build_baseline_profiles.py (already an average over contributing
    real users).

    CAVEAT (state this in the paper): scaling a representative-household
    curve by k_p reproduces the mix and the mean level, but NOT the
    within-profile household-to-household diversity, because the raw
    per-user telemetry is not resolved here. It is therefore a check that
    the heterogeneous community sits at the right mix-weighted LEVEL and
    SHAPE, not an independently metered community peak. Day-to-day
    variability (MRSD) cannot be composed this way because the profiles'
    real logging dates do not align, so this reference is a time-of-day
    curve only.
    """
    bins = np.arange(0, 24.25, 0.25)
    centers = bins[:-1]
    total = np.zeros(len(centers))
    found = False

    for pid, k in members:
        f = baseline_dir / f"baseline_profile_{pid}.csv"
        if not f.exists():
            print(f"[!] Baseline for profile {pid} not found ({f.name}); "
                  f"empirical reference will omit it.")
            continue
        b = pd.read_csv(f)
        b["timestamp"] = pd.to_datetime(b["timestamp"])
        b = b.dropna(subset=["power_w"])
        td = b["timestamp"].dt.hour + b["timestamp"].dt.minute / 60.0
        b = b.assign(_bin=pd.cut(td, bins, labels=centers))
        rep = (b.groupby("_bin", observed=True)["power_w"].mean()
                 .reindex(centers).fillna(0.0).values)
        total += k * rep
        found = True
        print(f"[*] Empirical reference: added profile {pid} x{k}.")

    if not found:
        return None
    return pd.DataFrame({"time_decimal": centers, "power_w": total})


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

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


def main():
    ap = argparse.ArgumentParser(
        description="Assemble heterogeneous and homogeneous community load "
                    "curves from run_simulation.py per-household outputs.")
    ap.add_argument("--sim_dir", type=Path, default=Path("simulation_results"),
                    help="Directory with profile_<pid>_minute.* files.")
    ap.add_argument("--counts", type=parse_counts, required=True,
                    help="Heterogeneous mix, e.g. '1=28,2=11,3=14,4=12' "
                         "(the real classified counts).")
    ap.add_argument("--homogeneous_pid", type=str, default=None,
                    help="Profile id of the single averaged Model A run "
                         "(omit to skip building the homogeneous community).")
    ap.add_argument("--homogeneous_n", type=int, default=None,
                    help="Number of Model A households = total community size "
                         "(defaults to the sum of --counts).")
    ap.add_argument("--out_dir", type=Path, default=Path("community_results"))
    ap.add_argument("--with_empirical", action="store_true",
                    help="Also compose the empirical reference daily curve.")
    ap.add_argument("--baseline_dir", type=Path,
                    default=Path("..") / ".." / "data" / "clean" / "timeseries" / "baseline_results",
                    help="Baseline dir (same as validate_simulation.py).")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    n_total = args.homogeneous_n or sum(c for _, c in args.counts)

    print("=" * 64)
    print("Building community load curves")
    print("=" * 64)
    print(f"Mix (heterogeneous) : {args.counts}  (N={sum(c for _, c in args.counts)})")
    print(f"Homogeneous         : "
          f"{'pid ' + args.homogeneous_pid + f' x{n_total}' if args.homogeneous_pid else '(skipped)'}")
    print(f"Sim dir             : {args.sim_dir.resolve()}")
    print(f"Out dir             : {args.out_dir.resolve()}")

    coincidence_frames: list[pd.DataFrame] = []

    # --- Heterogeneous (Model B) -------------------------------------------
    print("\n[*] Heterogeneous community (Model B):")
    het_df, het_kept = assemble_community(args.counts, args.sim_dir)
    het_path = args.out_dir / "community_heterogeneous_minute.csv"
    het_df.to_csv(het_path, index=False)
    print(f"[+] Saved: {het_path.name}  ({len(het_df)} minutes, "
          f"mean {het_df['power_w'].mean():.1f} W, peak {het_df['power_w'].max():.1f} W)")
    coincidence_frames.append(coincidence_table(het_df, het_kept, "heterogeneous"))

    # --- Homogeneous (Model A) ---------------------------------------------
    if args.homogeneous_pid is not None:
        print("\n[*] Homogeneous community (Model A):")
        homo_df, homo_kept = assemble_community(
            [(args.homogeneous_pid, n_total)], args.sim_dir)
        homo_path = args.out_dir / "community_homogeneous_minute.csv"
        homo_df.to_csv(homo_path, index=False)
        print(f"[+] Saved: {homo_path.name}  ({len(homo_df)} minutes, "
              f"mean {homo_df['power_w'].mean():.1f} W, peak {homo_df['power_w'].max():.1f} W)")
        coincidence_frames.append(coincidence_table(homo_df, homo_kept, "homogeneous"))

    # --- Coincidence factor summary ----------------------------------------
    coincidence = pd.concat(coincidence_frames, ignore_index=True)
    cf_path = args.out_dir / "community_coincidence.csv"
    coincidence.to_csv(cf_path, index=False)
    print(f"\n[+] Saved: {cf_path.name}")
    print("\n    Coincidence factor (mean over days) - lower = more diversity:")
    for lbl, g in coincidence.groupby("community"):
        print(f"      {lbl:15s}  CF={g['coincidence_factor'].mean():.3f}  "
              f"community peak={g['community_peak_w'].mean():.1f} W  "
              f"(sum of individual peaks={g['sum_individual_peaks_w'].mean():.1f} W)")

    # --- Optional empirical reference --------------------------------------
    if args.with_empirical:
        print("\n[*] Composed empirical reference (consistency check only):")
        emp = build_empirical_reference_daily(args.counts, args.baseline_dir)
        if emp is not None:
            emp_path = args.out_dir / "community_empirical_daily.csv"
            emp.to_csv(emp_path, index=False)
            print(f"[+] Saved: {emp_path.name}  (representative daily curve, "
                  f"peak {emp['power_w'].max():.1f} W)")
        else:
            print("[!] No baselines found; empirical reference not written.")

    print("\n[+] Done. Next: python validate_community.py --community_dir "
          f"{args.out_dir}")


if __name__ == "__main__":
    main()
