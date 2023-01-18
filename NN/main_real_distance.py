import pandas as pd
import numpy as np
import travelfile_real as travel

main_path = 'C:\\My files\\Dr Buzna\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'C:\\My files\\Dr Buzna\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']  
#***************************
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps','ps_sps'] 
# **************************
for ku in range(2,5): 
# for ku in range(0,1):
    tripdf_list = []
    for i in range(0,15):
    # for i in range(0,2):
        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+moves[ku]+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)

        trips = travel.func(move_type,vehicle_path,plate)
        tripdf_list.append(trips)
    trip_all = pd.concat(tripdf_list,axis=0,ignore_index=True)
    trip_all.to_csv('C:\\My files\\Dr Buzna\\trips\\NN\\tripdf_'+moves[ku]+'.csv')
    # trip_all.to_csv('C:\\My files\\Dr Buzna\\trips\\NN\\tripdf1_'+moves[ku]+'.csv')

