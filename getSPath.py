# getSPath calculates points along the S-shaped curve. It takes the starting point p1, direction vector v1, length of the curve l12, and curvature parameters kappa1 and kappa2 as inputs. The function returns an array of (x, y) coordinates representing points along the S-shaped curve.

import numpy as np

def get_S_path(p1, v1, l12, kappa1, kappa2):
    # Calculate step size
    n=100
    dl = l12 / n
    
    # Initialize arrays to store x and y coordinates of points
    xs = np.zeros(n)
    ys = np.zeros(n)
    
    # Set the first point to the starting point p1
    xs[0], ys[0] = p1
    
    # Calculate points along the S-shaped curve
    for i in range(1, n):
        t = i * dl / l12
        xs[i] = p1[0] + v1[0] * (t - kappa1 * np.sin(2 * np.pi * t) / (2 * np.pi))
        ys[i] = p1[1] + v1[1] * (t + kappa2 * (1 - np.cos(2 * np.pi * t)) / (2 * np.pi))
    
    # Return the array of S-shaped curve points as (x, y) coordinates
    return np.column_stack((xs, ys))
