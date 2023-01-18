
def func(marginal_df,weightdf,filtered_move,vehicle_path,plate):
    excluded_trips = []
    no_path_trips = []
    error_list=[]
    similarity_list=[]
    total_test_data = len(filtered_move) - round(0.8*len(filtered_move))
    coverability = pd.DataFrame({'Plate':[],'movement_id':[],'total_test_data':[],'uncovered_edges(%)':[]})
    # for jj in range(944,945):
    # for jj in range(0,len(filtered_move)):
    for jj in range(round(0.8*len(filtered_move)),len(filtered_move)):
        # match the indeces of filtered movements
        df = marginal_df.loc[marginal_df['movement_id']==filtered_move[jj]]
        # Filtering1: exclude trips longer than 40 min
        # if df['duration'].iloc[0] > 40:
        #    excluded_trips.append(filtered_move[jj]) 
        #    continue    
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
            #________________check coverability_________________#
            tot = len(EdgeIndex_unique)
            in_avail = sum(i in weightdf['EdgeID'].values for i in EdgeIndex_unique)
            ratio = in_avail/tot
            if ratio < 0.90:
                coverability = coverability.append({'Plate':plate,'movement_id':filtered_move[jj],
                'total_test_data':total_test_data,'uncovered_edges(%)':1-ratio}, ignore_index=True)
                continue
            #_____________________weight_df_____________________#
            df_specific['hour'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
            hr = int(df_specific['hour'].iloc[0])    
            time_list = []
            for ind, row in weightdf.iterrows():
                velocity = float(weightdf['weight'].iloc[ind][hr])
                traversetime = row['Length(m)(poly)']/velocity
                time_list.append(traversetime)
            # define the traversal time of an edge at a specific time as weight (instead of velocity weight)
            weightdf['weight(s)'] = time_list
            new_weightdf = weightdf[['EdgeID','from_node','to_node','weight(s)']]
            #_____________________network_______________________#
            # Extract required data from testing trip: duration, source_node, target_node, hour
            duration = df['duration'].iloc[0]*60
            for i in EdgeIndex_unique:
                if i in weightdf['EdgeID'].values:
                    start = i
                    break
            if EdgeIndex_unique[-2] not in weightdf['EdgeID'].values:
                a = [i in weightdf['EdgeID'].values for i in EdgeIndex_unique]
                output = [idx for idx, element in enumerate(a) if element==False][0]
                end = EdgeIndex_unique[output-1]
            else:
                end = EdgeIndex_unique[-2]
            source = weightdf.loc[weightdf['EdgeID'] == start, 'from_node'].iloc[0]
            try:
                target = weightdf.loc[weightdf['EdgeID'] == end, 'to_node'].iloc[0]
            except (ValueError,IndexError):
                continue
            output = net.mynetwork(source,target,new_weightdf,plate,filtered_move[jj],EdgeIndex_unique)

            if output is None:
                no_path_trips.append(filtered_move[jj])
                continue
            estimtime = output[0]
            path = output[1]
            #______________________similarity_________________________#
            node_list=[]
            for i in EdgeIndex_unique:
                try:
                    df = weightdf.loc[weightdf['EdgeID']==i]
                    node_list.extend([df['from_node'].iloc[0],df['to_node'].iloc[0]])
                except (TypeError, IndexError):
                    continue
            node_list_unique = list(set(node_list))
            path_unique = list(set(path))
            similarity = sum(i in node_list_unique for i in path)/len(path)
            #______________________time error_________________________#
            error = (duration - estimtime)/60
            error_list.append(error)
            similarity_list.append(similarity)
        
    return error_list, similarity_list, coverability, no_path_trips


import re
import os
import pandas as pd
import network as net
import SPpath_finder as getsp
import numpy as np
import matplotlib.pyplot as plt

