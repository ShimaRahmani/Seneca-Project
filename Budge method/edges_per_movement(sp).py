import travel_file0 as travel0
import pandas as pd


main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

speed_profile = pd.read_csv(main_path + 'road type average speed\\speed_profile_allvehicles.csv')
# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
Speed_list = []
TravelTime_list = []
Length_list = []
append_All_matched = []
append_All_SPs = []
Data_prepared_all_vehicles=[]
removed_list=[]
d= [ ]
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps','ps_sps'] 
#**************### 
for ku in range(0,5): 
    df_list=[]
    added_df_li = []
    Edge_list_list = []
    # for i in range(0,2):
    for i in range(0,15):

        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+moves[ku]+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)
        #********************************************************
        Edge_list, Number_added_edges_list = travel0.func(move_type,vehicle_path,local_path2[i])
        platform=[]
        veh = []
        for j in range(0,len(Edge_list)):
            platform.append(local_path2[i])
        for l in range(0,len(Number_added_edges_list)):
            veh.append(local_path2[i])

        dataframe = pd.DataFrame({'vehicle':platform,'Edges unique':Edge_list})
        added_df = pd.DataFrame({'vehicle':veh,'No added edges':Number_added_edges_list})        
        df_list.append(dataframe)
        added_df_li.append(added_df)
        Edge_list_list.append(Edge_list)
        
        q=1

    Edge_df = pd.DataFrame({'Edges':Edge_list_list})
    df_list_all = pd.concat(df_list,axis=0,ignore_index=True)
    added_df_li_all = pd.concat(added_df_li,axis=0,ignore_index=True)

    added_df_li_all.to_csv(main_path+'\\Upstream Vehicle Info\\'+moves[ku]+'_added_edges.csv')
    # Edge_df.to_csv(main_path+'\\Upstream Vehicle Info\\'+moves[ku]+'_Edges_used_all.csv')
    # df_list_all.to_csv(main_path+'\\Upstream Vehicle Info\\'+moves[ku]+'_trips_edges.csv')
    