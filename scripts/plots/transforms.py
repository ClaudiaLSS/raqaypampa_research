"""
The reductions behind Fig. 4-7, kept out of the plotting code.

Every figure script consumes one of two long-format tables (see data_io.py
for the schema contract) and reduces it here. Keeping the reductions in one
module means Fig. 4 and Fig. 5 are guaranteed to describe the same
underlying samples, and likewise Fig. 6 and Fig. 7.

  mean_daily_curve   minute-of-day mean            -> Fig. 4, Fig. 6
  ldc                duration-sorted curve         -> Fig. 5, Fig. 7a
  daily_envelope     across-day percentile band    -> Fig. 7b
"""

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ("series", "day", "time_min", "power_w")


def check_frame(df, extra_columns=()):
    """Fail early and loudly on a malformed input table."""
    missing = [
        c for c in (*REQUIRED_COLUMNS, *extra_columns) if c not in df.columns
    ]
    if missing:
        raise ValueError(
            f"input table is missing required column(s) {missing}; "
            f"got {list(df.columns)}. See data_io.py for the schema."
        )
    if df.empty:
        raise ValueError("input table is empty")
    bad = df["time_min"][~df["time_min"].between(0, 1439)]
    if len(bad):
        raise ValueError(
            f"time_min must be 0-1439; found {bad.min()}..{bad.max()}"
        )
    return df


def require_series(df, series_keys, context=""):
    """Fail if an expected series is absent, instead of plotting nothing."""
    present = set(df["series"].unique())
    missing = [s for s in series_keys if s not in present]
    if missing:
        where = f" for {context}" if context else ""
        raise ValueError(
            f"series {missing} absent{where}; present: {sorted(present)}"
        )


def check_common_resolution(df, group_cols=("series",), tolerance=0.05):
    """
    Warn when series compared in one panel were sampled at different rates.

    This matters far more for Fig. 5 and Fig. 7a than for the chronological
    curves. A 1-minute simulated series genuinely contains sharper extremes
    than a 10-minute measured average of the same load, so its LDC sits
    above the measured one at the top end for reasons that have nothing to
    do with model error. Resample both sides onto a common bin in data_io
    before plotting; this check exists to catch it when that is forgotten.

    Returns the list of warning strings (also printed).
    """
    warnings = []
    counts = (
        df.groupby([*group_cols, "day"], observed=True)
        .size()
        .groupby(level=list(range(len(group_cols))), observed=True)
        .median()
    )
    if len(counts) > 1:
        lo, hi = counts.min(), counts.max()
        if hi > 0 and (hi - lo) / hi > tolerance:
            detail = ", ".join(f"{k}={int(v)}/day" for k, v in counts.items())
            msg = (
                f"[!] resolution mismatch: {detail}. Duration-sorted curves "
                f"(Fig. 5, 7a) are not comparable across different sampling "
                f"rates — resample onto a common bin first."
            )
            print(msg)
            warnings.append(msg)
    return warnings


def mean_daily_curve(df, series):
    """
    Mean power at each minute-of-day, averaged over all days present.

    Returns a frame with columns time_min, power_w sorted by time_min.
    """
    sub = df[df["series"] == series]
    if sub.empty:
        raise ValueError(f"no rows for series {series!r}")
    out = (
        sub.groupby("time_min", observed=True)["power_w"]
        .mean()
        .reset_index()
        .sort_values("time_min")
    )
    return out


