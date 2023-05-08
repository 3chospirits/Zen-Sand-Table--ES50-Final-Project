import cv2
import numpy as np

# Define the file to be processed
file = "fox.png"

# Load the image in grayscale
img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to reduce noise
img_blur = cv2.GaussianBlur(img, (9,9), 0)

# Define a range of threshold values to try
thresholds1 = np.arange(5, 200, 10)
thresholds = np.arange(5, 200, 10)

# Initialize variables to store the minimum number of edges found and the corresponding threshold value
min_edges = float('inf')
best_threshold = 0

# Loop over the threshold values and compute the number of edges for each
for t1 in thresholds1:
    for threshold in thresholds:
        if t1 == threshold:
            continue 
        edges = cv2.Canny(img_blur, threshold1=t1, threshold2=threshold)
        img_blur2 = cv2.GaussianBlur(edges, (9,9), 0)
        edges2 = cv2.Canny(img_blur2, threshold1=t1, threshold2=threshold)
        num_edges = np.sum(edges2 > 0)
        if num_edges < min_edges:
            min_edges = num_edges
            best_threshold = threshold
        cv2.imwrite(f'output_imgs/edge_{t1}_{threshold}.jpg', edges2)

# Apply the edge detection algorithm with the best threshold found
edges = cv2.Canny(img_blur, threshold1=best_threshold*0.4, threshold2=best_threshold)
img_blur2 = cv2.GaussianBlur(edges, (9,9), 0)
edges2 = cv2.Canny(img_blur2, threshold1=best_threshold*0.8, threshold2=best_threshold)

# Display the original image and the edges detected
cv2.imshow('Original Image', img)
cv2.imshow('Edges', edges2)
cv2.waitKey(0)
cv2.destroyAllWindows()
