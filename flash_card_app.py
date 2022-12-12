from tkinter import *
import random, pandas


#initialize global variables
#change here and top of csv file for different data. In csv file: Question,Answer
FRONT_FC_TOPIC = 'Question'
BACK_FC_TOPIC = 'Answer'
#change data file, question font size and time in ms between card flips
GET_DATA = 'data/cs_questions.csv'
QUESTION_FONT_SIZE = 12
TIME = 10000
#window relevant
WINDOW = Tk()
#images
CARD_BACK = PhotoImage(file='images/card_back.png')
CARD_FRONT = PhotoImage(file='images/card_front.png')
RIGHT = PhotoImage(file='images/right.png')
WRONG = PhotoImage(file='images/wrong.png')
#background color and initialization of relevant dictionaries
BACKGROUND_COLOR = '#B1DDC6'
CURRENT = {}
TO_LEARN = {}


#get releavant data to use
try:
    data = pandas.read_csv('data/to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv(GET_DATA)
    TO_LEARN = original_data.to_dict(orient='records')
else:
    TO_LEARN = data.to_dict(orient='records')


def query():
    '''Randomizes query order, presents query, and passes to flip_card after the allotted time supplied expires.'''
    global CURRENT, FLIP_TIMER
    WINDOW.after_cancel(FLIP_TIMER)
    #randomize order of flash cards
    CURRENT = random.choice(TO_LEARN)
    CANVAS.itemconfig(CARD_TITLE, text=FRONT_FC_TOPIC, fill='black')
    CANVAS.itemconfig(CARD_WORD, text=CURRENT[FRONT_FC_TOPIC], fill='black')
    CANVAS.itemconfig(CARD_BACKGROUND, image=CARD_FRONT)
    FLIP_TIMER = WINDOW.after(TIME, func=flip_card)


def flip_card():
    '''Flip flash card functionality.'''
    CANVAS.itemconfig(CARD_TITLE, text=BACK_FC_TOPIC, fill='white')
    CANVAS.itemconfig(CARD_WORD, text=CURRENT[BACK_FC_TOPIC], fill='white')
    CANVAS.itemconfig(CARD_BACKGROUND, image=CARD_BACK)


def is_right():
    '''Determines if the answer is correct, supplies information to relevant dictionaries and continues to next query.'''
    TO_LEARN.remove(CURRENT)
    data = pandas.DataFrame(TO_LEARN)
    data.to_csv('data/words_to_learn.csv', index=False)
    query()


#global variable located here because python does not support hoisting
#buttons
RIGHT_BUTTON = Button(image=RIGHT, highlightthickness=0, command=is_right)
WRONG_BUTTON = Button(image=WRONG, highlightthickness=0, command=query)


#window configurations
WINDOW.title('Flash Card Learning')
WINDOW.config(padx=40, pady=40, bg=BACKGROUND_COLOR)
FLIP_TIMER = WINDOW.after(3000, func=flip_card)
RIGHT_BUTTON.grid(column=2, row=3)
WRONG_BUTTON.grid(column=1, row=3)


#canvas at bottom to ensure proper window functionality
CANVAS = Canvas(height=526, width=800)
CARD_BACKGROUND = CANVAS.create_image(400, 263, image=CARD_FRONT)
CARD_TITLE = CANVAS.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
CARD_WORD = CANVAS.create_text(400, 263, text='', font=('Ariel', QUESTION_FONT_SIZE, 'bold'))
CANVAS.config(bg=BACKGROUND_COLOR, highlightthickness=0)
CANVAS.grid(column=1, row=1, columnspan=2)


#start flashcard query functionality.
query()


#necessary for tkinter windows
WINDOW.mainloop()
