from turtle import Turtle, Screen
import random


# function for turtle creation
def create_turtle(scr, list_of_turtles):
    for x in range(0, 6):
        new_turtle = Turtle(shape="turtle")
        new_turtle.penup()
        new_turtle.color(colors[x])
        new_turtle.goto((scr.window_width() / 2 - 20) * - 1, 75 - x * 30)
        list_of_turtles.append(new_turtle)


screen = Screen()

# variable saying if the race started
race_started = False

# sizing of the screen
screen.setup(width=500, height=400)

# pop up for betting which turtle will win
user_bet = screen.textinput(title="Make your bet", prompt = "Which turtle will win the race? Enter a color (red, "
                                                            "orange, yellow, green, blue, purple): ").lower()
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
all_turtles = []

# creation of turtles
create_turtle(screen, all_turtles)

# if user gave the bet then the race started
if user_bet:
    race_started = True

# turtle moves till they will reach finish line
while race_started:
    for turtle in all_turtles:
        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)
        # turtle size is 40x40 - condition to close the game
        if turtle.xcor() > 230:
            race_started = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You have won! The {winning_color} turtle is the winner! Congratulations!")
            else:
                print(f"You have lost! The {winning_color} turtle is the winner, while you bet on {user_bet}!")

screen.exitonclick()
