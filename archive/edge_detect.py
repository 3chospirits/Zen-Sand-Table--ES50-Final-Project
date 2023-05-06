# file = "spoon.png"
file = "fox.png"
import cv2

# Load the image in grayscale
img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to reduce noise
img_blur = cv2.GaussianBlur(img, (9,9), 0)

# Detect edges using the Canny edge detection algorithm
# edges = cv2.Canny(img_blur, threshold1=30, threshold2=100)
edges = cv2.Canny(img_blur, threshold1=10, threshold2=90)

img_blur2 = cv2.GaussianBlur(edges, (9,9), 0)

edges2 = cv2.Canny(img_blur2, threshold1=80, threshold2=90)

# Display the original image and the edges detected
cv2.imshow('Original Image', img)
cv2.imshow('Edges', edges2)
cv2.waitKey(0)
cv2.destroyAllWindows()

