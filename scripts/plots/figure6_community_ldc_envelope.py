"""
Figure 6 — Community aggregate, two panels.

(a) Daily-trace envelopes across days, for both communities.
(b) Load Duration Curve, heterogeneous reference vs. homogeneous Model.

Panel (a) carries the mean daily curve of each community, which is the
whole of what used to be a separate Figure 6
(figure6_community_load_curve.py, now deleted). That was not a similar
figure but the same one: mean_daily_curve() and daily_envelope()["mean"]
are the identical groupby("time_min").mean() over the identical table, so
the old figure showed nothing this panel does not. Its window premise
mattered, though, and is kept below.

PREMISE — THE WINDOW DECIDES THE CLAIM
--------------------------------------
How strongly the homogeneous Model overstates community demand depends
almost entirely on the window, so the caption must name it:

    quantity        full year              May only
    mean power      +22.1% (76.2->93.1 W)   +3.1% (89.9->92.8 W)
    P95             +26.9%                  +7.4%
    peak of mean    +27.9%                  +10.5%

Over the full year the overstatement is large and is the substantive
result. In May alone it very nearly disappears, because May is a
high-consumption month for the heterogeneous community (mean 89.9 W
against its 76.2 W annual mean) while the homogeneous Model, built from a
single static year-round average, sits at ~93 W in both windows. That
flatness IS the finding, but it only becomes visible across the year.

Consequence: a May-only Fig. 6 would appear to vindicate the Survey-Based
Model. Fig. 6 is drawn on the full year while Fig. 4/5 are May panels —
the current default — so the difference in window has to be stated
explicitly in both captions, or a reader will assume all three figures
share one window. `window_label` defaults to "" but should never be left
empty: run_all.py always supplies it.

These numbers come from the community_results/ aggregate rebuilt by
build_community.py on 2026-08-31, which is consistent with the current
sim_community/ per-profile runs. This docstring's table is the one place
the mean-power and P95 rows are recorded; the peak-of-mean-curve row and
the spread statistics below are printed on every run.

PREMISE — REVISED, read this before writing the caption
-------------------------------------------------------
The earlier premise for panel (a) was that "the heterogeneous reference
spreads across a wide day-to-day band, the homogeneous Model a narrow,
near-deterministic one." That is NOT what the current runs show, and the
figure must not be captioned that way.

Measured mean p5-p95 band width across days:

    window      heterogeneous   homogeneous   ratio
    full year        51.1 W        38.5 W      1.33x
    May              34.2 W        35.5 W      0.96x

(heterogeneous rebuilt from the current sim_community per-profile runs, so
this is not an artefact of the stale aggregate — the stale file gives
52.6 W / 1.37x, essentially the same conclusion.)

Level-normalised shape coherence tells the same story: correlation of each
day to the mean daily shape is 0.975 heterogeneous vs 0.985 homogeneous
over the full year, and 0.984 vs 0.986 in May. The two are close on the
mean in both windows.

What IS supported, and what the caption can therefore claim:

  * Over the full year the heterogeneous community's day-to-day band is
    about a third wider, and its TAIL is markedly heavier: the most
    atypical day correlates 0.911 with the mean shape, against 0.959 for
    the homogeneous Model. The heterogeneous community produces genuinely
    aberrant days; the homogeneous one does not.
  * Restricted to May the two are indistinguishable on every measure
    tried. A May-only panel cannot carry a variability claim at all.
  * MRSD (0.150 vs 0.016 in the metrics tables) is a WITHIN-day roughness
    statistic, not an across-day one. It does not license a claim about
    day-to-day spread, and citing it for that is the likely origin of the
    original premise.

The real contrast in the community comparison is level and peak, not
spread — see the mean curves in panel (a) and the LDC in panel (b), where
the homogeneous Model overstates mean power by roughly 22% over the full
year.

This function prints all of these statistics on every run so the caption
can be checked against them.

Input: load_community_minutes().
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import transforms as tf
from style import (
    COMMUNITY_SERIES,
    FIGSIZE_WIDE,
    SERIES,
    apply_style,
    band_kwargs,
    figure_legend,
    fraction_ticks,
    line_kwargs,
    minutes_to_hhmm_ticks,
    save_fig,
)


def plot_figure6(
    df,
    out_path,
    basis="mean_day",
    band=(5, 95),
    traces=True,
    max_traces=60,
    trace_alpha=0.12,
    window_label="",
):
    """
    basis       LDC construction for panel (b); "mean_day" by default to
                match validate_community.py, which builds its LDC from
                representative_daily_curve(). See transforms.ldc.
    band        across-day percentiles for panel (a). (5, 95) by default;
                pass (0, 100) for a full min-max envelope, which is more
                dramatic but driven by single outlying days.
    traces      overplot individual daily curves at low alpha, on by
                default: this is what "daily-trace envelopes" describes
                literally, and with the band widths as close as they are
                (see the module docstring) the traces carry more of the
                panel's information than the percentile band does.
    max_traces  cap on overplotted days per series, for legibility.
    trace_alpha opacity of those individual traces. Low enough that the
                mean curve drawn over them stays the dominant mark --- the
                traces are context for it, not a competing series.

    Always read the printed statistics before writing the caption. The
    module docstring explains why the original "wide vs. narrow" premise
    cannot be used.
    """
    tf.check_frame(df)
    tf.require_series(df, COMMUNITY_SERIES, context="community aggregate")
    tf.check_common_resolution(df)
    apply_style()

    fig, (ax_env, ax_ldc) = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

    # --- (a) Daily-trace envelopes ----------------------------------------
    widths, peaks = {}, {}
    for series in COMMUNITY_SERIES:
        env = tf.daily_envelope(df, series, band=band)
        ax_env.fill_between(
            env["time_min"], env["lo"], env["hi"], **band_kwargs(series)
        )
        if traces:
            sub = df[df["series"] == series]
            days = sorted(sub["day"].unique())[:max_traces]
            for day in days:
                trace = sub[sub["day"] == day].sort_values("time_min")
                ax_env.plot(
                    trace["time_min"], trace["power_w"],
                    **line_kwargs(series, label=None, linewidth=0.35,
                                  alpha=trace_alpha, linestyle="-"),
                )
        ax_env.plot(env["time_min"], env["mean"], **line_kwargs(series))
        widths[series] = tf.band_width_summary(df, series, band=band)
        idx = env["mean"].idxmax()
        peaks[series] = (
            int(env.loc[idx, "time_min"]),
            float(env.loc[idx, "mean"]),
        )

    ax_env.set_ylabel("Power (W)")
    ax_env.set_xlabel("Time of day")
    ax_env.set_ylim(bottom=0)
    minutes_to_hhmm_ticks(ax_env, step_min=360)
    ax_env.set_title(
        f"(a) Daily traces and p{band[0]}\u2013p{band[1]} spread"
    )

    # --- (b) Load Duration Curve ------------------------------------------
    for series in COMMUNITY_SERIES:
        fraction, power = tf.ldc(df, series, basis=basis)
        ax_ldc.plot(fraction, power, **line_kwargs(series))

    ax_ldc.set_ylabel("Power (W)")
    ax_ldc.set_xlabel("Fraction of the day")
    ax_ldc.set_ylim(bottom=0)
    fraction_ticks(ax_ldc, step=0.25)
    ax_ldc.set_title("(b) Load Duration Curve")

    # Shared legend. Each band is drawn in its series' own color and the
    # (a) panel title states the percentile range, so line entries alone
    # identify both series.
    handles, labels = [], []
    for series in COMMUNITY_SERIES:
        spec = SERIES[series]
        handles.append(
            Line2D(
                [], [],
                color=spec["color"],
                linestyle=spec["linestyle"],
                linewidth=spec["linewidth"],
            )
        )
        labels.append(spec["label"])

    title = "Community aggregate: day-to-day spread and demand distribution"
    if window_label:
        title = f"{title} — {window_label}"
    fig.suptitle(title)  # window matters for the claim; see module docstring
    fig.tight_layout()

    figure_legend(fig, handles, labels, ncol=2)
    save_fig(fig, out_path)

    ratio = (
        widths["heterogeneous"] / widths["homogeneous"]
        if widths["homogeneous"]
        else float("inf")
    )
    # Peak of the mean curve. Inherited from the deleted mean-daily-load
    # figure, whose caption claim this is: the window table above gives the
    # relative errors, these are the levels behind them.
    for series in COMMUNITY_SERIES:
        t, power = peaks[series]
        print(
            f"    {series:15s} peak of mean curve "
            f"{t // 60:02d}:{t % 60:02d}, {power:.1f} W"
        )

    print(
        f"    p{band[0]}-p{band[1]} band width: "
        f"heterogeneous {widths['heterogeneous']:.1f} W, "
        f"homogeneous {widths['homogeneous']:.1f} W ({ratio:.2f}x)"
    )

    coherence = {s: tf.shape_coherence_summary(df, s) for s in COMMUNITY_SERIES}
    for series in COMMUNITY_SERIES:
        c = coherence[series]
        print(
            f"    {series:15s} shape r to mean {c['mean_r']:.4f} "
            f"(most atypical day {c['min_r']:.3f}), "
            f"normalised band {c['shape_band']:.3f}, n={c['n_days']} days"
        )

    if ratio < 1.5:
        print(
            "    [!] band widths are close — do NOT caption this panel as "
            "\"wide vs. narrow\" / \"near-deterministic\". The defensible "
            "claim is the heavier TAIL of atypical days "
            f"(min r {coherence['heterogeneous']['min_r']:.3f} vs "
            f"{coherence['homogeneous']['min_r']:.3f}), and only over the "
            "full year. See the module docstring."
        )
    return {"band_widths": widths, "coherence": coherence, "peaks": peaks}


if __name__ == "__main__":
    import data_io
    plot_figure6(
        data_io.load_community_minutes(),
        "out/figure6_community_ldc_envelope.png",
    )
