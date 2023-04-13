import cv2
import numpy as np

# Load the image and convert it to grayscale
# img = cv2.imread('drawing.jpeg')
img = cv2.imread('draw1.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a threshold to convert it to a binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imwrite('thresh.png', thresh)

# contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# # Simplify the contours to a single pixel width
# tolerance = 1
# simplified_contours = []
# for contour in contours:
#     simplified_contour = cv2.approxPolyDP(contour, tolerance, closed=True)
#     simplified_contours.append(simplified_contour)
# countors = simplified_contours

# complex
# Find the contours of the drawing
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Create an empty image to draw the contours on
# contour_img = np.zeros_like(gray)

# # Draw the contours with the thickness of the lines
# cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 10)

# # Find the contours of the drawing on the contour image
# contours, _ = cv2.findContours(contour_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

drawing = np.zeros_like(img)
cv2.drawContours(drawing, contours, -1, (0, 255, 0), 2)

# Display the drawing
cv2.imshow('Drawing', drawing)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Generate G-code commands for each contour
gcode = []
for contour in contours:
    gcode.append('{}, {}'.format(contour[0][0][0], contour[0][0][1]))
    # gcode.append('G0 X{} Y{}'.format(contour[0][0][0], contour[0][0][1]))
    for point in contour[1:]:
        gcode.append('{}, {}'.format(point[0][0], point[0][1]))

# Write the G-code commands to a file
with open('coords.gcode', 'w') as f:
    f.write('\n'.join(gcode))
