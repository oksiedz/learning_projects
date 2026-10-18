import turtle as t
tim = t.Turtle()


def move_forwards():
    """turtle is moving 10 steps forward"""
    tim.forward(10)


def move_backwards():
    """turtle is moving 10 steps back"""
    tim.backward(10)


def turn_cclockwise():
    """turtle is turning counterclockwise (left) by 5 degrees"""
    tim.left(5)


def turn_clockwise():
    """trutle is turning clockwise (right) by 5 degrees"""
    tim.right(5)


def clear_screen():
    """function clearning drawings done by the turtle and returning it to state 0,0"""
    tim.clearstamps()
    tim.clear()
    tim.setx(0)
    tim.sety(0)
    tim.clear()


def ech_a_scetch(screen):
    """function responsible for Ech a sketch game
    (requires providing screen)
    w - moves forward
    s - moves backwards
    a - turns left
    d - turns right
    c - clears the screen"""
    screen.onkey(key="w", fun=move_forwards)
    screen.onkey(key="s", fun=move_backwards)
    screen.onkey(key="a", fun=turn_cclockwise)
    screen.onkey(key="d", fun=turn_clockwise)
    screen.onkey(key='c', fun=clear_screen)