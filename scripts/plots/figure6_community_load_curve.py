"""
Figure 6 — Community-aggregate mean daily load: Socio-Technical
(heterogeneous, solid black) reference vs. Survey-Based (homogeneous,
dashed blue) Model.

Note the role switch from Fig. 4/5: here the Socio-Technical run is the
reference and the Survey-Based Model is the one under test, so the
Socio-Technical series takes solid black. See the SERIES ROLES note in
style.py.

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
Model. If Fig. 6 is drawn on the full year while Fig. 4/5 are May panels —
the current default — the difference in window has to be stated explicitly
in both captions, or a reader will assume all four figures share one
window. `window_label` is therefore required rather than optional.

These figures come from the community_results/ aggregate rebuilt by
build_community.py on 2026-08-31, which is consistent with the current
sim_community/ per-profile runs. Re-derive them after any further rebuild:
run_all.py prints the Fig. 7 statistics, and this docstring's table is the
one place the Fig. 6 numbers are recorded.

Input: load_community_minutes() — series, day, time_min, power_w.
"""

import matplotlib.pyplot as plt

import transforms as tf
from style import (
    COMMUNITY_SERIES,
    FIGSIZE_SINGLE,
    annotate,
    apply_style,
    line_kwargs,
    minutes_to_hhmm_ticks,
    save_fig,
)


def plot_figure6(df, out_path, window_label, annotate_peaks=True):
    """window_label is required: see the PREMISE note above."""
    tf.check_frame(df)
    tf.require_series(df, COMMUNITY_SERIES, context="community aggregate")
    tf.check_common_resolution(df)
    apply_style()

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    peaks = {}
    for series in COMMUNITY_SERIES:
        curve = tf.mean_daily_curve(df, series)
        ax.plot(curve["time_min"], curve["power_w"], **line_kwargs(series))
        idx = curve["power_w"].idxmax()
        peaks[series] = (
            int(curve.loc[idx, "time_min"]),
            float(curve.loc[idx, "power_w"]),
        )

    ax.set_ylabel("Mean power (W)")
    ax.set_xlabel("Time of day")
    # Headroom so the taller evening peak does not touch the top spine.
    top = max(p for _, p in peaks.values())
    ax.set_ylim(0, top * 1.15)
    minutes_to_hhmm_ticks(ax, step_min=180)
    ax.legend(loc="upper left")

    if annotate_peaks:
        het_t, het_p = peaks["heterogeneous"]
        hom_t, hom_p = peaks["homogeneous"]
        # Every corner is occupied on this figure: legend upper left,
        # evening peak upper right, base load along the bottom and the
        # homogeneous curve's tail through the lower right. The daytime
        # plateau leaves the mid-panel clear.
        annotate(
            ax,
            f"peak of mean curve\n"
            f"heterogeneous  {het_t // 60:02d}:{het_t % 60:02d}, {het_p:.0f} W\n"
            f"homogeneous  {hom_t // 60:02d}:{hom_t % 60:02d}, {hom_p:.0f} W",
            loc="center left",
        )

    ax.set_title(f"Community-aggregate mean daily load — {window_label}")
    fig.tight_layout()
    save_fig(fig, out_path)


if __name__ == "__main__":
    import data_io
    plot_figure6(
        data_io.load_community_minutes(),
        "out/figure6_community_load_curve.png",
    )
