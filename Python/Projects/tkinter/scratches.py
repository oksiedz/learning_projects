import tkinter as _tk


def button_clicked():
    my_label.config(text=input_field.get())


def spinbox_used():
    """gets the current value in spinbox"""
    print(spinbox.get())


def scale_used(value):
    print(value)


def checkbutton_used():
    """prints 1 if on button checked, otherwise 0."""
    print(checked_state.get())


def radio_used():
    print(radio_state.get())


def listbox_used(event):
    """Gets current selection from listbox"""
    print(listbox.get(listbox.curselection()))


window = _tk.Tk()
window.title("Simple GUI interface")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

# label
my_label = _tk.Label(text="Label text", font=("Arial", 24, "bold"))
# change of options of components
my_label["text"] = "New Text"
my_label.config(text="New Text 2")
# my_label.pack(side="top")  # component is put on the screen and centered
# my_label.place(x=0, y=0) # specific localization
my_label.grid(column=0, row=0)

# buttons
button = _tk.Button(text="Click me please", command=button_clicked)
# button.pack()
button.grid(column=1, row=1)
button.config(padx=20, pady=20)

# Entry component (input)
input_field = _tk.Entry(width=10)
# input_field.insert(END, string="example text")
print(input_field.get())
# input_field.pack()
input_field.grid(column=2, row=2)


# Text
text = _tk.Text(height=5, width=30)
text.focus()  # puts cursor in textbox
text.insert(_tk.END, "Example of multiline text entry")  # adds some text to begin with
print(text.get("1.0", _tk.END))  # gets the current value in textbox at line 1, character 0
# text.pack()
text.grid(column=3, row=3)


# spinbox
spinbox = _tk.Spinbox(from_=0, to=10, width=5, command=spinbox_used)
# spinbox.pack()
spinbox.grid(column=4, row=4)

# Scale
scale = _tk.Scale(from_=0, to=100, command=scale_used)
# scale.pack()
scale.grid(column=0, row=1)

# checkbutton
checked_state = _tk.IntVar()
checkbutton = _tk.Checkbutton(text="Is On?", variable=checked_state, command=checkbutton_used)
checked_state.get()
# checkbutton.pack()
checkbutton.grid(column=0, row=2)

# radiobutton
radio_state = _tk.IntVar()
radiobutton1 = _tk.Radiobutton(text="Option 1", value=1, variable=radio_state, command=radio_used)
radiobutton2 = _tk.Radiobutton(text="Option 2", value=2, variable=radio_state, command=radio_used)
# radiobutton1.pack()
# radiobutton2.pack()
radiobutton1.grid(column=1, row=2)
radiobutton2.grid(column=1, row=2)

# listbox
listbox = _tk.Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
# listbox.pack()
listbox.grid(column=3, row=2)
# always at the end, it is a while loop with listeners
window.mainloop()
