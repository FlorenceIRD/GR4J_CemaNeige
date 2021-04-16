

import netCDF4 as nc

fn = 'C:/Users/Florence/Documents/IRD/VIA/1.nc'  # path to netcdf file

ds = nc.Dataset(fn)  # read as netcdf dataset

la

#
# ds['prcp']
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