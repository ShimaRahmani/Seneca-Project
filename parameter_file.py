def param_extractor():
    
# Create File Paths

    main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
    local_path1 = 'h_300_c300_trips_KE_'
    local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                   '440HY','445LI','471IH','580IZ','624KK',
                   '724HU','761GV','796ES','853KK','992JH']

    main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
    local_path11 = ['1','2','3','4','5','6','7','8','9',
                    '11','12','13','14','15','16','17']

    speed_profile = pd.read_csv(main_path + 'road type average speed\\speed_profile_allvehicles.csv')
# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
#     i = 1
    Speed_list = []
    TravelTime_list = []
    Length_list = []
    append_All_matched = []
    append_All_SPs = []
    for k in range(0,len(local_path11)):
        # Find the vehicle path where the map matched roads of this vehicle travels are accessible
        vehicle_path = main_path11 + local_path11[k]

        local_path = local_path1 + local_path2[k]
        joint_path = main_path + local_path
        movementID_path = '\\selected_movements_id.csv'
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
        marginal_df = pd.read_csv(joint_path + marginal_file)

    # Call a function that filters movements initiated from active stations
        filtered_move, removed_sp_count = checker.station_checker(movement_ID,marginal_df)

        metric = 1
        if metric == 1:
            print('******metric1********')
            # Call a function that returns average speed of sp movement for each vehicle
            ave_speed,TravelTime,Length = travel.ave_speed_list(filtered_move, marginal_df)
            # Create a new csv-file, putting [Travel time & Distance] inside the file
            dict = {'TravelTime_sec':TravelTime, 'Length_m':Length, 'Speed_kmh':ave_speed}
            joint_df = pd.DataFrame(dict)
            Speed_file = '\\metric1\\time_length_speed.csv'
            joint_df.to_csv(joint_path + Speed_file, index = False)

        elif metric ==2:
            print('******metric2********')

            All_SPs, All_matched, errortime_list = travel2.func(marginal_df,filtered_move,vehicle_path,speed_profile)
            error = pd.DataFrame(errortime_list, columns=["errortime"])
            metric2_path = '\\metric2\\errortime.csv'
            error.to_csv(joint_path + metric2_path, index = False)

            Speed_file = '\\metric2\\MapMatched_EdgeID_time_length_speed.csv'
            All_matched.to_csv(joint_path + Speed_file, index = False)

            # append_All_SPs.append(All_SPs)

        elif metric ==3:
            print('******metric3********')
        elif metric ==4:
            print('******metric4********')
        else:
            print('******metric5********')

    # #############  metric1 #######################
    # folder = 'D:\\work\\Dr Buzna\\R files\\data\\trips'
    # path = folder + "\\**\\metric2\\sp_EdgeIndex.csv"

    # df_veh_sp_Edge = pd.concat(map(pd.read_csv, glob.iglob(path, recursive=True)))
    # print(df_veh_sp_Edge.head())

    # ############## metric2 #######################

    ######## extract speed profile and save it in dir
    # All_SPs_profile = '\\road type average speed\\append_All_SPs.csv'
    # # h = append_All_SPs[0]
    # All_SPs.to_csv(main_path  + All_SPs_profile)

    # g = pd.read_csv(main_path  + All_SPs_profile)
    # grouped = g.groupby('Highway')['road_speed'].mean()
    # speed_profile = '\\road type average speed\\speed_profile22222.csv'
    # grouped.to_csv(main_path  + speed_profile)
    ########

    # return Speed_list,TravelTime_list,Length_list


import movement_filter as checker
import sp_collector as sp
import travel_file as travel
import SPpath_finder as getsp
from datetime import datetime
import travel_file2 as travel2
import pandas as pd
import csv
import glob
import os
import re

param_extractor()
