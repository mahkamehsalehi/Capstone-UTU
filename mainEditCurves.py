import os

import cv2

from insertP import insert_p
from getSegment import get_segment
from getP import get_p
from showImg import show_img
from getCorners import get_corners
from get3Imgs import get_3_imgs
from scipy.io import loadmat, savemat

# !!!
# Data save and load not adjusted! They may not correspond to the Matlab
# data format in the Matlab version

# This code provides an interactive interface for editing images, including 
# adding and removing curves, adding and removing points, moving points, 
# setting orientation, and saving changes.

import numpy as np
import matplotlib.pyplot as plt

fData = './data/imgs.mat' # Change the file path!

# Initializes the data by either loading it from a file (imgs.mat) or generating it 
# using the get3Imgs function
if (os.path.exists(fData)):
	imgs = loadmat(fData)['imgs']
	print(type(imgs[0]['img0']))
else:
    print('File does not exist, reading 3 frames')
    imgs = get_3_imgs(72)
    savemat(fData, {'imgs': imgs})

dMax = 100  # point tolerance for editing
k = 3  # img number


# Figure 1
# Visualizes the img0 and img1. Shows 6(?) images - 3 per img.
for k0 in range(3):
    plt.subplot(2, 3, k0 + 1) # ChatGPT gave k0 + 1 !!!ValueError: num must be 1 <= num <= 6, not 0 with k0 + 0!!!
    plt.imshow(imgs[k0]['img0'])
    plt.title(str(k0))
    plt.subplot(2, 3, k0 + 3) # ChatGPT gave k0 + 4
    plt.imshow(imgs[k0]['img1'])
    plt.title(str(k0))

plt.show()

# Figure 2
show_img(imgs[k]['img1'], k, imgs[k]['pss'])

quitModus = 8 # Quits the drawing
modus = 0 # Defines what operations are performed within the image depending on the user's choice
orientationMode = 0
changesMade = 0 # 1 if changes have been made and 0 if not

# Registers keyinputs of the user. With this code the user can draw piecewise linear lines 
# and corner points on top of the fisheye image
while modus != quitModus:
    modus = 0
    while not 1 <= modus < quitModus + 1: # modus not in range(1, quitModus + 1):
        modus = int(input('1: +curve, 2: -curve, 3: +point, 4: -point, 5: +-point, 6: refresh+save, 7: set orientation, 8: quit '))
        if not 1 <= modus < quitModus + 1: # modus not in range(1, quitModus + 1):
            print('choose again')

    pss = imgs[k]['pss']
match modus:
		case 1: # add curve
		#if modus == 1:  # add curve
			print('1 curve+: press enter --> done')
			ps = np.array(plt.ginput())  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)

			if ps.size != 0:
				if not pss:
					pss = [{'ps': np.array([]), 'ori': 0}]
				m = len(pss)
				m += 1
				pss.append({'ps': ps, 'ori': 0})
				plt.plot(ps[:, 0], ps[:, 1], 'go')
				plt.plot(ps[:, 0], ps[:, 1], 'g')
				changesMade = 1
			imgs[k]['pss'] = pss
		
		case 2: # Remove curve
		# elif modus == 2:  # remove curve
			print('2 curve-: a far point --> no action')
			p = np.array(plt.ginput(1))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i0, j0 = get_p(pss, p, dMax)
			if flag:
				ps = pss[i0]['ps']
				plt.plot(ps[:, 0], ps[:, 1], 'ro')
				m = len(pss)
				inds = set(range(1, m + 1)) - {i0}
				imgs[k]['pss'] = [pss[i] for i in inds]
				m -= 1
				if m == 0:  # this might never happen!
					imgs[k]['pss'] = []
				changesMade = 1
		
		case '3': # Add point
		# elif modus == 3:  # add point
			print('3 add point at the center of the nearest segment')
			pNew = np.array(plt.ginput(1))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i, j = get_segment(pss, pNew, dMax)
			if flag:
				ps = pss[i]['ps']
				p1, p2 = ps[j, :], ps[j + 1, :]
				plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo')
				plt.plot(pNew[0], pNew[1], 'go')
				plt.plot([p1[0], pNew[0], p2[0]], [p1[1], pNew[1], p2[1]], 'g')
				pss[i]['ps'] = insert_p(ps, j, pNew)
				changesMade = 1
			imgs[k]['pss'] = pss
		
		case '4': # Remove point
		# elif modus == 4:  # remove point
			print('3 remove the nearest point')
			pOld = np.array(plt.ginput(1))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i, j = get_p(pss, pOld, dMax)
			if flag:
				plt.plot(pOld[0], pOld[1], 'ro')
				ps = pss[i]['ps']
				inds = set(range(ps.shape[0])) - {j}
				pss[i]['ps'] = ps[list(inds), :]
				changesMade = 1
			imgs[k]['pss'] = pss

		case '5': # Move point
		# elif modus == 5:  # move point
			print('3 move the nearest point')
			pNew = np.array(plt.ginput(1))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i, j = get_p(pss, pNew, dMax)
			if flag:
				pOld = pss[i]['ps'][j, :]
				pss[i]['ps'][j, :] = pNew
				changesMade = 1
			plt.plot(pOld[0], pOld[1], 'ro')
			plt.plot(pNew[0], pNew[1], 'go')
			imgs[k]['pss'] = pss

		case '6': # Refresh and save img
		# elif modus == 6:  # refresh + save img
			show_img(imgs[k]['img1'], k, imgs[k]['pss'])
			if int(input('is it ok to save (0/1) ')):
				# If changes have been made, adds crosspoints into the image
				if changesMade:
					print('img %d, adding the crosspoints' % k)
					imgs[k]['corners'] = get_corners(imgs[k]['pss'])
				print('saving img %d' % k)
				savemat(fData, {'imgs': imgs})
				# (*) ginput() coordinates must be fixed in the next phase
				# next phase is mainFit.m

		# When user sets the orientation, they are prompted to select a point on the image, 
		# and the orientation is set based on the user input.
		case '7': # set orientation
		# elif modus == 7:  # set orientation
			orientationMode = 0
			while not 1 <= orientationMode < 4: # orientationMode not in range(1, 4):
				orientationMode = int(input('set orientation mode 0,1,2,3 (quit/mag/cya/yel)'))

			while orientationMode != 0:
				print('setting orientation, %d' % orientationMode)
				pNew = np.array(plt.ginput(1))  # note: ginput() has weird coordinate system (*)
				flag, i, j = get_p(pss, pNew, dMax)
				if flag:
					imgs[k]['pss'][i]['ori'] = orientationMode
				else:
					orientationMode = 0

		case '8': # Quits the code
		# elif modus == 8:  # quit
			print('quitting')