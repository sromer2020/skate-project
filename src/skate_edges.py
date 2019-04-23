#Test Footage For Class

import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(cap.isOpened()):
    ret, frame = cap.read()

    vid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ret,th = cv2.threshold(vid,100,200,cv2.THRESH_BINARY)
    #th = cv2.adaptiveThreshold(vid,200,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,21)
    
    edges = cv2.Canny(th,100,200)
    
    cv2.imshow('frame',edges)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
