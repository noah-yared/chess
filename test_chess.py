import chess

# MOVE VALIDATION

def test_good_bishop_moves():
	# test that correct bishop moves are properly validated 
	move_1 = (2,2),(5,5)
	move_2 = (3,3),(0,0)
	move_3 = (6,6),(4,4)
	move_4 = (1,6),(4,3)
	move_5 = (2,4),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Bishop().check_move(move) == True

def test_wrong_bishop_moves():
	# test that incorrect bishop moves are properly detetcted:
	move_1 = (0,3),(1,1)
	move_2 = (3,3),(3,4)
	move_3 = (4,6),(7,5)
	move_4 = (7,7),(5,6)
	move_5 = (2,3),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Bishop().check_move(move) == False

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

def test_good_rook_moves():
	# test that correct rook moves are properly validated 
	move_1 = (0,1),(2,1)
	move_2 = (3,3),(3,4)
	move_3 = (6,5),(6,6)
	move_4 = (7,7),(7,6)
	move_5 = (2,4),(0,4)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Rook().check_move(move) == True

def test_wrong_rook_moves():
	# test that incorrect rook moves are properly detetcted:
	move_1 = (0,3),(2,1)
	move_2 = (3,3),(2,4)
	move_3 = (4,6),(7,8)
	move_4 = (9,9),(5,6)
	move_5 = (2,4),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Rook().check_move(move) == False

def test_good_queen_moves():
	# test that correct queen moves are properly validated 
	move_1 = (3,3),(3,6)
	move_2 = (2,4),(6,4)
	move_3 = (0,5),(0,0)
	move_4 = (5,2),(2,5)
	move_5 = (1,6),(5,2)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Queen().check_move(move) == True

def test_wrong_queen_moves():
	# test that incorrect queen moves are properly detetcted:
	move_1 = (0,0),(2,1)
	move_2 = (8,4),(3,3)
	move_3 = (4,6),(7,8)
	move_4 = (7,7),(5,6)
	move_5 = (1,4),(0,6)

	moves = [move_1, move_2, move_3, move_4, move_5]

	for move in moves:
		assert chess.Queen().check_move(move) == False

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