from Piece import Piece


class Board:
    def __init__(self):
        self.piecesMap = [[None for _ in range(8)] for _ in range(8)]
        self.piecesList = []

    def clear(self):
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
        if xTo == xFrom and yTo == yFrom: return

        self.piecesList.remove(self.piecesMap[xFrom][yFrom])
        if self.piecesMap[xTo][yTo] is not None:
            self.piecesList.remove(self.piecesMap[xTo][yTo])
        self.piecesMap[xTo][yTo] = self.piecesMap[xFrom][yFrom]
        self.piecesMap[xTo][yTo].x = xTo
        self.piecesMap[xTo][yTo].y = yTo
        self.piecesList.append(self.piecesMap[xTo][yTo])
        self.piecesMap[xFrom][yFrom] = None

        if self.piecesMap[xTo][yTo].name == "pawn":
            self.piecesMap[xTo][yTo].reset_time_since_last_move()

        self.increase_time()

    def increase_time(self):
        for piece in self.piecesList:
            if piece.name == "pawn" :
                piece.increase_time_since_last_move()

    # TODO: Chess coordinates to xy coordinates
    # TODO: FEN string
