"""
Shared style conventions for the Raqaypampa manuscript figures (Fig. 4-7).

Import this in every figure script so colors, line weights and axis
formatting stay identical across the whole set.

SERIES ROLES
------------
The same model appears in two different roles in the manuscript, and the
role — not the model — decides the styling:

  Fig. 4 / 5   measured telemetry is the reference (solid black) and the
               Socio-Technical model is under test (dashed blue).
  Fig. 6       the Socio-Technical heterogeneous run becomes the reference
               (solid blue) and the Survey-Based homogeneous Model is
               under test (dashed green).

So there are four series keys, not three:

  "measured"         solid black    Fig. 4, 5
  "socio_technical"  dashed blue    Fig. 4, 5
  "heterogeneous"    solid blue     Fig. 6
  "homogeneous"      dashed green   Fig. 6

In both pairs the reference is solid and the model under test is dashed,
so a reader carries one visual convention across all three figures. Note
that solid black marks the reference only in Fig. 4/5; Fig. 6's reference
is the Socio-Technical run, which keeps its own blue and takes the solid
stroke.

COLOR CHOICE
------------
STALE: the separations below were computed for an earlier black/navy
pairing (#21467f, #1f77b4). The inks actually in use are now INK,
LIGHTBLUE and GREEN as defined under "Series inks", and the community
pair is blue vs green rather than black vs blue. Re-run the check before
citing these numbers.

Every pair is separated by linestyle as well as hue, so identity is never
carried by color alone. Hues were checked for colorblind separation rather
than picked by eye (OKLab dE, x100):

  black vs navy #21467f    dE 20.9 normal / 20.2 deutan / 20.0 tritan
  black vs blue #1f77b4    dE 35.4 normal / 34.1 deutan / 35.9 tritan

Note on navy: the obvious #1f3864 scores only dE 15.2, right on the
readability floor and visibly muddy against black on paper. #21467f still
reads as navy and clears the floor comfortably. Do not darken it.

Black is deliberately used as a series color here, which a dashboard
palette would not do — in a print figure black is the conventional
"reference / ground truth" ink, and both pairs rely on that reading.
"""

from pathlib import Path

import matplotlib.pyplot as plt

# --- Series inks ----------------------------------------------------------
INK = "#1a1a1a"    # reference series (measured; Fig. 4/5 only)
LIGHTBLUE = "#2A78D6"   # Socio-Technical model, plotted against measured and also heterogeneus community
GREEN = "#3F9142"  # Survey-Based (heterogeneous) Model

# --- Non-data inks --------------------------------------------------------
TEXT = "#1a1a1a"
TEXT_MUTED = "#5c5c58"
GRID = "#c9c9c4"

# Series specifications. `band` is the fill color for percentile envelopes
# (Fig. 6a); `band_alpha` keeps overlapping bands readable.
SERIES = {
    "measured": {
        "label": "Measured",
        "color": INK,
        "linestyle": "-",
        "linewidth": 1.5,
        "zorder": 3,
        "band_alpha": 0.18,
    },
    "socio_technical": {
        "label": "Socio-Technical Model",
        "color": LIGHTBLUE,
        "linestyle": "--",
        "linewidth": 1.5,
        "zorder": 2,
        "band_alpha": 0.20,
    },
    "heterogeneous": {
        "label": "Socio-Technical (heterogeneous)",
        "color": LIGHTBLUE,
        "linestyle": "-",
        "linewidth": 1.8,
        "zorder": 3,
        "band_alpha": 0.18,
    },
    "homogeneous": {
        "label": "Survey-Based (homogeneous)",
        "color": GREEN,
        "linestyle": "--",
        "linewidth": 1.5,
        "zorder": 2,
        "band_alpha": 0.22,
    },
}

# Draw order within each figure: reference first in the legend.
PROFILE_SERIES = ("measured", "socio_technical")
COMMUNITY_SERIES = ("heterogeneous", "homogeneous")

PROFILE_LABELS = {
    1: "P1 — Educational & Agricultural Core",
    2: "P2 — Isolated Elderly",
    3: "P3 — Extended & Multi-Tasking Hub",
    4: "P4 — System Breakers",
}

PROFILES = (1, 2, 3, 4)

# --- Figure sizing (single-column 3.5in / double-column 7.2in) ------------
FIGSIZE_SINGLE = (5.2, 3.6)
FIGSIZE_GRID_2x2 = (7.2, 5.4)
FIGSIZE_WIDE = (7.2, 3.2)

DPI = 300

BASE_RC = {
    "font.size": 9,
    "axes.titlesize": 9.5,
    "axes.labelsize": 9,
    "legend.fontsize": 8.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": TEXT_MUTED,
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": TEXT_MUTED,
    "ytick.color": TEXT_MUTED,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.alpha": 0.55,
    "grid.linewidth": 0.5,
    "legend.frameon": False,
    "figure.dpi": 120,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
}


def apply_style():
    """Call once at the top of any figure function."""
    plt.rcParams.update(BASE_RC)


