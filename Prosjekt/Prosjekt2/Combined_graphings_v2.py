#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:19:28 2024

@author: abayomibuys and erljoess
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import convert_met_data as cmd       # Hentar inn funksjonane frå convert_met_data.py og kallar på dei med cmd.

    #CREATING LISTS FOR PRESSURE:
sola_date_pressure = []

with open("met.csv.txt","r") as sola_temp:
    for line in sola_temp:
        try:
        #Split data into different components
            values_sola = line.split(";")
         
        #Convert date and time
            date_part = values_sola[2]
            date_time = datetime.datetime.strptime(date_part, "%d.%m.%Y %H:%M")
            
        #convert pressure to readable in python
            pressure_sola = float(values_sola[4].replace(",","."))
           
        except(ValueError):
            continue
        
        sola_date_pressure.append((date_time, pressure_sola))
            #print(sola_date_pressure)

date_press = np.array(sola_date_pressure)
#print(sola_date_pressure[0])
date_met = date_press[:,0]
pressure = date_press[:,1]

data_abs_press = []
with open("time.csv.txt","r") as met_pressure:
    for line in met_pressure:
       try: 
       #Split data into different components
            values_met = line.split(";")
         
        #Convert date and time
            date_part = values_met[0]
            second_part = values_met[1]
            date_comp = datetime.datetime.strptime(date_part, "%m.%d.%Y %H:%M")
       except(ValueError):
            continue
        
       pressure_met = float(values_met[3].replace(",","."))
       pressure_adj = pressure_met*10
       data_abs_press.append((date_comp, pressure_adj))   
       #print(date_comp, pressure_adj)

date_abs_press = np.array(data_abs_press)
#print(date_abs_press[0])
date_met_2 = date_abs_press[:,0]
abs_pressure = date_abs_press[:,1]      

data = []

with open("time.csv.txt","r") as met_pressure:
    for line in met_pressure:
        try:
            values_met = line.split(";")            #Split data into different components
            barometer_val = float(values_met[2].replace(",","."))  
            if values_met[2] != "":
           #convert pressure to readable in python
                 barometer_adj = barometer_val*10
                                        
        #Convert date and time
            date_part = values_met[0]
            date_comp = datetime.datetime.strptime(date_part, "%m.%d.%Y %H:%M")
        except(ValueError):
                continue
        data.append((date_comp, barometer_adj)) 
        #print(date_comp, barometer_adj)

date_barometer = np.array(data)
date_time = date_barometer[:,0]
barometer = date_barometer[:,1]  

    #LAGAR DATA OG LISTER FOR TEMPERATUR:
Sola_data = []
Sola_data = cmd.convert_Sola_data() # Hentar inn data til Sola_data[]. Format: [2021, 6, 11, 1, 0, 16.1, 1013.7]

Time_data = []
Time_data = cmd.convert_Time_data() # Hentar inn data til Time_data[]. Format: [2021, 6, 11, 14, 23, 0, 1010.3, 1004.52, 17.18]

Sirdal_data =[]
Sauda_data = []
Sirdal_data, Sauda_data = cmd.convert_Sirdal_Sauda_data()              #Format: (2021, 6, 10, 1, 0, 14.9, 1017.1)
    
#Vil ha same start-tid for listene:
cut_date = Sola_data[0][2]
cut_hour = Sola_data[0][3]

#print(Time_data[:2], Sola_data[0], Sirdal_data[0], Sauda_data[0])
kutt = 0
for linje in Sola_data:
    if linje[2] < cut_date:
        kutt += 1
    elif linje[3] < cut_hour:
        kutt += 1
    else:
        break
Sola_data = Sola_data[kutt:]

kutt = 0
for linje in Sauda_data:
    if linje[2] < cut_date:
        kutt += 1
    elif linje[3] < cut_hour:
        kutt += 1
    else:
        break
Sauda_data = Sauda_data[kutt:]

kutt = 0
for linje in Sirdal_data:
   if linje[2] < cut_date:
        kutt += 1
   elif linje[3] < cut_hour:
        kutt += 1
   else:
        break
Sirdal_data = Sirdal_data[kutt:]

#print(Time_data[:2])
#print(Sola_data[:1])
#print(Sirdal_data[:1])
#print(Sauda_data[:1])
#print(len(Sola_data), len(Sirdal_data), len(Sauda_data))
Time_temp_min = []
Time_temp_max = []
Time_coldest = []
Time_warmest = []

for linje in Time_data:
    if not Time_temp_min or Time_temp_min[2] != linje[2]:
        if len(Time_temp_min) > 1:
            Time_coldest.append(Time_temp_min)                         # Legg til Time_temp_min i Time_coldest[], altså det kaldaste i Time_temp[] siste døgn.
        if len(Time_temp_max) > 1:
            Time_warmest.append(Time_temp_max)                         # Legg til Time_temp_max i Time_warmest[], altså det varmaste i Time_temp[] siste døgn.
        Time_temp_min = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5], linje[8]]   # Set Time_temp_min til første temp i nytt døgn.
        Time_temp_max = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5], linje[8]]   # Set Time_temp_max til første temp i nytt døgn.
    if Time_temp_min[6] > linje[8]:                                     #Viss registrert temperatur er lågare enn Time_temp_min, oppdater Time_temp_min.
        Time_temp_min = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5], linje[8]]
    if Time_temp_max[6] < linje[8]:                                     #Viss registrert temperatur er høgare enn Time_temp_max, oppdater Time_temp_max.
        Time_temp_max = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5], linje[8]]
