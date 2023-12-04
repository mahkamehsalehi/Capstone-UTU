# ChatGPT:
# The provided MATLAB function triInterpolate2 performs linear interpolation of vector values vs defined at points DT.Location for query points qs within the triangulation DT. The function handles points both within and outside the convex hull defined by the triangulation.
# This function uses the pointLocation function to determine which triangles in the triangulation DT contain the query points qs. It then performs linear interpolation for points within the mesh and a simple weighted average for points outside the mesh. The weights are based on the inverse distances from the query points to the vertices of the nearest triangles.

import numpy as np
from scipy.spatial import Delaunay, cKDTree
import matplotlib.pyplot as plt

# Input
# qs = query points
# vs = defined at points ps = DT.points, vector values associated with each vertex in the Delaunay triangulation
# DT = Delaunay(ps) ?? Delaunay triangulation object

# Output
# v(q) = interpolated vector values at q \in qs 

def tri_interpolate2(DT, vs, qs):

    ti1 = DT.find_simplex(qs)      # Indices of simplices for each point
    inds1 = np.where(ti1 >= 0)[0]  # Points within the mesh = convex hull
    inds2 = np.where(ti1 < 0)[0]   # Points outside the mesh, index -1
    vqs = np.zeros((len(qs), 2))   # Array for storing the interpolated vector values

    
    # 1) Points within the mesh DT 
    ti1 = ti1[inds1]           # Just the points inside the mesh
    qs1 = qs[inds1]
    # Transforming the query points (qs) so that they are in the local coordinate system of the simplices containing them
    bc1 = DT.transform[ti1, :2].dot((qs1 - DT.transform[ti1, 2]).T).T  
    tInds = DT.simplices[ti1]  # len(tInds) x 3, each row represents a simplex, and the columns are the indices of its vertices
    triVals1 = vs[tInds]       # The rows from the vs array corresponding to tInds

    for dim in range(2):
        # performs a contraction (sum over a common index) between the two arrays triVals1 and bc1 along the second dimension, calculating the dot product between the vector values and the barycentric coordinates for the current dimension
        # DIMENSION ISSUE !!! 
        # ValueError: operand has more dimensions than subscripts given in einstein sum, but no '...' ellipsis provided to broadcast the extra dimensions.
        vqs[inds1, dim] = np.einsum('ij,ji->i', triVals1[:, :, dim], bc1.T)  # = interpolated values

    
    # 2) Points outside the mesh DT
    tree = cKDTree(DT.points)                # Create a tree object of the coordinates of the input points that were used to construct the triangulation 
    q2p = tree.query(qs[inds2], k=3)         # Find the indices and distances of the three nearest neighbors
    ws = 1 / q2p[0]                          # Inverse of the distances -> the weigths 
    ws /= np.sum(ws, axis=1)[:, np.newaxis]  # Final interpolated value is a weighted sum of the values associated with the nearest neighbors

    for i, ind in enumerate(inds2):
        vqs[ind] = np.dot(vs[q2p[1][i]], ws[i])  # Update interpolated vector value for points outside mesh in vqs

    return vqs

# Example usage:
ps = np.random.rand(10, 2)  # Example point cloud
vs = np.random.rand(len(ps), 2)  # Example vector values at points
DT = Delaunay(ps)
qs = np.random.rand(5, 2)  # Example query points
'''
# Call the function
vqs = tri_interpolate2(DT, vs, qs)

# Visualize the result
plt.plot(ps[:, 0], ps[:, 1], 'bo')  # Plot point cloud
plt.plot(qs[:, 0], qs[:, 1], 'rx')  # Plot query points
plt.quiver(qs[:, 0], qs[:, 1], vqs[:, 0], vqs[:, 1], color='g', angles='xy', scale_units='xy', scale=0.1)
plt.show()
'''