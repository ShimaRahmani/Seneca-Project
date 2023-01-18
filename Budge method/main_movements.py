import pandas as pd
import time_distance as tdf
import movement_filter as check
import sp_collector as sp
import sp_collector_sphs as sp_sphs
import numpy as np

# def GetAllPointsForRegression():
    
# Create File Paths

main_path = 'C:\\My files\\Dr Buzna\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','569IZ','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
#     i = 1
num_move_sp=[]
num_move_ps=[]
num_move_spp=[]
num_move_ph=[]
num_move_hs=[]
sp_mean_t=[]
sp_mean_dist = []
ps_mean_t=[]
ps_mean_dist = []
spp_mean_t=[]
spp_mean_dist = []
ph_mean_t=[]
ph_mean_dist = []
hs_mean_t=[]
hs_mean_dist = []
plate=[]
for i in range(0,17):
    plate.append(local_path2[i])
    local_path = local_path1 + local_path2[i]
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
    movement_ID_sp = sp.sp_part(sps_movement,trip_df, local_path2[i])
# Extract only 'sphs' trips, and then only 'sp' movement
    movement_ID_sp_sphs = sp_sphs.sp_part_sphs(sps_movement,trip_df, local_path2[i])          


# Read database of 'marginal_GPS_poins_of_movements.csv'
    marginal_file = '\\marginal_GPS_poins_of_movements.csv'
    marginal_df = pd.read_csv(joint_path + marginal_file)

# Call a function that filters movements initiated from active stations
    # filtered_move_sp = check.station_checker(movement_ID_sp,marginal_df)
    # sp_df = marginal_df[marginal_df.movement_id.isin(filtered_move_sp)]
    # filtered_move_ps = [i+1 for i in filtered_move_sp]
    # ps_df = marginal_df[marginal_df.movement_id.isin(filtered_move_ps)]
    # filtered_move_spp = check.station_checker(movement_ID_sp_sphs,marginal_df)
    # spp_df = marginal_df[marginal_df.movement_id.isin(filtered_move_spp)]
    # filtered_move_ph = [i+1 for i in filtered_move_spp] 
    # ph_df = marginal_df[marginal_df.movement_id.isin(filtered_move_ph)]   
    # filtered_move_hs = [i+2 for i in filtered_move_spp] 
    # hs_df = marginal_df[marginal_df.movement_id.isin(filtered_move_hs)] 
    # sp_df.to_csv(joint_path + '\\sp_sps.csv', index = False)
    # ps_df.to_csv(joint_path + '\\ps_sps.csv', index = False)
    # spp_df.to_csv(joint_path + '\\sp_sphs.csv', index = False)
    # ph_df.to_csv(joint_path + '\\ph_sphs.csv', index = False)
    # hs_df.to_csv(joint_path + '\\hs_sphs.csv', index = False)
    # num_move_sp.append(len(filtered_move_sp))
    # num_move_spp.append(len(filtered_move_spp))
    sp_sps = pd.read_csv(joint_path + '\\sp_sps.csv', index_col=0)
    ps_sps = pd.read_csv(joint_path + '\\ps_sps.csv', index_col=0)
    spp_sphs = pd.read_csv(joint_path + '\\sp_sphs.csv', index_col=0)
    ph_sphs = pd.read_csv(joint_path + '\\ph_sphs.csv', index_col=0)
    hs_sphs = pd.read_csv(joint_path + '\\hs_sphs.csv', index_col=0)
    sp_Travel_time, sp_Distance = tdf.Travel_df(sp_sps)
    ps_Travel_time, ps_Distance = tdf.Travel_df(ps_sps)
    spp_Travel_time, spp_Distance = tdf.Travel_df(spp_sphs)
    ph_Travel_time, ph_Distance = tdf.Travel_df(ph_sphs)
    hs_Travel_time, hs_Distance = tdf.Travel_df(hs_sphs)
    sp_mean_t.append(np.mean(sp_Travel_time)) 
    sp_mean_dist.append(np.mean(sp_Distance))
    ps_mean_t.append(np.mean(ps_Travel_time))
    ps_mean_dist.append(np.mean(ps_Distance))
    spp_mean_t.append(np.mean(spp_Travel_time))
    spp_mean_dist.append(np.mean(spp_Distance))
    ph_mean_t.append(np.mean(ph_Travel_time)) 
    ph_mean_dist.append(np.mean(ph_Distance))
    hs_mean_t.append(np.mean(hs_Travel_time)) 
    hs_mean_dist.append(np.mean(hs_Distance))
df_mean = pd.DataFrame({'Plate':plate,
                    'sp_sps mean time':sp_mean_t,
                    'sp_sps mean distance':sp_mean_dist,
                    'ps-sps mean time':ps_mean_t,
                    'ps_sps mean distance':ps_mean_dist,
                    'sp_sphs mean time':spp_mean_t,
                    'sp_sphs mean distance':spp_mean_dist,
                    'ph_sphs mean time':ph_mean_t,
                    'ph_sphs mean distance':ph_mean_dist,
                    'hs_sphs mean time':hs_mean_t,
                    'hs_sphs mean distance':hs_mean_dist
                    })
# df_mean.to_csv(main_path+'\\Upstream Vehicle Info'+'\\info_mean.csv')
# df = pd.DataFrame({'Plate':plate,
#                     '#sps':num_move_sp,
#                     '#sphs':num_move_spp,
#                     })

# df.to_csv(main_path+'\\Upstream Vehicle Info'+'info.csv')
# Call a function that returns Travel time and Distance for each vehicle
    # Travel_time, Distance = tdf(filtered_move, marginal_df)

# Create a new csv-file, putting [Travel time & Distance] inside the file
#     dict = {'Duration':Travel_time, 'Length_m':Distance}
#     joint_df = pd.DataFrame(dict)
#     regression_file = '\\Regression-sps-sp\\travel_time_regression.csv'
#     joint_df.to_csv(joint_path + regression_file, index = False)

# # Read csv-file containing only [Travel time & Distance]
#     scatter_points = pd.read_csv(joint_path + regression_file)

# Call function to give a scatter plot 
# draw_pls = pt(joint_path , regression_file)
        

