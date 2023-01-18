import pandas as pd
import time_distance as tdf
import numpy as np
import travelfile_sp_sps as travel_sp
import math

# def GetAllPointsForRegression():
    
# Create File Paths

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']
main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

weightdf = pd.read_csv(main_path+'\\weighed_velocity.csv')
#**************###
move = 'sp_sphs' ##   
#**************### 
MAPE_list = []
RMSE_list = []
MAPE_dijk_list = []
RMSE_dijk_list = []
MAPE_length_list = []
RMSE_length_list = []     
sim_list = []     
for i in range(0,15):
# for i in range(1,2):
    plate = local_path2[i]
    vehicle_path = main_path11 + local_path11[i]
    local_path = local_path1 + local_path2[i]
    joint_path = main_path + local_path
    movementID_path = '\\'+move+'.csv'
    # params = [a,b,c,d0],  if d<d0: y_hat= c*sqrt(dist), else: y_hat= a*dist + b
    if move == 'sp_sps':
        params = [0.0009,3.1522,0.1453,10600]
    elif move == 'ps_sps':
        params = [0.0006,13.2483,0.7955,618]
    elif move == 'sp_sphs':
        params = [0.0008,4.4508,0.1285,9400]
    elif move == 'ph_sphs':
        params = [0.0010,3.1452,0.1865,28900]
    else:
        params = [0.0010,-0.3485,0.1566,16750]

    # Read File containing all sp (marginal) with their movement ids
    move_type = pd.read_csv(joint_path + movementID_path)
    MAPE,MAPE_dijk,RMSE,RMSE_dijk,MAPE_length,RMSE_length, similarity_list = travel_sp.func(move_type,weightdf,vehicle_path,plate,params)
    sim = np.mean(similarity_list)
    sim_list.append(sim)
    MAPE_length_list.append(MAPE_length)
    RMSE_length_list.append(RMSE_length)
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
                              'MAPE length': MAPE_length_list,
                              'RMSE length':RMSE_length_list,
                              'Similarity':sim_list
                              })
regression_df.to_csv(main_path+'\\Regression'+'\\regression metrics - sp_sphs.csv')
ass=1