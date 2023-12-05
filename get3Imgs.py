import cv2

def get_3_imgs(m):
   vIn = './data/printteri.mov'
   v = cv2.VideoCapture(vIn)

   imgs = {'img0': [], 'img1': [], 'pss': [], 'corners': []}

   # Read the first frame
   ret, img = v.read()
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   print('here')
   imgs['img0'].append(img)
   imgs['img1'].append(cv2.Canny(img, 0.03, 1.8))
   imgs['pss'].append([])
   imgs['corners'].append([])

   counter = 1
   while v.isOpened():
       ret, img = v.read()
       if not ret:
           break
       img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       if counter == m:
           imgs['img0'].append(img)
           imgs['img1'].append(cv2.Canny(img, 0.03, 1.8))
           imgs['pss'].append([])
           imgs['corners'].append([])
       counter += 1

   # Read the last frame
   imgs['img0'].append(img)
   imgs['img1'].append(cv2.Canny(img, 0.03, 1.8))
   imgs['pss'].append([])
   imgs['corners'].append([])

   return imgs