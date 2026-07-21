#!/usr/bin/env python3
"""
ebp_classification.py — EBP (Energy Behavior Profile) stratification

Classifies households into one of four structural profiles using five
survey-derived fields: family_type, occupation, children_in_school,
migration, portability_shs. Companion document: EBP_CLASSIFICATION_PROTOCOL.md
in this repository, which explains the rule logic, the missing-data
handling strategy, and how to adapt this script to a different dataset or
profile scheme.

Usage:
    python ebp_classification.py --input data_1.csv --output classifications.csv
    python ebp_classification.py --input data_1.csv --output classifications.csv \
        --previous previous_classifications.csv --audit-log audit_log.csv

Design principles (see protocol doc for full rationale):
  1. Classification uses ONLY structural/survey fields — never qualitative
     data — so it is a fixed, auditable rule applied identically to every
     household. Qualitative data (interviews, memos) is used separately,
     downstream, to validate the classification (see the companion
     concordance-check script) or to correct a specific miscoded field at
     its source — never to relabel a household directly.
  2. Missing values (-1) are never silently coerced by a boolean
     comparison. A household with missing field(s) is classified with
     confidence ONLY if every plausible value of the missing field(s)
     yields the same profile; otherwise it is left explicitly
     "Unclassified — Insufficient Data" with the ambiguity logged.
"""

import argparse
import itertools
import sys
from pathlib import Path

import pandas as pd

# =============================================================================
# CONFIGURATION — edit this section to adapt the script to a new dataset
# =============================================================================

# Coded value domains, per the codebook. Used both to validate input and to
# enumerate plausible values when a field is missing. Adjust to match your
# own codebook if variable names/codes differ.
FIELD_DOMAINS = {
    "family_type": list(range(1, 11)),  # 1..10, see FAMILY_TYPE_LABELS below
    "occupation": [1, 2, 3, 4],
    "children_in_school": [0, 1],
    "migration": [0, 1],
    "portability_shs": [0, 1],
}
CORE_FIELDS = list(FIELD_DOMAINS.keys())
MISSING_CODE = -1

FAMILY_TYPE_LABELS = {
    1: "Unipersonal", 2: "Monoparental", 3: "Monoparental numeroso",
    4: "Pareja nuclear", 5: "Nuclear completo", 6: "Nuclear completo numeroso",
    7: "Extendido", 8: "Extendido sin hijos", 9: "Extendido numeroso",
    10: "Extendido numeroso sin hijos", MISSING_CODE: "Missing",
}
OCCUPATION_LABELS = {1: "Domestic labour", 2: "Agriculture", 3: "Student",
                      4: "Mining", MISSING_CODE: "Missing"}
YES_NO_LABELS = {0: "No", 1: "Yes", MISSING_CODE: "Missing"}

PROFILE_1 = "Profile 1: Educational/Agricultural Core"
PROFILE_2 = "Profile 2: Isolated Elderly"
PROFILE_3 = "Profile 3: Extended Hub"
PROFILE_4 = "Profile 4: System Breakers"
UNCLASSIFIED = "Unclassified — Insufficient Data"

# Occupation codes that unconditionally force Profile 4, regardless of
# family structure (System Breaker occupations: Student, Mining).
BREAKER_OCCUPATIONS = (3, 4)


# =============================================================================
# CLASSIFICATION RULE — the stratification logic itself
# =============================================================================

