import math
import serial
import time

STEPSIZE = 0.1 # mm/step
MAX_RPM = 500 # max motor speed
TRAVEL_SPEED = 40 # mm/sec
STEPS_PER_REV = 200 # number of steps per full revolution of the motor
ARDUINO_BUFSIZE = 8 # number of (x_steps, y_steps, x_rpm, y_rpm) tuples arduino can hold in buffer

x, y = map(int, input("Current X, Y coordinates: ").split(",")) # get current position

arduino = serial.Serial(port='/dev/cu.usbmodem142401', 
                        baudrate=9600, 
                        timeout=1) # open serial connection
while(arduino.read(1) != b''): # ignore bytes sent on startup 
    pass

def arduino_write(zipped_output):
    """Sends calculated distances and speeds to arduino to control motors"""
    if len(zipped_output) % ARDUINO_BUFSIZE != 0: # ensure output is multiple of ARDUINO_BUFSIZE
        for i in range(ARDUINO_BUFSIZE - (len(zipped_output) % ARDUINO_BUFSIZE)):
            zipped_output.append(((0, 0), (0, 0))) # add dummy values to fill buffer
    
    progress = 0
    while (len(zipped_output) > 0): # while there are still coordinates to send
        bytes_list = []
        # get values to fill buffer with
        for i in range(ARDUINO_BUFSIZE):
            steps, rpm = zipped_output.pop(0) # get next coordinate
            x_steps, y_steps = int(steps[0]), int(steps[1]) # unpack steps
            x_rpm, y_rpm = int(rpm[0]), int(rpm[1]) # unpack rpms
            
            # convert all values to bytes to send over serial communication
            x_steps_bytes = x_steps.to_bytes(2, byteorder='little', signed=True)
            y_steps_bytes = y_steps.to_bytes(2, byteorder='little', signed=True)
            x_rpm_bytes = x_rpm.to_bytes(2, byteorder='little', signed=True)
            y_rpm_bytes = y_rpm.to_bytes(2, byteorder='little', signed=True)

            # add bytes to list to send
            bytes_list.append(x_steps_bytes)
            bytes_list.append(y_steps_bytes)
            bytes_list.append(x_rpm_bytes)
            bytes_list.append(y_rpm_bytes)
            
        arduino.write("<".encode("utf-8")) # send start of transmission character
        for i in range(len(bytes_list)):
            arduino.write(bytes_list[i]) # send data
        arduino.write(">".encode("utf-8")) # send end of transmission character
        
        progress += len(bytes_list) # update number of bytes sent
        print("Number of bytes sent: ", progress)
        res = "" 
        while (res != "ready"):
            res = arduino.read_until(b'\n').decode().strip()
            if res: 
                print(res)


def get_steps(dist):
    """Returns number of motor steps needed to go `dist` mm"""
    return math.floor(dist / STEPSIZE)

def get_rpm(steps, travel_time):
    """Returns rpm needed to travel `steps` steps in `travel_time` seconds"""
    if (steps == 0 or travel_time == 0):
        return 0
    return (steps / STEPS_PER_REV) / (travel_time / 60)

while True: # run loop continuously 
    inp = input("Enter a file name: ")
    f = open(inp) 
    steps = [] # array of steps numbers for motor
    rpms = [] # array of rpms for motor
    for i, next_coord in enumerate(f): # read in next coordinate
        next_x, next_y = tuple([int(val.strip()) for val in next_coord.split(",")])
        x_dist, y_dist = next_x - x, next_y - y # distance to travel in each direction
        total_dist = math.sqrt((next_x - x)**2 + (next_y - y)**2) # straight line distance
        travel_time = total_dist / TRAVEL_SPEED # time to travel total distance

        # add each coordinate's steps and rpms the output lists
        x_steps, y_steps = get_steps(x_dist), get_steps(y_dist) 
        steps.append((x_steps, y_steps))
        rpms.append((get_rpm(x_steps, travel_time), get_rpm(y_steps, travel_time)))
        x, y = next_x, next_y # update current position
    f.close()

    # format output for writing to arduino
    zipped_output = list(zip(steps, rpms))
    arduino_write(zipped_output)




