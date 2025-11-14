import os
import tkinter as tk
import tkinter.font as tkFont

LIGHT_GREY = "#212121"

class Menu:
    def __init__(self, master: tk.Tk, unit: int):
        self.master = master
        self.master.title("Chess menu")
        self.master.geometry(f"{unit*8 + 200}x{unit*8+20}")
        self.master.config(bg=LIGHT_GREY)

        custom_font = tkFont.Font(family="Courier New", size=14, weight="bold")

        pygame_frame = tk.Frame(master, width=unit*8, height=unit*8, bg="black")
        pygame_frame.pack(side="left", padx=10, pady=10, anchor="w")

        os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        options_frame = tk.Frame(master, width=200, height=200, bg=LIGHT_GREY)
        options_frame.pack(side="right", padx=10, pady=10, anchor="e")
        label_ = tk.Label(options_frame, text="Options", font=custom_font)
        label_.pack(pady=10)

        label = tk.Label(options_frame, text="Options", font=custom_font)
        label.pack(pady=10)
        start_button = tk.Button(options_frame, text="Restart Game", font=custom_font)
        start_button.pack(pady=5)
        quit_button = tk.Button(options_frame, text="Quit", command=quit, font=custom_font)
        quit_button.pack(pady=5)

        self.should_quit = False

    def update(self):
        self.master.update()

    def quit(self):
        self.master.destroy()
        self.should_quit = True

