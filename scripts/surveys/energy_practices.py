#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:51:45 2025

@author: claudia
energy_practices.py

Loads socioeconomic survey data and codebook, maps categorical codes to labels,
and generates summary statistics only for variables in the 'socioeconomic' dimension.

Usage:
    Run in your terminal or IDE (e.g., Spyder):
    $ python socioeconomic_profile.py
"""

import argparse
import pandas as pd
import os
import csv
import numpy as np

# === Paths (adjust to your project structure) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../../data/clean/surveys/data_1.csv")
CODEBOOK_PATH = os.path.join(BASE_DIR, "../../data/clean/surveys/codebook_1.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "../../results/energy_practices")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_NUMERICAL = os.path.join(OUTPUT_DIR, "numerical_summary.csv")
OUTPUT_CATEGORICAL = os.path.join(OUTPUT_DIR, "categorical_summary.csv")

OUTPUT_STRAT_NUMERICAL = os.path.join(OUTPUT_DIR, "stratified_numerical_summary.csv")
OUTPUT_STRAT_CATEGORICAL = os.path.join(OUTPUT_DIR, "stratified_categorical_summary.csv")

# EBP classification is computed separately by user_classification.py; this
# script only consumes its output to stratify the summaries by profile.
DEFAULT_CLASSIFICATIONS_PATH = os.path.join(
    BASE_DIR, "../../data/clean/surveys/classifications_oficial.csv")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--classifications", type=str, default=DEFAULT_CLASSIFICATIONS_PATH,
                     help="CSV produced by user_classification.py, with 'id' and "
                          "'ebp_profile' columns, used to stratify the summaries "
                          f"(default: {DEFAULT_CLASSIFICATIONS_PATH})")
args = parser.parse_args()
CLASSIFICATIONS_PATH = args.classifications

# === Load data ===
df = pd.read_csv(DATA_PATH, na_values=["-1"], encoding="latin1")

# Strip whitespace from data columns to prevent mismatch errors
df.columns = df.columns.str.strip()

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

dimensions_to_include = ['socioeconomics', "practices"]
selected_codebook = codebook[codebook["dimension"].isin(dimensions_to_include)]

for _, row in selected_codebook.iterrows():
    var = row["variable"]
    var_type = row["type"]
    codes = row["code"]

    if var not in df.columns:
        continue

    if var_type.lower() == "categorical" and isinstance(codes, str):
        mapping = parse_code_column(codes)
        if mapping:
            new_col = var + "_label"
            labeled_df[new_col] = df[var].map(mapping)

# =============================================================================
# === EBP CLASSIFICATION (loaded from user_classification.py output) ===
# =============================================================================

classifications = pd.read_csv(CLASSIFICATIONS_PATH)[["id", "ebp_profile"]]
labeled_df = labeled_df.merge(classifications, on="id", how="left")
labeled_df["ebp_profile"] = labeled_df["ebp_profile"].fillna("Unclassified")

unclassified_count = (labeled_df["ebp_profile"] == "Unclassified").sum()
print("\n" + "="*50)
print("EBP CLASSIFICATION (from user_classification.py)")
print("="*50)
print(labeled_df["ebp_profile"].value_counts())
if unclassified_count > 0:
    print(f"\n⚠️  WARNING: {unclassified_count} households have no matching "
          f"classification in {CLASSIFICATIONS_PATH}.")
print("="*50 + "\n")

# =============================================================================
# === Generate general summary ===
# =============================================================================
numerical_summary = []
categorical_summary = []

for _, row in selected_codebook.iterrows():
    var = row["variable"]
    var_type = row["type"]
    description = row.get("description", "")

    if var not in df.columns:
        continue

    if var_type.lower() == "numerical":
        stats = df[var].describe()
        numerical_summary.append({
            "variable": var,
            "description": description,
            "type": "Numerical",
            "mean": stats.get("mean", np.nan),
            "std": stats.get("std", np.nan),
            "min": stats.get("min", np.nan),
            "25%": stats.get("25%", np.nan),
            "50% (median)": stats.get("50%", np.nan),
            "75%": stats.get("75%", np.nan),
            "max": stats.get("max", np.nan),
            "missing": df[var].isna().sum()
        })

    elif var_type.lower() == "categorical":
        label_col = var + "_label"
        if label_col not in labeled_df.columns:
            continue

        counts = labeled_df[label_col].value_counts(dropna=False)
        total = counts.sum()
        freq_table = []
        for k, v in counts.items():
            label = str(k) if pd.notna(k) else "Missing"
            percentage = (v / total) * 100 if total > 0 else 0
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

# =============================================================================
# === Stratified Analysis by ebp_profile ===
# =============================================================================
strat_col = "ebp_profile"
stratified_numerical_summary = []
stratified_categorical_summary = []

if strat_col in labeled_df.columns:
    groups = labeled_df[strat_col].dropna().unique()

    for group in groups:
        group_df = labeled_df[labeled_df[strat_col] == group]

        for _, row in selected_codebook.iterrows():
            var = row["variable"]
            var_type = row["type"]
            description = row.get("description", "")

            if var not in group_df.columns:
                continue
            
            if var == "family_type":  
                continue

            if var_type.lower() == "numerical":
                stats = group_df[var].describe()
                stratified_numerical_summary.append({
                    "ebp_profile": group,
                    "variable": var,
                    "description": description,
                    "type": "Numerical",
                    "mean": stats.get("mean", np.nan),
                    "std": stats.get("std", np.nan),
                    "min": stats.get("min", np.nan),
                    "25%": stats.get("25%", np.nan),
                    "50% (median)": stats.get("50%", np.nan),
                    "75%": stats.get("75%", np.nan),
                    "max": stats.get("max", np.nan),
                    "missing": group_df[var].isna().sum()
                })

            elif var_type.lower() == "categorical":
                label_col = var + "_label"
                if label_col not in group_df.columns:
                    continue

                counts = group_df[label_col].value_counts(dropna=False)
                total = counts.sum()
                freq_table = []
                for k, v in counts.items():
                    label = str(k) if pd.notna(k) else "Missing"
                    percentage = (v / total) * 100 if total > 0 else 0
                    freq_table.append(f"{label}: {v} ({percentage:.1f}%)")

                freq_str = "; ".join(freq_table)

                stratified_categorical_summary.append({
                    "ebp_profile": group,
                    "variable": var,
                    "description": description,
                    "type": "Categorical",
                    "frequencies": freq_str,
                    "most_frequent": counts.index[0] if not counts.empty else None,
                    "missing": group_df[var].isna().sum()
                })

# === Save summaries ===
numerical_df = pd.DataFrame(numerical_summary)
categorical_df = pd.DataFrame(categorical_summary)
strat_num_df = pd.DataFrame(stratified_numerical_summary)
strat_cat_df = pd.DataFrame(stratified_categorical_summary)

numerical_df.to_csv(OUTPUT_NUMERICAL, index=False, quoting=csv.QUOTE_ALL)
categorical_df.to_csv(OUTPUT_CATEGORICAL, index=False, quoting=csv.QUOTE_ALL)

if not strat_num_df.empty:
    strat_num_df.to_csv(OUTPUT_STRAT_NUMERICAL, index=False, quoting=csv.QUOTE_ALL)
    strat_cat_df.to_csv(OUTPUT_STRAT_CATEGORICAL, index=False, quoting=csv.QUOTE_ALL)

print("✅ Summaries saved to:", OUTPUT_DIR)

'''
# === EXTENDED CORRELATION ANALYSIS (Numerical & Categorical) ===
print("\n🔍 Running extended correlation analysis (numerical–categorical–categorical)...")

# Separate numerical and categorical variables
numerical_vars = selected_codebook[selected_codebook["type"].str.lower() == "numerical"]["variable"].tolist()
categorical_vars = selected_codebook[selected_codebook["type"].str.lower() == "categorical"]["variable"].tolist()

numerical_vars = [v for v in numerical_vars if v in df.columns]
categorical_vars = [v for v in categorical_vars if v + "_label" in labeled_df.columns]

# Helper: Correlation ratio (η) for numerical–categorical
def correlation_ratio(categories, values):
    """Compute correlation ratio (η) between categorical and numerical variable."""
    try:
        categories = np.array(categories)
        values = np.array(values)
        fcat, _ = pd.factorize(categories)
        cat_num = np.max(fcat) + 1
        y_avg = np.nanmean(values)
        numerator = 0.0
        denominator = np.nansum((values - y_avg) ** 2)
        for i in range(cat_num):
            cat_values = values[np.argwhere(fcat == i).flatten()]
            if cat_values.size > 0:
                n_i = cat_values.size
                y_i = np.nanmean(cat_values)
                numerator += n_i * (y_i - y_avg) ** 2
        return np.sqrt(numerator / denominator) if denominator != 0 else np.nan
    except Exception:
        return np.nan

# Helper: Cramér’s V for categorical–categorical
def cramers_v(x, y):
    """Compute Cramér’s V for two categorical variables."""
    try:
        confusion_matrix = pd.crosstab(x, y)
        chi2 = chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        phi2corr = max(0, phi2 - ((k - 1)*(r - 1))/(n - 1))
        rcorr = r - ((r - 1)**2)/(n - 1)
        kcorr = k - ((k - 1)**2)/(n - 1)
        return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))
    except Exception:
        return np.nan

# Store all correlations
extended_corrs = []

# 1. Numerical–Numerical (Pearson)
for i, var1 in enumerate(numerical_vars):
    for var2 in numerical_vars[i+1:]:
        valid_data = df[[var1, var2]].dropna()
        if len(valid_data) > 1:
            # pearsonr returns (statistic, pvalue)
            corr, p_val = pearsonr(valid_data[var1], valid_data[var2])
        else:
            corr, p_val = np.nan, np.nan
            
        extended_corrs.append({
            "Variable 1": var1,
            "Variable 2": var2,
            "Type": "Numerical–Numerical",
            "Method": "Pearson",
            "Correlation": corr,
            "P-Value": p_val
        })

# 2. Numerical–Categorical (Correlation ratio)
for num_var in numerical_vars:
    for cat_var in categorical_vars:
        label_col = cat_var + "_label"
        eta = correlation_ratio(labeled_df[label_col], df[num_var])
        p_val = np.nan  # correlation_ratio does not compute p-value
        extended_corrs.append({
            "Variable 1": num_var,
            "Variable 2": cat_var,
            "Type": "Numerical–Categorical",
            "Method": "Correlation ratio (η)",
            "Correlation": eta,
            "P-Value": p_val
        })

# 3. Categorical–Categorical (Cramér’s V)
for i, var1 in enumerate(categorical_vars):
    for var2 in categorical_vars[i+1:]:
        label1 = var1 + "_label"
        label2 = var2 + "_label"
        v = cramers_v(labeled_df[label1], labeled_df[label2])
        p_val = np.nan  # cramers_v does not compute p-value
        extended_corrs.append({
            "Variable 1": var1,
            "Variable 2": var2,
            "Type": "Categorical–Categorical",
            "Method": "Cramér’s V",
            "Correlation": v,
            "P-Value": p_val
        })

# === Save extended correlations ===
extended_corrs_df = pd.DataFrame(extended_corrs)
extended_corrs_df["abs_corr"] = extended_corrs_df["Correlation"].abs()
extended_corrs_df = extended_corrs_df.sort_values("abs_corr", ascending=False)

extended_corrs_path = os.path.join(OUTPUT_DIR, "extended_correlations.csv")
extended_corrs_df.to_csv(extended_corrs_path, index=False, quoting=csv.QUOTE_ALL)

print(f"✅ Extended correlations (all variable types) saved to: {extended_corrs_path}")


'''