
def func(sp,weightdf,vehicle_path,plate):
    for_mape_list = []
    for_mape_list2 = []
    for_mape_dijk_list = []
    error_Dijk_list=[]
    similarity_list=[]
    similarity_list=[]
    y_origin_list1 = []
    y_origin_list2 = []
    y_list = []
    for_mape_dijk_list2=[]
    error_Dijk_list2=[]
    similarity_list2=[]
    error_original_2 =[]
    error_originali=[]
    # for jj in range(0,5):
    # for jj in range(round(0.8*len(sp)),round(0.82*len(sp))):
    for jj in range(round(0.8*len(sp)),len(sp)):
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
            new_weightdf = weightdf[['EdgeID','from_node','to_node','weight(s)','time_metric2']]
            new_weightdf['mean_weight'] = (new_weightdf['weight(s)'] + new_weightdf['time_metric2'])/2
            for indx, row in new_weightdf.iterrows():
                new_weightdf['weight(s)'][indx] = float(row['weight(s)'])

            df_weighted = pd.merge(new_df, new_weightdf[['EdgeID','weight(s)']], how="left", left_on = 'EdgeIndex', right_on = 'EdgeID')

            df_weighted2 = pd.merge(df_matched, new_weightdf[['EdgeID','weight(s)']], how="left", left_on = 'Index', right_on = 'EdgeID')

            # df_weighted3 = pd.merge(df_matched, new_weightdf[['EdgeID','mean_weight']], how="left", left_on = 'Index', right_on = 'EdgeID')
            weight = df_weighted['weight(s)'].to_list()
            weight2 = df_weighted2['weight(s)'].to_list()
            # weight = [x for x in weight if math.isnan(x) == False]
            # weight2 = [x for x in weight2 if math.isnan(x) == False]

            m_weight1 = (sum(weight)+0.5*sum(weight2))/2
            
            # m_weight2 = df_weighted3['mean_weight'].sum()
            y_original1 = m_weight1
            # y_original2 = m_weight2
            y_origin_list1.append(y_original1)
            # y_origin_list2.append(y_original2)
            
            error1 = (y - y_original1)
            error_originali.append(error1)
            # error2 = (y - y_original2)
            # error_original_2.append(error2)
            y_original = sum([float(o) for o in weight])
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
            flag = 1
            output1 = net.mynetwork(source,target,new_weightdf,flag)
            # flag = 2
            # output2 = net.mynetwork(source,target,new_weightdf,flag)

            if output1 is None:
                y_dijk1 = np.nan
            else:
                y_dijk1 = output1[0]
                path1 = output1[1]

            # if output2 is None:
            #     y_dijk2 = np.nan
            # else:
            #     y_dijk2 = output2[0]
            #     path2 = output2[1]
            #______________________Whole Travel Time___________________#
            y_list.append(y)
            # ______________________similarity_________________________#
            node_list1=[]
            node_list2=[]
            for i in EdgeIndex_unique:
                try:
                    df = weightdf.loc[weightdf['EdgeID']==i]
                    node_list1.extend([df['from_node'].iloc[0],df['to_node'].iloc[0]])
                    node_list2.extend([df['from_node'].iloc[0],df['to_node'].iloc[0]])
                except (TypeError, IndexError):
                    continue
            node_list_unique1 = list(set(node_list1))
            node_list_unique2 = list(set(node_list2))
            path_unique = list(set(path1))
            similarity = sum(i in node_list_unique1 for i in path1)/len(path1)
            # similarity2 = sum(i in node_list_unique2 for i in path2)/len(path2)
            #______________________time error_________________________#

            # error_dijk = (y - y_dijk1)
            error_original1 = [x for x in error_originali if math.isnan(x) == False]
            for_mape_list.append(abs(error1/y))
            error_dijk = (y - y_dijk1)
            # error_dijk2 = (y - y_dijk2)
            error_original2 = [x for x in error_original_2 if math.isnan(x) == False]
            # for_mape_list2.append(abs(error2/y))
            for_mape_dijk_list.append(abs(error_dijk/y))
            error_Dijk_list.append(error_dijk)
            similarity_list.append(similarity)
            # for_mape_dijk_list2.append(abs(error_dijk2/y))
            # error_Dijk_list2.append(error_dijk2)
            # similarity_list2.append(similarity2)

    # MAPE2 = (1/len(for_mape_list2))*sum(for_mape_list2)
    # MAPE_dijk2 = (1/len(for_mape_dijk_list2))*sum(for_mape_dijk_list2)
    # error_orig2 = [x for x in error_original_2  if np.isnan(x) == False]
    # RMSE2 = math.sqrt((1/len(error_orig2))*sum(error_orig2)**2)
    # RMSE_dijk2 = math.sqrt((1/len(error_Dijk_list2))*sum(error_Dijk_list2)**2)

    MAPE = (1/len(for_mape_list))*sum(for_mape_list)
    MAPE_dijk = (1/len(for_mape_dijk_list))*sum(for_mape_dijk_list)
    error_orig = [x for x in error_originali  if np.isnan(x) == False]
    RMSE = math.sqrt((1/len(error_orig))*sum(error_orig)**2)
    RMSE_dijk = math.sqrt((1/len(error_Dijk_list))*sum(error_Dijk_list)**2)

    # return y_origin_list1,error_originali,y_origin_list2,error_original_2,error_Dijk_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list,error_Dijk_list2,MAPE2,MAPE_dijk2,RMSE2,RMSE_dijk2, similarity_list2
    return y_origin_list1,error_originali,error_Dijk_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list
    # return y_list,error_Dijk_list,error_Dijk_list2

import re
import os
import math
import pandas as pd
import numpy as np
import network as net
import SPpath_finder as getsp
import speed_file as t


