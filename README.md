The file convert_met_data.py converts the data from time.csv.txt, met.csv.txt, temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt to similar formats, in:
Time_data: Format [Y,M,D,h,m,s,bar-press, abs-press, temp], -1 if no bar-press: [2021, 6, 11, 14, 23, 0, 1010.3, 1004.52, 17.18], [2021, 6, 11, 14, 23, 10, -1, 1004.78, 17.1]
Sola_data, Sauda_data, Sirdal_data: Format [Y,M,D,h,m, temp, bar-press]: [2021, 6, 11, 1, 0, 16.1, 1013.7]

The file Combined_graphings_v2.py is updated with a, d and e from Øving 10, and the lists Sauda_data and Sirdal_data are cut down to Sola_data size.
