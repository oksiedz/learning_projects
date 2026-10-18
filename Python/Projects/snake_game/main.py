from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

# constants
WALL_UP = 280
WALL_DOWN = -280
FOOD_EATING_DISTANCE = 15
TAIL_DISTANCE = 10

# screen configuration
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake game")
screen.tracer(0)  # parameter responsible for screen not updating automatically

snake = Snake()
food = Food()
score = Scoreboard()
# enabling listening of the keyboard
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)  # one second daly after each snake's segment moves
    snake.move()
    # detection of collision of snake and food (used by distance)
    if snake.snake_head.distance(food) < FOOD_EATING_DISTANCE:
        # 15 since size of food is 10x10 circle
        # food should go to random location
        food.new_food_location()
        score.increase_score()
        snake.extend()

    # detect collision with wall
    if snake.snake_head.xcor() > WALL_UP or snake.snake_head.xcor() < WALL_DOWN or snake.snake_head.ycor() > WALL_UP or snake.snake_head.ycor() < WALL_DOWN:
        # game_is_on = False
        # score.game_over()
        score.reset_scoreboard()
        snake.reset_snake()

    # detect collision with tail
    # head collide with any segment in tail
    for snake_piece in snake.snakes[1:]:
        if snake.snake_head.distance(snake_piece) < TAIL_DISTANCE:
            # game_is_on = False
            # score.game_over()
            score.reset_scoreboard()
            snake.reset_snake()

screen.exitonclick()
