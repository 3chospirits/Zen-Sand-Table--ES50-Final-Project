import math
import serial

STEPSIZE = 0.1 # mm/step
MAX_RPM = 500 # max motor speed
TRAVEL_SPEED = 40 # mm/sec
STEPS_PER_REV = 200 # number of steps per full revolution of the motor
ARDUINO_COORD_BUFSIZE = 50 # number of (x, y) pairs that arduino can hold in buffer

x_steps = [] # array of step numbers for x motor
y_steps = [] # array of step numbers for y motor
x_rpms = [] # array of rpms for x motor
y_rpms = [] # array of rpms for y motor
x = 0 # current x position
y = 0 # current y position

arduino = serial.Serial(port='/dev/cu.usbmodem142401', baudrate=9600, timeout=.1)

def arduino_write(zipped_output):
    """Sends calculated distances and speeds to arduino to control motors"""
    while (len(zipped_output) > 0): # while there are still coordinates to send
        for _ in range(min(ARDUINO_COORD_BUFSIZE, len(zipped_output))): 
            steps, rpm = zipped_output.pop(0) # get next coordinate
            x_steps, y_steps = int(steps[0]), int(steps[1]) # unpack steps
            x_rpm, y_rpm = int(rpm[0]), int(rpm[1]) # unpack rpms
            
            # convert all values to bytes to send over serial communication
            x_steps_bytes = x_steps.to_bytes(2, byteorder='little', signed=True)
            y_steps_bytes = y_steps.to_bytes(2, byteorder='little', signed=True)
            x_rpm_bytes = x_rpm.to_bytes(2, byteorder='little', signed=True)
            y_rpm_bytes = y_rpm.to_bytes(2, byteorder='little', signed=True)

            # send bytes to arduino
            arduino.write(x_steps_bytes)
            arduino.write(y_steps_bytes)
            arduino.write(x_rpm_bytes)
            arduino.write(y_rpm_bytes)
        
        print("Buffer refilled!")
        arduino.read(size=1) # blocks until arduino ready to refill buffer
        print("Buffer empty, refilling...")

def dist_btwn_coords(x1, y1, x2, y2):
    """Returns distance between two points (x1, y1) and (x2, y2)"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def motor_steps_from_distance(dist):
    """Returns number of motor steps needed to go `dist` mm"""
    return math.floor(dist / STEPSIZE)

def get_travel_time(dist):
    """Returns time in seconds to travel `dist` mm at `TRAVEL_SPEED` mm/sec"""
    return dist / TRAVEL_SPEED

def calculate_rpm(steps, travel_time):
    """Returns rpm needed to travel `steps` steps in `travel_time` seconds"""
    if (steps == 0 or travel_time == 0):
        return 0
    return (steps / STEPS_PER_REV) / (travel_time / 60)

while True: # run until the program is stopped with Ctr + c
    inp = input("Enter a file name: ")
    with open(inp) as f:
        for i, next_coord in enumerate(f): # read in next coordinate
            next_x, next_y = tuple([int(val.strip()) for val in next_coord.split(",")])
            x_dist = next_x - x # distance to travel in x direction
            y_dist = next_y - y # distance to travel in y direction
            total_dist = dist_btwn_coords(x, y, next_x, next_y) # total distance to travel
            travel_time = get_travel_time(total_dist) # time to travel total distance

            # add each coordinate's steps and rpms the output lists
            x_steps.append(motor_steps_from_distance(x_dist))
            y_steps.append(motor_steps_from_distance(y_dist))
            x_rpms.append(calculate_rpm(x_steps[i], travel_time))
            y_rpms.append(calculate_rpm(y_steps[i], travel_time))
            x, y = next_x, next_y # update current position

    # format output for writing to arduino
    steps = list(zip(x_steps, y_steps))
    rpms = list(zip(x_rpms, y_rpms))
    zipped_output = list(zip(steps, rpms))
    arduino_write(zipped_output)



