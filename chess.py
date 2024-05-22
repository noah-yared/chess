# CODE BASE REFACTORED!
# ________________________________________
# X FIX GET_DIRECTION_OF_LINE() -- BUG FIXED!!!
# X ADD TESTS FOR POSSIBLE_MOVE() FOR EACH PIECE
# X TEST CHECK() FUNCTION USING OLD TESTCASES
# X TEST CHECKMATES() FUNCTION USING OLD TESTCASES
# X TEST STALEMATE() FUNCTION
# __________________________________________
# X MAKE SURE TO ADD CLEAR DOCSTRING/COMMENTS!!!
# __________________________________________

# GOALS:
# _________________________________________
# MAKE FUNCTION PARAMETERS STANDARDIZED:
# X DO NOT SHY AWAY FROM PASSING BOARD AS A PARAMETER TO FUNCTION
# X KEEP PYGAME GUI IN MIND WHEN WRITING FUNCTIONS
# X MAKE FUNCTIONS TESTABLE
# X TEST FUNCTIONS AS I GO



def reformat_board(chessboard):
    """
    Parameter(s): Takes list of lists of characters denoting each piece
    Returns: Dictionary of pieces that matches chess.py representation
    """

    mapping = {
        "P": Pawn("white"),
        "p": Pawn("black"),
        "R": Rook("white"),
        "r": Rook("black"),
        "B": Bishop("white"),
        "b": Bishop("black"),
        "N": Knight("white"),
        "n": Knight("black"),
        "Q": Queen("white"),
        "q": Queen("black"),
        "K": King("white"),
        "k": King("black")
    }

    return {
        (row, col): mapping[chessboard[row][col]]
        for row in range(8)
        for col in range(8)
        if chessboard[row][col] != "."
    }



### PIECE CLASSES ###




class Pawn:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_double_step(self, position):
        """
        Parameter(s): Takes in position of pawn
        Returns: True if pawn can double step, else False
        """
        if self.color == "white":
            if position[0] == 6:
                return True
        else:
            if position[0] == 1:
                return True
        return False

    def possible_move(self, pieces, move):
        """
        Parameter(s): Takes current board state, pawn move to be validated
        Returns: True if move is valid, else False
        """

        UP, DOWN = -1, 1
        dr = UP if self.color == "white" else DOWN
        (r1, c1), (r2, c2) = move
        if (r2, c2) not in pieces:
            if (r1 + dr, c1) == (r2, c2) or (
                self.can_double_step((r1, c1)) and (r1 + 2 * dr, c1) == (r2, c2)
            ):
                return True
        elif not is_same_color(pieces, (r1, c1), (r2, c2)):
            print((r2,c2) in pieces)
            if (r1, c1) in generate_pawn_attack_positions(pieces, (r2, c2)):
                return True
        return False


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def possible_move(self, pieces, move):
        if (abs(move[0][0] - move[1][0], abs(move[0][1] - move[1][1]))) not in {
            (1, 2),
            (2, 1),
        }:
            return False
        if not is_same_color(pieces, *move):
            return True
        return False


class Rook:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def possible_move(self, pieces, move):
        return has_line_of_sight(pieces, *move)


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def possible_move(self, pieces, move):
        return has_line_of_sight(pieces, *move)


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def possible_move(self, pieces, move):
        return has_line_of_sight(pieces, *move)


class King:
    def __init__(self, color):
        self.color = color
        self.danger = None
        self.location = (7, 4) if color == "white" else (0, 4)
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
    (1, 0): (Rook, Queen, King),
    (0, 1): (Rook, Queen, King),
    (-1, 0): (Rook, Queen, King),
    (0, -1): (Rook, Queen, King),
    (1, 1): (Bishop, Queen, King),
    (-1, 1): (Bishop, Queen, King),
    (1, -1): (Bishop, Queen, King),
    (-1, -1): (Bishop, Queen, King),
}


def in_board(square):
    """
    Parameter(s): Takes position tuple of integer coordinates
    Returns: True if square lies in board, else False
    """
    return (0 <= square[0] and square[0] <= 7) and (0 <= square[1] and square[1] <= 7)


def get_line_of_attack(king, attack):
    """
    Parameter(s): Takes position of king (square1) and piece on square2
    Returns: list of squares that lie on line between square1 and square2
    not including square1.
    """
    dr, dc = get_direction_of_line(king, attack)
    r, c = king
    r += dr
    c += dc  # adjust starting position one step

    line_of_attack = []
    while (r, c) != attack:
        line_of_attack.append((r, c))
        r += dr
        c += dc
    line_of_attack.append(attack)

    return line_of_attack


