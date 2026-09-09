"""
validate_community.py
=====================
Carries the assembled community load curves (build_community.py) into the
same dual-tier comparison used per-profile in validate_simulation.py, and
adds the aggregate-only metrics that matter at community scale (coincidence
factor, sizing-relevant peak / base load).

What this compares, and why it is framed this way
-------------------------------------------------
There is no independently metered 65-household community total, so the
community layer is NOT a new ground-truth validation. Instead:

  * PRIMARY comparison  - Heterogeneous (Model B) vs Homogeneous (Model A),
    both simulated on the same calendar. This quantifies what the standard
    single-profile approach gets wrong at the aggregate level - the planning
    payoff. The heterogeneous community is used as the *reference* series
    because its per-profile curves each inherit validation against telemetry
    (validate_simulation.py); the homogeneous community is the approximation
    being characterised. In the printed/CSV table the "Real" column is the
    heterogeneous reference and "Sim" is the homogeneous model.

  * OPTIONAL consistency check - Heterogeneous community vs the composed
    empirical reference (mix-weighted sum of measured baselines). This is a
    time-of-day curve check on level and shape only; see the caveat in
    build_community.build_empirical_reference_daily().

Per-profile validation against telemetry remains the empirical anchor and
is unchanged - run validate_simulation.py for that as before.

Usage
-----
    python validate_community.py --community_dir community_results
    python validate_community.py --community_dir community_results --months 5 6
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Reuse the existing, already-reviewed metric + plot machinery unchanged.
from validate_simulation import (
    apply_time_filters,
    calculate_validation_metrics,
    calculate_structural_metrics,
    calculate_ldc_metrics,
    _lcss,
    plot_overlaid_averages,
    plot_load_duration_curve,
    plot_shadows_and_average,
)

BINS = np.arange(0, 24.25, 0.25)
CENTERS = BINS[:-1]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_community_series(path: Path) -> pd.DataFrame:
    """Load a community_*_minute.csv into validate_simulation's schema."""
    if not path.exists():
        print(f"[-] Community file not found: {path}")
        sys.exit(1)
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # one row per timestamp already; group defensively in case of duplicates
    df = df.groupby("timestamp", as_index=False)["power_w"].sum()
    df["p_total"] = df["power_w"]
    df["date_only"] = df["timestamp"].dt.date
    df["time_decimal"] = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60.0
    return df[["timestamp", "p_total", "date_only", "time_decimal"]]


def representative_daily_curve(df: pd.DataFrame) -> np.ndarray:
    """Collapse a full series to a 96-point (15-min) time-of-day curve."""
    d = df.copy()
    d["bin"] = pd.cut(d["time_decimal"], BINS, labels=CENTERS)
    return (d.groupby("bin", observed=True)["p_total"].mean()
              .reindex(CENTERS).fillna(0.0).values)


# ---------------------------------------------------------------------------
# Aggregate-only summaries (sizing + coincidence)
# ---------------------------------------------------------------------------

def sizing_summary(df_het: pd.DataFrame, df_homo: pd.DataFrame | None,
                   coincidence_csv: Path, metrics_dir: Path) -> pd.DataFrame:
    """
    Planning-relevant aggregate quantities for each community, plus the
    Model-A-minus-Model-B delta expressed the way a system sizer reads it.
    """
    def block(df, label):
        s = calculate_structural_metrics(df, label=label)
        p95 = float(np.percentile(df["p_total"], 95))
        peak = float(df["p_total"].max())
        return {
            "community": label,
            "coincident_peak_W": peak,
            "p95_W": p95,
            "base_load_0004_W": s["base_mean"],
            "daily_energy_Wh": s["wh_mean"],
            "modal_peak_hour": s["modal_peak"],
            "mrsd": s["mrsd"],
        }

    rows = [block(df_het, "heterogeneous")]
    if df_homo is not None:
        rows.append(block(df_homo, "homogeneous"))
    summ = pd.DataFrame(rows)

    # fold in mean coincidence factor from build_community output
    if coincidence_csv.exists():
        cf = pd.read_csv(coincidence_csv)
        cf_mean = cf.groupby("community")["coincidence_factor"].mean()
        summ["coincidence_factor"] = summ["community"].map(cf_mean)

    out = metrics_dir / "community_sizing_summary.csv"
    summ.to_csv(out, index=False)

    print("\n" + "=" * 78)
    print(" COMMUNITY SIZING SUMMARY  (what the two modelling choices imply)")
    print("=" * 78)
    print(summ.to_string(index=False))
    if df_homo is not None:
        h = summ.set_index("community")
        def delta(col):
            return h.loc["homogeneous", col] - h.loc["heterogeneous", col]
        def pct(col):
            base = h.loc["heterogeneous", col]
            return 100 * delta(col) / base if base else float("nan")
        print("\n Model A (homogeneous) relative to Model B (heterogeneous):")
        print(f"   coincident peak : {delta('coincident_peak_W'):+.1f} W "
              f"({pct('coincident_peak_W'):+.1f}%)  -> inverter / peak dispatch sizing")
        print(f"   P95 power       : {delta('p95_W'):+.1f} W "
              f"({pct('p95_W'):+.1f}%)")
        print(f"   overnight base  : {delta('base_load_0004_W'):+.1f} W "
              f"({pct('base_load_0004_W'):+.1f}%)  -> battery depth-of-discharge / kWh")
        print(f"   daily energy    : {delta('daily_energy_Wh'):+.1f} Wh "
              f"({pct('daily_energy_Wh'):+.1f}%)  -> generation / PV sizing")
        if "coincidence_factor" in summ.columns:
            print(f"   coincidence f.  : het={h.loc['heterogeneous','coincidence_factor']:.3f}  "
                  f"homo={h.loc['homogeneous','coincidence_factor']:.3f}  "
                  f"(homo>het means the standard model overstates the coincident peak)")
    print("=" * 78 + "\n")
    print(f"[+] Saved sizing summary: {out.name}")
    return summ


