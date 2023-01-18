def func(sp,vehicle_path):
    freq_list = []
    # for jj in range(0,round(0.5*len(sp))):
    for jj in range(0,round(1*len(sp))):

        df = sp.loc[sp.index==jj]

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
            df1 = df_specific.copy()
            sec_list = [0]
            df1['TimeDiff'].iloc[0] = 0
            for i in range(1,len(df1['TimeDiff'])):
                a = df1['TimeDiff'].iloc[i][10:15]
                sec = int(a[0:2])*60 + int(a[3:5]) 
                sec_list.append(sec)

            # prepared_df['Hour_of_Day'] = int(df1['datetime'].iloc[i+1][11:13])
            df1['TimeDiff0'] = sec_list
            df1['TimeDiff0'].iloc[0]=0
            li = df1['TimeDiff0'].to_list()
            li = li[1:]
            freq_list.append(li)
    flat = [item for sublist in freq_list for item in sublist]

    return flat
import pandas as pd
import re
import os
import numpy as np