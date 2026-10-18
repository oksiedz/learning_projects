from turtle import Turtle

INITIAL_VALUE = 0
INITIAL_X = 0
INITIAL_Y = 260
ALIGNMENT = "center"
FONT_STYLE = ("Arial", 15, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.value = INITIAL_VALUE
        self.high_score = INITIAL_VALUE
        self.penup()
        self.hideturtle()
        self.color("white")
        self.goto(INITIAL_X, INITIAL_Y)
        self.print_score()

    def increase_score(self):
        """Method increasing score with increment value 1"""
        self.value = self.value + 1
        self.print_score()

    def print_score(self):
        """Method printing the current score"""
        self.clear()
        self.write(f'Score: {self.value} High Score: {self.high_score}', align=ALIGNMENT, font=FONT_STYLE)

    def reset_scoreboard(self):
        """Method resetting the scoreboard in case of the snake hitting the wall or eating itself"""
        if self.value > self.high_score:
            self.high_score = self.value
        self.value = INITIAL_VALUE
        self.print_score()

    def game_over(self):
        """Method printing the Gave Over and the final result"""
        self.clear()
        self.write("Game Over Your Score: " + str(self.value), align=ALIGNMENT, font=FONT_STYLE)
