import pandas as pd
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
weightdf = pd.read_csv(main_path+'\\weighed_velocity.csv')
#**************###
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
#**************### 
err_list = []   
for move in moves:
 
    for i in range(0,15):
    # for i in range(1,2):
        plate = local_path2[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+move+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)
        if move == 'sp_sps':
            speed = 11.48671845
        elif move == 'ps_sps':
            speed = 9.633819235
        elif move == 'sp_sphs':
            speed = 11.23785949
        elif move == 'ph_sphs':
            speed = 10.43722261
        elif move == 'hs_sphs':
            speed = 11.4576594
        else:
            speed = 10.85
            
        speed = 10.85
        err = travel_sp.func(move_type,plate,speed)
        err_list.append(err)
flat = [item for sublist in err_list for item in sublist]
df = pd.DataFrame({'Error Time (s)': flat})
df.to_csv(main_path+'\\metric1'+'\\naive.csv')
ass=1