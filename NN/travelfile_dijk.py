
def func(sp,weightdf,vehicle_path,plate):
    dflist = []
    # for jj in range(0,3):
    for jj in range(0,len(sp)):
        # match the indeces of filtered movements
        df = sp.loc[sp.index==jj]
        TravelTime = float(df['duration'])
        if TravelTime > 40:
            continue
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
            full_path_ID = vehicle_path+'\\'+matchedroadID_file[0]
            df_id = pd.read_csv(full_path_ID)
        else:
            continue

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
        df_matched = getsp.find_chunk(df_specific, df_id, EdgeIndex_unique1)

        if df_matched is None:
            continue
        
        EdgeIndex_unique = df_matched['Index'].unique()
        if len(EdgeIndex_unique) < 2:
            continue
        EdgeIndex_unique = df_matched['Index'].unique()
        new_df = t.calc_time(df_specific)
        y = new_df['TimeDiff0'].iloc[:].sum()
        #_____________________weight_df_____________________#
        df_specific['hour'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
        hr = int(df_specific['hour'].iloc[0])    
        time_list = []
        for ind, row in weightdf.iterrows():
            traversetime = row['weight'][hr]
            time_list.append(traversetime)
        # define the traversal time of an edge at a specific time as weight (instead of velocity weight)
        weightdf['weight(s)'] = time_list
        
        # _____________________network_______________________#
        # Extract required data from testing trip: duration, source_node, target_node, hour
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

        output = net.mynetwork(source,target,weightdf)

        if output is None:
            y_dijk1 = np.nan
            continue
        else:
            y_dijk1 = output[0]
            path_dijk = output[1]
            dijk_dist = output[2]

        # ______________________similarity_________________________#
        node_list1=[]
        for i in EdgeIndex_unique:
            try:
                df = weightdf.loc[weightdf['EdgeID']==i]
                node_list1.extend([df['from_node'].iloc[0],df['to_node'].iloc[0]])
            except (TypeError, IndexError):
                continue
        node_list_unique1 = list(set(node_list1))
        similarity = sum(i in node_list_unique1 for i in path_dijk)/len(node_list_unique1)
        sim = sum(i in node_list_unique1 for i in path_dijk)/len(path_dijk)
        #************** Total route travel time ******************
        sumtime_traversal = new_df['TimeDiff0'].iloc[:].sum() 
        #**********************************************
        df_specific['hour'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
        #************** hour of day *************
        hr = int(df_specific['hour'].iloc[0]) # hour of day
        #***************** Total route distance ********************
        distance = df_matched['Distance'].sum()
        #**********************************************************

        tripdf = pd.DataFrame([{'travel time':sumtime_traversal,'hour of day':hr,
         'distance': distance, 'est_dist': dijk_dist, 'similarity':similarity, 'similarity_dijk':sim}])


        dflist.append(tripdf)
    all_tripdf = pd.concat(dflist, axis=0, ignore_index=True)
    
    return all_tripdf




import re
import os
import pandas as pd
import numpy as np
import network as net
import SPpath_finder as getsp
import speed_file as t


