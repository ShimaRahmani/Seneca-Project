import travel_file4 as travel4
import pandas as pd



main_path = 'D:\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'D:\\map_matching\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16']

speed_profile = pd.read_csv(main_path + 'road type average speed\\speed_profile_allvehicles.csv')
# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles

#**************###
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps','ps_sps']
#**************### 
for move in moves:
    Speed_list = []
    TravelTime_list = []
    Length_list = []
    append_All_matched = []
    append_All_SPs = []
    Data_prepared_all_vehicles=[]
    removed_list=[]
    for k in range(0,16):

        vehicle_path = main_path11 + local_path11[k]
        local_path = local_path1 + local_path2[k]
        joint_path = main_path + local_path
        movementID_path = '\\'+move+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)
        #********************************* End (Find SP-Trips ID)  ****************************************
        #**************************************************************************************************
        Data_prepared_one_vehicle,excluded_trips = travel4.func(move_type,
        vehicle_path,local_path2[k])
        removed = pd.DataFrame({'plate':local_path2[k], 'movement_id':excluded_trips})
        removed_list.append(removed)
        # Data_prepared_one_vehicle.to_csv(joint_path+'\\Data_Prep.csv')
        # removed.to_csv(joint_path+'\\excluded_trip.csv')
        Data_prepared_all_vehicles.append(Data_prepared_one_vehicle)
    removed_list_all = pd.concat(removed_list, axis=0, ignore_index = True)
    Data_prep_All = pd.concat(Data_prepared_all_vehicles, axis=0, ignore_index = True)
    Data_prep_All.to_csv(main_path+'\\metric3\\Data_Prep_'+move+'.csv')
    # removed_list_all.to_csv(main_path+'\\removed_trips.csv')
    