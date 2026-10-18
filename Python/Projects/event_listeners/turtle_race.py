import turtle as t

def turtle_race(screen):

    # definition of the width and height of the screen
    screen.setup(width=500, height=400)

    # popup to bet which turtle will win
    user_bet = (screen.textinput(title="Make your bet", prompt="Which turtle will win the race (green, yellow, red, "
                                                               "purple, blue):")).lower()
