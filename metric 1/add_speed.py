def add_speedcol(df_specific,vehicle,platform,last_edge,first_edge):
    df_specific = df_specific.drop(df_specific[df_specific['EdgeIndex']==last_edge].index)
    df_specific = df_specific.drop(df_specific[df_specific['EdgeIndex']==first_edge].index)
    vehicle['minute'] = vehicle['minute'].astype(int)
    df_specific['Min'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%M')
    df_specific['Min'] = df_specific['Min'].astype(int)
    df_specific['hr'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
    df_specific['hr'] = df_specific['hr'].astype(int)
    # vehicle['Date'] = pd.to_datetime(vehicle['Date_str']).dt.date
    df_specific['Date'] = pd.to_datetime(df_specific['datetime'], errors = 'coerce')
    # df_specific['Date'] = df_specific['Date'].dt.strftime('%m/%d/%Y')
    if vehicle['date'].iloc[0][4]=='-':
        a = df_specific['Date'].dt.strftime('%Y-%m-%d')
    else:
        a = df_specific['Date'].dt.strftime('%#m/%#d/%Y')

    df_specific['Date'] = a

    df_specific['speed']=''

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
    df_speci = df_specific[df_specific['speed'].notna()]

    return df_speci


import pandas as pd
import re
import numpy as np
import math
