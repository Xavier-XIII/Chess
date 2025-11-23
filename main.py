import sys
import tkinter as tk

import pygame

from Board import Board
from Menu import Menu
from Piece import Piece, make_piece
from Renderer import Renderer

#This is a fork of chess repo

unit = 60  # size of each square
root = tk.Tk()
board = Board()
menu = Menu(root, unit, board)
renderer = Renderer(unit, board)
display = renderer.display
currently_playing = "white"
turn_number = 1
selected_piece:Piece|None = None
selected_piece_moves:set[tuple[int, int]] = set()
updated = True
tick_num = True
unrestricted = False

images = {
    "white": {
        "pawn": pygame.transform.scale(pygame.image.load('images/pieces/white_pawn.png').convert_alpha(), (unit, unit)),
        "knight": pygame.transform.scale(pygame.image.load('images/pieces/white_knight.png').convert_alpha(), (unit, unit)),
        "bishop": pygame.transform.scale(pygame.image.load('images/pieces/white_bishop.png').convert_alpha(), (unit, unit)),
        "rook": pygame.transform.scale(pygame.image.load('images/pieces/white_rook.png').convert_alpha(), (unit, unit)),
        "queen": pygame.transform.scale(pygame.image.load('images/pieces/white_queen.png').convert_alpha(), (unit, unit)),
        "king": pygame.transform.scale(pygame.image.load('images/pieces/white_king.png').convert_alpha(), (unit, unit))
    },
    "black": {
        "pawn": pygame.transform.scale(pygame.image.load('images/pieces/black_pawn.png').convert_alpha(), (unit, unit)),
        "knight": pygame.transform.scale(pygame.image.load('images/pieces/black_knight.png').convert_alpha(), (unit, unit)),
        "bishop": pygame.transform.scale(pygame.image.load('images/pieces/black_bishop.png').convert_alpha(), (unit, unit)),
        "rook": pygame.transform.scale(pygame.image.load('images/pieces/black_rook.png').convert_alpha(), (unit, unit)),
        "queen": pygame.transform.scale(pygame.image.load('images/pieces/black_queen.png').convert_alpha(), (unit, unit)),
        "king": pygame.transform.scale(pygame.image.load('images/pieces/black_king.png').convert_alpha(), (unit, unit))
    }
}


def get_image(piece: Piece):
    return images[piece.colour][piece.__class__.__name__.lower()]


def place_piece(colour: str, name: str, x: int, y: int):
    piece = make_piece(name, colour, x, y)
    renderer.draw_piece(get_image(piece), x, y)
    board.add_piece(piece, x, y)


def set_selected_piece(piece: Piece | None):
    global selected_piece
    global selected_piece_moves

    selected_piece = piece
    if piece is not None and not unrestricted:
        selected_piece_moves = piece.get_possible_moves(board.piecesMap)
    else:
        selected_piece_moves = set()

    renderer.changed_squares.add((piece.x, piece.y)) if piece is not None else None


def try_move_piece(piece: Piece, xTo: int, yTo: int) -> bool:
    global currently_playing
    global selected_piece_moves

    if piece.colour != currently_playing:
        return False
    if (xTo, yTo) in selected_piece_moves:
        result = board.move_piece(piece.x, piece.y, xTo, yTo)
        if result is not None:
            menu.history.insert(0, result[1])
            if result[0] is not None:
                renderer.changed_squares = renderer.changed_squares.union(result[0])
        currently_playing = "black" if currently_playing == "white" else "white"
        set_selected_piece(None)
        return True
    return False


