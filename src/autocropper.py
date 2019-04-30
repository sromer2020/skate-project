import cv2

def iterate_image(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            yield (i, j)

class AutoCropper:
    
    def __init__(self, threshold=225, padding=10, pre_crop=10):
        self.threshold = threshold
        self.padding = padding
        self.pre_crop = pre_crop
        self.CROP_FAILURE_THRESHOLD = 10
    
    def _prepare_mask(self, mask):
        # blur out some noise below "white" threshold
        mask = cv2.GaussianBlur(mask, (17, 17), 1500)
        return mask
    
    def crop(self, img, mask):
        # crop flat amound around edge
        img = img[self.pre_crop:-self.pre_crop, self.pre_crop:-self.pre_crop]
        mask = mask[self.pre_crop:-self.pre_crop, self.pre_crop:-self.pre_crop]
        mask = self._prepare_mask(img)
        
        bounds_min = [mask.shape[i] for i in [0, 1]]
        bounds_max = [0, 0]
        
        for i, j in iterate_image(mask):
            # mask is B&W, W is object of interest
            if mask[i, j] > self.threshold:
                bounds_min[0] = min(bounds_min[0], i)
                bounds_max[0] = max(bounds_max[0], i)
                bounds_min[1] = min(bounds_min[1], j)
                bounds_max[1] = max(bounds_max[1], j)
                
        for i in [0, 1]:
            bounds_min[i] = max(bounds_min[i] - self.padding, 0)
            bounds_max[i] = min(bounds_max[i] + self.padding, mask.shape[i] - 1)
        
        if (bounds_max[0] - bounds_min[0] < self.CROP_FAILURE_THRESHOLD
                or bounds_max[1] - bounds_min[1] < self.CROP_FAILURE_THRESHOLD):
            return None
        
        return img[bounds_min[0]:bounds_max[0], bounds_min[1]:bounds_max[1]]
