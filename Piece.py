pieces = [
    "pawn",
    "knight",
    "bishop",
    "rook",
    "queen",
    "king"
]

class Piece:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

    def get_name(self) -> str:
        return self.name