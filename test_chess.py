import chess

# helper function

def reformatBoard(chessboard):

	mapping = {
		"P": chess.Pawn(), "p":chess.Pawn(),
		"R": chess.Rook(), "r":chess.Rook(),
		"B": chess.Bishop(), "b":chess.Bishop(),
		"N": chess.Knight(), "n":chess.Knight(),
		"Q": chess.Queen(), "q":chess.Queen(),
		"K": chess.King(), "k":chess.King()
	}


	white, black = {}, {}
	for row in range(8):
		for col in range(8):
			if chessboard[row][col] != ".":
				if chessboard[row][col].isupper():
					white[(col, row)] = mapping[chessboard[row][col]]
				else:
					black[(col, row)] = mapping[chessboard[row][col]]


	return white, black

# # MOVE VALIDATION --- NEED TO FIX TESTS -> ADD PIECES PARAMETER FOR NON-KNIGHT/NON-PAWN PIECES

# def test_good_bishop_moves():
# 	# test that correct bishop moves are properly validated 
# 	move_1 = (2,2),(5,5)
# 	move_2 = (3,3),(0,0)
# 	move_3 = (6,6),(4,4)
# 	move_4 = (1,6),(4,3)
# 	move_5 = (2,4),(0,6)

# 	moves = [move_1, move_2, move_3, move_4, move_5]

# 	for move in moves:
# 		assert chess.Bishop().check_move(move) == True

# def test_wrong_bishop_moves():
# 	# test that incorrect bishop moves are properly detetcted:
# 	move_1 = (0,3),(1,1)
# 	move_2 = (3,3),(3,4)
# 	move_3 = (4,6),(7,5)
# 	move_4 = (7,7),(5,6)
# 	move_5 = (2,3),(0,6)

# 	moves = [move_1, move_2, move_3, move_4, move_5]

# 	for move in moves:
# 		assert chess.Bishop().check_move(move) == False

def test_good_knight_moves():
	# test that correct knight moves are properly validated 
	move_1 = (0,0),(2,1)
	move_2 = (3,3),(1,4)
	move_3 = (6,5),(4,6)
	move_4 = (7,7),(5,6)
	move_5 = (2,4),(0,5)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Knight().check_move(move) == True

def test_wrong_knight_moves():
	# test that incorrect knight moves are properly detetcted:
	move_1 = (0,3),(2,1)
	move_2 = (3,3),(3,3)
	move_3 = (4,6),(7,8)
	move_4 = (9,9),(5,6)
	move_5 = (2,4),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Knight().check_move(move) == False

# def test_good_rook_moves():
# 	# test that correct rook moves are properly validated 
# 	move_1 = (0,1),(2,1)
# 	move_2 = (3,3),(3,4)
# 	move_3 = (6,5),(6,6)
# 	move_4 = (7,7),(7,6)
# 	move_5 = (2,4),(0,4)

# 	moves = [move_1, move_2, move_3, move_4, move_5]

# 	for move in moves:
# 		assert chess.Rook().check_move(move) == True

# def test_wrong_rook_moves():
# 	# test that incorrect rook moves are properly detetcted:
# 	move_1 = (0,3),(2,1)
# 	move_2 = (3,3),(2,4)
# 	move_3 = (4,6),(7,8)
# 	move_4 = (9,9),(5,6)
# 	move_5 = (2,4),(0,6)

# 	moves = [move_1, move_2, move_3, move_4, move_5]

# 	for move in moves:
# 		assert chess.Rook().check_move(move) == False

# def test_good_queen_moves():
# 	# test that correct queen moves are properly validated 
# 	move_1 = (3,3),(3,6)
# 	move_2 = (2,4),(6,4)
# 	move_3 = (0,5),(0,0)
# 	move_4 = (5,2),(2,5)
# 	move_5 = (1,6),(5,2)

# 	moves = [move_1, move_2, move_3, move_4, move_5]

# 	for move in moves:
# 		assert chess.Queen().check_move(move) == True

# def test_wrong_queen_moves():
# 	# test that incorrect queen moves are properly detetcted:
# 	move_1 = (0,0),(2,1)
# 	move_2 = (8,4),(3,3)
# 	move_3 = (4,6),(7,8)
# 	move_4 = (7,7),(5,6)
# 	move_5 = (1,4),(0,6)

