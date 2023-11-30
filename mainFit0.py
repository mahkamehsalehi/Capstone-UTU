import sys, os
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

# Inputs
# r1, r2 ?

# 1) initial values for the map
# 1.1) size of the frames

sys.path.append('../Codes')

# Load the image and unpack the shape
fIn = '../imgs.mat'
if os.path.exists(fIn):
    # Load MATLAB data
    mat_data = loadmat(fIn)
    # Access the 'imgs' structure
    imgs1 = mat_data['imgs']  
    sz = imgs1[0]['img1'].shape  # !!! wrong dimensions, array of 3 arrays
    ni, nj = sz[0], sz[1]
    # imgs == <<img0,img1,pss,corners>,...>
    # pss  == <<ps,ori>,...> ori \in {1,2,3}
    # corners == <<p,curves>,...>
    # curves == [i,j] (indices to 2 curves crossing at p)
else:
    print('run main0.py first (to get the marker groups done)')
    sys.exit()

# a loop should be here:
# rMax range, thetaMax range, c range

# 1.2) r12,r21 mappings
rMax = 677  # (pix)
thetaMax = (90 + 20) / 180 * np.pi  # (rad)
a = np.sin(thetaMax / 2) / rMax
b = rMax / thetaMax
c = np.array([994, 712])  # [712,994]; % center pixel

# r --> theta ==> r1 --> r2
def r12(r1):
    return 2 * np.arcsin(a * r1) * b

# theta --> r ==> r2 --> r1
def r21(r2):
    return np.sin(r2 / b / 2) / a

# 1.3) ori = 1,2,3 in each image, but in the collection of images,
# each ori category have to be unique
usedOris = []

for k in range(3):  # 3 images
    pss1 = imgs1[k]['pss']
    nCurves = len(pss1)  # raw image chessboard border curves

    # 1.3) ori category uniqueness management
    allOris, uniqueOris = np.unique([ps['ori'] for ps in pss1], return_inverse=True)
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

    pss2 = [{'ps': [], 'ori': 0, 'corners': []} for _ in range(nCurves)]  # ideal (equisolidity assumption) border curves
    pss3 = [{'ps': [], 'ori': 0, 'corners': []} for _ in range(nCurves)]  # ideal fit of GC curves to pss2

    for i in range(nCurves):
        pss2[i]['ps'] = mapPixels(pss1[i]['ps'], r12, c, sz, rMax)
        pss2[i]['ori'] = pss1[i]['ori']

    if 1:
        
        plt.figure(2)
        plt.clf()
        plt.box(True)
        plt.hold(True)

        for i in range(nCurves):
            ps = pss1[i]['ps']
            plt.plot(ps[:, 0], ps[:, 1], 'bo')

            ps = pss2[i]['ps']
            if ps:
                plt.plot(ps[:, 0], ps[:, 1], 'go')

        plt.axis('equal')
        plt.show()

    # 2) find individual GCs
    CSCs = np.zeros((nCurves, 4))  # <<aPixel, ori>, ...>

    for i in range(nCurves):
        ps = pss2[i]['ps']
        ori = pss2[i]['ori']

        if ps:
            aPixel, h, e, flag = fitCSC1(ps)
            cps = getCSCpoints(aPixel, h)
            pss3[i]['ps'] = cps
            pss3[i]['ori'] = ori

            CSCs[i, :] = [aPixel, h, ori]

    # 2.1) choose a common axis point per orientation category
    categories = [{'inds': [], 'aPixel': [], 'hs': []} for _ in range(3)]
    cColors = ['mo', 'co', 'yo']
    showInitialMatch = False

    if showInitialMatch:
        plt.figure(3)
        plt.subplot(2, 1, 1)
        plt.clf()
        plt.box(True)
        plt.hold(True)

    for ori in range(1, 4):
        inds = np.where(CSCs[:, 3] == ori)[0]
        aPixel = np.mean(CSCs[inds, :2], axis=0)
        hs = CSCs[inds, 2]

        categories[ori - 1]['inds'] = inds
        categories[ori - 1]['aPixel'] = aPixel
        categories[ori - 1]['hs'] = hs

        if showInitialMatch:
            plt.figure(3)
            plt.subplot(2, 1, 1)
            plt.hold(True)
            plt.plot(CSCs[inds, 0], CSCs[inds, 1], cColors[ori - 1])

    if showInitialMatch:
        plt.axis('equal')
        plt.grid(True)
        plt.title('axis pixels of orientation categories')
        plt.xlabel('i')
        plt.ylabel('j')
        plt.hold(False)

        plt.subplot(2, 1, 2)
        plt.box(True)
        plt.hold(True)

        for ori in range(1, 4):
            hs = categories[ori - 1]['hs']
            f, h = np.histogram(hs, bins=10)
            f = f / np.trapz(f, h)
            plt.plot(h, f)

        plt.xlabel('h')
        plt.ylabel('freq.')
        plt.title('distribution of h')

        plt.show()

# 2.2) make a final fit: one optimization task per category group