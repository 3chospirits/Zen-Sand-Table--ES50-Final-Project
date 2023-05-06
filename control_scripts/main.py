# main.py
# Accepts input for gcode file and sends instructions to arduino to control motors 
# using serial communication.

import math
import serial

STEPSIZE = 0.1          # mm/step
TRAVEL_SPEED = 80       # mm/sec
STEPS_PER_REV = 200     # number of steps per full revolution of the motor
ARDUINO_BUFSIZE = 8     # number of (x_steps, y_steps, x_rpm, y_rpm) tuples arduino can hold in buffer

x, y = map(int, input("Current X, Y coordinates: ").split(","))  # get current position of motors

arduino = serial.Serial(
    port="/dev/cu.usbmodem14301", baudrate=9600, timeout=1
)  # open serial connection

while arduino.read(1) != b"":  # ignore bytes sent on startup
    pass


def arduino_write(zipped_output):
    """Sends calculated distances and speeds to arduino to control motors"""
    # ensure output is multiple of ARDUINO_BUFSIZE
    if len(zipped_output) % ARDUINO_BUFSIZE != 0:  
        for i in range(ARDUINO_BUFSIZE - (len(zipped_output) % ARDUINO_BUFSIZE)):
            # add dummy values to fill buffer (ensure buffer size is constant)
            zipped_output.append(((0, 0), (0, 0)))  

    progress = 0
    while len(zipped_output) > 0:  # while there are still coordinates to send
        print("Instructions sending...")
        bytes_list = []
        # get values to fill buffer with
        for i in range(ARDUINO_BUFSIZE):
            steps, rpm = zipped_output.pop(0)  # get next coordinate
            x_steps, y_steps = int(steps[0]), int(steps[1])  # unpack steps
            x_rpm, y_rpm = int(rpm[0]), int(rpm[1])  # unpack rpms

            # convert all values to bytes to send over serial communication
            x_steps_bytes = x_steps.to_bytes(2, byteorder="little", signed=True)
            y_steps_bytes = y_steps.to_bytes(2, byteorder="little", signed=True)
            x_rpm_bytes = x_rpm.to_bytes(2, byteorder="little", signed=True)
            y_rpm_bytes = y_rpm.to_bytes(2, byteorder="little", signed=True)

            # add bytes to list to send
            bytes_list.append(x_steps_bytes)
            bytes_list.append(y_steps_bytes)
            bytes_list.append(x_rpm_bytes)
            bytes_list.append(y_rpm_bytes)
            print(x_steps, y_steps, x_rpm, y_rpm)

        arduino.write("<".encode("utf-8"))  # send start of transmission character
        for i in range(len(bytes_list)):
            arduino.write(bytes_list[i])  # send data

        progress += len(bytes_list)  # update number of bytes sent
        print("Number of bytes sent: ", progress)
        res = ""
        while res != "ready":
            res = arduino.read_until(b"\n").decode().strip()
            if res:
                print(res)


def get_steps(dist):
    """Returns number of motor steps needed to go `dist` mm"""
    return math.floor(dist / STEPSIZE)


def get_rpm(steps, travel_time):
    """Returns rpm needed to travel `steps` steps in `travel_time` seconds"""
    if steps == 0 or travel_time == 0:
        return 0
    return (steps / STEPS_PER_REV) / (travel_time / 60)


def get_scale(filename):
    """Scale coordinates from coordinates file to fit/fill the board"""
    max_val = 0
    min_val = 0
    scale = 1

    f = open(filename)
    for line in f:
        vals = [int(val.strip()) for val in line.split(",")]
        biggest_val = max(vals)
        smalles_val = min(vals)
        max_val = biggest_val if biggest_val > max_val else max_val
        min_val = smalles_val if smalles_val < min_val else min_val
    scale = 1850 / (max_val - min_val)
    f.close()

    return scale


while True:  # main loop
    # ask for coordinates file
    inp = input("Enter a file name: ")
    scale = get_scale(inp)

    f = open(inp)
    steps = []  # step counts for motor
    rpms = []  # rpms for motor
    for i, next_coord in enumerate(f):  # read in next coordinate
        next_x, next_y = tuple([int(val.strip()) for val in next_coord.split(",")])
        next_x, next_y = int(scale * next_x), int(scale * next_y)  # scale coordinates
        print(next_x, next_y)
        
        # distance to travel in each direction
        x_dist, y_dist = next_x - x, next_y - y  

        # add each coordinate's steps and rpms the output lists
        x_steps, y_steps = get_steps(x_dist), get_steps(y_dist)
        steps.append((x_steps, y_steps))

        # calculate rpms for each motor to enusre they arrive at destination simultaneously
        total_dist = math.sqrt((next_x - x) ** 2 + (next_y - y) ** 2)  
        travel_time = total_dist / TRAVEL_SPEED
        rpms.append((get_rpm(x_steps, travel_time), get_rpm(y_steps, travel_time)))
        x, y = next_x, next_y  # update current positino to position after instruction execution
    f.close()

    # format output for writing to arduino
    zipped_output = list(zip(steps, rpms))
    arduino_write(zipped_output)
