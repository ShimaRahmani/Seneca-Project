import pandas as pd
import time_distance as tdf
import numpy as np
import frequency_data as freq
import math

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']
main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

move = 'sp_sphs' ##   
#**************### 
   
for i in range(0,17):
# for i in range(1,2):
    plate = local_path2[i]
    vehicle_path = main_path11 + local_path11[i]
    local_path = local_path1 + local_path2[i]
    joint_path = main_path + local_path
    movementID_path = '\\'+move+'.csv'

    # Read File containing all sp (marginal) with their movement ids
    move_type = pd.read_csv(joint_path + movementID_path)
    list_timediff = freq.func(move_type,vehicle_path)
    freq_mean = np.mean(list_timediff)
    ass=11
                  