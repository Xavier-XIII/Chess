pieces = [
    "pawn",
    "knight",
    "bishop",
    "rook",
    "queen",
    "king"
]
unit = 60

knight_offsets = {(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)}
bishop_directions = {(-1, -1), (1, -1), (1, 1), (-1, 1)}
rook_directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
king_offsets = {(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)}


def within_bounds(x: int, y: int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8


def make_piece(name: str, colour: str, x: int, y: int) -> 'Piece':
    if name == "pawn":
        return Pawn(colour, x, y)
    elif name == "knight":
        return Knight(colour, x, y)
    elif name == "bishop":
        return Bishop(colour, x, y)
    elif name == "rook":
        return Rook(colour, x, y)
    elif name == "queen":
        return Queen(colour, x, y)
    elif name == "king":
        return King(colour, x, y)
    else:
        raise ValueError(f"Unknown piece name: {name}")


def get_offset_moves(piece:'Piece', board_map: list[list['Piece']], offsets: set[tuple[int, int]]) -> set[tuple[int, int]]:
    moves = set()
    for move in offsets:
        target_x = piece.x + move[0]
        target_y = piece.y + move[1]
        if 0 <= target_x < 8 and 0 <= target_y < 8:
            p = board_map[target_x][target_y]
            if p is None or p.colour != piece.colour:
                moves.add((target_x, target_y))
    return moves

def get_linear_moves(piece:'Piece', board_map: list[list['Piece']], directions: set[tuple[int, int]]) -> set[tuple[int, int]]:
    moves = set()
    for d in directions:
        for i in range(1, 8):
            x = piece.x + d[0] * i
            y = piece.y + d[1] * i
            if x < 0 or x > 7 or y < 0 or y > 7: break
            p = board_map[x][y]
            if p is None:
                moves.add((x, y))
            else:
                if p.colour != piece.colour:
                    moves.add((x, y))
                break
    return moves


def is_square_under_attack(px: int, py: int, colour: str, board_map: list[list['Piece']]) -> bool:
    # Pawn
    o = 1 if colour == "black" else -1
    if within_bounds(px + 1, py + o) and isinstance(board_map[px + 1][py + o], Pawn) and board_map[px + 1][py + o].colour != colour:
        return True
    if within_bounds(px - 1, py + o) and isinstance(board_map[px - 1][py + o], Pawn) and board_map[px - 1][py + o].colour != colour:
        return True
    # Knight
    for move in knight_offsets:
        target_x = px + move[0]
        target_y = py + move[1]
        if 0 <= target_x < 8 and 0 <= target_y < 8:
            p = board_map[target_x][target_y]
            if p is not None and isinstance(p, Knight) and p.colour != colour:
                return True
    # Rook and Queen
    for d in rook_directions:
        for i in range(1, 8):
            target_x = px + d[0] * i
            target_y = py + d[1] * i
            if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7: break
            p = board_map[target_x][target_y]
            if p is not None:
                if (isinstance(p, Rook) or isinstance(p, Queen)) and p.colour != colour:
                    return True
                break
    # Bishop and Queen
    for d in bishop_directions:
        for i in range(1, 8):
            target_x = px + d[0] * i
            target_y = py + d[1] * i
            if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7: break
            p = board_map[target_x][target_y]
            if p is not None:
                if (isinstance(p, Bishop) or isinstance(p, Queen)) and p.colour != colour:
                    return True
                break

    # King
    for move in king_offsets:
        target_x = px + move[0]
        target_y = py + move[1]
        if 0 <= target_x < 8 and 0 <= target_y < 8:
            p = board_map[target_x][target_y]
            if p is not None and isinstance(p, King) and p.colour != colour:
                return True

    return False


class Piece:
    def __init__(self, colour: str, x: int, y: int):
        self.colour = colour
        self.x = x
        self.y = y
        self.has_moved = False
        self.pinned = False # TODO: Implement pinned pieces

    def get_possible_moves(self, board_map: list[list['Piece']]) -> set[tuple[int, int]]:
        pass

    def get_actual_positions(self, moves: set[tuple[int, int]]) -> set[tuple[int, int]]:
        actual_moves = set()
        for move in moves:
            actual_moves.add((self.x + move[0], self.y + move[1]))
        return actual_moves

    def __str__(self) -> str:
        return f"{self.colour} {self.__class__.__name__} at ({self.x}, {self.y})"


class Pawn(Piece):
    def __init__(self, colour: str, x: int, y: int):
        super().__init__(colour, x, y)
        self.time_since_last_move = 0

    def get_possible_moves(self, board_map: list[list[Piece]]) -> set[tuple[int, int]]:
        moves = set()

        if self.y == 7 or self.y == 0:
            return moves

        i = 1 if self.colour == "black" else -1
        if board_map[self.x][self.y + i] is None:
            moves.add((0, i))
            if (((self.y == 1 and self.colour == "black") or (self.y == 6 and self.colour == "white"))
                    and board_map[self.x][self.y + 2 * i] is None):
                moves.add((0, 2 * i))
        if within_bounds(self.x + 1, self.y + i) and board_map[self.x + 1][self.y + i] is not None:
            if board_map[self.x + 1][self.y + i].colour != self.colour:
                moves.add((1, i))
        if within_bounds(self.x - 1, self.y + i) and board_map[self.x - 1][self.y + i] is not None:
            if board_map[self.x - 1][self.y + i].colour != self.colour:
                moves.add((-1, i))

        for r in [-1, 1]:
            if self.x + r > 7 or self.x + r < 0: continue

            p = board_map[self.x + r][self.y]
            if p is not None:
                if (p.colour != self.colour and
                    isinstance(p, Pawn) and
                    p.time_since_last_move == 1 and
                    self.y == (3 if p.colour == "black" else 4)):
                    moves.add((r, i))

        return self.get_actual_positions(moves)

    def increase_time_since_last_move(self):
        self.time_since_last_move += 1

    def reset_time_since_last_move(self):
        self.time_since_last_move = 0


class Knight(Piece):
    def __init__(self, colour: str, x: int, y: int):
        super().__init__(colour, x, y)

    def get_possible_moves(self, board_map: list[list[Piece]]) -> set[tuple[int, int]]:
        return get_offset_moves(self, board_map, knight_offsets)


class Bishop(Piece):
    def __init__(self, colour: str, x: int, y: int):
        super().__init__(colour, x, y)

    def get_possible_moves(self, board_map: list[list[Piece]]) -> set[tuple[int, int]]:
        return get_linear_moves(self, board_map, bishop_directions)


class Rook(Piece):
    def __init__(self, colour: str, x: int, y: int):
        super().__init__(colour, x, y)

    def get_possible_moves(self, board_map: list[list[Piece]]) -> set[tuple[int, int]]:
        return get_linear_moves(self, board_map, rook_directions)


class Queen(Piece):
    def __init__(self, colour: str, x: int, y: int):
        super().__init__(colour, x, y)

    def get_possible_moves(self, board_map: list[list[Piece]]) -> set[tuple[int, int]]:
        return get_linear_moves(self, board_map, bishop_directions.union(rook_directions))


class King(Piece):
    def __init__(self, colour: str, x: int, y: int):
        super().__init__(colour, x, y)
        self.is_castling = False
        self.in_check = False

    def get_possible_moves(self, board_map: list[list[Piece]]) -> set[tuple[int, int]]:
        moves = get_offset_moves(self, board_map, king_offsets)
        if (self.colour == "white" and self.y == 7) or (self.colour == "black" and self.y == 0) and not self.in_check and not self.has_moved:
            # Kingside castling
            if (board_map[self.x + 1][self.y] is None and
                    board_map[self.x + 2][self.y] is None and
                    not is_square_under_attack(self.x + 2, self.y, self.colour, board_map)):
                rook = board_map[self.x + 3][self.y]
                if rook is not None and isinstance(rook, Rook) and not rook.has_moved:
                    moves.add((self.x + 2, self.y))
                    self.is_castling = True
            # Queenside castling
            if (board_map[self.x - 1][self.y] is None and
                    board_map[self.x - 2][self.y] is None and
                    not is_square_under_attack(self.x - 2, self.y, self.colour, board_map) and
                    board_map[self.x - 3][self.y] is None):
                rook = board_map[self.x - 4][self.y]
                if rook is not None and isinstance(rook, Rook) and not rook.has_moved:
                    moves.add((self.x - 2, self.y))
                    self.is_castling = True

        moves_to_remove = set()
        for move in moves:
            if is_square_under_attack(move[0], move[1], self.colour, board_map):
                moves_to_remove.add(move)

        return moves.difference(moves_to_remove)



