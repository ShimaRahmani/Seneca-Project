
def func(sp,vehicle_path,local_path):
    Edge_list = []
    Number_added_edges = []

    prepared_df_list = []
    # for jj in range(0,5):
    
    for jj in range(0,len(sp)):
        
    # for jj in range(0,round(0.8*len(filtered_move))):
        df = sp.loc[sp.index==jj]
        
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
            # find the unique road IDs
            EdgeIndex_unique = df_specific['EdgeIndex'].unique()
            last_edge = EdgeIndex_unique[:-1]
            df_matched = getsp.find_chunck(df_specific, df_id, EdgeIndex_unique)

            if df_matched is None:
                continue

            EdgeIndex_unique1 = df_matched['Index'].unique()

            Edge_list.append(EdgeIndex_unique1)
            # dataframe = pd.concat(Edge_list, axis=0, ignore_index=True)
            # Data_for_one_vehicle = pd.concat(Edge_list, axis=0, ignore_index = True)
    # dataframe = pd.DataFrame({'trip No':trip_list,'Edges unique':Edge_list})
            diff = len(df_matched['Index'].unique()) - len(df_specific['EdgeIndex'].unique())
            Number_added_edges.append(diff)
    return Edge_list, Number_added_edges


import re
import os
import pandas as pd
import SPpath_finder as getsp
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns