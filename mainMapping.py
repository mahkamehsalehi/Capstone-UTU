import os
import pickle
import numpy as np
from scipy.spatial import Delaunay, distance
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

from get3Imgs import get_3_imgs
from getAdjacencyMatrix import get_adjacency_matrix
from triInterpolate2 import tri_interpolate_2
from generateViewPixels import generate_view_pixels
from bump import bump


# Load matrix v from file
fIn = 'data/v.txt'
fOut = 'data/pixelMap.npy'
v = np.loadtxt(fIn) #  v == <<p1, v(p1)>,...> where v(p1)= p2 - p1
#ps1, vs12 = v[:, :2], v[:, 2:] # ps1 = points, vs12 = vector field

# Initialize lense constants
# r12,r21 mappings
rMax = 677
thetaMax = (90 + 20) / 180 * np.pi
a = np.sin(thetaMax / 2) / rMax
b = rMax / thetaMax
c = np.array([712, 994])

r12 = lambda r1: 2 * np.arcsin(a * r1) * b
r21 = lambda r2: np.sin(r2 / b) / a

##############################
# Get frame size ni x nj
data_file = 'data/checkerboard_imgs.pkl'
data_dict_names = []

if (os.path.exists(data_file)):
	with open(data_file, 'rb') as f:
		imgs = pickle.load(f)
	
else:
    print('File does not exist, reading 3 frames')
    imgs = get_3_imgs(72)
    with open(data_file, 'wb') as f:
	    pickle.dump(imgs, f)
plt.imshow(imgs[0]['img1']) 
plt.show()

sz = np.array(imgs[0]['img1']).shape
ni, nj = sz[0], sz[1]
##############################

# Set hyperparameters
lambda_val = 0.5 #0.7 # The degree of Fourier truncation
bumpR = 20.0 # Support width of the radial function (pixels)


# Graph Fourier smoothing (not tuned)
ps1, vs12 = v[:, :2], v[:, 2:]
n = ps1.shape[0]
nEigen = round(lambda_val * n)

ls, tris = distance.cdist(ps1, ps1), Delaunay(ps1)
l0 = np.mean(ls) # Mean distance between natural (Voronoi) neighbors

# There is a version with [_,_,_,_]= ... , too
L0, _, _, _ = get_adjacency_matrix(tris.simplices, ps1, l0)

D, V = np.linalg.eig(L0)
lambdas = np.diag(D)
Vn = V[:, :nEigen]
# Regularized vector field (it's based on Laplacian matrix)
us12 = Vn @ Vn.T @ vs12

# Show regularized vector field
print('Drawing the vector field...')
plt.figure(1)
plt.clf()
plt.quiver(ps1[:, 0], ps1[:, 1], us12[:, 0], us12[:, 1])#, scale=0.1)
plt.axis('equal')
plt.xlabel('i')
plt.ylabel('j')
plt.title('Pixel Mapping Vector Field')
plt.show()

# Generalization to all pixes in img1 (the view circle)
# qs = pixel coordinates = view area pixels
# inds1 = qs' corresponding indices = indices of the view area pixels
inds1, qs = generate_view_pixels(c, rMax, ni, nj)
nq = qs.shape[0]

# Use Delaunay triangulation (DT) to interpolate the smoothed vector field (us12) at query points qs
DT = Delaunay(ps1) # Limited by the convex hull
vs12dense = tri_interpolate_2(DT, us12, qs)
nv = vs12dense.shape[0] # All pixels generalized


# Inverse mapping v21
# Paavo: ps2= ps1; % img2 pixels (not instantiated to spare memory!)
# Paavo: ps1ref= ps1 + us12 (not instantiated to spare memory!)
# Compute distances ds between query points and their k-nearest neighbors.

# initialize model
neigh = NearestNeighbors(n_neighbors = 4, metric='euclidean')
# train for getting distances between nearest neighbours and their indexes
neigh.fit(qs + vs12dense)
ds, inds2 = neigh.kneighbors(qs)

ws = bump(ds / bumpR) # ws = weights, A bump function based on the distances

ws = np.nan_to_num(ws, nan = 0.0)


for col in range(4):
    for row in range(nq):
        #ws[k, 3] = np.array([ws[k, 0] / np.sum(ws[k, 0:4]), ws[k, 1] / np.sum(ws[k, 0:4]), ws[k, 2] / np.sum(ws[k, 0:4]), ws[k, 3] / np.sum(ws[k, 0:4])])
        #ws[k, 2] = np.array([ws[k, 0] / np.sum(ws[k, 0:3]), ws[k, 1] / np.sum(ws[k, 0:3]), ws[k, 2] / np.sum(ws[k, 0:3])])
        #ws[k, 1] = np.array([ws[k, 0] / np.sum(ws[k, 0:2]), ws[k, 1] / np.sum(ws[k, 0:2])])
        #ws[k, 0] = np.array([ws[k, 0] / np.sum(ws[k, 0])])
        ws[row, col] = np.divide(ws[row, col], np.sum(ws[row, col]))


#np.divide(ws[:,k], np.sum(ws[:,k]))
ws = np.nan_to_num(ws, nan = 0.0)

# Delete the following 2 rows when not needed anymore
uni, counts= np.unique(np.round(ws,3), return_counts=True)

# Visualize the distribution of distances and weights in two subplots
if True:
    # A plot to tune bumpR
    # A plot for showing the distances
    plt.boxplot(ds)
    plt.yscale('log')
    plt.xlabel('k')
    plt.ylabel('||v(p)||')
    plt.title('Distance to k nearest pixel neighbors')
    plt.show()
    
    # A plot for showing the weights with different k values
    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Weight w of nearest pixel neighbors')
    i = 0

    for col in range(4):
        weights_for_diff_k = np.zeros((nq, col+1))
        for row in range(nq):
            weights_for_diff_k[row, :col+1] = np.divide(ws[row, :col+1], np.sum(ws[row, :col+1]))
        col_copy = col
        if col == 0 or col == 1:
            i = 0
            axs[i, col].boxplot(weights_for_diff_k)
            #axs[1].set_yscale('log')
            axs[i, col].set_xlabel('k:th neighbor')
            axs[i, col].set_ylabel('weights')
            axs[i, col].set_title('{} neighbors'.format(col))
        else:
            i = 1
            if col == 2:
                 col_copy = 0
            else:
                 col_copy = 1
            print(i, col_copy)
            axs[i, col_copy].boxplot(weights_for_diff_k)
            #axs[1].set_yscale('log')
            axs[i, col_copy].set_xlabel('k:th neighbor')
            axs[i, col_copy].set_ylabel('weights')
            axs[i, col_copy].set_title('{} neighbors'.format(col))
    plt.show()

# Save results
np.save(fOut, {'inds1': inds1, 'inds2': inds2, 'ws': ws})