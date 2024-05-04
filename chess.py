import math

# REFACTOR CODEBASE:
# ________________________________________
# X ADD GET SAME_SIDE AND GET OPPOSING PIECES FUNCTION
# X REDUCE COMPLEXITY OF UPDATE_MOVE() + THOROUGHLY TEST 
# X CREATE ONE FUNCTION FOR ITERATING ALONG LINE ON BOARD:
# (GREATLY REDUCES COMPLEXITY OF GET_POSSIBLE_MOVE() AND IN_CHECK())
# X CREATE A SINGLE FUNCTION FOR ITERATION IN CHECKMATE() AND STALEMATE()
# X ADD SIMULATED_MOVE_IN_CHECK FUNCTION
# X ADD CAN_CAPTURE/CAN_LAND_ON OR CAN_BLOCK
# X TRY TO INCORPORATE IF (CONDITION) CONTINUE CONTROL FLOWS
# TO REDUCE INDENTATIONS AND MAKE CODEBASE MORE READABLE
# X MAYBE ADD CHECK_PIECE_TYPE() FUNCTION (MAYBE NOT NECESSARY??)
# __________________________________________
# X MAKE SURE TO ADD CLEAR DOCSTRING/COMMENTS!!!
#__________________________________________

# GOALS:
# _________________________________________
# MAKE FUNCTION PARAMETERS STANDARDIZED:
# X DO NOT SHY AWAY FROM PASSING BOARD AS A PARAMETER TO FUNCTION
# X KEEP PYGAME GUI IN MIND WHEN WRITING FUNCTIONS
# X MAKE FUNCTIONS TESTABLE
# X TEST FUNCTIONS AS I GO


### PIECE CLASSES ###

class Pawn():
	def __init__(self, color):
		self.color = color

	def get_color(self):
		return self.color

class Knight():
	def __init__(self, color):
		self.color = color

	def get_color(self):
		return self.color

class Rook():
	def __init__(self, color):
		self.color = color

	def get_color(self):
		return self.color

class Bishop():
	def __init__(self, color):
		self.color = color

	def get_color(self):
		return self.color

class Queen():
	def __init__(self, color):
		self.color = color

	def get_color(self):
		return self.color

class King():
	def __init__(self, color):
		self.color = color
		self.danger = None
		self.location = (4,7) if color == "white" else (4,0)
		self.moved = False

	def get_color(self):
		return self.color
	
	def set_danger(self, square):
		self.danger = square

	def remove_danger(self):
		self.danger = None

	def set_location(self, square):
		self.location = square
		self.moved = True

# dictionary representing possible move_directions of each piece (EXCLUDING PAWNS):
move_directions = {
	(1,2): Knight, (2,1): Knight,
	(1,0): (Rook, Queen, King), (0,1): (Rook, Queen, King),
	(-1,0): (Rook, Queen, King), (0,-1): (Rook, Queen, King),
	(1,1): (Bishop, Queen, King), (-1,1): (Bishop, Queen, King),
	(1,-1): (Bishop, Queen, King), (-1,-1): (Bishop, Queen, King)
}

def in_board(square):
	"""
	Parameter(s): Takes position tuple of integer coordinates
	Returns: True if square lies in board, else False
	"""
	return ((0<=square[0] and square[0]<=7) and 
			(0<=square[1] and square[1]<=7)) 

def get_line_of_attack(king, attack):
	"""
	Parameter(s): Takes position of king (square1) and piece on square2
	Returns: list of squares that lie on line between square1 and square2 
	not including square1.
	"""
	dr, dc = get_direction_of_line(king, attack)
	r, c = king
	r+=dr; c+=dc # adjust starting position one step

	line_of_attack = []
	while (r,c) != attack:
		line_of_attack.append((r,c))
		r+=dr; c+=dc
	
	return line_of_attack

def in_same_side(pieces, square, color):
	return pieces[square].get_color() == color

def has_straight_path(square1, square2):
	"""
	Parameter(s): Takes position of two pieces on board square1, square2
	Returns: True if there is a straight path of squares between the two pieces, else False
	"""
	r1, c1, = square1
	r2, c2 = square2
	return (r1 == r2) or (c1 == c2) or \
		abs(r1-r2) == abs(c1-c2)

def get_direction_of_line(square1, square2):
	"""
	Parameter(s): Takes two positions square1, square2
	Returns: tuple of integers (dy, dx) that describe direction of line
	between the points i.e. (0,1), (1,1), (1,-1)
	"""
	r1, c1 = square1
	r2, c2 = square2
	
	if r1 == r2:
		return (0,1) if c2>c1 else (0,-1)
	elif c1 == c2:
		return (1,0) if r2>r1 else (-1,0)
	elif r2 > r1:
		return (1,1) if c2>c1 else (1,-1)
	return (-1,1) if c2<c1 else (-1,-1)

def is_opposing(pieces, square1, square2):
	"""
	Parameter(s): Takes current board state, locations square1, square2
	of two pieces on the board
	Returns: True if pieces have different color, else False
	"""
	return pieces[square1].get_color() != pieces[square2].get_color()

def possible_move(pieces, move):
	"""
	Parameter(s): Takes current board state, move to be validated
	Returns: True if step has valid step size for piece type
	"""
	return isinstance(pieces[move[0]], move_directions(get_direction_of_line(move)))	

