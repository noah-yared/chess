from flask import Flask, jsonify, request
from flask_cors import CORS
import chess_main


app = Flask(__name__)
CORS(app)


@app.route("/validate-move", methods=["POST"])
def check_move():
    # EXAMPLE JSON DATA:
    # {
    # 	"board" : "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqKQ -", # FEN notation
    # 	"move" : [[6, 4], [4,4]]  # Move pawn to e5
    # }
    data = request.get_json()
    print(data)
    assert data is not None, "Data is not in json format"
    move = tuple(data["move"][0]), tuple(data["move"][1])
    game = chess_main.game(parse_FEN(data["board"]))
    is_valid_move = game.make_move(move)
    # update board FEN
    response = {
        "fen": game.fen,
        "valid": is_valid_move,
        "gameover": game.game_over,
        "check": game.check,
        "castled": game.castled,
        "enpassant": game.enpassant,
        "promotion": game.promotion
    }
    print(response)
    return jsonify(response)


mapping = {
    "P": chess_main.Pawn("white"),
    "p": chess_main.Pawn("black"),
    "R": chess_main.Rook("white"),
    "r": chess_main.Rook("black"),
    "B": chess_main.Bishop("white"),
    "b": chess_main.Bishop("black"),
    "N": chess_main.Knight("white"),
    "n": chess_main.Knight("black"),
    "Q": chess_main.Queen("white"),
    "q": chess_main.Queen("black"),
    "K": chess_main.King("white"),
    "k": chess_main.King("black"),
}


def parse_FEN(board_fen: str) -> tuple:
    tokens = board_fen.split()
    return (
        tokens[0],
        parse_pieces(tokens[0]),
        tokens[1],
        parse_castling_privileges(tokens[2]),
        parse_enpassant_squares(tokens[3]),
    )


def parse_pieces(piece_placement: str) -> tuple:
    pieces = {}
    for row_index, row in enumerate(piece_placement.split("/")):
        col_index = 0
        for ch in row:
            try:
                col_index += int(ch)
            except ValueError:
                if ch == "K":
                    white_king = row_index, col_index
                elif ch == "k":
                    black_king = row_index, col_index
                pieces[(row_index, col_index)] = mapping[ch]
                col_index += 1
    return pieces, white_king, black_king


def parse_enpassant_squares(squares: str) -> set:
    if squares == "-":
        return set()
    return {
        parse_algebraic_notation(squares[i : i + 2]) for i in range(0, len(squares), 2)
    }


def parse_algebraic_notation(square: str) -> tuple:
    return 8 - int(square[1]), ord(square[0]) - ord('a')


def parse_castling_privileges(privileges: str) -> set:
    if privileges == "-":
        return set()
    return set(privileges)
