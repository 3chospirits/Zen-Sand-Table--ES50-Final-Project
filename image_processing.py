import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math

BW_THRESHOLD = 128


def flatten(l):
    return [item for sublist in l for item in sublist]

image_name = input("Image file: ") # get image from user
color = Image.open(image_name).convert("RGB") # load the image as RGB
gray = color.convert("L") # create a grayscale copy of image
bw = color.convert("1") # create a black and white copy of image
bw_arr = np.asarray(bw) # convert black and white image to numpy array
edges = bw_arr.copy() # create array to store edge-detected image
height, width = np.asarray(bw).shape # get size of image

# set up filter matrices to detect edges
vertical_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
horizontal_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
max_vertical_sum = sum([i for i in flatten(vertical_kernel) if i > 0])
max_horizontal_sum = sum([i for i in flatten(horizontal_kernel) if i > 0])

for row in range(3, height - 2):
    for col in range(3, width - 2):
        se = bw_arr[row - 1 : row + 2, col - 1 : col + 2] # get pixels to use for edge detection
        vertical_sum = (vertical_kernel * se).sum() / 4 # use vertical filter on pixel
        horizontal_sum = (horizontal_kernel * se).sum() / 4 # use horizontal filter on pixel
        sign = 1 if vertical_sum + horizontal_sum >= 0 else -1 # get sign of new pixel value
        value = sign * round(math.sqrt(vertical_sum**2 + horizontal_sum**2)) # get new pixel value
        edges[row, col] = value # set new pixel value

edges = Image.fromarray(np.array(edges / edges.max()).astype(dtype=bool)) # convert array to image
edges.save(image_name.split(".")[0] + "_edges.png") # save image

plt.imshow(edges)
plt.show()