# 	moves = [move_1, move_2, move_3, move_4, move_5]

# 	for move in moves:
# 		assert chess.Queen().check_move(move) == False

def test_good_king_moves():
	# test that correct king moves are properly validated 
	move_1 = (3,3),(2,3)
	move_2 = (4,3),(4,4)
	move_3 = (6,5),(5,4)
	move_4 = (7,7),(6,7)
	move_5 = (2,4),(3,5)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.King().check_move(move) == True

def test_wrong_king_moves():
	# test that incorrect king moves are properly detetcted:
	move_1 = (0,3),(2,1)
	move_2 = (3,5),(3,3)
	move_3 = (4,6),(7,8)
	move_4 = (7,7),(5,6)
	move_5 = (2,4),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.King().check_move(move) == False

def test_good_white_pawn_moves():
	move_1 = (0,3),(2,1)
	move_2 = (3,5),(3,3)
	move_3 = (4,6),(7,8)
	move_4 = (7,7),(5,6)
	move_5 = (2,4),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]
	NotImplemented

def test_bad_white_pawn_moves():
	NotImplemented

def test_good_black_pawn_moves():
	NotImplemented

def test_bad_black_pawn_moves():
	NotImplemented

def test_in_check_01():
	# Check that in_check function correctly returns False for white king
	# in the default state of a chess board

	ChessBoard = \
				[
					["R", "N", "B", "K", "Q", "B", "N", "R"],
					["P", "P", "P", "P", "P", "P", "P", "P"],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "p", "p", "p", "p", "p", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]
	
	white, black = reformatBoard(ChessBoard)

	assert chess.game().in_check("white", (3,0), (white, black)) == False


def test_in_check_02():
	# Check that the in_check function returns False for 
	# black king for default state of chess board

	ChessBoard = \
				[
					["R", "N", "B", "K", "Q", "B", "N", "R"],
					["P", "P", "P", "P", "P", "P", "P", "P"],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "p", "p", "p", "p", "p", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]
	
	white, black = reformatBoard(ChessBoard)

	assert chess.game().in_check("black", (3,7), (white, black)) == False


