from turtle import Turtle

# constant
SHAPE = "square"
COLOUR = "white"
WIDTH_STRETCH = 5
LENGTH_STRETCH = 1
STARTING_X = 350
STARTING_Y = 0
HEADING = 90
STEP = 20
UP_DOWN_BOUNDARY = 255


class Paddle(Turtle):
    def __init__(self, paddle_number):
        super().__init__()
        self.shape(SHAPE)
        self.color(COLOUR)
        self.shapesize(stretch_wid=WIDTH_STRETCH, stretch_len=LENGTH_STRETCH)
        self.penup()
        self.position(paddle_number=paddle_number)

    def position(self, paddle_number):
        if paddle_number == 1:
            self.goto(x=STARTING_X, y=STARTING_Y)
        if paddle_number == 2:
            self.goto(x=-STARTING_X, y=STARTING_Y)

    def up(self):
        new_y = self.ycor() + STEP
        if new_y > UP_DOWN_BOUNDARY:
            pass
        else:
            self.goto(self.xcor(), new_y)

    def down(self):
        new_y = self.ycor() - STEP
        if new_y < -UP_DOWN_BOUNDARY:
            pass
        else:
            self.goto(self.xcor(), new_y)
