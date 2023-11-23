import numpy as np

def densify_curve(ps, delta):
    # densify_curve densifies the piecewise linear curve
    # qs = densify_curve(ps, delta)

    qs = np.zeros((1000, 2))  # Initialize an array to store the densified points
    counter = 0  # Initialize a counter to keep track of the number of densified points

    n = ps.shape[0]  # Number of vertices in the original curve

    for i in range(1, n):
        p1 = ps[i-1, :]  # Get the coordinates of the first vertex of the segment
        p2 = ps[i, :]    # Get the coordinates of the second vertex of the segment

        l = np.linalg.norm(p2 - p1)  # Compute the length of the segment

        ts = np.arange(0.0, l, delta/2) / l  # Create a vector of parameter values spaced by delta/2 along the segment
        ts = ts[:-1]  # Remove the last element to avoid duplicating the endpoints

        m = len(ts)  # Number of new points to be added along the segment

        for j in range(m):
            t = ts[j]  # Get the current parameter value
            counter += 1
            qs[counter, :] = p1 * (1 - t) + p2 * t  # Compute the densified point using linear interpolation

    qs = qs[:counter, :]  # Trim the array to remove unused pre-allocated space

    return qs
