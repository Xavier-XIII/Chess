import pygame

pieces = [
    "pawn",
    "knight",
    "bishop",
    "rook",
    "queen",
    "king"
]
unit = 60


class Piece:
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

    def __init__(self, name: str, colour: str, x: int, y: int):
        self.name = name
        self.colour = colour
        self.x = x
        self.y = y

    def get_image(self):
        return self.images[self.colour][self.name]

    def __str__(self):
        return f"{self.colour} {self.name} at ({self.x}, {self.y})"