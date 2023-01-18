import travel_file2 as travel2
import pandas as pd


main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
#     i = 1
Speed_list = []
TravelTime_list = []
Length_list = []
append_All_matched = []
append_All_trips = []
all_moves_spped = []
#**************###
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
#**************### 
for move in moves:
    move_speed = []
    for i in range(0,15):
        # Find the vehicle path where the map matched roads of this vehicle travels are accessible
        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+move+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)

        All_trips = travel2.func(move_type,vehicle_path)
        append_All_trips.append(All_trips)
    move_speed = pd.concat(append_All_trips , axis=0, ignore_index = True) 
    grouped = move_speed.groupby('Highway')['road_speed'].mean()
    grouped.to_csv(main_path+'\\metric2'+'\\'+move+'.csv')
    all_moves_spped.append(move_speed)
all_move_speed = pd.concat(all_moves_spped , axis=0, ignore_index = True) 
grouped_all = all_move_speed.groupby('Highway')['road_speed'].mean()
grouped_all.to_csv(main_path+'\\metric2'+'\\speed_profile_RoadType.csv')



