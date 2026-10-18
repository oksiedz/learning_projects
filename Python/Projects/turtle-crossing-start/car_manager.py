import random
from turtle import Turtle

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        """Constructor for the CarManager"""
        self.list_of_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def add_car(self):
        """Method adding cars (Turtle) to car manager list"""
        if random.randint(1, 6) == 1:
            car = Turtle()
            car.penup()
            car.shape("square")
            car.shapesize(stretch_wid=1, stretch_len=2, outline=None)
            car.fillcolor(random.choice(COLORS))
            starting_x_cor = random.randrange(-260, 260)
            car.sety(starting_x_cor)
            car.setx(280)
            car.setheading(180)
            self.list_of_cars.append(car)

    def move_cars(self):
        """Method moving all cars in Car Manager"""
        for car in self.list_of_cars:
            car.forward(self.car_speed)

    def set_movement_speed(self):
        """Method increasing the speed of cars"""
        self.car_speed += MOVE_INCREMENT
