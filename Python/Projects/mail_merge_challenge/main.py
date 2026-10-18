# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".

# Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
# Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
# Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

STRING_TO_REPLACE = "[name]"

with open(file="./Input/Names/invited_names.txt", mode="r") as file_with_names:
    names = file_with_names.readlines()

with open(file="./Input/Letters/starting_letter.txt", mode="r") as file_letter_template:
    letter_template = file_letter_template.read()
    for name in names:
        trimmed_name = name.strip()
        filled_letter = letter_template.replace(STRING_TO_REPLACE, trimmed_name)
        print(filled_letter)
        with open(file=f"./Output/ReadyToSend/letter_for_{trimmed_name}.txt", mode="w") as final_letter:
            final_letter.write(filled_letter)

