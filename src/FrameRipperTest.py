import cv2
import numpy as np
import os
import pafy

url = "https://www.youtube.com/watch?v=2S7Yak00e6E"
v = pafy.new(url)
play = v.getbest(preftype="webm")

print(v.title)
print(v.duration)
print(v.rating)
print(v.author)
print(v.length)
print(v.keywords)
print(v.thumb)
print(v.videoid)
print(v.viewcount)

cap = cv2.VideoCapture(play.url) 

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
         #if no ret the break the loop
        break 
    # Saves image of the current frame in jpg file
    name = './data/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)   
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

