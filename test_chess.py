import chess


def reformat_board(chessboard):
    """
    Parameter(s): Takes list of lists of characters denoting each piece
    Returns: Dictionary of pieces that matches chess.py representation
    """

    mapping = {
        "P": chess.Pawn("white"),
        "p": chess.Pawn("black"),
        "R": chess.Rook("white"),
        "r": chess.Rook("black"),
        "B": chess.Bishop("white"),
        "b": chess.Bishop("black"),
        "N": chess.Knight("white"),
        "n": chess.Knight("black"),
        "Q": chess.Queen("white"),
        "q": chess.Queen("black"),
        "K": chess.King("white"),
        "k": chess.King("black"),
    }

    return {
        (row, col): mapping[chessboard[row][col]]
        for row in range(8)
        for col in range(8)
        if chessboard[row][col] != "."
    }


def test_in_board():
    """
    Testing in_board() function
    """
    locations = [(1, 9), (8, 8), (3, 3), (4, 3), (5, 6), (6, 8)]
    expected_results = [False, False, True, True, True, False]

    for location, expected in zip(locations, expected_results):
        assert chess.in_board(location) is expected


def test_get_direction_of_line():
    """
    Testing get_direction_of_line() function
    """
    king_locations = [(1, 3), (3, 4), (7, 4), (5, 6), (1, 1), (7, 7)]
    attacker_locations = [(4, 0), (1, 2), (3, 4), (6, 7), (7, 7), (7, 1)]
    expected_results = [(1, -1), (-1, -1), (-1, 0), (1, 1), (1, 1), (0, -1)]

    for king, attack, expected in zip(
        king_locations, attacker_locations, expected_results
    ):
        assert chess.get_direction_of_line(king, attack) == expected


def test_get_line_of_attack():
    """
    Testing get_line_of_attack() function
    """
    king_locations = [(1, 3), (3, 4), (7, 4), (5, 6), (1, 1), (7, 7)]
    attacker_locations = [(4, 0), (1, 2), (3, 4), (6, 7), (7, 7), (7, 1)]
    expected_results = [
        [(2, 2), (3, 1), (4, 0)],
        [(2, 3), (1, 2)],
        [(6, 4), (5, 4), (4, 4), (3, 4)],
        [(6, 7)],
        [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
        [(7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1)],
    ]

    for king, attack, expected in zip(
        king_locations, attacker_locations, expected_results
    ):
        assert chess.get_line_of_attack(king, attack) == expected


def test_is_same_color():
    """
    Testing is_same_color() function
    """
    chessboard = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]
    squares1 = [(0, 4), (5, 6), (1, 7), (6, 6), (7, 1), (1, 1), (0, 1)]
    squares2 = [(1, 7), (6, 5), (7, 7), (1, 6), (7, 2), (1, 1), (1, 3)]
    expected_results = [True, False, False, False, True, True, True]

    for square1, square2, expected in zip(squares1, squares2, expected_results):
        assert (
            chess.is_same_color(reformat_board(chessboard), square1, square2)
            is expected
        )


def test_has_straight_path():
    """
    Testing has_straight_path() function
    """
    squares1 = [
        (3, 2),
        (0, 7),
        (6, 3),
        (5, 4),
        (2, 1),
        (4, 5),
        (6, 3),
        (1, 6),
        (3, 7),
        (2, 0),
    ]
    squares2 = [
        (7, 3),
        (4, 0),
        (6, 6),
        (3, 1),
        (0, 4),
        (5, 2),
        (2, 7),
        (1, 5),
        (5, 5),
        (5, 3),
    ]
    expected_results = [False, False, True, False, False, False, True, True, True, True]

    for square1, square2, expected in zip(squares1, squares2, expected_results):
        assert chess.has_straight_path(square1, square2) is expected