def is_same_color(pieces, square1, square2):
    """
    Parameter(s): Takes current board state, position of two pieces on board square1, square2
    Returns: True if there are two pieces in each square with the same color, else False
    """
    return (
        square1 in pieces
        and square2 in pieces
        and pieces[square1].get_color() == pieces[square2].get_color()
    )


def has_straight_path(square1, square2):
    """
    Parameter(s): Takes position of two pieces on board square1, square2
    Returns: True if there is a straight path of squares between the two pieces, else False
    """
    r1, c1 = square1
    r2, c2 = square2
    return (r1 == r2) or (c1 == c2) or abs(r1 - r2) == abs(c1 - c2)


def get_direction_of_line(square1, square2):
    """
    Parameter(s): Takes two positions square1, square2
    Returns: tuple of integers (dy, dx) that describe direction of line
    between the points i.e. (0,1), (1,1), (1,-1)
    """
    r1, c1 = square1
    r2, c2 = square2

    if r1 == r2:
        return (0, 1) if c2 > c1 else (0, -1)
    if c1 == c2:
        return (1, 0) if r2 > r1 else (-1, 0)
    if r2 > r1:
        return (1, 1) if c2 > c1 else (1, -1)
    return (-1, 1) if c2 > c1 else (-1, -1)


def possible_step(pieces, move):
    """
    Parameter(s): Takes current board state, move to be validated (ONLY TAKES QUEEN, BISHOP, ROOK)
    Returns: True if step has valid step size for piece type
    """
    return (
        isinstance(pieces[move[0]], move_directions[get_direction_of_line(*move)])
        if has_straight_path(*move)
        else False
    )


def has_line_of_sight(pieces, square1, square2):
    """
    Parameter(s): Takes position of piece on square1 and position square2
    (DOES NOT TAKE KNIGHTS OR PAWNS)
    Returns: True if there is no piece lying on the line of squares between
    square1 and square2, else False
    """
    if not has_straight_path(square1, square2) or not possible_step(
        pieces, (square1, square2)
    ):  # CANNOT REACH
        return False
    dr, dc = get_direction_of_line(square1, square2)
    r, c = square1
    r += dr
    c += dc
    while (r, c) != square2:
        if (r, c) in pieces:
            return False
        r += dr
        c += dc
    return True


def is_king_directly_attacked_along_direction(pieces, king, direction):
    """
    Parameter(s): Takes current board state, location of king, and
    direction along which to look for attack
    Returns: True if there is a piece (ROOK, BISHOP, OR QUEEN) with direct attack on king
    """
    r, c = king
    dr, dc = direction
    r += dr
    c += dc
    while in_board((r, c)):
        if (r, c) not in pieces:
            r+=dr; c+=dc
            continue
        if is_same_color(pieces, king, (r, c)) or not isinstance(
            pieces[(r, c)], move_directions[(dr, dc)]
        ):
            break
        pieces[king].set_danger((r, c))  # store attacking piece in danger
        return True
    return False


def simulate_move(pieces, move):
    """
    Parameter(s): Takes current board state, move to be simulated
    Returns: copy of board dictionary with move made
    """
    return {
        (loc if loc != move[0] else move[1]): piece
        for loc, piece in pieces.items()
        if loc != move[1]
    }

def generate_knight_reachable_squares(square):
    """
    Parameter(s): Takes current board state, square on board
    Returns: list of all the possible knight positions
    that can reach the square
    """
    r, c = square
    directions = [
        (1, 2),
        (-1, 2),
        (1, -2),
        (-1, -2),
        (2, 1),
        (-2, 1),
        (2, -1),
        (-2, -1),
    ]
    return [(r + dr, c + dc) for (dr, dc) in directions if in_board((r + dr, c + dc))]


def generate_pawn_attack_positions(pieces, king):
    """
    Parameter(s): Takes current board state, location of king
    Returns: list of all the possible opposing pawn positions
    that attack the king
    """
    r, c = king
    return (
        [(r - 1, c - 1), (r - 1, c + 1)]
        if pieces[king].get_color() == "white"
        else [(r + 1, c - 1), (r + 1, c + 1)]
    )


def is_king_attacked_by_knight(pieces, king, square):
    """
    Parameter(s): Takes current board state, location of king, and
    square to be checked
    Returns: True if opposing knight at location square is attacking
    king, else False
    """
    if square not in pieces:
        return False
    if is_same_color(pieces, king, square) or not isinstance(pieces[square], Knight):
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
    if is_same_color(pieces, king, square) or not isinstance(pieces[square], Pawn):
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
    for location in generate_knight_reachable_squares(king):
        if is_king_attacked_by_knight(pieces, king, location):
            return True

    # pawn check -- if opposition is black dr is +1, else dr is -1
    for location in generate_pawn_attack_positions(pieces, king):
        if is_king_attacked_by_pawn(pieces, king, location):
            return True

    # rook, bishop, or queen check
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
    for direction in directions:
        if is_king_directly_attacked_along_direction(pieces, king, direction):
            return True
    return False


