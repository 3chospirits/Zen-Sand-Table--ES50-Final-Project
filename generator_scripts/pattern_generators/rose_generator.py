from turtle import *
from math import *

RANGE = 600
SPACING = 10
OFFSET = SPACING * RANGE / 20 * pi
print(OFFSET)

coords = []
width = height = 18000


# Draws a maurer rose with value n and d it's size about `size`
def drawMaurerRose(n, d, size):
    # color("blue")
    # down()
    for i in range(0, 181):
        # The equation of a maurer rose
        k = i * d
        r = size * sin(radians(n * k))

        # Converting to cartesian co-ordinates
        x = r * cos(radians(k))
        y = r * sin(radians(k))

        coords.append(int(width / 2 + x))
        coords.append(int(height / 2 + y))
        # goto(x, y)
    # up()
    # done()


def drawPattern():
    # Try changing these values to what you want
    drawMaurerRose(7, 17, 9000)


drawPattern()

f = open("../gcode/rose.gcode", "w")
for i, coord in enumerate(coords):
    f.write(str(coord))
    if i % 2 == 0:
        f.write(", ")
    else:
        f.write("\n")
