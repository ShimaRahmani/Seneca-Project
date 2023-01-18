def calc_speed(df_specific, df_sp_EdgeID):

    df = df_specific[['EdgeIndex','OSM_ID','datetime','TimeDiff', 'Highway']].copy()

    sec_list = [3000]
    df['TimeDiff'].iloc[0] = 0
    for i in range(1,len(df['TimeDiff'])):
        a = df['TimeDiff'].iloc[i][10:15]
        sec = int(a[0:2])*60 + int(a[3:5]) 
        sec_list.append(sec)
    df['TimeDiff0'] = sec_list

    adj_check = (df.EdgeIndex != df.EdgeIndex.shift()).cumsum()
    df_new = df.groupby(['Highway','EdgeIndex', adj_check], as_index=False, sort=False)['TimeDiff0'].sum()

    dist_list = []
    for index, row in df_new.iterrows():
        for index, rowid in df_sp_EdgeID.iterrows():
            if rowid['Index'] == row['EdgeIndex']:
                dist_list.append(rowid['Distance'])
                break
    # print('size match between df_new & distance_list: ',len(df_new)==len(dist_list))
    
    # time.sleep(3) # Sleep for 3 seconds

    df_new['Distance'] = dist_list
    # print('size match between df_new & distance_list: ',len(df_new)==len(dist_list))
    speed = [i/j for i,j in zip(df_new['Distance'], df_new['TimeDiff0']) if j != 0]  # m/s
    # print('size match between df_new & speed_list: ',len(df_new)==len(speed))
    # time.sleep(3) # Sleep for 3 seconds
    # try:
    df_new['road_speed'] = speed
    # except:
        # pass
    return df_new


import time