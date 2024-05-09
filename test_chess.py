import pytest 
import chess


def reformatBoard(chessboard):
  """
  Parameter(s): Takes list of lists of characters denoting each piece
  Returns: Dictionary of pieces that matches chess.py representation
  """

  mapping = {
		"P": chess.Pawn("white"), "p":chess.Pawn("black"),
		"R": chess.Rook("white"), "r":chess.Rook("black"),
		"B": chess.Bishop("white"), "b":chess.Bishop("black"),
		"N": chess.Knight("white"), "n":chess.Knight("black"),
		"Q": chess.Queen("white"), "q":chess.Queen("black"),
		"K": chess.King("white"), "k":chess.King("black")
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
	locations = [(1,9),(8,8),(3,3),(4,3),(5,6),(6,8)] 
	expected_results  = [False, False, True, True, True, False]
	
	for	location, expected in zip(locations, expected_results):
		assert chess.in_board(location) is expected
    

def test_get_direction_of_line():
	"""
	Testing get_direction_of_line() function
	"""
	king_locations = [(1,3), (3,4), (7,4), (5,6), (1,1), (7,7)]
	attacker_locations = [(4,0), (1,2), (3,4), (6,7), (7,7), (7,1)]
	expected_results = [(1,-1), (-1,-1), (-1,0), (1,1), (1,1), (0,-1)]

	for king, attack, expected in zip(king_locations, attacker_locations, expected_results):
		assert chess.get_direction_of_line(king, attack) == expected
	


def test_get_line_of_attack():
	"""
	Testing get_line_of_attack() function
	"""
	king_locations = [(1,3), (3,4), (7,4), (5,6), (1,1), (7,7)]
	attacker_locations = [(4,0), (1,2), (3,4), (6,7), (7,7), (7,1)]
	expected_results = [
			[(2,2),(3,1),(4,0)],
			[(2,3),(1,2)],
			[(6,4),(5,4),(4,4),(3,4)],
			[(6,7)],
			[(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)],
			[(7,6),(7,5),(7,4),(7,3),(7,2),(7,1)]
	]

	for king, attack, expected in zip(king_locations, attacker_locations, expected_results):
		assert chess.get_line_of_attack(king, attack) == expected


def test_is_same_color():
	"""
	Testing is_same_color() function
	"""
	chessboard = \
	[
		["r", "n", "b", "q", "k", "b", "n", "r"],
		["p", "p", "p", "p", "p", "p", "p", "p"],
		[".", ".", ".", ".", ".", ".", ".", "."],
		[".", ".", ".", ".", ".", ".", ".", "."],
		[".", ".", ".", ".", ".", ".", ".", "."],
		[".", ".", ".", ".", ".", ".", ".", "."],
		["P", "P", "P", "P", "P", "P", "P", "P"],
		["R", "N", "B", "Q", "K", "B", "N", "R"]
	]
	squares1 = [(0,4), (5,6), (1,7), (6,6), (7,1), (1,1), (0,1)]
	squares2 = [(1,7), (6,5), (7,7), (1,6), (7,2), (1,1), (1,3)]
	expected_results = [True, False, False, False, True, True, True]

	for square1, square2, expected in zip(squares1, squares2, expected_results):
		assert chess.is_same_color(reformatBoard(chessboard), square1, square2) is expected


def test_has_straight_path():
	"""
	Testing has_straight_path() function 
	"""
	squares1 = [(3, 2), (0, 7), (6, 3), (5, 4), (2, 1), (4, 5), (6, 3), (1, 6), (3, 7), (2, 0)]
	squares2 = [(7, 3), (4, 0), (6, 6), (3, 1), (0, 4), (5, 2), (2, 7), (1, 5), (5, 5), (5, 3)]
	expected_results = [False, False, True, False, False, False, True, True, True, True]

	for square1, square2, expected in zip(squares1, squares2, expected_results):
		assert chess.has_straight_path(square1, square2) is expected


def test_possible_step_queen():
	"""
	Testing possible_step() function for queen
	"""
	chessboard = [
		['N', '.', '.', '.', '.', '.', 'k', '.'],
		['.', '.', '.', 'P', '.', '.', '.', '.'],
		['.', '.', '.', 'B', '.', '.', '.', '.'],
		['.', '.', '.', '.', 'q', '.', '.', '.'],
		['.', '.', '.', '.', 'p', 'r', '.', 'b'],
		['.', 'p', '.', '.', 'p', '.', '.', '.'],
		['.', '.', 'P', 'P', '.', '.', '.', 'Q'],
		['.', '.', 'K', '.', '.', '.', '.', '.']
	]
	queen = (6, 7)
	squares = [(7, 2), (0, 2), (6, 6), (1, 2), (4, 2), (0, 3), (6, 2), (4, 0), (3, 3), (7, 0)]
	expected_results = [False, False, True, True, False, False, True, False, False, False]

	for square, expected in zip(squares, expected_results):
		assert chess.possible_step(reformatBoard(chessboard), (queen, square)) is expected


def test_possible_step_bishop():
	"""
	Testing possible_step() function for bishop
	"""
	chessboard = [
		['N', '.', '.', '.', '.', '.', 'k', '.'],
		['.', '.', '.', 'P', '.', '.', '.', '.'],
		['.', '.', '.', 'B', '.', '.', '.', '.'],
		['.', '.', '.', '.', 'q', '.', '.', '.'],
		['.', '.', '.', '.', 'p', 'r', '.', 'b'],
		['.', 'p', '.', '.', 'p', '.', '.', '.'],
		['.', '.', 'P', 'P', '.', '.', '.', 'Q'],
		['.', '.', 'K', '.', '.', '.', '.', '.']
	]
	bishop = (4,7)
	squares = [(5, 6), (1, 2), (3, 4), (2, 0), (7, 1), (2, 5), (7, 5), (1, 4), (5, 5), (2, 1)]
	expected_results = [True, False, False, False, False, True, False, True, False, False]

	for square, expected in zip(squares, expected_results):
		assert chess.possible_step(reformatBoard(chessboard), (bishop, square)) is expected
	
def test_possible_step_rook():
	"""
	Testing possible_step() function for rook
	"""
	chessboard = [
		['N', '.', '.', '.', '.', '.', 'k', '.'],
		['.', '.', '.', 'P', '.', '.', '.', '.'],
		['.', '.', '.', 'B', '.', '.', '.', '.'],
		['.', '.', '.', '.', 'q', '.', '.', '.'],
		['.', '.', '.', '.', '.', 'r', '.', '.'],
		['.', 'p', '.', '.', 'p', '.', '.', '.'],
		['.', '.', 'P', 'P', '.', '.', '.', 'Q'],
		['.', '.', 'K', '.', '.', '.', '.', '.']
	]
	rook = (4, 5)
	squares = [(2, 4), (5, 0), (2, 5), (2, 3), (3, 1), (1, 6), (0, 1), (3, 1), (7, 3), (4, 2)]
	expected_results = [False, False, True, False, False, False, False, False, False, True]

	for square, expected in zip(squares, expected_results):
		assert chess.possible_step(reformatBoard(chessboard), (rook, square)) is expected



# def test_in_board():
# 	NotImplemented


# 	# ChessBoard = \
# 	# 	[
# 	# 		["r", "n", "b", "q", "k", "b", "n", "r"],
# 	# 		["p", "p", "p", "p", "p", "p", "p", "p"],
# 	# 		[".", ".", ".", ".", ".", ".", ".", "."],
# 	# 		[".", ".", ".", ".", ".", ".", ".", "."],
# 	# 		[".", ".", ".", ".", ".", ".", ".", "."],
# 	# 		[".", ".", ".", ".", ".", ".", ".", "."],
# 	# 		["P", "P", "P", "P", "P", "P", "P", "P"],
# 	# 		["R", "N", "B", "Q", "K", "B", "N", "R"]
# 	# 	]
  
# 	# assert chess.in_check(reformatBoard(ChessBoard), (7,4)) is True