def line_kwargs(series, **overrides):
    """Matplotlib kwargs for a series key. Raises on an unknown key."""
    if series not in SERIES:
        raise KeyError(
            f"unknown series {series!r}; expected one of {sorted(SERIES)}"
        )
    spec = SERIES[series]
    kwargs = {
        "label": spec["label"],
        "color": spec["color"],
        "linestyle": spec["linestyle"],
        "linewidth": spec["linewidth"],
        "zorder": spec["zorder"],
        "solid_capstyle": "round",
    }
    kwargs.update(overrides)
    return kwargs


def band_kwargs(series, **overrides):
    """Matplotlib kwargs for a fill_between envelope of a series."""
    spec = SERIES[series]
    kwargs = {
        "color": spec["color"],
        "alpha": spec["band_alpha"],
        "linewidth": 0,
        "zorder": spec["zorder"] - 1,
    }
    kwargs.update(overrides)
    return kwargs


def minutes_to_hhmm_ticks(ax, step_min=360):
    """Format a 0-1439 minute-of-day x axis as HH:00 labels."""
    ticks = list(range(0, 1440 + 1, step_min))
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t // 60:02d}:00" for t in ticks])
    ax.set_xlim(0, 1440)


def fraction_ticks(ax, step=0.25):
    """Format a 0-1 duration-fraction x axis as percentages."""
    n = int(round(1 / step))
    ticks = [i * step for i in range(n + 1)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t * 100:.0f}%" for t in ticks])
    ax.set_xlim(0, 1)


def panel_label(ax, letter, dx=-0.14, dy=1.06):
    """
    Put a bold (a) / (b) panel label above the axes.

    No current caller: Fig. 6 carries its letters in the panel titles
    instead, which keeps the label from colliding with the top y-tick.
    """
    ax.text(
        dx, dy, f"({letter})",
        transform=ax.transAxes,
        fontsize=10, fontweight="bold", va="top", ha="left",
    )


def annotate(ax, text, loc="upper right", boxed=True):
    """
    Small muted corner note, e.g. sample sizes.

    boxed draws the text on an opaque rounded panel. The notes sit inside
    the axes, where gridlines and the curves themselves run underneath the
    glyphs and break up their strokes; the panel masks whatever it covers
    so the text stays legible. Pass boxed=False only where the note lands
    on genuinely empty background.
    """
    xy = {
        "upper right": (0.98, 0.96, "right", "top"),
        "upper left": (0.02, 0.96, "left", "top"),
        "lower right": (0.98, 0.04, "right", "bottom"),
        "lower left": (0.02, 0.04, "left", "bottom"),
        # For a two-peak daily load curve the corners are all occupied
        # (morning peak, evening peak, base load) but the daytime plateau
        # leaves the mid-panel empty. No current caller: this was the
        # mean-daily-load figure's slot, and that figure is gone.
        "center left": (0.30, 0.70, "left", "top"),
        # A Load Duration Curve descends from left to right, so its whole
        # right flank is open. Sitting lower than "upper right" uses that
        # space and clears the title band above. Used by Fig. 5.
        "right": (0.98, 0.75, "right", "top"),
    }[loc]
    bbox = dict(
        boxstyle="round,pad=0.35",
        facecolor="white",
        edgecolor=GRID,
        linewidth=0.5,
        alpha=0.92,
    ) if boxed else None

    ax.text(
        xy[0], xy[1], text,
        transform=ax.transAxes, fontsize=7.5, color=TEXT_MUTED,
        ha=xy[2], va=xy[3],
        # Above the gridlines (0.5-ish) and the plotted series (2).
        zorder=6, bbox=bbox,
    )


def axes_legend(ax, loc="upper left", ncol=1):
    """
    Legend drawn inside the axes, on an opaque panel.

    BASE_RC turns legend frames off, which is right for the shared legend
    below a figure but not for one sitting over the plot: the gridlines
    and the curves run straight through the label text. This restores the
    frame with the same white panel and hairline edge as annotate(), and
    lifts it above the series. No current caller — every surviving figure
    puts its legend below the axes via figure_legend() — but kept for the
    next figure that needs one inside the plot.
    """
    leg = ax.legend(
        loc=loc, ncol=ncol,
        frameon=True, framealpha=0.92,
        facecolor="white", edgecolor=GRID,
    )
    leg.get_frame().set_linewidth(0.5)
    leg.set_zorder(6)
    return leg


def figure_legend(fig, handles, labels, ncol=2, y=0.03):
    """
    One shared legend below a multi-panel figure.

    Call fig.tight_layout() BEFORE this, not after: tight_layout ignores
    figure-level legends, so adding the legend first lets tight_layout
    reclaim its space and the legend lands on top of the x-axis labels.
    savefig(bbox_inches="tight") expands the canvas to include it.

    y is the figure-fraction anchor for the legend's top edge. It sits just
    inside the bottom of the tight_layout box rather than below it, so the
    legend rides close under the x-axis labels instead of floating away
    from the panels. Raise it further only after checking the legend does
    not collide with the x-axis labels.
    """
    fig.legend(
        handles, labels,
        loc="upper center", bbox_to_anchor=(0.5, y),
        ncol=ncol, frameon=False,
    )


def save_fig(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    print(f"[+] {path}")
    plt.close(fig)
