import cv2 as cv

haar_front = cv.CascadeClassifier('sk8board_haar/front.xml')
haar_horizontal = cv.CascadeClassifier('sk8board_haar/horizontal.xml')
haar_right_diag = cv.CascadeClassifier('sk8board_haar/right_diag.xml')
haar_left_diag = cv.CascadeClassifier('sk8board_haar/left_diag.xml')
haar_vertical = cv.CascadeClassifier('sk8board_haar/vertical.xml')

def process(img):
    img = cv.resize(img, (0,0), fx=0.5, fy=0.5) 
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    sk8 = haar_front.detectMultiScale(gray, 1.3, 3)
    for (x, y, w, h) in sk8:
        img = cv.rectangle(img, (x , y), (x + w, y + h), (0, 0, 255), 2)
    
    sk8 = haar_horizontal.detectMultiScale(gray, 1.3, 3)
    for (x, y, w, h) in sk8:
        img = cv.rectangle(img, (x , y), (x + w, y + h), (0, 255, 0), 2)
        
    sk8 = haar_left_diag.detectMultiScale(gray, 1.3, 3)
    for (x, y, w, h) in sk8:
        img = cv.rectangle(img, (x , y), (x + w, y + h), (255, 0, 0), 2)
        
    sk8 = haar_left_diag.detectMultiScale(gray, 1.3, 3)
    for (x, y, w, h) in sk8:
        img = cv.rectangle(img, (x , y), (x + w, y + h), (0, 255, 255), 2)
        
    sk8 = haar_vertical.detectMultiScale(gray, 1.3, 3)
    for (x, y, w, h) in sk8:
        img = cv.rectangle(img, (x , y), (x + w, y + h), (255, 255, 0), 2)
    
    return img
    
cap = cv.VideoCapture('examples/example_skateboard_video.mp4')
while(1):
    ret, frame = cap.read()
    if not ret:
        break
    frame = process(frame)
    cv.imshow('skateboard', frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
