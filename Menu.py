import os
import tkinter as tk
import tkinter.font as tkFont
from typing import Callable

import API
from Board import Board

GREEN = "#44a83d"
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
        self.unrestricted = False
        self.playing_as = "manual"
        self.opponent = "manual"
        self.ai_state = "pause"
        self.changed_squares = set()

        self.master = master
        self.master.title("Chess")
        self.master.geometry(f"{unit*8 + 500}x{unit*8 + 200}")
        self.master.config(bg=LIGHT_GREY)
        self.master.resizable(False, False)

        title = tkFont.Font(family="Courier New", size=18, weight="bold")
        small = tkFont.Font(family="Courier New", size=12, weight="bold")

        top_frame = tk.Frame(master, width=unit*8 + 300, height=unit*8, bg=LIGHT_GREY)
        top_frame.pack(side="top", padx=10, pady=10)

        for num in range(1, 9):
            label_frame = tk.Frame(top_frame, height=unit, width=20)
            label_frame.pack_propagate(False)
            tk.Label(label_frame, text=(9 - num), font=title, height=20, width=unit,
                     bg=LIGHT_YELLOW if num % 2 == 0 else BROWN).pack()
            label_frame.place(x=0, y=(num - 1) * unit + 20)

        for i, letter in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
            label_frame = tk.Frame(top_frame, height=20, width=unit)
            label_frame.pack_propagate(False)
            tk.Label(label_frame, text=letter, font=title, height=20, width=unit,
                     bg=LIGHT_YELLOW if i % 2 == 0 else BROWN).pack()
            label_frame.place(x=i * unit + 20, y=unit * 8 + 20)

        pygame_frame = tk.Frame(top_frame, width=unit*8, height=unit*8, bg="black")
        pygame_frame.pack(side="left", padx=20, pady=20, anchor="nw")
        os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'


        ai_control_frame = tk.Frame(top_frame, width=300, height=unit * 8, bg=LIGHT_GREY)
        ai_control_frame.pack(side="right", padx=10, pady=20, anchor="nw")
        ai_control_label = tk.Label(ai_control_frame, text="AI Control:", font=title, bg=LIGHT_GREY, fg="white")
        ai_control_label.pack(pady=10)
        self.play_button = tk.Button(ai_control_frame, text="Play", command=lambda: self.set_ai_state("play"), state="disabled", font=small, bg=LIGHT_GREY, fg="white")
        self.play_button.pack(pady=5)
        self.pause_button = tk.Button(ai_control_frame, text="Pause", command=lambda: self.set_ai_state("pause"), state="disabled", font=small, bg=GREEN, fg="white")
        self.pause_button.pack(pady=5)
        self.step_button = tk.Button(ai_control_frame, text="Step", command=lambda: self.set_ai_state("step"), state="disabled", font=small, bg=LIGHT_GREY, fg="white")
        self.step_button.pack(pady=5)

        self.unrestricted_button = tk.Button(ai_control_frame, text="Restricted", command=self.flip_restricted, font=small, bg=LIGHT_GREY, fg="white")
        self.unrestricted_button.pack(pady=5)

        ttc_frame = tk.Frame(ai_control_frame, width=300, height=50, bg=LIGHT_GREY)
        ttc_frame.pack(side="right", padx=10, pady=20, anchor="e")
        ttc_label = tk.Label(ttc_frame, text="Time to compute (ms):", font=small, bg=LIGHT_GREY, fg="white")
        ttc_label.pack(pady=10)
        self.ttc_entry = tk.Entry(ttc_frame, font=small, bg="white", fg="black")
        self.ttc_entry.pack(pady=5)
        self.ttc_entry.insert(0, "200")


        info_frame = tk.Frame(top_frame, width=300, height=unit*8, bg=LIGHT_GREY)
        info_frame.pack(side="right", padx=10, pady=20, anchor="nw")
        info_label = tk.Label(info_frame, text="Info:", font=title, bg=LIGHT_GREY, fg="white")
        info_label.pack(pady=10)
        self.currently_playing_label = tk.Label(info_frame, text="White playing", font=small, bg=LIGHT_GREY, fg="white")
        self.currently_playing_label.pack(pady=20)
        self.turn_number_label = tk.Label(info_frame, text="Turn #1", font=small, bg=LIGHT_GREY, fg="white")
        self.turn_number_label.pack(pady=20)
        self.history = tk.Listbox(info_frame, font=small, bg=LIGHT_GREY, fg="white")
        self.history.pack(pady=20)


        choosing_frame = tk.Frame(master, width=unit*8 + 300, height=200, bg=LIGHT_GREY)
        choosing_frame.pack(side="top", padx=10, pady=20)

        opponent_frame = tk.Frame(choosing_frame, width=unit*8 + 300, height=100, bg=LIGHT_GREY)
        opponent_frame.pack(padx=10, side="left")
        opponent_label = tk.Label(opponent_frame, text="Opponent:", font=title, bg=LIGHT_GREY, fg="white")
        opponent_label.pack(pady=10)
        self.opponent_manual = tk.Button(opponent_frame, text="Manual", command=lambda: self.set_opponent("manual"), font=small, bg=GREEN, fg="white")
        self.opponent_manual.pack(pady=5, side="left")
        self.opponent_random = tk.Button(opponent_frame, text="Random", command=lambda: self.set_opponent("random"), font=small, bg=LIGHT_GREY, fg="white")
        self.opponent_random.pack(pady=5, side="left")
        self.opponent_chessgpt = tk.Button(opponent_frame, text="ChessGPT", command=lambda: self.set_opponent("chessgpt"), font=small, bg=LIGHT_GREY, fg="white")
        self.opponent_chessgpt.pack(pady=5, side="left")
        self.opponent_stockfish = tk.Button(opponent_frame, text="Stockfish", command=lambda: self.set_opponent("stockfish"), font=small, bg=LIGHT_GREY, fg="white")
        self.opponent_stockfish.pack(pady=5, side="left")

        playing_as_frame = tk.Frame(choosing_frame, width=unit*8 + 300, height=100, bg=LIGHT_GREY)
        playing_as_frame.pack(padx=10, side="right")
        playing_as_label = tk.Label(playing_as_frame, text="Playing as:", font=title, bg=LIGHT_GREY, fg="white")
        playing_as_label.pack(pady=10)
        self.playing_as_manual = tk.Button(playing_as_frame, text="Manual", command=lambda: self.set_playing_as("manual"), font=small, bg=GREEN, fg="white")
        self.playing_as_manual.pack(pady=5, side="left")
        self.playing_as_random = tk.Button(playing_as_frame, text="Random", command=lambda: self.set_playing_as("random"), font=small, bg=LIGHT_GREY, fg="white")
        self.playing_as_random.pack(pady=5, side="left")
        self.playing_as_chessgpt = tk.Button(playing_as_frame, text="ChessGPT", command=lambda: self.set_playing_as("chessgpt"), font=small, bg=LIGHT_GREY, fg="white")
        self.playing_as_chessgpt.pack(pady=5, side="left")
        self.playing_as_stockfish = tk.Button(playing_as_frame, text="Stockfish", command=lambda: self.set_playing_as("stockfish"), font=small, bg=LIGHT_GREY, fg="white")
        self.playing_as_stockfish.pack(pady=5, side="left")

        self.should_quit = False

    def update(self, currently_playing: str, updated: bool, turn_number: int) -> tuple[bool, str, bool, set]:
        self.currently_playing_label.config(text=f"{currently_playing.capitalize()} playing")
        self.currently_playing = currently_playing
        self.turn_number_label.config(text=f"Turn #{turn_number}")

        if (self.playing_as != "manual" or self.opponent != "manual") and self.ai_state != "pause":
            self.make_next_move()
            if self.ai_state == "step":
                self.set_ai_state("pause")

        if self.computed:
            if self.currently_playing == "white":
                self.currently_playing = "black"
            else:
                self.currently_playing = "white"

        updated_return = self.updated or updated or self.computed
        if self.updated or self.computed:
            self.updated = False
            self.computed = False

        changed_squares_copy = self.changed_squares.copy()
        self.changed_squares.clear()

        return updated_return, self.currently_playing, self.unrestricted, changed_squares_copy

    def set_playing_as(self, playing_as: str):
        self.playing_as = playing_as
        self.playing_as_manual.config(bg=GREEN if playing_as == "manual" else LIGHT_GREY)
        self.playing_as_random.config(bg=GREEN if playing_as == "random" else LIGHT_GREY)
        self.playing_as_chessgpt.config(bg=GREEN if playing_as == "chessgpt" else LIGHT_GREY)
        self.playing_as_stockfish.config(bg=GREEN if playing_as == "stockfish" else LIGHT_GREY)
        self.play_button.config(state="normal" if (playing_as != "manual" or self.opponent != "manual") else "disabled")
        self.pause_button.config(state="normal" if (playing_as != "manual" or self.opponent != "manual") else "disabled")
        self.step_button.config(state="normal" if (playing_as != "manual" or self.opponent != "manual") else "disabled")
        self.unrestricted_button.config(state="normal" if playing_as == "manual" else "disabled")

    def set_opponent(self, opponent: str):
        self.opponent = opponent
        self.opponent_manual.config(bg=GREEN if opponent == "manual" else LIGHT_GREY)
        self.opponent_random.config(bg=GREEN if opponent == "random" else LIGHT_GREY)
        self.opponent_chessgpt.config(bg=GREEN if opponent == "chessgpt" else LIGHT_GREY)
        self.opponent_stockfish.config(bg=GREEN if opponent == "stockfish" else LIGHT_GREY)
        self.play_button.config(state="normal" if (opponent != "manual" or self.playing_as != "manual") else "disabled")
        self.pause_button.config(state="normal" if (opponent != "manual" or self.playing_as != "manual") else "disabled")
        self.step_button.config(state="normal" if (opponent != "manual" or self.playing_as != "manual") else "disabled")
        self.unrestricted_button.config(state="normal" if opponent == "manual" else "disabled")

    def set_ai_state(self, state: str):
        self.ai_state = state
        self.play_button.config(bg=GREEN if state == "play" else LIGHT_GREY)
        self.pause_button.config(bg=GREEN if state == "pause" else LIGHT_GREY)
        self.step_button.config(bg=GREEN if state == "step" else LIGHT_GREY)

    def set_restart(self, restart: Callable):
        self.restart = restart

    def get_restart(self):
        self.restart()

    def flip_restricted(self):
        self.unrestricted = not self.unrestricted
        self.unrestricted_button.config(text="Restricted" if not self.unrestricted else "Unrestricted", bg=LIGHT_GREY if not self.unrestricted else "RED")

    def make_next_move(self):
        move = None
        match self.playing_as if self.currently_playing == "white" else self.opponent:
            case "random":
                move = API.random_turn(self.board.piecesMap, self.board.piecesList, self.currently_playing, float(self.ttc_entry.get()) / 1000)
            case "stockfish":
                move = API.stockfish_turn(self.board.piecesList, self.currently_playing, float(self.ttc_entry.get()) / 1000)
            case "chessgpt":
                move = API.chess_gpt_turn(self.board.piecesMap, self.board.piecesList, self.currently_playing, float(self.ttc_entry.get()) / 1000)

        if move is not None and self.ai_state != "pause":
            result = self.board.move_piece(move[0][0], move[0][1], move[1][0], move[1][1], True)
            if result is not None:
                if result[0] is not None:
                    self.changed_squares = self.changed_squares.union(result[0])
                self.history.insert(0, result[1])
            self.changed_squares.add(move[0])
            self.changed_squares.add(move[1])
            self.history.insert(0, f"{move[0]} to {move[1]}")
            self.computed = True

    def quit(self):
        self.master.destroy()
        self.should_quit = True

