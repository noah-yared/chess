import chess_main


def reformat_board(chess_board):
    """
    Parameter(s): Takes list of lists of characters denoting each piece
    Returns: Dictionary of pieces that matches chess.py representation
    """

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

    return {
        (row, col): mapping[chess_board[row][col]]
        for row in range(8)
        for col in range(8)
        if chess_board[row][col] != "."
    }


def test_in_board():
    """
    Testing in_board() function
    """
    locations = [(1, 9), (8, 8), (3, 3), (4, 3), (5, 6), (6, 8)]
    expected_results = [False, False, True, True, True, False]

    for location, expected in zip(locations, expected_results):
        assert chess_main.in_board(location) is expected


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
        assert chess_main.get_direction_of_line(king, attack) == expected


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
        assert chess_main.get_line_of_attack(king, attack) == expected


def test_is_same_color():
    """
    Testing is_same_color() function
    """
    chess_board = [
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
            chess_main.is_same_color(reformat_board(chess_board), square1, square2)
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
        assert chess_main.has_straight_path(square1, square2) is expected


def test_possible_step_queen():
    """
    Testing possible_step() function for queen
    """
    chess_board = [
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
            chess_main.possible_step(reformat_board(chess_board), (queen, square))
            is expected
        )


def test_possible_step_bishop():
    """
    Testing possible_step() function for bishop
    """
    chess_board = [
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
            chess_main.possible_step(reformat_board(chess_board), (bishop, square))
            is expected
        )


def test_possible_step_rook():
    """
    Testing possible_step() function for rook
    """
    chess_board = [
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
            chess_main.possible_step(reformat_board(chess_board), (rook, square)) is expected
        )


def test_in_check_01():
    # Check that in_check function correctly returns False for white king
    # in the default state of a chess board

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    assert chess_main.in_check(reformat_board(chess_board), (7, 4)) == False


def test_in_check_02():
    # Check that the in_check function returns False for
    # black king for default state of chess board

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    assert chess_main.in_check(reformat_board(chess_board), (0, 3)) is False


def test_in_check_03():
    # Check that the in_check function returns false for a case where King is
    # not in direct line of attack of bishop

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", ".", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "p", ".", "B", "."],
        [".", ".", ".", "P", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", "P", "P", "P", "P"],
        ["R", "N", ".", "Q", "K", "B", "N", "R"],
    ]

    assert chess_main.in_check(reformat_board(chess_board), (7, 4)) is False


def test_in_check_04():
    # Check that the in_check function returns True for a case where black king is
    # in direct line of attack of bishop

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", ".", ".", "p", "p", "p"],
        [".", ".", ".", "p", ".", ".", ".", "."],
        [".", "B", ".", ".", "p", ".", ".", "."],
        [".", ".", ".", ".", "P", ".", ".", "."],
        [".", ".", ".", ".", ".", "N", ".", "."],
        ["P", "P", "P", "P", ".", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", ".", ".", "R"],
    ]
    assert chess_main.in_check(reformat_board(chess_board), (0, 4)) is True


def test_in_check_05():
    # Check that the in_check function returns False for a case where black king is
    # protected from bishop in direct line of attack.

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", ".", ".", "p", "p", "p", "p"],
        [".", ".", "p", ".", ".", ".", ".", "."],
        [".", "B", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", "P", "p", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", ".", "P", ".", "P"],
        ["R", "N", ".", "Q", "K", ".", "N", "R"],
    ]

    assert chess_main.in_check(reformat_board(chess_board), (0, 4)) is False


def test_in_check_06():

    chess_board = [
        ["r", "n", "b", "q", "k", ".", "n", "r"],
        ["p", "p", ".", ".", ".", "B", "p", "p"],
        [".", ".", ".", "p", ".", "n", ".", "."],
        [".", ".", ".", "N", "p", ".", ".", "."],
        [".", ".", "b", ".", "P", ".", ".", "."],
        ["P", ".", ".", ".", ".", ".", ".", "."],
        [".", "P", "P", ".", ".", "P", "P", "P"],
        ["R", ".", ".", ".", "K", ".", ".", "R"],
    ]

    assert chess_main.in_check(reformat_board(chess_board), (0, 4)) is True


