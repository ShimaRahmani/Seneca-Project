#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Speed_list,TravelTime_list,Length_list = par.param_extractor()

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                   '440HY','445LI','471IH','','580IZ','624KK',
                   '724HU','761GV','796ES','853KK','992JH']


speed_list_all=[]
length_list=[]
time_list=[]
err_list = []
# for i in range(1,2):
for i in range(0,17):
    if i == 9:
        continue
    else:
        local_path = local_path1 + local_path2[i]
        joint_path = main_path + local_path
        metric2_path = '\\metric2\\errortime.csv'
        path = joint_path + metric2_path
        df = pd.read_csv(path)
        errortime = df['errortime'].values

        # remove outliers: all time differences greater than 1000 sec
        error = [i for i in errortime if abs(i)<=500]
        error = [-i for i in errortime if abs(i)<=500]
        
        err_list.extend(error)

        # plt.figure(figsize=(16,10), dpi= 80)
        # sns.kdeplot(error, shade=True, color="g", alpha=.7)
        # plt.rc('font', family='serif', serif = "Times New Roman")
        # # Labels
        # plt.title('Density Plot of time error for vehicle %i' %(i+1), fontsize=32)
        # plt.legend()
        # plt.xlabel('Actual route prediction error (sec)',fontsize=30)
        # plt.ylabel('Frequency',fontsize=30)
        # dirc = 'D:\\work\\Dr Buzna\\R files\\data\\metrics pictures\\metric2\\'
        # plt.savefig(dirc+'%i' %(i+1)+'.pdf')
        # plt.show()
err_list =  [i for i in err_list]
plt.figure(figsize=(16,10), dpi= 80)
sns.kdeplot(err_list, shade=True, color="g", alpha=.7)
plt.rc('font', family='serif', serif = "Times New Roman")
# Labels
plt.title('Density Plot of time error for vehicle %i' %(i+1), fontsize=32)
plt.legend()
plt.xlabel('Actual route prediction error (sec)',fontsize=30)
plt.ylabel('Frequency',fontsize=30)
dirc = 'D:\\work\\Dr Buzna\\R files\\data\\metrics pictures\\metric2\\'
plt.savefig(dirc+'All_vehicles'+'.pdf')
plt.show()


# %%
