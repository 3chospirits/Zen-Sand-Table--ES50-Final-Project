input = input("gcode file: ")

SCALE = 2000

new_f = open(input + "_modified", "w")
with open(input) as f:
    for i, line in enumerate(f):
        lst = line.split(' ')
        if len(lst) > 1:
            x, y = lst[1].strip("X"), lst[2].strip("Y\n")
            # x, y = str(int(x) / SCALE), str(int(y) / SCALE)
        new_f.write("G1 X" + x + ".0 Y" + y + ".0\n")

new_f.close()