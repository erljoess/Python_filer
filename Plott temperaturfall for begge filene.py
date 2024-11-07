# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 00:43:15 2024

@author: tanil
"""

import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Function to read data from a CSV file
def read_csv(file):
    timestamps = []
    temperatures = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            try:
                timestamps.append(datetime.strptime(row[2], '%d.%m.%Y %H:%M'))
                temperatures.append(float(row[3].replace(',', '.')))
            except ValueError:
                continue  # Skip rows with invalid date format
    return timestamps, temperatures

# Read data from the files
timestamps1, temperatures1 = read_csv("C:\\Bachelor File (DATA TEKNOLOGY)\\Ist semester\\DAT120-1 24H Grunnleggende programmering\\temperatur_trykk_sauda.txt")
timestamps2, temperatures2 = read_csv("C:\\Bachelor File (DATA TEKNOLOGY)\\Ist semester\\DAT120-1 24H Grunnleggende programmering\\temperatur_trykk_met_samme_rune_time_datasett.csv.txt")

# Filter data for June 11 and June 12
def filter_data(timestamps, temperatures, date):
    return [(t, temp) for t, temp in zip(timestamps, temperatures) if t.date() == date]

data1_june11 = filter_data(timestamps1, temperatures1, datetime(2021, 6, 11).date())
data1_june12 = filter_data(timestamps1, temperatures1, datetime(2021, 6, 12).date())

data2_june11 = filter_data(timestamps2, temperatures2, datetime(2021, 6, 11).date())
data2_june12 = filter_data(timestamps2, temperatures2, datetime(2021, 6, 12).date())

# Find highest temperature on June 11 and lowest temperature on June 12 for both files
max_temp_time1 = max(data1_june11, key=lambda x: x[1])[0]
min_temp_time1 = min(data1_june12, key=lambda x: x[1])[0]

max_temp_time2 = max(data2_june11, key=lambda x: x[1])[0]
min_temp_time2 = min(data2_june12, key=lambda x: x[1])[0]

# Filter data based on found timestamps
def filter_by_time_range(timestamps, temperatures, start_time, end_time):
    return [(t, temp) for t, temp in zip(timestamps, temperatures) if start_time <= t <= end_time]

filtered_data1 = filter_by_time_range(timestamps1, temperatures1, max_temp_time1, min_temp_time1)
filtered_data2 = filter_by_time_range(timestamps2, temperatures2, max_temp_time2, min_temp_time2)

# Plot temperature fall for both files
plt.figure(figsize=(10, 6))
plt.plot([t for t, temp in filtered_data1], [temp for t, temp in filtered_data1], label='temperatur_trykk_sauda.txt')
plt.plot([t for t, temp in filtered_data2], [temp for t, temp in filtered_data2], label='temperatur_trykk_met_samme_rune_time_datasett.csv.txt')
plt.xlabel('Timestamp')
plt.ylabel('Temperature')
plt.title('Temperature Fall on June 11 and June 12')
plt.legend()
plt.show()
