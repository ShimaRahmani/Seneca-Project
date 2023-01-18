
def func(marginal_df,filtered_move,vehicle_path,speed_profile):
# Function of this code: finding the right chunck of (edges_all.csv)&(matched_index.csv) describing an sp trip
# Inputs: (marginal.csv), list of cleansed moves, dir of map-matched files
# Output: a dataframe of sp trips containing columns: each road segment's
#  1. edge_index, 2.OSM_id, 3. type, 4.traveled time, 5.length, 6.calculated speed (speed = length/duration)

    appended_new_df = []
    appended_matched_id = []
    errortime_list = []
    matched_list = []

    # for jj in range(257,258):
    for jj in range(0,len(filtered_move)):
        print('#######################################')
        print('(marginal) sp trip: ', filtered_move[jj])
        print('#######################################')
        # match the indeces of filtered movements
        df = marginal_df.loc[marginal_df['movement_id']==filtered_move[jj]]

        # split 'date' & 'start_time' & 'end_time' of (marginal.csv) file
        df['Dates'] = pd.to_datetime(df['first_time']).dt.date
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

            # MISSION GETS STARTED HERE;
            # 1. match start_time of an sp trip with time of (edge_all.csv) file
            # 2. match end_time of an sp trip with time of (edges_all.csv) file
            # 3. get the unique IDs for use in finding corresponding chunck in (matched_index.csv) file
            # 4. find chunck of (matched_index.csv) that matches the current sp trip

            df_all['HrMin'] = pd.to_datetime(df_all['datetime']).dt.strftime('%H:%M')

            for index, row in df_all.iterrows():

                # match start time of an sp trip
                if row['HrMin'] == df['HrMin_start'].iloc[0]:
                    first_index = row['Index']

                    # match end_time of an sp trip with time of (edges_all.csv) file
                    for index, roww in df_all[df_all['Index']>=first_index].iterrows():

                        if roww['HrMin'] == df['HrMin_end'].iloc[0]:
                            last_index = roww['Index']
                            if last_index > first_index:
                                # extract the sp trip part from (edges_all.csv)
                                df_specific = df_all[(df_all['Index'] >= first_index) & (df_all['Index'] <= last_index)]
                                # find the unique road IDs
                                EdgeIndex_unique = df_specific['EdgeIndex'].unique()
                                # explore each chunck of (matched_index.csv) to find relevant sp trip
                                df_sp_EdgeID = getsp.find_chunck(df_specific, df_id, EdgeIndex_unique)

                                if df_sp_EdgeID is None:
                                    print('no chunck found for jj: ',jj)
                                    time.sleep(3) # Sleep for 3 seconds
                                    break

                                else:
                                    # create a new df for sp involving road type, speeper road seg
                                    new_df = sp.calc_speed(df_specific, df_sp_EdgeID)
                                    # store all new interesting dataframes (df_new & df_sp_EdgeID) in a list
                                    appended_new_df.append(new_df)
                                    appended_matched_id.append(df_sp_EdgeID)
                                    errortime, df_sp_EdgeID = go.errortime(df, df_sp_EdgeID,speed_profile)
                                    if errortime is None:
                                        break
                                    errortime_list.append(errortime)
                                    matched_list.append(df_sp_EdgeID)
                                    
                            else:
                                continue

                            #if row['HrMin'] == df['HrMin_end'].iloc[0]
                            break
                 #if row['HrMin'] == df['HrMin_start'].iloc[0]
                    break
        # if bool(matchedroadID_file)
        else:
            continue

    All_SPs = pd.concat(appended_new_df, axis=0, ignore_index = True)
    All_matched = pd.concat(matched_list, axis=0, ignore_index = True)

    return All_SPs, All_matched, errortime_list


import re
import os
import time
import pandas as pd
import SPpath_finder as getsp
import speed_file as sp
import metric2 as go
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns