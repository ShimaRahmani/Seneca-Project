
import pandas as pd
import datetime
from datetime import datetime
import re
import os

main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']

# Extract travel-time & distance of 'sp' movement from 'sps' trips
# Do it for all vehicles
#     i = 1
Speed_list = []
TravelTime_list = []
Length_list = []

for k in range(0,1):
    # Find the vehicle path where the map matched roads of this vehicle travels are accessible
    vehicle_path = main_path11 + local_path11[k]

    matchedroadall_file = [str(f) for f in os.listdir(vehicle_path) if 
                re.match(r'.*_all', f)]

    # for i in range(0,len(matchedroadall_file)):
    for i in range(0,4):
        full_path_all = vehicle_path+'\\'+matchedroadall_file[i]
        # print(full_path_all)
        df_all = pd.read_csv(full_path_all)

        df_all['HrMinSec'] = pd.to_datetime(df_all['datetime']).dt.strftime('%H:%M:%S')
        df_all['HrMinSec'] = pd.to_datetime(df_all['HrMinSec'] , format='%H:%M:%S')



        print(df_all.head())

        #Create a new column for time diff:
        df_all['TimeDiff'] = df_all['HrMinSec'].diff()

        try:
            df_all.to_csv(full_path_all)
        except PermissionError:
            continue
