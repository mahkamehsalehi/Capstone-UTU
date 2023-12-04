import numpy as np
from scipy.spatial import Delaunay, distance
import matplotlib.pyplot as plt

from triInterpolate2 import tri_interpolate_2
from generateViewPixels import generative_view_pixels
from bump import bump
from generateViewPixels import generate_view_pixels

# Load matrix v from file
fIn = '../data/v.txt'
fOut = '../data/pixelMap.npy'
v = np.loadtxt(fIn) #  v == <<p1, v(p1)>,...> where v(p1)= p2 - p1
ps1, vs12 = v[:, :2], v[:, 2:] # ps1 = points, vs12 = vector field


# Initialize lense constants (vakiot in Finnish)
# r12,r21 mappings
rMax = 677
thetaMax = (90 + 20) / 180 * np.pi
a = np.sin(thetaMax / 2) / rMax
b = rMax / thetaMax
c = np.array([712, 994])

r12 = lambda r1: 2 * np.arcsin(a * r1) * b
r21 = lambda r2: np.sin(r2 / b) / a

# Get frame size ni x nj
fIn = '../data/imgs.npy'
imgs1 = np.load(fIn, allow_pickle=True)
sz = imgs1[0]['img1'].shape
ni, nj = sz[0], sz[1]

# Set hyperparameters
lambda_val = 0.5 # The degree of Fourier truncation
bumpR = 20.0 # Support width of the radial function (pixels)


# Graph Fourier smoothing (not tuned)
ps1, vs12 = v[:, :2], v[:, 2:]
n = ps1.shape[0]
nEigen = round(lambda_val * n)

ls, tris = distance.cdist(ps1, ps1), Delaunay(ps1)
l0 = np.mean(ls) # Mean distance between natural (Voronoi) neighbors
# There is a version with [_,_,_,_]= ... , too
L0, _, _, _ = getAdjacencyMatrix(tris.simplices, ps1, l0)

D, V = np.linalg.eig(L0)
lambdas = np.diag(D)
Vn = V[:, :nEigen]
# Smoothed vector field us12 (regularized vector field in Paavo's words)(it's based on Laplacian matrix)
us12 = Vn @ Vn.T @ vs12


# Generalization to all pixes in img1 (the view circle)
# qs = pixel coordinates = view area pixels
# inds1 = qs' corresponding indices = indices of the view area pixels
inds1, qs = generate_view_pixels(c, rMax, ni, nj)
nq = qs.shape[0]

# Use Delaunay triangulation (DT) to interpolate the smoothed vector field (us12) at query points qs
DT = Delaunay(ps1) # Limited by the convex hull
vs12dense = tri_Interpolate_2(DT, us12, qs)
nv = vs12dense.shape[0] # All pixels generalized


# Inverse mapping v21
# Paavo: ps2= ps1; % img2 pixels (not instantiated to spare memory!)
# Paavo: ps1ref= ps1 + us12 (not instantiated to spare memory!)
# Compute distances ds between query points and their k-nearest neighbors.
inds2, ds = distance.cdist(qs + vs12dense, qs, metric='euclidean'), knnsearch(qs + vs12dense, qs, k=4)
ws = bump(ds / bumpR) # ws = weights, A bump function based on the distances

for k in range(nq):
    ws[k, :] = ws[k, :] / np.sum(ws[k, :])

# Visualize the distribution of distances and weights in two subplots
if True:
    # A plot to tune bumpR
    fig, axs = plt.subplots(1, 2)
    axs[0].boxplot(ds)
    axs[0].set_yscale('log')
    axs[0].set_xlabel('k')
    axs[0].set_ylabel('||v(p)||')
    axs[0].set_title('Distance to k nearest pixel neighbors')

    axs[1].boxplot(ws)
    axs[1].set_yscale('log')
    axs[1].set_xlabel('k')
    axs[1].set_ylabel('w')
    axs[1].set_title('Weight w of nearest pixel neighbors')

# Save results
np.save(fOut, {'inds1': inds1, 'inds2': inds2, 'ws': ws})