import movement_filter as checker
import sp_collector as sp
from datetime import datetime
import travel_file3 as travel3
import pandas as pd
import csv
import glob
import os
import re

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
Speed_list = []
TravelTime_list = []
Length_list = []
append_All_matched = []
append_All_SPs = []

for k in range(0,1):

# for k in range(0,len(local_path11)):
    # Find the vehicle path where the map matched roads of this vehicle travels are accessible
    vehicle_path = main_path11 + local_path11[k]
#****************************************************************************************************
#************************************* Start(Find SP-Trips ID)  *************************************
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
#********************************* End (Find SP-Trips ID)  ****************************************
#**************************************************************************************************
   # TRAVEL_file2
    # All_SPs, All_matched = travel2.func(marginal_df,filtered_move,vehicle_path)
   # Travel_file3
    All_SPs, All_matched = travel3.func(marginal_df,filtered_move,vehicle_path)
    

