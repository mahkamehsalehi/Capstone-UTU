import pickle
from networkx import is_empty
import numpy as np
import matplotlib.pyplot as plt
import os.path

from fitCSC1 import fit_csc1
from getCSCpointsAndCSCerror import get_CSC_points
from getCrossing2 import getCrossing
from getOris import getNewOris
from mapPixels import map_pixels


# 1) Initial values for the map
# 1.1) Size of the frames
fIn = './data/checkerboard_imgs.pkl'
if os.path.exists(fIn):
    with open(fIn, 'rb') as f:
        imgs1 = pickle.load(f)
    sz = imgs1[0]['img1']
    ni, nj = sz[0], sz[1]
else:
    print('Run mainEditCurves.m first (to get the marker groups done)')
    exit()

# Global variables
rMax = 677  # (pix) range of pixels from 674 to 680
thetaMax = (90 + 20) / 180 * np.pi  # (rad)
a = np.sin(thetaMax / 2) / rMax
b = rMax / thetaMax
c = np.array([994, 712])  # [712,994]  # center pixel [[993, 711],[994, 712],[995, 713]]
x_coordinates = [993, 994, 995]
y_coordinates = [711, 712, 713]
x_values = []
y_values = []
rMax_values = []
total_errors_from_runs = []
total_minimum_errors_from_runs = []

# 3) Build the vector field v(p)
vs = np.zeros((1000, 4))
counterV = 0

for x_coord in x_coordinates:

    for y_coord in y_coordinates:

        c = np.array([x_coord, y_coord])
        print("Testing with center pixel:", c)  
        for rMax in range(674, 681):
            x_values.append(x_coord)
            y_values.append(y_coord)
            rMax_values.append(rMax)
            a = np.sin(thetaMax / 2) / rMax
            b = rMax / thetaMax
            # r --> theta ==> r1 --> r2
            def r12(r1):
                return 2 * np.arcsin(a * r1) * b

            def r21(r2):
                return np.sin(r2 / b / 2) / a
            
            total_error = 0
            minimum_error = float('inf')
            usedOris = []

            for k in range(0,3):  # 3 images
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
                        'ori': pss1[i]['ori']} for i in range(nCurves) if i!=0]


                if True:
                    plt.figure(2)
                    plt.clf()
                    plt.box(True)
                    plt.axis('equal')
                    
                    for i in range(1, nCurves):
                        ps = pss1[i]['ps']
                        plt.plot(ps[:, 0], ps[:, 1], 'bo')
                        ps = pss2[i-1]['ps']
                        if ps.size != 0:
                            plt.plot(ps[:, 0], ps[:, 1], 'go')

                    plt.xlabel('i')
                    plt.ylabel('j')
                    plt.title('Pixel Mapping')
                    plt.show()

                # 2.3) Find individual GCs
                CSCs = np.zeros((nCurves-1, 4))  # <<aPixel, ori>, ...>
                pss3 = [{'ps': [], 'ori': 0, 'corners': []} for _ in range(nCurves-1)]
                all_errors = 0
                minimum_error = []
                for i in range(nCurves-1):
                    ps = pss2[i]['ps']
                    ori = pss2[i]['ori']

                    if ps.size != 0:
                        aPixel, h, e, l, flag = fit_csc1(ps)
                        print("Error: ",e)
                        total_error += e
                        minimum_error = min(minimum_error, e)  
                        cps = get_CSC_points(aPixel, h)  
                        pss3[i]['ps'] = cps
                        pss3[i]['ori'] = ori
                        CSCs[i] = [aPixel[0], aPixel[1], h, ori]

                total_errors_from_runs.append(total_error)
                total_minimum_errors_from_runs.append(minimum_error)

                # 2.4) Record corner points of CSCs
                print('Recording corner pointsof CSCs...')
                for i in range(len(imgs1[k]['corners'])):
                    p1 = imgs1[k]['corners'][i]['p']
                    j1j2 = imgs1[k]['corners'][i]['curves']
                    j1, j2 = j1j2[0]-1, j1j2[1]-1
                    p2 = getCrossing(pss3[j1]['ps'], pss3[j2]['ps'], p1)  
                    
                    if len(p2) != 0:
                        counterV += 1
                        vs[counterV, :] = [p1[1], p1[0], p2[1] - p1[1], p2[0] - p1[0]]

# 2) Go through images and fit GCs
# 2.1) ori = 1,2,3 in each image, but in the collection of images,
# each ori category has to be unique

vs = vs[:counterV, :]

# 3) Construct the vector field (from corner points to corner points)
print('Drawing the vector field...')
plt.figure(1)
plt.clf()
plt.quiver(vs[:, 0], vs[:, 1], vs[:, 2], vs[:, 3])#, scale=0.1)
plt.axis('equal')
plt.xlabel('i')
plt.ylabel('j')
plt.title('Pixel Mapping Vector Field')
plt.show()

# Save vs to a text file
np.savetxt('./data/v.txt', vs)

print("Total errors from runs:", total_errors_from_runs)
print("Total minimum errors from runs:", total_minimum_errors_from_runs)
print("X values:", x_values)
print("Y values:", y_values)
print("rMax values:", rMax_values)