def classify_one(family_type, occupation, children_in_school, migration,
                  portability_shs):
    """Classify a single household from five concrete (non-missing) field
    values. See EBP_CLASSIFICATION_PROTOCOL.md for the plain-language
    decision tree this implements."""
    is_breaker = occupation in BREAKER_OCCUPATIONS

    # Profile 2 — Isolated Elderly / Couples: single-person or childless-
    # couple households, unless the occupation is itself a breaker.
    cond2 = family_type in (1, 4) and not is_breaker

    # Profile 1 — Educational/Agricultural Core, two paths to qualify:
    #   (a) a nuclear-shaped family with children in school, or
    #   (b) an extended-shaped family with children in school AND
    #       "stable" (doesn't migrate, keeps the SHS at home)
    prof1_nuclear = family_type in (2, 3, 5, 6) and children_in_school == 1
    prof1_extended_stable = (
        family_type in (7, 8, 9, 10)
        and children_in_school == 1
        and migration != 1
        and portability_shs == 1
    )
    cond1 = (prof1_nuclear or prof1_extended_stable) and not is_breaker

    # Profile 3 — Extended Hub: numerous/extended families that didn't
    # qualify for Profile 1 (e.g. extended but unstable, or no children
    # in school), and aren't a breaker occupation.
    cond3 = family_type in (3, 6, 7, 8, 9, 10) and not cond1 and not is_breaker

    # Profile 4 — System Breakers: everyone else, including every breaker
    # occupation regardless of family structure.
    cond4 = not (cond1 or cond2 or cond3)

    if cond1:
        return PROFILE_1
    if cond2:
        return PROFILE_2
    if cond3:
        return PROFILE_3
    assert cond4
    return PROFILE_4


def classify_row_with_sensitivity(row):
    """Classify one household, handling missing (-1) fields by checking
    whether the missing value(s) actually change the outcome.

    Returns a dict with: ebp_profile, missing_fields (list),
    outcome_ambiguous (bool), possible_profiles (set).
    """
    values = {f: row[f] for f in CORE_FIELDS}
    missing = [f for f in CORE_FIELDS if values[f] == MISSING_CODE]

    if not missing:
        profile = classify_one(**values)
        return {"ebp_profile": profile, "missing_fields": [],
                "outcome_ambiguous": False, "possible_profiles": {profile}}

    # Brute-force every plausible value for each missing field, holding
    # known fields fixed, and see whether the outcome ever changes.
    trial_domains = [FIELD_DOMAINS[f] for f in missing]
    outcomes = set()
    for combo in itertools.product(*trial_domains):
        trial_values = {**values, **dict(zip(missing, combo))}
        outcomes.add(classify_one(**trial_values))

    if len(outcomes) == 1:
        return {"ebp_profile": outcomes.pop(), "missing_fields": missing,
                "outcome_ambiguous": False, "possible_profiles": outcomes}
    return {"ebp_profile": UNCLASSIFIED, "missing_fields": missing,
            "outcome_ambiguous": True, "possible_profiles": outcomes}


# =============================================================================
# PIPELINE
# =============================================================================

def validate_input(df: pd.DataFrame) -> None:
    missing_cols = [f for f in CORE_FIELDS if f not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Input file is missing required column(s): {missing_cols}. "
            f"Required: {CORE_FIELDS}"
        )
    for field, domain in FIELD_DOMAINS.items():
        valid = set(domain) | {MISSING_CODE}
        bad_values = set(df[field].unique()) - valid
        if bad_values:
            raise ValueError(
                f"Column '{field}' contains value(s) outside its coded "
                f"domain {sorted(valid)}: {sorted(bad_values)}. Check for "
                f"a codebook mismatch before proceeding."
            )


def classify_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["family_type_label"] = df["family_type"].map(FAMILY_TYPE_LABELS)
    out["occupation_label"] = df["occupation"].map(OCCUPATION_LABELS)
    out["children_in_school_label"] = df["children_in_school"].map(YES_NO_LABELS)
    out["migration_label"] = df["migration"].map(YES_NO_LABELS)
    out["portability_shs_label"] = df["portability_shs"].map(YES_NO_LABELS)

    results = df.apply(classify_row_with_sensitivity, axis=1, result_type="expand")
    out["ebp_profile"] = results["ebp_profile"]
    out["missing_fields"] = results["missing_fields"].apply(
        lambda x: ",".join(x) if x else "")
    out["outcome_ambiguous_due_to_missing_data"] = results["outcome_ambiguous"]
    out["possible_profiles_if_ambiguous"] = results["possible_profiles"].apply(
        lambda s: " | ".join(sorted(s)) if len(s) > 1 else "")
    return out


