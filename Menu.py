import os
import tkinter as tk
import tkinter.font as tkFont
from typing import Callable

import API
from Board import Board

LIGHT_GREY = "#212121"
LIGHT_YELLOW = "#ebc459"
BROWN = "#80511f"

class Menu:
    def __init__(self, master: tk.Tk, unit: int, board: Board):
        self.currently_playing = None
        self.restart = None
        self.board = board
        self.updated = False
        self.computed = False

        self.master = master
        self.master.title("Chess")
        self.master.geometry(f"{unit*8 + 200}x{unit*8+40}")
        self.master.config(bg=LIGHT_GREY)
        self.master.resizable(False, False)

        title = tkFont.Font(family="Courier New", size=18, weight="bold")
        font = tkFont.Font(family="Courier New", size=12, weight="bold")

        for num in range(1, 9):
            label_frame = tk.Frame(master, height=unit, width=20)
            label_frame.pack_propagate(False)
            tk.Label(label_frame, text=(9 - num), font=title, height=20, width=unit,
                     bg=LIGHT_YELLOW if num % 2 == 0 else BROWN).pack()
            label_frame.place(x=0, y=(num - 1) * unit + 20)

        for i, letter in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
            label_frame = tk.Frame(master, height=20, width=unit)
            label_frame.pack_propagate(False)
            tk.Label(label_frame, text=letter, font=title, height=20, width=unit,
                     bg=LIGHT_YELLOW if i % 2 == 0 else BROWN).pack()
            label_frame.place(x=i * unit + 20, y=unit * 8 + 20)


        pygame_frame = tk.Frame(master, width=unit*8, height=unit*8, bg="black")
        pygame_frame.pack(side="left", padx=20, pady=20, anchor="w")

        os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        options_frame = tk.Frame(master, width=200, height=200, bg=LIGHT_GREY)
        options_frame.pack(side="right", padx=10, pady=10, anchor="ne")
        self.currently_playing_label = tk.Label(options_frame, text="White's\nturn", font=title, bg=LIGHT_GREY, fg="white")
        self.currently_playing_label.pack(pady=20)

        self.compute_black_button = tk.Button(options_frame, text="Compute\nBlack's turn",
                                         command=self.compute_turn, font=font, bg=LIGHT_GREY, fg="white")
        self.compute_black_button.pack(pady=5)
        self.compute_white_button = tk.Button(options_frame, text="Compute\nWhite's turn",
                                         command=self.compute_turn, font=font, bg=LIGHT_GREY, fg="white")
        self.compute_white_button.pack(pady=20)

        # TODO: History of moves

        tk.Label(options_frame, text="Options", font=title, bg=LIGHT_GREY, fg="white").pack(pady=10)
        tk.Button(options_frame, text="Restart Game", command=self.get_restart, font=font, bg=LIGHT_GREY, fg="white").pack(pady=5)
        tk.Button(options_frame, text="Quit", command=self.quit, font=font, bg=LIGHT_GREY, fg="white").pack(pady=5)

        self.should_quit = False

    def update(self, currently_playing: str, updated: bool) -> tuple[bool, str]:
        self.currently_playing_label.config(text=f"{currently_playing.capitalize()}'s\nturn")
        self.currently_playing = currently_playing

        if currently_playing == "white":
            self.compute_white_button.config(state="normal")
            self.compute_black_button.config(state="disabled")
        else:
            self.compute_white_button.config(state="disabled")
            self.compute_black_button.config(state="normal")

        if self.computed:
            if self.currently_playing == "white":
                self.currently_playing = "black"
            else:
                self.currently_playing = "white"

        to_return = self.updated or updated or self.computed
        if self.updated or self.computed:
            self.updated = False
            self.computed = False

        return to_return, self.currently_playing

    def set_restart(self, restart: Callable):
        self.restart = restart

    def get_restart(self):
        self.restart()

    def compute_turn(self):
        move = API.compute_turn(self.board.piecesMap, self.board.piecesList, self.currently_playing)
        self.board.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
        self.computed = True

    def quit(self):
        self.master.destroy()
        self.should_quit = True