Time_coldest.append(Time_temp_min)
Time_coldest = Time_coldest[1:] #Treng ikkje første døgn sidan max manglar. Same for siste døgn med warmest.

    #Etablerer ei liste med tid og temperatur for den høgaste og lågaste temperaturen i Time_temp[]:
Time_temp_drop = []
#print(Time_warmest)

for i in range((len(Time_warmest))*2): # Gjer klart til plotting
    if i %2 == 0: #Dei høgaste temperaturane er lagra i partal
        Time_temp_drop.append(Time_warmest[(int(i/2))])
    else:
        Time_temp_drop.append(Time_coldest[(int((i-1)/2))])
        
Sola_temp_min = []
Sola_temp_max = []
Sola_coldest = []
Sola_warmest = []

for linje in Sola_data:
    if not Sola_temp_min or Sola_temp_min[2] != linje[2]:
        if len(Sola_temp_min) > 1:
            Sola_coldest.append(Sola_temp_min)                         # Legg til Sola_temp_min i Sola_coldest[], altså det kaldaste i Sola_temp[] siste døgn.
        if len(Sola_temp_max) > 1:
            Sola_warmest.append(Sola_temp_max)                         # Legg til Sola_temp_max i Sola_warmest[], altså det varmaste i Sola_temp[] siste døgn.
        Sola_temp_min = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5]]   # Set Sola_temp_min til første temp i nytt døgn.
        Sola_temp_max = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5]]   # Set Sola_temp_max til første temp i nytt døgn.
    if Sola_temp_min[5] > linje[5]:                                     #Viss registrert temperatur er lågare enn Sola_temp_min, oppdater Sola_temp_min.
        Sola_temp_min = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5]]
    if Sola_temp_max[5] < linje[5]:                                     #Viss registrert temperatur er høgare enn Sola_temp_max, oppdater Sola_temp_max.
        Sola_temp_max = [linje[0], linje[1], linje[2], linje [3], linje[4], linje[5]]
Sola_coldest.append(Sola_temp_min)
Sola_coldest = Sola_coldest[1:] #Treng ikkje første døgn sidan max manglar. Same for siste døgn med warmest.

    #Etablerer ei liste med tid og temperatur for den høgaste og lågaste temperaturen i Sola_temp[]:
Sola_temp_drop = []
#print(Sola_warmest, Sola_coldest)

for i in range((len(Sola_warmest))*2): # Gjer klart til plotting
    if i %2 == 0: #Dei høgaste temperaturane er lagra i partal
        Sola_temp_drop.append(Sola_warmest[(int(i/2))])
    else:
        Sola_temp_drop.append(Sola_coldest[(int((i-1)/2))])

#print(Sola_temp_drop)

    #Bereknar gjennomsnittstemperaturen for dei siste 5 minutta i Time_temp[]:
Time_temp_total = []
Time_temp_snitt = []

for i, linje in enumerate(Time_data):           #Går gjennom kvar linje i Time_data, og bereknar snitt av dei siste 5 minutta.
    Time_temp_total.append(float(linje[8]))
    if i % 6 == 0:
        while len(Time_temp_total) > 30:         #For å få rett lengde på gjennomsnitts-berekninga:
            Time_temp_total.pop(0)               #Fjernar det eldste elementet i Time_temp_total[].
        if i >= 29:                              #Igjen; startar berekninga av gjennomsnittet etter 30 linjer.
            Time_temp_snitt.append([linje[0], linje[1], linje[2], linje[3], linje[4], linje[5], float(f"{sum(Time_temp_total)/30:.2f}")]) #Her måtte eg bruke "float" for å ikkje få string?!.

Time_underveis =[]
Time_data_lik_Sola_tider = []
for linje in Time_data:
    if linje[6] != -1:
        Time_underveis.append(linje)
for linje in Time_underveis:
    if linje[4] == 0:
        Time_data_lik_Sola_tider.append(linje)
Time_underveis = None
#print(Time_data_lik_Sola_tider[:2])

Sola_tider_lik_Time_tider = Sola_data
cut_date = Time_data[0][2]
cut_hour = Time_data[0][3]

#print(Time_data[:2], Sola_data[0], Sirdal_data[0], Sauda_data[0])
kutt = 0
for linje in Sola_data:
    if linje[2] < cut_date:
        kutt += 1
    elif linje[3] < cut_hour:
        kutt += 1
    else:
        break
Sola_tider_lik_Time_tider = Sola_tider_lik_Time_tider[kutt + 1:]
#print(Time_data_lik_Sola_tider[:1], Sola_tider_lik_Time_tider[:1], len(Sola_tider_lik_Time_tider), len(Time_data_lik_Sola_tider))