def check_against_empirical(df_het: pd.DataFrame, empirical_csv: Path,
                            metrics_dir: Path, epsilon_watts: float = 0.5) -> None:
    """
    Lightweight consistency check of the heterogeneous community against the
    composed empirical reference, on the representative daily curve only
    (Tier 1 + LDC + peak-timing). Structural/variability metrics are not
    computed here because the empirical reference is a single time-of-day
    curve by construction (see build_community caveat).
    """
    if not empirical_csv.exists():
        return
    print("\n[*] Consistency check: heterogeneous community vs composed empirical reference")
    emp = pd.read_csv(empirical_csv)
    ref = emp["power_w"].reindex(range(len(CENTERS))).fillna(0.0).values \
        if len(emp) == len(CENTERS) else emp["power_w"].values
    sim = representative_daily_curve(df_het)
    n = min(len(ref), len(sim))
    ref, sim = ref[:n], sim[:n]

    rmse = float(np.sqrt(np.mean((ref - sim) ** 2)))
    mpdada = (abs(sim.max() - ref.max()) / ref.mean()) if ref.mean() > 0 else float("nan")
    lcss = _lcss(ref, sim, epsilon_watts)
    ldc = calculate_ldc_metrics(ref, sim)
    peak_hr_ref = float(CENTERS[int(np.argmax(ref))])
    peak_hr_sim = float(CENTERS[int(np.argmax(sim))])

    tbl = pd.DataFrame([
        {"Metric": "RMSE (W)", "Value": f"{rmse:.2f}"},
        {"Metric": "LCSS score", "Value": f"{lcss:.3f}"},
        {"Metric": "MPDADA ratio", "Value": f"{mpdada:.3f}"},
        {"Metric": "LDC-RMSE (W)", "Value": f"{ldc['ldc_rmse']:.2f}"},
        {"Metric": "P95 empirical / sim (W)",
         "Value": f"{ldc['p95_real']:.1f} / {ldc['p95_sim']:.1f}"},
        {"Metric": "Peak hour empirical / sim",
         "Value": f"{peak_hr_ref:.2f} / {peak_hr_sim:.2f}"},
    ])
    out = metrics_dir / "community_empirical_consistency.csv"
    tbl.to_csv(out, index=False)
    print(tbl.to_string(index=False))
    print(f"[+] Saved: {out.name}")


# ---------------------------------------------------------------------------
# §4.3 validation figure: black / red / blue community overlay
# ---------------------------------------------------------------------------

def _empirical_curve(empirical_csv: Path) -> np.ndarray | None:
    """Load the composed empirical reference as a CENTERS-aligned curve."""
    if not empirical_csv.exists():
        return None
    emp = pd.read_csv(empirical_csv)
    if len(emp) == len(CENTERS):
        return emp["power_w"].reindex(range(len(CENTERS))).fillna(0.0).values
    # fall back: re-bin on its own time_decimal if it isn't already 96-point
    d = emp.copy()
    d["bin"] = pd.cut(d["time_decimal"], BINS, labels=CENTERS)
    return (d.groupby("bin", observed=True)["power_w"].mean()
              .reindex(CENTERS).fillna(0.0).values)


