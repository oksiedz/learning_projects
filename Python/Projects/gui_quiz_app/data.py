import requests
import html

# Fetch questions from Open Trivia Database API
def get_trivia_questions():
    url = "https://opentdb.com/api.php"
    params = {
        "amount": 10,
        "type": "boolean"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["response_code"] == 0:
            # Normalize the questions to match our expected format
            normalized_questions = []
            for question in data["results"]:
                # Unescape HTML entities in the question
                normalized_question = {
                    "category": question["category"],
                    "type": question["type"],
                    "difficulty": question["difficulty"],
                    "question": html.unescape(question["question"]),
                    "correct_answer": question["correct_answer"],
                    "incorrect_answers": [answer for answer in question["incorrect_answers"]]
                }
                normalized_questions.append(normalized_question)
            return normalized_questions
        else:
            print(f"API error: response_code {data['response_code']}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")
        return []

# Get the questions
try:
    question_data = get_trivia_questions()
    if not question_data:
        print("Failed to fetch questions, using empty list")
        question_data = []
except Exception as e:
    print(f"Error: {e}")
    question_data = []
