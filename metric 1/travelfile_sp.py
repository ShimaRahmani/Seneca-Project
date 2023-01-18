def func(sp,weightdf,vehicle_path,plate,speed):
    for_mape_list = []
    for_mape_dijk_list = []
    y_hat_list = []
    y_list = []
    y_dijk_list = []
    y_hat_dijk_list = []
    no_path_trips = []
    error_regress_Dijk_list=[]
    err_origin_list = []
    similarity_list=[]
    length_error_list = []
    length_err = []
    err_list = []
    total_test_data = len(sp) - round(0.8*len(sp))
    coverability = pd.DataFrame({'Plate':[],'movement_id':[],'total_test_data':[],'uncovered_edges(%)':[]})
    for jj in range(round(0.8*len(sp)),len(sp)):
    # for jj in range(round(0.8*len(sp)),round(0.9*len(sp))):
        # match the indeces of filtered movements
        df = sp.loc[sp.index==jj]
        TravelTime = float(df['duration'])
        if TravelTime > 40:
            continue
        TravelTime_sec = TravelTime*60
        Length = float(df['length_metres'])
        TravelTime_hat = Length/speed
        err = TravelTime_sec - TravelTime_hat
        err_list.append(err)
        if TravelTime < 2:
            continue
        for_mape = abs(err/(TravelTime_sec))
        for_mape_list.append(for_mape)
        err_origin_list.append(err)

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
            #________________check coverability_________________#
            tot = len(EdgeIndex_unique)
            in_avail = sum(i in weightdf['EdgeID'].values for i in EdgeIndex_unique)
            ratio = in_avail/tot
            coverability = coverability.append({'Plate':plate,'movement_id':df['movement_id'],
                'total_test_data':total_test_data,'uncovered_edges(%)':1-ratio}, ignore_index=True)
            if ratio < 0.90:
                continue
            #_____________________weight_df_____________________#
            # new_weightdf = weightdf[['EdgeID','from_node','to_node','Length(m)(poly)']]
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
            #_______add speed to weightdf_______
            weightdf['speed'] = speed
            travel_time_hat = weightdf['Length(m)(poly)'] / weightdf['speed']
            weightdf['time'] = travel_time_hat
            #___________________________________
            output = net.mynetwork(source,target,weightdf)

            if output is None:
                no_path_trips.append(df['movement_id'])
                continue
            time_tot = output[0]
            path = output[1]
            #______________________similarity_________________________#
            node_list=[]
            for i in EdgeIndex_unique:
                try:
                    dff = weightdf.loc[weightdf['EdgeID']==i]
                    node_list.extend([dff['from_node'].iloc[0],dff['to_node'].iloc[0]])
                except (TypeError, IndexError):
                    continue
            node_list_unique = list(set(node_list))
            path_unique = list(set(path))
            similarity = sum(i in node_list_unique for i in path)/len(path)
            #______________________time error_________________________#
            y_hat_dijk = time_tot
            y = TravelTime_sec
            error_dijk = (y - y_hat_dijk)
            for_mape_dijk_list.append(abs(error_dijk/y))
            error_regress_Dijk_list.append(error_dijk)
            similarity_list.append(similarity)
            y_hat_dijk_list.append(y_hat_dijk)
            y_dijk_list.append(y)

    MAPE = (1/len(for_mape_list))*sum(for_mape_list)
    MAPE_dijk = (1/len(for_mape_dijk_list))*sum(for_mape_dijk_list)
    RMSE = math.sqrt((1/len(err_origin_list))*sum(err_origin_list)**2)
    RMSE_dijk = math.sqrt((1/len(error_regress_Dijk_list))*sum(error_regress_Dijk_list)**2)

    return err_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list


import math
import re
import os
import pandas as pd
import network as net
import numpy as np
import SPpath_finder as getsp
