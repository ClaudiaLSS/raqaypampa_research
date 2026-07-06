"""
extract_parameters.py
=====================
Parses Raqaypampa profile markdown files and writes one JSON parameter
file per profile (plus a combined file) that Script 2 uses to build the
RAMP model.

This script is the single source of truth adapter: edit the markdowns,
re-run this script, and the simulation picks up the changes automatically.
It works with any number of profile markdowns that follow the same
document convention — drop a new file in PROFILES_DIR and it will be
included in the next extraction run.

Usage
-----
    python extract_parameters.py
    python extract_parameters.py --profile_id 1
    python extract_parameters.py --profile_id 1 --single_profile_output
    python extract_parameters.py --profiles_dir path/to/markdowns --output_dir path/to/params

Markdown conventions assumed
-----------------------------
Profile title line:
    # **Profile <N>: <Name>**

Virtual Appliance blocks:
    ### **Virtual Appliance <N>: <label>**
    - **power:** <float> W ...
    - **w_1:** [<int>, <int>] ...
    - **w_2:** [<int>, <int>] ...        (optional)
    - **func_time:** <int> minutes ...
    - **func_cycle:** <int> minutes ...
    - **occasional_use:** <float> ...

Seasonality section (at end of file):
    Parameters that change during the <Season(s)> season(s):
    - Virtual Appliance <N>: <label>
        - <param>: <value> ...

The parser is intentionally lenient on surrounding prose: it uses
targeted regexes on field lines rather than a rigid section parser,
so minor markdown edits (rewording narratives, adding bullets) will
not break it.
"""

import re
import json
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Season calendar
# ---------------------------------------------------------------------------

SEASON_MONTHS = {
    "planting":    [10, 11, 12, 1],   # Oct–Jan  (baseline for most profiles)
    "growing":     [2, 3, 4],         # Feb–Apr
    "harvesting":  [5, 6],            # May–Jun  (baseline for most profiles)
    "free_grazing":[7, 8, 9],         # Jul–Sep
}

# Inverse: month -> season name
MONTH_TO_SEASON = {m: s for s, months in SEASON_MONTHS.items() for m in months}

# Human-readable phrases that appear in the markdown -> canonical season keys
# The parser looks for these substrings (case-insensitive) in the
# "Parameters that change during …" heading line.
SEASON_PHRASE_MAP = {
    "planting":     "planting",
    "growing":      "growing",
    "early harvest":"growing",        # "Growing & Early Harvest" -> growing
    "harvesting":   "harvesting",
    "free grazing": "free_grazing",
    "grazing":      "free_grazing",
    "migration":    "free_grazing",
}

# Parameters that are floats vs ints
FLOAT_PARAMS  = {"occasional_use", "power", "thermal_p_var"}
INT_PARAMS    = {"func_time", "func_cycle"}


# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

# Matches:  ### **Virtual Appliance 3: Indoor evening light**
RE_VA_HEADER = re.compile(
    r"###\s+\**Virtual Appliance\s+(\d+)\s*:\s*(.+?)\**\s*$",
    re.IGNORECASE,
)

# Matches field lines inside a VA block, e.g.:
#   - **power:** 3 W (nominal power)
#   - **w_1:** [300, 420] (05:00 – 08:00)
#   - **occasional_use:** 0.42 (Casual/Seasonal …)
RE_FIELD = re.compile(
    r"-\s+\**(\w+)\**\s*:\s*(.+)",
    re.IGNORECASE,
)

# Matches a time window like [300, 420]
RE_WINDOW = re.compile(r"\[(\d+),\s*(\d+)\]")

# Matches the first number in a string (for power / func_time / etc.)
RE_FIRST_NUMBER = re.compile(r"(\d+(?:\.\d+)?)")

# Detects the start of the seasonality section
RE_SEASON_SECTION = re.compile(
    r"(parameters\s+that\s+change\s+during)",
    re.IGNORECASE,
)

# Detects a VA reference line inside the seasonality section, e.g.:
#   - Virtual Appliance 3: Indoor evening light
RE_SEASON_VA_REF = re.compile(
    r"-\s+\**Virtual Appliance\s+(\d+)\s*:",
    re.IGNORECASE,
)

# Detects a parameter override line, e.g.:
#     - occasional_use: 0.71
#     - func_time: 300 minutes
RE_SEASON_PARAM = re.compile(
    r"^\s+-\s+\**(\w+)\**\s*:\s*(.+)",
)


# ---------------------------------------------------------------------------
# Parsing functions
# ---------------------------------------------------------------------------

