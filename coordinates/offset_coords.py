
filename = input("FILENAME: ")
f = open(filename, "r")
f2 = open(filename.split(".")[0] + "_offset.gcode", "w")

min_y_val = 0
min_x_val = 0
for line in f:
    x, y = tuple([int(val.strip()) for val in line.split(",")])
    min_x_val = x if x < min_x_val else min_x_val
    min_y_val = y if y < min_y_val else min_y_val
f.close() 

print(min_x_val, min_y_val)

f = open(filename, "r")
for line in f:
    x, y = tuple([int(val.strip()) for val in line.split(",")])
    print(x + abs(min_x_val), y + abs(min_y_val))
    f2.write("{},{}\n".format(x + abs(min_x_val), y + abs(min_y_val)))

f.close()
f2.close()