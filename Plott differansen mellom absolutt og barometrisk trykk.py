# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 01:42:13 2024

@author: tanil
"""

import csv
import matplotlib.pyplot as plt

# Function to read data from a CSV file
def read_csv(file):
    timestamps = []
    pressure_diff = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            try:
                barometric_pressure = float(row[2].replace(',', '.'))
                absolute_pressure = float(row[3].replace(',', '.'))
                timestamps.append(int(row[1]))
                pressure_diff.append(absolute_pressure - barometric_pressure)
            except ValueError:
                continue  # Skip rows with invalid data
    return timestamps, pressure_diff

# Function to calculate the rolling mean
def rolling_mean(data, window_size):
    smoothed_data = []
    for i in range(len(data)):
        start = max(0, i - window_size)
        end = min(len(data), i + window_size + 1)
        smoothed_data.append(sum(data[start:end]) / (end - start))
    return smoothed_data

# Read data from the file
file_path = 'trykk_og_temperaturlogg_rune_time.csv.txt'
timestamps, pressure_diff = read_csv(file_path)

# Calculate the rolling mean to smooth the data
smoothed_pressure_diff = rolling_mean(pressure_diff, 10)

# Plot the smoothed pressure difference
plt.figure(figsize=(12, 6))
plt.plot(timestamps, smoothed_pressure_diff, label='Smoothed Pressure Difference')
plt.xlabel('Time since start (seconds)')
plt.ylabel('Pressure Difference (bar)')
plt.title('Smoothed Pressure Difference between Absolute and Barometric Pressure')
plt.legend()
plt.grid(True)
plt.show()