def ldc(df, series, basis="mean_day"):
    """
    Load Duration Curve: power sorted descending against the fraction of
    time spent at or above that level.

    `basis` decides WHAT gets sorted, and the three options are genuinely
    different curves — not cosmetic variants. Getting this wrong is the
    single easiest way to make a correct pipeline disagree with the
    validation tables, so the default is pinned to the project convention.

    "mean_day" (DEFAULT — matches the rest of the project)
        Average across days first to get the representative daily curve
        (96 fifteen-minute bins), then sort that. This is what
        validate_simulation.py's plot_load_duration_curve and
        calculate_ldc_metrics both do, and what validate_community.py does
        via representative_daily_curve(). The LDC-RMSE and P95 values in
        the metrics tables are computed on THIS basis, and the draft
        val_ldc_*.png figures show THIS curve. It is also the only basis on
        which the axis label "fraction of the day" is literally true, since
        the sorted series is exactly one day long.

    "pooled"
        Sort every sample in the window without averaging (e.g. 31 days x
        96 bins = 2976 points). A defensible object in its own right, and
        arguably the more honest one for sizing questions, because it
        retains the day-to-day extremes that averaging removes. But it is
        NOT what the tables report: for P1 measured it gives a maximum of
        7.50 W and P95 of 4.66 W, against 4.90 W and 4.22 W on the
        "mean_day" basis. Use it only deliberately, and do not quote table
        numbers alongside it.

    "per_day"
        Build one LDC per day, then average the sorted curves across days.
        Different again from sorting the averaged curve. Included for
        completeness; nothing else in the project uses it.

    Returns (fraction, power) arrays of equal length, fraction ascending
    from 0 to 1.
    """
    sub = df[df["series"] == series]
    if sub.empty:
        raise ValueError(f"no rows for series {series!r}")

    if basis == "mean_day":
        power = (
            sub.groupby("time_min", observed=True)["power_w"]
            .mean()
            .sort_index()
            .to_numpy()
        )
        power = np.sort(power)[::-1]
    elif basis == "pooled":
        power = np.sort(sub["power_w"].to_numpy())[::-1]
    elif basis == "per_day":
        per = [
            np.sort(g["power_w"].to_numpy())[::-1]
            for _, g in sub.groupby("day", observed=True)
        ]
        n = min(len(a) for a in per)
        if n == 0:
            raise ValueError(f"a day has no samples for series {series!r}")
        power = np.vstack([a[:n] for a in per]).mean(axis=0)
    else:
        raise ValueError(
            f"unknown basis {basis!r}; expected 'mean_day', 'pooled' or 'per_day'"
        )

    fraction = (np.arange(len(power)) + 0.5) / len(power)
    return fraction, power


def daily_envelope(df, series, band=(5, 95)):
    """
    Across-day spread at each minute-of-day.

    Returns a frame with columns time_min, lo, hi, mean — the `band`
    percentiles and the mean, taken across days. Pass band=(0, 100) for a
    full min-max envelope.
    """
    sub = df[df["series"] == series]
    if sub.empty:
        raise ValueError(f"no rows for series {series!r}")
    lo_q, hi_q = band
    grouped = sub.groupby("time_min", observed=True)["power_w"]
    out = pd.DataFrame(
        {
            "lo": grouped.quantile(lo_q / 100.0),
            "hi": grouped.quantile(hi_q / 100.0),
            "mean": grouped.mean(),
        }
    ).reset_index().sort_values("time_min")
    return out


def band_width_summary(df, series, band=(5, 95)):
    """Mean vertical width of the daily envelope, in W."""
    env = daily_envelope(df, series, band=band)
    return float((env["hi"] - env["lo"]).mean())


def _day_matrix(df, series):
    """days x minute-of-day matrix, complete days only."""
    sub = df[df["series"] == series]
    if sub.empty:
        raise ValueError(f"no rows for series {series!r}")
    wide = sub.pivot_table(
        index="day", columns="time_min", values="power_w"
    ).dropna()
    if wide.empty:
        raise ValueError(f"no complete days for series {series!r}")
    return wide.to_numpy()


def shape_coherence_summary(df, series):
    """
    How repeatable the SHAPE of the daily curve is, independent of level.

    Each day is divided by its own daily mean, removing level differences,
    and correlated against the mean normalised shape. Returns a dict:

        mean_r   average correlation to the mean shape
        min_r    the most atypical day; the tail matters more than the mean
        shape_band  mean p5-p95 width of the level-normalised traces

    Why this exists: Fig. 7b was originally premised on the homogeneous
    Model producing a narrow, near-deterministic band. That does not hold
    (see the CAVEAT in figure7_community_ldc_envelope.plot_figure7), so the
    panel needs a statistic that reports what IS there rather than one
    chosen to confirm the caption. Use these numbers to write the caption.
    """
    raw = _day_matrix(df, series)
    shape = raw / raw.mean(axis=1, keepdims=True)
    mean_shape = shape.mean(axis=0)
    r = np.array([np.corrcoef(day, mean_shape)[0, 1] for day in shape])
    lo = np.percentile(shape, 5, axis=0)
    hi = np.percentile(shape, 95, axis=0)
    return {
        "mean_r": float(r.mean()),
        "min_r": float(r.min()),
        "shape_band": float((hi - lo).mean()),
        "n_days": int(raw.shape[0]),
    }
