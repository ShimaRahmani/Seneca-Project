import travelfile_test as travel
import pandas as pd
import numpy as np

main_path = 'C:\\My files\\Dr Buzna\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'C:\\My files\\Dr Buzna\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

removed_trips = pd.read_csv(main_path+'\\removed_trips.csv',index_col=None)
# Read database containing Edges with their hour-by-hour speed weight
weightdf = pd.read_csv(main_path+'\\weighed_speed.csv')
weightdf['weight'] = [x.strip('[]').split(',') for x in weightdf['weight']] # convert string_list to real list
# for ind,row in weightdf.iterrows():
#     s = [x.replace("'", "") for x in row['weight']]
#     w=[float(x) for x in s]
#     weightdf['weight'][ind] = w
# weightdf.to_csv(main_path+'\\weighed_speed1.csv')
# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
#**************###
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps','ps_sps']
#**************### 
for move in moves: 
    MAPE_list = []
    RMSE_list = []
    MAPE_dijk_list = []
    RMSE_dijk_list = []
    MAPE_length_list = []
    MAPE_naive_list = []
    RMSE_length_list = []   
    err_list = []
    sim_list = [] 
    err_list_dijk = []
    for i in range(0,15):
        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+move+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)
    #********************************* End (Find SP-Trips ID)  ****************************************
    #**************************************************************************************************
        error_original,error_Dijk_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list = travel.func(
            move_type,weightdf,vehicle_path,plate)
        err_list.append(error_original)
        err_list_dijk.append(error_Dijk_list)
        sim = np.mean(similarity_list)
        sim_list.append(sim)
        MAPE_list.append(MAPE)
        RMSE_list.append(RMSE)
        MAPE_dijk_list.append(MAPE_dijk)
        RMSE_dijk_list.append(RMSE_dijk)
        plate0 = local_path2[0:-1]

    regression_df = pd.DataFrame({'Plate': plate0,
                                'MAPE original route':MAPE_list,
                                'RMSE original route':RMSE_list,
                                'MAPE Dijk route':MAPE_dijk_list,
                                'RMSE Dijk route':RMSE_dijk_list,
                                'Similarity':sim_list
                                })
    flat = [item for sublist in err_list for item in sublist]
    df = pd.DataFrame({'Time Error [s]':flat})
    df.to_csv(main_path+'\\metric3'+'\\'+move+'_errortime.csv')
    regression_df.to_csv(main_path+'\\metric3\\'+move+'.csv')


ass=1