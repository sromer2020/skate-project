import cv2
import numpy as np

# note: opencv hue is 0 - 179
lower_red1 = np.array([0, 50, 50]) # red near orange
upper_red1 = np.array([9, 255, 255])  
lower_red2 = np.array([168, 50, 50]) # red near purple
upper_red2 = np.array([179, 255, 255])

lower_red = np.array([lower_red1, lower_red2])
upper_red = np.array([upper_red1, upper_red2])

def isolate_colors(frame, hsv_frame, lower_colors, upper_colors):
    mask = cv2.inRange(hsv_frame, lower_colors[0], upper_colors[0])
    for i in range(1, len(lower_colors)):
        mask = cv2.bitwise_or(mask, 
                 cv2.inRange(hsv_frame, lower_colors[i], upper_colors[i]))
    return mask

def autocrop(img, padding):
    src = img
    img = isolate_colors(img, cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower_red, upper_red)
    
    height, width = img.shape[0], img.shape[1]
    xmin = width
    ymin = height
    xmax = 0
    ymax = 0
    
    for i in range(height):
        for j in range(width):
            if (img[i, j] == 255):
                xmin = min(xmin, j)
                ymin = min(ymin, i)
                xmax = max(xmax, j)
                ymax = max(ymax, i)
                
    xmin = max(xmin - padding, 0)
    ymin = max(ymin - padding, 0)
    xmax = min(xmax + padding, width - 1)
    ymax = min(ymax + padding, height - 1)
    
    cropped = src[ymin:ymax, xmin:xmax]
    cv2.rectangle(src, (xmin, ymin) , (xmax, ymax) , (0, 0, 0), 1)
    return src, cropped

img = cv2.imread('test.png')

img, cropped = autocrop(img, 10)

cv2.imshow('img', img)
cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
