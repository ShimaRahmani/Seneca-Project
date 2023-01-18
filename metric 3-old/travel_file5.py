
def func(marginal_df,filtered_move,finaldf,vehicle_path,plate,removed_trips):
    prepared_df_list = []
    error_time = []
    criticdf_append = []
    errordf_append = []
    removed_trips = removed_trips[removed_trips['plate']==plate]
    # for jj in range(0,10):
    # for jj in range(0,len(filtered_move)):
    for jj in range(0,round(0.8*len(filtered_move))):
        # print('#######################################')
        # print('(marginal) sp trip: ', filtered_move[jj])
        # print('trip numer: ',jj,'/',round(0.8*len(filtered_move)))
        # print('#######################################')
        if filtered_move[jj] in removed_trips['movement_id'].values:
            continue
        # match the indeces of filtered movements
        df = marginal_df.loc[marginal_df['movement_id']==filtered_move[jj]]
        # if df['duration'].iloc[0]>45:
        #     continue
        # get real travel time from marginal_file
        triptime = df['duration'].iloc[0] * 60
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
            # match start time of an sp trip
            first_index = df_all[df_all['HrMin'] == df['HrMin_start'].iloc[0]].index[0]
            # match end_time of an sp trip with time of (edges_all.csv) file
            last_in = df_all[df_all['HrMin'] == df['HrMin_end'].iloc[0]].index
            last_index = last_in[-1]
            # last_index = last_in[last_in > first_index]
            # extract the sp trip part from (edges_all.csv)
            df_specific = df_all[(df_all.index >= first_index) & (df_all.index <= last_index)]
            # aggregate traversal time of each edge
            sec_list = [0]
            df_specific['TimeDiff'].iloc[0] = 0
            for i in range(1,len(df_specific['TimeDiff'])):
                a = df_specific['TimeDiff'].iloc[i][10:15]
                sec = int(a[0:2])*60 + int(a[3:5]) 
                sec_list.append(sec)
            df_specific['TimeDiff0'] = sec_list
            df_specific['TimeDiff0'].iloc[0]=0
            # a seriese with edges and their corresponding traversal time
            edgetime = df_specific.groupby(['EdgeIndex'])['TimeDiff0'].sum()
            # find the unique road IDs
            df_specific['hour'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
            hr = int(df_specific['hour'].iloc[0])
            EdgeIndex_unique = df_specific['EdgeIndex'].unique()
            li = []
            critical = []
            flag_first = 0
            flag_last = 0
            for i in EdgeIndex_unique[:-1]:
                criticdf = pd.DataFrame({'plate':plate,'date':str_date,
                'movement_id':str(filtered_move[jj]),'edge':[],'is_first_edge':flag_first,'is_last_edge':flag_last,'real edge time':[],'estimate edge time':[],'time diff':[]})
           
                # match an edge of sequences of edges forming this trip
                row = finaldf[finaldf['EdgeID']==i]
                if i==EdgeIndex_unique[0]:
                    flag_first = 1
                else:
                    flag_first = 0                 
                if i==EdgeIndex_unique[-1]:
                    flag_last = 1
                else:
                    flag_last = 0
                try:
                    # get speed for specified hour
                    speed = float(row['weight'].iloc[0][hr])
                    # estimate travel time form speed weight burrowed from Poulton suggested method
                    estimtime = row['Length(m)(poly)'].iloc[0]/speed
                    li.append(estimtime)
                    # catch an edge causing criticality in time difference
                    diff = edgetime[row['EdgeID'].iloc[0]] - estimtime
                    if abs(diff) > 30:
                        criticdf = criticdf.append({
                        'plate':plate,
                        'date':str_date,
                        'movement_id':str(filtered_move[jj]), 
                        'edge':int(row['EdgeID'].iloc[0]),
                        'is_first_edge':flag_first,
                        'is_last_edge':flag_last,
                        'real edge time': edgetime[row['EdgeID'].iloc[0]],
                        'estimate edge time':estimtime,
                        'time diff':diff}, ignore_index = True)

                        criticdf_append.append(criticdf)
                except (TypeError, IndexError):
                    continue
            errordf =pd.DataFrame({'plate':plate,
                                'date':str_date,
                                'movement_id':str(filtered_move[jj]),
                                'estimated trip time(s)':[],
                                'real trip time(s)':[],
                                'errortime(min)':[]})
            estimatedtime = sum(li)
            timediff = triptime - estimatedtime
            timediff = timediff/60
            errordf = errordf.append({'plate':plate,
                    'date':str_date,
                    'movement_id':str(filtered_move[jj]),
                    'estimated trip time(s)':estimatedtime,
                    'real trip time(s)':triptime,
                    'errortime(min)':timediff}, ignore_index = True)
            errordf_append.append(errordf)
    ctiricaledges = pd.concat(criticdf_append, axis=0, ignore_index = True)
    errordf = pd.concat(errordf_append, axis=0, ignore_index = True)
    return errordf, ctiricaledges


import re
import os
import time
import pandas as pd
import SPpath_finder as getsp
import numpy as np
import add_speed as adsp
import matplotlib.pyplot as plt
import new_df as prep
# import seaborn as sns