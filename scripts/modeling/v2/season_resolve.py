"""
season_resolve.py
==================
Single shared definition of the four canonical seasons, the function that
resolves a VA's baseline + `seasonal_overrides` into one season's
parameters, and the equivalent resolution for the profile-level
**occupancy** block (`prob_home`).

Both extract_parameters.py (for its optional --season flag) and
run_simulation.py (for actual simulation, per season block) import this
module rather than each defining their own copy. Having season logic in
two places was exactly how the JSON format and run_simulation.py drifted
out of sync before - this module exists specifically so extraction and
simulation can't silently disagree about what a season means or how an
override is applied.

Occupancy lives here for the same reason, and validation lives here
rather than in the parser so that a hand-edited JSON gets checked at
simulation time too, not only at extraction time.
"""

VALID_SEASONS = {"planting", "growing", "harvesting", "free_grazing"}

# Calendar mapping - used by run_simulation.py to build the year's season
# blocks. Kept here (not duplicated in run_simulation.py) for the same
# single-source-of-truth reason as VALID_SEASONS above.
SEASON_MONTHS: dict[str, list[int]] = {
    "planting":     [10, 11, 12, 1],
    "growing":      [2, 3, 4],
    "harvesting":   [5, 6],
    "free_grazing": [7, 8, 9],
}
MONTH_TO_SEASON: dict[int, str] = {
    m: s for s, months in SEASON_MONTHS.items() for m in months
}


def resolve_va_params(va: dict, season: str) -> dict:
    """
    Return a copy of a VA's parameter dict with seasonal overrides applied
    for `season`. Baseline values are used unchanged for any parameter
    that has no override defined for this season. `seasonal_overrides`
    itself is dropped from the returned dict, since it's extraction
    metadata, not a RAMP/Appliance kwarg.

    Raises ValueError on an unrecognized season name rather than silently
    falling back to baseline - a typo'd season should be loud, not a
    quiet no-op.
    """
    if season not in VALID_SEASONS:
        raise ValueError(
            f"Unknown season '{season}'. Valid seasons: {sorted(VALID_SEASONS)}"
        )
    resolved = {k: v for k, v in va.items() if k != "seasonal_overrides"}
    overrides = va.get("seasonal_overrides", {}).get(season, {})
    resolved.update(overrides)
    return resolved


# ---------------------------------------------------------------------------
# Household-level occupancy (`prob_home`)
# ---------------------------------------------------------------------------
# The occupancy mask is a HOUSEHOLD-level axis, not a per-appliance one: one
# presence draw per household per day gates every VA of that household at
# once. It therefore lives on the profile, not on a VA, and is carried in the
# profile markdown's §6 as a single ```yaml occupancy fence (see
# extract_parameters.py's module docstring for the authoring convention and
# each profile's §6 for its derivation).
#
# Semantics, matching RAMP's `User.prob_home`:
#     P(a VA runs on a given day) = prob_home * occasional_use
# so the two draws are independent and multiplicative. `prob_home = None`
# disables the mask entirely and consumes no random number, leaving the
# random stream identical to a run without the feature - which is why a
# profile with no absence evidence should say `prob_home: null` rather than
# `1.0`.

OCCUPANCY_KEYS = {"prob_home", "seasonal_prob_home", "occasional_use_basis"}

# How to read each VA's `occasional_use` once the mask is active:
#   present_conditional - the authored value is already "fraction of HOME
#       days" and is passed to RAMP unchanged. Mean energy falls by roughly
#       the absence fraction, which is the point of modelling absence.
#   all_days - the authored value is "fraction of ALL days" and is divided by
#       prob_home so the mean load curve is preserved and only the day-to-day
#       variance changes. Capped at 1.0: an appliance cannot run more often
#       than every single home day.
VALID_OCCASIONAL_USE_BASES = {"present_conditional", "all_days"}
DEFAULT_OCCASIONAL_USE_BASIS = "present_conditional"

# What resolve_occupancy returns when a profile carries no occupancy block at
# all: mask off, values used as authored. Keeps profiles written before this
# feature existed (and Model A's hand-built parameters) working unchanged.
OCCUPANCY_DISABLED = {
    "prob_home": None,
    "occasional_use_basis": DEFAULT_OCCASIONAL_USE_BASIS,
}


def _check_probability(value, label: str, where: str) -> float | None:
    """Validate one probability-or-None field, returning it as float/None."""
    if value is None:
        return None
    # bool is an int subclass, and `prob_home: true` in YAML is a typo worth
    # catching rather than silently reading as 1.0.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"{where}: {label} must be a number in [0, 1] or null, "
            f"got {value!r} ({type(value).__name__})."
        )
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(
            f"{where}: {label} is {value}, it must be a probability within [0, 1]."
        )
    return float(value)


