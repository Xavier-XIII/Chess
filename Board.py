import tkinter as tk

from Piece import Piece, Pawn, make_piece, King

to_return = ""
def choose_piece() -> str:
    global to_return
    root = tk.Tk()
    root.title("Choose piece")
    root.geometry("300x150")

    to_return = ""

    tk.Label(root, text="Choose which piece").pack(pady=10)

    def queen():
        global to_return
        root.quit()
        to_return = "queen"
    def rook():
        global to_return
        root.quit()
        to_return = "rook"
    def knight():
        global to_return
        root.quit()
        to_return = "knight"
    def bishop():
        global to_return
        root.quit()
        to_return = "bishop"

    tk.Button(root, text="Queen", command=queen).pack(padx=10)
    tk.Button(root, text="Rook", command=rook).pack(padx=10)
    tk.Button(root, text="Knight", command=knight).pack(padx=10)
    tk.Button(root, text="Bishop", command=bishop).pack(padx=10)

    root.mainloop()
    root.destroy()

    return to_return


class Board:
    def __init__(self):
        self.piecesMap:list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]
        self.piecesList:list[Piece] = []
        self.white_king:Piece|None = None
        self.black_king:Piece|None = None

    def clear(self):
        self.piecesMap = [[None for _ in range(8)] for _ in range(8)]
        self.piecesList = []

    def add_piece(self, piece: Piece, x: int, y: int):
        self.piecesMap[x][y] = piece
        piece.x = x
        piece.y = y
        self.piecesList.append(piece)
        if isinstance(piece, King):
            if piece.colour == "white":
                self.white_king = piece
            else:
                self.black_king = piece

    def get_piece(self, x: int, y: int) -> Piece:
        return self.piecesMap[x][y]

    def move_piece(self, xFrom: int, yFrom:int, xTo: int, yTo: int):
        if xTo == xFrom and yTo == yFrom: return

        p = self.piecesMap[xTo][yTo]

        self.piecesList.remove(self.piecesMap[xFrom][yFrom])
        if p is not None:
            self.piecesList.remove(p)
        self.piecesMap[xTo][yTo] = self.piecesMap[xFrom][yFrom]
        self.piecesMap[xTo][yTo].x = xTo
        self.piecesMap[xTo][yTo].y = yTo
        self.piecesMap[xTo][yTo].has_moved = True
        self.piecesList.append(self.piecesMap[xTo][yTo])
        self.piecesMap[xFrom][yFrom] = None

        p = self.piecesMap[xTo][yTo]
        if isinstance(p, Pawn):
            p.reset_time_since_last_move()
            # En passant capture
            behind = self.get_piece(xTo, yTo + 1) if p.colour == "white" else self.get_piece(xTo, yTo - 1)
            if behind is not None and isinstance(behind, Pawn) and behind.colour != p.colour and behind.time_since_last_move == 1:
                self.piecesList.remove(behind)
                self.piecesMap[behind.x][behind.y] = None
            # Promotion
            if (p.colour == "white" and yTo == 0) or (p.colour == "black" and yTo == 7):
                self.piecesList.remove(p)
                self.piecesMap[xTo][yTo] = make_piece(choose_piece(), p.colour, xTo, yTo)
                self.piecesMap[xTo][yTo].has_moved = p.has_moved
                self.piecesList.append(self.piecesMap[xTo][yTo])

        if isinstance(p, King) and p.is_castling:
            if xTo == 6: # Kingside
                rook = self.get_piece(7, yTo)
                self.piecesList.remove(rook)
                self.piecesMap[5][yTo] = rook
                rook.x = 5
                rook.y = yTo
                rook.has_moved = True
                self.piecesMap[7][yTo] = None
                self.piecesList.append(rook)
            elif xTo == 2: # Queenside
                rook = self.get_piece(0, yTo)
                self.piecesList.remove(rook)
                self.piecesMap[3][yTo] = rook
                rook.x = 3
                rook.y = yTo
                rook.has_moved = True
                self.piecesMap[0][yTo] = None
                self.piecesList.append(rook)
            p.is_castling = False

        self.increase_time()

    def increase_time(self):
        for piece in self.piecesList:
            if isinstance(piece, Pawn):
                piece.increase_time_since_last_move()

    # TODO: Chess coordinates to xy coordinates
    # TODO: FEN string
