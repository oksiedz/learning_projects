import turtle as t

import ech_a_sketch as eas
import turtle_race as tr
screen = t.Screen()

# below screen needs to start listening to events
screen.listen()

tr.turtle_race(screen=screen)

# eas.ech_a_scetch(screen=screen)

screen.exitonclick()
