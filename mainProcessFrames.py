import numpy as np
import cv2

# Load pixel mapping data
fIn = '../data/pixelMap.npy'
try:
    data = np.load(fIn, allow_pickle=True).item()
    inds1 = data['inds1']
    inds2 = data['inds2']
    ws = data['ws']
except FileNotFoundError:
    print('Run mainMapping.m first (to get the pixel mapping found)')
    raise

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
vIn = '../data/printteri.mov'
vOut = '../data/output.avi'
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
        img2[0, inds1] = img1[0, inds1[inds2[:, 0]]]
    else:  # k == 2,3,4
        temp = np.zeros((1, nq))
        for i in range(k):
            temp = temp + ws[:, k-1] * img1[0, inds1[inds2[:, k-1]]]
        img2[0, inds1] = temp

    img2 = img2.reshape((nj, ni)).T
    cv2.imshow('Output', img2)
    temp = (img2 * 255).astype(np.uint8)
    v2.write(temp)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

v1.release()
v2.release()
cv2.destroyAllWindows()