def ave_speed_list(sp_df):
    # Catch the travel time and duration of corresponding movemetns
    TravelTime_list = []
    Length_list = []
    for i in range(0,len(sp_df)):
        # row selection: build a dataframe only with sp movements


        # All units are in SI system
        TravelTime = float(sp_df['duration'].iloc[i])
        TravelTime_sec = TravelTime*60
        Length = float(sp_df['length_metres'].iloc[i])
        Length_m = Length

        TravelTime_list.append(TravelTime_sec)
        Length_list.append(Length_m)
        try:
            ave_speed = [i/j for i,j in zip(Length_list,TravelTime_list)]
        except ZeroDivisionError:
            continue
            
    return ave_speed, TravelTime_list, Length_list
    