def manage_click(x: int, y: int):
    global turn_number
    global selected_piece
    global updated
    global unrestricted
    boardX = int(x / unit)
    boardY = int(y / unit)

    updated = True

    if unrestricted:
        piece = board.get_piece(boardX, boardY)
        if selected_piece is None:
            set_selected_piece(piece)
            return

        if piece is not selected_piece and selected_piece is not None:
            result = board.move_piece(selected_piece.x, selected_piece.y, boardX, boardY)
            if result is not None:
                menu.history.insert(0, result[1])
                if result[0] is not None:
                    renderer.changed_squares = renderer.changed_squares.union(result[0])
            set_selected_piece(None)
        else:
            if selected_piece is not None:
                set_selected_piece(None)
    else:
        if selected_piece is not None and boardX == selected_piece.x and boardY == selected_piece.y:
            set_selected_piece(None)
            return

        if selected_piece is None or (boardX, boardY) not in selected_piece_moves:
            set_selected_piece(board.get_piece(boardX, boardY))
        else:
            if try_move_piece(selected_piece, boardX, boardY):
                turn_number += 1


def place_pieces():
    global currently_playing
    global updated

    board.clear()
    currently_playing = "white"

    for i in range(8):
        place_piece("white", "pawn", i, 6)
        place_piece("black", "pawn", i, 1)
    place_piece("white", "rook", 0, 7)
    place_piece("white", "knight", 1, 7)
    place_piece("white", "bishop", 2, 7)
    place_piece("white", "queen", 3, 7)
    place_piece("white", "king", 4, 7)
    place_piece("white", "bishop", 5, 7)
    place_piece("white", "knight", 6, 7)
    place_piece("white", "rook", 7, 7)
    place_piece("black", "rook", 0, 0)
    place_piece("black", "knight", 1, 0)
    place_piece("black", "bishop", 2, 0)
    place_piece("black", "queen", 3, 0)
    place_piece("black", "king", 4, 0)
    place_piece("black", "bishop", 5, 0)
    place_piece("black", "knight", 6, 0)
    place_piece("black", "rook", 7, 0)
    updated = True

menu.set_restart(place_pieces)
place_pieces()

def tick_game():
    global updated
    global currently_playing
    global unrestricted
    global tick_num

    if updated or tick_num < 15:
        if tick_num < 15:
            renderer.draw_grid()
            for piece in board.piecesList:
                renderer.draw_piece(get_image(piece), piece.x, piece.y)
            renderer.changed_squares = set()

        pieces_to_draw = set()

        for square in renderer.changed_squares:
            renderer.erase_quare(square[0], square[1])
            if board.get_piece(square[0], square[1]) is not None:
                pieces_to_draw.add((board.get_piece(square[0], square[1]), square[0], square[1]))

        if board.last_to is not None:
            renderer.draw_square(board.last_from[0], board.last_from[1], (210, 219, 101))
            renderer.draw_square(board.last_to[0], board.last_to[1], (210, 219, 101))

        if selected_piece is not None:
            renderer.draw_square(selected_piece.x, selected_piece.y, (210, 224, 99))
            if selected_piece.colour == currently_playing and not unrestricted:
                renderer.draw_possible_moves(selected_piece_moves)

        for item in pieces_to_draw:
            renderer.draw_piece(get_image(item[0]), item[1], item[2], changed=False)


        squares_to_remove = set()
        for square in renderer.changed_squares:
            if (square not in selected_piece_moves and
                    square != board.last_from and square != board.last_to):
                if selected_piece is None:
                    squares_to_remove.add(square)
                elif square[0] != selected_piece.x and square[1] != selected_piece.y:
                    squares_to_remove.add(square)

        renderer.changed_squares = renderer.changed_squares.difference(squares_to_remove)

        updated = False
        tick_num += 1

    pygame.display.flip()

    result = menu.update(currently_playing, updated, turn_number)
    updated = result[0]
    currently_playing = result[1]
    unrestricted = result[2]
    renderer.changed_squares = renderer.changed_squares.union(result[3])

    for event in pygame.event.get():
        if event.type == pygame.QUIT or menu.should_quit:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                manage_click(event.pos[0], event.pos[1])
    root.after(10, tick_game)


if __name__ == "__main__":
    tick_game()
    root.mainloop()
    pygame.quit()
