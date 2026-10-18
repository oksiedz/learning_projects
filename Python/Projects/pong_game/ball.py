from turtle import Turtle

# constants
COLOUR = "white"
SHAPE = "circle"
X_DEFAULT_STEP = 10
Y_DEFAULT_STEP = 10
STARTING_X = 0
STARTING_Y = 0
STARTING_MOVE_SPEED = 0.1


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR)
        self.shape(SHAPE)
        self.penup()
        self.x_step = X_DEFAULT_STEP
        self.y_step = Y_DEFAULT_STEP
        self.moves_speed = STARTING_MOVE_SPEED

    # vertical = 1 if up -1 if down, horizontal 1 if right, -1 if left
    def move(self):
        new_x = self.xcor() + self.x_step
        new_y = self.ycor() + self.y_step
        self.goto(new_x, new_y)

    def wall_bounce(self):
        self.y_step *= -1

    def paddle_bounce(self):
        self.x_step *= -1
        self.moves_speed *= 0.9

    def starting_position(self):
        # balls returns to the beginning
        self.goto(STARTING_X, STARTING_Y)
        # the ball will start into the opposite direction
        self.x_step *= -1
        self.moves_speed = STARTING_MOVE_SPEED
