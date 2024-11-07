# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 01:07:45 2024

@author: tanil
"""
import csv
import matplotlib.pyplot as plt

# Function to read data from a CSV file
def read_csv(file):
    temperatures = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            try:
                temperatures.append(float(row[3].replace(',', '.')))
            except ValueError:
                continue  # Skip rows with invalid temperature format
    return temperatures

# Read data from the files
temperatures1 = read_csv('temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt')
temperatures2 = read_csv('temperatur_trykk_sauda.txt')

# Plot histogram over temperatures from both files
plt.figure(figsize=(10, 6))
plt.hist(temperatures1, bins=range(int(min(temperatures1)), int(max(temperatures1)) + 1), alpha=0.5, label='File 1')
plt.hist(temperatures2, bins=range(int(min(temperatures2)), int(max(temperatures2)) + 1), alpha=0.5, label='File 2')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')
plt.title('Histogram of Temperatures from Both Files')
plt.legend()
plt.show()
