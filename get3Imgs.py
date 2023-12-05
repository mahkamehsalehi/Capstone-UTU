import cv2
from matplotlib import pyplot as plt

def get_3_imgs(m):
    vIn = 'data/printteri.mov'
    cap = cv2.VideoCapture(vIn) 
    
    imgs= []
    ret, img = cap.read()
    if img is None:
        return imgs # No frames read or error occurred
        
    sz = img.shape[:2]
    img0 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img1 = ~cv2.Canny(img0, 30, 100)
    imgs.append({'img0': img0, 'img1': img1, 'pss': [], 'corners': []})
    
    counter = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) # Get current frame position
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
            
        counter += int(cap.get(cv2.CAP_PROP_POS_FRAMES)) 
        if counter == m:
            if img is None: # Check if frame was read correctly
                break
                
            img0 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img1 = ~cv2.Canny(img0, 30, 100)
            imgs.append({'img0': img0, 'img1': img1, 'pss': [], 'corners': []})
            
    if img is None: # Check after the loop to see if there was an error reading frames
        return imgs 
        
    img0 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img1 = ~cv2.Canny(img0, 30, 100)
    imgs.append({'img0': img0, 'img1': img1, 'pss': [], 'corners': []})
    
    cap.release()
    return imgs
