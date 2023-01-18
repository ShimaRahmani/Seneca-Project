import pandas as pd
import travelfile_speedpattern as travel
import numpy as np

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
#**************###  
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps','ps_sps']
#**************###   
df_li = []
df_hr_li = []
df_road_li = []
for move in moves: 
    df_list = []
    df_hr_list = []
    df_road_list = []
    for i in range(0,16):
    # for i in range(0,2):
        plate = local_path2[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+move+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)
        vehicle_file = joint_path + '\\vehicle.csv'
        vehicle = pd.read_csv(vehicle_file, encoding = "ISO-8859-1")
        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        df , df_hr, df_road = travel.func(vehicle,move_type,vehicle_path,move,plate)
        df_hr_list.append(df_hr)
        df_road_list.append(df_road)
        df_list.append(df)
        # df_list.to_csv(main_path+'\\Upstream Vehicle Info\\speed_hour_'+move+'_'+plate+'.csv')
    df_hr_conc = pd.concat(df_hr_list, axis=0, ignore_index=True)
    df_road_conc = pd.concat(df_road_list, axis=0, ignore_index=True)
    df_hr_conc['move']=move
    df_road_conc['move']=move
    df_hr_li.append(df_hr_conc)
    df_road_li.append(df_road_conc)
    df = pd.concat(df_list , axis=0, ignore_index = True) 
    df_li.append(df)
    # df_li.to_csv(main_path+'\\Upstream Vehicle Info\\speed_hour_'+move+'.csv')
df_hr_final = pd.concat(df_hr_li, axis=0, ignore_index=True)
df_road_final = pd.concat(df_road_li, axis=0, ignore_index=True)
df_final = pd.concat(df_li , axis=0, ignore_index = True)
# df_final.to_csv(main_path+'\\Upstream Vehicle Info\\speed_hour_hs.csv')
ass=1