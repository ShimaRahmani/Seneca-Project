def calc_speed(df_specific, df_sp_EdgeID,speedf,speed_profile0):
    

    df = df_specific[['EdgeIndex','OSM_ID','datetime','TimeDiff', 'Highway']].copy()

    sec_list = [3000]
    df['TimeDiff'].iloc[0] = 0
    for i in range(1,len(df['TimeDiff'])):
        a = df['TimeDiff'].iloc[i][10:15]
        sec = int(a[0:2])*60 + int(a[3:5]) 
        sec_list.append(sec)
    df['TimeDiff0'] = sec_list

    adj_check = (df.EdgeIndex != df.EdgeIndex.shift()).cumsum()
    df_new = df.groupby(['EdgeIndex','Highway', adj_check], as_index=False, sort=False)['TimeDiff0'].sum()
    dist_list = []
    for index, row in df_new.iterrows():
        for index, rowid in df_sp_EdgeID.iterrows():
            if rowid['Index'] == row['EdgeIndex']:
                dist_list.append(rowid['Distance'])
                break
    df_new['Distance'] = dist_list
    df_new = pd.merge(df_new,speedf, how='left',on=['Highway'])
    df_new = pd.merge(df_new,speed_profile0, how='left',on=['Highway'])
    
    df_new['time_hat'] = df_new['Distance']/df_new.iloc[:,4]
    df_new['time_hat_naive'] = df_new['Distance']/df_new['road_speed']
    df_new['mini_err'] = df_new['TimeDiff0'] - df_new['time_hat']
    df_new['mini_err_naive'] = df_new['TimeDiff0'] - df_new['time_hat_naive']

    return df_new[1:]

import pandas as pd