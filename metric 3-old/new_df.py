def plsprepare(df,df_specific, df_matched,platform,last_edge):
    # Create identifier Column based on trip pattern & movement_id & vehicle plate
    name = ['SP_'+str(df['movement_id'].iloc[0])+'_'+platform]*len(df_matched)
    prepared_df = pd.DataFrame(name, columns = ['name'])
    # Create EdgeID Column
    prepared_df['EdgeID'] = df_matched['Index'].values
    # Sum of traveled time over each non-missing Edge
    df1 = df_specific[['EdgeIndex','OSM_ID','datetime','TimeDiff', 'Highway']].copy()
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
        # print('!!!!!!!!!!!')
        # print('movement_id is: ',movement_id)
        # print('!!!!!!!!!!!!!')
        prepared_df['time_poly(s)'].iloc[0] = NaN
    # Create Column "Velocity"
    prepared_df['Length(m)(poly)'] = df_matched['Distance'].values
    speed = [i/j for i,j in zip(prepared_df['Length(m)(poly)'], prepared_df['time_poly(s)']) if j != NaN and j != 0]  # m/s
    prepared_df['Velocity(m/s)(poly)'] = speed
    # if prepared_df['Travelsal_time(s)(Poly)'].iloc[0] == 0:
    #     prepared_df['Velocity(m/s)(poly)'].iloc[0] == NaN

        # Fill Missing Values for Velocity by Interpolation
    prepared_df['Velocity(m/s)(poly)']=prepared_df['Velocity(m/s)(poly)'].interpolate()
    prepared_df['Velocity(m/s)(poly)'] = prepared_df['Velocity(m/s)(poly)'].fillna(method="bfill")
    # Create Column Hour_of_Day
    for index0, rowid in prepared_df.iterrows():
        for index, row in df_specific.iterrows():
            if rowid['EdgeID'] == row['EdgeIndex']:
                # Set hour of day
                prepared_df.loc[index0,'Hour_of_Day'] = int(row['datetime'][11:13])
                break

    # df1=df_specific.groupby(['EdgeIndex'])['speed'].mean().to_frame(name='speed').reset_index()
    # for m,num in prepared_df.iterrows():
    #     for inv, ro in df1.iterrows():
    #         if num['EdgeID'] == ro['EdgeIndex']:
    #             prepared_df.loc[m,'speed (m/s)'] =ro['speed']
    #             break

    # prepared_df['speed (m/s)']=prepared_df['speed (m/s)'].interpolate()

    prepared_df['Hour_of_Day']=prepared_df['Hour_of_Day'].fillna(method='ffill')
    triptime_real = prepared_df['time_poly(s)'].sum(skipna=True)
    prepared_df['triptime_real(s)']=triptime_real
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print('MAXIMUM TRAVERSAL TIME is: ',prepared_df['time_poly(s)'].max())
    # max_idx = prepared_df['time_poly(s)'].idxmax()
    # print('index is: ',max_idx)
    # print('Edge is: ',prepared_df['EdgeID'].iloc[max_idx])
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # if prepared_df['time_poly(s)'].max() > 2000:
    #     time.sleep(4)

    # filter movements that is not a mission due to long stop in the halfway (reful,repair,launch etc.)
    # prepared_df = prepared_df.drop(prepared_df[(prepared_df['time_poly(s)'] >600) & (prepared_df['Length(m)(poly)'] < 160)].index)
    if prepared_df[(prepared_df['time_poly(s)'] >600) & (prepared_df['Length(m)(poly)'] < 160)].index.any():
        del prepared_df 
        return None
    if prepared_df[(prepared_df['time_poly(s)'] >300) & (prepared_df['Length(m)(poly)'] < 350)].index.any():
        return None
    return prepared_df

import pandas as pd
import re
import numpy as np
import Distance_Calculator as haver
from numpy.core.numeric import NaN
import time