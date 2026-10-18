from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        """Constructor of the player turtle"""
        super().__init__()
        self.set_turtle_parameters()
        self.set_starting_position()
        self.game_level = 1

    def set_turtle_parameters(self):
        """Method setting starting turtle attributes: shape - turtle, raising pen up and set heading to 90 (up of the
        screen)"""
        self.shape("turtle")
        self.penup()
        self.setheading(90)

    def set_starting_position(self):
        """Method setting starting position of the turtle to the one defined in constant STARTING_POSITION"""
        self.setposition(STARTING_POSITION)

    def move_forward(self):
        """Method used to move player turtle"""
        self.forward(MOVE_DISTANCE)

    def add_score(self):
        """Method increasing score of the game"""
        self.game_level += 1

    def cross_finish_line(self):
        """Method describing what actions have to happen when player cross the finish line"""
        self.add_score()
        self.set_starting_position()

    def if_finish_line_crossed(self):
        """Return Method, returning boolean if the player crossed the finish line"""
        if self.ycor() >= FINISH_LINE_Y:
            return True
        else:
            return False
