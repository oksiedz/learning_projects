import colorgram as c
import turtle as t
import random as r

AMOUNT_OF_COLOURS = 30
IMAGE_NAME = 'image.jpg'
# extract colours from picture
colors = c.extract(IMAGE_NAME, AMOUNT_OF_COLOURS)

list_of_colors_tuples = []

# loop populating list with most common colours from photo
for i in range(0, AMOUNT_OF_COLOURS):
    # assignment of color object into variable
    first_color = colors[i]
    # extract rgb
    rgb = first_color.rgb
    # assignment rbg into separate variables
    red = rgb.r
    green = rgb.g
    blue = rgb.b
    # creation of tuple
    color_tuple = (red, green, blue)
    # appending the list of tuples
    list_of_colors_tuples.append(color_tuple)

print(colors)
print(list_of_colors_tuples)


def print_row(my_turtle, my_list_of_colors):
    """function printing row of colorful dots, with centers in distance of 70,
    Parameters:
        my_turtle - turtle object
        my_list_of_colors - list of rgb color tuple"""
    for iterator in (range(10)):
        # my_turtle.pendown()
        my_turtle.pencolor(r.choice(my_list_of_colors))
        my_turtle.dot(20)
        # my_turtle.penup()
        if iterator != 9:
            my_turtle.forward(70)


def move_row_up(my_turtle, iteration):
    """function moving the position of turtle
    Parameters:
        my_turtle - turtle object
        iteration - number of iterations"""
    tim.penup()
    my_turtle.setx(-330)
    new_y = -330 + 70 * iteration
    my_turtle.sety(new_y)


tim = t.Turtle()
t.colormode(255)

# full length is 10 * 20 + 50 * 10 = 200 + 500 = 700

for i in range(10):
    move_row_up(tim, i)
    print_row(tim, list_of_colors_tuples)

tim.hideturtle()

t.Screen().exitonclick()
