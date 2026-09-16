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

import textwrap

import matplotlib.pyplot as plt
import numpy as np

import transforms as tf
from style import (
    FIGSIZE_GRID_2x2,
    FIGSIZE_ROW_1x4,
    FIGSIZE_STACK_4x1,
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


# (nrows, ncols, figsize) per layout key. "grid" is the default and the
# only one that was in use before; the other two exist so the figure can be
# placed in a two-column manuscript without being rescaled (see style.py).
LAYOUTS = {
    "grid": (2, 2, FIGSIZE_GRID_2x2),    # double-column float, figure*
    "row": (1, 4, FIGSIZE_ROW_1x4),      # double-column float, figure*
    "stack": (4, 1, FIGSIZE_STACK_4x1),  # single-column float, figure
}


def plot_figure5(
    df,
    out_path,
    profiles=PROFILES,
    basis="mean_day",
    month_label="May",
    annotate_p95=True,
    layout="grid",
):
    """
    basis  "mean_day" (default) sorts the representative daily curve, which
           is what validate_simulation.py's plot_load_duration_curve and
           calculate_ldc_metrics do — so these panels match both the draft
           val_ldc_*.png figures and the LDC-RMSE / P95 values in the
           metrics tables. "pooled" and "per_day" are different curves; see
           transforms.ldc before using them.

    layout "grid"  2x2 at double-column width (7.2in) — the default, unchanged.
           "row"   1x4 across the full double-column width, one panel per
                   profile side by side. Panels are only 1.8in wide, so the
                   x axis drops to three ticks, the axis label is shared, and
                   the P95 note wraps onto two lines.
           "stack" 4x1 at single-column width (3.5in), matching Fig. 4's
                   stacked option, for a figure that sits in one column.

           Both non-default layouts are sized to be placed at 100% scale.
           Shrinking the 7.2in grid into a 3.5in column instead would scale
           the 9pt type down to roughly 4.4pt.
    """
    if layout not in LAYOUTS:
        raise ValueError(
            f"unknown layout {layout!r}; expected one of {sorted(LAYOUTS)}"
        )

    tf.check_frame(df, extra_columns=("profile",))
    apply_style()

    nrows, ncols, figsize = LAYOUTS[layout]
    # squeeze=False keeps `axes` 2-D for every layout, so the row/column
    # indexing below works unchanged whichever geometry is in use.
    fig, axes = plt.subplots(
        nrows, ncols, figsize=figsize, sharex=True, squeeze=False,
    )

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

        # A full profile label is ~35 characters, roughly twice what fits
        # across a 1.8in panel at 9.5pt, and adjacent titles run into each
        # other. Wrapping keeps the names rather than reducing them to bare
        # "P1".."P4" codes the reader would have to look up in the caption.
        ax.set_title(
            textwrap.fill(PROFILE_LABELS[profile], width=20)
            if layout == "row" else PROFILE_LABELS[profile]
        )
        ax.set_ylim(bottom=0)
        # 1.8in panels cannot carry five "100%"-width labels without the
        # end ones colliding, so the row layout keeps 0 / 50 / 100 only.
        fraction_ticks(ax, step=0.5 if layout == "row" else 0.25)

        if annotate_p95:
            gap = p95["socio_technical"] - p95["measured"]
            if layout == "row":
                # On one line this note is wider than a 1.8in panel, and even
                # split in two the value line still overhangs the axes. Three
                # lines keep the longest at ~13 characters, inside the panel.
                note = (
                    f"P95\n{p95['measured']:.2f} → "
                    f"{p95['socio_technical']:.2f} W\n({gap:+.2f})"
                )
            else:
                note = (
                    f"P95: {p95['measured']:.2f} → "
                    f"{p95['socio_technical']:.2f} W ({gap:+.2f})"
                )
            annotate(ax, note, loc="right")

    if layout == "stack":
        # One shared label instead of four repeats: at 3.5in wide the
        # repeated label costs more width than the panels can spare.
        fig.supylabel("Power (W)", fontsize=plt.rcParams["axes.labelsize"])
    else:
        for ax in axes[:, 0]:
            ax.set_ylabel("Power (W)")

    xlabel = "Fraction of the day at or above level"
    if layout == "row":
        # Every panel is a bottom panel here, and the label is far wider
        # than 1.8in, so it goes once under the whole row.
        fig.supxlabel(xlabel, fontsize=plt.rcParams["axes.labelsize"])
    else:
        for ax in axes[-1, :]:
            ax.set_xlabel(xlabel)

    # The suptitle is dropped in the stacked layout: it does not fit on one
    # line at 3.5in, and a two-column manuscript expects the caption to
    # carry it anyway.
    if layout != "stack":
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
