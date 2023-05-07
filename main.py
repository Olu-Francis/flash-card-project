from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
word = {}
to_learn = {}

# ----------------- FUNCTIONALITIES ---------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_words, text=word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_f)
    flip_timer = window.after(3000, card_flip_mechanism)

# ---- Card flip mechanism ---- #

def card_flip_mechanism():
    # To change the image:
    canvas.itemconfig(canvas_image, image=card_b)
    # To change the text:
    global word
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_words, fill="white", text=word["English"])

def learnt():
    to_learn.remove(word)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ----------------- UI ---------------- #
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, card_flip_mechanism)

# Images
card_f = PhotoImage(file="images/card_front.png")
card_b = PhotoImage(file="images/card_back.png")
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_f)
card_title = canvas.create_text(400, 150, text="", fill="black", font=(FONT_NAME, 40, "italic"))
card_words = canvas.create_text(400, 263, text="", fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_btn_img = PhotoImage(file="images/wrong.png")
right_btn_img = PhotoImage(file="images/right.png")
wrong_btn = Button(image=wrong_btn_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_btn.grid(row=1, column=0)
right_btn = Button(image=right_btn_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=learnt)
right_btn.grid(row=1, column=1)

next_card()

window.mainloop()
