def Travel_df(movement_ID):
    # Catch the travel time and duration of corresponding movemetns

    TravelTime = (movement_ID['duration']) #min
    Distance = (movement_ID['length_metres'])/1000 #km

    return TravelTime, Distance