def test_possible_step_queen():
    """
    Testing possible_step() function for queen
    """
    chessboard = [
        ["N", ".", ".", ".", ".", ".", "k", "."],
        [".", ".", ".", "P", ".", ".", ".", "."],
        [".", ".", ".", "B", ".", ".", ".", "."],
        [".", ".", ".", ".", "q", ".", ".", "."],
        [".", ".", ".", ".", "p", "r", ".", "b"],
        [".", "p", ".", ".", "p", ".", ".", "."],
        [".", ".", "P", "P", ".", ".", ".", "Q"],
        [".", ".", "K", ".", ".", ".", ".", "."],
    ]
    queen = (6, 7)
    squares = [
        (7, 2),
        (0, 2),
        (6, 6),
        (1, 2),
        (4, 2),
        (0, 3),
        (6, 2),
        (4, 0),
        (3, 3),
        (7, 0),
    ]
    expected_results = [
        False,
        False,
        True,
        True,
        False,
        False,
        True,
        False,
        False,
        False,
    ]

    for square, expected in zip(squares, expected_results):
        assert (
            chess.possible_step(reformat_board(chessboard), (queen, square)) is expected
        )


def test_possible_step_bishop():
    """
    Testing possible_step() function for bishop
    """
    chessboard = [
        ["N", ".", ".", ".", ".", ".", "k", "."],
        [".", ".", ".", "P", ".", ".", ".", "."],
        [".", ".", ".", "B", ".", ".", ".", "."],
        [".", ".", ".", ".", "q", ".", ".", "."],
        [".", ".", ".", ".", "p", "r", ".", "b"],
        [".", "p", ".", ".", "p", ".", ".", "."],
        [".", ".", "P", "P", ".", ".", ".", "Q"],
        [".", ".", "K", ".", ".", ".", ".", "."],
    ]
    bishop = (4, 7)
    squares = [
        (5, 6),
        (1, 2),
        (3, 4),
        (2, 0),
        (7, 1),
        (2, 5),
        (7, 5),
        (1, 4),
        (5, 5),
        (2, 1),
    ]
    expected_results = [
        True,
        False,
        False,
        False,
        False,
        True,
        False,
        True,
        False,
        False,
    ]

    for square, expected in zip(squares, expected_results):
        assert (
            chess.possible_step(reformat_board(chessboard), (bishop, square))
            is expected
        )


def test_possible_step_rook():
    """
    Testing possible_step() function for rook
    """
    chessboard = [
        ["N", ".", ".", ".", ".", ".", "k", "."],
        [".", ".", ".", "P", ".", ".", ".", "."],
        [".", ".", ".", "B", ".", ".", ".", "."],
        [".", ".", ".", ".", "q", ".", ".", "."],
        [".", ".", ".", ".", ".", "r", ".", "."],
        [".", "p", ".", ".", "p", ".", ".", "."],
        [".", ".", "P", "P", ".", ".", ".", "Q"],
        [".", ".", "K", ".", ".", ".", ".", "."],
    ]
    rook = (4, 5)
    squares = [
        (2, 4),
        (5, 0),
        (2, 5),
        (2, 3),
        (3, 1),
        (1, 6),
        (0, 1),
        (3, 1),
        (7, 3),
        (4, 2),
    ]
    expected_results = [
        False,
        False,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
    ]

    for square, expected in zip(squares, expected_results):
        assert (
            chess.possible_step(reformat_board(chessboard), (rook, square)) is expected
        )


def test_in_check_01():
    # Check that in_check function correctly returns False for white king
    # in the default state of a chess board

    ChessBoard = [
        ["r", "n", "b", "k", "q", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "K", "Q", "B", "N", "R"],
    ]

    assert chess.in_check(reformat_board(ChessBoard), (7, 3)) == False


def test_in_check_02():
    # Check that the in_check function returns False for
    # black king for default state of chess board

    ChessBoard = [
        ["r", "n", "b", "k", "q", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "K", "Q", "B", "N", "R"],
    ]

    assert chess.in_check(reformat_board(ChessBoard), (0, 3)) is False


