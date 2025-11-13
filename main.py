import pygame
import sys

from Renderer import Renderer

unit = 60  # size of each square
fps = 15
renderer = Renderer(unit, fps)

from Board import Board
from Piece import Piece

board = Board()
display = renderer.display
clock = renderer.clock
frequency = 1  # in updates per second
fps_per_frequency = int(fps / frequency)
frame = fps_per_frequency
player_playing_as = "white"
selected_piece = None
updated = False


def place_piece(colour: str, name: str, x: int, y: int):
    piece = Piece(name, colour, x, y)
    renderer.draw_piece(piece.get_image(), x, y)
    board.add_piece(piece, x, y)


def manage_click(x: int, y: int):
    global selected_piece
    global updated
    boardX = int(x / unit)
    boardY = int(y / unit)
    print("click at", x, y, boardX, boardY)

    if selected_piece is None:
        selected_piece = board.get_piece(boardX, boardY)
        print("selected piece:", selected_piece)
    else:
        board.move_piece(selected_piece.x, selected_piece.y, boardX, boardY)
        selected_piece = None
        print("moved piece to:", boardX, boardY)
        print(board.get_piece(boardX, boardY))
    updated = True


def place_pieces():
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
    place_piece("white", "bishop", 7, 7)
    place_piece("black", "rook", 0, 0)
    place_piece("black", "knight", 1, 0)
    place_piece("black", "bishop", 2, 0)
    place_piece("black", "queen", 3, 0)
    place_piece("black", "king", 4, 0)
    place_piece("black", "bishop", 5, 0)
    place_piece("black", "knight", 6, 0)
    place_piece("black", "bishop", 7, 0)

renderer.draw_grid()
place_pieces()

# forever loop
while True:
    # frame clock ticking
    clock.tick(fps)

    # draw stuff once per second
    if frame == fps_per_frequency:

        frame = 0
        ticks = pygame.time.get_ticks()

    frame += 1

    if updated:
        print("updating board")
        renderer.draw_grid()
        if selected_piece is not None:
            renderer.draw_square(selected_piece.x, selected_piece.y, (221, 227, 57))
        for piece in board.piecesList:
            renderer.draw_piece(piece.get_image(), piece.x, piece.y)
        updated = False

    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                manage_click(event.pos[0], event.pos[1])
