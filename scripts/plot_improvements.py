#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 16:01:23 2025

@author: claudia
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Example data
data = {
    'Improved children’s education': {'Samionta': {'Yes': 74, 'No': 26}, 'Gbowele': {'Yes': 78, 'No': 22}},
    'Better communication/information at home': {'Samionta': {'Yes': 82, 'No': 18}, 'Gbowele': {'Yes': 87, 'No': 13}},
    'Improved household task performance': {'Samionta': {'Yes': 42, 'No': 58}, 'Gbowele': {'Yes': 73, 'No': 27}},
    'New activities possible at home': {'Samionta': {'Yes': 11, 'No': 89}, 'Gbowele': {'Yes': 11, 'No': 89}},
    'Improved health': {'Samionta': {'Yes': 0, 'No': 100}, 'Gbowele': {'Yes': 0, 'No': 100}},
    'Limits to connect more appliances': {'Samionta': {'Yes': 0, 'No': 100}, 'Gbowele': {'Yes': 16, 'No': 84}},
    'Improved income': {'Samionta': {'Yes': 16, 'No': 84}, 'Gbowele': {'Yes': 3, 'No': 97}},
    'More free time': {'Samionta': {'Yes': 5, 'No': 95}, 'Gbowele': {'Yes': 0, 'No': 100}},
}

variables = list(data.keys())
y = np.arange(len(variables))

# Get values
yes_samionta = [-data[v]['Samionta']['Yes'] for v in variables]  # Negative for left
no_samionta  = [-data[v]['Samionta']['No']  for v in variables]

yes_gbowele = [data[v]['Gbowele']['Yes'] for v in variables]
no_gbowele  = [data[v]['Gbowele']['No']  for v in variables]

bar_height = 0.4

# Shared colors
yes_color = "#6fc276"  # Greenish
no_color = "#db5856"   # Orange

fig, ax = plt.subplots(figsize=(10, 6))

# Plot Samionta (left side)
ax.barh(y, yes_samionta, height=bar_height, color=yes_color, edgecolor='black', label="Yes", alpha=0.6)
ax.barh(y, no_samionta, height=bar_height, left=yes_samionta, color=no_color, edgecolor='black', label="No", alpha=0.6)

# Plot Gbowele (right side)
ax.barh(y, yes_gbowele, height=bar_height, color=yes_color, edgecolor='black',alpha=0.6)
ax.barh(y, no_gbowele, height=bar_height, left=yes_gbowele, color=no_color, edgecolor='black', alpha=0.6)

# Center line
ax.axvline(0, color='black', linewidth=0.8)

# Text labels (skip zeros)
for i in range(len(variables)):
    if -yes_samionta[i] != 0:
        ax.text(yes_samionta[i]/2, y[i], f"{-yes_samionta[i]}%", va='center', ha='center', fontsize=9)
    if -no_samionta[i] != 0:
        ax.text(yes_samionta[i] + no_samionta[i]/2, y[i], f"{-no_samionta[i]}%", va='center', ha='center', fontsize=9)
    if yes_gbowele[i] != 0:
        ax.text(yes_gbowele[i]/2, y[i], f"{yes_gbowele[i]}%", va='center', ha='center', fontsize=9)
    if no_gbowele[i] != 0:
        ax.text(yes_gbowele[i] + no_gbowele[i]/2, y[i], f"{no_gbowele[i]}%", va='center', ha='center', fontsize=9)

# Format
ax.set_yticks(y)
ax.set_yticklabels(variables, fontsize=12)
ax.set_xlabel('')                      # Remove x-axis label
ax.set_xticks([])                     # Remove x-axis tick numbers
ax.spines['bottom'].set_visible(False)  # Remove x-axis line

ax.set_title('', fontsize=14, weight='bold')
ax.set_xlim(-100, 100)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), ncol=2, title="Response")
ax.grid(axis='x', linestyle='--', alpha=0.5)

# Annotations for villages
ax.text(-102, len(variables)-0.3, "Samionta", ha='left', fontsize=11, fontweight='bold')
ax.text(102, len(variables)-0.3, "Gbowele", ha='right', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig("diverging_bar_yes_no_villages_2.png", dpi=300, bbox_inches='tight')
plt.show()