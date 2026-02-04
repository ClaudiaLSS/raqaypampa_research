#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 21 09:41:18 2025

@author: claudia

Clusters survey respondents using both categorical and numerical variables
from selected dimensions using Gower distance and K-Medoids.
"""

import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn_extra.cluster import KMedoids
import gower
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/surveys/data_1.csv")
CODEBOOK_PATH = os.path.join(BASE_DIR, "../data/surveys/codebook.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "../results/clustering")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load data ===
df = pd.read_csv(DATA_PATH, na_values=["-1"], encoding="latin1")
codebook = pd.read_csv(CODEBOOK_PATH, encoding="latin1")

# === Clean codebook ===
codebook.columns = codebook.columns.str.strip()
codebook["variable"] = codebook["variable"].astype(str).str.strip()
codebook["type"] = codebook["type"].astype(str).str.strip().str.lower()
codebook["dimension"] = codebook["dimension"].astype(str).str.strip().str.lower()

# === Specify dimensions to include ===
dimensions_to_include = ["socioeconomics", "practices"]  # ← Edit this list to match your analysis

# === Select variables from specified dimensions ===
selected_cb = codebook[codebook["dimension"].isin(dimensions_to_include)]
num_vars = selected_cb[selected_cb["type"] == "numerical"]["variable"].tolist()
cat_vars = selected_cb[selected_cb["type"] == "categorical"]["variable"].tolist()

# === Ensure selected variables exist in the dataset ===
selected_vars = num_vars + cat_vars
available_vars = [var for var in selected_vars if var in df.columns]
missing_vars = [var for var in selected_vars if var not in df.columns]
if missing_vars:
    print("⚠️ Variables in codebook but missing in data:", missing_vars)

# Filter lists to keep only available variables
num_vars = [var for var in num_vars if var in available_vars]
cat_vars = [var for var in cat_vars if var in available_vars]

# === Subset dataframe ===
df_selected = df[num_vars + cat_vars].copy()

print(f"✅ Variables selected for clustering from dimensions {dimensions_to_include}:")
print(num_vars + cat_vars)

# === Imputation ===
if num_vars:
    imputer_num = SimpleImputer(strategy="mean")
    df_selected[num_vars] = imputer_num.fit_transform(df_selected[num_vars])

if cat_vars:
    imputer_cat = SimpleImputer(strategy="most_frequent")
    df_selected[cat_vars] = imputer_cat.fit_transform(df_selected[cat_vars].astype(str))

# === Compute Gower matrix ===
gower_matrix = gower.gower_matrix(df_selected)

# === Automatically select best k ===
silhouette_scores = []
cluster_range = range(2, 10)
for k in cluster_range:
    model_k = KMedoids(n_clusters=k, metric="precomputed", random_state=42)
    model_k.fit(gower_matrix)
    labels_k = model_k.labels_
    score = silhouette_score(gower_matrix, labels_k, metric="precomputed")
    silhouette_scores.append(score)
    print(f"Silhouette score for k={k}: {score:.3f}")

# === Find best k ===
best_k = cluster_range[np.argmax(silhouette_scores)]
print(f"\n✅ Best number of clusters based on silhouette: {best_k}")

# === Final clustering ===
model = KMedoids(n_clusters=best_k, metric="precomputed", random_state=42)
model.fit(gower_matrix)
df_selected["cluster"] = model.labels_

# === Save clustered data ===
df_clustered = df.copy()
df_clustered["cluster"] = model.labels_
df_clustered.to_csv(os.path.join(OUTPUT_DIR, "clustered_data_mixed.csv"), index=False)

# === Save and print medoids ===
medoid_indices = model.medoid_indices_
medoids = df_selected.iloc[medoid_indices].copy()
medoids["cluster"] = range(best_k)
medoids.to_csv(os.path.join(OUTPUT_DIR, "medoids.csv"), index=False)

print("\n📌 Medoids (Representative Households):")
print(medoids.head())

print("✅ Clustering complete. Results saved in:", OUTPUT_DIR)
print(df_selected.shape)
print(len(model.medoid_indices_))
print(best_k)