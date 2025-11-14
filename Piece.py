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


class Piece:
    def __init__(self, name: str, colour: str, x: int, y: int):
        self.name = name
        self.colour = colour
        self.x = x
        self.y = y

    def get_possible_moves(self, board_map: dict) -> set[tuple[int, int]]:
        moves = set()
        match self.name:
            case "pawn":
                moves = self.get_pawn_moves(board_map)
            case "knight":
                moves = self.get_offset_moves(board_map, knight_offsets)
            case "bishop":
                moves = self.get_linear_moves(board_map, bishop_directions)
            case "rook":
                moves = self.get_linear_moves(board_map, rook_directions)
            case "queen":
                moves = self.get_linear_moves(board_map, bishop_directions.union(rook_directions))
            case "king":
                moves = self.get_offset_moves(board_map, king_offsets)

        return moves

    def get_pawn_moves(self, board_map: dict) -> set[tuple[int, int]]:
        moves = set()
        # TODO: En passant, promotion
        i = 1 if self.colour == "black" else -1
        if board_map[self.x][self.y + i] is None:
            moves.add((0, i))
            if (((self.y == 1 and self.colour == "black") or (self.y == 6 and self.colour == "white"))
                    and board_map[self.x][self.y + 2 * i] is None):
                moves.add((0, 2 * i))
        if board_map[self.x + 1][self.y + i] is not None:
            if board_map[self.x + 1][self.y + i].colour != self.colour:
                moves.add((1, i))
        if board_map[self.x - 1][self.y + i] is not None:
            if board_map[self.x - 1][self.y + i].colour != self.colour:
                moves.add((-1, i))
        return self.get_actual_positions(moves)

    def get_offset_moves(self, board_map: dict, offsets: set[tuple[int, int]]) -> set[tuple[int, int]]:
        moves = set()
        for move in offsets:
            target_x = self.x + move[0]
            target_y = self.y + move[1]
            if 0 <= target_x < 8 and 0 <= target_y < 8:
                p = board_map[target_x][target_y]
                if p is None or p.colour != self.colour:
                    moves.add((target_x, target_y))
        return moves

    def get_linear_moves(self, board_map: dict, directions: set[tuple[int, int]]) -> set[tuple[int, int]]:
        moves = set()
        for d in directions:
            for i in range(1, 8):
                pos = (self.x + d[0] * i, self.y + d[1] * i)
                try:
                    p = board_map[pos[0]][pos[1]]
                except IndexError:
                    break
                if p is None:
                    moves.add((d[0] * i, d[1] * i))
                else:
                    if p.colour != self.colour:
                        moves.add((d[0] * i, d[1] * i))
                    break
        return self.get_actual_positions(moves)

    def get_actual_positions(self, moves: set[tuple[int, int]]) -> set[tuple[int, int]]:
        actual_moves = set()
        for move in moves:
            actual_moves.add((self.x + move[0], self.y + move[1]))
        return actual_moves

    def __str__(self) -> str:
        return f"{self.colour} {self.name} at ({self.x}, {self.y})"