import random
from graphics import hangman_logo, hangman_ascii
word_list = ["player", "cat", "roundabout"]
selected_word = random.choice(word_list).lower()
lives = 6
end_of_game = False

answer = []
for letter in selected_word:
    answer.append("_")

print(hangman_logo)

while not end_of_game:
    print(f"Word to guess is: {answer}")
    guess = input("Please provide a letter\n").lower()

    if guess not in selected_word:
        print(f"Letter {guess} is not existing in the word to be guessed")
        lives -= 1
        if lives == 0:
            end_of_game = True
            print("You used all guesses - you lose.")
    else:
        if guess in answer:
            print(f"You already provided letter {guess}")
        else:
            for i in range(0, len(selected_word)):
                if selected_word[i] == guess:
                    answer[i] = guess
            if "_" not in answer:
                end_of_game = True
                print(f"You guessed the word {selected_word}, you won!")
    print(hangman_ascii[lives])