from Piece import Piece


class Board:
    def __init__(self):
        self.piecesMap = [[]]
        self.piecesList = []

    def add_piece(self, piece: Piece, x: int, y: int):
        self.piecesMap[x][y] = piece
        piece.x = x
        piece.y = y
        self.piecesList.append(piece)

    def get_piece(self, x: int, y: int) -> Piece:
        return self.piecesMap[x][y]

    def move_piece(self, xFrom: int, yFrom:int, xTo: int, yTo: int):
        self.piecesMap[xTo][yTo] = self.piecesMap[xFrom][yFrom]
