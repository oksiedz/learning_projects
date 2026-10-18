import random
import pandas

# comprehension example 1
numbers = [1, 2, 3]
new_numbers = [n * 2 for n in numbers]

# comprehension example 2
string = "Richard"
new_list = [letter.upper() for letter in string]
print(new_list)

# comprehension example 3
new_list2 = [n * 2 for n in range(1, 5)]
print(new_list2)

# conditional list comprehension
names = ["Alex", "Beth", "Caroline", "Dave", "Elanor", "Freddie"]
# print only names shorter than 5 signs
print([name for name in names if len(name) < 5])
print([name.upper() for name in names if len(name) >= 5])

# example 4
numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
print("squared list")
print([pow(number, 2) for number in numbers])

# example 5
input_list = "1, 1, 2, 3, 5, 8, 13, 21, 34, 55"
list_of_strings = input_list.split(',')
input_list_int = [int(i) for i in list_of_strings]
odd_numbers = [number for number in input_list_int if number % 2 != 0]
even_numbers = [number for number in input_list_int if number not in odd_numbers]
print(f'Even numbers: {even_numbers}')

# example 6
FILE1_PATH = "Input_files/file1.txt"
FILE2_PATH = "Input_files/file2.txt"
MODE = "r"


def list_without_new_lines_symbol(in_string):
    return [int(line.replace("\n", "")) for line in in_string]


with open(file=FILE1_PATH, mode=MODE) as file1:
    file1_content = list_without_new_lines_symbol(file1.readlines())

with open(file=FILE2_PATH, mode=MODE) as file2:
    file2_content = list_without_new_lines_symbol(file2.readlines())

# only common numbers from both lists
result = [item for item in file1_content if item in file2_content]
print(result)

# ############################################# #
# ############################################# #
# Dictionary Comprehension
# ############################################# #
# ############################################# #
# new_dict = {new_key:new_value for item in list}
# new_dict = {new_key:new_value for (key, value) in dict.items if test}

# example 1 - create random results for students
names = ["Alex", "Beth", "Caroline", "Dave", "Elanor", "Freddie"]
student_scores = {student: random.randint(1, 100) for student in names}
passed_students = {key: value for (key, value) in student_scores.items() if value >= 60}
print(student_scores)
print(passed_students)

# example 2
input_text = "What is the Airspeed Velocity of an Unladen Swallow?"
list_of_words = input_text.split(sep=" ")
result = {word: len(word) for word in list_of_words}
print(result)

# example 3
input_dict = {"Monday": 12,
              "Tuesday": 14,
              "Wednesday": 15,
              "Thursday": 14,
              "Friday": 21,
              "Saturday": 22,
              "Sunday": 24}

dict_with_fahrenheits = {day: temperature * 9/5 + 32 for (day, temperature) in input_dict.items()}
print(dict_with_fahrenheits)

# How to iterate over a Pandas DataFrame
student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}

# looping through dictionaries:
for (key, value) in student_dict.items():
    print(value)

student_data_frame = pandas.DataFrame(student_dict)
print(student_data_frame)
# loop through data frame
# for (key, value) in student_data_frame.items():
#     print(key)
#     print(value)
for (index,row) in student_data_frame.iterrows():
    print(index)
    print(row)
    print(row.student)
    if row.student == "Angela":
        print(f'{row.student} achieved {row.score}')