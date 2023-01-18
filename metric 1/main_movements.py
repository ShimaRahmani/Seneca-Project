import pandas as pd
import speed_calc as speed
import numpy as np

# def GetAllPointsForRegression():
    
# Create File Paths

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','569IZ','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
#     i = 1
sp_mean_speed=[]
ps_mean_speed=[]
spp_mean_speed=[]
ph_mean_speed=[]
hs_mean_speed=[]

plate=[]
for i in range(0,17):
    plate.append(local_path2[i])
    local_path = local_path1 + local_path2[i]
    joint_path = main_path + local_path
    # movementID_path = '\\selected_movements_id.csv'
    # movementID_path = joint_path + movementID_path
    # selected_trip_path = '\\results_selected_trips.csv'

    sp_sps = pd.read_csv(joint_path + '\\sp_sps.csv', index_col=0)
    ps_sps = pd.read_csv(joint_path + '\\ps_sps.csv', index_col=0)
    spp_sphs = pd.read_csv(joint_path + '\\sp_sphs.csv', index_col=0)
    ph_sphs = pd.read_csv(joint_path + '\\ph_sphs.csv', index_col=0)
    hs_sphs = pd.read_csv(joint_path + '\\hs_sphs.csv', index_col=0)
    sp_ave_speed, sp_TravelTime_list, sp_Length_list = speed.ave_speed_list(sp_sps)
    ps_ave_speed, ps_TravelTime_list, ps_Length_list = speed.ave_speed_list(ps_sps)
    spp_ave_speed, spp_TravelTime_list, spp_Length_list = speed.ave_speed_list(spp_sphs)
    ph_ave_speed, ph_TravelTime_list, ph_Length_list = speed.ave_speed_list(ph_sphs)
    hs_ave_speed, hs_TravelTime_list, hs_Length_list = speed.ave_speed_list(hs_sphs)

    sp_mean_speed.append(np.mean(sp_ave_speed)) 
    ps_mean_speed.append(np.mean(ps_ave_speed))
    spp_mean_speed.append(np.mean(spp_ave_speed))
    ph_mean_speed.append(np.mean(ph_ave_speed)) 
    hs_mean_speed.append(np.mean(hs_ave_speed)) 

    df_mean = pd.DataFrame({'Plate':plate,
                    'sp_sps mean speed':sp_mean_speed,
                    'ps-sps mean speed':ps_mean_speed,
                    'sp_sphs mean speed':spp_mean_speed,
                    'ph_sphs mean speed':ph_mean_speed,
                    'hs_sphs mean speed':hs_mean_speed,
                    })
    ass=1
    df_mean.to_csv(joint_path+'\\metric1'+'\\move_speed_mean.csv')
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
        

