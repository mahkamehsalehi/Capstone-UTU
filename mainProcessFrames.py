import os
import numpy as np
from scipy.io import loadmat
import cv2

fIn = 'data/pixelMap.mat'
data = loadmat(fIn)
inds1 = data['inds1'].flatten()
inds2 = data['inds2']
ws = data['ws']

# Normalize weights for k = 2 or 3
k = 3
nq = len(inds1)
if k in [2, 3]:
    for j in range(nq):
        ws[j, :k] = ws[j, :k] / np.sum(ws[j, :k])
        
# Video processing
vIn = 'data/printteri.mov'
vOut = 'data/output.avi'

# Create a VideoCapture object to read the video
cap = cv2.VideoCapture(vIn)

# Get video frame dimensions
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create a VideoWriter object to write the video
out = cv2.VideoWriter(vOut, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width, frame_height), False)
        
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale and normalize
    img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img1 = img1/255.0
    ni, nj = img1.shape
    img1 = img1.T.flatten()
    
    inds1 = inds1 - 1
    inds2 = inds2 - 1
    
    img2 = np.copy(img1)
    
    if k == 1:
        img2[inds1] = img1[inds1[inds2[:, 0]]]
    else:  # k == 2, 3, 4
        temp = np.zeros(nq)
        for i in range(k):
            temp += ws[:, i] * img1[inds1[inds2[:, i]]]
        img2[inds1] = temp
    img2 = np.copy(img1)
    img2 = np.reshape(img2, (nj, ni)).T  # Reshape and transpose back to original shape
    img2 = (img2 * 255).astype(np.uint8)  # Convert to uint8
    
    out.write(img2)  # Write the processed frame

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
