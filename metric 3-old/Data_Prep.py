from math import isnan
import movement_filter as checker
import sp_collector as sp
from datetime import datetime
import travel_file4 as travel4
import numpy as np
import pandas as pd
import ast
import math

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

#---------------------------------------------------
df0 = pd.read_csv(main_path+'\\Data_Prep_removedoutlier.csv')
# # df = All_df[pd.notnull(All_df['speed (m/s)'])]

# Calculate difference between Weight and mean of group
df0['diff'] = df0['Velocity(m/s)(poly)'].sub(df0.groupby(['EdgeID','Length(m)(poly)','Hour_of_Day'])['Velocity(m/s)(poly)'].transform('mean'))
# Calculate standard deviation of group
df0['std'] = df0.groupby(['EdgeID','Length(m)(poly)','Hour_of_Day'])['Velocity(m/s)(poly)'].transform('std')

# Remove rows (=edges) identified as outlier, beneficial for first edges of a trip with high variability in velocity
df = df0.loc[(np.abs(df0['diff']) <= df0['std'])]
# df.to_csv(main_path+'\\Data_Prep_removedoutlier.csv')
#------------------------------------------------------
res = df.groupby(['EdgeID', 'Hour_of_Day','Length(m)(poly)'])['Velocity(m/s)(poly)'].mean().reset_index()
# # res = df.groupby(['EdgeID', 'Hour_of_Day','Length(m)(poly)'])['speed (m/s)'].mean().reset_index()
# summariz = res.groupby('EdgeID')['Hour_of_Day'].nunique()
# s = summariz.value_counts().sort_values()
# res.to_csv(main_path+'\\res.csv')
# # df = pd.read_csv(main_path+'\\res.csv')
df = res.copy()
df['weight']=''
for i in range(0,len(df)): 
    df.at[i,'weight']=[0]*24
for ind, row in df.iterrows(): 
    df['weight'].iloc[ind][int(df['Hour_of_Day'].iloc[ind])]=df['Velocity(m/s)(poly)'].iloc[ind]
# # for ind, row in df.iterrows(): df['weight'].iloc[ind][int(df['Hour_of_Day'].iloc[ind])]=df['speed (m/s)'].iloc[ind]
# finaldf = df.groupby(['EdgeID'], as_index = False).weight.apply(lambda g: [sum(i) for i in list(zip(*g))])
finaldf = df.groupby(['EdgeID']).weight.apply(lambda g: [sum(i) for i in (zip(*g))])
finaldf = finaldf.to_frame()
# finaldf = finaldf.reset_index
# finaldf.to_csv(main_path+'\\r1.csv', index = False)
# finaldf =pd.read_csv(main_path+'\\r1.csv',index_col=None)
# newdf = pd.merge(finaldf,All_df, on = 'EdgeID', how = 'outer')
# finaldf['Length'] = finaldf['EdgeID'].map(All_df.set_index('EdgeID')['Velocity(m/s)(poly)'])
newdf = pd.merge(finaldf,df0, on = 'EdgeID')
df = newdf.drop_duplicates(subset='EdgeID', keep="first")
finaldf = df[['EdgeID','Length(m)(poly)','weight']]
finaldf = finaldf.reset_index(drop=True)
listed = []
for i in finaldf['weight'].values:
    non_zero = sum(1 for t in i if t != 0)
    listed.append(non_zero)
    # print(i)
finaldf['data avail'] = listed
# finaldf['weight'] = [x.strip('[]').split(',') for x in finaldf['weight']] # convert string_list to real list
# finaldf[finaldf['EdgeID']==222]['Length(m)(poly)'][0]
# s = finaldf.loc[126]
# finaldf = finaldf[158:159]
mylist = []
for ind,row in finaldf.iterrows():
    try:
        # a = ast.literal_eval(row['weight'])
        # a = ast.literal_eval(row['weight'].replace('nan', '0'))
        a = ast.literal_eval(str(row['weight']).replace('nan', '0'))
        # a=[0 if math.isnan(x) else x for x in a]
    except(TypeError, ValueError):
        continue
    if a[0]==np.nan:
        # print('First nan appeared!!!!!!')
        # print('index is: ',ind)
        mylist = next(x for x in a if not isnan(x))
    if a[0]==0:
        b = np.array(a)
        if sum(b==0) == 24:
            # print('No weight for Edge', row['EdgeID'],' index:', ind)
            # finaldf.drop(ind, inplace=True)
            finaldf.drop(ind)
            continue
        li_ = list(np.nonzero(b)[0])
        mylist=[a[li_[0]]]

    for i,num in enumerate(a):
        if num != 0:
            mylist.append(num)
        else:
            a[i] = mylist[-1]
        # print(a)

    finaldf['weight'].iloc[ind] = a

# finaldf.to_csv(main_path+'weighed_speed.csv')
# finaldf = pd.read_csv(main_path+'\\weighed_speed.csv')
# finaldf.to_csv(main_path+'weighed_velocity.csv')
ass=1