antall = 0
forskjell = 0
forskjell_total = 0
storst_forskjell = 0
storst_forskjell_tid = []
minst_forskjell = 1000
minst_forskjell_tid = []
for linje, element in enumerate(Time_data_lik_Sola_tider):
    forskjell = Sola_tider_lik_Time_tider[linje][5] - Time_data_lik_Sola_tider[linje][8]
    antall += 1
    forskjell_total += forskjell
    if abs(forskjell) > storst_forskjell:
        storst_forskjell_tid = Sola_tider_lik_Time_tider[linje][:4]
        storst_forskjell = abs(forskjell)
    if abs(forskjell) < minst_forskjell:
        minst_forskjell_tid = Sola_tider_lik_Time_tider[linje][:4]
        minst_forskjell = abs(forskjell)
snitt_forskjell = forskjell_total / antall
print(f"Average deviation in temperature between met and time was {abs(snitt_forskjell):.2f}.")
print(f"The largest difference was the {storst_forskjell_tid[2]}th, at {storst_forskjell_tid[3]:02d}:00, with {storst_forskjell:.2f} degrees.")
print(f"The smallest difference was the {minst_forskjell_tid[2]}th, at {minst_forskjell_tid[3]:02d}:00, with {minst_forskjell:.2f} degrees.")

    # Hentar ut tid og temperatur frå listene, og konverterer tid til datetime-objekt for å ha felles x-verdiar:: 
Sola_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Sola_data]
Sola_temps = [d[5] for d in Sola_data]
Sirdal_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Sirdal_data]
Sirdal_temps = [d[5] for d in Sirdal_data]
Sirdal_press = [d[6] for d in Sirdal_data]
Sauda_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Sauda_data]
Sauda_temps = [d[5] for d in Sauda_data]
Sauda_press = [d[6] for d in Sauda_data]
#print(Sauda_data[:1], Sirdal_data[:1])
Time_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Time_data]
Time_temps = [d[8] for d in Time_data]
Time_temp_avg = [d[6] for d in Time_temp_snitt]  
Time_temp_avg_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Time_temp_snitt]
#Time_temp_drop = Time_temp_drop[2:4]
Time_temp_drop_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Time_temp_drop]
Time_temp_drop = [d[6] for d in Time_temp_drop]
Sola_temp_drop_tider = [datetime.datetime(d[0], d[1], d[2], d[3], d[4]) for d in Sola_temp_drop]
Sola_temp_drop = [d[5] for d in Sola_temp_drop]
#print(Sola_temp_drop_tider)
#print(Sola_temp_drop)
    #Lagar ein funksjon for å plotte data:
def plot_graphs():
    # Lagar figurvindauget, med to undervindauger, og set storleik.
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 14))
# Temperatur-plotta:
    ax1.plot(Time_tider, Time_temps, color="blue", label="Temperature (Time)")
    ax1.plot(Time_temp_avg_tider, Time_temp_avg, color="orange", linewidth=0.5, label="Average temperature (Time)")
    ax1.plot(Sola_tider, Sola_temps, color="green", label="Temperature (MET)")
    ax1.plot(Sauda_tider, Sauda_temps, color="gray", label="Temperature (Sauda)")
    ax1.plot(Sirdal_tider, Sirdal_temps, color="red", label="Temperature (Sirdal)")
    #Plotting av to og to temperaturar, blir mange slices:
    ax1.plot(Time_temp_drop_tider[:2], Time_temp_drop[:2], color="violet", label='Temperature drop from max til min, time data')
    ax1.plot(Time_temp_drop_tider[-2:], Time_temp_drop[-2:], color="violet")
    ax1.plot(Sola_temp_drop_tider[:2], Sola_temp_drop[:2], color="pink", label='Temperature drop from max til min, met data')
    ax1.plot(Sola_temp_drop_tider[2:4], Sola_temp_drop[2:4], color="pink")
    # Formaterer x-aksen:
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
    #Set overskrift og aksetitlar, samt plasserer "skiltet" (legend) med plot labels der det er best plass:
    ax1.set_title('Temperature/Date graph')
    ax1.set_xlabel('Time (DD-MO HH:MI)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.legend(loc="upper left", fontsize=9)

# Pressure graph    
    ax2.plot(date_met, pressure, color="red", label ="Absolute Pressure MET")
    ax2.plot(date_met_2, abs_pressure, color="blue", label ="Absolute Pressure")
    ax2.plot(date_time, barometer, color="black", label ="Barometer")
    ax2.plot(Sauda_tider, Sauda_press, color="green", label = "Sauda Pressure")
    ax2.plot(Sirdal_tider, Sirdal_press, color="orange", label = "Sirdal Pressure")

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))  
    ax2.set_xlabel('Dates')
    ax2.set_ylabel('Pressure')
    ax2.set_ylim(1000,1025)
    ax2.set_title('Pressure/Date graph')
    ax2.legend()

# Vis plottet
    plt.tight_layout()
    plt.show()

plot_graphs() #Kallar på funksjonen for å plotte temperaturdata.