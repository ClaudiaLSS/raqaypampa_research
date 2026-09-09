"""
extract_parameters.py
=====================
Parses Raqaypampa profile markdown files and writes one JSON parameter
file per profile (plus a combined file) that Script 2 uses to build the
RAMP model.

This script is the single source-of-truth adapter: edit the markdowns,
re-run this script, and the simulation picks up the changes automatically.
It works with any number of profile markdowns that follow the same
document convention — drop a new file in PROFILES_DIR and it will be
included in the next extraction run.

Usage
-----
    python extract_parameters.py
    python extract_parameters.py --profiles_dir path/to/markdowns --output_dir path/to/params

Markdown convention (v3 — fenced-YAML VAs + a profile-level occupancy block)
----------------------------------------------------------------------------
Profile title line:
    # Profile <N>: <Name> — RAMP truth file (protocol-applied)

Population block (fenced, first ``` block in the file):
    ```
    Population: N_survey = <int> (...)
                N_interview = <int> (...)
    ...
    ```

Section headers (numbered, one canonical set):
    ## Methodological basis
    ## 1. Demographic summary
    ## 2. The driving social rules
    ## 3. Appliance inventory — [SPEC]
    ## 4. Daily social practices and anthropological windows
    ## 5. Virtual Appliance parameterisation
    ## 6. Seasonality
    ## 7. Provenance (anchor quotes → parameters)
    ## 8. Open items carried forward

Virtual Appliance blocks, each a level-3 heading immediately followed
(after a blank line) by a fenced YAML block holding ONLY machine-readable
values — no narrative, no derivation tags, no markdown emphasis:

    ### VA<N> — <label> (<hardware>)

    ```yaml
    power: 3
    num_windows: 1
    window_1: [300, 420]           # [start_min, end_min], matches RAMP's window_1/window_2/window_3
    func_time: 84
    func_cycle: 50
    time_fraction_random_variability: 0.20
    random_var_w: 0.30
    occasional_use: 0.20
    thermal_p_var: 0.2             # optional
    status: placeholder_artifact   # optional (window-continuity filler)
    ```

Keys are RAMP's own `Appliance.__init__`/`Appliance.windows()` kwarg names
verbatim (`power`, `num_windows`, `window_1`/`window_2`/`window_3`,
`func_time`, `func_cycle`, `time_fraction_random_variability`,
`random_var_w`, `occasional_use`, `thermal_p_var`), so a parsed VA dict can
be passed to those calls with `**appliance` after stripping the extraction-
only keys (`index`, `name`, `retired`, `status`), rather than needing a
translation step.

A VA heading with **no** fenced YAML block immediately following it is a
**retired VA**: a real, evidenced zero, not a behavioral estimate, and it
is not passed to RAMP. It is still recorded (with `retired: true` and no
parameters) so the appliance-index numbering stays comparable across
profiles.

Occupancy block (profile-level, at most one per file)
-----------------------------------------------------
Household-level structural absence is not a per-appliance parameter — one
presence draw per household per day gates *every* VA of that household at
once — so it is authored once per profile rather than per VA, in a fence
tagged ``occupancy`` (conventionally in ``## 6. Seasonality``, next to the
derivation it belongs to):

    ```yaml occupancy
    prob_home: 0.96                  # baseline: P(household is home on a given day)
    occasional_use_basis: present_conditional
    seasonal_prob_home:              # optional per-season overrides
      free_grazing: 0.78
    ```

The ``occupancy`` word in the fence info string is what distinguishes this
block from a VA's parameter fence, which opens with a bare ```yaml — the two
regexes are mutually exclusive by construction, so an occupancy block can
never be mistaken for a VA's baseline or seasonal fence and vice versa.

Keys (all optional; validated by season_resolve.validate_occupancy):
  ``prob_home``             probability in [0, 1], or ``null`` to disable the
                            mask. Maps to RAMP's ``User.prob_home``.
  ``seasonal_prob_home``    mapping of canonical season name -> probability (or
                            ``null``); seasons absent from it use ``prob_home``.
  ``occasional_use_basis``  ``present_conditional`` (default — authored
                            ``occasional_use`` values are a fraction of HOME
                            days, passed through unchanged) or ``all_days``
                            (fraction of ALL days, divided by ``prob_home`` so
                            the mean load curve is preserved).

A profile with no occupancy fence at all simulates with the mask off, exactly
as before this feature existed. A profile with no absence evidence should still
say so explicitly with ``prob_home: null`` — that records the finding in the
truth file, and ``null`` (unlike ``1.0``) also skips the presence draw entirely,
leaving that profile's random stream bit-identical to a pre-feature run.

Everything outside the YAML fences (narrative, quotes, derivation tags,
provenance tables, open items, etc.) is intentionally NOT parsed by this
script — it exists for human readers and paper-writing, not for the
simulation pipeline. The parser is therefore deliberately narrow: find
each VA heading, look for a YAML fence before the next heading, parse it
if present, else mark the VA retired.
"""

