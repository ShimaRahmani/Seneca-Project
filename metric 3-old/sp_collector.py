def sp_part(movement_table, trip_df, vehicle_id):
    jj = 0
    pp = 0
    movement_ID = []
    for i in range(1,max(movement_table['x'])+1):

        # check if the trip is a selected one
        if i in trip_df.to_numpy('int'):
            pp += 1
        #print(i)
            count_number = (movement_table['x']==i).sum()

        # check if this is a sps movement
            if count_number==2:
                jj += 1

            #only take the sp part
                sp_part = movement_table.iloc[:,0][movement_table['x']==i].iloc[0]
                movement_ID.append(sp_part)
            #print('sp_part ',jj, ':',sp_part)

    return movement_ID