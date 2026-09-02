"""
Synthetic data in the canonical schemas, for checking figure LAYOUT only.

`python run_all.py --demo` renders all four figures from this module, which
is useful for verifying panel geometry, legend placement and label
collisions without touching the real results. The numbers are meaningless —
never put a --demo figure in the manuscript.

The schemas here ARE the contract in data_io.py. If you change one, change
both.
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

BIN_MINUTES = 15
TIME_MIN = np.arange(0, 1440, BIN_MINUTES)

# Rough per-profile shapes, so the panels look plausible and distinguishable.
PROFILE_SHAPE = {
    1: dict(base=0.9, morning=(6.5, 1.3, 1.6), evening=(19.0, 1.4, 3.9)),
    2: dict(base=0.3, morning=(7.0, 1.0, 0.4), evening=(19.5, 1.2, 1.3)),
    3: dict(base=1.0, morning=(6.0, 1.5, 1.9), evening=(20.0, 1.8, 4.2)),
    4: dict(base=0.4, morning=(6.8, 1.1, 0.8), evening=(19.5, 1.3, 2.3)),
}


def _bump(hours, center, width, height):
    return height * np.exp(-0.5 * ((hours - center) / width) ** 2)


def _day(shape, jitter=1.0, smooth=False, dropout=0.0):
    hours = TIME_MIN / 60.0
    y = np.full_like(hours, shape["base"], dtype=float)
    for key in ("morning", "evening"):
        center, width, height = shape[key]
        center = center + RNG.normal(0, 0.35 * jitter)
        height = height * (1 + RNG.normal(0, 0.22 * jitter))
        y = y + _bump(hours, center, width, height)
    if smooth:
        # the homogeneous / survey-based model flattens toward its own mean
        y = shape["base"] + 0.75 * (y - shape["base"])
        y = pd.Series(y).rolling(5, center=True, min_periods=1).mean().to_numpy()
        jitter *= 0.15
    y = y + RNG.normal(0, 0.09 * jitter, size=y.size)
    if dropout and RNG.random() < dropout:
        y = np.full_like(y, shape["base"] * 0.15)
    return np.clip(y, 0, None)


def get_profile_minutes(profiles=(1, 2, 3, 4), n_days=31):
    """Mock of data_io.load_profile_minutes()."""
    rows = []
    for profile in profiles:
        shape = PROFILE_SHAPE[profile]
        for series, jitter, dropout in (
            ("measured", 1.0, 0.10 if profile == 4 else 0.0),
            ("socio_technical", 0.9, 0.08 if profile == 4 else 0.0),
        ):
            for day in range(n_days):
                power = _day(shape, jitter=jitter, dropout=dropout)
                rows.append(
                    pd.DataFrame(
                        {
                            "profile": profile,
                            "series": series,
                            "day": day,
                            "time_min": TIME_MIN,
                            "power_w": power,
                        }
                    )
                )
    return pd.concat(rows, ignore_index=True)


def get_community_minutes(n_days=120, n_households=40):
    """
    Mock of data_io.load_community_minutes().

    Both sides sum n_households independent households, so per-household
    jitter cancels as sqrt(n) in both. What makes the heterogeneous band
    wide in Fig. 7b is the part that does NOT cancel: a shared day-level
    common mode (season/weather shifting the whole community together) and
    occasional whole-household dropouts. The homogeneous side has neither —
    identical representative households with community-average windows
    reproduce nearly the same day every day, which is why the real run
    scores MRSD 0.016 against the heterogeneous run's 0.150.

    Do not "simplify" this to n_households * one_day: that multiplies a
    single household's noise by n and inverts the very contrast the panel
    is built to show.
    """
    shapes = list(PROFILE_SHAPE.values())
    rows = []
    for day in range(n_days):
        common_mode = 1 + RNG.normal(0, 0.16)  # shared across the community
        het = np.zeros_like(TIME_MIN, dtype=float)
        for i in range(n_households):
            het = het + _day(shapes[i % len(shapes)], jitter=1.2, dropout=0.05)
        het = het * common_mode

        hom = np.zeros_like(TIME_MIN, dtype=float)
        for _ in range(n_households):
            hom = hom + _day(PROFILE_SHAPE[1], jitter=1.0, smooth=True)

        for series, power in (("heterogeneous", het), ("homogeneous", hom)):
            rows.append(
                pd.DataFrame(
                    {
                        "series": series,
                        "day": day,
                        "time_min": TIME_MIN,
                        "power_w": power,
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)
