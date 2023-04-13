import cv2
import numpy as np

# Load the image and convert it to grayscale
# img = cv2.imread('drawing.jpeg')
img = cv2.imread('swirl3.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a threshold to convert it to a binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imwrite('thresh.png', thresh)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


drawing = np.zeros_like(img)
cv2.drawContours(drawing, contours, -1, (0, 255, 0), cv2.FILLED, 1)

# Display the drawing
cv2.imshow('Drawing', drawing)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Generate G-code commands for each contour

gcode = []
for contour in cv2.findContours(drawing[:,:,0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
    gcode.append('{}, {}'.format(contour[0][0][0], contour[0][0][1]))
    # gcode.append('G0 X{} Y{}'.format(contour[0][0][0], contour[0][0][1]))
    for point in contour[1:]:
        gcode.append('{}, {}'.format(point[0][0], point[0][1]))

# Write the G-code commands to a file
with open('coords.gcode', 'w') as f:
    f.write('\n'.join(gcode))
