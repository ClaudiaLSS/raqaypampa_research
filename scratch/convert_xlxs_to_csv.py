#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 17:47:08 2023

@author: claudia
"""

import pandas as pd

# Name of the sheet you want to convert
sheet_name = 'Martin Salazar'  # Replace with the name of your sheet

# Read the specified sheet from the Excel file
df = pd.read_excel('datos_raq.xlsx', sheet_name=sheet_name)

# Convert to CSV
df.to_csv('martin_salazar_test.csv', index=False)  # Save to CSV without index
