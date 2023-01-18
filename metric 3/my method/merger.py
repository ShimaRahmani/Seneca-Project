
import pandas as pd
# mov = ['Data_Prep_sp_sps2','Data_Prep_ps_sps2','Data_Prep_sp_sphs2','Data_Prep_ph_sphs2','Data_Prep_hs_sphs2']
# weightdf1 = pd.read_csv('D:\\trips\\metric3\\my\\weighdf_Data_Prep_sp_sps2.csv')
# weightdf2 = pd.read_csv('D:\\trips\\metric3\\my\\weighdf_Data_Prep_ps_sps2.csv')
# weightdf3 = pd.read_csv('D:\\trips\\metric3\\my\\weighdf_Data_Prep_sp_sphs2.csv')
# weightdf4 = pd.read_csv('D:\\trips\\metric3\\my\\weighdf_Data_Prep_ph_sphs2.csv')
# weightdf5 = pd.read_csv('D:\\trips\\metric3\\my\\weighdf_Data_Prep_hs_sphs2.csv')
# frames = [weightdf1,weightdf2,weightdf3,weightdf4,weightdf5]
# weightdf = pd.concat(frames)
''''
weightdf = pd.read_csv('D:\\trips\\weight_All.csv')

weightdf['weight'] = [x.strip('[]').split(',') for x in weightdf['weight']] # convert string_list to real list
for i in range(0,len(weightdf)):
    b = weightdf['weight'][i]
    b = [gg.replace("'", "") for gg in b]
    a = [float(g) for g in b]
    weightdf['weight'][i] = a
finaldf = weightdf.groupby(['EdgeID']).weight.apply(lambda g: [sum(i)/len(i) for i in (zip(*g))])
ass=1
'''
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
weightdf = pd.read_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weight_All.csv')
merger = pd.merge(weightdf,edgedf, left_on = 'EdgeID', right_on = 'Edge')
merger.to_csv('D:\\work\\Dr Buzna\\R files\\data\\trips\\metric3\\weight_All3.csv')