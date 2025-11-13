from Piece import Piece


class Board:
    def __init__(self):
        self.piecesMap = [[None for _ in range(8)] for _ in range(8)]
        self.piecesList = []

    def add_piece(self, piece: Piece, x: int, y: int):
        self.piecesMap[x][y] = piece
        piece.x = x
        piece.y = y
        self.piecesList.append(piece)

    def get_piece(self, x: int, y: int) -> Piece:
        return self.piecesMap[x][y]

    def move_piece(self, xFrom: int, yFrom:int, xTo: int, yTo: int):
        print("moving piece from", xFrom, yFrom, "to", xTo, yTo)
        self.piecesList.remove(self.piecesMap[xFrom][yFrom])
        if self.piecesMap[xTo][yTo] is not None:
            self.piecesList.remove(self.piecesMap[xTo][yTo])
        self.piecesMap[xTo][yTo] = self.piecesMap[xFrom][yFrom]
        self.piecesMap[xTo][yTo].x = xTo
        self.piecesMap[xTo][yTo].y = yTo
        self.piecesList.append(self.piecesMap[xTo][yTo])
        self.piecesMap[xFrom][yFrom] = None
