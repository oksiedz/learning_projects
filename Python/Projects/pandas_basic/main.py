import turtle
import pandas

IMAGE = "US_game/blank_states_img.gif"
STATE_DATA = "US_game/50_states.csv"
EXIT_STRING = "exit"
OUTPUT_DATA = "US_game/states_to_learn.csv"

screen = turtle.Screen()
screen.title("U.S.A. States guessing game")
screen.addshape(IMAGE)

turtle.shape(IMAGE)

# method reading the coordinates from the click on map
# def get_mouse_click_coor(x, y):
#     print(x, y)
#
# turtle.onscreenclick(get_mouse_click_coor)
# empty list with correct answers
guessed_states = []

while len(guessed_states) < 50:
    answered_state = screen.textinput(title=f"{len(guessed_states)}/50 States correct",
                                      prompt="What's another state's name?").lower()
    data = pandas.read_csv(filepath_or_buffer=STATE_DATA)
    list_of_states = data.state.to_list()
    # conversion to lowercase
    list_of_states_lower = []
    for state in list_of_states:
        list_of_states_lower.append(state.lower())
    # print(list_of_states_lower)

    if answered_state in list_of_states_lower:
        row_with_answer = data[data.state.str.lower() == answered_state]
        # new turtle which will be writing answers
        writer_turtle = turtle.Turtle()
        writer_turtle.penup()
        writer_turtle.hideturtle()
        writer_turtle.goto(int(row_with_answer.x.iloc[0]), int(row_with_answer.y.iloc[0]))
        writer_turtle.write(row_with_answer.state.item())
        if answered_state not in guessed_states:
            guessed_states.append(answered_state)

        print(row_with_answer)
        print(answered_state)

    # exit the game
    if answered_state == EXIT_STRING.lower():
        missing_states = [state for state in list_of_states_lower if state not in guessed_states]
        # missing_states = []
        # for state in list_of_states_lower:
        #     if state not in guessed_states:
        #         missing_states.append(state.title())

        # save the file with not guessed states to CSV
        output_data = pandas.DataFrame(missing_states)
        output_data.to_csv(OUTPUT_DATA)

        break

turtle.mainloop()
# screen.exitonclick()
