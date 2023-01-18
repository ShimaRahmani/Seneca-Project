def func(sp,vehicle_path,plate):

    dflist = []
    # for jj in range(0,11):
    for jj in range(0,len(sp)):
        # tripdf = pd.DataFrame([{'travel time':[],'distance': [], 'hour of day':[], 'living_street':0,
        # 'motorway':0, 'motorway_link':0,'primary':0, 'primary_link':0, 'residential':0, 'road':0,
        # 'secondary':0, 'secondary_link':0,'service':0, 'tertiary':0, 'track':0, 'trunk':0,
        # 'trunk_link':0, 'unclassified':0, 'others':0}])
        df = sp.loc[sp.index==jj]

        TravelTime = float(df['duration']) #min
        Distance = (df['length_metres'])/1000 #km

        if TravelTime > 40:
            continue
        if TravelTime < 2:
            continue

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
        if bool(matchedroadID_file)==False:
            continue

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
        df_matched = chunk.find_chunk(df_specific, df_id, EdgeIndex_unique1)             
        if df_matched is None:
            continue
        EdgeIndex_unique = df_matched['Index'].unique()
        if len(EdgeIndex_unique) < 2:
            continue
        EdgeIndex_unique = df_matched['Index'].unique()
        new_df = t.calc_time(df_specific)
        #************** Total route travel time ******************
        sumtime_traversal = new_df['TimeDiff0'].iloc[:].sum() 
        #**********************************************
        df_specific['hour'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
        #************** hour of day *************
        hr = int(df_specific['hour'].iloc[0]) # hour of day
        #***************** Total route distance ********************
        distance = df_matched['Distance'].sum()
        #**********************************************************
        a = df_matched.groupby(['Highway'])['Distance'].sum().reset_index().sort_values('Distance',ascending=False)
        a['distance ratio'] = a['Distance']/distance
        li = [i for i in a['Highway']]
        li2 = [i for i in a['distance ratio']]
        if 6-len(li) > 0:
            lis = np.append(li, np.repeat(np.nan, 6-len(li)))
            lis2 = np.append(li2, np.repeat(np.nan, 6-len(li2)))
        elif 6-len(li) == 0:
            lis = li
            lis2 = li2
        else:
            # print('################\n###############\n#############')
            lis = li[0:6]
            lis2 = li2[0:6]
        
        tripdf = pd.DataFrame([{'travel time':sumtime_traversal,
         'distance': distance, 'hour of day':hr, '1st ranked':[],
         '2nd ranked':[], '3rd ranked':[], '4d ranked':[], '5th ranked':[], '6th ranked':[],
         '1st dist':[],'2nd dist':[], '3rd dist':[], '4rd dist':[], '5th dist':[], '6th dist':[]}])
        tripdf.loc[:,3:9]=lis
        tripdf.loc[:,9:]=lis2

        tripdf['travel time'] = sumtime_traversal
        tripdf['distance'] = distance
        tripdf['hour of day'] = hr
        # a = a[['Highway','Distance']].reset_index(drop=True)
        # for ind,row in a.iterrows():
        #     if any(tripdf.columns == row['Highway']):
        #         tripdf.loc[0,tripdf.columns == row['Highway']]= row['Distance']
        #     else:
        #         tripdf['others'] = row['Distance']

        dflist.append(tripdf)
    all_tripdf = pd.concat(dflist, axis=0, ignore_index=True)
    
    return all_tripdf

import re
import os
import math
import pandas as pd
import numpy as np
import SPpath_finder as chunk
import speed_file as t