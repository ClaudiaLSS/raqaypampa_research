#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
socioeconomic_profile.py

Loads socioeconomic survey data and codebook, maps categorical codes to labels,
and generates summary statistics only for variables in the 'socioeconomic' dimension.

Usage:
    Run in your terminal or IDE (e.g., Spyder):
    $ python socioeconomic_profile.py
"""

import pandas as pd
import os
import csv
import numpy as np
from scipy.stats import chi2_contingency

# === Paths (adjust to your project structure) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/surveys/data_benin_2.csv")
CODEBOOK_PATH = os.path.join(BASE_DIR, "../data/surveys/codebook_hh_benin.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "../results/impact")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_NUMERICAL = os.path.join(OUTPUT_DIR, "numerical_summary_benin.csv")
OUTPUT_CATEGORICAL = os.path.join(OUTPUT_DIR, "categorical_summary_benin.csv")

# === Load data ===
df = pd.read_csv(DATA_PATH, na_values=["-1"], encoding="latin1")
codebook = pd.read_csv(CODEBOOK_PATH, encoding="latin1")

# Clean headers
codebook.columns = codebook.columns.str.strip()
codebook["variable"] = codebook["variable"].astype(str).str.strip()
codebook["type"] = codebook["type"].astype(str).str.strip()
codebook["code"] = codebook["code"].astype(str).fillna("")
codebook["dimension"] = codebook["dimension"].astype(str).str.strip().str.lower()

# === Helper function ===
def parse_code_column(code_str):
    """Parses code string like '1 = Female; 2 = Male' into a dict."""
    if pd.isna(code_str):
        return None
    items = [item.strip() for item in code_str.split(";")]
    mapping = {}
    for item in items:
        if "=" in item:
            k, v = item.split("=")
            mapping[int(k.strip())] = v.strip()
    return mapping

# === Apply categorical labels ===
labeled_df = df.copy()

dimensions_to_include = ['impact']
selected_codebook = codebook[codebook["dimension"].isin(dimensions_to_include)]

for _, row in selected_codebook.iterrows():
    var = row["variable"]
    var_type = row["type"]
    codes = row["code"]

    if var not in df.columns:
        print(f"⚠️ Skipping missing variable (not in dataset): {var}")
        continue

    if var_type.lower() == "categorical" and isinstance(codes, str):
        mapping = parse_code_column(codes)
        if mapping:
            new_col = var + "_label"
            labeled_df[new_col] = df[var].map(mapping)

# === Generate summary ===
numerical_summary = []
categorical_summary = []

for _, row in selected_codebook.iterrows():
    var = row["variable"]
    var_type = row["type"]
    description = row.get("description", "")

    if var not in df.columns:
        print(f"⚠️ Skipping missing variable (not in dataset): {var}")
        continue

    if var_type.lower() == "numerical":
        stats = df[var].describe()
        numerical_summary.append({
            "variable": var,
            "description": description,
            "type": "Numerical",
            "mean": stats["mean"],
            "std": stats["std"],
            "min": stats["min"],
            "25%": stats["25%"],
            "50% (median)": stats["50%"],
            "75%": stats["75%"],
            "max": stats["max"],
            "missing": df[var].isna().sum()
        })

    elif var_type.lower() == "categorical":
        label_col = var + "_label"
        if label_col not in labeled_df.columns:
            print(f"⚠️ No labels found for categorical variable: {var}")
            continue

        # Frequency analysis
        counts = labeled_df[label_col].value_counts(dropna=False)
        total = counts.sum()
        freq_table = []
        for k, v in counts.items():
            label = str(k) if pd.notna(k) else "Missing"
            percentage = (v / total) * 100
            freq_table.append(f"{label}: {v} ({percentage:.1f}%)")

        freq_str = "; ".join(freq_table)

        categorical_summary.append({
            "variable": var,
            "description": description,
            "type": "Categorical",
            "frequencies": freq_str,
            "most_frequent": counts.index[0] if not counts.empty else None,
            "missing": df[var].isna().sum()
        })

# === Save summaries ===
numerical_df = pd.DataFrame(numerical_summary)
categorical_df = pd.DataFrame(categorical_summary)

numerical_df.to_csv(OUTPUT_NUMERICAL, index=False, quoting=csv.QUOTE_ALL)
categorical_df.to_csv(OUTPUT_CATEGORICAL, index=False, quoting=csv.QUOTE_ALL)

print("✅ Socioeconomic summaries saved to:")
print("  -", OUTPUT_NUMERICAL)
print("  -", OUTPUT_CATEGORICAL)


# === Stratified Analysis (Corrected) ===
STRATIFY_BY = ["village"]

for strat_var in STRATIFY_BY:
    if strat_var not in df.columns:
        print(f"⚠️ Stratification variable not found in dataset: {strat_var}")
        continue

    print(f"\n🔎 Stratified analysis by: {strat_var}")

    # Drop NA to get valid strata names
    strata = df[strat_var].dropna().unique()

    for val in strata:
        stratum_name = f"{strat_var}_{val}"
        print(f"  • Processing stratum: {stratum_name}")
        
        # Select data for the current stratum
        stratum_df = df[df[strat_var] == val].copy()
        labeled_stratum_df = labeled_df[labeled_df[strat_var] == val].copy()

        stratum_numerical_summary = []
        stratum_categorical_summary = []

        # Loop through variables selected in the codebook (e.g., 'socioeconomic')
        for _, row in selected_codebook.iterrows():
            var = row["variable"]
            var_type = row["type"]
            description = row.get("description", "")

            if var not in stratum_df.columns:
                continue

            if var_type.lower() == "numerical":
                # --- CORRECTED: Use stratum_df for calculations ---
                stats = stratum_df[var].describe() 
                
                # Check if enough data exists for stats
                if stats.empty or stats.get("count", 0) == 0:
                    continue
                    
                stratum_numerical_summary.append({
                    "stratum": val,
                    "variable": var,
                    "description": description,
                    "type": "Numerical",
                    "mean": stats.get("mean", None),
                    "std": stats.get("std", None),
                    "min": stats.get("min", None),
                    "25%": stats.get("25%", None),
                    "50% (median)": stats.get("50%", None),
                    "75%": stats.get("75%", None),
                    "max": stats.get("max", None),
                    "count_n": stats.get("count", 0), # Added count for clarity
                    "missing": stratum_df[var].isna().sum()
                })

            elif var_type.lower() == "categorical":
                label_col = var + "_label"
                if label_col not in labeled_stratum_df.columns:
                    continue

                # --- CORRECTED: Use labeled_stratum_df for frequencies ---
                counts = labeled_stratum_df[label_col].value_counts(dropna=False)
                total = counts.sum()
                
                if total == 0:
                    continue
                    
                freq_table = []
                for k, v in counts.items():
                    label = str(k) if pd.notna(k) else "Missing"
                    percentage = (v / total) * 100
                    freq_table.append(f"{label}: {v} ({percentage:.1f}%)")

                freq_str = "; ".join(freq_table)

                stratum_categorical_summary.append({
                    "stratum": val,
                    "variable": var,
                    "description": description,
                    "type": "Categorical",
                    "frequencies": freq_str,
                    "most_frequent": counts.index[0] if not counts.empty else None,
                    "count_n": total, # Added count for clarity
                    "missing": stratum_df[var].isna().sum()
                })

        # === Save stratified summaries ===
        if stratum_numerical_summary:
            stratum_num_path = os.path.join(OUTPUT_DIR, f"numerical_summary_{stratum_name}.csv")
            pd.DataFrame(stratum_numerical_summary).to_csv(stratum_num_path, index=False, quoting=csv.QUOTE_ALL)
            print(f"    → Numerical saved to: {stratum_num_path}")
        
        if stratum_categorical_summary:
            stratum_cat_path = os.path.join(OUTPUT_DIR, f"categorical_summary_{stratum_name}.csv")
            pd.DataFrame(stratum_categorical_summary).to_csv(stratum_cat_path, index=False, quoting=csv.QUOTE_ALL)
            print(f"    → Categorical saved to: {stratum_cat_path}")