def plot_community_overlay(df_het: pd.DataFrame,
                           df_homo: pd.DataFrame | None,
                           empirical_csv: Path,
                           figures_dir: Path) -> None:
    """
    The §4.3 figure at community scale, in the checklist's colour scheme:

        black = empirical telemetry (composed reference, if available)
        red   = Model A  (homogeneous community)
        blue  = Model B  (heterogeneous community)

    Each series is collapsed to its representative daily (time-of-day) curve
    so the three sit on one axis. A dot marks each curve's peak, making the
    peak-magnitude and peak-timing divergence - the thing a single-profile
    model misses - legible at a glance and anchorable in prose.
    """
    het = representative_daily_curve(df_het)          # blue: Model B
    homo = representative_daily_curve(df_homo) if df_homo is not None else None  # red: Model A
    emp = _empirical_curve(empirical_csv)             # black: telemetry

    plt.figure(figsize=(11, 6))

    def _draw(curve, color, label, ls="-", lw=3.0, z=2):
        if curve is None:
            return
        plt.plot(CENTERS, curve, color=color, linewidth=lw, linestyle=ls,
                 label=label, zorder=z)
        pk = int(np.argmax(curve))
        plt.scatter([CENTERS[pk]], [curve[pk]], color=color, s=45,
                    zorder=z + 1, edgecolor="white", linewidth=0.8)

    # black underneath, then red, then blue on top (the model of record)
    _draw(emp, "black", "Empirical (composed telemetry)", lw=3.5, z=2)
    _draw(homo, "red", "Model A (homogeneous)", ls="--", lw=2.5, z=3)
    _draw(het, "blue", "Model B (heterogeneous)", lw=2.5, z=4)

    plt.title("Community Load Curve: Empirical vs Model A vs Model B",
              fontsize=14, fontweight="bold")
    plt.xlabel("Hour of the Day", fontsize=12)
    plt.ylabel("Community Power Demand (W)", fontsize=12)
    plt.xticks(np.arange(0, 25, 3))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper left", fontsize=11)
    plt.ylim(bottom=0)
    plt.tight_layout()

    out = figures_dir / "community_overlay_black_red_blue.png"
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[+] Saved §4.3 community overlay: {out.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Validate/compare the assembled community load curves.")
    ap.add_argument("--community_dir", type=Path, default=Path("community_results"),
                    help="Directory written by build_community.py.")
    ap.add_argument("--months", type=int, nargs="+", choices=range(1, 13), default=None,
                    help="Limit to specific months (e.g. --months 5 6).")
    args = ap.parse_args()

    figures_dir = args.community_dir / "figures"
    metrics_dir = args.community_dir / "metrics"
    figures_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    het_path = args.community_dir / "community_heterogeneous_minute.csv"
    homo_path = args.community_dir / "community_homogeneous_minute.csv"
    coincidence_csv = args.community_dir / "community_coincidence.csv"
    empirical_csv = args.community_dir / "community_empirical_daily.csv"

    df_het = load_community_series(het_path)
    df_homo = load_community_series(homo_path) if homo_path.exists() else None
    if df_homo is None:
        print("[!] No homogeneous community found; running heterogeneous-only "
              "summaries. Build Model A to get the A/B comparison.")

    # --- Primary: heterogeneous (reference) vs homogeneous -----------------
    if df_homo is not None:
        ref, cmp = apply_time_filters(df_het.copy(), df_homo.copy(), args.months)
        plot_shadows_and_average(ref, cmp, "community_heterogeneous",
                                 "COMMUNITY_HOMOGENEOUS", figures_dir)
        plot_overlaid_averages(ref, cmp, "community_heterogeneous",
                               "COMMUNITY_HOMOGENEOUS", figures_dir)
        plot_load_duration_curve(ref, cmp, "community_heterogeneous",
                                 "COMMUNITY_HOMOGENEOUS", figures_dir)
        print("\n[i] In the table below, 'Real' = heterogeneous reference "
              "(Model B), 'Sim' = homogeneous (Model A).")
        calculate_validation_metrics(
            ref, cmp, "community_heterogeneous",
            "COMMUNITY_HOMOGENEOUS", metrics_dir)

    # --- Aggregate-only sizing + coincidence summary -----------------------
    # (recompute on the filtered window if months were given)
    df_het_f = df_het
    df_homo_f = df_homo
    if args.months is not None:
        df_het_f = df_het[df_het["timestamp"].dt.month.isin(args.months)]
        if df_homo is not None:
            df_homo_f = df_homo[df_homo["timestamp"].dt.month.isin(args.months)]
    sizing_summary(df_het_f, df_homo_f, coincidence_csv, metrics_dir)

    # --- §4.3 figure: black/red/blue community overlay ---------------------
    plot_community_overlay(df_het_f, df_homo_f, empirical_csv, figures_dir)

    # --- Optional empirical consistency check ------------------------------
    check_against_empirical(df_het_f, empirical_csv, metrics_dir)

    print("[+] Community validation complete!")


if __name__ == "__main__":
    main()
