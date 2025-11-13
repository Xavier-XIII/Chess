import pygame

DARK_GREEN = (40, 173, 49)
LIGHT_GREEN = (79, 238, 90)
RED = (191, 25, 25)

class Renderer:
    def __init__(self, unit: int, fps: int):
        # initialize pygame
        pygame.init()

        # configurations
        self.unit = unit
        self.fps = fps
        self.window_height = 8 * self.unit
        self.window_width = 8 * self.unit

        # creating window
        self.display = pygame.display.set_mode((self.window_width, self.window_height))

        # title and logo
        pygame.display.set_caption("Chess")
        # https://www.freepik.com/premium-vector/chess-logo-business-abstract-concept-icon-black-game-figure-sign-vector-flat-style_65312141.htm
        logo = pygame.image.load('images/logo.png')
        pygame.display.set_icon(logo)

        # creating our frame regulator
        self.clock = pygame.time.Clock()

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
