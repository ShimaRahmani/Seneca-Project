import travelfile_test as travel
import pandas as pd
import numpy as np

main_path = 'C:\\My files\\Dr Buzna\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'C:\\My files\\Dr Buzna\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

#**************###
mov = ['Data_Prep_sp_sps','Data_Prep_ps_sps','Data_Prep_sp_sphs','Data_Prep_ph_sphs','Data_Prep_hs_sphs']
# mov = ['Data_Prep_sp_sps','Data_Prep_ps_sps']
moves = ['sp_sps','ps_sps','sp_sphs','ph_sphs','hs_sphs'] 
# moves = ['sp_sps','ps_sps'] 
#**************### 
for ku in range(0,5): 
# for ku in range(1,2): 

    # Read database containing Edges with their hour-by-hour speed weight
    weightdf = pd.read_csv('C:\\My files\\Dr Buzna\\trips\\metric3\\weighdf_'+mov[ku]+'.csv')
    weightdf['weight'] = [x.strip('[]').split(',') for x in weightdf['weight']] # convert string_list to real list
    for ind, row in weightdf.iterrows():
        weightdf['weight'][ind] = [float(f) for f in row['weight']]

    MAPE_list = []
    RMSE_list = []
    MAPE_dijk_list = []
    RMSE_dijk_list = []
    err_list = []
    sim_list = [] 
    err_list_dijk = []
    y_list = []
    MAPE_list2 = []
    RMSE_list2 = []
    MAPE_dijk_list2 = []
    RMSE_dijk_list2 = []
    err_list_dijk2 = []
    err_list2 = []
    sim_list2 = [] 
    y_list2 = []
    y_list0 = []
    for i in range(0,15):
    # for i in range(0,2):
        plate = local_path2[i]
        vehicle_path = main_path11 + local_path11[i]
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        movementID_path = '\\'+moves[ku]+'.csv'
        move_type = pd.read_csv(joint_path + movementID_path)
    #********************************* End (Find SP-Trips ID)  ****************************************
    #**************************************************************************************************
        y_origin_list1,error_originali,error_Dijk_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list = travel.func(
            move_type,weightdf,vehicle_path,plate)
        # y_origin_list1,error_original1,y_origin_list2,error_original2,error_Dijk_list,MAPE,MAPE_dijk,RMSE,RMSE_dijk, similarity_list,error_Dijk_list2,MAPE2,MAPE_dijk2,RMSE2,RMSE_dijk2, similarity_list2= travel.func(
        # move_type,weightdf,vehicle_path,plate)
        # y_list,error_Dijk_list,error_Dijk_list2= travel.func(move_type,weightdf,vehicle_path,plate)
        y_list0.append(y_list)
        y_list.append(y_origin_list1)
        # err_list.append(error_original1)
        # y_list2.append(y_origin_list2)
        # err_list2.append(error_original2)
        err_list_dijk.append(error_Dijk_list)
        sim = np.mean(similarity_list)
        sim_list.append(sim)
        MAPE_list.append(MAPE)
        RMSE_list.append(RMSE)
        MAPE_dijk_list.append(MAPE_dijk)
        RMSE_dijk_list.append(RMSE_dijk)
        # err_list_dijk2.append(error_Dijk_list2)
        # sim2 = np.mean(similarity_list2)
        # sim_list2.append(sim2)
        # MAPE_list2.append(MAPE2)
        # RMSE_list2.append(RMSE2)
        # MAPE_dijk_list2.append(MAPE_dijk2)
        # RMSE_dijk_list2.append(RMSE_dijk2)
        plate0 = local_path2[0:-1]

    regression_df = pd.DataFrame({#'Plate': plate0,
                                'MAPE original route':MAPE_list,
                                'RMSE original route':RMSE_list,
                                'MAPE Dijk route':MAPE_dijk_list,
                                'RMSE Dijk route':RMSE_dijk_list,
                                'Similarity':sim_list
                                })
    # regression_df2 = pd.DataFrame({#'Plate': plate0,
    #                             'MAPE original route':MAPE_list2,
    #                             'RMSE original route':RMSE_list2,
    #                             'MAPE Dijk route':MAPE_dijk_list2,
    #                             'RMSE Dijk route':RMSE_dijk_list2,
    #                             'Similarity':sim_list2
    #                             })
    flaten_y = [item for sublist in y_list0 for item in sublist]
    # fla = [item for sublist in y_list for item in sublist]
    # flat = [item for sublist in err_list for item in sublist]
    # flat = [x for x in flat  if np.isnan(x) == False]
    # df1 = pd.DataFrame({'Time Error [s]':flat,'Whole trip time':fla})
    flatten = [item for sublist in err_list_dijk for item in sublist]
    df_dijk = pd.DataFrame({'Time Error [s]':flatten,'Whole trip time':flaten_y})
    df_dijk.to_csv(main_path+'\\metric3\\my\\newest_wednesday\\method1\\'+moves[ku]+'_dijk_errortime.csv')
    # df1.to_csv(main_path+'\\metric3\\my\\newest_wednesday\\method1\\'+moves[ku]+'_errortime1.csv')
    # regression_df.to_csv(main_path+'\\metric3\\my\\newest_wednesday\\method1\\'+moves[ku]+'.csv', index=False)

    # fla2 = [item for sublist in y_list2 for item in sublist]
    # flat2 = [item for sublist in err_list2 for item in sublist]
    # flatten2 = [item for sublist in err_list_dijk2 for item in sublist]
    # flat2 = [x for x in flat2  if np.isnan(x) == False]
    # df2 = pd.DataFrame({'Time Error [s]':flat2,'Whole trip time':fla2})
    # df_dijk2 = pd.DataFrame({'Time Error [s]':flatten2,'Whole trip time':flaten_y})
    # df_dijk2.to_csv(main_path+'\\metric3\\my\\newest_wednesday\\method2\\'+moves[ku]+'_dijk_errortime.csv')
    # df2.to_csv(main_path+'\\metric3\\my\\newest_wednesday\\method2\\'+moves[ku]+'_errortime2.csv')
    # regression_df2.to_csv(main_path+'\\metric3\\my\\newest_wednesday\\method2\\'+moves[ku]+'.csv', index=False)

ass=1