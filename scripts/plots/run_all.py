"""
Render every manuscript figure produced by this folder.

    python run_all.py                 # real results, via data_io.py
    python run_all.py --demo          # synthetic data, layout check only
    python run_all.py --only 5 7      # just those figures
    python run_all.py --out ../../manuscript/Figures

Figures
    4  Measured vs. Socio-Technical mean daily load curves, by profile (May)
    5  Load Duration Curve by profile, measured vs. Socio-Technical
    6  Community-aggregate mean daily load, heterogeneous vs. homogeneous
    7  Community LDC (a) and daily-trace envelopes (b)

Editing inputs: everything about where data comes from lives in data_io.py.
Nothing in this file or in the figure scripts needs to change when paths,
runs or the validation window change.
"""

import argparse
from pathlib import Path

from figure4_profile_load_curves import plot_figure4
from figure5_profile_ldc import plot_figure5
from figure6_community_load_curve import plot_figure6
from figure7_community_ldc_envelope import plot_figure7

DEFAULT_OUT = Path(__file__).resolve().parent / "out"

MONTHS = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
    6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
    11: "November", 12: "December",
}

FILENAMES = {
    4: "figure4_profile_load_curves.png",
    5: "figure5_profile_ldc.png",
    6: "figure6_community_load_curve.png",
    7: "figure7_community_ldc_envelope.png",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--demo", action="store_true",
        help="render from mock_data.py instead of real results (layout only)",
    )
    ap.add_argument(
        "--only", type=int, nargs="+", choices=sorted(FILENAMES),
        default=sorted(FILENAMES), help="subset of figures to render",
    )
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument(
        "--month", type=int, default=None,
        help="override the profile-panel month (default: data_io.VALIDATION_MONTH)",
    )
    ap.add_argument(
        "--ldc-basis", choices=("mean_day", "pooled", "per_day"),
        default="mean_day",
        help="what Fig. 5 and 7a sort. 'mean_day' (default) sorts the "
             "representative daily curve, matching the draft val_ldc_*.png "
             "figures and the LDC-RMSE/P95 values in the metrics tables. "
             "'pooled' sorts every sample and gives a much wider curve that "
             "will NOT reconcile with those tables. See transforms.ldc.",
    )
    ap.add_argument(
        "--band", type=int, nargs=2, default=(5, 95), metavar=("LO", "HI"),
        help="Fig. 7b across-day percentile band (use 0 100 for min-max)",
    )
    ap.add_argument(
        "--no-traces", dest="traces", action="store_false",
        help="Fig. 7b: draw only the percentile band, without the "
             "individual daily curves (traces are on by default)",
    )
    ap.add_argument(
        "--community-month", type=int, default=None,
        help="restrict Fig. 6 and 7 to one month (default: full year)",
    )
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    wants_profiles = any(f in args.only for f in (4, 5))
    wants_community = any(f in args.only for f in (6, 7))

    if args.demo:
        import mock_data
        print("[*] DEMO MODE — synthetic data, do not use these figures\n")
        profile_df = mock_data.get_profile_minutes() if wants_profiles else None
        community_df = mock_data.get_community_minutes() if wants_community else None
        n_households, month_label, window_label = None, "mock", "mock"
    else:
        import data_io
        month = args.month if args.month is not None else data_io.VALIDATION_MONTH
        month_label = MONTHS[month]
        print(f"[*] Loading results (profile panels: {month_label})")
        profile_df = (
            data_io.load_profile_minutes(month=month) if wants_profiles else None
        )
        community_df = (
            data_io.load_community_minutes(month=args.community_month)
            if wants_community else None
        )
        n_households = data_io.N_HOUSEHOLDS
        # The community panels default to the full year, and that window
        # decides how strong Fig. 6/7's contrast looks (see the PREMISE note
        # in figure6). Label it, never leave it implicit.
        window_label = (
            MONTHS[args.community_month] if args.community_month else "full year"
        )

    if 4 in args.only:
        plot_figure4(
            profile_df, args.out / FILENAMES[4],
            n_households=n_households, month_label=month_label,
        )
    if 5 in args.only:
        plot_figure5(
            profile_df, args.out / FILENAMES[5],
            basis=args.ldc_basis, month_label=month_label,
        )
    if 6 in args.only:
        plot_figure6(
            community_df, args.out / FILENAMES[6], window_label,
        )
    if 7 in args.only:
        plot_figure7(
            community_df, args.out / FILENAMES[7],
            basis=args.ldc_basis, band=tuple(args.band),
            traces=args.traces, window_label=window_label,
        )

    print(f"\nFigures written to: {args.out}")


if __name__ == "__main__":
    main()
