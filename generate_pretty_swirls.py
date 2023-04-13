import turtle
import os
import math

def draw_flower_spirals():
    os.makedirs("swirls", exist_ok=True)
    
    for i in range(1, 6):
        t = turtle.Turtle()
        t.speed(0)
        t.penup()
        t.goto(500, 500)
        t.pendown()
        
        # Set up the parameters for the flower/spiral
        angle = 137.5 * i
        scale = 1 + (3 * i)

        with open(f"swirls/flower_spiral_{i}.gcode", "w") as f:
            for n in range(1, 200):
                t.circle(scale * math.sqrt(n), angle)
                t.pendown()
                x, y = t.position()
                
                if 0 <= x <= 1000 and 0 <= y <= 1000:
                    f.write(f"{int(x)}, {int(y)}\n")
                else:
                    break
                    
        t.showturtle()

    turtle.done()

if __name__ == "__main__":
    draw_flower_spirals()