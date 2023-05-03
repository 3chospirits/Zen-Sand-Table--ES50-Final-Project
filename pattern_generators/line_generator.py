LINES = 40
WIDTH = 19000
HEIGHT = 19000

coords = []

for i in range(LINES):
    if i % 2 == 0:
        coords.append(WIDTH / LINES * i)
        coords.append(0)
        coords.append(WIDTH / LINES * i)
        coords.append(HEIGHT)
    else:
        coords.append(WIDTH / LINES * i)
        coords.append(HEIGHT)
        coords.append(WIDTH / LINES * i)
        coords.append(0)


f = open("../gcode/lines.gcode", "w")
for i, coord in enumerate(coords):
    f.write(str(coord))
    if i % 2 == 0:
        f.write(", ")
    else:
        f.write("\n")
