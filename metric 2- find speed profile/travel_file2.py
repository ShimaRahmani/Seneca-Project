
def func(sp,vehicle_path):
# Function of this code: finding the right chunck of (edges_all.csv)&(matched_index.csv) describing an sp trip
# Inputs: (marginal.csv), list of cleansed moves, dir of map-matched files
# Output: a dataframe of sp trips containing columns: each road segment's
#  1. edge_index, 2.OSM_id, 3. type, 4.traveled time, 5.length, 6.calculated speed (speed = length/duration)
    appended_new_df = []
    for jj in range(0,round(0.8*len(sp))):
        # match the indeces of filtered movements
        df = sp.loc[sp.index==jj]
        TravelTime = float(df['duration'])
        if TravelTime > 40:
            continue
        if TravelTime < 2:
            continue
        # MISSION GETS STARTED HERE;
        # 1. match start_time of an sp trip with time of (edge_all.csv) file
        # 2. match end_time of an sp trip with time of (edges_all.csv) file
        # 3. get the unique IDs for use in finding corresponding chunck in (matched_index.csv) file
        # 4. find chunck of (matched_index.csv) that matches the current sp trip
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
            full_path_ID = vehicle_path+'\\'+matchedroadID_file[0]
            df_id = pd.read_csv(full_path_ID)

            # Open (edges_all.csv) file that matches the date of current sp trip
            matchedroadall_file = [str(f) for f in os.listdir(vehicle_path) if 
                                   re.match(rf'.*{re.escape(str_date)}.*_all', f)]
            full_path_all = vehicle_path+'\\'+matchedroadall_file[0]
            df_all = pd.read_csv(full_path_all)

            df_all['HrMin'] = pd.to_datetime(df_all['datetime']).dt.strftime('%H:%M')
            first_index = df_all[df_all['HrMin'] == df['HrMin_start'].iloc[0]].index[0]
            last_in = df_all[df_all['HrMin'] == df['HrMin_end'].iloc[0]].index
            last_index = last_in[-1]
            df_specific = df_all[(df_all.index >= first_index) & (df_all.index <= last_index)]
            EdgeIndex_unique1 = df_specific['EdgeIndex'].unique()
            df_matched = getsp.find_chunck(df_specific, df_id, EdgeIndex_unique1)
            if df_matched is None:
                continue
            EdgeIndex_unique = df_matched['Index'].unique()
            if len(EdgeIndex_unique) < 2:
                continue
            # create a new df for sp involving road type, speed per road seg
            new_df = speed.calc_speed(df_specific, df_matched)
            # store all new interesting dataframes (df_new & df_sp_EdgeID) in a list
            appended_new_df.append(new_df)
    All_SPs = pd.concat(appended_new_df, axis=0, ignore_index = True)
    return All_SPs


import re
import os
import pandas as pd
import SPpath_finder as getsp
import speed_file as speed

