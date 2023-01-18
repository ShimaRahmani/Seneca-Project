# catch sp movement of an sphs trip

def sp_part_sphs(movement_table, trip_df, vehicle_id):
    jj = 0
    pp = 0
    movement_ID = []
    for i in range(1,max(movement_table['x'])+1):

        # check if 
        if i in trip_df.to_numpy('int'):
            pp += 1
        #print(i)
            count_number = (movement_table['x']==i).sum()

        # check if this is a sphs movement
            if count_number==3:
                jj += 1

            #only take the sp part
                sp_part = movement_table.iloc[:,0][movement_table['x']==i].iloc[0]
                movement_ID.append(sp_part)
            #print('sp_part ',jj, ':',sp_part)

    # print('********************')
    # print('Vehicle ID is: ', vehicle_id)
    # print('total number of trips: ', i)
    # print('number of accepted trips is: ', pp)
    # print('number of movements: ', len(movement_ID))
    return movement_ID