def test_in_check_07():

    chess_board = [
        [".", "k", ".", ".", "R", ".", ".", "."],
        ["p", "p", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "K", ".", ".", "."],
    ]

    assert chess_main.in_check(reformat_board(chess_board), (0, 1)) is True


def test_checkmate_default_board():
    """
    Check that checkmate() returns False for the default state of the board
    """

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "q", "k", "B", "N", "R"],
    ]
    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 4)):
        assert chess_main.checkmate(board, (7, 4)) is False


def test_checkmate_bishop_check():
    """
    Check that checkmate function returns False for the case where a
    white bishop is attacking the black king and Black's bishop, pawn,
    and queen can move to block it.
    """

    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", ".", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", "B", ".", "p", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "P", ".", ".", "."],
        ["P", "P", "P", "P", ".", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", ".", "N", "R"],
    ]
    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 4)):
        assert chess_main.checkmate(board, (0, 4)) is False


def test_checkmate_backrank_mate():
    """
          Check that checkmate function returns True for backrank
    as king is trapped in backrank.
    """
    chess_board = [
        [".", "k", ".", "R", ".", ".", ".", "."],
        ["p", "p", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "K", ".", ".", "."],
    ]
    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 1)):
        assert chess_main.checkmate(board, (0, 1)) is True


def test_checkmate_smothered_mate():
    """
    Check that checkmate function returns True for
    smothered mate case, where king is smothered by
    his pieces
    """
    chess_board = [
        ["k", "r", ".", ".", ".", ".", ".", "."],
        ["p", "p", "N", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "K", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 0)):
        assert chess_main.checkmate(board, (0, 0)) is True


