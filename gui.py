# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import random
import json

#TODO - make the load in mulitple files for different quesiton sets
#subroutine to load question file in
def load_questions(file):
    with open(file, "r") as file:
        return json.load(file)

class FamilyPursuitApp:
    def __init__(self, root):
        self.root = root #the current game window
        #style and label variables
        self.root.title("Family Pursuit")
        self.root.geometry("1920x1080") #TODO - make hi-res
        #TODO - find a better theme and this rat shit
        style = Style(theme="flatly")
        #variables for keeping track of what questions have been asked already
        self.questions = load_questions("questions.json")
        self.current_question_index = 0
        self.score = 0
        self.total_questions = len(self.questions)

        #initialize game screens
        self.home_frame = tk.Frame(self.root)
        self.setup_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.question_frame = tk.Frame(self.root)
        #TODO - maybe add a results screen but unsure ATM

        #pack all the game screens (only one will be visible at a time)
        for frame in (self.home_frame, self.setup_frame, self.main_frame, self.question_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        
        #build and show the home pagev
        self.create_home_page()
        self.show_frame(self.home_frame)
    
    def create_home_page(self):
        print("Creating Home Page") #print debug statement bc im cringe and like cmdline debug
        #home screen buttons (literally just read them they explanatory)
        title_label = tk.Label(self.home_frame, text="Family Pursuit", font=("Times New Roman", 24, "bold"))
        title_label.pack(pady=20)

        start_button = tk.Button(self.home_frame, text="Start Game", font=("Times New Roman", 16), command=self.start_game)
        start_button.pack(pady=10)

        exit_button = tk.Button(self.home_frame, text="Exit", font=("Times New Roman", 16), command=self.root.quit)
        exit_button.pack(pady=10)
    
    def start_game(self):
        #cmd debug and show main screen
        print("Game Started!")
        self.show_frame(self.main_frame)

        #display the gameboard
        self.create_gameboard()

        #dice roll button
        roll_button = tk.Button(self.main_frame, text="Roll Dice", font=("Times New Roman", 16), command=self.roll_dice)
        roll_button.pack(pady=10)

        #dice roll result
        self.dice_result_label = tk.Label(self.main_frame, text="Roll the Dice!", font=("Times New Roman", 16))
        self.dice_result_label.pack(pady=10)

    def create_gameboard(self):
        #create the gameboard visuals on the main_frame (bro how do i do this)
        pass

    def roll_dice(self):
        #roll da dice and show result
        roll = random.randint(1, 6)
        self.dice_result_label.config(text=f"You rolled a {roll}!")


    def show_frame(self, frame):
            #raise frame to front screen
            frame.tkraise()
