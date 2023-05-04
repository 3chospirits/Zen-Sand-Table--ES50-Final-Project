import numpy as np
import cv2
from skimage.morphology import skeletonize
from skimage import data
from skimage.util import invert

image_name = input("Image file: ") # get image from user
img = cv2.imread(image_name, 0) # load the image as grayscale

# create structuring elements
se1 = cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4)) 
se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
se3 = cv2.getStructuringElement(cv2.MORPH_CROSS,(12,12))

# must dilate first, or some images will lose all their lines
dilation = cv2.dilate(img, se1, iterations = 1)
erosion = cv2.erode(dilation, se1, iterations = 1) 

# use large SE to join nearby lines, if needed
dilation2 = cv2.dilate(erosion, se2, iterations = 1)
final = cv2.erode(dilation2, se2, iterations = 1)

# perform skeletonization
skeleton = np.array(skeletonize(final)).astype(np.uint8)*255 # make image single-width line

cv2.imwrite(image_name.split(".")[0] + "_eroded.png", erosion)
cv2.imwrite(image_name.split(".")[0] + "_dilated.png", dilation)
cv2.imwrite(image_name.split(".")[0] + "_dilated2.png", dilation2)
cv2.imwrite(image_name.split(".")[0] + "_processed.png", skeleton)


# img_final = Image.fromarray(result, "1")
# img_final.save(image_name.split(".")[0] + "_processed.png") # save image

# plt.imshow(img_final)
# plt.show()