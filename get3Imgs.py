import cv2
import numpy as np

def get_3_imgs(m):
    vIn = './data/printteri.mov'
    cap = cv2.VideoCapture(vIn)
    
    if not cap.isOpened():  # Check if video file opened successfully
        print("Error opening video file")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
    if m > total_frames:   # If 'm' exceeds the total number of frames, return empty list
        print("'m' exceeds total number of frames")
        cap.release()
        return []

    imgs = []
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:    # If end of file is reached
            break

        if i == 0 or i == m - 1 or i == total_frames - 1:
            img0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img1 = ~cv2.Canny(img0, 3, 1.8)
            imgs.append({'img0': img0.tolist(), 'img1': img0.tolist(), 'pss': [{'ps':[], 'ori': 0}], 'corners': []})

    cap.release()
    return imgs
