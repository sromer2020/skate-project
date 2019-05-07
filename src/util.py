
def iterate_image(img, stride):
    for i in range(img.shape[0] // stride):
        for j in range(img.shape[1] // stride):
            yield (i * stride, j * stride)
