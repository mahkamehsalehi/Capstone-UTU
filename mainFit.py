import pickle
import numpy as np
import matplotlib.pyplot as plt

from fitCSC1 import fit_csc1
from getCSCpointsAndCSCerror import get_CSC_points
from getCrossing2 import getCrossing
from getOris import getNewOris
from mapPixels import map_pixels
import os.path

# 1) Initial values for the map
# 1.1) Size of the frames
fIn = './data/imgs.pkl'
if os.path.exists(fIn):
    with open(fIn, 'rb') as f:
        imgs1 = pickle.load(f)
    sz = imgs1[0]['img1']
    ni, nj = sz[0], sz[1]
else:
    print('Run mainEditCurves.m first (to get the marker groups done)')
    exit()

# Global variables
rMax = 677  # (pix)
thetaMax = (90 + 20) / 180 * np.pi  # (rad)
a = np.sin(thetaMax / 2) / rMax
b = rMax / thetaMax
c = np.array([994, 712])  # [712,994]  # center pixel

# r --> theta ==> r1 --> r2
def r12(r1):
    return 2 * np.arcsin(a * r1) * b

def r21(r2):
    return np.sin(r2 / b / 2) / a

# 3) Build the vector field v(p)
vs = np.zeros((1000, 4))
counterV = 0

# 2) Go through images and fit GCs
# 2.1) ori = 1,2,3 in each image, but in the collection of images,
# each ori category has to be unique
usedOris = []

for k in range(3):  # 3 images
    pss1 = imgs1[k]['pss']
    nCurves = len(pss1)  # raw image chessboard border curves

    # 2.2) Ori category uniqueness management
    allOris, uniqueOris = getNewOris(pss1)  # Assuming getOris exists
    nLen = len(uniqueOris)

    for i in range(nLen):
        uniqueOri = uniqueOris[i]
        inds = np.where(uniqueOri == allOris)[0]
        nInds = len(inds)

        if uniqueOri in usedOris:
            freeOriIndex = max(usedOris) + 1
            uniqueOris[i] = freeOriIndex

            for j0 in range(nInds):
                j = inds[j0]
                pss1[j]['ori'] = freeOriIndex

            usedOris.append(freeOriIndex)
        else:
            usedOris.append(uniqueOri)

    pss2 = [{'ps': map_pixels(pss1[i]['ps'], r12, c, sz, rMax),
             'ori': pss1[i]['ori']} for i in range(nCurves)]

    if True:
        plt.figure(2)
        plt.clf()
        plt.box(True)
        plt.axis('equal')
        for i in range(nCurves):
            ps = pss1[i]['ps']
            plt.plot(ps[:, 0], ps[:, 1], 'bo')
            ps = pss2[i]['ps']
            if ps:
                plt.plot(ps[:, 0], ps[:, 1], 'go')

        plt.xlabel('i')
        plt.ylabel('j')
        plt.title('Pixel Mapping')
        plt.show()

    # 2.3) Find individual GCs
    CSCs = np.zeros((nCurves, 4))  # <<aPixel, ori>, ...>
    pss3 = [{'ps': [], 'ori': 0, 'corners': []} for _ in range(nCurves)]

    for i in range(nCurves):
        ps = pss2[i]['ps']
        ori = pss2[i]['ori']

        if ps:
            aPixel, h, e, flag = fit_csc1(ps)  # Assuming fitCSC1 exists
            cps = get_CSC_points(aPixel, h)  # Assuming getCSCpoints exists
            pss3[i]['ps'] = cps
            pss3[i]['ori'] = ori
            CSCs[i, :] = [aPixel, h, ori]

    # 2.4) Record corner points of CSCs
    for i in range(len(imgs1[k]['corners'])):
        p1 = imgs1[k]['corners'][i]['p']
        j1j2 = imgs1[k]['corners'][i]['curves']
        j1, j2 = j1j2[0], j1j2[1]
        p2 = getCrossing(pss3[j1]['ps'], pss3[j2]['ps'], p1)  # Assuming getCrossing2 exists
        if p2:
            counterV += 1
            vs[counterV, :] = [p1[1], p1[0], p2[1] - p1[1], p2[0] - p1[0]]

vs = vs[:counterV, :]

# 3) Construct the vector field (from corner points to corner points)
plt.figure(1)
plt.clf()
plt.quiver(vs[:, 0], vs[:, 1], vs[:, 2], vs[:, 3], scale=0.1)
plt.axis('equal')
plt.xlabel('i')
plt.ylabel('j')
plt.title('Pixel Mapping Vector Field')
plt.show()

# Save vs to a text file
np.savetxt('./data/v.txt', vs)
