import random
import pygame
from pygame import gfxdraw
import sys

# initialize pygame
pygame.init()

# configurations
frequency = 1 # in updates per second
unit = 60
block_width_number = 8
block_height_number = 8
block_number = block_height_number*block_width_number
fps = 15
window_height = block_height_number * unit
window_width = block_width_number * unit
fps_per_frequency = int(fps / frequency)
frame = fps_per_frequency

# creating window
display = pygame.display.set_mode((window_width, window_height))

# images of each piece
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

# title and logo
pygame.display.set_caption("Chess")
# https://www.freepik.com/premium-vector/chess-logo-business-abstract-concept-icon-black-game-figure-sign-vector-flat-style_65312141.htm
logo = pygame.image.load('images/logo.png')
pygame.display.set_icon(logo)

# colours (yes, I'm canadian, I put u's in words)
DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)
RED = (191, 25, 25)

# creating our frame regulator
clock = pygame.time.Clock()


def place_piece(colour: str, piece: str, x: int, y: int):
    display.blit(images[colour][piece], (x * unit, y * unit))


def draw_grid():
    for x in range(int(block_width_number)):
        for y in range(int(block_height_number)):
            rect = pygame.Rect(x * unit, y * unit, unit, unit)
            pygame.draw.rect(display, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN, rect)
            """
            # for showing positions of each cell
            text = pygame.font.Font('comfortaa.ttf', 15)
            text_surface = text.render(f"{x}, {y}", True, RED)
            text_rect = text_surface.get_rect(center=((x * block_size) + block_size / 2, (y * block_size) + block_size / 2))
            display.blit(text_surface, text_rect)
            """
            # if apples[x][y]:
            #     gfxdraw.filled_circle(display, x * unit + int(unit / 2),
            #                           y * unit + int(unit / 2), int(3 * unit / 8), RED)
            #     gfxdraw.aacircle(display, x * unit + int(unit / 2),
            #                      y * unit + int(unit / 2), int(3 * unit / 8), RED)
    pygame.display.flip()


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

draw_grid()
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



    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
