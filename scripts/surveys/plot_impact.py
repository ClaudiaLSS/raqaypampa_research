#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 14:23:33 2025

@author: claudia
"""

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# === Sample Data ===
data = {
    'Quality': {
        'Excellent': [6, 4],
        'Good': [31, 34],
        'Bad': [0, 0],
        'N/A': [0, 0]
    },
    'Affordability': {
        'Accessible': [36, 38],
        'Inaccessible': [1, 0]
    },
    'Satisfaction': {
        'Very satisfied': [4, 1],
        'Satisfied': [33, 37],
        'Unsatisfied': [1, 0],
        'N/A': [1, 0]
    },
    'Blackouts': {
        'Never': [29, 37],
        '2 per month': [1, 0],
        'Can not stimate': [7, 0]
    }
}

raw_data = data

# === Use Pastel palette for all variables ===
palettes = {}
for var in raw_data:
    n_labels = len(raw_data[var])
    palettes[var] = sns.color_palette("pastel", n_colors=n_labels)

label_color_map = {}
for var in raw_data:
    labels = list(raw_data[var].keys())
    colors = palettes[var]
    label_color_map[var] = dict(zip(labels, colors))


for var in raw_data:
    fig, ax = plt.subplots(figsize=(10, 3))
    plt.rcParams.update({'font.family':'serif'})  # Serif font for report style

    responses = raw_data[var]
    labels = list(responses.keys())

    sam_bottom = 0
    gbo_bottom = 0
    y_pos = 0  # single bar at y=0

    # Plot bars with a slight edge shadow effect and smaller height
    for label in labels:
        sam_val = responses[label][0]
        gbo_val = responses[label][1]
        color = label_color_map[var][label]

        ax.barh(y_pos, sam_val, left=sam_bottom, color=color, edgecolor='black', alpha=0.85, height=0.2)
        sam_bottom += sam_val

        ax.barh(y_pos, -gbo_val, left=-gbo_bottom, color=color, edgecolor='black', alpha=0.85, height=0.2)
        gbo_bottom += gbo_val

    # Axes formatting
    ax.set_yticks([y_pos])
    ax.set_yticklabels([var], fontsize=14, weight='bold', color='black')
    ax.axvline(0, color='black', linewidth=1.1, linestyle='--', alpha=0.8)
    ax.grid(axis='x', linestyle='--', color='lightgray', alpha=0.6)
    
    # Hide unnecessary spines for a clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{abs(int(x))}'))

    limit = max(sam_bottom, gbo_bottom)
    ax.set_xlim(-limit - 5, limit + 5)

    # Tighter y limits so bars hug the x-axis line
    ax.set_ylim(-0.25, 0.25)  

    # === Legend outside above the plot ===
    fig.subplots_adjust(top=0.75)

    legend_y = 0.85  # figure coords
    box_size = 0.027
    spacing = 0.14

    n_labels = len(labels)
    total_legend_width = spacing * n_labels
    start_x = 0.55 - total_legend_width / 2

    for i, label in enumerate(labels):
        color = label_color_map[var][label]
        rect_x = start_x + i * spacing

        # Legend boxes and text
        fig.patches.append(
            plt.Rectangle((rect_x, legend_y), box_size, box_size,
                          transform=fig.transFigure, color=color, clip_on=False, ec='black', lw=0.5)
        )
        fig.text(rect_x + box_size + 0.009, legend_y + box_size / 2, label,
                 fontsize=11, ha='left', va='center', family='serif', color='black')

    # Label x axis nicely
    ax.set_xlabel('Number of Households', fontsize=14, color='black', labelpad=12)

    plt.tight_layout(rect=[0, 0, 1, 0.9])  # leave top space for legend
    
    # Save the figure as a PNG file
    fig.savefig(f"{var}.png", dpi=300, bbox_inches='tight')
    
    plt.show()
