#TODO: asking a question
#TODO: checking if the answer is correct
#TODO: checking if we're at the of the quiz

# attributes - question_number = 0, questions_list
# method - next question()

class QuizBrain:
    def __init__(self, in_question_list):
        """Constructor stetting question number to 0, score to 0 and as questions_list provided input"""
        self.question_number = 0
        self.questions_list = in_question_list
        self.score = 0

    def next_question(self):
        """Method asking the next question"""
        current_question = self.questions_list[self.question_number]
        self.question_number += 1
        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False)? ")
        self.check_answer(user_answer, current_question.answer)

    def still_have_questions(self):
        """Method returns boolean if there are still questions which were not asked"""
        return self.question_number < len(self.questions_list)

    def check_answer(self, input_answer, corr_answer):
        """Method checking if there was provided correct answer or not"""
        if input_answer.lower() == corr_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong!")
        print(f"The correct answer was: {corr_answer}")
        print(f"Your current score is {self.score}/{self.question_number}")
        print("\n")

