import pandas as pd
import numpy as np
import travelfile_sp as travel_sp
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
move = 'hs_sphs' ##   
#**************### 
MAPE_list = []
RMSE_list = []
MAPE_dijk_list = []
RMSE_dijk_list = []
MAPE_length_list = []
RMSE_length_list = []   
err_list = []
sim_list = []     
for i in range(0,15):
# for i in range(1,2):
    plate = local_path2[i]
    vehicle_path = main_path11 + local_path11[i]
    local_path = local_path1 + local_path2[i]
    joint_path = main_path + local_path
    movementID_path = '\\'+move+'.csv'
    # params = [a,b,c,d0],  if d<d0: y_hat= c*sqrt(dist), else: y_hat= a*dist + b
    if move == 'sp_sps' or move == 'sp_sphs':
        speed = 11.36
    elif move == 'ps_sps':
        speed = 9.633819235
    elif move == 'ph_sphs':
        speed = 10.43722261
    elif move == 'hs_sphs':
        speed = 11.4576594

    # Read File containing all sp (marginal) with their movement ids
    move_type = pd.read_csv(joint_path + movementID_path)
    err,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list = travel_sp.func(move_type,weightdf,vehicle_path,plate,speed)
    err_list.append(err)
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
df.to_csv(main_path+'\\metric1'+'\\'+move+'_naive.csv')
regression_df.to_csv(main_path+'\\metric1'+'\\hs.csv')
ass=1