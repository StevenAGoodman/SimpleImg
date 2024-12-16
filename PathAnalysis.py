import numpy as np
from PIL import Image
import Filters

def computeGradients(img_pixels, width, height):
    gradients = []

    # Sobel kernels
    gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])




def detectPath(img_pixels):
    height, width = list(img_pixels.shape)[0:2] 

    # gaussian bluring
    img_pixels = Filters.applyGaussianBlur(img_pixels, 5)

    # compute gradients
    gradients = computeGradients(img_pixels, width, height)


img = Filters.initImg("./samples/coke1.jpg")
result = Image.fromarray(img)
result.show()