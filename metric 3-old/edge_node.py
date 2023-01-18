import movement_filter as checker
import sp_collector as sp
from datetime import datetime
import travel_file4 as travel4
import pandas as pd
import csv
import glob
import os
import re
import midpoint as mid

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

# for k in range(0,16):
#     vehicle_path = main_path11 + local_path11[k]
#     Geometry_data_path = vehicle_path + '\\whole_graph_edges_incid.txt'     
#     edge_list = []
#     from_list = []
#     to_list = []    
#     df_list = []
#     with open(Geometry_data_path) as f:
#         lines = f.readlines()
#         for i in lines:
#             edge_node = re.findall('\d*',i)
#             edge = edge_node[0]
#             from_node = edge_node[4]
#             to_node = edge_node[8]
#             edge_list.append(edge)
#             from_list.append(from_node)
#             to_list.append(to_node)
#     edgenode_df0 = pd.DataFrame({
#         'Edge:':edge_list, 'from_node':from_list, 'to_node':to_list
#     })
#     df_list.append(edgenode_df0) 
# edgenode_df = pd.concat(df_list, axis=0, ignore_index = True)
# ass=1
# edgenode_df.to_csv(main_path+'\\edge node\\edge_node.csv', index = False)   
# edgenode_df = pd.read_csv(main_path+'\\edge node\\edge_node.csv',index_col=None)   
# for k in range(0,16):
#     vehicle_path = main_path11 + local_path11[k]
#     node_file = vehicle_path + '\\whole_graph_nodes.vec' 
#     node_list = []
#     node_lat_list = []
#     node_lon_list = []    
#     dff_list = []
#     with open(node_file) as f:
#         lines = f.readlines()
#         for i in range(0,len(lines)):
#             if i%2 == 0:
#                 line = lines[i]
#                 node = re.findall('\d*',line)[0]
#                 node_lat = re.split('\s',lines[i+1])[3]
#                 node_lon = re.split('\s',lines[i+1])[1]
#                 node_list.append(node)
#                 node_lat_list.append(node_lat)
#                 node_lon_list.append(node_lon)
#             else:
#                 continue
#         node_df0 = pd.DataFrame({
#             'node':node_list, 'lat':node_lat_list, 'lon':node_lon_list
#         })
#     dff_list.append(node_df0) 
# node_df = pd.concat(dff_list, axis=0, ignore_index = True)
# node_df.to_csv(main_path+'\\edge node\\node.csv', index = False)  
# node_df = pd.read_csv(main_path+'\\edge node\\node.csv',index_col=None)  
# result_from = pd.merge(edgenode_df,node_df,left_on='from_node',right_on='node',how='left')
# result_to = pd.merge(result_from,node_df,left_on='to_node',right_on='node',how='left')
# result_to.to_csv(main_path+'\\edge node\\full egde node.csv', index = False)
edgenode = pd.read_csv(main_path+'\\edge node\\full egde node.csv',index_col=None) 
df = pd.read_csv(main_path+'weighed_velocity.csv',index_col=None)
Data_Prep_filtered2 = pd.merge(df,edgenode,left_on='EdgeID',right_on='Edge',how='left')
# Data_Prep_filtered2.to_csv(main_path+'weighed_velocity.csv', index = False)
# df = pd.read_csv(main_path+'weighed_velocity.csv',index_col=None) 
# critic =pd.read_csv(main_path + 'metric3' + '\\critical_edges3.csv', index_col=None)
# df1=df.drop_duplicates(['EdgeID'])
# result = pd.merge(left=critic,right=df1[['EdgeID','Length(m)(poly)','Length(m)(euclid)']],left_on='edge',right_on='EdgeID',how='left')
# a = (result['Length(m)(euclid)'].values)
# b= result['Length(m)(poly)'].values
# import numpy as np
# a=a.astype(np.float)
# b=b.astype(np.float)
# c = a/b
# result['tortuosity'] = c
# # result.to_csv(main_path + 'metric3' + '\\critical_edges2.csv')
ass=1


