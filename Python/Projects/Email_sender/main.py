# import smtplib
#
# my_email = "test_gmail@gmail.com"
# e_mail_pass = "abcdefghij"
#
# connection = smtplib.SMTP(host="smtp.gmail.com")
# # securing the connection with TLS
# connection.starttls()
# connection.login(user=my_email, password=e_mail_pass)
# connection.sendmail(from_addr=my_email, to_addrs="test_receiver@yahoo.com",
#                     msg="Subject:Hell\n\n"
#                         "This is the body of my e-mail")
# connection.close()
#
# # to avoid closing we can just write above as:
# # with smtplib.SMTP(host="smtp.gmail.com") as connection:
# #     # securing the connection with TLS
# #     connection.starttls()
# #     connection.login(user=my_email, password=e_mail_pass)
# #     connection.sendmail(from_addr=my_email, to_addrs="test_receiver@yahoo.com",
# #                         msg="Subject:Hell\n\n"
# #                             "This is the body of my e-mail")

#
# import datetime as dt
# # current date and time
# print(dt.datetime.now())
# now = dt.datetime.now()
# year_of_now = now.year
# if year_of_now == 2024:
#     print("super")


# # send random quotes
# import datetime as dt
# import random as rd
# import smtplib
#
#
# now = dt.datetime.now()
# if now.weekday() == 6:
#     with open(file="quotes.txt", mode="r") as file:
#         file_lines = file.readlines()
#         random_quote = rd.choice(file_lines)
#
#     my_email = "test_gmail@gmail.com"
#     e_mail_pass = "abcdefghij"
#     with smtplib.SMTP(host="smtp.gmail.com") as connection:
#         # securing the connection with TLS
#         connection.starttls()
#         connection.login(user=my_email, password=e_mail_pass)
#         connection.sendmail(from_addr=my_email, to_addrs="test_receiver@yahoo.com",
#                             msg=f'Subject:Quote of the day\n\n'
#                                 f'{random_quote}')
#     print(now)


##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.
import smtplib

import pandas as pd
import datetime as dt
import os
import random as rd

my_email = "test_gmail@gmail.com"
e_mail_pass = "abcdefghij"

# list of letter templates
list_of_letters = []
path_for_letters = "./letter_templates"
for path in os.listdir(path_for_letters):
    if os.path.isfile(os.path.join(path_for_letters, path)):
        list_of_letters.append(path)
    else:
        pass


birthday_data = pd.read_csv(filepath_or_buffer="birthdays.csv")
now = dt.datetime.now()
now_month = now.month
now_day = now.day
# birthdays_dict = {(birthday_data["month"], birthday_data["day"]) : data_row for (index, data_row) in birthday_data.iterrows()}
# it returns key as tupple and whole row as value
birthday_people = birthday_data[(birthday_data["month"] == now_month) & (birthday_data["day"] == now.day)]
if len(birthday_people) > 0:
    for index, row in birthday_people.iterrows():
        name = birthday_data.at[index, "name"]
        email = birthday_people.at[index, "email"]
        selected_template = path_for_letters + '/' + rd.choice(list_of_letters)
        with open(file=selected_template, mode="r") as open_template:
            letter = open_template.read()
            updated_letter = letter.replace('[NAME]', name)

            with smtplib.SMTP(host="smtp.gmail.com") as connection:
                # securing the connection with TLS
                connection.starttls()
                connection.login(user=my_email, password=e_mail_pass)
                connection.sendmail(from_addr=my_email, to_addrs=email,
                                    msg=f'Subject:Happy Birthday!\n\n'
                                        f'{updated_letter}')
else:
    pass




