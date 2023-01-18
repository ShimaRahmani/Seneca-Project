def calc_time(df_specific):
    

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
  
    return df_new[1:]

import pandas as pd