import math

STEPSIZE = 0.1 # mm/step
MAX_RPM = 500 # max motor speed
TRAVEL_SPEED = 40 # mm/sec
STEPS_PER_REV = 200

x_steps = [] 
y_steps = []
x_rpms = []
y_rpms = []
x = 0
y = 0

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


with open('test.gcode') as f:
	for i, next_coord in enumerate(f):
		next_x, next_y = tuple([int(val.strip()) for val in next_coord.split(",")])
		x_dist = next_x - x
		y_dist = next_y - y
		total_distance = distance_between_coords(x, y, next_x, next_y)
		travel_time = calculate_travel_time(total_distance)

		print(travel_time)
		x_steps.append(motor_steps_from_distance(x_dist))
		y_steps.append(motor_steps_from_distance(y_dist))
		x_rpms.append(calculate_rpm(x_steps[i], travel_time))
		y_rpms.append(calculate_rpm(y_steps[i], travel_time))
		x, y = next_x, next_y

steps = zip(x_steps, y_steps)
rpms = zip(x_rpms, y_rpms)
out = zip(steps, rpms)
for o in out:
	print(o)



