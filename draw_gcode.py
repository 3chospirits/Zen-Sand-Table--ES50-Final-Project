import turtle

# Set up screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

num = 4

file = f"swirls/flower_spiral_{num}.gcode"

# Find max values
max_x = max_y = 0
with open(file) as f:
    for line in f:
        x, y = map(int, line.strip().split(','))
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

# Scale values to fit screen
scale_factor = min(SCREEN_WIDTH / max_x, SCREEN_HEIGHT / max_y)
max_x *= scale_factor
max_y *= scale_factor

# Initialize turtle
turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
turtle.speed('fastest')
turtle.penup()

# Follow points and draw
with open(file) as f:
    for line in f:
        x, y = map(int, line.strip().split(','))
        turtle.goto(x * scale_factor - max_x / 2, y * scale_factor - max_y / 2)
        turtle.pendown()

turtle.done()