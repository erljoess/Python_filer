#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 21:49:00 2024

@author: abayomibuys
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

with open("time.csv.txt", "r") as text:
    data_temp = []
    for line in text:
        try:
            # Split data into different components
            values = line.split(";")
        # Convert date and time
            date_part = values[0]
            date_comp = datetime.datetime.strptime(date_part, "%d.%m.%Y %H:%M")

        # converttemperature to readable in python
            temperature = float(values[4].replace(",", "."))

        # Create list
            data_temp.append((date_part, temperature))

        except (ValueError):
            continue
date_temp = np.array(data_temp)
date_met = date_temp[:, 0]
temperature = date_temp[:, 1].astype(float)
# print(temperature)


chunk_size = 30
index = 0
data = []
while index + chunk_size <= len(date_temp):
    start_index = index
    end_index = min(index + chunk_size, len(date_temp))
    start_date = date_met[start_index]
    chunk = temperature[start_index:end_index]
    average = np.mean(chunk)
    st_dev = np.std(chunk)
    data.append((start_date, average, st_dev))
  
    index += chunk_size

# print(data)
# print(f" Date: {start_date}, Temperature: {chunk}, Average: {average}")
plot_data = np.array(data)
date_used = plot_data[:, 0]
avg_temp = plot_data[:, 1].astype(float)
std_dev = plot_data[:, 2].astype(float)
# print(f"Date: {plot_data}")

#print(avg_temp)

# PLOT GRAPH

fig, ax = plt.subplots(figsize=(18, 14))
#ax.plot(date_used,avg_temp , color="orange", linewidth=0.5, label="Average temperature (Time)")
ax.errorbar(date_used, avg_temp, yerr = std_dev, errorevery = 30, capsize=5, capthick=1, ecolor='red', color='blue')  
   
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))   
ax.set_title('Average Temperature/Date graph with Errorbars')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.legend()

plt.show()


