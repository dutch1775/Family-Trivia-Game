# game.py
import tkinter as tk
from gui import FamilyPursuitApp

def main():
    print("Starting TrivialFamily Pursuit App") #cmd debug
    #make tkinter process
    root = tk.Tk()
    
    #create an instance of the game
    app = FamilyPursuitApp(root)
    
    #start tkinter loop
    root.mainloop()

if __name__ == "__main__":
    main()
