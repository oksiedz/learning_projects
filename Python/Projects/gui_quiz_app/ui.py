from tkinter import *

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Quiz App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score label (top right)
        self.score_label = Label(text="Score = 0", font=("Arial", 14, "bold"), fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1, sticky="e")

        # Canvas with text area
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.canvas.create_text(
            150,
            125,
            text="Pytanie quizowe",
            font=("Arial", 20, "italic"),
            width=280,
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)

        # Load images
        self.true_img = PhotoImage(file="images/true.png")
        self.false_img = PhotoImage(file="images/false.png")

        # Buttons (labels with images)
        self.true_label = Label(image=self.true_img, bg=THEME_COLOR)
        self.false_label = Label(image=self.false_img, bg=THEME_COLOR)

        self.true_label.grid(row=2, column=0, padx=20)
        self.false_label.grid(row=2, column=1, padx=20)

        self.window.mainloop()
