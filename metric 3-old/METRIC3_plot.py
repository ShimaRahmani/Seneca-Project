#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'

speed_list_all=[]
length_list=[]
time_list=[]
err_list = []
errortime = pd.read_csv(main_path + 'metric3' + '\\errortime_speed.csv')
errortime = errortime['error time']

errortime =  [i for i in errortime]
plt.figure(figsize=(16,10), dpi= 80)
# sns.distplot(errortime, hist=True, kde=True, 
#              bins=int(180/5), color = 'darkblue', 
#              hist_kws={'edgecolor':'black'},
#              kde_kws={'linewidth': 4})
sns.kdeplot(errortime, shade=True, color="g", alpha=.7)
plt.rc('font', family='serif', serif = "Times New Roman")
# Labels
plt.title('Density Plot of time error based on metric 3', fontsize=32)
plt.legend()
plt.xlabel('Actual route prediction error (sec)',fontsize=30)
plt.ylabel('Frequency',fontsize=30)
dirc = 'D:\\work\\Dr Buzna\\R files\\data\\metrics pictures\\metric3\\'
plt.savefig(dirc+'All_vehicles'+'.pdf')
plt.show()
# %%
