import os
import tkinter as tk
import tkinter.font as tkFont
from typing import Callable

LIGHT_GREY = "#212121"
LIGHT_YELLOW = "#ebc459"
BROWN = "#80511f"

class Menu:
    def __init__(self, master: tk.Tk, unit: int):
        self.restart = None
        self.master = master
        self.master.title("Chess menu")
        self.master.geometry(f"{unit*8 + 200}x{unit*8+40}")
        self.master.config(bg=LIGHT_GREY)
        self.master.resizable(False, False)

        custom_font = tkFont.Font(family="Courier New", size=14, weight="bold")

        for num in range(1, 9):
            label_frame = tk.Frame(master, height=unit, width=20)
            label_frame.pack_propagate(False)
            tk.Label(label_frame, text=(9 - num), font=custom_font, height=20, width=unit,
                     bg=LIGHT_YELLOW if num % 2 == 0 else BROWN).pack()
            label_frame.place(x=0, y=(num - 1) * unit + 20)

        for i, letter in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
            label_frame = tk.Frame(master, height=20, width=unit)
            label_frame.pack_propagate(False)
            tk.Label(label_frame, text=letter, font=custom_font, height=20, width=unit,
                     bg=LIGHT_YELLOW if i % 2 == 0 else BROWN).pack()
            label_frame.place(x=i * unit + 20, y=unit * 8 + 20)


        pygame_frame = tk.Frame(master, width=unit*8, height=unit*8, bg="black")
        pygame_frame.pack(side="left", padx=20, pady=20, anchor="w")

        os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        options_frame = tk.Frame(master, width=200, height=200, bg=LIGHT_GREY)
        options_frame.pack(side="right", padx=10, pady=10, anchor="ne")
        self.currently_playing_label = tk.Label(options_frame, text="White's turn", font=custom_font, bg=LIGHT_GREY, fg="white")
        self.currently_playing_label.pack(pady=10)

        label = tk.Label(options_frame, text="Options", font=custom_font, bg=LIGHT_GREY, fg="white")
        label.pack(pady=10)
        start_button = tk.Button(options_frame, text="Restart Game", command=self.get_restart, font=custom_font, bg=LIGHT_GREY, fg="white")
        start_button.pack(pady=5)
        quit_button = tk.Button(options_frame, text="Quit", command=self.quit, font=custom_font, bg=LIGHT_GREY, fg="white")
        quit_button.pack(pady=5)

        self.should_quit = False

    def update(self, currently_playing: str, updated: bool) -> bool:
        self.currently_playing_label.config(text=f"{currently_playing.capitalize()}'s turn")
        return updated

    def set_restart(self, restart: Callable):
        self.restart = restart

    def get_restart(self):
        self.restart()

    def quit(self):
        self.master.destroy()
        self.should_quit = True