def validate_occupancy(block: dict, where: str = "occupancy block") -> dict:
    """
    Validate a profile-level occupancy block and return it normalized, with
    all three keys always present (`prob_home`, `seasonal_prob_home`,
    `occasional_use_basis`).

    Every failure raises. These blocks are authored by hand in a truth file
    and read straight into a published simulation, so a typo'd key or an
    out-of-range probability has to be loud - the failure mode of a silently
    ignored `prob_hom:` is a run that looks fine and models no absence at all.
    """
    if not isinstance(block, dict):
        raise ValueError(
            f"{where}: expected a mapping of "
            f"{sorted(OCCUPANCY_KEYS)}, got {type(block).__name__}."
        )

    unknown = set(block) - OCCUPANCY_KEYS
    if unknown:
        raise ValueError(
            f"{where}: unknown key(s) {sorted(unknown)}. "
            f"Valid keys: {sorted(OCCUPANCY_KEYS)}."
        )

    prob_home = _check_probability(block.get("prob_home"), "prob_home", where)

    seasonal_raw = block.get("seasonal_prob_home") or {}
    if not isinstance(seasonal_raw, dict):
        raise ValueError(
            f"{where}: seasonal_prob_home must be a mapping of season -> "
            f"probability, got {type(seasonal_raw).__name__}."
        )
    unknown_seasons = set(seasonal_raw) - VALID_SEASONS
    if unknown_seasons:
        raise ValueError(
            f"{where}: seasonal_prob_home names unknown season(s) "
            f"{sorted(unknown_seasons)}. Valid seasons: {sorted(VALID_SEASONS)}."
        )
    seasonal = {
        season: _check_probability(value, f"seasonal_prob_home[{season}]", where)
        for season, value in seasonal_raw.items()
    }

    basis = block.get("occasional_use_basis", DEFAULT_OCCASIONAL_USE_BASIS)
    if basis not in VALID_OCCASIONAL_USE_BASES:
        raise ValueError(
            f"{where}: occasional_use_basis is {basis!r}, must be one of "
            f"{sorted(VALID_OCCASIONAL_USE_BASES)}. This declares whether the "
            f"authored occasional_use values are a fraction of HOME days "
            f"('present_conditional') or of ALL days ('all_days')."
        )

    return {
        "prob_home": prob_home,
        "seasonal_prob_home": seasonal,
        "occasional_use_basis": basis,
    }


def resolve_occupancy(profile: dict, season: str) -> dict:
    """
    Resolve a profile's occupancy block for one season, returning
    ``{"prob_home": float | None, "occasional_use_basis": str}``.

    A season listed in `seasonal_prob_home` uses that value; every other
    season falls back to the block's baseline `prob_home`. Both levels accept
    null, so "mask off except in free grazing" is expressible as a null
    baseline plus one seasonal entry, and "mask on except in harvesting" as
    the reverse.

    A profile with no `occupancy` key resolves to OCCUPANCY_DISABLED rather
    than raising - absence of the block means the mask was never authored for
    that profile, which is a valid state (Profiles 1 and 2 both declare it
    explicitly as `prob_home: null`, but a pre-feature JSON simply has no
    block at all).
    """
    if season not in VALID_SEASONS:
        raise ValueError(
            f"Unknown season '{season}'. Valid seasons: {sorted(VALID_SEASONS)}"
        )

    block = profile.get("occupancy")
    if not block:
        return dict(OCCUPANCY_DISABLED)

    where = f"occupancy block of profile {profile.get('profile_id', '?')}"
    validated = validate_occupancy(block, where=where)

    prob_home = validated["prob_home"]
    if season in validated["seasonal_prob_home"]:
        prob_home = validated["seasonal_prob_home"][season]

    return {
        "prob_home": prob_home,
        "occasional_use_basis": validated["occasional_use_basis"],
    }


def rescale_occasional_use(
    occasional_use: float, prob_home: float | None, basis: str
) -> tuple[float, bool]:
    """
    Convert an authored `occasional_use` into the present-conditional value
    RAMP expects, returning ``(value, was_capped)``.

    Under `present_conditional` (the default) this is a no-op: the authored
    value already means "fraction of HOME days", which is what RAMP reads it
    as once the mask is active.

    Under `all_days` the authored value means "fraction of ALL days", so it is
    divided by `prob_home` to hold the mean load curve fixed while absence
    redistributes it onto fewer, fuller days. The result is capped at 1.0 and
    the cap is reported rather than swallowed: hitting it means the authored
    frequency is incompatible with the authored absence rate (the appliance
    would have to run more often than every single home day), so the mean is
    NOT preserved for that VA and the caller should say so.
    """
    value = float(occasional_use)
    if basis != "all_days" or prob_home is None:
        return value, False
    if prob_home == 0.0:
        # Never home: no day survives the presence draw, so occasional_use is
        # irrelevant to the output. Report the cap so the log records that the
        # requested rescaling was unachievable.
        return 1.0, True
    scaled = value / prob_home
    if scaled > 1.0:
        return 1.0, True
    return scaled, False