import pygame
from pygame import gfxdraw

from Board import Board

DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)
YELLOW = (221, 227, 57)

base_radius = 15

class Renderer:
    def __init__(self, unit: int, board: Board):
        pygame.init()

        self.unit = unit
        self.window_height = 8 * self.unit
        self.window_width = 8 * self.unit

        self.display = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_caption("Chess")
        # https://www.freepik.com/premium-vector/chess-logo-business-abstract-concept-icon-black-game-figure-sign-vector-flat-style_65312141.htm
        logo = pygame.image.load('images/logo.png')
        pygame.display.set_icon(logo)

        self.board = board

    def draw_grid(self):
        for x in range(8):
            for y in range(8):
                self.erase_quare(x, y)
        pygame.display.flip()

    def erase_quare(self, x: int, y: int):
        self.draw_square(x, y, DARK_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN)

    def draw_square(self, x: int, y: int, colour: tuple):
        rect = pygame.Rect(x * self.unit, y * self.unit, self.unit, self.unit)
        pygame.draw.rect(self.display, colour, rect)

    def draw_piece(self, image, x: int, y: int):
        self.display.blit(image, (x * self.unit, y * self.unit))

    def draw_circle(self, x: int, y: int, radius: int = base_radius):
        gfxdraw.filled_circle(self.display, x * self.unit + int(self.unit / 2),
                              y * self.unit + int(self.unit / 2), radius, YELLOW)
        gfxdraw.aacircle(self.display, x * self.unit + int(self.unit / 2),
                         y * self.unit + int(self.unit / 2), radius, YELLOW)

    def draw_possible_moves(self, moves: set[tuple[int, int]]):
        for move in moves:
            target_x = move[0]
            target_y = move[1]
            if 0 <= target_x < 8 and 0 <= target_y < 8:
                self.draw_circle(target_x, target_y)

