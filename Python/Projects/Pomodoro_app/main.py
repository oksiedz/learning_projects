import tkinter as tk
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 224
SEC_IN_MIN = 60

repetitions = 0
timer = None


def increase_rep():
    global repetitions
    repetitions += 1


def reset_repetitions():
    global repetitions
    repetitions = 0


def add_checkmark():
    global repetitions
    times = math.floor(repetitions / 2)
    label_text = ""
    for i in range(times):
        label_text += "☑"

    check_label.config(text=label_text)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_pomodoro():
    window.after_cancel(timer)
    reset_repetitions()
    check_label.config(text="")
    pomodoro_timer_label.config(fg=GREEN, text="Timer")
    canvas.itemconfig(tagOrId=timer_text, text=f'00:00')


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_pomodoro():
    increase_rep()

    work_sec = WORK_MIN * SEC_IN_MIN
    short_break = SHORT_BREAK_MIN * SEC_IN_MIN
    long_break = LONG_BREAK_MIN * SEC_IN_MIN

    if repetitions in (1, 3, 5, 7):
        count_down(work_sec)
        pomodoro_timer_label.config(text="Work", fg=GREEN)
    elif repetitions == 8:
        count_down(long_break)
        pomodoro_timer_label.config(text="Break", fg=RED)
    elif repetitions in (2, 4, 6):
        count_down(short_break)
        pomodoro_timer_label.config(text="Break", fg=PINK)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'

    canvas.itemconfig(tagOrId=timer_text, text=f'{count_min}:{count_sec}')
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    if count == 0:
        start_pomodoro()
        add_checkmark()


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro app")
window.config(padx=100, pady=50, bg=YELLOW)

# canvas
canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=YELLOW, highlightthickness=0)
tomato_picture = tk.PhotoImage(file="Attachments/tomato.png")
canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=tomato_picture)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# label Timer
pomodoro_timer_label = tk.Label(fg=GREEN, bg=YELLOW, text="Timer", font=(FONT_NAME, 35, "bold"))
pomodoro_timer_label.grid(column=1, row=0)
# label checkboxes
check_label = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
check_label.grid(column=1, row=3)

# start and reset button
start_button = tk.Button(text="Start", command=start_pomodoro, highlightthickness=0)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_pomodoro, highlightthickness=0)
reset_button.grid(column=2, row=2)

window.mainloop()
