# WORK IN PROGRESS

import math
import os
import cv2

from filter_finder import FilterFinder
from image_filter import ImageFilter
from FrameRipper import create_data_directory

def main():
    path = 'Videos/Board1.mp4data'
    
    generator = FilterFinder()
    sk8_filter = ImageFilter(generator.get_default_filters())
    
    for subfolder in ['right_diag', 'left_diag', 'horizontal', 'vertical']:
        create_data_directory(path + '/' + subfolder)
    
    files = filter((lambda f: os.path.isfile(os.path.join(path, f))), 
                   os.listdir(path))[:100]
    for file_name in files:
        print(file_name)
        img = cv2.imread(path + '/' + file_name)
        mask = sk8_filter.get_aggregate_mask(img)
        sort(img, mask, '{}/{}/{}'.format(path, '{}', file_name))

def sort(img, mask, file_name):
    points = get_points(mask)
    lr = LinearRegression([p[1] for p in points], [p[0] for p in points])
    slope = lr.b1
    
    base_angle = 40
    
    btw_horiz_and_right_diag = define_slope(base_angle)
    btw_right_diag_and_vertical = define_slope(90 - base_angle)
    btw_vertical_and_left_diag = define_slope(90 + base_angle)
    btw_left_diag_and_horiz = define_slope(180 - base_angle)
    
    if slope > btw_horiz_and_right_diag and slope < btw_right_diag_and_vertical:
        file_name = file_name.format('right_diag')
        print(file_name)
        cv2.imwrite(file_name, img)
    elif slope > btw_vertical_and_left_diag and slope < btw_left_diag_and_horiz:
        file_name = file_name.format('left_diag')
        print(file_name)
        cv2.imwrite(file_name.format('left_diag'), img)
    elif slope > btw_left_diag_and_horiz and slope < btw_horiz_and_right_diag:
        file_name = file_name.format('horizontal')
        print(file_name)
        cv2.imwrite(file_name.format('horizontal'), img)
    else:
        file_name = file_name.format('vertical')
        print(file_name)
        cv2.imwrite(file_name.format('vertical'), img)
        
def define_slope(angle):
    rad_conv = math.pi / 180
    return math.sin(angle * rad_conv) / math.cos(angle * rad_conv)

def get_points(img):
    points = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (img[i, j] == 255):
                points.append((i, j))
    return points

class LinearRegression:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        x_ = sum(x) / len(x)
        y_ = sum(y) / len(y)
        
        xmx_ = [a - x_ for a in x]
        ymy_ = [a - y_ for a in y]
        
        xmx_sqr = [a**2 for a in xmx_]
        
        b1 = sum(a * b for a, b in zip(xmx_, ymy_)) / sum(xmx_sqr)
        
        #b0 = y_ - (b1 * x_)
        
        #self.b0 = b0
        self.b1 = b1
        
if __name__ == '__main__':
    main()
