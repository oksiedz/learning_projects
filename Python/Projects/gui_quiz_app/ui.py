from tkinter import *

from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quiz App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score label (top right)
        self.score_label = Label(text="Score = 0", font=("Arial", 14, "bold"), fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1, sticky="e")

        # Canvas with text area
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, # half of width
            125, # half of height
            text="Pytanie quizowe",
            font=("Arial", 20, "italic"),
            fill=THEME_COLOR,
            width=280,
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # Load images
        self.true_img = PhotoImage(file="images/true.png")
        self.false_img = PhotoImage(file="images/false.png")

        # Buttons (labels with images)        
        self.true_button = Button(image=self.true_img, highlightthickness=0, command=self.true_pressed)
        self.false_button = Button(image=self.false_img, highlightthickness=0, command=self.false_pressed)

        self.true_button.grid(row=2, column=0, padx=20)
        self.false_button.grid(row=2, column=1, padx=20)

        self.get_next_question()  # Load the first question
        self.get_score()  # Update the score label
    
        # end of loop
        self.window.mainloop()

    def get_next_question(self):
        """Method to get the next question from the quiz and update the UI."""
        question_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=question_text)

    def true_pressed(self):
        """Method to handle the event when the 'True' button is pressed."""
        self.quiz.check_answer("True")
        self.get_next_question()
        self.get_score()

    def false_pressed(self):
        """Method to handle the event when the 'False' button is pressed."""
        self.quiz.check_answer("False")
        self.get_next_question()
        self.get_score()

    def get_score(self):
        """Method to get the current score from the quiz."""
        score_value = self.quiz.score
        self.score_label.config(text=f"Score = {score_value}")
