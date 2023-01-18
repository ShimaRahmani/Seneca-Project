def func(sp,plate,speed):
    err_list = []
    for jj in range(round(0.8*len(sp)),len(sp)):
    # for jj in range(round(0.8*len(sp)),round(0.9*len(sp))):
        # match the indeces of filtered movements
        df = sp.loc[sp.index==jj]
        TravelTime = float(df['duration'])
        if TravelTime > 40:
            continue
        TravelTime_sec = TravelTime*60
        Length = float(df['length_metres'])
        TravelTime_hat = Length/speed
        err = TravelTime_sec - TravelTime_hat
        err_list.append(err)
    return err_list