def has_line_of_sight(pieces, square1, square2):
	"""
	Parameter(s): Takes position of piece on square1 and position square2 (DOES NOT TAKE KNIGHTS OR PAWNS)
	Returns: True if there is no piece lying on the line of squares between 
	square1 and square2, else False
  	"""
	if not has_straight_path(square1, square2) or not possible_move(pieces, (square1, square2)): # CANNOT REACH
		return False
	dr, dc = get_direction_of_line(square1, square2)
	r,c = square1
	r+=dr; c+=dc
	while (r,c) != square2:
		if (r,c) in pieces:
			return False
		r+=dr; c+=dc
	return True

def is_king_directly_attacked_along_direction(pieces, king, direction):
	"""
	Parameter(s): Takes current board state, location of king, and
	directtion along which to look for attack
	Returns: True if there is a piece (ROOK, BISHOP, OR QUEEN) with direct attack on king
	"""
	r,c = king
	dr, dc = direction
	r+=dr; c+=dc
	while in_board((r,c)):
		if (r,c) not in pieces:
			continue
		if not is_opposing(pieces, king, (r,c)) or \
			not isinstance(pieces[(r,c)], move_directions[(r,c)]):
			break
		pieces[king].set_danger((r,c)) # store attacking piece in danger
		return True
	return False

def simulate_move(pieces, move):
	"""
	Parameter(s): Takes current board state, move to be simulated
	Returns: copy of board dictionary with move made
	"""
	return {
			(loc if loc != move[0] else move[1]):piece 
			for loc, piece in pieces.items() 
			if loc != move[1]
		}

def generate_knight_attack_positions(king):
	"""
	Parameter(s): Takes current board state, location of king
	Returns: list of all the possible opposing knight positions
	that attack the king
	"""
	r,c = king
	directions = [
		(1,2),(-1,2),(1,-2),(-1,-2)
		(2,1),(-2,1),(2,-1),(-2,-1)
	]
	return [(r+dr, c+dc) for (dr,dc) in directions 
				 if in_board(r+dr, c+dc)] 

def generate_pawn_attack_positions(pieces, king):
	"""
	Parameter(s): Takes current board state, location of king
	Returns: list of all the possible opposing pawn positions 
	that attack the king
	"""
	r,c = king 
	return [(r+1,c-1), (r+1,c-1)] \
		if pieces[king].get_color() == "white" \
		else [(r-1,c-1), (r-1,c+1)]

def is_king_attacked_by_knight(pieces, king, square):
	"""
	Parameter(s): Takes current board state, location of king, and 
	square to be checkd
	Returns: True if opposing knight at location square is attacking
	king, else False
	"""
	if square not in pieces:
		return False
	if not is_opposing(pieces, king, square) or \
		not isinstance(pieces[square], Knight):
		return False
	pieces[king].set_danger(square)
	return True

def is_king_attacked_by_pawn(pieces, king, square):
	"""
	Parameter(s): Takes current board state, location of king, and
	square to be checked
	Returns: True if opposing pawn at location square is attacking 
	king, else False
	"""
	if square not in pieces:
		return False
	if not is_opposing(pieces, king, square) or \
		not isinstance(pieces[square], Pawn):
		return False
	pieces[king].set_danger(square)
	return True

def in_check(pieces, king):
	"""
	Parameter(s): Takes current board state, location of king
	Returns: True if king is in_check in current board state, 
	else False
	"""
	# knight check
	for location in generate_knight_attack_positions(king):
		if is_king_attacked_by_knight(pieces, king, location):
			return True

	# pawn check -- if opposition is black dr is +1, else dr is -1 
	for location in generate_pawn_attack_positions(pieces, king):
		if is_king_attacked_by_pawn(pieces, king, location):
			return True

	# directions for rook, bishop, or queen check
	directions = [
		(0,1),(0,-1),(1,0),(-1,0),
		(-1,1),(1,-1),(1,1),(-1,1)
	]
	for direction in directions:
		if is_king_directly_attacked_along_direction(pieces, king, direction):
			return True
	return False

def generate_king_moves(king):
	"""
	Parameter(s): Takes current king location
	Returns: list of possible valid moves that king can make
	"""
	pass

def can_block(pieces, king, attack, blocking_piece):
	"""
	Parameter(s): Takes current board state, position of king on square1, 
	position of attacking piece on square2, and position of blocking_piece
	Returns: True if blocking_piece can obstruct line of attack of attack piece
	on king
	"""
	## I DONT KNOW IF NEEDED (LIKELY NOT)
	pass
	


def can_capture(pieces, square1, square2):
	"""
	Parameter(s): Takes current board state, position of piece on square1 
	and position square2.
	Returns: True if piece on square1 can capture piece on square2
	"""
	return is_opposing(pieces, square1, square2) and \
		has_line_of_sight(pieces, square1, square2)


def update_board(pieces, move):
	"""
	Parameter(s): Takes current board state, validated move (tuple of coordinates (square1, square2))
	Returns: None, just alters board state to reflect move being made.
	"""
	if isinstance(pieces[move[0]], King): # update king position
		pieces[move[0]].set_location(move[1])
	pieces[move[1]] = pieces.pop(move[0])

def checkmate(pieces, king):
	"""
	Parameter(s): Takes current board state, player who is represented by "white" or "black"
	Returns: True if player is in checkmate, else Falses
	"""


class game():
	
	def __init__(self):
		self.white_pieces = {

		}
		
		self.black_pieces = {

		}

	# TO BE FURTHER IMPLEMENTED ONCE HELPER FUNCTIONS ARE COMPLETE AND TESTED