def _parse_value(param_name: str, raw: str):
    """Return a correctly typed value for a RAMP parameter field."""
    m = RE_FIRST_NUMBER.search(raw)
    if not m:
        return None
    if param_name in FLOAT_PARAMS:
        return float(m.group(1))
    if param_name in INT_PARAMS:
        return int(float(m.group(1)))
    return float(m.group(1))


def _parse_windows(lines_in_block: list[str]) -> list[list[int]]:
    """Collect w_1 and w_2 window values from the raw lines of a VA block."""
    windows = []
    for line in lines_in_block:
        m = RE_FIELD.search(line)
        if not m:
            continue
        key = m.group(1).lower()
        if key in ("w_1", "w_2", "w1", "w2"):
            wm = RE_WINDOW.search(m.group(2))
            if wm:
                windows.append([int(wm.group(1)), int(wm.group(2))])
    return windows


def _parse_profile_header(text: str) -> tuple[int, str]:
    """Extract (profile_id, profile_name) from the first heading line."""
    m = re.search(
        r"#\s+\**Profile\s+(\d+)\s*:\s*(.+?)\**\s*$",
        text, re.MULTILINE | re.IGNORECASE,
    )
    if not m:
        return -1, "Unknown"
    return int(m.group(1)), m.group(2).strip()


def _parse_demographic_summary(text: str) -> str:
    """Extract the demographic summary paragraph."""
    m = re.search(
        r"\*\*Demographic summary:\*\*\s*(.+?)(?=\n##|\n###)",
        text, re.DOTALL | re.IGNORECASE,
    )
    return m.group(1).strip() if m else ""


def _parse_virtual_appliances(text: str) -> list[dict]:
    """
    Parse all Virtual Appliance blocks from the markdown body.
    Returns a list of dicts ordered by VA index.
    """
    lines = text.splitlines()
    appliances = []
    current_va = None
    current_block_lines = []

    def _finalise(va, block_lines):
        """Close out the current VA block and append to appliances."""
        if va is None:
            return
        va["windows"] = _parse_windows(block_lines)
        for line in block_lines:
            m = RE_FIELD.search(line)
            if not m:
                continue
            key = m.group(1).lower()
            val_str = m.group(2)
            if key in FLOAT_PARAMS | INT_PARAMS:
                va[key] = _parse_value(key, val_str)
        appliances.append(va)

    for line in lines:
        m = RE_VA_HEADER.match(line.strip())
        if m:
            _finalise(current_va, current_block_lines)
            current_va = {
                "index": int(m.group(1)),
                "name": m.group(2).strip().strip("*").strip(),
                "power": None,
                "thermal_p_var": None,
                "windows": [],
                "func_time": None,
                "func_cycle": None,
                "occasional_use": None,
                "seasonal_overrides": {},
            }
            current_block_lines = []
        elif current_va is not None:
            # Stop collecting block lines when we hit the Seasonality section
            if RE_SEASON_SECTION.search(line):
                _finalise(current_va, current_block_lines)
                current_va = None
                current_block_lines = []
            else:
                current_block_lines.append(line)

    _finalise(current_va, current_block_lines)
    return sorted(appliances, key=lambda a: a["index"])


def _detect_seasons_in_heading(heading_line: str) -> list[str]:
    """
    Given a line like:
        'Parameters that change during the Growing and Grazing season:'
    Return the list of matching canonical season keys.
    """
    lower = heading_line.lower()
    found = []
    for phrase, season_key in SEASON_PHRASE_MAP.items():
        if phrase in lower and season_key not in found:
            found.append(season_key)
    return found


def _parse_seasonality(text: str, appliances: list[dict]) -> None:
    """
    Scan the seasonality section of the markdown and attach
    seasonal_overrides to the matching appliance dicts (mutates in place).
    """
    # Build a quick lookup: va_index -> appliance dict
    va_by_index = {a["index"]: a for a in appliances}

    lines = text.splitlines()

    in_season_section = False
    active_seasons: list[str] = []
    active_va_index: int | None = None

    for line in lines:
        # Detect entry into seasonality section
        if RE_SEASON_SECTION.search(line):
            in_season_section = True
            active_seasons = _detect_seasons_in_heading(line)
            active_va_index = None
            continue

        if not in_season_section:
            continue

        # A new "Parameters that change during …" sub-heading resets the context
        if RE_SEASON_SECTION.search(line):
            active_seasons = _detect_seasons_in_heading(line)
            active_va_index = None
            continue

        # VA reference line
        m_va = RE_SEASON_VA_REF.match(line)
        if m_va:
            active_va_index = int(m_va.group(1))
            continue

        # Parameter override line (indented bullet)
        if active_va_index is not None and active_seasons:
            m_p = RE_SEASON_PARAM.match(line)
            if m_p:
                param = m_p.group(1).lower()
                val_str = m_p.group(2)
                if param in FLOAT_PARAMS | INT_PARAMS:
                    value = _parse_value(param, val_str)
                    if value is not None and active_va_index in va_by_index:
                        for season in active_seasons:
                            overrides = va_by_index[active_va_index]["seasonal_overrides"]
                            if season not in overrides:
                                overrides[season] = {}
                            overrides[season][param] = value


