import turtle

# def move_to_coordinates(coords):
#     # Create a Turtle object
#     t = turtle.Turtle()

#     # Loop through the coordinates and move to each one
#     for coord in coords:
#         x, y = coord
#         t.goto(x, y)

#     # Keep the window open until it is closed
#     turtle.done()


# spiral_coords = [(0, 0), (20, 0), (20, 20), (0, 20), (-20, 20), (-20, 0), (-20, -20), (0, -20), (20, -20), (40, -20), (40, 0), (40, 20), (40, 40), (20, 40), (0, 40), (-20, 40), (-40, 40), (-40, 20), (-40, 0), (-40, -20), (-40, -40), (-20, -40), (0, -40), (20, -40), (40, -40), (60, -40), (60, -20), (60, 0), (60, 20), (60, 40), (60, 60), (40, 60), (20, 60), (0, 60), (-20, 60), (-40, 60), (-60, 60), (-60, 40), (-60, 20), (-60, 0), (-60, -20), (-60, -40), (-60, -60), (-40, -60), (-20, -60), (0, -60), (20, -60), (40, -60), (60, -60)]

# move_to_coordinates(spiral_coords)








# Create a Turtle object
t = turtle.Turtle()

# Set the circle's radius
radius = 100

# Move the pen to the starting point
t.penup()
t.goto(0, -radius)
t.pendown()

# Draw the circle
t.circle(radius)

# Keep the window open until it is closed
turtle.done()


