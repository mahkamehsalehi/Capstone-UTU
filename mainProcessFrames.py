import numpy as np
import cv2
import scipy.io
# Load pixel mapping data
fIn= 'data/pixelMap.mat'
data = scipy.io.loadmat(fIn)
inds1 = data['inds1']
inds1 = inds1.flatten() - 1 # MATLAB indexing starts from 1
inds2 = data['inds2']
inds2 = inds2 - 1 # MATLAB indexing starts from 1
ws = data['ws']

# k: number of reference pixels.
# k == 1: some granularity
# k == 2: would require randomizing the orientation of the pair of the reference pixels
# k == 3: a rather good quality
# k == 4: somewhat blurred for some applications
k = 3
nq = len(inds1)

if k == 2 or k == 3:
    for j in range(nq):
        ws[j, :k] = ws[j, :k] / np.sum(ws[j, :k])

# Video input and output
vIn = 'data/printteri.mov'
vOut = 'data/output.avi'
v1 = cv2.VideoCapture(vIn)
fps = v1.get(cv2.CAP_PROP_FPS)
v2 = cv2.VideoWriter(vOut, cv2.VideoWriter_fourcc(*'XVID'), fps, (int(v1.get(3)), int(v1.get(4))))

while v1.isOpened():
    ret, frame = v1.read()
    if not ret:
        break

    img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.0
    ni, nj = img1.shape
    img1 = img1.reshape(1, ni * nj)
    img2 = img1.copy()
    if k == 1:
        img2[0, inds1] = img1[0, inds2[:, 0]]
    else:
    # Iterate over the indices to avoid large memory allocation
     for i in range(nq):
          weighted_sum = 0
          for j in range(k):
              ind = inds2[i, j]  # Get the index for the current reference pixel
              weight = ws[i, j]  # Corresponding weight
              weighted_sum += weight * img1[0, inds1[ind]]  # Weighted pixel value
          img2[0, inds1[i]] = weighted_sum   

    img2 = img2.reshape((nj, ni)).T
    cv2.imshow('Output', img2)
    temp = (img2 * 255).astype(np.uint8)
    v2.write(temp)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

v1.release()
v2.release()
cv2.destroyAllWindows()
