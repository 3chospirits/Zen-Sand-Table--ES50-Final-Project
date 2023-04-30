import sys
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import numpy as np
import cv2

# Get the filename of the input image from the command line
if len(sys.argv) < 2:
    print("Usage: python single_line_art.py input_image.jpg")
    sys.exit(1)

input_filename = sys.argv[1]

# Load image and convert to grayscale
image = Image.open(input_filename)
image = image.convert('L')

# Apply edge detection filter
image = image.filter(ImageFilter.FIND_EDGES)

# Invert colors
image = ImageOps.invert(image)

# Create a new image to draw on
output_image = Image.new("RGB", image.size, "white")
draw = ImageDraw.Draw(output_image)

# Find contours using the Canny algorithm
contours, hierarchy = cv2.findContours(np.array(image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw a single line that follows the contours
for contour in contours:
    for i in range(len(contour) - 1):
        x1, y1 = contour[i][0]
        x2, y2 = contour[i+1][0]
        draw.line((x1, y1, x2, y2), fill="black", width=1)

# Save the output image
output_filename = input_filename + ".jpg"
output_image.save(output_filename)

print("Output saved as", output_filename)
