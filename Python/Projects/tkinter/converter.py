import tkinter as tk


def convert_miles_to_km():
    """Method converting the value inserted in input field to kilometers
    It refreshes the value presented in label4"""
    try:
        miles = float(input_field.get())
        kilometers = miles * 1.609344
        label4.config(text=kilometers)
    except:
        print("No miles were inserted")


window = tk.Tk()
window.title("Mile to kilometers converter")
window.config(padx=20, pady=20)

default_value_in_input_field = tk.StringVar()
default_value_in_input_field.set("0")

input_field = tk.Entry(width=5, textvariable=default_value_in_input_field)
input_field.grid(column=1, row=0)

label1 = tk.Label(text="Miles")
label1.grid(column=2, row=0)

label2 = tk.Label(text="equals to:")
label2.grid(column=0, row=1)

label4 = tk.Label(text="0")
label4.grid(column=1, row=1)

label3 = tk.Label(text="kilometers")
label3.grid(column=2, row=1)

button = tk.Button(text="Convert", command=convert_miles_to_km)
button.grid(column=1, row=2)
button.config(padx=5, pady=5)

window.mainloop()