def test_checkmate_protected_queen_01():
    """
    Check that checkmate() returns True when white Queen
    is protected by white Bishop and is attacking black King.
    """
    chess_board = [
        [".", "k", "r", ".", ".", ".", ".", "."],
        ["p", "Q", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "B", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", "R", "K", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 1)):
        assert chess_main.checkmate(board, (0, 1)) is True


def test_checkmate_anastasias_mate():
    """
    Check that checkmate() returns True for anastasias checkmate pattern.
    """
    chess_board = [
        ["r", ".", ".", ".", "k", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", "p", ".", ".", ".", "."],
        ["K", "P", "b", ".", ".", ".", ".", "."],
        [".", "R", "R", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (6, 0)):
        assert chess_main.checkmate(board, (6, 0))


def test_checkmate_legals_mate():
    chess_board = [
        ["r", "n", "b", ".", "q", ".", "n", "r"],
        ["p", "p", "B", "k", ".", ".", "p", "p"],
        [".", ".", ".", ".", "p", "n", ".", "."],
        [".", "b", ".", "N", "N", ".", ".", "."],
        [".", ".", ".", "P", ".", ".", ".", "."],
        ["P", ".", ".", ".", ".", ".", ".", "."],
        [".", "P", "P", ".", "P", "P", "P", "P"],
        ["R", ".", ".", ".", "K", "B", ".", "R"],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (1, 3)):
        assert chess_main.checkmate(board, (1, 3)) is True


def test_checkmate_corner_mate():
    """
    Check that checkmate() returns True for queen and king corner checkmate pattern.
    """
    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "k"],
        [".", ".", ".", ".", ".", ".", "q", "."],
        ["R", ".", ".", ".", ".", ".", "K", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 6)):
        assert chess_main.checkmate(board, (7, 6)) is True


def test_checkmate_opera_mate():
    """
    Check that checkmate() returns True for opera mate checkmate pattern.
    """
    chess_board = [
        [".", "k", ".", ".", ".", ".", ".", "."],
        ["p", "p", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "b", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "P", ".", ".", "P", ".", "."],
        [".", ".", ".", "r", "K", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 4)):
        assert chess_main.checkmate(board, (7, 4)) is True


def test_checkmate_blackburnes_mate():
    """
    Check that checkmate() returns True for Blackburne's checkmate pattern.
    """
    chess_board = [
        [".", ".", "k", ".", ".", ".", ".", "."],
        [".", "b", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "n", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "b"],
        [".", "R", ".", ".", ".", "R", "K", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 6)):
        assert chess_main.checkmate(board, (7, 6)) is True


def test_checkmate_hook_mate():
    """
    Check that checkmate() returns True for hook mate checkmate pattern.
    """
    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["k", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "p", ".", "B", ".", ".", "."],
        [".", "n", ".", ".", ".", ".", ".", "."],
        [".", "P", "K", ".", ".", ".", ".", "."],
        [".", ".", "r", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (6, 2)):
        assert chess_main.checkmate(board, (6, 2)) is True


def test_checkmate_hook_mate():
    """
    Check that checkmate() returns True for hook mate checkmate pattern.
    """
    chess_board = [
        [".", ".", "r", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "Q", ".", ".", ".", ".", "."],
        ["k", ".", ".", ".", ".", ".", ".", "."],
        ["R", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", "P", "K", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (3, 0)):
        assert chess_main.checkmate(board, (3, 0)) is True


def test_checkmate_fools_mate():
    """
    Check that checkmate() returns True for the fools mate checkmate pattern
    """
    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", ".", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "p", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "P", "q"],
        [".", ".", ".", ".", ".", "P", ".", "."],
        ["P", "P", "P", "P", "P", ".", ".", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 4)):
        assert chess_main.checkmate(board, (7, 4)) is True


def test_miscellaneous_checkmate_01():
    chess_board = [
        [".", "k", ".", "r", ".", "q", ".", "."],
        ["p", "p", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["r", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "n", "B", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "P", ".", "P", ".", ".", "."],
        [".", ".", "R", "K", ".", ".", "r", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 3)):
        assert chess_main.checkmate(board, (7, 3)) is True


def test_miscellaneous_checkmate_02():

    chess_board = [
        ["k", ".", ".", ".", "R", ".", ".", "."],
        ["p", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "b", ".", ".", ".", ".", "."],
        ["N", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", ".", ".", ".", "."],
        [".", "K", "R", ".", ".", ".", ".", "B"],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 0)):
        assert chess_main.checkmate(board, (0, 0)) is True


def test_no_checkmate_01():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["k", ".", ".", ".", ".", ".", ".", "."],
        ["b", ".", ".", ".", ".", ".", ".", "."],
        [".", "q", ".", ".", ".", "n", ".", "."],
        [".", "P", "K", ".", ".", ".", ".", "."],
        [".", ".", "r", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (6, 2)):
        assert chess_main.checkmate(board, (6, 2)) is False


def test_no_checkmate_02():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["k", "Q", ".", ".", ".", ".", ".", "."],
        ["R", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "B", ".", ".", "."],
        [".", "P", "K", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (3, 0)):
        assert chess_main.checkmate(board, (3, 0)) is False


def test_no_checkmate_03():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "n", ".", ".", ".", "q", "."],
        ["k", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", "K", ".", ".", ".", "B"],
        [".", ".", "r", ".", "r", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (6, 3)):
        assert chess_main.checkmate(board, (6, 3)) is False


def test_no_checkmate_04():
    chess_board = [
        [".", ".", "r", "k", ".", ".", "R", "."],
        [".", ".", "p", "p", "p", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "b"],
        ["R", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", ".", ".", ".", "."],
        [".", "K", "R", ".", ".", "Q", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 3)):
        assert chess_main.checkmate(board, (0, 3)) is False


def test_no_checkmate_05():

    chess_board = [
        [".", "k", ".", "r", ".", ".", ".", "."],
        ["p", "p", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["r", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "b", "."],
        [".", ".", "P", ".", "P", ".", ".", "."],
        [".", ".", "R", "K", ".", ".", "Q", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 3)):
        assert chess_main.checkmate(board, (7, 3)) is False


def test_no_checkmate_06():

    chess_board = [
        [".", ".", "r", "k", ".", ".", "q", "."],
        [".", ".", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "p", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["B", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", ".", ".", ".", "."],
        [".", "K", ".", "R", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 3)):
        assert chess_main.checkmate(board, (0, 3)) is False


def test_no_checkmate_07():

    chess_board = [
        [".", "k", "r", ".", ".", ".", ".", "."],
        ["p", "p", "p", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "q", "P", ".", ".", ".", ".", "."],
        [".", "K", ".", "R", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 1)):
        assert chess_main.checkmate(board, (7, 1)) is False


def test_no_checkmate_08():

    chess_board = [
        [".", ".", ".", ".", ".", ".", "k", "."],
        ["p", "B", "p", ".", ".", "p", "p", "p"],
        [".", "p", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["n", ".", ".", ".", ".", ".", ".", "."],
        [".", "P", "P", ".", ".", ".", ".", "."],
        ["P", "R", ".", ".", ".", "r", ".", "."],
        [".", ".", "K", ".", ".", ".", ".", "r"],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 2)):
        assert chess_main.checkmate(board, (7, 2)) is False


def test_no_checkmate_09():

    chess_board = [
        [".", "k", "r", ".", ".", ".", ".", "b"],
        ["p", "p", "p", ".", ".", ".", ".", "b"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["N", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", ".", ".", ".", ".", ".", ".", "."],
        ["K", ".", "R", ".", "r", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (7, 0)):
        assert chess_main.checkmate(board, (7, 0)) is False


def test_no_checkmate_10():

    chess_board = [
        [".", "k", ".", "r", ".", ".", ".", "."],
        ["p", ".", ".", ".", ".", ".", ".", "."],
        ["B", "Q", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", ".", ".", ".", ".", "."],
        [".", "K", "R", ".", ".", ".", ".", "B"],
    ]

    board = reformat_board(chess_board)
    if chess_main.in_check(board, (0, 1)):
        assert chess_main.checkmate(board, (0, 1)) is False


def test_stalemate_01():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "k"],
        [".", ".", ".", "K", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "Q", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 7)) is True


def test_stalemate_02():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "k"],
        [".", ".", ".", ".", ".", ".", ".", "P"],
        [".", ".", ".", ".", ".", ".", ".", "K"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 7)) is True


def test_stalemate_03():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "k"],
        ["p", ".", ".", ".", ".", ".", ".", "."],
        ["P", ".", "p", ".", ".", ".", ".", "K"],
        [".", ".", "P", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", "B", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 7)) is True


def test_stalemate_04():

    chess_board = [
        [".", "k", ".", ".", ".", ".", ".", "."],
        ["b", ".", ".", ".", ".", ".", ".", "."],
        [".", "p", ".", ".", ".", ".", ".", "."],
        [".", "P", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "B", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "R", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 1)) is True


def test_no_stalemate_01():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "k"],
        [".", "p", ".", "K", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "Q", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 7)) is False


def test_no_stalemate_02():

    chess_board = [
        [".", ".", ".", ".", ".", ".", ".", "k"],
        [".", "p", ".", ".", ".", ".", ".", "P"],
        ["P", "P", ".", ".", ".", ".", ".", "K"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 7)) is False


def test_no_stalemate_03():

    chess_board = [
        [".", "k", ".", ".", ".", ".", ".", "."],
        ["b", ".", ".", ".", ".", ".", ".", "."],
        [".", "p", ".", ".", ".", ".", ".", "."],
        ["P", "P", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "B", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "R", ".", "K", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 1)) is False


def test_no_stalemate_04():

    chess_board = [
        [".", "k", ".", ".", ".", ".", ".", "."],
        ["b", "B", ".", ".", ".", ".", ".", "."],
        [".", "p", ".", ".", ".", ".", ".", "."],
        [".", "P", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", "R", ".", ".", ".", ".", "."],
    ]

    board = reformat_board(chess_board)
    assert chess_main.stalemate(board, (0, 1)) is False


if __name__ == "__main__":
    pass
