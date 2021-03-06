
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import csv
import pandas as pd
import xarray
import time

dates_debut = [1981, 1984, 1987, 1990, 1993, 1996, 1999, 2002, 2005, 2008, 2011, 2014, 2017]
dates_fin = [x+2 for x in dates_debut]

#region IMPORT DES DONNEES DEPUIS DOSSIER
#--------------------------------------------------------------------
# for k in range(len(dates_debut)):
for k in dates_debut:

    url = 'C:/Users/Florence/Documents/IRD/VIA/Data_ERA5-Land/ERA5-LAND_' + str(dates_debut[k]) + '-'\
         + str(dates_fin[k]) + '.nc'  # path to netcdf file
    ds = nc.Dataset(url) # read as netcdf dataset


    #endregion -----------------------------------------
    #region CHOIX DU BV
    #---------------------------------------------------

    decoupe_BV = pd.read_csv('suface_zones_bv1.csv', header=0)
    zones = decoupe_BV['fichier'].tolist()
    surfaces = decoupe_BV['area'].tolist()
    surface_tot = sum(surfaces)

    #endregion -----------------------------------------
    #region CREATION DE DATAFRAME JOURNALIERS
    #---------------------------------------------------
    total_precipitation = ds['tp']
    potential_evaporation = ds['pev']
    skin_temperature = ds['skt']
    # time = ds['time']
    n_jour = int(len(total_precipitation) / 24)

    dataset_daily_mm = pd.DataFrame({'P' : [0.] * n_jour,
                                  'T' : [0.] * n_jour,
                                  'E' : [0.] * n_jour,
                                  })

    print("import " + str(time.process_time())) # environ 3 sec, à raccourcir
    index = 0
    while index<len(zones):
        z = zones[index]
        i, j = int(z.split(sep="_")[0]), int(z.split(sep="_")[1])
        surface_zone = surfaces[index]
        print("import_zones " + str(time.process_time()))
        # PASSAGE PLUIES JOURNALIERES
        #---------------------------------------------------

        dataset_daily_mm['P'] = pd.Series(sum(total_precipitation[jour*24+h][i][j] for h in range(23))* surface_zone/(surface_tot) * 1000 for jour in range(n_jour))

        #region version lente
        # TP_jour = 0 #initialisation somme
        # for jour in range(int(len(total_precipitation)/24)) :
        #     for h in range(24):
        #         if type(total_precipitation[jour*24+h][i][j]) is np.float64 :
        #             TP_jour += total_precipitation[jour*24+h][i][j]
        #     #ponderation par zone et conversion en mm
        #     dataset_daily_mm['P'][jour] += TP_jour * surface_zone/(surface_tot) * 1000
        #
        #     #remise des compteurs à zero pour le jour suivant
        # endregion    TP_jour = 0
        print("TP" + str(time.process_time()))


        # PASSAGE EVAPOTRANSPIRATIONS JOURNALIERES
        #---------------------------------------------------
        dataset_daily_mm['E'] = pd.Series(
            sum(potential_evaporation[jour * 24 + h][i][j] for h in range(23)) * surface_zone / (surface_tot) /24 for
            jour in range(n_jour))

        #region version lente
    #     PE_jour = 0  # initialisation somme
    #     for jour in range(int(len(potential_evaporation) / 24)):
    #         for h in range(24):
    #             if type(potential_evaporation[jour * 24 + h][i][j]) is np.float64:
    #                 PE_jour += potential_evaporation[jour * 24 + h][i][j]
    #
    #         # ponderation par zone et moyennage journalier
    #         dataset_daily_mm['E'][jour] += PE_jour * (surface_zone / surface_tot) / 24
    #         # remise des compteurs à zero pour le jour suivant
    #         PE_jour = 0
    # endregion
        print("PE" + str(time.process_time()))


        # PASSAGE TEMPERATURE JOURNALIERES
        #---------------------------------------------------
        dataset_daily_mm['T'] = pd.Series(
            (sum(skin_temperature[jour * 24 + h][i][j] for h in range(23)) *
                surface_zone / (surface_tot) / 24) for jour in range(n_jour))
    #region version lente
    #     h = 0  # compteur d'heure
    #     SKT_jour = 0  # initialisation somme
    #     for jour in range(int(len(skin_temperature) / 24)):
    #         for h in range(24):
    #             if type(skin_temperature[jour * 24 + h][i][j]) is np.float64:
    #                 SKT_jour += skin_temperature[jour * 24 + h][i][j]
    #         # ponderation par zone, moyennage journalier, conversion en degrés Celsius
    #         dataset_daily_mm['T'][jour] += SKT_jour * surface_zone / (surface_tot) / 24 - 273.15
    #         # remise des compteurs à zero pour le jour suivant
    #         SKT_jour = 0
    # endregion
        print("SKT" + str(time.process_time()))
        index += 1

    plt.subplot(3, 1, 1)
    plt.plot([i for i in range(len(dataset_daily_mm['P']))], dataset_daily_mm['P'])
    plt.subplot(3, 1, 2)
    plt.plot([i for i in range(len(dataset_daily_mm['E']))], dataset_daily_mm['E'])
    plt.subplot(3, 1, 3)
    plt.plot([i for i in range(len(dataset_daily_mm['T']))], dataset_daily_mm['T'])
    plt.show()

    # filewriter = csv.writer(csvfile, delimiter=';')
    # # filewriter.writerow(['T'])
    # # for x in SKT_BV:
    # #     filewriter.writerow([x])


