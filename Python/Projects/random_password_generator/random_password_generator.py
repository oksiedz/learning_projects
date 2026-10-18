#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many letters would you like in your password?\n")) 
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

#Eazy Level - Order not randomised:
#e.g. 4 letter, 2 symbol, 2 number = JduE&!91

password = ""
for number in range(0,nr_letters):
  random_value_letter = random.randint(0, len(letters)-1)
  password += letters[random_value_letter]                       

for number in (range(0, nr_symbols)):
  random_value_symbol = random.randint(0, len(symbols) - 1)
  password += symbols[random_value_symbol]

for number in range(0, nr_numbers):
  random_value_number = random.randint(0, len(numbers) - 1)
  password += numbers[random_value_number]

print(password)

#Hard Level - Order of characters randomised:
#e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P
password_hard = ""
list_of_chars = []
used_letters = 0
used_symbols = 0
used_numbers = 0

for number in range(0, nr_letters + nr_symbols + nr_numbers):
  remaining_letters = nr_letters - used_letters
  remaining_symbols = nr_symbols - used_symbols
  remaining_numbers = nr_numbers - used_numbers
  chosed_type = ""
  if (remaining_letters > 0) and (remaining_symbols > 0) and (remaining_numbers > 0):
    chosed_type = random.choice(["l","s","n"])
    list_of_chars.append(chosed_type)
  elif (remaining_letters > 0) and (remaining_symbols > 0):
    chosed_type = random.choice(["l","s"])
    list_of_chars.append(chosed_type)
  elif (remaining_letters > 0) and (remaining_numbers > 0):
    chosed_type = random.choice(["l","n"])
    list_of_chars.append(chosed_type)  
  elif (remaining_symbols > 0) and (remaining_numbers > 0):
    chosed_type = random.choice(["s","n"])
    list_of_chars.append(chosed_type)  
  elif (remaining_letters > 0):
    chosed_type = "l"
    list_of_chars.append(chosed_type)
  elif (remaining_symbols > 0):
    chosed_type = "s"
    list_of_chars.append(chosed_type)  
  elif (remaining_numbers > 0):
    chosed_type = "n"
    list_of_chars.append(chosed_type)
    if chosed_type == "l":
      used_letters += 1
    elif chosed_type == "s":
      used_symbols += 1
    else:
      used_numbers += 1

for char in list_of_chars:
  if char == "l":
    password_hard += random.choice(letters)
  elif char == "s":
    password_hard += random.choice(symbols)
  else:
    password_hard += random.choice(numbers)

print(password_hard)

#second option ofr hard version
password_hard2_list = []
for number in range(0,nr_letters):
  random_value_letter = random.randint(0, len(letters)-1)
  password_hard2_list.append(letters[random_value_letter])

for number in (range(0, nr_symbols)):
  random_value_symbol = random.randint(0, len(symbols) - 1)
  password_hard2_list.append(symbols[random_value_symbol])

for number in range(0, nr_numbers):
  random_value_number = random.randint(0, len(numbers) - 1)
  password_hard2_list.append(numbers[random_value_number])

#print(password_hard2_list)
random.shuffle(password_hard2_list)
#print(password_hard2_list)

password_hard2 = ""
for password_sign in password_hard2_list:
  password_hard2 += password_sign
print(password_hard2)