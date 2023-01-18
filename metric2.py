from numpy.core.numeric import NaN


def errortime(marginal_df, df_sp_EdgeID,speed_profile):

    speed_list = []
    for index, row in df_sp_EdgeID.iterrows():
        if row['Highway'] in speed_profile['Highway'].unique():
            for indexx, roww in speed_profile.iterrows():
                if row['Highway'] == roww['Highway']:
                    row['Seg_ave_speed'] = roww['road_speed']
                    speed_list.append(roww['road_speed'])
        else:
            df_sp_EdgeID = df_sp_EdgeID.drop([index])

    try:
        df_sp_EdgeID['Seg_ave_speed'] = speed_list
        df_sp_EdgeID['Seg_travel_time'] = [i/j for i,j in zip(df_sp_EdgeID['Distance'],df_sp_EdgeID['Seg_ave_speed'])]

        Estimated_SP_TravelTime = df_sp_EdgeID['Seg_travel_time'].sum()   #sec

        real_time_hr = int(marginal_df['HrMin_end'].iloc[0][0:2])-int(marginal_df['HrMin_start'].iloc[0][0:2])
        real_time_min = int(marginal_df['HrMin_end'].iloc[0][3:5])-int(marginal_df['HrMin_start'].iloc[0][3:5])

        # For each sp trip we need a travel time comparison
        Real_SP_TravelTime = (real_time_hr*60 + real_time_min) * 60   #sec
        error_time = Estimated_SP_TravelTime - Real_SP_TravelTime    #sec

        df_sp_EdgeID.drop(['Surface','Transport Mode', 'Bridge','Tunnel','Rondabout'], axis = 1)
        df_sp_EdgeID['movement_id'] = marginal_df['movement_id'].iloc[0]
        return error_time, df_sp_EdgeID
    except:
        return None, df_sp_EdgeID




import pandas as pd