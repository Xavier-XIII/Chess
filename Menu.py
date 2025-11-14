import tkinter as tk

class Menu:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Menu Example")

        self.label = tk.Label(master, text="Welcome to the Menu")
        self.label.pack(pady=10)
        self.start_button = tk.Button(master, text="Start Game")
        self.start_button.pack(pady=5)
        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(pady=5)

