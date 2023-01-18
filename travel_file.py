def ave_speed_list(movement_ID, marginal_df):
    # Catch the travel time and duration of corresponding movemetns
    TravelTime_list = []
    Length_list = []
    for i in range(0,len(movement_ID)):
        # row selection: build a dataframe only with sp movements
        sp_df = marginal_df.loc[marginal_df['movement_id']==movement_ID[i]]

        # All units are in SI system
        TravelTime = float(sp_df['duration'])
        TravelTime_sec = TravelTime*60
        Length = float(sp_df['length_metres'])
        Length_m = Length

        TravelTime_list.append(TravelTime_sec)
        Length_list.append(Length_m)
        
    ave_speed = [(i/1000)/(j/3600) for i,j in zip(Length_list,TravelTime_list)]
    
    return ave_speed, TravelTime_list, Length_list