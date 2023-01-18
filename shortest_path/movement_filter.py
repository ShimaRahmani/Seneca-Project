def station_checker(movement_ID, marginal_df):
    
    active_station =[42, 98, 115, 142, 176, 207, 223, 243, 270, 271, 272, 273, 286, 370]
    
#     active_station = [2, 22, 42, 43, 50, 93, 98, 99, 115, 120, 137, 142, 176, 184,
#                       206, 207, 223, 234, 242, 243, 257, 270, 271, 272, 273, 280, 
#                       286, 288, 314, 331, 335, 341, 359, 360, 370, 371]
    station = []
    # Find sp_movements that doesn not belong to an active center and make them 'None' in the movement_ID list
    for j in range(len(movement_ID)):
        sp_df = marginal_df.loc[marginal_df['movement_id']==movement_ID[j]]
        Closest_center = int(sp_df['first_position_closest_centre_id'])

        station.append(Closest_center)

        if (Closest_center not in active_station):
            # print(f'{i}: '+ 'Nooooooooooooooooooo')
            # print('movement_id is:', sp_df['movement_id'])
            # print('station id is: ', sp_df['first_position_closest_centre_id'])
            movement_ID[j] = None

        else:
            continue
            # print(f'{i}: '+ 'it is in active station list')
            # print('movement_id is:', sp_df['movement_id'])
            # print('station id is: ', sp_df['first_position_closest_centre_id'])
    removed_sp_count = movement_ID.count(None)
    # print(removed_sp_count)

    filtered_move = []
    None_list = []
    for val in movement_ID:
        if val != None:
            filtered_move.append(val)
        else:
            None_list.append(val)

    return filtered_move, removed_sp_count
##################################################################