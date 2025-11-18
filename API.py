import random


def compute_turn(board_map: dict, board_list: list, currently_playing: str) -> tuple[tuple[int, int], tuple[int, int]]:
    piece = None
    move = None
    while move is None:
        piece = random.choice(board_list)
        if piece.colour != currently_playing: continue
        moves = list(piece.get_possible_moves(board_map))
        if len(moves) != 0:
            move = random.choice(moves)

    return (piece.x, piece.y), move
