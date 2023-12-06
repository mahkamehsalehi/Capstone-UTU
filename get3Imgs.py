import cv2
import numpy as np

def get_3_imgs(m, n=3):  # m represents starting frame and n represents number of following frames
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
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
    counter = 0
    if m >= total_frames:   # If starting frame exceeds the total number of frames, return empty list
        print("Starting frame exceeds total number of frames")
        cap.release()
        return []

    for _ in range(m-1):  # Skip 'm' frames
        ret, _ = cap.read()
    
    while len(imgs) < n:   # Capture 'n' following frames
        if not ret or counter == total_frames - m + 1:    # If end of file is reached or all frames have been stored
            break
            
        img0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img1 = ~cv2.Canny(img0, 3, 1.8)
        imgs.append({'img0': img0.tolist(), 'img1': img1.tolist(), 'pss': [], 'corners': []})
        
    cap.release()
    
    return imgs