def is_square_attacked_by_knight(pieces, square, knight):
    """
    Parameter(s): Takes current board state, square to check, and location
    of knight
    Returns: True if square is attacked by the knight, else False
    """
    if is_same_color(pieces, square, knight):
        return False
    dr, dc = abs(knight[0] - square[0]), abs(knight[1] - square[1])
    return (dr, dc) in [(1, 2), (2, 1)]


def is_square_attacked_by_pawn(pieces, square, pawn):
    """
    Parameter(s): Takes current board state, square to check, and location
    of pawn
    Returns: True if square is attacked by the pawn, else False
    """
    return pieces[pawn].possible_move(pieces, (pawn, square))


def generate_king_reachable_squares(king):
    """
    Parameter(s): Takes current king location
    Returns: list of possible valid moves that king can make
    """
    r, c = king
    return [
        (r + dr, c + dc)
        for dr in range(-1, 2)
        for dc in range(-1, 2)
        if in_board((r + dr, c + dc))
    ]


def can_block(pieces, blocking_piece, attack):
    """
    Parameter(s): Takes current board state, position of king on square1,
    position of attacking piece on square2, and position of blocking_piece
    Returns: True if blocking_piece can obstruct line of attack of attack piece
    on king
    """
    ## I DONT KNOW IF NEEDED (LIKELY NOT)
    pass


def is_square_attacked_by_piece(pieces, piece_location, square):
    """
    Parameter(s): Takes current board state, position of piece on square1
    and location on board square2.
    Returns: True if piece on square1 is attacking square2, else False
    """
    if isinstance(pieces[piece_location], Pawn):
        return is_square_attacked_by_pawn(pieces, square, piece_location)
    if isinstance(pieces[piece_location], Knight):
        return is_square_attacked_by_knight(pieces, square, piece_location)
    return not is_same_color(pieces, piece_location, square) and has_line_of_sight(
        pieces, piece_location, square
    )


def update_board(pieces, move):
    """
    Parameter(s): Takes current board state, validated move (coordinate tuple (square1, square2))
    Returns: None, just alters board state to reflect move being made.
    """
    if isinstance(pieces[move[0]], King):  # update king position
        pieces[move[0]].set_location(move[1])
    pieces[move[1]] = pieces.pop(move[0])


def is_threat_resolved(pieces, king, move):
    """
    Parameter(s): Takes current board state, current location of king, move to be simulated.
    Returns: True if the king is no longer in check after move is made, else False
    """
    new_pieces = simulate_move(pieces, move)
    new_king = move[1] if isinstance(move[0], King) else king
    print (move, "\n")
    print(pieces)
    print(new_king)
    return not in_check(new_pieces, new_king)


def can_king_evade_check(pieces, king):
    """
    Parameter(s): Takes current board state, current location of king
    Returns: True if king can escape check
    """
    for square in generate_king_reachable_squares(king):
        if is_same_color(pieces, king, square):  # check if king can land on square
            continue
        if is_threat_resolved(pieces, king, (king, square)):
            return True


# def can_pawn_disrupt_line_of_attack(pieces, king, pawn, line_of_attack):
# 	"""
# 	Parameter(s): Takes current board state, current location of king,
# 	location of pawn, list of squares in line of attack
# 	Returns: True if pawn can block the attack coming from the line of attakc
# 	"""
# 	for square in line_of_attack:
# 		if is_same_color(pieces, pawn, square):
# 			continue
# 		if is_square_attacked_by_pawn(pieces, square, pawn):
# 			if is_threat_resolved(pieces, king, (pawn, square)):
# 				pieces[king].remove_danger()
# 				return False


def checkmate(pieces, king):
    """
    Parameter(s): Takes current board state, player who is represented by "white" or "black"
    Returns: True if player is in checkmate, else False
    """
    threat = pieces[king].danger
    print(f"threat: {threat, pieces[threat]}")

    # attempt to handle threat by king escaping
    if can_king_evade_check(pieces, king):
        pieces[king].remove_danger()  # danger is defused so set to None
        return False

    # Knight or Pawn threat
    if isinstance(threat, (Knight, Pawn)):
        # must capture to handle threat
        for location in pieces:
            if is_square_attacked_by_piece(pieces, location, threat):
                if is_threat_resolved(pieces, king, (location, threat)):
                    pieces[king].remove_danger()
                    return False
    else:
        # can block or capture to handle threat
        line_of_attack = get_line_of_attack(king, threat)
        for location in pieces:
            if isinstance(pieces[location], King):
                continue
            for square in line_of_attack:
                if is_square_attacked_by_piece(pieces, location, square):
                    if is_threat_resolved(pieces, king, (location, square)):
                        pieces[king].remove_danger()
                        return False

    return True


