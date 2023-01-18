def add_speedcol(df_specific,vehicle,Geometry_data_path,midpoint_df):

    vehicle['minute'] = vehicle['minute'].astype(int)
    df_specific['Min'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%M')
    df_specific['Min'] = df_specific['Min'].astype(int)
    df_specific['hr'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
    df_specific['hr'] = df_specific['hr'].astype(int)
    # vehicle['Date'] = pd.to_datetime(vehicle['Date_str']).dt.date
    df_specific['Date'] = pd.to_datetime(df_specific['datetime'], errors = 'coerce')
    # df_specific['Date'] = df_specific['Date'].dt.strftime('%m/%d/%Y')
    a = df_specific['Date'].dt.strftime('%Y-%m-%d')
    df_specific['Date'] = a

    # if df_specific['Date'].iloc[0][0:1]=='0':
    #     mon=df_specific['Date'].iloc[0][1]
    # else: 
    #     mon=df_specific['Date'].iloc[0][0:2]
    # if df_specific['Date'].iloc[0][3]=='0':
    #     da = df_specific['Date'].iloc[0][4]
    # else:
    #     da = df_specific['Date'].iloc[0][3:5]
    # dat = mon+'/'+da+'/'+df_specific['Date'].iloc[0][6:10]
    # df_specific['Date'] = dat
    df_specific['speed']=''
    # df_specific['Date'] = pd.to_datetime(df_specific['datetime']).dt.date
    # df_specific.latitude.round(5)
    # df_specific.longitude.round(5)
    # vehicle.LAT.round(5)
    # vehicle.LON.round(5)
    vehicle=vehicle.round(5)
    df_specific=df_specific.round(5)
    df3 = pd.merge(vehicle,df_specific, left_on=["LON","LAT","date"], right_on=['longitude','latitude','Date'])
    for indx, row in df3.iterrows():
        a=df_specific.loc[df_specific['longitude']==row['LON']].index[0]
        df_specific.loc[a,'speed']=row['Speed']

    speed_numer = []
    for i in df_specific['speed'].values:
        if (type(i)==str) & (i != ''):
            numer = re.findall(r'\d*', i)[0]
            numer = float(numer)*(10/36)
            speed_numer.append(numer)
        else:
            speed_numer.append(np.nan)
    df_specific['speed'] = speed_numer

    # df_specific.index = df3.index
    # df_specific['speed'] = df3['Speed']

    df_specific = reject_points(df_specific,midpoint_df) ################################3


    return df_specific

def reject_points(df_specific,midpoint_df):

    a=df_specific.merge(midpoint_df, left_on='EdgeIndex', right_on='EdgeIndex', how='left')

    for i, r in a.iterrows():

        # compute box bounds in lat/lon:
        your_meters = 250
        earth = 6378.137 # radius of earth in km
        pi = math.pi
        m = (1 / ((2 * pi / 360) * earth)) / 1000 # /1 meter in degree
        lat_upper_bnd = r['lat'] + (your_meters * m)
        lat_lower_bnd = r['lat'] - (your_meters * m)
        lon_upper_bnd = r['lon'] + (your_meters * m)/ math.cos(r['lat'] * (pi / 180))
        lon_lower_bnd = r['lon'] - (your_meters * m)/ math.cos(r['lat'] * (pi / 180))
        lat = r['latitude']
        lon = r['longitude']
        if lat>lat_upper_bnd or lat<lat_lower_bnd or lon>lon_upper_bnd or lon<lon_lower_bnd:
            r['speed'] = np.nan
    # print('number of nan_speed: ',a['speed'].isnull().sum())
    b = a.iloc[:, :21]
    return b

import pandas as pd
import re
import numpy as np
import math
