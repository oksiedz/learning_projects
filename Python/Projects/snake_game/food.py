from turtle import Turtle
import random

WIDTH = 0.5
LENGTH = 0.5
LOW_X = -280  # not edge value
HIGH_X = 280
LOW_Y = -280
HIGH_Y = 280


# Food is inheriting from Turtle class
class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=WIDTH, stretch_len=LENGTH)  # it's 50% of initial size 20
        self.color("yellow")
        self.speed("fastest")
        self.new_food_location()

    def new_food_location(self):
        """Method setting random location of snake food"""
        # setting random location
        random_x = random.randint(LOW_X, HIGH_X)
        random_y = random.randint(LOW_Y, HIGH_Y)
        self.goto(random_x, random_y)
