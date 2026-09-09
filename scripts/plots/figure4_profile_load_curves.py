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
* Sample sizes are small and unequal: 2 households for P1/P3/P4, 1 for P2,
  and P2's measured baseline has a real gap (245 NaN samples covering all
  of 31 May and most of 30 May), so its panel rests on 30 days, not 31.
  The panels no longer state this — the caption must carry it, or a reader
  will assume they are comparable in weight.

Input: load_profile_minutes() — profile, series, day, time_min, power_w.
"""

import matplotlib.pyplot as plt

import transforms as tf
from style import (
    FIGSIZE_GRID_2x2,
    PROFILES,
    PROFILE_LABELS,
    PROFILE_SERIES,
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
    share_y=False,
    month_label="May",
):
    """
    df            long table from data_io.load_profile_minutes()
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
    )
