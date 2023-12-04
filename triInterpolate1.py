# A fancy interpolation function
# ChatGPT: This code essentially performs linear interpolation for 
# points inside the convex hull and a weighted interpolation for 
# points outside the convex hull using the Delaunay triangulation.

import numpy as np
from scipy.spatial import Delaunay, delaunay_plot_2d
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

def tri_interpolate1(DT, qs, fs):
	# DT = a Delaunay triangulation object
    # triInterpolate returns interpolated scalar values f(q) at q \in qs
    # fs defined at points DT.Points
    # fqs= triInterpolate1(DT, qs, fs)
    # fs is related to ps (ps == DT.points)

    ti1 = DT.find_simplex(qs)
    inds1 = np.where(ti1 >= 0)[0]  # points within the mesh
    inds2 = np.where(ti1 < 0)[0]   # points outside the mesh
    fqs = np.zeros(qs.shape[0])

    # 1) points within the mesh DT (inside the convex hull)
    ti1 = ti1[inds1]
    tri_vals1 = fs[DT.simplices[ti1]]
    bc1 = DT.transform[ti1, :2].dot((qs[inds1] - DT.transform[ti1, 2]).T).T
    fqs[inds1] = np.einsum('ij,ij->i', bc1, tri_vals1)

    # 2) points outside the mesh DT (outside the convex hull)
    if len(inds2) > 0:
        ps = DT.points
        q2p = np.array(DT.query(qs[inds2], k=3, return_distance=False))
        ws = np.zeros((len(inds2), 3))
        for i in range(len(inds2)):
            q = qs[inds2[i]]
            psi = ps[q2p[i]]
            for j in range(3):
                pj = psi[j]
                ws[i, j] = 1 / np.linalg.norm(pj - q)
            ws[i, :] /= np.sum(ws[i, :])

            fqs[inds2[i]] = np.dot(fs[q2p[i]], ws[i, :])

    return fqs

# Example usage:
# Assuming DT (Delaunay triangulation) and qs, fs are defined
# DT = Delaunay(points)
# qs = query_points
# fs = values_at_points
# fqs = triInterpolate1(DT, qs, fs)