#
# with open('C:/Users/Florence/Documents/IRD/VIA/6_Code/GR4JCemaneige_light/GR4JCemaneigeLight/ET.csv', 'w',
#           newline='') as csvfile:
#     filewriter.writerow(['E'])
#     for x in PE_BV:
#         filewriter.writerow([x])
#     #
#     # filewriter.writerow(['P'])
#     # for x in TP_BV:
#     #      filewriter.writerow([x])



#region export des données brutes en csv
#    lat = 7
#     lon = 11
#for i in range(lat):
#     for j in range(lon):
# precip= [[total_precip[k][i][j]] for k in range(len(total_precip))]
# with open('C:/Users/Florence/Documents/IRD/VIA/Data_ERA5-Land/potential_evaporation'
#           '/ERA5-LAND_' + str(dates_debut[k]) + '-' + str(dates_fin[k]) + '_'  + str(i) +
#           '_' + str(j)+'.csv', 'w', newline='') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=';')
#     filewriter.writerow(['total_precip'])
#     for x in precip:
#         filewriter.writerow(x)

# pe = [[potential_evaporation[k][i][j]] for k in range(len(potential_evaporation))]
# with open('C:/Users/Florence/Documents/IRD/VIA/Data_ERA5-Land/potential_evaporation'
#           '/ERA5-LAND_' + str(dates_debut[k]) + '-' + str(dates_fin[k]) + '_' + str(i) +
#           '_' + str(j) + '.csv', 'w', newline='') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=';')
#     filewriter.writerow(['potential_evaporation'])
#     for x in pe:
#         filewriter.writerow(x)

# skt = [[skin_temp[k][i][j]] for k in range(len(skin_temp))]
# with open('C:/Users/Florence/Documents/IRD/VIA/Data_ERA5-Land/skin_temp'
#           '/ERA5-LAND_' + str(dates_debut[k]) + '-' + str(dates_fin[k]) + '_' + str(i) +
#           '_' + str(j) + '.csv', 'w', newline='') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=';')
#     filewriter.writerow(['skin_temp'])
#     for x in skt:
#         filewriter.writerow(x)
#endregion

# plt.plot(precip_1)
# plt.show()
# print(max(precip_1))


#
# prcp = ds['prcp'][:]  # get data for variable
#
# print(prcp[0, 4000:4005, 4000:4005])  # print slice of data
#




# import cdsapi
# import pygrib
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import cartopy.crs as ccrs
# # from mpl_toolkits.basemap import Basemap
# # from mpl_toolkits.basemap import shiftgrid
# import numpy as np
# #
# # c = cdsapi.Client()
# #
# # c.retrieve(
# #     'reanalysis-era5-land',
# #     {
# #         'variable': ['potential_evaporation', '2m_temperature',
# #                      'skin_temperature', 'soil_temperature_level_1', 'total_precipitation'],
# #         'year': [
# #             '1981', '1982', '1983',
# #             '1984', '1985', '1986',
# #             '1987', '1988', '1989',
# #             '1990', '1991', '1992',
# #             '1993', '1994', '1995',
# #             '1996', '1997', '1998',
# #             '1999', '2000', '2001',
# #             '2002', '2003', '2004',
# #             '2005', '2006', '2007',
# #             '2008', '2009', '2010',
# #             '2011', '2012', '2013',
# #             '2014', '2015', '2016',
# #             '2017', '2018', '2019',
# #         ],
# #         'month': [
# #             '01', '02', '03',
# #             '04', '05', '06',
# #             '07', '08', '09',
# #             '10', '11', '12',
# #         ],
# #         'day': [
# #             '01', '02', '03',
# #             '04', '05', '06',
# #             '07', '08', '09',
# #             '10', '11', '12',
# #             '13', '14', '15',
# #             '16', '17', '18',
# #             '19', '20', '21',
# #             '22', '23', '24',
# #             '25', '26', '27',
# #             '28', '29', '30',
# #             '31',
# #         ],
# #         'time': [
# #             '00:00', '06:00', '12:00',
# #             '18:00',
# #         ],
# #         'area': [
# #             31.3, -8, 31,
# #             -7.8,
# #         ],
# #         'format': 'grib',
# #     },
# #     'download.grib')
#
# plt.figure(figsize=(12, 8))
#
# grib = 'test.grib'  # Set the file name of your input GRIB file
# grbs = pygrib.open(grib)
#
# grb = grbs.select()[0]
# data = grb.values
#
# # need to shift data grid longitudes from (0..360) to (-180..180)
# lons = np.linspace(float(grb['longitudeOfFirstGridPointInDegrees']), \
#                    float(grb['longitudeOfLastGridPointInDegrees']), int(grb['Ni']))
# lats = np.linspace(float(grb['latitudeOfFirstGridPointInDegrees']), \
#                    float(grb['latitudeOfLastGridPointInDegrees']), int(grb['Nj']))
# data, lons = shiftgrid(180., data, lons, start=False)
# grid_lon, grid_lat = np.meshgrid(lons, lats)  # regularly spaced 2D grid
#
# m = Basemap(projection='cyl', llcrnrlon=-180, \
#             urcrnrlon=180., llcrnrlat=lats.min(), urcrnrlat=lats.max(), \
#             resolution='c')
#
# x, y = m(grid_lon, grid_lat)
#
# cs = m.pcolormesh(x, y, data, shading='flat', cmap=plt.cm.gist_stern_r)
#
# m.drawcoastlines()
# m.drawmapboundary()
# m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
# m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])
#
# plt.colorbar(cs, orientation='vertical', shrink=0.5)
# plt.title('CAMS AOD forecast')  # Set the name of the variable to plot
# plt.savefig(grib + '.png')  # Set the output file name