def test_in_check_03():
    # Check that the in_check function returns false for a case where King is
    # not in direct line of attack of bishop

    ChessBoard = [
        ["R", "N", "B", "K", "Q", ".", "N", "R"],
        ["P", "P", "P", "P", "P", ".", ".", "P"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "B", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["p", "p", "p", "p", ".", "p", "p", "p"],
        ["r", "n", "b", "k", "q", "b", "n", "r"],
    ]

    assert chess.in_check(reformat_board(ChessBoard), (7, 3)) is False


def test_in_check_04():
    # Check that the in_check function returns True for a case where black king is
    # in direct line of attack of bishop

    ChessBoard = [
        ["r", "n", "b", "k", "q", "b", "n", "r"],
        ["p", "p", "p", "p", ".", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "B", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", "P", "P", ".", "P"],
        ["R", "N", ".", "K", "Q", "B", "N", "R"],
    ]
    assert chess.in_check(reformat_board(ChessBoard), (0, 3)) is True


def test_in_check_05():
    # Check that the in_check function returns False for a case where black king is
    # protected from bishop in direct line of attack.

    ChessBoard = [
        ["r", "n", "b", "k", "q", "b", "n", "r"],
        ["p", "p", "p", "p", ".", ".", "p", "p"],
        [".", ".", ".", ".", ".", "p", ".", "."],
        [".", ".", ".", ".", ".", ".", "B", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", "P", "P", ".", "P"],
        ["R", "N", ".", "K", "Q", "B", "N", "R"],
    ]

    assert chess.in_check(reformat_board(ChessBoard), (0, 3)) is False


def test_in_check_06():

    ChessBoard = [
        ["r", "n", "b", "k", "q", ".", "n", "r"],
        ["p", "p", "B", ".", ".", ".", "p", "p"],
        [".", ".", ".", ".", "p", "n", ".", "."],
        [".", ".", ".", "N", "N", ".", ".", "."],
        [".", ".", ".", "P", ".", ".", ".", "."],
        ["P", ".", ".", ".", ".", ".", ".", "."],
        [".", "P", "P", ".", "P", "P", "P", "P"],
        ["R", ".", ".", "K", "b", "B", ".", "R"],
    ]

    assert chess.in_check(reformat_board(ChessBoard), (0, 3)) is True


def test_in_check_07():

    ChessBoard = [
        [".", "k", ".", ".", "R", ".", ".", "."],
        ["p", "p", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "K", ".", ".", "."],
    ]

    assert chess.in_check(reformat_board(ChessBoard), (0, 1)) is True


def test_checkmate_default_board():
    """
    Check that checkmate() returns False for the default state of the board
    """

    ChessBoard = [
        ["r", "n", "b", "k", "q", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "K", "Q", "B", "N", "R"],
    ]
    board = reformat_board(ChessBoard)
    if chess.in_check(board, (7, 3)):
        assert chess.checkmate(board, (7, 3)) is False


# def test_checkmate_bishop_check():
#     """
#     Check that checkmate function returns False for the case where a
#     white bishop is attacking the black king Black's bishop, pawn,
#     and queen can move to block it.
#     """

#     ChessBoard = [
#         ["r", "n", "b", "k", "q", "b", "n", "r"],
#         ["p", "p", "p", "p", ".", "p", "p", "p"],
#         [".", ".", ".", ".", ".", ".", ".", "."],
#         [".", ".", ".", ".", ".", ".", "B", "."],
#         [".", ".", ".", ".", ".", ".", ".", "."],
#         [".", ".", ".", "P", ".", ".", ".", "."],
#         ["P", "P", "P", ".", "P", "P", "P", "P"],
#         ["R", "N", ".", "K", "Q", "B", "N", "R"],
#     ]
#     board = reformat_board(ChessBoard)
#     if chess.in_check(board, (0, 3)):
#         assert chess.checkmate(board, (0, 3)) is False


# def test_checkmate_scholars_mate():
# 	"""
# 	Check that checkmate function returns True for scholar's
# 	mate as king is trapped in backrank.
# 	"""
# 	ChessBoard = \
# 			[
# 				[".", ".", ".", ".", "K", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["p", "p", "p", ".", ".", ".", ".", "."],
# 				[".", "k", ".", ".", "R", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (1,7), (white, black)):
# 		assert new_game.checkmate("black", (1,7), (white, black)) == True


# def test_checkmate_smothered_mate():
# 	"""
# 	Check that checkmate function returns True for
# 	smothered mate case, where king is smothered by
# 	his pieces
# 	"""
# 	ChessBoard = \
# 			[
# 				[".", ".", ".", ".", "K", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["p", "p", "N", ".", ".", ".", ".", "."],
# 				["k", "r", ".", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (1,7), (white, black)):
# 		assert new_game.checkmate("black", (0,7), (white, black)) == True

# def test_checkmate_protected_queen():
# 	"""
# 	Check that checkmate() returns True when white Queen
# 	is protected by white Bishop and is attacking black King.
# 	"""
# 	ChessBoard = \
# 			[
# 				[".", ".", ".", "R", "K", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", "B", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["p", "Q", "p", ".", ".", ".", ".", "."],
# 				[".", "k", "r", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (1,7), (white, black)):
# 		assert new_game.checkmate("black", (1,7), (white, black)) == True

# def test_checkmate_anastasias_mate_01():
# 	"""
# 	Check that checkmate() returns True for anastasias checkmate pattern.
# 	"""
# 	ChessBoard = \
# 				[
# 					[".", ".", ".", "R", "K", ".", ".", "."],
# 					[".", ".", ".", ".", ".", ".", ".", "."],
# 					[".", ".", ".", ".", ".", "B", ".", "."],
# 					[".", ".", ".", ".", ".", ".", ".", "."],
# 					[".", ".", ".", ".", ".", ".", ".", "."],
# 					[".", ".", ".", ".", ".", ".", ".", "."],
# 					["p", "Q", "p", ".", ".", ".", ".", "."],
# 					[".", "k", "r", ".", ".", ".", ".", "."]
# 				]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (1,7), (white, black)):
# 		assert new_game.checkmate("black", (1,7), (white, black)) == True

# def test_checkmate_anastasias_mate_02():
# 	"""
# 	Check that checkmate() returns True for anastasias checkmate pattern.
# 	"""
# 	ChessBoard = \
# 			[
# 				["R", ".", ".", ".", "K", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", "B", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["k", "p", "N", ".", ".", ".", ".", "."],
# 				[".", "r", "r", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (0,6), (white, black)):
# 		assert new_game.checkmate("black", (0,6), (white, black)) == True


# def test_checkmate_legals_mate():
# 	ChessBoard = \
# 				[
# 					["R", ".", ".", "K", "b", "B", ".", "R"],
# 					[".", "P", "P", ".", "P", "P", "P", "P"],
# 					["P", ".", ".", ".", ".", ".", ".", "."],
# 					[".", ".", ".", "P", ".", ".", ".", "."],
# 					[".", ".", ".", "N", "N", ".", ".", "."],
# 					[".", ".", ".", ".", "p", "n", ".", "."],
# 					["p", "p", "B", "k", ".", ".", "p", "p"],
# 					["r", "n", "b", ".", "q", ".", "n", "r"]
# 				]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (3,6), (white, black)):
# 		assert new_game.checkmate("black", (3,6), (white, black)) == True


# def test_checkmate_corner_mate():
# 	"""
# 	Check that checkmate() returns True for queen and king corner checkmate pattern.
# 	"""
# 	ChessBoard = \
# 			[
# 				["R", ".", ".", ".", ".", ".", "K", "."],
# 				[".", ".", ".", ".", ".", ".", "q", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "k"],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("white", (6,0), (white, black)):
# 		assert new_game.checkmate("white", (6,0), (white, black)) == True


# def test_checkmate_opera_mate():
# 	"""
# 	Check that checkmate() returns True for opera mate checkmate pattern.
# 	"""
# 	ChessBoard = \
# 			[
# 				[".", ".", ".", "r", "K", ".", ".", "."],
# 				[".", ".", "P", ".", ".", "P", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", "b", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["p", "p", ".", ".", ".", ".", ".", "."],
# 				[".", "k", ".", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("white", (4,0), (white, black)):
# 		assert new_game.checkmate("white", (4,0), (white, black)) == True

# def test_checkmate_blackburnes_mate():
# 	"""
# 	Check that checkmate() returns True for Blackburne's checkmate pattern.
# 	"""
# 	ChessBoard = \
# 			[
# 				["R", ".", ".", ".", ".", "R", "K", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "b"],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", "n", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", "b", ".", ".", ".", ".", ".", "."],
# 				[".", ".", "k", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("white", (6,0), (white, black)):
# 		assert new_game.checkmate("white", (6,0), (white, black)) == True


# def test_checkmate_hook_mate():
# 	"""
# 	Check that checkmate() returns True for hook mate checkmate pattern.
# 	"""
# 	ChessBoard = \
# 			[
# 				[".", ".", "r", ".", ".", ".", ".", "."],
# 				[".", "P", "K", ".", ".", ".", ".", "."],
# 				[".", "n", ".", ".", "B", ".", ".", "."],
# 				[".", ".", "p", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["k", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", "r", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (1,2), (white, black)):
# 		assert new_game.checkmate("black", (1,2), (white, black)) == True


# def test_checkmate_hook_mate():
# 	"""
# 	Check that checkmate() returns True for hook mate checkmate pattern.
# 	"""
# 	ChessBoard = \
# 			[
# 				[".", ".", "r", ".", ".", ".", ".", "."],
# 				[".", "P", "K", ".", ".", ".", ".", "."],
# 				[".", "n", ".", ".", "B", ".", ".", "."],
# 				["R", ".", ".", ".", ".", ".", ".", "."],
# 				["k", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", "Q", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", "r", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("black", (0,4), (white, black)):
# 		assert new_game.checkmate("black", (0,4), (white, black)) == True

# def test_checkmate_fools_mate():
# 	"""
# 	Check that checkmate() returns True for the fools mate checkmate pattern
# 	"""
# 	ChessBoard = \
# 			[
# 				["R", "N", "B", "K", "Q", "B", "N", "R"],
# 				["P", ".", ".", "P", "P", "P", "P", "P"],
# 				[".", ".", "P", ".", ".", ".", ".", "."],
# 				["q", "P", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", "p", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				["p", "p", "p", ".", "p", "p", "p", "p"],
# 				["r", "n", "b", "k", ".", "b", "n", "r"]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	if new_game.in_check("white", (3,0), (white, black)):
# 		assert new_game.checkmate("white", (3,0), (white, black)) == True

# def test_no_checkmate_01():

# 	ChessBoard = \
# 			[
# 				[".", ".", "r", ".", ".", ".", ".", "."],
# 				[".", "P", "K", ".", ".", ".", ".", "."],
# 				[".", "q", ".", ".", ".", ".", ".", "."],
# 				["b", ".", ".", ".", ".", ".", ".", "."],
# 				["k", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("white", (2,1), (white, black))
# 	assert new_game.checkmate("white", (2,1), (white, black)) == False

# def test_no_checkmate_02():

# 	ChessBoard = \
# 			[
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", "P", "K", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", "B", ".", ".", "."],
# 				["R", ".", ".", ".", ".", ".", ".", "."],
# 				["k", "Q", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."],
# 				[".", ".", ".", ".", ".", ".", ".", "."]
# 			]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("black", (0,4), (white, black))
# 	assert new_game.checkmate("black", (0,4), (white, black)) == False

# def test_no_checkmate_03():

# 	ChessBoard = \
# 		[
# 			[".", ".", ".", ".", "r", ".", ".", "."],
# 			[".", ".", ".", "K", ".", ".", ".", "B"],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", "n", ".", ".", ".", ".", ".", "."],
# 			["k", ".", ".", ".", ".", ".", "q", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", "r", ".", ".", ".", ".", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("white", (3,1), (white, black))
# 	assert new_game.checkmate("white", (3,1), (white, black)) == False


# def test_no_checkmate_04():
# 	ChessBoard = \
# 		[
# 			[".", "K", "R", ".", ".", "Q", ".", "."],
# 			["P", "P", "P", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["R", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "b"],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", "p", "p", "p", ".", ".", "."],
# 			[".", ".", "r", "k", ".", ".", "R", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("black", (3,7), (white, black))
# 	assert new_game.checkmate("black", (3,7), (white, black)) == False


# def test_no_checkmate_05():

# 	ChessBoard = \
# 		[
# 			[".", "K", ".", "R", ".", ".", ".", "."],
# 			["P", "P", "P", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["R", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", "B", "."],
# 			[".", ".", "p", ".", "p", ".", ".", "."],
# 			[".", ".", "r", "k", ".", ".", "q", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("black", (3,7), (white, black))
# 	assert new_game.checkmate("black", (3,7), (white, black)) == False

# def test_no_checkmate_06():

# 	ChessBoard = \
# 		[
# 			[".", "K", ".", "R", ".", ".", ".", "."],
# 			["P", "P", "P", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["R", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", "p", ".", ".", "."],
# 			[".", ".", "p", ".", ".", ".", ".", "."],
# 			[".", ".", "r", "k", ".", ".", "q", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("black", (3,7), (white, black))
# 	assert new_game.checkmate("black", (3,7), (white, black)) == False

# def test_no_checkmate_07():

# 	ChessBoard = \
# 		[
# 			[".", "K", ".", "R", ".", ".", ".", "."],
# 			["P", "q", "P", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["p", "p", "p", ".", ".", ".", ".", "."],
# 			[".", "k", "r", ".", ".", ".", ".", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("white", (1,0), (white, black))
# 	assert new_game.checkmate("white", (1,0), (white, black)) == False

# def test_no_checkmate_08():

# 	ChessBoard = \
# 		[
# 			[".", ".", "K", ".", ".", ".", ".", "r"],
# 			["P", "R", ".", ".", ".", "r", ".", "."],
# 			[".", "P", "P", ".", ".", ".", ".", "."],
# 			["n", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", "p", ".", ".", ".", ".", ".", "."],
# 			["p", "B", "p", ".", ".", "p", "p", "p"],
# 			[".", ".", ".", ".", ".", ".", "k", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	assert new_game.in_check("white", (2,0), (white, black)) == True
# 	print(new_game.danger)
# 	assert new_game.checkmate("white", (2,0), (white, black)) == False


# def test_no_checkmate_09():

# 	ChessBoard = \
# 		[
# 			["K", ".", "R", ".", "r", ".", ".", "."],
# 			["P", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["N", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["p", "p", "p", ".", ".", ".", ".", "b"],
# 			[".", "k", "r", ".", ".", ".", ".", "b"]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("white", (0,0), (white, black))
# 	assert new_game.checkmate("white", (0,0), (white, black)) == False

# def test_no_checkmate_10():

# 	ChessBoard = \
# 		[
# 			[".", "K", ".", "R", ".", ".", ".", "."],
# 			["P", ".", ".", ".", ".", ".", ".", "."],
# 			["b", "q", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["p", "p", "p", ".", ".", ".", ".", "."],
# 			[".", "k", "r", ".", ".", ".", ".", "b"]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("white", (1,0), (white, black))
# 	assert new_game.checkmate("white", (1,0), (white, black)) == False

# def test_checkmate_01():
# 	ChessBoard = \
# 		[
# 			[".", "K", ".", "R", ".", "Q", ".", "."],
# 			["P", "P", "P", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["R", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", "N", "b", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", "p", ".", "p", ".", ".", "."],
# 			[".", ".", "r", "k", ".", ".", "R", "."]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("black", (3,7), (white, black))
# 	assert new_game.checkmate("black", (3,7), (white, black)) == True


# def test_checkmate_02():

# 	ChessBoard = \
# 		[
# 			["K", ".", ".", ".", "r", ".", ".", "."],
# 			["P", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", "B", ".", ".", ".", ".", "."],
# 			["n", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			[".", ".", ".", ".", ".", ".", ".", "."],
# 			["p", "p", "p", ".", ".", ".", ".", "."],
# 			[".", "k", "r", ".", ".", ".", ".", "b"]
# 		]

# 	white, black = reformatBoard(ChessBoard)

# 	new_game = chess.game()
# 	new_game.in_check("white", (0,0), (white, black))
# 	assert new_game.checkmate("white", (0,0), (white, black)) == True


if __name__ == "__main__":
    pass
