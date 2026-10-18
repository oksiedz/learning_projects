from game_data import data
from random import choice
from art import logo, vs


def start_new_game():
    """Function asks if player want to finish and close game or to start the new game"""
    answer = ""
    while answer not in ("yes", "no"):
        answer = input("Do you want to play new game? yes/no ").lower()
    if answer == "yes":
        higher_lower_game()
    else:
        return


def choice_string(provided_choice):
    """returns a string of choice"""
    return f"{provided_choice['name']}, a {provided_choice['description']}, from {provided_choice['country']}"


def correct_guess(answer, follower_1, follower_2):
    """Function compares the answer with the correct results.
    Return True or False"""
    if follower_1 > follower_2:
        return answer == "a"
    elif follower_2 > follower_1:
        return answer == 'b'
    else:
        False


def higher_lower_game():
    score = 0
    the_end = 0
    first_choice = {}
    second_choice = {}

    while the_end == 0:
        if score == 0:
            first_choice = choice(data)
        else:
            first_choice = second_choice
        second_choice = choice(data)
        while first_choice == second_choice:
            second_choice = choice(data)

        print(logo)
        if score != 0:
            print(f"You are right! Current score: {score}")
        print(f"Compare A: {choice_string(first_choice)}")
        print(vs)
        print(f"Against B: {choice_string(second_choice)}")
        answer = ""
        while answer not in ("a", "b"):
            answer = input("Who has more followers? A or B: ").lower()

        if correct_guess(answer=answer, follower_1=first_choice['follower_count'],
                         follower_2=second_choice['follower_count']):
            score += 1
        else:
            the_end = 1

        if the_end == 1:
            print(f"Sorry that's wrong. Final score {score}")
            start_new_game()


higher_lower_game()
