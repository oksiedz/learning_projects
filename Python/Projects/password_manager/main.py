import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json

# CONSTANTS #

FILE = "credentials.json"


def set_default_email_username():
    entry_email_username.delete(0, tk.END)
    entry_email_username.insert(0, "example@email.com")


def empty_value():
    print("There are some empty values")
    messagebox.showinfo(title="Entry error", message="Please do not leave any field empty!")


def read_json():
    with open(file=FILE, mode="r") as file:
        # reading old data
        return json.load(fp=file)


def write_json(json_data):
    with open(file=FILE, mode="w") as file:
        json.dump(obj=json_data, fp=file, indent=4)


def clear_entries():
    entry_website.delete(0, tk.END)
    set_default_email_username()
    entry_password.delete(0, tk.END)
    entry_website.focus()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generate():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    # concatenating symbols
    password = "".join(password_list)

    print(f"Your password is generated")

    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    # keeping value in copy and paste
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    """Method is saving website, username/email and password"""
    # save inserted values as variables
    website = entry_website.get()
    email_username = entry_email_username.get()
    password = entry_password.get()

    new_data = {
        website: {
            "email": email_username,
            "password": password
        }
    }
    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        empty_value()
    else:
        print("All values are not empty")
        # adding message box
        save_confirmed = messagebox.askokcancel(title="Please confirm",
                                                message=f'You entered below details:\n'
                                                        f'Website: {website}\n'
                                                        f'Email/Username: {email_username}\n'
                                                        f'Password: {password}\n'
                                                        f'Do you want to save them?')
        if save_confirmed:
            print("Password saving is confirmed")
            # open the file and check if the value already exists if not then add
            try:
                data = read_json()
                # updating old data with new data
            except FileNotFoundError:
                write_json(json_data=new_data)
            else:
                if new_data.items() <= data.items():
                    print("Such connection string already exists")
                else:
                    data.update(new_data)
                    print(data)
                    # how to write new json to the file
                    write_json(json_data=new_data)
                    print("Connection string saved")
            finally:
                # cleaning the entries
                clear_entries()
        else:
            print("Password saving not confirmed")
            messagebox.showinfo(title="Info", message="Credentials not saved!")
            clear_entries()


def search_credentials():
    try:
        data = read_json()
    except FileNotFoundError:
        messagebox.showinfo(title="File not found", message="There is no file with passwords yet.!")
    else:
        website = entry_website.get()
        if website in data:
            email_username = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title="Password found",
                                message=f"For website: {website} and username/email: {email_username} "
                                        f"there is saved password: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error",
                                message=f"There is no password for website: {website}")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(bg="white", padx=50, pady=50)
# canvas
canvas = tk.Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_logo)
canvas.grid(column=1, row=0)
# labels
label_website = tk.Label(text="Website:", bg="white", justify="right")
label_website.grid(column=0, row=1)
label_email_username = tk.Label(text="Email/Username:", bg="white")
label_email_username.grid(column=0, row=2)
label_password = tk.Label(text="Password:", bg="white")
label_password.grid(column=0, row=3)
# entries
entry_website = tk.Entry(width=21)
entry_website.grid(column=1, row=1)
# setting cursor on the entry for website
entry_website.focus()

entry_email_username = tk.Entry(width=35)
entry_email_username.grid(column=1, row=2, columnspan=2)
# insert already default value at the begging of the field - 0
entry_email_username.insert(0, "example@email.com")

entry_password = tk.Entry(width=21)
entry_password.grid(column=1, row=3)
# buttons
button_generate_password = tk.Button(text="Generate Password", command=password_generate)
button_generate_password.grid(column=2, row=3)

button_add = tk.Button(text="Add", command=add_password, width=36)
button_add.grid(column=1, row=4, columnspan=2)

button_search = tk.Button(text="Search", command=search_credentials)
button_search.grid(column=2, row=1)

window.mainloop()
