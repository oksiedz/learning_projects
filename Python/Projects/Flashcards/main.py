import tkinter as tk
import random

import pandas as pandas

BACKGROUND_COLOR = "#B1DDC6"
CANVAS_HEIGHT = 526
CANVAS_WIDTH = 800

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

dict_to_learn = data.to_dict(orient='records')
card = {}


def next_flashcard():
    """Method taking words from data frame and show them on canvas"""
    global card, flip_time
    window.after_cancel(flip_time)
    card = random.choice(dict_to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=card["French"], fill="black")
    canvas.itemconfig(card_background, image=img_cr_front)
    # to turn the card after 3 seconds
    flip_time = window.after(3000, func=flip_card)


def incorrect_button():
    next_flashcard()


def correct_button():
    dict_to_learn.remove(card)
    data_to_learn = pandas.DataFrame(dict_to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_flashcard()


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=card["English"], fill="white")
    canvas.itemconfig(card_background, image=img_cr_back)


window = tk.Tk()
window.title("Flashcard app")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# after 3 seconds call function flip card
flip_time = window.after(3000, func=flip_card)

img_wrong = tk.PhotoImage(file="./images/wrong.png")
img_right = tk.PhotoImage(file="./images/right.png")
img_cr_front = tk.PhotoImage(file='./images/card_front.png')
img_cr_back = tk.PhotoImage(file='./images/card_back.png')
canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0, bg=BACKGROUND_COLOR)
card_background = canvas.create_image(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, image=img_cr_front)
# card_back = canvas.create_image(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, image=img_cr_back)
card_title = canvas.create_text(CANVAS_WIDTH/2, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, text="bottom", font=("Ariel", 60, "bold"))

but_wrong = tk.Button(image=img_wrong, highlightthickness=0, command=incorrect_button)
but_right = tk.Button(image=img_right, highlightthickness=0, command=correct_button)

# locations
but_wrong.grid(column=0, row=1)
but_right.grid(column=1, row=1)
canvas.grid(column=0, row=0, columnspan=2)

# generate new flashcard at the beginning
next_flashcard()

window.mainloop()
