def plsprepare(df_specific, df_matched,last_edge):
   
    prepared_df = pd.DataFrame()
    # Create EdgeID Column
    prepared_df['EdgeID'] = df_matched['Index'].values
    # Sum of traveled time over each non-missing Edge
    df1 = df_specific[['EdgeIndex','datetime','TimeDiff', 'Highway']].copy()
    # last edge shouldn't have contribution in time prediction due to irregularities
    df1=df1.drop(df1[df1['EdgeIndex']==last_edge].index)
    # last edge shouldn't have contribution in time prediction due to irregularities
    prepared_df=prepared_df.drop(prepared_df[prepared_df['EdgeID']==last_edge].index)
    # last edge shouldn't have contribution in time prediction due to irregularities
    df_matched=df_matched.drop(df_matched[df_matched['Index']==last_edge].index)
    if df1.empty:
        return None
    sec_list = [3000]
    df1['TimeDiff'].iloc[0] = 0
    for i in range(1,len(df1['TimeDiff'])):
        a = df1['TimeDiff'].iloc[i][10:15]
        sec = int(a[0:2])*60 + int(a[3:5]) 
        sec_list.append(sec)

    # prepared_df['Hour_of_Day'] = int(df1['datetime'].iloc[i+1][11:13])
    df1['TimeDiff0'] = sec_list
    df1['TimeDiff0'].iloc[0]=0
    new = df1.groupby(['EdgeIndex'])['TimeDiff0'].sum()
    dfnew = new.to_frame().reset_index()
    # Create a New Column "Traversal_Time"
    time_list = []
    for index0, rowid in prepared_df.iterrows():
        for index, row in dfnew.iterrows():
            if rowid['EdgeID'] == row['EdgeIndex']:
                time_list.append(row['TimeDiff0'])
                prepared_df.at[index0, 'time_poly(s)'] = row['TimeDiff0']
                break
    prepared_df.loc[prepared_df['time_poly(s)']==0,'time_poly(s)'] = np.nan
    if prepared_df['time_poly(s)'].iloc[0] == 0:
        prepared_df['time_poly(s)'].iloc[0] = NaN
    # Create Column "Velocity"
    prepared_df['Length(m)(poly)'] = df_matched['Distance'].values
    # Create Column Hour_of_Day
    for index0, rowid in prepared_df.iterrows():
        for index, row in df_specific.iterrows():
            if rowid['EdgeID'] == row['EdgeIndex']:
                # Set hour of day
                prepared_df.loc[index0,'Hour_of_Day'] = int(row['datetime'][11:13])
                break
    prepared_df['Hour_of_Day']=prepared_df['Hour_of_Day'].fillna(method='ffill')
    # filter movements that is not a mission due to long stop in the halfway (reful,repair,launch etc.)
    # prepared_df = prepared_df.drop(prepared_df[(prepared_df['time_poly(s)'] >600) & (prepared_df['Length(m)(poly)'] < 160)].index)
    if prepared_df[(prepared_df['time_poly(s)'] >600)].index.any():
        del prepared_df 
        return None
    if prepared_df[(prepared_df['time_poly(s)'] >300) & (prepared_df['Length(m)(poly)'] < 350)].index.any():
        return None
    return prepared_df

import pandas as pd
import numpy as np
from numpy.core.numeric import NaN