def test_in_check_03():
	# Check that the in_check function returns false for a case where King is
	# not in direct line of attack of bishop

	ChessBoard = \
				[
					["R", "N", "B", "K", "Q", ".", "N", "R"],
					["P", "P", "P", "P", "P", ".", ".", "P"],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", "B", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "p", "p", "p", ".", "p", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]

	assert chess.game().in_check("black", (3,7), reformatBoard(ChessBoard)) == False

def test_in_check_bishop_attack_unblocked():
	# Check that the in_check function returns True for a case where black king is
	# in direct line of attack of bishop

	ChessBoard = \
				[
					["R", "N", ".", "K", "Q", "B", "N", "R"],
					["P", "P", "P", ".", "P", "P", ".", "P"],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", "B", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "p", "p", "p", ".", "p", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]

	assert chess.game().in_check("black", (3,7), reformatBoard(ChessBoard)) == True

def test_in_check_bishop_attack_blocked():
	# Check that the in_check function returns False for a case where black king is
	# protected from bishop in direct line of attack.

	ChessBoard = \
				[
					["R", "N", ".", "K", "Q", "B", "N", "R"],
					["P", "P", "P", ".", "P", "P", ".", "P"],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", "B", "."],
					[".", ".", ".", ".", ".", "p", ".", "."],
					["p", "p", "p", "p", ".", ".", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]

	assert chess.game().in_check("black", (3,7), reformatBoard(ChessBoard)) == False

def test_in_check_bishop_attack():
	ChessBoard = \
				[
					["R", ".", ".", "K", "b", "B", ".", "R"],
					[".", "P", "P", ".", "P", "P", "P", "P"],
					["P", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", "P", ".", ".", ".", "."],
					[".", ".", ".", "N", "N", ".", ".", "."],
					[".", ".", ".", ".", "p", "n", ".", "."],
					["p", "p", "B", ".", ".", ".", "p", "p"],
					["r", "n", "b", "k", "q", ".", "n", "r"]
				]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	assert new_game.in_check("black", (3,7), (white, black)) == True

def test_in_check_rook_attack():
	ChessBoard = \
			[
				[".", ".", ".", ".", "K", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["p", "p", "p", ".", ".", ".", ".", "."],
				[".", "k", ".", ".", "R", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)
	new_game = chess.game()
	assert new_game.in_check("black", (1,7), (white, black)) == True

def test_checkmate_default_board():
	"""
	Check that checkmate() returns False for the default state of the board
	"""
	ChessBoard = \
				[
					["R", "N", "B", "K", "Q", "B", "N", "R"],
					["P", "P", "P", "P", "P", "P", "P", "P"],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "p", "p", "p", "p", "p", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (3,7), (white, black)):
		assert chess.game().checkmate("white", (3,0), (white, black)) == False

def test_checkmate_bishop_check():
	"""
	Check that checkmate function returns False for the case where a 
	white bishop is attacking the black king Black's bishop, pawn, 
	and queen can move to block it.
	"""

	ChessBoard = \
				[
					["R", "N", ".", "K", "Q", "B", "N", "R"],
					["P", "P", "P", ".", "P", "P", "P", "P"],
					[".", ".", ".", "P", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", "B", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "p", "p", "p", ".", "p", "p", "p"],
					["r", "n", "b", "k", "q", "b", "n", "r"]
				]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (3,7), (white, black)):
		assert new_game.checkmate("black", (3,7), (white, black)) == False
	

def test_checkmate_scholars_mate():
	"""
	Check that checkmate function returns True for scholar's 
	mate as king is trapped in backrank.
	"""
	ChessBoard = \
			[
				[".", ".", ".", ".", "K", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["p", "p", "p", ".", ".", ".", ".", "."],
				[".", "k", ".", ".", "R", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (1,7), (white, black)):
		assert new_game.checkmate("black", (1,7), (white, black)) == True


def test_checkmate_smothered_mate():
	"""
	Check that checkmate function returns True for 
	smothered mate case, where king is smothered by 
	his pieces
	"""
	ChessBoard = \
			[
				[".", ".", ".", ".", "K", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["p", "p", "N", ".", ".", ".", ".", "."],
				["k", "r", ".", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (1,7), (white, black)):
		assert new_game.checkmate("black", (0,7), (white, black)) == True

def test_checkmate_protected_queen():
	"""
	Check that checkmate() returns True when white Queen 
	is protected by white Bishop and is attacking black King.
	"""
	ChessBoard = \
			[
				[".", ".", ".", "R", "K", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", "B", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["p", "Q", "p", ".", ".", ".", ".", "."],
				[".", "k", "r", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (1,7), (white, black)):
		assert new_game.checkmate("black", (1,7), (white, black)) == True

def test_checkmate_anastasias_mate_01():
	"""
	Check that checkmate() returns True for anastasias checkmate pattern.
	"""
	ChessBoard = \
				[
					[".", ".", ".", "R", "K", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", "B", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", ".", ".", ".", ".", "."],
					["p", "Q", "p", ".", ".", ".", ".", "."],
					[".", "k", "r", ".", ".", ".", ".", "."]
				]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (1,7), (white, black)):
		assert new_game.checkmate("black", (1,7), (white, black)) == True

def test_checkmate_anastasias_mate_02():
	"""
	Check that checkmate() returns True for anastasias checkmate pattern.
	"""
	ChessBoard = \
			[
				["R", ".", ".", ".", "K", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", "B", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["k", "p", "N", ".", ".", ".", ".", "."],
				[".", "r", "r", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (0,6), (white, black)):
		assert new_game.checkmate("black", (0,6), (white, black)) == True


def test_checkmate_legals_mate():
	ChessBoard = \
				[
					["R", ".", ".", "K", "b", "B", ".", "R"],
					[".", "P", "P", ".", "P", "P", "P", "P"],
					["P", ".", ".", ".", ".", ".", ".", "."],
					[".", ".", ".", "P", ".", ".", ".", "."],
					[".", ".", ".", "N", "N", ".", ".", "."],
					[".", ".", ".", ".", "p", "n", ".", "."],
					["p", "p", "B", "k", ".", ".", "p", "p"],
					["r", "n", "b", ".", "q", ".", "n", "r"]
				]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (3,6), (white, black)):
		assert new_game.checkmate("black", (3,6), (white, black)) == True


def test_checkmate_corner_mate():
	"""
	Check that checkmate() returns True for queen and king corner checkmate pattern.
	"""
	ChessBoard = \
			[
				["R", ".", ".", ".", ".", ".", "K", "."],
				[".", ".", ".", ".", ".", ".", "q", "."],
				[".", ".", ".", ".", ".", ".", ".", "k"],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("white", (6,0), (white, black)):
		assert new_game.checkmate("white", (6,0), (white, black)) == True


def test_checkmate_opera_mate():
	"""
	Check that checkmate() returns True for opera mate checkmate pattern.
	"""
	ChessBoard = \
			[
				[".", ".", ".", "r", "K", ".", ".", "."],
				[".", ".", "P", ".", ".", "P", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", "b", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["p", "p", ".", ".", ".", ".", ".", "."],
				[".", "k", ".", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("white", (4,0), (white, black)):
		assert new_game.checkmate("white", (4,0), (white, black)) == True

def test_checkmate_blackburnes_mate():
	"""
	Check that checkmate() returns True for Blackburne's checkmate pattern.
	"""
	ChessBoard = \
			[
				["R", ".", ".", ".", ".", "R", "K", "."],
				[".", ".", ".", ".", ".", ".", ".", "b"],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", "n", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", "b", ".", ".", ".", ".", ".", "."],
				[".", ".", "k", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("white", (6,0), (white, black)):
		assert new_game.checkmate("white", (6,0), (white, black)) == True


def test_checkmate_hook_mate():
	"""	
	Check that checkmate() returns True for hook mate checkmate pattern.
	"""
	ChessBoard = \
			[
				[".", ".", "r", ".", ".", ".", ".", "."],
				[".", "P", "K", ".", ".", ".", ".", "."],
				[".", "n", ".", ".", "B", ".", ".", "."],
				[".", ".", "p", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["k", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", "r", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (1,2), (white, black)):
		assert new_game.checkmate("black", (1,2), (white, black)) == True


def test_checkmate_hook_mate():
	"""	
	Check that checkmate() returns True for hook mate checkmate pattern.
	"""
	ChessBoard = \
			[
				[".", ".", "r", ".", ".", ".", ".", "."],
				[".", "P", "K", ".", ".", ".", ".", "."],
				[".", "n", ".", ".", "B", ".", ".", "."],
				["R", ".", ".", ".", ".", ".", ".", "."],
				["k", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", "Q", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", "r", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("black", (0,4), (white, black)):
		assert new_game.checkmate("black", (0,4), (white, black)) == True

def test_checkmate_fools_mate():
	"""
	Check that checkmate() returns True for the fools mate checkmate pattern
	"""
	ChessBoard = \
			[
				["R", "N", "B", "K", "Q", "B", "N", "R"],
				["P", ".", ".", "P", "P", "P", "P", "P"],
				[".", ".", "P", ".", ".", ".", ".", "."],
				["q", "P", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", "p", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				["p", "p", "p", ".", "p", "p", "p", "p"],
				["r", "n", "b", "k", ".", "b", "n", "r"]
			]
	
	white, black = reformatBoard(ChessBoard)

	new_game = chess.game()
	if new_game.in_check("white", (3,0), (white, black)):
		assert new_game.checkmate("white", (3,0), (white, black)) == True

def test_no_checkmate_01():
	
	ChessBoard = \
			[
				[".", ".", "r", ".", ".", ".", ".", "."],
				[".", "P", "K", ".", ".", ".", ".", "."],
				[".", "q", ".", ".", ".", ".", ".", "."],
				["b", ".", ".", ".", ".", ".", ".", "."],
				["k", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("white", (2,1), (white, black))
	assert new_game.checkmate("white", (2,1), (white, black)) == False

def test_no_checkmate_02():

	ChessBoard = \
			[
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", "P", "K", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", "B", ".", ".", "."],
				["R", ".", ".", ".", ".", ".", ".", "."],
				["k", "Q", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."],
				[".", ".", ".", ".", ".", ".", ".", "."]
			]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("black", (0,4), (white, black))
	assert new_game.checkmate("black", (0,4), (white, black)) == False

def test_no_checkmate_03():

	ChessBoard = \
		[
			[".", ".", ".", ".", "r", ".", ".", "."],
			[".", ".", ".", "K", ".", ".", ".", "B"],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", "n", ".", ".", ".", ".", ".", "."],
			["k", ".", ".", ".", ".", ".", "q", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", "r", ".", ".", ".", ".", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("white", (3,1), (white, black))
	assert new_game.checkmate("white", (3,1), (white, black)) == False


def test_no_checkmate_04():
	ChessBoard = \
		[
			[".", "K", "R", ".", ".", "Q", ".", "."],
			["P", "P", "P", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["R", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "b"],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", "p", "p", "p", ".", ".", "."],
			[".", ".", "r", "k", ".", ".", "R", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("black", (3,7), (white, black))
	assert new_game.checkmate("black", (3,7), (white, black)) == False


def test_no_checkmate_05():

	ChessBoard = \
		[
			[".", "K", ".", "R", ".", ".", ".", "."],
			["P", "P", "P", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["R", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", "B", "."],
			[".", ".", "p", ".", "p", ".", ".", "."],
			[".", ".", "r", "k", ".", ".", "q", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("black", (3,7), (white, black))
	assert new_game.checkmate("black", (3,7), (white, black)) == False

def test_no_checkmate_06():

	ChessBoard = \
		[
			[".", "K", ".", "R", ".", ".", ".", "."],
			["P", "P", "P", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["R", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", "p", ".", ".", "."],
			[".", ".", "p", ".", ".", ".", ".", "."],
			[".", ".", "r", "k", ".", ".", "q", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("black", (3,7), (white, black))
	assert new_game.checkmate("black", (3,7), (white, black)) == False

def test_no_checkmate_07():

	ChessBoard = \
		[
			[".", "K", ".", "R", ".", ".", ".", "."],
			["P", "q", "P", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["p", "p", "p", ".", ".", ".", ".", "."],
			[".", "k", "r", ".", ".", ".", ".", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("white", (1,0), (white, black))
	assert new_game.checkmate("white", (1,0), (white, black)) == False

def test_no_checkmate_08():

	ChessBoard = \
		[
			[".", ".", "K", ".", ".", ".", ".", "r"],
			["P", "R", ".", ".", ".", "r", ".", "."],
			[".", "P", "P", ".", ".", ".", ".", "."],
			["n", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", "p", ".", ".", ".", ".", ".", "."],
			["p", "B", "p", ".", ".", "p", "p", "p"],
			[".", ".", ".", ".", ".", ".", "k", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	assert new_game.in_check("white", (2,0), (white, black)) == True
	print(new_game.danger)
	assert new_game.checkmate("white", (2,0), (white, black)) == False


def test_no_checkmate_09():

	ChessBoard = \
		[
			["K", ".", "R", ".", "r", ".", ".", "."],
			["P", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["N", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["p", "p", "p", ".", ".", ".", ".", "b"],
			[".", "k", "r", ".", ".", ".", ".", "b"]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("white", (0,0), (white, black))
	assert new_game.checkmate("white", (0,0), (white, black)) == False

def test_no_checkmate_10():

	ChessBoard = \
		[
			[".", "K", ".", "R", ".", ".", ".", "."],
			["P", ".", ".", ".", ".", ".", ".", "."],
			["b", "q", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["p", "p", "p", ".", ".", ".", ".", "."],
			[".", "k", "r", ".", ".", ".", ".", "b"]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("white", (1,0), (white, black))
	assert new_game.checkmate("white", (1,0), (white, black)) == False

def test_checkmate_01():
	ChessBoard = \
		[
			[".", "K", ".", "R", ".", "Q", ".", "."],
			["P", "P", "P", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["R", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", "N", "b", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", "p", ".", "p", ".", ".", "."],
			[".", ".", "r", "k", ".", ".", "R", "."]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("black", (3,7), (white, black))
	assert new_game.checkmate("black", (3,7), (white, black)) == True


def test_checkmate_02():

	ChessBoard = \
		[
			["K", ".", ".", ".", "r", ".", ".", "."],
			["P", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", "B", ".", ".", ".", ".", "."],
			["n", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "."],
			["p", "p", "p", ".", ".", ".", ".", "."],
			[".", "k", "r", ".", ".", ".", ".", "b"]
		]
	
	white, black = reformatBoard(ChessBoard)	

	new_game = chess.game()
	new_game.in_check("white", (0,0), (white, black))
	assert new_game.checkmate("white", (0,0), (white, black)) == True

