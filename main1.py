#this code performs image rectification on a given frame from a video by transforming marker points using polar-to-rectangular mappings. 
#The mappings are defined by the functions r12 and r21. 
#The results are stored in arrays ps1s and ps2s.
import numpy as np
import cv2

# Load video and read the first frame
v_in = '../data/cage.mov' 
cap = cv2.VideoCapture(v_in)
ret, img1 = cap.read()
sz = img1.shape[:2]
cap.release()

# Parameters for r12, r21 mappings
r_max = 677
theta_max = (90 + 20) / 180 * np.pi
a = np.sin(theta_max / 2) / r_max
b = r_max / theta_max
c = np.array([712, 994])  # center pixel

# r --> theta ==> r1 --> r2
def r12(r1):
    return 2 * np.arcsin(a * r1) * b

# r2 --> r1
def r21(r2):
    return np.sin(r2 / b / 2) / a

# Example plot for pixel radius mappings
if False:
    import matplotlib.pyplot as plt

    r1s = np.arange(0, r_max + 1)
    r2s = np.array([r12(r1) for r1 in r1s])
    r1s0 = np.array([r21(r2) for r2 in r2s])

    plt.figure(3)
    plt.plot(r1s, r2s, r2s, r1s0, r1s, r1s0)
    plt.axis('equal')
    plt.grid(True)
    plt.xlabel('orig. pixels')
    plt.ylabel('rectified pixels')
    plt.title('Pixel Radius Mappings')
    plt.legend(['1 --> 2', '2 --> 1', '1 --> 2 --> 1'])
    plt.show()

# Load marker data
f_data = '../data/imgs.npy' # Assumed format is NumPy array!
imgs = np.load(f_data, allow_pickle=True).item()

# Image rectification
k = 1  # Image being rectified
pss = imgs[k]['pss']
m = len(pss)

ps1s = [np.empty((0, 2)) for _ in range(3)]
ps2s = [np.empty((0, 2)) for _ in range(3)]