def has_valid_pawn_move_from_square(pieces, king, square):
    """
    Parameter(s): Takes current board state, location of king, location of pawn
    Returns: True if there is a valid pawn move, else False
    """
    pawn = pieces[square]
    r, c = square

    UP, DOWN = -1, 1
    dr = UP if pawn.get_color() == "white" else DOWN

    # check forward move
    if (r + dr, c) not in pieces:
        if is_threat_resolved(pieces, king, ((r, c), (r + dr, c))):
            return True
        if pawn.can_double_step(square) and (r + 2 * dr) not in pieces:
            if is_threat_resolved(pieces, king, ((r, c), (r + 2 * dr, c))):
                return True

    # check diagonal moves
    for dc in (-1, 1):
        if (r + dr, c + dc) in pieces:
            if not is_same_color(pieces, (r, c), (r + dr, c + dc)):
                if is_threat_resolved(pieces, king, ((r, c), (r + dr, c + dc))):
                    return True
    return False


def has_valid_knight_move_from_square(pieces, king, square):
    """
    Parameter(s): Takes current board state, location of king, location of knight
    Returns: True if there is a valid knight move, else False
    """
    for location in generate_knight_reachable_squares(square):
        if is_threat_resolved(pieces, king, (square, location)):
            return True
    return False


def has_valid_move_from_square_along_direction(pieces, king, square, directions):
    """
    Parameter(s): Takes current board state, location of king, location of piece,
    list of directions to check
    Returns: True if there is a valid move for piece from square, else False
    """
    r, c = square
    for dr, dc in directions:
        if is_same_color(pieces, (r, c), (r + dr, c + dc)):
            continue
        if is_threat_resolved(pieces, king, ((r, c), (r + dr, c + dc))):
            return True
    return False


def has_valid_reachable_square_from_piece(pieces, king, square):
    """
    Parameter(s): Takes current board state, location of king, location of piece
    Returns: True if there is a valid move for piece, else False
    """
    piece = pieces[square]
    if isinstance(piece, Pawn):
        return has_valid_pawn_move_from_square(pieces, king, square)
    if isinstance(piece, Knight):
        return has_valid_knight_move_from_square(pieces, king, square)

    directions = []  # initialize list of directions to check for moves in
    if isinstance(piece, (Rook, Queen)):
        directions.extend([(-1, 0), (1, 0), (0, -1), (0, 1)])
    if isinstance(piece, (Bishop, Queen)):
        directions.extend([(-1, 1), (1, 1), (1, -1), (-1, -1)])
    return has_valid_move_from_square_along_direction(pieces, king, square, directions)


def stalemate(pieces, king):
    """
    Parameter(s): Takes current board state, location of king
    Returns: True if there are no possible moves that prevent king
    from getting into check, else False
    """
    # check if every king move leads to check
    if can_king_evade_check(pieces, king):
        return False

    # find any possible piece that can be moved on the kings side
    for location in pieces:
        if isinstance(pieces[location], King) or not is_same_color(
            pieces, king, location
        ):
            continue
        if has_valid_reachable_square_from_piece(pieces, king, location):
            return False
    return True


# # TO BE FURTHER IMPLEMENTED ONCE HELPER FUNCTIONS ARE TESTED
# class game():
# 	raise NotImplementedError


if __name__ == "__main__":
    pass
    # king_locations = [(1, 3), (3, 4), (7, 4), (5, 6), (1, 1), (7, 7)]
    # attacker_locations = [(4, 0), (1, 2), (3, 4), (6, 7), (7, 7), (7, 1)]

    # for king, attack in zip(king_locations, attacker_locations):
    #     print(get_direction_of_line(king, attack))

    # ChessBoard = \
	# 			[
	# 				["R", "N", "B", "K", "Q", ".", "N", "R"],
	# 				["P", "P", "P", "P", "P", ".", ".", "P"],
	# 				[".", ".", ".", ".", ".", ".", ".", "."],
	# 				[".", ".", ".", ".", ".", ".", "B", "."],
	# 				[".", ".", ".", ".", ".", ".", ".", "."],
	# 				[".", ".", ".", ".", ".", ".", ".", "."],
	# 				["p", "p", "p", "p", ".", "p", "p", "p"],
	# 				["r", "n", "b", "k", "q", "b", "n", "r"]
	# 			]

    # print(in_check(reformat_board(ChessBoard), (7,3)))