def parse_profile(md_path: Path) -> dict:
    """
    Parse a single profile markdown file.
    Returns a dict ready to be serialised to JSON.
    """
    text = md_path.read_text(encoding="utf-8")

    profile_id, profile_name = _parse_profile_header(text)
    description = _parse_demographic_summary(text)
    appliances = _parse_virtual_appliances(text)
    _parse_seasonality(text, appliances)

    return {
        "profile_id":   profile_id,
        "profile_name": profile_name,
        "source_file":  md_path.name,
        "description":  description,
        "appliances":   appliances,
    }


def parse_all_profiles(profiles_dir: Path) -> dict:
    """
    Parse every *.md file in profiles_dir and return a combined structure.
    Files are sorted by filename so the order is deterministic.
    """
    md_files = sorted(profiles_dir.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in {profiles_dir}")

    profiles = {}
    for md_file in md_files:
        print(f"  Parsing: {md_file.name}")
        profile = parse_profile(md_file)
        pid = str(profile["profile_id"])
        profiles[pid] = profile

    return {
        "profiles":      profiles,
        "season_months": SEASON_MONTHS,
        "month_to_season": {str(k): v for k, v in MONTH_TO_SEASON.items()},
        "metadata": {
            "location":            "Raqaypampa, Bolivia",
            "battery_capacity_wh": 89,
            "appliance_inventory": ["LED_1 (indoor)", "LED_2 (outdoor)", "USB (charging)"],
            "baseline_seasons":    ["planting", "harvesting"],
        },
    }


def filter_profiles(combined: dict, profile_id: int | None) -> dict:
    """Return a copy of combined with only the requested profile, if set."""
    if profile_id is None:
        return combined

    pid = str(profile_id)
    if pid not in combined["profiles"]:
        available = ", ".join(sorted(combined["profiles"].keys()))
        raise KeyError(f"Profile {pid} not found. Available profiles: {available}")

    filtered = dict(combined)
    filtered["profiles"] = {pid: combined["profiles"][pid]}
    return filtered


def save_parameters(combined: dict, output_dir: Path, save_combined: bool = True) -> None:
    """Write one JSON per profile and optionally one combined JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for pid, profile in combined["profiles"].items():
        filepath = output_dir / f"profile_{pid}_params.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {filepath}")

    if save_combined:
        combined_path = output_dir / "all_profiles_params.json"
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {combined_path}")


def print_extraction_summary(combined: dict) -> None:
    """Print a human-readable summary of what was extracted."""
    print("\n" + "=" * 60)
    print("Extraction summary")
    print("=" * 60)
    for pid, profile in combined["profiles"].items():
        vas = profile["appliances"]
        print(f"\nProfile {pid}: {profile['profile_name']}")
        print(f"  Source file : {profile['source_file']}")
        print(f"  Appliances  : {len(vas)}")
        for va in vas:
            overrides_info = ""
            if va["seasonal_overrides"]:
                seasons = ", ".join(sorted(va["seasonal_overrides"]))
                overrides_info = f"  [overrides in: {seasons}]"
            print(
                f"    VA{va['index']:>2}: {va['name'][:45]:<45}"
                f"  {va['power']}W  occ={va['occasional_use']}"
                f"{overrides_info}"
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
        "--profile_id", type=int, default=None,
        help="Optional profile ID to extract (default: all profiles)"
    )
    parser.add_argument(
        "--single_profile_output", action="store_true",
        help="When extracting one profile, skip writing all_profiles_params.json"
    )
    args = parser.parse_args()

    profiles_dir = Path(args.profiles_dir)
    output_dir   = Path(args.output_dir)

    print(f"Reading profiles from : {profiles_dir.resolve()}")
    print(f"Writing parameters to : {output_dir.resolve()}")
    print()

    combined = parse_all_profiles(profiles_dir)
    combined = filter_profiles(combined, args.profile_id)
    print_extraction_summary(combined)

    print()
    save_parameters(combined, output_dir, save_combined=not args.single_profile_output)
    print("\nDone.")


if __name__ == "__main__":
    main()