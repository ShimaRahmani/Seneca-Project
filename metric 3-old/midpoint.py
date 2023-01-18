def boxit(Geometry_data_path):

    with open(Geometry_data_path, "r") as fp:
        lines = fp.readlines()
        # result = {}
        data_list = []
        i=0
        for idx, ln in enumerate(lines):
            matched = re.findall(r'\d*',ln)
            if matched[0].isdigit():
                fidx = idx + int(matched[2])
                Geom = lines[idx+1:fidx+1]
                List_points = [i.strip().split(',') for i in Geom]
            
                paths = [re.sub("\s+", ",", i[0].strip()) for i in List_points]
                paths = [[float(x) for x in k.split(',')] for k in paths]

                # Compute the distance and the half of the distance for this polyline
                distance_line = get_distance_line(paths)
                middle_dist = distance_line / 2
                midpoint = get_point_at_distance(paths, middle_dist)
                # result[matched[0]] = midpoint
                if bool(midpoint):
                    data = [[matched[0], midpoint[0], midpoint[1]],distance_line]
                    data_list.extend(data)
        df = pd.DataFrame(data_list, columns = ['EdgeIndex', 'lon', 'lat','poly_length(m)'])  
    return df

            # Euclidean distance between two points
def get_distance(p1, p2):
    return sum([(x-y)**2 for (x,y) in zip(p1, p2)]) ** (0.5)

# Length of a polyline by summing the length of its segments
def get_distance_line(line):
    total = 0
    for start_index in range(len(line) - 1):
        stop_index = start_index + 1
        total += get_distance(line[start_index], line[stop_index])
    return total

# Compute the target point at `_target_dist`
# of `p1` along the p1-p2 segment
def _get_pt_at_dist(p1, p2, _target_dist):
    # Define the vector from p1 to p2
    vx = p2[0] - p1[0]
    vy = p2[1] - p1[1]
    # Compute the length of the vector
    lv = (vx ** 2 + vy ** 2) ** 0.5
    # Compute the unit vector (the vector with length 1)
    nv = [vx / lv, vy / lv]
    # Compute the target point
    return [
        p1[0] + nv[0] * _target_dist,
        p1[1] + nv[1] * _target_dist,]

# Get a point at a specific distance on a Polyline
# - 1st step to find the two points enclosing the `target_dist
# - 2nd step to calculate the midpoint along the 2 previously selected points
def get_point_at_distance(line, target_dist):
    sum_dist = 0
    for start_index in range(len(line) - 1):
        stop_index = start_index + 1
        n_dist = get_distance(line[start_index], line[stop_index])
        if sum_dist + n_dist > target_dist:
            # We have found the two enclosing points
            p1, p2 = line[start_index], line[stop_index]
            _target_dist = target_dist - sum_dist
            return _get_pt_at_dist(p1, p2, _target_dist)
        else:
            sum_dist += n_dist

    # raise ValueError("target distance is greater than the length of the line")



import re
import pandas as pd