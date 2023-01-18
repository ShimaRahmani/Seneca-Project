def find_chunck(df_specific, df_id, EdgeIndex_unique):
    # STEP 4 of (travel_file2.py)

    try:
        # go to (matched_index.csv) and find location of first road ID of sp trip. it can be more than one loc in table
        List_StartEdgeID = df_id.loc[df_id['Index']==EdgeIndex_unique[0]].index.values

        j = 0
        df_sp_EdgeID_previous = list(range(0,100000))
        for i in range(0,len(List_StartEdgeID)):
            try:
                df_specific_id = df_id[(df_id.index >= List_StartEdgeID[i]) & (df_id.index <= List_StartEdgeID[i+1])]
            except IndexError:
                df_specific_id = df_id[(df_id.index >= List_StartEdgeID[i])]
            # to find the right chunck, all roads should exist in the chuck under investigation
            count = 0
            ind_df_id_previous=-1
            for j in EdgeIndex_unique:
                if j in df_specific_id['Index'].values:

                    ind_df_id = df_specific_id.index[df_specific_id['Index'] == j].tolist()
                    # print('the EDGE is: ',j, 'and its index in matched_id is: ',ind_df_id)
                    # print('previous index: ', ind_df_id_previous)

                    if len(ind_df_id) > 1:
                        if ind_df_id[0]>= ind_df_id_previous:
                            count += 1
                            # print('current index: ', ind_df_id[0])
                            # print('-------------------------------------------')
                            ind_df_id_previous = ind_df_id[0]  

                        else:  
                            if ind_df_id[1]> ind_df_id_previous:
                                count += 1
                                # print('current index: ', ind_df_id[0])
                                # print('-------------------------------------------')
                                ind_df_id_previous = ind_df_id[1]  
                    else:
                        if ind_df_id[0] > ind_df_id_previous:
                            # print('current index: ', ind_df_id[0])
                            # print('-------------------------------------------')
                            ind_df_id_previous = ind_df_id[0]
                            count += 1
            # if the right chunck is identified, make a new df with the right identified end time

            if count == len(EdgeIndex_unique):

                loci_final = df_specific_id.index[df_specific_id['Index']==EdgeIndex_unique[-1]].tolist()
                # df_sp_EdgeID = df_specific_id.loc[0:loci_final[0]]
                o = 0
                while o <= len(loci_final):
                    df_sp_EdgeID = df_specific_id.loc[0:loci_final[o]]
                    o += 1
                    if set(EdgeIndex_unique).issubset(df_sp_EdgeID['Index']):
                        # print(set(EdgeIndex_unique).issubset(df_sp_EdgeID['Index']))
                        break

                ################################
                # not only count is the same but also order has maintained!!!!!!!
                if len(df_sp_EdgeID) - len(df_specific) < len(df_sp_EdgeID_previous) - len(df_specific):
                    df_sp_EdgeID_final = df_sp_EdgeID
                    df_sp_EdgeID_previous = df_sp_EdgeID
                ################################

        return df_sp_EdgeID_final

    except:
        # print('No chunck does exist for jj: ',jj)
        return None
