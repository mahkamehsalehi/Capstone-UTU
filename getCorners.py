from getCrossing import get_crossing

def get_corners(pss):  # This function is used to find all corners in a given set of polygons
    corners = []       # This list will hold information about all corner points found
    counter = 0        # A counter variable that keeps track of how many corners have been found
    m = len(pss)       # The number of polygons in the input array 'pss'

    for i in range(m-1):  # This loop iterates over all pairs of polygons (excluding the last one)
        ps1 = pss[i]['ps']   # Extract the point set of the first polygon
        ori1 = pss[i]['ori'] # Extract the orientation of the first polygon

        for j in range(i+1, m):  # This loop iterates over all polygons that come after the current one
            ps2 = pss[j]['ps']   # Extract the point set of the second polygon
            ori2 = pss[j]['ori'] # Extract the orientation of the second polygon

            if ori2 != ori1:  # If the orientations of the two polygons are different, a chance for crossing might exist
                p = get_crossing(ps1, ps2)  # Call to function 'get_crossing' that returns any intersection points between ps1 and ps2

                if len(p) > 0:   # If there is at least one intersection point...
                    print("found crossing")
                    counter += 1    # Increase the corner count by one
                    corners.append({'p': p, 'curves': [i, j]})  # Add information about this corner to the list of corners

    return corners  # Return a list containing all found corners and their indices in the original polygon array
