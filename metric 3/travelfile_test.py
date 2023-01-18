
def func(sp,weightdf,vehicle_path,plate):
    for_mape_list = []
    for_mape_dijk_list = []
    error_Dijk_list=[]
    similarity_list=[]
    error_original=[]
    similarity_list=[]
    # for jj in range(944,945):
    for jj in range(round(0.8*len(sp)),round(0.82*len(sp))):
    # for jj in range(round(0.8*len(sp)),len(sp)):
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
            EdgeIndex_unique = df_matched['Index'].unique()
            new_df = t.calc_time(df_specific)
            y = new_df['TimeDiff0'].iloc[1:].sum()
            #_____________________weight_df_____________________#
            df_specific['hour'] = pd.to_datetime(df_specific['datetime']).dt.strftime('%H')
            hr = int(df_specific['hour'].iloc[0])    
            time_list = []
            for ind, row in weightdf.iterrows():
                velocity = float(weightdf['weight'].iloc[ind][hr])
                try:
                    traversetime = row['Length(m)(poly)']/velocity
                except ZeroDivisionError:
                    pass
                time_list.append(traversetime)
            # define the traversal time of an edge at a specific time as weight (instead of velocity weight)
            weightdf['weight(s)'] = time_list
            new_weightdf = weightdf[['EdgeID','from_node','to_node','weight(s)']]
            df_weighted = pd.merge(df_matched, new_weightdf[['EdgeID','weight(s)']], how="left", left_on = 'Index', right_on = 'EdgeID')
            y_original = df_weighted['weight(s)'].sum()
            #_____________________network_______________________#
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
            output = net.mynetwork(source,target,new_weightdf)

            if output is None:
                continue
            y_dijk = output[0]
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
            error = (y - y_original)
            error_original.append(error)
            error_dijk = (y - y_dijk)
            for_mape_list.append(abs(error/y))
            for_mape_dijk_list.append(abs(error_dijk/y))
            error_Dijk_list.append(error_dijk)
            similarity_list.append(similarity)
        
    MAPE = (1/len(for_mape_list))*sum(for_mape_list)
    MAPE_dijk = (1/len(for_mape_dijk_list))*sum(for_mape_dijk_list)
    RMSE = math.sqrt((1/len(error_original))*sum(error_original)**2)
    RMSE_dijk = math.sqrt((1/len(error_Dijk_list))*sum(error_Dijk_list)**2)

    return error_original,error_Dijk_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list

import re
import os
import math
import pandas as pd
import network as net
import SPpath_finder as getsp
import speed_file as t


