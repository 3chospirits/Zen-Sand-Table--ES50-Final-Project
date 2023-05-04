import numpy as np
import cv2
from skimage.morphology import skeletonize
from skimage import data
from skimage.util import invert

image_name = input("Image file: ") # get image from user

img = cv2.imread(image_name, 0)
# ret,thresh = cv2.threshold(img,64,255,cv2.THRESH_BINARY)
# kernel = np.ones((5, 5), np.uint8)
# erode = cv2.erode(thresh, kernel, iterations = 1)
# result = cv2.bitwise_or(img, erode)

kernel = np.ones((2,2),np.uint8)
se1 = cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4))
se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
se3 = cv2.getStructuringElement(cv2.MORPH_CROSS,(12,12))

dilation = cv2.dilate(img, se1, iterations = 1)
erosion = cv2.erode(dilation, se1, iterations = 1)

dilation2 = cv2.dilate(erosion, se2, iterations = 1)
final = cv2.erode(dilation2, se2, iterations = 1)

# perform skeletonization
skeleton = np.array(skeletonize(final)).astype(np.uint8)*255


cv2.imwrite(image_name.split(".")[0] + "_eroded.png", erosion)
cv2.imwrite(image_name.split(".")[0] + "_dilated.png", dilation)
cv2.imwrite(image_name.split(".")[0] + "_dilated2.png", dilation2)
cv2.imwrite(image_name.split(".")[0] + "_processed.png", skeleton)


# img_final = Image.fromarray(result, "1")
# img_final.save(image_name.split(".")[0] + "_processed.png") # save image

# plt.imshow(img_final)
# plt.show()