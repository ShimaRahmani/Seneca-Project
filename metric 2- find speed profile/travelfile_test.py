def func(sp,weightdf,vehicle_path,plate,speedf,speed_profile0):
    for_mape_list = []
    for_mape_dijk_list = []
    no_path_trips = []
    error_regress_Dijk_list=[]
    similarity_list=[]
    error_Dijk_list =[]
    y_list = []
    roadf_list = []
    appended_new_df = []
    appended_matched_id = []
    errortime_list = []
    errortime_list_naive = []
    for_mape_naive_list = []
    count = 0
    # coverability = pd.DataFrame({'Plate':[],'movement_id':[],'total_test_data':[],'uncovered_edges(%)':[]})
    for jj in range(round(0.8*len(sp)),len(sp)):
    # for jj in range(round(0.8*len(sp)),round(0.82*len(sp))):
        # match the indeces of filtered movements
        df = sp.loc[sp.index==jj]
        TravelTime = float(df['duration'])
        if TravelTime > 40:
            count = count+1
            continue
        if TravelTime < 2:
            count = count+1
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
            # create a new df for sp involving road type, speeper road seg
            new_df = speed.calc_speed(df_specific, df_matched,speedf,speed_profile0)
            roadf = new_df[['Highway','mini_err','mini_err_naive']]
            roadf_list.append(roadf)
            # store all new interesting dataframes (df_new & df_matched) in a list
            appended_new_df.append(new_df)
            appended_matched_id.append(df_matched)
            err = new_df['mini_err'].sum()
            err_naive = new_df['mini_err_naive'].sum()
            errortime_list.append(err)
            errortime_list_naive.append(err_naive)
            time_actual = new_df['TimeDiff0'].sum()
            time_hat = new_df['time_hat'].sum()
            time_hat_naive = new_df['time_hat_naive'].sum()
            for_mape_list.append(abs(time_actual- time_hat)/time_actual)
            for_mape_naive_list.append(abs(time_actual- time_hat_naive)/time_actual)
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
            output = net.mynetwork(source,target,weightdf)

            if output is None:
                no_path_trips.append(df['movement_id'])
                continue
            time_tot = output[0]
            path = output[1]
            y_dijk1 = output[0]
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
            # y_hat_dijk = time_tot
            # y = new_df['TimeDiff0'].iloc[1:].sum()
            error_dijk = (time_actual - y_dijk1)
            error_Dijk_list.append(error_dijk)
            y_list.append(time_actual)
            # for_mape_dijk_list.append(abs(error_dijk/y))
            # error_regress_Dijk_list.append(error_dijk)
            # similarity_list.append(similarity)
    
    MAPE_naive = (1/len(for_mape_naive_list))*sum(for_mape_naive_list)
    MAPE = (1/len(for_mape_list))*sum(for_mape_list)
    # MAPE_dijk = (1/len(for_mape_dijk_list))*sum(for_mape_dijk_list)
    # RMSE = math.sqrt((1/len(errortime_list))*sum(errortime_list)**2)
    # RMSE_naive = math.sqrt((1/len(errortime_list_naive))*sum(errortime_list_naive)**2)
    # RMSE_dijk = math.sqrt((1/len(error_regress_Dijk_list))*sum(error_regress_Dijk_list)**2)

    # return roadf_list,errortime_list,errortime_list_naive,MAPE,MAPE_naive,MAPE_dijk,RMSE,RMSE_naive,RMSE_dijk, similarity_list
    return MAPE,MAPE_naive,count,error_Dijk_list,y_list


import math
import re
import os
import pandas as pd
import network as net
import speed_file as speed
import metric2 as go
import numpy as np
import SPpath_finder as getsp
