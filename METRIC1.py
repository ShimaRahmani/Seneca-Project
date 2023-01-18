#%%

from statistics import mean
from numpy.core.fromnumeric import std
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import parameter_file as par


# Speed_list,TravelTime_list,Length_list = par.param_extractor()

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','569IZ','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']


speed_list_all=[]
length_list=[]
time_list=[]
for i in range(0,17):

    local_path = local_path1 + local_path2[i]
    joint_path = main_path + local_path
    metric1_path = '\\metric1\\time_length_speed.csv'
    path = joint_path + metric1_path
    df = pd.read_csv(path)
    speed = df['Speed_kmh'].values
    length = df['Length_m'].values
    time = df['TravelTime_sec'].values

    error1=[]
    estimated_time = [i/37 for i in length]
    error1 = [(j-i) for i,j in zip(time,estimated_time)]

    # remove outliers: all time differences greater than 1000 sec
    error = [i for i in error1 if abs(i)<=500]

    plt.figure(figsize=(16,10), dpi= 80)
    sns.kdeplot(error, shade=True, color="g", label="Cyl=4", alpha=.7)
    # Labels
    plt.title('Density Plot of time error for vehicle %i' %(i+1), fontsize=22)
    plt.legend()
    plt.xlabel('Actual route prediction error (sec)',fontsize=15)
    plt.ylabel('Frequency',fontsize=15)
    plt.show()

    speed_list_all.extend(df['Speed_kmh'].values)
    length_list.extend( df['Length_m'].values)
    time_list.extend(df['TravelTime_sec'].values)


# METRIC I: Calculate average speed of all vehicles for sp movement
from statistics import mean
fixed_ave_speed = mean(speed_list_all)

print('We are using a fixed average speed equalls: ',fixed_ave_speed)
# fixed_ave_speed = 37 #kmh
# Find the difference between real travel time and estimated travel time based on METRIC 1
error1=[]
estimated_time = [i/fixed_ave_speed for i in length_list]
error1 = [(j-i) for i,j in zip(time_list,estimated_time)]

# remove outliers: all time differences greater than 1000 sec
error = [i for i in error1 if abs(i)<=500]
print('mean of error is: ',mean(error),'and std is: ',std(error))
plt.figure(figsize=(16,10), dpi= 80)
sns.kdeplot(error, shade=True, color="g", label="Cyl=4", alpha=.7)
# Decoration
plt.title('Density Plot of time error', fontsize=22)
plt.legend()
plt.xlabel('Actual route prediction error (sec)',fontsize=15)
plt.ylabel('Frequency',fontsize=15)
plt.show()
# %%
