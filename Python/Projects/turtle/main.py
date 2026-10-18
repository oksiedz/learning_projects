from turtle import Turtle, Screen
import turtle as t
import random
tim = Turtle()
tim.shape("turtle")
tim.color("green")
t.colormode(255)
# colors = ["aquamarine", "azure4", "black", "blue", "BlueViolet", "brown", "burlywood", "CadetBlue", "cyan", "DarkGrey", "DarkOliveGreen", "DarkRed", "DeepPnk", "LightPink"]
#for i in range(50):
 #   timmy_the_turtle.pendown()
  #  timmy_the_turtle.forward(10)
  #  timmy_the_turtle.penup()
   # timmy_the_turtle.forward(10)

# side_length = 100
# full_circle = 360
# for i in range (3, 11):
#     tim.pencolor(random.choice(colors))
#     for j in range(i):
#         tim.right(full_circle / i)
#         tim.forward(side_length)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# random walk
# tim.width(10)

# for _ in range(10000):
    # tim.pencolor(random.choice(colors))
#     tim.pencolor(random_color())
#     turn = random.choice((1, 2, 3, 4)) * 90
#     tim.right(turn)
#     tim.forward(10)

# printing a spirograph
#tim.speed(0)
#for _ in range(180):
#    tim.circle(100)
#    tim.pencolor(random_color())
#    tim.left(2)



screen = Screen()
screen.exitonclick()