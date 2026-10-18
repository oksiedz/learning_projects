# ############## Our Blackjack House Rules #####################

# The deck is unlimited in size.
# There are no jokers.
# The Jack/Queen/King all count as 10.
# The Ace can count as 11 or 1.
# Use the following list as the deck of cards:
# cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# The cards in the list have equal probability of being drawn.
# Cards are not removed from the deck as they are drawn.
# The computer is the dealer.

# import section
import random


def add_card(deck):
    """function selects the random card and add it to the deck
    if the card is ace and sum of cards with ace is higher than 21
    then it counts ace as 1
    returns extended deck"""
    # variable creation
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    new_card = random.choice(cards)
    if new_card == 11 and (sum(deck) + new_card) > 21:
        new_card = 1
    deck.append(new_card)
    return deck


def show_cards(deck, mode):
    """function shows the cards from a deck
    mode = 0 only first card
    mode = 1 all cards"""
    if mode == 0:
        return deck[0]
    elif mode == 1:
        return deck


def print_players_deck(deck, who):
    print(f"{who.title()}'s deck is: {show_cards(deck, 1)}, with sum of cards equal = {sum(deck)}")


def calculate_score(deck):
    """Function Calculates the score"""
    # if there are two cards, and it's blackjack - specific situation
    if len(deck) == 2 and sum(deck) == 21:
        return -1
    return sum(deck)


def compare_results(player_score, dealer_score):
    """Function which is comparing scores of a player and a dealer
    and based on the results return result of the game"""
    if player_score == dealer_score:
        return "Draw"
    elif player_score == -1:
        return "You won - blackjack"
    elif dealer_score == -1:
        return "You lose - dealer's blackjack"
    elif player_score > 21:
        return "You lose - you exceeded blackjack"
    elif dealer_score > 21:
        return "You win - dealer exceeded blackjack"
    elif player_score > dealer_score:
        return "You win - you are closer to blackjack"
    else:
        return "You lose, dealer is closer to blackjack"



def play_blackjack():
    # empty decks
    players_deck = []
    dealers_deck = []

    # two cards for computer and for player
    for i in range(2):
        add_card(deck=players_deck)
        add_card(deck=dealers_deck)

    # flag for game loop
    game_over = False
    while not game_over:
        # calculation of the sum of cards
        user_score = calculate_score(players_deck)
        dealers_score = calculate_score(dealers_deck)

        print_players_deck(players_deck, "Player")
        print(f"First card of the dealer is: {show_cards(dealers_deck, 0)}")

        # if after two cards, and it's blackjack or player has more than 21 - game_over
        if user_score == -1 or dealers_score ==-1 or user_score > 21:
            game_over = True
        else:
            take_next_card = ""
            while take_next_card not in ("yes", "no"):
                take_next_card = input("Do you want to take another card? yes/no\n").lower()
                if take_next_card == "yes":
                    # take new card
                    add_card(deck=players_deck)
                elif take_next_card == "no":
                    # stop taking cards for the player
                    game_over = True

    # add cards of dealer if it does not have blackjack (-1) and score is lower than 17
    while dealers_score != -1 and dealers_score < 17:
        # add card
        add_card(deck= dealers_deck)
        # recalculate score
        dealers_score = calculate_score(deck=dealers_deck)

    # printing the final result + decks
    print(compare_results(player_score=user_score, dealer_score=dealers_score))
    print_players_deck(players_deck, "Player")
    print_players_deck(dealers_deck, "Dealer")

    new_game = ""
    while new_game not in ("yes", "no"):
        new_game = input("Do you want to play new game? yes/no: ").lower()
    if new_game == "yes":
        play_blackjack()
    else:
        return 0


play_blackjack()
