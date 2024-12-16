import numpy as np
from PIL import Image
import math

def initImg(img_path: str):
    img = Image.open(img_path)
    img_pixels = np.array(img)
    return img_pixels
    
def applyStaticBlur(img_pixels, radius):
    height, width = list(img_pixels.shape)[0:2] 


    # create Integral Image
    integral_img = np.zeros((height + 1, width + 1, 3))
    for y in range(1, height + 1): 
        for x in range(1, width + 1): 
            integral_img[y, x] = img_pixels[y - 1, x - 1] + integral_img[y - 1, x] + integral_img[y, x - 1] - integral_img[y - 1, x - 1]

    # average surrounding pixels
    res_pixels = np.zeros((height, width, 3), dtype="uint8")
    for y in range(radius, height - radius): # ignore edge cases
        for x in range(radius, width - radius): # ignore edge cases
            surrounding_sum = integral_img[y + radius + 1, x + radius + 1] - integral_img[y + radius + 1, x - radius] - integral_img[y - radius, x + radius + 1] + integral_img[y - radius, x - radius]
            res_pixels[y, x] = surrounding_sum / (2 * radius + 1)**2

    return res_pixels

def gaussianKernel(sigma: int):
    diameter = sigma * 3
    kernel_1D = np.linspace(-(diameter // 2), diameter // 2, diameter)

    dnorm = lambda x, mu, sd: 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)
    for i in range(diameter):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)
 
    kernel_2D *= 1.0 / kernel_2D.sum()

    return kernel_2D

def applyGaussianBlur(img_pixels, sigma): 
    height, width = list(img_pixels.shape)[0:2] 

    # create 2d gaussian kernel
    kernel = gaussianKernel(sigma)
    kernel = kernel.reshape((len(kernel), len(kernel), 1))
    radius = math.floor(len(kernel) / 2)

    padded_image = np.zeros((height + (2 * radius), width + (2 * radius), 3))
    padded_image[radius:padded_image.shape[0] - radius, radius:padded_image.shape[1] - radius] = img_pixels

    # get surrounding points and apply gaussian kernel
        # TO DO: Make so that it ignores edge pix instead of border
    res_pixels = np.zeros((height, width, 3), dtype="uint8")
    for y in range(radius, height - radius):
        for x in range(radius, width - radius):
            surrounding_pixels = padded_image[y - radius : y + radius + 1, x - radius : x + radius + 1]
            res_pixels[y, x] =  np.sum(kernel * surrounding_pixels, axis=(0,1))

    return res_pixels
    

# img = initImg("./samples/coke1.jpg")
# for i in range(8):  
#     img = applyGaussianBlur(img, 3)
# result = Image.fromarray(img)
# result.show()