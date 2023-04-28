import math
import serial

STEPSIZE = 0.1 # mm/step
MAX_RPM = 500 # max motor speed
TRAVEL_SPEED = 40 # mm/sec
STEPS_PER_REV = 200 # number of steps per full revolution of the motor
ARDUINO_COORD_BUFSIZE = 50 # number of (x, y) pairs that arduino can hold in buffer

x_steps = [] 
y_steps = []
x_rpms = []
y_rpms = []
x = 0
y = 0

arduino = serial.Serial(port='/dev/cu.usbmodem142401', baudrate=9600, timeout=.1)

def arduino_write():
    while (len(out) > 0):
        for _ in range(min(ARDUINO_COORD_BUFSIZE, len(out))):
            steps, rpm = out.pop(0)
            x_steps, y_steps = int(steps[0]), int(steps[1])
            x_rpm, y_rpm = int(rpm[0]), int(rpm[1])
            x_steps_bytes = x_steps.to_bytes(2, byteorder='little', signed=True)
            y_steps_bytes = y_steps.to_bytes(2, byteorder='little', signed=True)
            x_rpm_bytes = x_rpm.to_bytes(2, byteorder='little', signed=True)
            y_rpm_bytes = y_rpm.to_bytes(2, byteorder='little', signed=True)

            arduino.write(x_steps_bytes)
            arduino.write(y_steps_bytes)
            arduino.write(x_rpm_bytes)
            arduino.write(y_rpm_bytes)
        
        print("Buffer refilled!")
        arduino.read(size=1) # blocks until arduino ready to refill buffer
        print("Buffer empty, refilling...")

def distance_between_coords(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# returns number of motor steps needed to go `dist` mm
def motor_steps_from_distance(dist):
    return math.floor(dist / STEPSIZE)

def calculate_travel_time(dist):
    return dist / TRAVEL_SPEED

def calculate_rpm(steps, travel_time):
    if (steps == 0 or travel_time == 0):
        return 0
    return (steps / STEPS_PER_REV) / (travel_time / 60)

while True:
    inp = input("Enter a file name: ")
    with open(inp) as f:
        for i, next_coord in enumerate(f):
            next_x, next_y = tuple([int(val.strip()) for val in next_coord.split(",")])
            x_dist = next_x - x
            y_dist = next_y - y
            total_distance = distance_between_coords(x, y, next_x, next_y)
            travel_time = calculate_travel_time(total_distance)

            x_steps.append(motor_steps_from_distance(x_dist))
            y_steps.append(motor_steps_from_distance(y_dist))
            x_rpms.append(calculate_rpm(x_steps[i], travel_time))
            y_rpms.append(calculate_rpm(y_steps[i], travel_time))
            x, y = next_x, next_y

    steps = list(zip(x_steps, y_steps))
    rpms = list(zip(x_rpms, y_rpms))
    out = list(zip(steps, rpms))

    arduino_write()



