
def iterate_image(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            yield (i, j)
