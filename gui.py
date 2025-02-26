import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import random
import json

# Load questions from JSON file
def load_questions(file):
    with open(file, "r") as f:
        return json.load(f)

class FamilyPursuitApp:
    def __init__(self, root):
        #TODO - figure out how to get all elements centered and get new theme
        self.root = root
        self.root.title("Family Pursuit")
        self.root.geometry("800x600") 
        style = Style(theme="flatly") 

        #load questions
        self.questions = load_questions("questions.json")

        #extract unique categories from questions
        self.categories = list(set(q["category"] for q in self.questions if "category" in q))

        #initialize team variables
        self.team1 = None
        self.team2 = None
        self.current_team = None
        self.team_progress = {}

        #create game frames
        self.home_frame = tk.Frame(self.root)
        self.setup_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.question_frame = tk.Frame(self.root)

        for frame in (self.home_frame, self.setup_frame, self.main_frame, self.question_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_home_page()
        self.show_frame(self.home_frame)

    #show a specific frame
    def show_frame(self, frame):
        frame.tkraise()

    def create_home_page(self):
        print("Creating Home Page")

        title_label = tk.Label(self.home_frame, text="Family Pursuit", font=("Times New Roman", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        start_button = tk.Button(self.home_frame, text="Start Game", font=("Times New Roman", 16), command=self.start_game)
        start_button.grid(row=1, column=0, columnspan=2, pady=10)

        exit_button = tk.Button(self.home_frame, text="Exit", font=("Times New Roman", 16), command=self.root.quit)
        exit_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)

    #setup screen
    def start_game(self):
        print("Game Started!")
        self.show_frame(self.setup_frame)

        for widget in self.setup_frame.winfo_children():
            widget.destroy()

        tk.Label(self.setup_frame, text="Enter Team 1 Name:", font=("Times New Roman", 16)).grid(row=0, column=0, padx=10, pady=5)
        self.team1_entry = tk.Entry(self.setup_frame, font=("Times New Roman", 16))
        self.team1_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.setup_frame, text="Enter Team 2 Name:", font=("Times New Roman", 16)).grid(row=1, column=0, padx=10, pady=5)
        self.team2_entry = tk.Entry(self.setup_frame, font=("Times New Roman", 16))
        self.team2_entry.grid(row=1, column=1, padx=10, pady=5)

        start_button = tk.Button(self.setup_frame, text="Start Game", font=("Times New Roman", 16),
                                 command=self.initialize_teams)
        start_button.grid(row=2, column=0, columnspan=2, pady=10)

    #initialize teams
    def initialize_teams(self):
        self.team1 = self.team1_entry.get() or "Team 1"
        self.team2 = self.team2_entry.get() or "Team 2"
        self.current_team = self.team1  #team 1 starts

        #track progress for both teams
        self.team_progress = {
            self.team1: {category: False for category in self.categories},
            self.team2: {category: False for category in self.categories}
        }

        print(f"Teams: {self.team1} vs {self.team2}")

        self.show_frame(self.main_frame)
        self.create_gameboard()

    #create gameboard with categories
    def create_gameboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.team_turn_label = tk.Label(self.main_frame, text=f"{self.current_team}'s Turn",
                                        font=("Times New Roman", 18, "bold"))
        self.team_turn_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.category_buttons = {}

        for i, category in enumerate(self.categories):
            btn = tk.Button(self.main_frame, text=category, font=("Times New Roman", 16),
                            command=lambda c=category: self.ask_question(c))
            btn.grid(row=(i // 2) + 1, column=i % 2, padx=10, pady=5)
            self.category_buttons[category] = btn

    #ask a question from a category
    #TODO - make questions randomized
    def ask_question(self, category):
        print(f"ask_question called with category: {category}")

        questions_in_category = [q for q in self.questions if q.get("category") == category]

        if not questions_in_category:
            messagebox.showinfo("No Questions", f"No questions available for {category}!")
            return

        self.current_question = random.choice(questions_in_category)
        self.questions.remove(self.current_question)

        self.show_frame(self.question_frame)

        for widget in self.question_frame.winfo_children():
            widget.destroy()

        question_label = tk.Label(self.question_frame, text=self.current_question["question"],
                                  font=("Times New Roman", 16))
        question_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.answer_entry = tk.Entry(self.question_frame, font=("Times New Roman", 16))
        self.answer_entry.grid(row=1, column=0, columnspan=2, pady=5)

        submit_button = tk.Button(self.question_frame, text="Submit",
                                  command=lambda: self.check_answer(category))
        submit_button.grid(row=2, column=0, columnspan=2, pady=5)

    #check the answer
    def check_answer(self, category):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_question["answer"].strip().lower()

        if user_answer == correct_answer:
            messagebox.showinfo("Correct!", f"{self.current_team} got it right!")
            self.team_progress[self.current_team][category] = True

            if all(self.team_progress[team][category] for team in self.team_progress):
                self.category_buttons[category].config(state=tk.DISABLED)
        else:
            messagebox.showerror("Wrong!", f"Sorry, the correct answer was: {self.current_question['answer']}")

        self.current_team = self.team1 if self.current_team == self.team2 else self.team2
        self.team_turn_label.config(text=f"{self.current_team}'s Turn")

        self.check_game_completion()
        self.show_frame(self.main_frame)

    #check if all categories are completed
    def check_game_completion(self):
        team1_completed = all(self.team_progress[self.team1].values())
        team2_completed = all(self.team_progress[self.team2].values())

        if team1_completed and team2_completed:
            messagebox.showinfo("Game Over!", "Both teams have completed all categories! Game Over!")
            self.root.quit()
