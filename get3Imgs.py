import cv2
import numpy as np

def get_3_imgs(m):
    vIn = './data/printteri.mov'
    cap = cv2.VideoCapture(vIn)
    
    if not cap.isOpened():  # Check if video file opened successfully
        print("Error opening video file")
        return []

    imgs= []
    ret, frame = cap.read()
    img0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img1 = ~cv2.Canny(img0, 3, 1.8)
    imgs.append({'img0': img0.tolist(), 'img1': img0.tolist(), 'pss': [], 'corners': []})
    
    counter = m if cap.get(cv2.CAP_PROP_FRAME_COUNT) > m else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Ensure m doesn't exceed the total number of frames in the video
    
    while True:
        ret, frame = cap.read()
        if not ret or counter == 0:  # If end of file is reached or all frames have been stored
            break
            
        counter -= 1
        
        img0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img1 = ~cv2.Canny(img0, 3, 1.8)
        imgs.append({'img0': img0.tolist(), 'img1': img1.tolist(), 'pss': [], 'corners': []})
            
    cap.release()
    
    return imgs