import re
import json
import argparse
from pathlib import Path

from season_resolve import (
    VALID_SEASONS,
    resolve_va_params,
    resolve_occupancy,
    validate_occupancy,
)


# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

# Matches the title line, capturing profile id and name, and dropping the
# fixed " — RAMP truth file (protocol-applied)" suffix if present.
RE_TITLE = re.compile(
    r"^#\s+Profile\s+(\d+)\s*:\s*(.+?)(?:\s+—\s+RAMP truth file.*)?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Matches a VA heading, e.g.:
#   ### VA1 — Morning indoor light (LED_1)
#   ### VA2 — Daytime indoor light (LED_1) ⚠ **structural placeholder, not a behavioural estimate**
#   ### VA6 — Outdoor daytime light (LED_2) — **retired, no parameters**
RE_VA_HEADER = re.compile(
    r"^###\s+VA(\d+)\s*—\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Matches any level-2 or level-3 heading (used as a stopping boundary when
# scanning for a VA's YAML fence).
RE_ANY_HEADING = re.compile(r"^#{2,3}\s+", re.MULTILINE)

# Matches a fenced YAML block: ```yaml ... ```
RE_YAML_FENCE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)

# Matches the profile-level occupancy block: ```yaml occupancy ... ```
# The [ \t]+ (rather than \s+) is deliberate: it cannot cross the newline, so
# this pattern and RE_YAML_FENCE above are mutually exclusive. A VA's bare
# ```yaml fence can never be read as an occupancy block, and an occupancy
# block can never be picked up as a VA's baseline or seasonal-override fence.
RE_OCCUPANCY_FENCE = re.compile(r"```yaml[ \t]+occupancy[ \t]*\n(.*?)\n```", re.DOTALL)

# Matches the population fenced block (plain, unlabeled fence) that follows
# the title/derivation-authority blockquote.
RE_POPULATION_FENCE = re.compile(r"```\n(Population:.*?)\n```", re.DOTALL)

RE_N_SURVEY = re.compile(r"N_survey\s*=\s*(\d+)")
RE_N_INTERVIEW = re.compile(r"N_interview\s*=\s*(\d+)")

# Matches numbered/unnumbered "## " section headings, capturing the text
# after any leading "N. " so sections can be looked up by name regardless
# of their number (numbers can legitimately differ across profiles if a
# section is ever added or removed for one profile).
RE_SECTION = re.compile(r"^##\s+(?:\d+\.\s+)?(.+?)\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Parsing functions
# ---------------------------------------------------------------------------

def _parse_title(text: str) -> tuple[int, str]:
    """Extract (profile_id, profile_name) from the title line."""
    m = RE_TITLE.search(text)
    if not m:
        return -1, "Unknown"
    return int(m.group(1)), m.group(2).strip()


def _parse_population(text: str) -> dict:
    """Extract the population fenced block, plus the two headline counts."""
    m = RE_POPULATION_FENCE.search(text)
    if not m:
        return {"raw": "", "n_survey": None, "n_interview": None}
    raw = m.group(1).strip()
    n_survey_m = RE_N_SURVEY.search(raw)
    n_interview_m = RE_N_INTERVIEW.search(raw)
    return {
        "raw": raw,
        "n_survey": int(n_survey_m.group(1)) if n_survey_m else None,
        "n_interview": int(n_interview_m.group(1)) if n_interview_m else None,
    }


def _parse_sections(text: str) -> dict:
    """
    Split the document into { section_name: section_text } by level-2
    headings, keyed by heading text with any leading "N. " stripped so
    lookups don't depend on a section's number. Internal only: the parsed
    profile dict does not include the full sections dict (it would be
    almost entirely narrative prose, tables, and quotes — not something
    Script 2 or any downstream RAMP code needs), just the one short
    "Demographic summary" field pulled from it for readability.
    """
    headings = list(RE_SECTION.finditer(text))
    sections = {}
    for i, m in enumerate(headings):
        name = m.group(1).strip()
        start = m.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def _load_yaml():
    """Import PyYAML on demand, with an actionable message if it's missing."""
    try:
        import yaml
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to parse VA blocks. Install with: "
            "pip install pyyaml --break-system-packages"
        ) from exc
    return yaml


def _parse_occupancy(text: str, source: str) -> dict | None:
    """
    Extract the profile-level ```yaml occupancy block, or None if the file
    has none (which means the occupancy mask is simply not modelled for that
    profile - see the module docstring).

    Two or more occupancy fences in one file is an authoring error and raises:
    occupancy is a single household-level axis, and silently letting the last
    fence win would make a stale, forgotten block override the intended one.
    """
    matches = list(RE_OCCUPANCY_FENCE.finditer(text))
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(
            f"{source}: found {len(matches)} '```yaml occupancy' blocks. A profile "
            f"has exactly one household-level occupancy declaration - merge them, "
            f"using 'seasonal_prob_home' for per-season values."
        )

    block = _load_yaml().safe_load(matches[0].group(1)) or {}
    # Validated at extraction time so an authoring error surfaces when the
    # markdown is edited, not hours into a simulation run. season_resolve
    # re-validates at simulation time, which also covers hand-edited JSON.
    return validate_occupancy(block, where=f"{source} occupancy block")


def _parse_virtual_appliances(text: str) -> list[dict]:
    """
    Find every VA heading, then look for fenced YAML blocks between that
    heading and the next heading (level 2 or 3).

    The FIRST YAML fence in a VA's block is its baseline parameters. If
    there is no YAML fence at all, the VA is retired (no parameters,
    `retired: true`).

    Any ADDITIONAL YAML fence in the same block is a seasonal override
    and MUST contain a `seasons` key: a list of one or more canonical
    season names (planting/growing/harvesting/free_grazing) this
    override applies to. Its other keys are merged on top of the
    baseline for those seasons only. A non-first fence missing `seasons`
    is an authoring error and raises immediately, rather than being
    silently treated as another baseline (which would just overwrite the
    real one with whatever came last).

    Resulting appliance dict shape:
        {index, name, retired, <baseline params...>,
         seasonal_overrides: {season_name: {overridden params...}, ...}}
    `seasonal_overrides` is only present if at least one override fence
    was found; profiles/VAs with no seasonal variation simply don't have
    the key, and resolve_va_params() in run_simulation.py already treats
    a missing key as "no override for this season".
    """
    va_headers = list(RE_VA_HEADER.finditer(text))
    all_headings = list(RE_ANY_HEADING.finditer(text))

    appliances = []
    for m in va_headers:
        index = int(m.group(1))
        name = m.group(2).strip()
        # Strip a trailing " — **retired, no parameters**" / "⚠ **...**"
        # annotation from the label for a clean display name; the actual
        # retired/active determination is made structurally below, from
        # whether a YAML fence is present — never from this text.
        name = re.sub(r"\s*(⚠.*|—\s*\*\*retired.*)$", "", name).strip()

        block_start = m.end()
        # Find the next heading (level 2 or 3) after this VA header; that's
        # the right edge of this VA's own block.
        next_heading_starts = [h.start() for h in all_headings if h.start() > m.start()]
        block_end = min(next_heading_starts) if next_heading_starts else len(text)
        block_text = text[block_start:block_end]

        yaml_matches = list(RE_YAML_FENCE.finditer(block_text))

        appliance = {
            "index": index,
            "name": name,
            "retired": len(yaml_matches) == 0,
        }

        if not yaml_matches:
            appliances.append(appliance)
            continue

        yaml = _load_yaml()  # local import: only needed if a YAML fence exists

        baseline = yaml.safe_load(yaml_matches[0].group(1)) or {}
        appliance.update(baseline)

        seasonal_overrides: dict = {}
        for extra_fence in yaml_matches[1:]:
            override = yaml.safe_load(extra_fence.group(1)) or {}
            seasons = override.pop("seasons", None)
            if not seasons:
                raise ValueError(
                    f"VA{index} ('{name}') has a second YAML fence with no "
                    f"'seasons' key. Every non-baseline YAML block in a VA "
                    f"must declare which season(s) it applies to, e.g. "
                    f"'seasons: [growing, free_grazing]'. Fence contents: {override}"
                )
            unknown = set(seasons) - VALID_SEASONS
            if unknown:
                raise ValueError(
                    f"VA{index} ('{name}') declares unknown season(s) {sorted(unknown)}. "
                    f"Valid seasons: {sorted(VALID_SEASONS)}"
                )
            for season in seasons:
                seasonal_overrides.setdefault(season, {}).update(override)

        if seasonal_overrides:
            appliance["seasonal_overrides"] = seasonal_overrides

        appliances.append(appliance)

    return sorted(appliances, key=lambda a: a["index"])


def parse_profile(md_path: Path) -> dict:
    """Parse a single profile markdown file. Returns a dict ready for JSON."""
    text = md_path.read_text(encoding="utf-8")

    profile_id, profile_name = _parse_title(text)
    population = _parse_population(text)
    sections = _parse_sections(text)  # used only to pull the one short field below
    appliances = _parse_virtual_appliances(text)
    occupancy = _parse_occupancy(text, md_path.name)

    n_active = sum(1 for a in appliances if not a["retired"])
    n_retired = sum(1 for a in appliances if a["retired"])

    profile = {
        "profile_id": profile_id,
        "profile_name": profile_name,
        "source_file": md_path.name,
        "population": population,
        "description": sections.get("Demographic summary", ""),
        "appliances": appliances,
        "appliance_counts": {"active": n_active, "retired": n_retired, "total": len(appliances)},
    }

    # Only emitted when the markdown actually declares one, so a profile
    # without the block keeps exactly its pre-feature JSON shape.
    if occupancy is not None:
        profile["occupancy"] = occupancy

    return profile


def apply_season(profile: dict, season: str) -> dict:
    """
    Return a copy of a parsed profile with every active VA's parameters
    resolved (flattened) for `season`, via the same resolve_va_params
    used by run_simulation.py. Retired VAs are left untouched.
    `seasonal_overrides` is dropped from each VA in the output, since
    it's now baked into the resolved values - the output represents
    exactly what would be simulated for that one season, nothing more.

    The profile-level occupancy block is flattened the same way: the
    season's effective `prob_home` replaces the baseline and
    `seasonal_prob_home` is dropped, so the block also describes exactly
    that one season.
    """
    resolved_profile = dict(profile)
    resolved_appliances = []
    for va in profile["appliances"]:
        if va.get("retired"):
            resolved_appliances.append(va)
            continue
        resolved_appliances.append(resolve_va_params(va, season))
    resolved_profile["appliances"] = resolved_appliances

    if "occupancy" in profile:
        resolved_profile["occupancy"] = resolve_occupancy(profile, season)

    resolved_profile["season"] = season
    return resolved_profile


def parse_all_profiles(profiles_dir: Path) -> dict:
    """Parse every *.md file in profiles_dir and return a combined structure."""
    md_files = sorted(profiles_dir.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in {profiles_dir}")

    profiles = {}
    for md_file in md_files:
        print(f"  Parsing: {md_file.name}")
        profile = parse_profile(md_file)
        pid = str(profile["profile_id"])

        if profile["profile_id"] == -1:
            raise ValueError(
                f"Could not parse a profile id/name from the title line of "
                f"{md_file.name}. Expected a line matching "
                f"'# Profile <N>: <Name> — RAMP truth file (protocol-applied)'. "
                f"Check that file's title heading against that pattern."
            )
        if pid in profiles:
            raise ValueError(
                f"Profile id {pid} appears in both {profiles[pid]['source_file']} "
                f"and {md_file.name} — each file must have a unique 'Profile <N>' "
                f"in its title line."
            )
        profiles[pid] = profile

    return {
        "profiles": profiles,
        "metadata": {
            "location": "Raqaypampa, Bolivia",
            "battery_capacity_wh": 89,
            "appliance_inventory": ["LED_1 (indoor)", "LED_2 (indoor or outdoor, profile-dependent)", "USB (charging)"],
        },
    }


def save_parameters(combined: dict, output_dir: Path, season: str | None = None) -> None:
    """Write one JSON per profile and one combined JSON.

    If `season` is given, output filenames get a '_<season>' suffix so a
    season-filtered run never collides with (or is mistaken for) the
    default full-year extraction.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{season}" if season else ""

    for pid, profile in combined["profiles"].items():
        filepath = output_dir / f"profile_{pid}_params{suffix}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {filepath}")

    combined_path = output_dir / f"all_profiles_params{suffix}.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {combined_path}")


def _format_occupancy(profile: dict) -> str:
    """
    One-line description of a profile's occupancy setting for the summary.

    Distinguishes the three states that matter when reading a run log: no
    block authored at all, a block that explicitly disables the mask, and a
    block that enables it (with the per-season values spelled out, since those
    are the numbers that change the simulation).
    """
    block = profile.get("occupancy")
    if block is None:
        return "no block in markdown - mask OFF"

    basis = block.get("occasional_use_basis")
    baseline = block.get("prob_home")
    seasonal = block.get("seasonal_prob_home") or {}

    if baseline is None and not any(v is not None for v in seasonal.values()):
        return "prob_home=null - mask OFF (declared explicitly)"

    parts = [f"prob_home={baseline}"]
    if seasonal:
        parts.append(
            "seasonal={" + ", ".join(
                f"{s}={seasonal[s]}" for s in sorted(seasonal)
            ) + "}"
        )
    parts.append(f"occasional_use_basis={basis}")
    return "mask ON  " + "  ".join(parts)


def print_extraction_summary(combined: dict) -> None:
    """Print a human-readable summary of what was extracted."""
    print("\n" + "=" * 60)
    print("Extraction summary")
    print("=" * 60)
    for pid, profile in combined["profiles"].items():
        vas = profile["appliances"]
        counts = profile["appliance_counts"]
        print(f"\nProfile {pid}: {profile['profile_name']}")
        print(f"  Source file : {profile['source_file']}")
        print(f"  Population  : N_survey={profile['population']['n_survey']}  "
              f"N_interview={profile['population']['n_interview']}")
        print(f"  Appliances  : {counts['active']} active, {counts['retired']} retired "
              f"({counts['total']} total slots)")
        print(f"  Occupancy   : {_format_occupancy(profile)}")
        for va in vas:
            if va["retired"]:
                print(f"    VA{va['index']:>2}: {va['name'][:45]:<45}  RETIRED (no parameters)")
            else:
                override_note = ""
                if "seasonal_overrides" in va:
                    override_note = f"  [seasonal overrides: {sorted(va['seasonal_overrides'])}]"
                elif "season" in profile:
                    override_note = "  [resolved for this season]"
                print(
                    f"    VA{va['index']:>2}: {va['name'][:45]:<45}"
                    f"  {va.get('power')}W  occ={va.get('occasional_use')}"
                    f"{override_note}"
                )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Parse Raqaypampa profile markdowns into RAMP parameter JSON files."
    )
    parser.add_argument(
        "--profiles_dir", default=".",
        help="Directory containing the profile *.md files (default: current directory)"
    )
    parser.add_argument(
        "--output_dir", default="parameters",
        help="Directory to write JSON parameter files (default: ./parameters)"
    )
    parser.add_argument(
        "--season", default=None, choices=sorted(VALID_SEASONS),
        help="If given, resolve every VA's seasonal overrides for this one season and "
             "write flattened (baseline+override-applied) JSON instead of the full "
             "baseline+seasonal_overrides structure. Output filenames get a "
             "'_<season>' suffix so they don't collide with a full extraction run. "
             "Omit this flag to get the full year-round structure (the default, and "
             "what run_simulation.py's full-year mode consumes)."
    )
    args = parser.parse_args()

    profiles_dir = Path(args.profiles_dir)
    output_dir = Path(args.output_dir)

    print(f"Reading profiles from : {profiles_dir.resolve()}")
    print(f"Writing parameters to : {output_dir.resolve()}")
    if args.season:
        print(f"Season filter          : {args.season}")
    print()

    combined = parse_all_profiles(profiles_dir)

    if args.season:
        for pid, profile in combined["profiles"].items():
            combined["profiles"][pid] = apply_season(profile, args.season)

    print_extraction_summary(combined)

    print()
    save_parameters(combined, output_dir, season=args.season)
    print("\nDone.")


if __name__ == "__main__":
    main()