#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 21 14:41:35 2025

@author: claudia
"""

def select_relevant_variables(df, num_vars, cat_vars, missing_threshold=0.4, corr_threshold=0.9, dominant_threshold=0.8):
    """
    Automatically filters variables before clustering:
    - Removes constant variables
    - Removes variables with too much missing data
    - Removes highly correlated numerical variables
    - Removes categorical variables dominated by a single category
    """
    # Remove constant variables
    low_var_cols = df.nunique()[df.nunique() <= 1].index.tolist()
    num_vars = [v for v in num_vars if v not in low_var_cols]
    cat_vars = [v for v in cat_vars if v not in low_var_cols]

    # Remove variables with high missingness
    missing_ratio = df.isnull().mean()
    high_missing = missing_ratio[missing_ratio > missing_threshold].index.tolist()
    num_vars = [v for v in num_vars if v not in high_missing]
    cat_vars = [v for v in cat_vars if v not in high_missing]

    # Remove highly correlated numerical variables
    if num_vars:
        corr_matrix = df[num_vars].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop_corr = [col for col in upper.columns if any(upper[col] > corr_threshold)]
        num_vars = [v for v in num_vars if v not in to_drop_corr]

    # Remove categorical variables with a dominant category (e.g., ≥95% same value)
    dominant_cats = []
    for col in cat_vars:
        top_freq = df[col].value_counts(normalize=True, dropna=True).max()
        if top_freq >= dominant_threshold:
            dominant_cats.append(col)
    cat_vars = [v for v in cat_vars if v not in dominant_cats]

    return num_vars, cat_vars