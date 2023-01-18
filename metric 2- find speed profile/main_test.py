import pandas as pd
import numpy as np
import travelfile_test as travel
import math

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

weightdf = pd.read_csv(main_path+'\\weighed_velocity.csv')
speed_profile = pd.read_csv(main_path+'\\metric2\\SpeedProfile_RoadType_Movements.csv')
speed_profile0 = pd.read_csv(main_path+'\\metric2\\Speed_RoadType.csv')
EdgeRoad = pd.read_csv(main_path+'metric2\\Data_Prep_all_ForRoad.csv')
result = pd.merge(EdgeRoad, weightdf[['EdgeID','from_node','to_node','Length(m)(poly)']], how="left", on = 'EdgeID')
#**************###
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps']
#**************###   
roadf_list = []
roadf_move = []
for move in moves: 
    MAPE_list = []
    RMSE_list = []
    MAPE_dijk_list = []
    RMSE_dijk_list = []
    MAPE_length_list = []
    MAPE_naive_list = []
    RMSE_length_list = []   
    err_list = []
    sim_list = [] 
    y_list0 = []
    err_list_dijk = []
    err_naive_list=[] 
    RMSE_naive_list = []
    for i in range(0,15):
    # for i in range(0,2):
        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+move+'.csv'

        if move == 'sp_sps':
            speedf = speed_profile[['Highway','sp_road_speed']]
        elif move == 'sp_sphs':
            speedf = speed_profile[['Highway','spp_road_speed']]
        elif move == 'ps_sps':
            speedf = speed_profile[['Highway','ps_road_speed']]
        elif move == 'ph_sphs':
            speedf = speed_profile[['Highway','ph_road_speed']]
        elif move == 'hs_sphs':
            speedf = speed_profile[['Highway','hs_road_speed']]

        weight = pd.merge(result,speedf,on = 'Highway')
        weight = weight[weight['from_node'].notna()]
        weight = weight.drop_duplicates()
        weight['time'] = weight['Length(m)(poly)']/weight.iloc[:,-1]
        weight['time'] = weight['time'] 
        # Read File containing all sp (marginal) with their movement ids
        move_type = pd.read_csv(joint_path + movementID_path)
        # roadf,err,err_naive,MAPE,MAPE_naive,MAPE_dijk,RMSE,RMSE_naive,RMSE_dijk, similarity_list = travel.func(move_type,weight,vehicle_path,plate,speedf,speed_profile0)
        MAPE,MAPE_naive,excluded_trips,error_Dijk_list,y_list = travel.func(move_type,weight,vehicle_path,plate,speedf,speed_profile0)
        # roadf = pd.concat(roadf, axis=0, ignore_index = True)
        # roadf = roadf.groupby("Highway", as_index=True)[['mini_err','mini_err_naive']].mean()
        # roadf = roadf.reset_index()
        # err_list.append(err)
        y_list0.append(y_list)
        err_list_dijk.append(error_Dijk_list)
        # err_naive_list.append(err_naive)
        # sim = np.mean(similarity_list)
        # sim_list.append(sim)
        MAPE_list.append(MAPE)
        MAPE_naive_list.append(MAPE)
        # RMSE_list.append(RMSE)
        # RMSE_naive_list.append(RMSE)
        # MAPE_dijk_list.append(MAPE_dijk)
        # RMSE_dijk_list.append(RMSE_dijk)
        plate0 = local_path2[0:-1]
        # roadf_list.append(roadf)
    # roadf = pd.concat(roadf_list, axis=0, ignore_index = True)
    # roadf = roadf.groupby("Highway", as_index=True)[['mini_err','mini_err_naive']].mean()
    # roadf = roadf.reset_index()
    # roadf['move'] = move
    # roadf_move.append(roadf)
    # regression_df = pd.DataFrame({'Plate': plate0,
                                # 'MAPE original route':MAPE_list,
                                #'RMSE original route':RMSE_list,
                                # 'MAPE_naive original route':MAPE_naive_list,
                                #'RMSE_naive original route':RMSE_naive_list,
                                #'MAPE Dijk route':MAPE_dijk_list,
                                #'RMSE Dijk route':RMSE_dijk_list,
                                #'Similarity':sim_list
                                # })
    # flat = [item for sublist in err_list for item in sublist]
    # flatn = [item for sublist in err_naive_list for item in sublist]
    # df = pd.DataFrame({'Time Error [s]':flat,'Naive Time Error [s]':flatn})
    # df.to_csv(main_path+'\\metric2\\new'+'\\'+move+'_errortime.csv')
    # regression_df.to_csv(main_path+'\\metric2\\new\\'+move+'.csv')
    flatten = [item for sublist in err_list_dijk for item in sublist]
    flaten_y = [item for sublist in y_list0 for item in sublist]
    df_dijk = pd.DataFrame({'Time Error [s]':flatten,'Whole trip time':flaten_y})
    df_dijk.to_csv(main_path+'\\metric2\\'+move +'_dijk_errortime.csv')
# roadf_move = pd.concat(roadf_move, axis=0, ignore_index = True)
# roadf_naive = roadf_move[['Highway','mini_err_naive']]
# roadf_naive = roadf_naive .groupby("Highway", as_index=True)[['mini_err_naive']].mean()
# roadf_naive = roadf_naive .reset_index()
# roadf_move.to_csv(main_path+'\\metric2'+'\\move_road1.csv')
# roadf_naive.to_csv(main_path+'\\metric2'+'\\naive_road1.csv')
ass=1