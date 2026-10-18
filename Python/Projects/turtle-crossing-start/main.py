import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.listen()
player = Player()
scoreboard = Scoreboard()
car_manager = CarManager()

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.add_car()
    car_manager.move_cars()

    screen.onkey(player.move_forward, "Up")

    # instruction checking if turtle crossed the finish line and then performing action
    if player.if_finish_line_crossed():
        player.cross_finish_line()
        scoreboard.print_value(player.game_level)
        car_manager.set_movement_speed()

    else:
        pass

    for car in car_manager.list_of_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

screen.exitonclick()
