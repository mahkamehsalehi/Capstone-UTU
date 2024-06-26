import os
import cv2
from insertP import insert_p
from getSegment import get_segment
from getP import get_p
from showImg import show_img
from getCorners import get_corners
from get3Imgs import get_3_imgs
from scipy.io import loadmat, savemat
import pickle

# !!!
# Data save and load not adjusted! They may not correspond to the Matlab
# data format in the Matlab version

# This code provides an interactive interface for editing images, including 
# adding and removing curves, adding and removing points, moving points, 
# setting orientation, and saving changes.

import numpy as np
import matplotlib.pyplot as plt

fData = './data/checkerboard_imgs.pkl' # Change the file path!

# Initializes the data by either loading it from a file (imgs.mat) or generating it 
# using the get3Imgs function
if (os.path.exists(fData)):
	with open(fData, 'rb') as f:
		imgs = pickle.load(f)
	
else:
    print('File does not exist, reading 3 frames')
    imgs = get_3_imgs(72)
    with open(fData, 'wb') as f:
	    pickle.dump(imgs, f)  
	

dMax = 100  # point tolerance for editing
k = 2  # img number was 3 but python index starts from 0 so changed to 2 

# Figure 1
# Visualizes the img0 and img1. Shows 6(?) images - 3 per img.

# Plotting each image in a subplot
for i, img_dict in enumerate(imgs):
    plt.subplot(len(imgs), 2, i*2+1)
    plt.imshow(img_dict['img0'], cmap='gray')
    plt.title('Image 0')
    
    plt.subplot(len(imgs), 2, i*2+2)
    plt.imshow(img_dict['img1'], cmap='gray')
    plt.title('Image 1')
#plt.show()

# Old plotting

##for k0 in range(len(imgs)): # Use len(imgs) to get the number of elements in imgs list
##    plt.subplot(2, 3, k0 + 1) 
##    plt.imshow(imgs[k0]['img0'], cmap='gray') # Added 'cmap='gray'' for grayscale image
##    plt.title(str(k0))
##    plt.subplot(2, 3, k0 + 3) # Changed from k0 + 3 to k0 + 4
##	  plt.imshow(imgs[k0]['img1'], cmap='gray') # Added 'cmap='gray'' for grayscale image
##    plt.title(str(k0))

plt.imshow(imgs[k]['img1'])
# Figure 2
#show_img(imgs[k]['img1'], k, imgs[k]['pss'])

quitModus = 8 # Quits the drawing
modus = 0 # Defines what operations are performed within the image depending on the user's choice
orientationMode = 0
changesMade = 0 # 1 if changes have been made and 0 if not
open_img = 0

# Registers keyinputs of the user. With this code the user can draw piecewise linear lines 
# and corner points on top of the fisheye image
while modus != quitModus:
	modus = 0
	while not 1 <= modus < quitModus + 1: # modus not in range(1, quitModus + 1):
		modus = int(input('1: +curve, 2: -curve, 3: +point, 4: -point, 5: +-point, 6: refresh+save, 7: set orientation, 8: quit '))
		if not 1 <= modus < quitModus + 1: # modus not in range(1, quitModus + 1):
			print('choose again')
	
	show_img(imgs[k]['img1'], k, imgs[k]['pss'], open_img)
	
	pss = imgs[k]['pss']
	match modus:
		case 1: # add points and draw a piecewise curve between the points
			print('1 curve+: press enter --> done')
			ps = np.array(plt.ginput(-1, timeout=0))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)

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
		
		case 2: # Remove a curve
			print('2 curve-: a far point --> no action')
			p = np.array(plt.ginput(1, timeout=0))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i0, j0 = get_p(pss, p, dMax)
			print('FLAG ETC:',flag, i0, j0)
			if flag:
				print('PSS: ',pss)
				ps = pss[i0]['ps']
				print('PS: ',ps)
				plt.plot(ps[:, 0], ps[:, 1], 'ro')
				plt.show()
				m = len(pss)
				inds = set(range(0, m)) - {i0}
				imgs[k]['pss'] = [pss[i] for i in inds]
				m -= 1
				if m == 0:  # this might never happen!
					imgs[k]['pss'] = []
				changesMade = 1
		
		case 3: # Add point to an existing curve
			#TODO: adding a point duplicates connections to endpoints. FIX
			print('3 add point at the center of the nearest segment')
			pNew = np.array(plt.ginput(1, timeout=0))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i, j = get_segment(pss, pNew, dMax)
			if flag:
				print(pNew)
				ps = pss[i]['ps']
				p1, p2 = ps[j, :], ps[j + 1, :]
				print(i, j)
				plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo')
				plt.plot(pNew[0][0], pNew[0][1], 'go')
				plt.plot([p1[0], pNew[0][0], p2[0]], [p1[1], pNew[0][1], p2[1]], 'g')
				plt.show()
				pss[i]['ps'] = insert_p(ps, j, pNew)
				changesMade = 1
			imgs[k]['pss'] = pss
		
		case 4: # Remove point from an existing curve
			print('4 remove the nearest point')
			pOld = np.array(plt.ginput(1, timeout=0))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i, j = get_p(pss, pOld, dMax)
			if flag:
				plt.plot(pOld[0][0], pOld[0][1], 'ro')
				ps = pss[i]['ps']
				inds = np.where(np.arange(ps.shape[0]) != j)[0]
				pss[i]['ps'] = ps[inds, :]
				changesMade = 1
			imgs[k]['pss'] = pss

		case 5: # Move point in an existing curve
			print('3 move the nearest point')
			pNew = np.array(plt.ginput(1, timeout=0))  # Registers a keyinput. NOTE: ginput() has weird coordinate system (*)
			flag, i, j = get_p(pss, pNew, dMax)
			if flag:
				pOld = pss[i]['ps'][j, :]
				pss[i]['ps'][j, :] = pNew
				changesMade = 1
			plt.plot(pOld[0], pOld[1], 'ro')
			plt.plot(pNew[0], pNew[1], 'go')
			imgs[k]['pss'] = pss

		case 6: # Refresh and save img
			open_img = 1
			show_img(imgs[k]['img1'], k, imgs[k]['pss'], open_img)
			open_img = 0

			if int(input('is it ok to save (0/1) ')):
				# If changes have been made, adds crosspoints into the image
				if 1:#changesMade: 
					print('img %d, adding the crosspoints' % k)
					imgs[k]['corners'] = get_corners(imgs[k]['pss'])
				print('saving img %d' % k)
				with open(fData, 'wb') as f:
					pickle.dump(imgs, f)
				# (*) ginput() coordinates must be fixed in the next phase
				# next phase is mainFit.m

		# When user sets the orientation, they are prompted to select a point on the image, 
		# and the orientation is set based on the user input.
		case 7: # set orientation
			orientationMode = 0
			while not 1 <= orientationMode < 4: # orientationMode not in range(1, 4):
				orientationMode = int(input('set orientation mode 0,1,2,3 (quit/mag/cya/yel)'))

			while orientationMode != 0:
				print('setting orientation, %d' % orientationMode)
				pNew = np.array(plt.ginput(1, timeout= 0))  # note: ginput() has weird coordinate system (*)
				print(pNew)
				flag, i, j = get_p(pss, pNew, dMax)
				if flag and imgs[k]['pss'][i]['ori'] == 0:
					imgs[k]['pss'][i]['ori'] = orientationMode
				elif not imgs[k]['pss'][i]['ori'] == 0:
					print("Curve already has a non-zero orientation!")
				else:
					orientationMode = 0

		case 8: # Quits the code
			print('quitting')