def print_summary(out: pd.DataFrame) -> None:
    unclassified_count = (out["ebp_profile"] == UNCLASSIFIED).sum()
    resolved_despite_missing = ((out["missing_fields"] != "")
                                 & ~out["outcome_ambiguous_due_to_missing_data"]).sum()
    print("\n" + "=" * 50)
    print("EBP CLASSIFICATION RESULTS")
    print("=" * 50)
    print(out["ebp_profile"].value_counts().to_string())
    if unclassified_count:
        print(f"\n⚠️  {unclassified_count} household(s) left Unclassified — "
              f"the missing field(s) change the outcome depending on their "
              f"true value. See the sensitivity log.")
    if resolved_despite_missing:
        print(f"✅ {resolved_despite_missing} household(s) had missing "
              f"field(s) but were classified anyway — every plausible "
              f"value led to the same profile.")
    print("=" * 50 + "\n")


def write_outputs(out: pd.DataFrame, output_path: Path,
                   sensitivity_log_path: Path | None,
                   previous_path: Path | None, audit_log_path: Path | None) -> None:
    export_cols = ["id", "name", "family_type_label", "occupation_label",
                    "children_in_school_label", "migration_label",
                    "portability_shs_label", "ebp_profile"]
    export_cols = [c for c in export_cols if c in out.columns]
    out[export_cols].to_csv(output_path, index=False)
    print(f"📄 Classification saved to: {output_path}")

    if sensitivity_log_path is not None:
        sens_cols = export_cols + ["missing_fields",
                                    "outcome_ambiguous_due_to_missing_data",
                                    "possible_profiles_if_ambiguous"]
        sens_cols = [c for c in sens_cols if c in out.columns]
        sens = out.loc[out["missing_fields"] != "", sens_cols]
        sens.to_csv(sensitivity_log_path, index=False)
        print(f"📄 Missing-data sensitivity log ({len(sens)} household(s)) "
              f"saved to: {sensitivity_log_path}")

    if previous_path is not None and audit_log_path is not None:
        if not previous_path.exists():
            print(f"(Previous classification file not found at "
                  f"{previous_path} — skipping audit diff.)")
            return
        previous = pd.read_csv(previous_path)[["id", "ebp_profile"]].rename(
            columns={"ebp_profile": "previous_profile"})
        audit = out[["id", "name", "family_type_label", "ebp_profile"]].rename(
            columns={"ebp_profile": "new_profile"})
        audit = audit.merge(previous, on="id", how="left")
        audit["changed"] = audit["previous_profile"] != audit["new_profile"]
        changed = audit.loc[audit["changed"]]
        changed.to_csv(audit_log_path, index=False)
        print(f"📄 Audit log of {len(changed)} changed household(s) saved "
              f"to: {audit_log_path}")
        if len(changed):
            print(changed[["id", "name", "family_type_label",
                            "previous_profile", "new_profile"]].to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, type=Path,
                         help="CSV with columns: id, name, family_type, "
                              "occupation, children_in_school, migration, "
                              "portability_shs")
    parser.add_argument("--output", required=True, type=Path,
                         help="Where to write the classified household list")
    parser.add_argument("--sensitivity-log", type=Path, default=None,
                         help="Optional: where to log households whose "
                              "missing fields were resolved or left ambiguous")
    parser.add_argument("--previous", type=Path, default=None,
                         help="Optional: a prior classification CSV to diff against")
    parser.add_argument("--audit-log", type=Path, default=None,
                         help="Optional: where to write the diff against --previous "
                              "(requires --previous)")
    args = parser.parse_args()

    if args.previous and not args.audit_log:
        args.audit_log = args.output.with_name(args.output.stem + "_audit_log.csv")
    if args.sensitivity_log is None:
        args.sensitivity_log = args.output.with_name(
            args.output.stem + "_sensitivity_log.csv")

    df = pd.read_csv(args.input)
    try:
        validate_input(df)
    except ValueError as e:
        print(f"❌ Input validation failed: {e}", file=sys.stderr)
        sys.exit(1)

    out = classify_dataframe(df)
    print_summary(out)
    write_outputs(out, args.output, args.sensitivity_log, args.previous, args.audit_log)


if __name__ == "__main__":
    main()