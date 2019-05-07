import cv2

from util import iterate_image

__author__ = 'Thomas'

class AutoCropper:
    
    def __init__(self, img_stride=2, blur_size=17, blur_amt=1500, 
                 threshold=250, padding=10, pre_crop=10):
        """
        Parameters
        ----------
        img_stride : int
            skip every img_stride pixels when determining the cropping bounds.
        blur_size : int
            Blur filter width and height.
        blur_amt : int
            Gaussian blur strength.
        threshold : int
            Only consider white pixels above this threshold for the region of interest.
        padding : int
            Expand cropped area by padding on all four sides.
        pre_crop : int
            Flat crop around edges before autocropping.
        """
        self.img_stride = img_stride
        self.blur_size = blur_size
        self.blur_amt = blur_amt
        self.threshold = threshold
        self.padding = padding
        self.pre_crop = pre_crop
        # a copped image with height or width below this value indicates a failed crop
        self.CROP_FAILURE_THRESHOLD = 10
    
    def _prepare_mask(self, mask):
        # blur out some noise below "white" threshold
        # noise, for example, will blur too much with the black background
        # and will then not count towards the cropping bounds
        mask = cv2.GaussianBlur(mask, (self.blur_size, self.blur_size), self.blur_amt)
        return mask
    
    def crop(self, img, mask):
        # crop flat amound around edge
        if self.pre_crop != 0:
            img = img[self.pre_crop:-self.pre_crop, self.pre_crop:-self.pre_crop]
            mask = mask[self.pre_crop:-self.pre_crop, self.pre_crop:-self.pre_crop]
        mask = self._prepare_mask(mask)
        
        # min and max pixels found as cropping bounds
        bounds_min = [mask.shape[i] for i in [0, 1]]
        bounds_max = [0, 0]
        
        # find new boundaries of mask
        # should be the bounding box around the pixels that are the object of interest
        # which is the white area in the mask
        for i, j in iterate_image(mask, self.img_stride):
            # mask is B&W, W is object of interest
            if mask[i, j] > self.threshold:
                bounds_min[0] = min(bounds_min[0], i)
                bounds_max[0] = max(bounds_max[0], i)
                bounds_min[1] = min(bounds_min[1], j)
                bounds_max[1] = max(bounds_max[1], j)
        
        # add padding for each dimension
        for i in [0, 1]:
            bounds_min[i] = max(bounds_min[i] - self.padding, 0)
            bounds_max[i] = min(bounds_max[i] + self.padding, mask.shape[i] - 1)
        
        if (bounds_max[0] - bounds_min[0] < self.CROP_FAILURE_THRESHOLD
                or bounds_max[1] - bounds_min[1] < self.CROP_FAILURE_THRESHOLD):
            return None
        
        return img[bounds_min[0]:bounds_max[0], bounds_min[1]:bounds_max[1]]
