from turtle import *
from math import *

RANGE = 600
SPACING = 10
OFFSET = SPACING * RANGE / 20 * pi
print(OFFSET)

coords = []

# color("blue")
# down()
for i in range(RANGE):
    t = i / 20 * pi
    x = (1 * SPACING * t) * cos(t) + OFFSET
    y = (1 * SPACING * t) * sin(t) + OFFSET
    coords.append((int(x), int(y)))

    # goto(x, y)
# up()
# done()

f = open("gcode/spiral.gcode", "w")
for coord in coords:
    f.write(str(coord))
    f.write("\n")
