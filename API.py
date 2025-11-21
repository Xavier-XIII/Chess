import random
import time

import chess
import chess.engine


def random_turn(board_map: list[list], board_list: list, currently_playing: str, limit: float) -> tuple[tuple[int, int], tuple[int, int]]:
    piece = None
    move = None
    while move is None:
        piece = random.choice(board_list)
        if piece.colour != currently_playing: continue
        moves = list(piece.get_possible_moves(board_map))
        if len(moves) != 0:
            move = random.choice(moves)

    time.sleep(limit)
    return (piece.x, piece.y), move


def chess_gpt_turn(board_map: list[list], board_list: list, currently_playing: str, limit: float) -> tuple[tuple[int, int], tuple[int, int]]:
    piece = None
    move = None
    while move is None:
        piece = random.choice(board_list)
        if piece.colour != currently_playing: continue
        moves = list(piece.get_possible_moves(board_map))
        if len(moves) != 0:
            move = random.choice(moves)

    time.sleep(limit)
    return (piece.x, piece.y), move


def stockfish_turn(board_list: list, currently_playing: str, limit: float) -> tuple[tuple[int, int], tuple[int, int]]:
    board = chess.Board()

    board.turn = chess.WHITE if currently_playing == "white" else chess.BLACK

    piece_to_square = {
        (piece.x, piece.y): chess.square(piece.x, 7 - piece.y)
        for piece in board_list
    }

    for piece in board_list:
        square = piece_to_square[(piece.x, piece.y)]
        if piece.colour == "white":
            if isinstance(piece, chess.Piece):
                board.set_piece_at(square, chess.Piece(piece_type=piece.piece_type, color=chess.WHITE))
        else:
            if isinstance(piece, chess.Piece):
                board.set_piece_at(square, chess.Piece(piece_type=piece.piece_type, color=chess.BLACK))

    engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish.exe")
    result = engine.play(board, chess.engine.Limit(time=limit))
    engine.quit()

    print(result)
    from_square = result.move.from_square
    to_square = result.move.to_square
    print(from_square, to_square)

    xFrom = chess.square_file(from_square)
    yFrom = 7 - chess.square_rank(from_square)
    xTo = chess.square_file(to_square)
    yTo = 7 - chess.square_rank(to_square)

    return (xFrom, yFrom), (xTo, yTo)
