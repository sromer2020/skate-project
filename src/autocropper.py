import cv2

def iterate_image(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            yield (i, j)

class AutoCropper:
    
    def __init__(self, color_lower, color_upper, padding=10):
        """
        'color_lower' and 'color_upper' are arrays of [H, S, V]
        """
        self.color_lower = color_lower
        self.color_upper = color_upper
        self.padding = padding
        self.CROP_FAILURE_THRESHOLD = 10
        
    def _isolate_colors(self, hsv_frame, lower_colors, upper_colors):
        mask = cv2.inRange(hsv_frame, lower_colors[0], upper_colors[0])
        for i in range(1, len(lower_colors)):
            mask = cv2.bitwise_or(mask, 
                     cv2.inRange(hsv_frame, lower_colors[i], upper_colors[i]))
        return mask
    
    def _prepare_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = self._isolate_colors(img, self.color_lower, self.color_upper)
        return img
    
    def crop(self, img):
        src = img
        img = self._prepare_image(img)
        
        bounds_min = [img.shape[i] for i in [0, 1]]
        bounds_max = [0, 0]
        
        for i, j in iterate_image(img):
            if (img[i, j] == 255):
                bounds_min[0] = min(bounds_min[0], i)
                bounds_max[0] = max(bounds_max[0], i)
                bounds_min[1] = min(bounds_min[1], j)
                bounds_max[1] = max(bounds_max[1], j)
                
        for i in [0, 1]:
            bounds_min[i] = max(bounds_min[i] - self.padding, 0)
            bounds_max[i] = min(bounds_max[i] + self.padding, img.shape[i] - 1)
            
        if (bounds_max[0] - bounds_min[0] < self.CROP_FAILURE_THRESHOLD
                or bounds_max[1] - bounds_min[1] < self.CROP_FAILURE_THRESHOLD):
            return None, None

        return src[bounds_min[0]:bounds_max[0], bounds_min[1]:bounds_max[1]]
