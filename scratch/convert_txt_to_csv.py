# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv

# Input and output file paths
txt_file_path = '/home/claudia/Documents/data_processing/celestina_inturias/20000106.txt'  # Replace with the path to your semicolon-delimited .txt file
csv_file_path = '/home/claudia/Documents/data_processing/celestina_inturias/20000106.csv'  # Replace with the desired output CSV file path

# Open the .txt file for reading and the CSV file for writing
with open(txt_file_path, 'r', encoding='utf-8', errors='ignore') as txt_file, open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer with a comma (',') as the delimiter
    csv_writer = csv.writer(csv_file, delimiter=',')

    # Read each line from the .txt file and write it to the CSV file
    for line in txt_file:
        # Split the line using semicolon (';') as the delimiter
        fields = line.strip().split(';')

        # Write the fields to the CSV file
        csv_writer.writerow(fields)

print(f'Conversion from {txt_file_path} to {csv_file_path} complete.')

