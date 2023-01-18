
import pandas as pd
mov = ['Data_Prep_sp_sps2','Data_Prep_ps_sps2','Data_Prep_sp_sphs2','Data_Prep_ph_sphs2','Data_Prep_hs_sphs2']
weightdf1 = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weighdf_Data_Prep_sp_sps.csv')
weightdf2 = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weighdf_Data_Prep_ps_sps.csv')
weightdf3 = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weighdf_Data_Prep_sp_sphs.csv')
weightdf4 = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weighdf_Data_Prep_ph_sphs.csv')
weightdf5 = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weighdf_Data_Prep_hs_sphs.csv')
frames = [weightdf1,weightdf2,weightdf3,weightdf4,weightdf5]
weightdf = pd.concat(frames)
# weightdf.to_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weight_All.csv')
weightdf = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weight_All.csv')

weightdf['weight'] = [x.strip('[]').split(',') for x in weightdf['weight']] # convert string_list to real list
for i in range(0,len(weightdf)):
    b = weightdf['weight'][i]
    b = [gg.replace("'", "") for gg in b]
    a = [float(g) for g in b]
    weightdf['weight'][i] = a
df = weightdf.groupby(['EdgeID','Length(m)(poly)']).weight.apply(lambda g: [sum(i)/len(i) for i in (zip(*g))])
df = df.to_frame()
df = df.reset_index()
ass=1

#################
edgedf = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\edge node\\full egde node.csv')
# mov = ['Data_Prep_sp_sps2','Data_Prep_ps_sps2','Data_Prep_sp_sphs2','Data_Prep_ph_sphs2','Data_Prep_hs_sphs2']
# movee = ['Data_Prep_sp_sps3','Data_Prep_ps_sps3','Data_Prep_sp_sphs3','Data_Prep_ph_sphs3','Data_Prep_hs_sphs3']
# for i in range(0,5):
#     weightdf = pd.read_csv('D:\\trips\\metric3\\my\\weighdf_'+mov[i]+'.csv')
#     merger = pd.merge(weightdf,edgedf, left_on = 'EdgeID', right_on = 'Edge')
#     del merger['Edge']
#     merger.to_csv('D:\\trips\\metric3\\my\\weighdf_'+movee[i]+'.csv')

##################
# weightdf = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weight_All.csv')
df_avail = weightdf.loc[weightdf.groupby(["EdgeID"])["data avail"].idxmax()] 
df_avail.drop(df_avail.columns[0:3], axis=1, inplace=True)
weightdf.drop(weightdf.columns[0:3], axis=1, inplace=True)
df_avail1 = df_avail.iloc[:,0:4]
df_avail1.drop(df_avail1.columns[2], axis=1, inplace=True)
merger = pd.merge(df,df_avail1, on = 'EdgeID')
a = pd.merge(df,edgedf, left_on = 'EdgeID', right_on = 'Edge')
a.to_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weight_All5.csv')