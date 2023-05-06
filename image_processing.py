import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
from skimage.morphology import skeletonize
from PIL import Image

BW_THRESHOLD = 128


def flatten(l):
    return [item for sublist in l for item in sublist]

def detect_edges(inf):
    color = Image.open(inf).convert("RGB") # load the image as RGB
    bw = color.convert("1") # create a black and white copy of image
    height, width = np.asarray(bw).shape # get size of image
    bw_arr = np.asarray(bw) # convert black and white image to numpy array
    edges = bw_arr.copy() # create array to store edge-detected image

    # create vertical and horizontal Sobel filters for edge detection
    vertical_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    horizontal_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    max_vertical_sum = sum([i for i in flatten(vertical_kernel) if i > 0])
    max_horizontal_sum = sum([i for i in flatten(horizontal_kernel) if i > 0])

    for row in range(3, height - 2):
        for col in range(3, width - 2):
            # get pixels to use for edge detection
            se = bw_arr[row - 1 : row + 2, col - 1 : col + 2]
            
            # use vertical and horizontal filters
            vertical_sum = (vertical_kernel * se).sum() / max_horizontal_sum
            horizontal_sum = (horizontal_kernel * se).sum() / max_vertical_sum
            
            # get and set new pixel value from vertical and horizontal sums and
            sign = 1 if vertical_sum + horizontal_sum >= 0 else -1
            value = sign * round(math.sqrt(vertical_sum**2 + horizontal_sum**2))
            edges[row, col] = value

    edges_pil = Image.fromarray(np.array(edges / edges.max()).astype(dtype=bool)) # convert array to image
    edges_pil.save(inf.split(".")[0] + "_edges.jpeg") # save image
    # plt.imshow(edges_pil)
    # plt.show()
    
    return edges

def adjust_lines(img, inf, cross, rect):
    # load the image as grayscale
    # img = cv2.imread(image_name, 0) 
    img = img.astype(np.uint8)*255 # convert image to uint8

    # create structuring elements
    se1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,tuple([int(i) for i in cross])) 
    se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,tuple([int(i) for i in rect]))

    # perform closing. Dilating first is necessary to prevent detected edges from being erased!
    dilation = cv2.dilate(img, se1, iterations = 1)
    erosion = cv2.erode(dilation, se1, iterations = 1) 

    # use large SE to join separated lines
    dilation2 = cv2.dilate(erosion, se2, iterations = 1)
    #final = cv2.erode(dilation2, se2, iterations = 1)

    # perform skeletonization
    skeleton = np.array(skeletonize(dilation2)).astype(np.uint8)*255 # make image single-width line

    cv2.imwrite("images/step1_dilated.jpeg", dilation)
    cv2.imwrite("images/step2_eroded.jpeg", erosion)
    cv2.imwrite("images/step3_dilated2.jpeg", dilation2)
    cv2.imwrite(inf.split(".")[0] + "_processed.jpeg", skeleton)


def main():
    inf = input("Image file: ")
    cross = input("Small SE size (two comma separated values): ").split(",")
    rect = input("Large SE size (two comma separated values): ").split(",")
    edge_img = detect_edges(inf)
    fully_processed_img = adjust_lines(edge_img, inf, cross, rect)

if __name__ == "__main__":
    main()