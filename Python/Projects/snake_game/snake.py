from turtle import Turtle

MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
STARTING_POSITIONS = ((0, 0), (-20, 0), (-40, 0))


class Snake:

    def __init__(self):
        self.snakes = []
        self.create_snake()
        self.snake_head = self.snakes[0]

    def create_snake(self):
        """Method creating snake at the beginning of the game"""
        # creation of first snake created from 3 squares
        for x in STARTING_POSITIONS:
            self.add_segments(x)

    # snake movement, changing coordination from the last segment to the new previous one
    def move(self):
        """Method responsible for moving the snake"""
        for snake_piece in range(len(self.snakes) - 1, 0, -1):
            new_x = self.snakes[snake_piece - 1].xcor()
            new_y = self.snakes[snake_piece - 1].ycor()
            self.snakes[snake_piece].goto(new_x, new_y)
        self.snake_head.forward(MOVE_DISTANCE)

    # going up
    def up(self):
        """Method responsible to move the head of a snake up"""
        if self.snake_head.heading() in (UP, DOWN):
            pass
        else:
            self.snake_head.setheading(UP)

    # going down
    def down(self):
        """Method responsible to move the head of a snake down"""
        if self.snake_head.heading() in (UP, DOWN):
            pass
        else:
            self.snake_head.setheading(DOWN)

    # going left
    def left(self):
        """Method responsible to move the head of a snake left"""
        if self.snake_head.heading() in (LEFT, RIGHT):
            pass
        else:
            self.snake_head.setheading(LEFT)

    # going right
    def right(self):
        """Method responsible to move the head of a snake right"""
        if self.snake_head.heading() in (LEFT, RIGHT):
            pass
        else:
            self.snake_head.setheading(RIGHT)

    # adding segment to the snake
    def add_segments(self, position):
        """Method responsible for adding new segment to the snake when it eats food"""
        new_turtle = Turtle(shape="square")
        new_turtle.penup()
        new_turtle.color("white")
        # starting positions of the snake are set here
        new_turtle.goto(position)
        self.snakes.append(new_turtle)

    # extending snake by new segment at the end of the tale
    def extend(self):
        """Method calling add_segments method"""
        self.add_segments(self.snakes[-1].position())

    def reset_snake(self):
        """Method to reset the snake to the beginning of the game"""
        for segment in self.snakes:
            segment.goto(1000, 1000)
        self.snakes.clear()
        self.create_snake()
        self.snake_head = self.snakes[0]