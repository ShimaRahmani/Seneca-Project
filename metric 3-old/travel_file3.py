def func(marginal_df,filtered_move,vehicle_path):

    appended_new_df = []
    pos_list = []
    errortime_list = []
    matched_list = []
    global jj
    h = nx.Graph()
    # for jj in range(257,258):
    for jj in range(0,len(filtered_move)):

        # match the indeces of filtered movements with marginal file
        # output: a row from marginal file showing an sp movement
        df = marginal_df.loc[marginal_df['movement_id']==filtered_move[jj]]

        # split 'date' & 'start_time' & 'end_time' of (marginal.csv) file
        df['Dates'] = pd.to_datetime(df['first_time']).dt.date
        df['HrMin_start'] = pd.to_datetime(df['first_time']).dt.strftime('%H:%M')
        df['HrMin_end'] = pd.to_datetime(df['last_time']).dt.strftime('%H:%M')
        

        # Open (edges_all.csv) file that matches the date of current sp trip
        str_date = str(df['Dates'].iloc[0])
        matchedroadall_file = [str(f) for f in os.listdir(vehicle_path) if 
                                re.match(rf'.*{re.escape(str_date)}.*_all', f)]

        # for some days there is no file. Ignore them
        if bool(matchedroadall_file):
            full_path_all = vehicle_path+'\\'+matchedroadall_file[0]
            df_all = pd.read_csv(full_path_all)

            # MISSION GETS STARTED HERE;
            # 1. match start_time of an sp trip with time of (edge_all.csv) file
            # 2. match end_time of an sp trip with time of (edges_all.csv) file

            df_all['HrMin'] = pd.to_datetime(df_all['datetime']).dt.strftime('%H:%M')

            for index, row in df_all.iterrows():

                # match start time of an sp trip
                if row['HrMin'] == df['HrMin_start'].iloc[0]:
                    first_index = row['Index']

                    # match end_time of an sp trip with time of (edges_all.csv) file
                    for index, roww in df_all[df_all['Index']>=first_index].iterrows():

                        if roww['HrMin'] == df['HrMin_end'].iloc[0]:
                            last_index = roww['Index']
                            if last_index > first_index:
                                # extract the sp trip part from (edges_all.csv)
                                df_specific = df_all[(df_all['Index'] >= first_index) & (df_all['Index'] <= last_index)]
                                # Compile a network of sp moves
                                
                                g,dic = net.network(h,df_specific,matchedroadall_file)
                                h.add_nodes_from(g.nodes())
                                h.add_edges_from(g.edges())
                                pos_list.append(dic)
                                # lis = [{'1':1},{'2':2}]
                                final={}
                                for i in pos_list:
                                    for m,n in i.items():
                                        final.update({m:n})
                                # nx.draw(h,pos=final,alpha=0.1)
                                
                                # find the unique road IDs
                                EdgeIndex_unique = df_specific['EdgeIndex'].unique()

                                # create a new df for sp involving road type, speed per road seg
                                #new_df = sp.calc_speed(df_specific, df_sp_EdgeID)
                                # store all new interesting dataframes (df_new & df_sp_EdgeID) in a list
                                #appended_new_df.append(new_df)
                        
                            else:
                                continue

                            #if row['HrMin'] == df['HrMin_end'].iloc[0]
                            break
                 #if row['HrMin'] == df['HrMin_start'].iloc[0]
                    break
        # if bool(matchedroadID_file)
        else:
            continue

    All_SPs = pd.concat(appended_new_df, axis=0, ignore_index = True)
    All_matched = pd.concat(matched_list, axis=0, ignore_index = True)

    return All_SPs, All_matched, errortime_list


import re
import os
import time
import networkx as nx
import pandas as pd
import numpy as np
import create_network as net
import matplotlib.pyplot as plt
# import seaborn as sns