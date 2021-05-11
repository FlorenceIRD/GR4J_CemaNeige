
import matplotlib.pyplot as plt
import netCDF4 as nc
import csv
import numpy as np
import pandas as pd


# dates_debut = [1981, 1984, 1987, 1990, 1993, 1996, 1999, 2002, 2005, 2008, 2011, 2014, 2017]
# dates_fin = [x+2 for x in dates_debut]
dates_debut = [1990]
dates_fin = [1992]
decoupe_BV = pd.read_csv('suface_zones_bv1.csv', header=0)
zones = decoupe_BV['fichier'].tolist()
surfaces=  decoupe_BV['area'].tolist()

TP_BV = []
PE_BV = []
SKT_BV = []

for annees in range(len(dates_debut)): #decompte des années
    fn = 'C:/Users/Florence/Documents/IRD/VIA/Data_ERA5-Land/ERA5-LAND_' + str(dates_debut[annees]) + '-'\
         + str(dates_fin[annees]) + '.nc'  # path to netcdf file
    ds = nc.Dataset(fn)  # read as netcdf dataset

    time = ds['time']
    total_precip = ds['tp']
    potential_evaporation = ds['pev']
    skin_temp = ds['skt']
    TP_BV_annees = [0.] * int(len(total_precip)/24)
    PE_BV_annees = [0.] * int(len(potential_evaporation)/24)
    SKT_BV_annees = [0.] * int((len(skin_temp))/24)

    surface_tot = sum(surfaces)
    for index in range(len(zones)):
        z = zones[index]
        i, j = int(z.split(sep="_")[0]), int(z.split(sep="_")[1])
        surface_zone = surfaces[index]

        h=0 #compteur d'heure
        TP_jour = 0 #initialisation somme
        TP_zone = []
        for k in range(len(total_precip)) :
            if type(total_precip[k][i][j]) is np.float64 :
                TP_jour += total_precip[k][i][j]

            h+=1
            if h==24 :
                TP_zone.append(TP_jour*surface_zone/(24*surface_tot))
                h=0

        h = 0  # compteur d'heure
        PE_jour = 0  # initialisation somme
        PE_zone = []

        for k in range(len(potential_evaporation)) :
            if type(potential_evaporation[k][i][j]) is np.float64:
                PE_jour += potential_evaporation[k][i][j]
            h+=1
            if h==24 :
                PE_zone.append(PE_jour*surface_zone/surface_tot)
                h=0

        h = 0  # compteur d'heure
        SKT_jour = 0  # initialisation somme
        SKT_zone = []

        for k in range(len(skin_temp)):
            if type(skin_temp[k][i][j]) is np.float64 :
                SKT_jour += skin_temp[k][i][j]
            h += 1
            if h == 24:
                SKT_zone.append(SKT_jour * surface_zone/(24*surface_tot))
                h = 0

        TP_BV_annees = [TP_zone[i] + TP_BV[i] for i in range(len(TP_BV))]
        PE_BV_annees= [PE_zone[i] + PE_BV[i] for i in range(len(PE_BV))]
        SKT_BV_annees= [SKT_zone[i] + SKT_BV[i] for i in range(len(SKT_BV))]


    TP_BV.append(TP_BV_annees)
    PE_BV.append(PE_BV_annees)
    SKT_BV.append(SKT_BV_annees)



    with open('C:/Users\Florence\Documents\IRD\VIA/'
              '6_Code\GR4JCemaneige_light\GR4JCemaneigeLight\Basin1.csv') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['T'])
        for x in SKT_BV:
            filewriter.writerow(x)

        filewriter.writerow(['E'])
        for x in PE_BV:
            filewriter.writerow(x)

        filewriter.writerow(['P'])
        for x in TP_BV:
            filewriter.writerow(x)

    print(0)

