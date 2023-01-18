
import pandas as pd


main_path = 'D:\\work\\Dr Buzna\\R files\\data\\trips\\'
local_path1 = 'h_300_c300_trips_KE_'
local_path2 = ['110JG','111IZ','125KK','171LF','278JI','417IZ',
                '440HY','445LI','471IH','580IZ','624KK',
                '724HU','761GV','796ES','853KK','992JH']

main_path11 = 'D:\\work\\Dr Buzna\\R files\\data\\map_matching2\\Export_Vehicle_'
local_path11 = ['1','2','3','4','5','6','7','8','9',
                '11','12','13','14','15','16','17']
df_list = []
for k in range(10,14):

# for k in range(0,len(local_path11)):
    # Find the vehicle path where the map matched roads of this vehicle travels are accessible
    vehicle_path = main_path11 + local_path11[k]
    a = pd.read_csv(vehicle_path+'\\whole_graph_edges.atr')
    d = pd.read_csv(vehicle_path+'\\whole_graph_edges_incid.txt')
    a.columns = ['unkown']
    df = pd.concat([a['unkown'].str.split(' ', expand=True)], axis=1)
    df['EdgeID'] = df.iloc[:,0]
    df['Highway'] = df.iloc[:,3]
    df = df.iloc[:,10:12]
    df_list.append(df)
Data_prep_All = pd.concat(df_list, axis=0, ignore_index = True)
ass=1