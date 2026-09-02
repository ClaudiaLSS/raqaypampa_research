"""
Figure 5 — Load Duration Curve by profile: measured (solid black) vs.
Socio-Technical simulated (dashed navy) power, each sorted descending
against the fraction of the day at or above that level.

Discarding timing isolates how well the model reproduces the distribution
of demand levels a household sits at — which is also the sizing-relevant
question, since inverter and battery ratings depend on how long a
household sits at each level rather than on when it does.

PREMISE NOTES
-------------
* The "Provisional — panels to be regenerated against this validation run"
  qualifier is now obsolete and should come out of the caption. These
  panels ARE generated against the current run, by this script, in the
  journal style defined in style.py. The equivalent note in main.tex
  ("Provisional styling — to be replaced with journal-formatted version")
  should go too, along with the four \includegraphics pointing at
  validate_simulation.py's val_ldc_*.png outputs, which this figure
  replaces.
* The panels sort the representative daily curve (the "mean_day" basis),
  matching validate_simulation.py's plot_load_duration_curve and
  calculate_ldc_metrics. Figure, draft val_ldc_*.png and metrics table
  therefore all describe the same curve. Pooling every sample instead
  produces a visibly different, much wider curve — see transforms.ldc.

Input: load_profile_minutes() — the same table Fig. 4 uses, so the two
figures are guaranteed to describe the same samples.
"""

import matplotlib.pyplot as plt
import numpy as np

import transforms as tf
from style import (
    FIGSIZE_GRID_2x2,
    PROFILES,
    PROFILE_LABELS,
    PROFILE_SERIES,
    annotate,
    apply_style,
    figure_legend,
    fraction_ticks,
    line_kwargs,
    save_fig,
)


def plot_figure5(
    df,
    out_path,
    profiles=PROFILES,
    basis="mean_day",
    month_label="May",
    annotate_p95=True,
):
    """
    basis  "mean_day" (default) sorts the representative daily curve, which
           is what validate_simulation.py's plot_load_duration_curve and
           calculate_ldc_metrics do — so these panels match both the draft
           val_ldc_*.png figures and the LDC-RMSE / P95 values in the
           metrics tables. "pooled" and "per_day" are different curves; see
           transforms.ldc before using them.
    """
    tf.check_frame(df, extra_columns=("profile",))
    apply_style()

    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE_GRID_2x2, sharex=True)

    for ax, profile in zip(axes.flat, profiles):
        sub = df[df["profile"] == profile]
        tf.require_series(sub, PROFILE_SERIES, context=f"profile {profile}")
        tf.check_common_resolution(sub)

        p95 = {}
        for series in PROFILE_SERIES:
            fraction, power = tf.ldc(sub, series, basis=basis)
            ax.plot(fraction, power, **line_kwargs(series))
            # np.percentile, matching calculate_ldc_metrics' p95_real /
            # p95_sim exactly. NOT the level at 5% duration, which on a
            # peaky 96-bin curve reads noticeably higher (4.75 vs 4.22 W
            # for P1 measured).
            p95[series] = float(np.percentile(power, 95))

        ax.set_title(PROFILE_LABELS[profile])
        ax.set_ylim(bottom=0)
        fraction_ticks(ax, step=0.25)

        if annotate_p95:
            gap = p95["socio_technical"] - p95["measured"]
            annotate(
                ax,
                f"P95: {p95['measured']:.2f} → {p95['socio_technical']:.2f} W "
                f"({gap:+.2f})",
            )

    for ax in axes[:, 0]:
        ax.set_ylabel("Power (W)")
    for ax in axes[1, :]:
        ax.set_xlabel("Fraction of the day at or above level")

    fig.suptitle(
        f"Load Duration Curve by Energy Behavior Profile — {month_label}"
    )
    fig.tight_layout()

    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure_legend(fig, handles, labels, ncol=2)
    save_fig(fig, out_path)


if __name__ == "__main__":
    import data_io
    plot_figure5(
        data_io.load_profile_minutes(),
        "out/figure5_profile_ldc.png",
    )
