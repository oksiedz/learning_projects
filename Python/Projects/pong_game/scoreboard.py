from turtle import Turtle

COLOUR = "white"
ALIGNMENT = "center"
FONT_STYLE = ("Courier", 80, "normal")
FONT_GAME_OVER = ("Courier", 10, "normal")
SCORE_X_COR = 100
SCORE_Y_COR = 200


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR)
        self.penup()
        # I do not want to see the turtle just writing
        self.hideturtle()
        self.paddle_1_score = 0
        self.paddle_2_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-SCORE_X_COR, SCORE_Y_COR)
        self.write(self.paddle_2_score, align=ALIGNMENT, font= FONT_STYLE)
        self.goto(SCORE_X_COR, SCORE_Y_COR)
        self.write(self.paddle_1_score, align=ALIGNMENT, font= FONT_STYLE)

    def paddle_1_point(self):
        self.paddle_1_score += 1
        self.update_scoreboard()

    def paddle_2_point(self):
        self.paddle_2_score += 1
        self.update_scoreboard()

    def game_over(self):
        self.clear()
        self.goto(0, SCORE_Y_COR)
        self.write(f"Game Over: Left Player scored {self.paddle_2_score} and Right Player scored {self.paddle_1_score}", align=ALIGNMENT, font=FONT_GAME_OVER)
