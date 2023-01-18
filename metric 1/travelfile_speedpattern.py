
def func(vehicle,sp,vehicle_path,move,platform):
    df_list = []
    list_hr = []
    list_road = []
    # for jj in range(0,2):
    for jj in range(0,round(len(sp))):
        df = sp.loc[sp.index==jj]
        TravelTime = float(df['duration'])
        # if TravelTime > 40:
        #     continue
        if TravelTime < 2:
            continue
       # split 'date' & 'start_time' & 'end_time' of (marginal.csv) file
        df['Dates'] = pd.to_datetime(df['first_time']).dt.date
        s = pd.to_datetime(df['last_time']).dt.date
        if df['Dates'].iloc[0]!=s.iloc[0]:
            continue
        df['HrMin_start'] = pd.to_datetime(df['first_time']).dt.strftime('%H:%M')
        df['HrMin_end'] = pd.to_datetime(df['last_time']).dt.strftime('%H:%M')

        # Open (matched_index.csv) file that matches the date of current sp trip
        str_date = str(df['Dates'].iloc[0])
        matchedroadID_file = [str(f) for f in os.listdir(vehicle_path) if 
                              re.match(rf'.*{re.escape(str_date)}.*_indexes', f)]
        
        # for some days there is no file. Ignore them
        if bool(matchedroadID_file):
            # full_path_ID = vehicle_path+'\\'+matchedroadID_file[0]
            # df_id = pd.read_csv(full_path_ID)

            # Open (edges_all.csv) file that matches the date of current sp trip
            matchedroadall_file = [str(f) for f in os.listdir(vehicle_path) if 
                                   re.match(rf'.*{re.escape(str_date)}.*_all', f)]
            full_path_all = vehicle_path+'\\'+matchedroadall_file[0]
            df_all = pd.read_csv(full_path_all)
            df_all['HrMin'] = pd.to_datetime(df_all['datetime']).dt.strftime('%H:%M')
            # match start time of an sp trip
            try:
                first_index = df_all[df_all['HrMin'] == df['HrMin_start'].iloc[0]].index[0]
            except IndexError:
                continue           
            # match end_time of an sp trip with time of (edges_all.csv) file
            last_in = df_all[df_all['HrMin'] == df['HrMin_end'].iloc[0]].index
            try:
                last_index = last_in[-1]
            except IndexError:
                continue
            # last_index = last_in[last_in > first_index]
            # extract the sp trip part from (edges_all.csv)
            df_specific = df_all[(df_all.index >= first_index) & (df_all.index <= last_index)]
            EdgeIndex_unique = df_specific['EdgeIndex'].unique()
            last_edge = EdgeIndex_unique[-1]
            first_edge = EdgeIndex_unique[0]
            # required for reproducing Poulton's paper using instant speed
            df_specific = adsp.add_speedcol(df_specific,vehicle,platform,last_edge,first_edge)
            try:
                hr=df_specific['hr'].iloc[0]
            except IndexError:
                continue
            dff = pd.DataFrame({'move':move, 'vehicle':platform,
             'hour':hr,'mean_speed':df_specific['speed'].mean()}, index=[0])
            df_list.append(dff)
            list_hr.append(hr)
            list_road.append(df_specific['Highway'].unique().tolist())
    list_road = [item for sublist in list_road for item in sublist]
    df_hr = pd.DataFrame({'list_hr':list_hr}) # required to find the contribution of each hour_of_day in all trips
    df_road = pd.DataFrame({'road_type':list_road}) # required to find the contribution of each road_type in all trips
    df = pd.concat(df_list , axis=0, ignore_index = True) 
    return df , df_hr, df_road

import pandas as pd
import add_speed as adsp
import re
import os
import pandas as pd
import add_speed as adsp
