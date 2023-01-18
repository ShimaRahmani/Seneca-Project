from math import isnan
# import movement_filter as checker
# import sp_collector as sp
# from datetime import datetime
# import travel_file4 as travel4
import numpy as np
import pandas as pd
import ast
import math

main_path = 'D:\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']
#**************###
mov = ['Data_Prep_sp_sps2','Data_Prep_ps_sps2','Data_Prep_sp_sphs2','Data_Prep_ph_sphs2','Data_Prep_hs_sphs2']
#**************### 
for move in mov:
    data = main_path + 'metric3\\my\\'+move+'.csv'
    df = pd.read_csv(data)
    #------------------------------------------------------
    res = df.groupby(['EdgeID','Length(m)(poly)','Hour_of_Day'])['time_poly(s)'].mean().reset_index()
    # # res = df.groupby(['EdgeID', 'Hour_of_Day','Length(m)(poly)'])['speed (m/s)'].mean().reset_index()
    summariz = res.groupby('EdgeID')['Hour_of_Day'].nunique()
    summariz = summariz.to_frame()
    summariz = summariz.rename(columns = {'Hour_of_Day':'data avail'})
    summariz = summariz.reset_index()
    df = res.copy()
    df['weight']=''
    for i in range(0,len(df)): 
        df.at[i,'weight']=[0]*24
    for ind, row in df.iterrows(): 
        df['weight'].iloc[ind][int(df['Hour_of_Day'].iloc[ind])]=df['time_poly(s)'].iloc[ind]

    finaldf = df.groupby(['EdgeID']).weight.apply(lambda g: [sum(i) for i in (zip(*g))])
    finaldf = finaldf.to_frame()
    finaldf = finaldf.reset_index()
    newdf = pd.merge(finaldf,df, on = 'EdgeID')
    df = newdf.drop_duplicates(subset='EdgeID', keep="first")
    finaldf = df[['EdgeID','Length(m)(poly)','weight_x']]
    finaldf = finaldf.reset_index(drop=True)
    finaldf = pd.merge(finaldf,summariz, on = 'EdgeID')
    listed = []
    mylist = []
    for ind,row in finaldf.iterrows():
        try:
            a = ast.literal_eval(str(row['weight_x']).replace('nan', '0'))
        except(TypeError, ValueError):
            continue
        if a[0]==np.nan:
            mylist = next(x for x in a if not isnan(x))
        if a[0]==0:
            b = np.array(a)
            if sum(b==0) == 24:
                finaldf.drop(ind)
                continue
            li_ = list(np.nonzero(b)[0])
            mylist=[a[li_[0]]]

        for i,num in enumerate(a):
            if num != 0:
                mylist.append(num)
            else:
                a[i] = mylist[-1]

        finaldf['weight_x'].iloc[ind] = a
    # finaldf.to_csv('D:\\trips\\metric3\\my\\weighdf_'+move+'.csv')
    ass=1


