import movement_filter as checker
import sp_collector as sp
import travel_file5 as travel5
import travel_file4 as travel4
import pandas as pd

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

speed_profile = pd.read_csv(main_path + 'road type average speed\\speed_profile_allvehicles.csv',index_col=None)
removed_trips = pd.read_csv(main_path+'\\removed_trips.csv',index_col=None)
# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
Speed_list = []
TravelTime_list = []
Length_list = []
append_All_matched = []
append_All_SPs = []
errordf_list = []
critic_list = []
# Read database containing Edges with their hour-by-hour speed weight
finaldf = pd.read_csv(main_path+'\\weighed_velocity.csv')
finaldf['weight'] = [x.strip('[]').split(',') for x in finaldf['weight']] # convert string_list to real list
for k in range(0,16):
    plate = local_path2[k]
    # Find the vehicle path where the map matched roads of this vehicle travels are accessible
    vehicle_path = main_path11 + local_path11[k]
    path = main_path+local_path1+local_path2[k]
#****************************************************************************************************
#************************************* Start(Find SP-Trips ID)  *************************************
    local_path = local_path1 + local_path2[k]
    joint_path = main_path + local_path
    movementID_path = '\\selected_movements_id.csv'
    # Read vehicle file
    movementID_path = joint_path + movementID_path
    selected_trip_path = '\\results_selected_trips.csv'
    trip_table = joint_path + selected_trip_path
    # Read File containing all trips with their movement ids
    sps_movement = pd.read_csv(movementID_path)
    # Read file containing selected trips
    trip_df = pd.read_csv(trip_table)
    # Extract only 'sps' trips, and then only 'sp' movement
    movement_ID = sp.sp_part(sps_movement,trip_df, local_path2[k])
    # Read database of 'marginal_GPS_poins_of_movements.csv'
    marginal_file = '\\marginal_GPS_poins_of_movements.csv'
    marginaldf = pd.read_csv(joint_path + marginal_file)
    # Call a function that filters movements initiated from active stations
    filtered_move, removed_sp_count = checker.station_checker(movement_ID,marginaldf)
    #********************************* End (Find SP-Trips ID)  ****************************************
    #**************************************************************************************************
    errordf, ctiricaledges = travel5.func(marginaldf,filtered_move,finaldf,vehicle_path,plate,removed_trips)
    errordf_list.append(errordf)
    critic_list.append(ctiricaledges)
    # errordf.to_csv(path+'\\metric3'+'\\error time31.csv')
    # ctiricaledges.to_csv(path+'\\metric3'+'\\critical edges1.csv')
All_critic = pd.concat(critic_list, axis=0, ignore_index = True)
All_error = pd.concat(errordf_list, axis=0, ignore_index = True)

# All_error.to_csv(main_path + 'metric3' + '\\errortime_velocity1.csv')
# All_critic.to_csv(main_path + 'metric3' + '\\critical_edges1.csv')

# # To concat all 'critical_edges.csv' to one dataframe
# dfs = []
# for i in range(0,16):
#     local_path = local_path1 + local_path2[i]
#     joint_path = main_path + local_path
#     df = pd.read_csv(joint_path + '\\metric3\\critical edges.csv')
#     dfs.append(df)
# criticdf = pd.concat(dfs, axis=0, ignore_index = True)
# criticdf.to_csv(main_path + 'metric3' + '\\critical_edges.csv')