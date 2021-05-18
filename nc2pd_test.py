# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:45:55 2021

@author: Michel Le Page - CESBIO-IRD
"""

# read a netcdf
import xarray

url = "G:\\S1S2\\for_git\\data\\irrigation_plus\\netcdf\\Input netcdf\\netcdf_with_ndvi\\TEST_SITE_FRANCE_LOT_NEW_SSM_NDVI.nc"

ds = xarray.open_dataset(url)
df = ds.to_dataframe()
df_var = df.filter(regex=r'^Irrig', axis=1)     # filter variables on the variable_type
df_plot=df.filter(regex=r'Lot-495-2016$',axis=1)    # filter variables on the plot name
df_list=df.filter(['ET_Lot-495-2016','Irrigation_Lot-495-2016'])    # filter variables on a list

# read a csv

import pandas as pd
asset_name = "G:\\S1S2\\for_git\\data\\irrigation_plus\\data_sat\\Ehsan\\Eur_Gr_It_Fr_estimated.csv"   
df_csv = pd.read_csv(asset_name)
df_csv["date"] = pd.to_datetime(df_csv["date"])
df_csv_list=df_csv.filter(['M(VH_dB)','M(VV_dB)', 'date', 'label','orbit', 'M(NDVI)', 'soil_moisture'])    # filter variables on a list
df_csv_list = df_csv_list.sort_values(["date"]).reset_index(drop=True)          
df_csv_list.index = df_csv_list['date']
df_csv_list = df_csv_list.drop(labels=['date'],axis=1)

# selections
df_csv_loc = df_csv_list.loc[df_csv_list['label'] == 0]    # select a plot
df_csv_orbit = df_csv_loc.loc[df_csv_loc['orbit'] == 'ASC']    # select on orbit
df_csv_backscat = df_csv_loc.loc[df_csv_loc['M(VV_dB)'] > -15]    # select on VV backscattering
df_csv_dates = df_csv_loc["2019-1-1":"2019-12-31"]          # select on date

