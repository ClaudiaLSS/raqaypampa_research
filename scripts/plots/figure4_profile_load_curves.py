"""
Figure 4 — Measured vs. simulated (Socio-Technical Model) mean daily load
curves, by Energy Behavior Profile, for May.

2x2 grid, one panel per profile. Measured is the reference (solid black),
the Socio-Technical Model is under test (dashed navy).

PREMISE NOTES
-------------
* The May window is not incidental and belongs in the caption. It is the
  month with continuous telemetry across the logger set, and it falls
  between the community's two mobility peaks (growing season Feb-Apr,
  free-grazing/migration Jul-Sep), which minimises the confounding effect
  of household absence. main.tex states this in the section prose but its
  figure caption omits it — the caption should say "for May".
* Sample sizes are small and unequal: 2 households for P1/P3/P4, 1 for P2.
  Pass n_households so each panel states its own n rather than leaving a
  reader to assume the panels are comparable in weight.
* P2's measured baseline has a real gap — 245 NaN samples covering all of
  31 May and most of 30 May — so its panel rests on 30 days, not 31. The
  annotation reports the actual count per panel.

Input: load_profile_minutes() — profile, series, day, time_min, power_w.
"""

import matplotlib.pyplot as plt

import transforms as tf
from style import (
    FIGSIZE_GRID_2x2,
    PROFILES,
    PROFILE_LABELS,
    PROFILE_SERIES,
    annotate,
    apply_style,
    figure_legend,
    line_kwargs,
    minutes_to_hhmm_ticks,
    save_fig,
)


def plot_figure4(
    df,
    out_path,
    profiles=PROFILES,
    n_households=None,
    share_y=False,
    month_label="May",
):
    """
    df            long table from data_io.load_profile_minutes()
    n_households  optional {profile: n} shown in each panel corner. The
                  measured pools are small and unequal, so stating them in
                  the figure is more honest than leaving it to the caption.
    share_y       False by default. Mean power differs by roughly a factor
                  of three across profiles, so a shared y axis would flatten
                  P2 into the baseline. Set True only if the manuscript
                  argues about absolute magnitudes between panels.
    """
    tf.check_frame(df, extra_columns=("profile",))
    apply_style()

    fig, axes = plt.subplots(
        2, 2, figsize=FIGSIZE_GRID_2x2, sharex=True, sharey=share_y
    )

    for ax, profile in zip(axes.flat, profiles):
        sub = df[df["profile"] == profile]
        tf.require_series(sub, PROFILE_SERIES, context=f"profile {profile}")
        tf.check_common_resolution(sub)

        for series in PROFILE_SERIES:
            curve = tf.mean_daily_curve(sub, series)
            ax.plot(curve["time_min"], curve["power_w"], **line_kwargs(series))

        ax.set_title(PROFILE_LABELS[profile])
        ax.set_ylim(bottom=0)
        minutes_to_hhmm_ticks(ax, step_min=360)

        if n_households:
            # Count days on the measured series alone. The two series are
            # stamped in different years, so a nunique() over the whole
            # subset would double-count.
            n_days = sub.loc[sub["series"] == "measured", "day"].nunique()
            n_hh = n_households.get(profile)
            hh = (
                f"{n_hh} household" + ("s" if n_hh != 1 else "")
                if n_hh is not None else "? households"
            )
            annotate(ax, f"n = {hh} · {n_days} days measured", loc="upper left")

    for ax in axes[:, 0]:
        ax.set_ylabel("Mean power (W)")
    for ax in axes[1, :]:
        ax.set_xlabel("Time of day")

    fig.suptitle(
        f"Mean daily load curve by Energy Behavior Profile — {month_label}"
    )
    fig.tight_layout()

    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure_legend(fig, handles, labels, ncol=2)
    save_fig(fig, out_path)


if __name__ == "__main__":
    import data_io
    plot_figure4(
        data_io.load_profile_minutes(),
        "out/figure4_profile_load_curves.png",
        n_households=data_io.N_HOUSEHOLDS,
    )
