# Refactored!


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
        "k": King("black"),
    }

    return {
        (row, col): mapping[chessboard[row][col]]
        for row in range(8)
        for col in range(8)
        if chessboard[row][col] != "."
    }


default_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


### PIECE CLASSES ###


class Pawn:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_type(self):
        return "P" if self.color == "white" else "p"

    def can_double_step(self, position):
        """
        Parameter(s): Takes in position of pawn
        Returns: True if pawn can double step, else False
        """
        if self.color == "white":
            if position[0] == 6:
                return True
        elif position[0] == 1:
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
            if (r1, c1) in generate_pawn_attack_positions(pieces, (r2, c2)):
                return True
        return False

    def generate_moves(self, pieces, square):
        moves = []
        dr = -1 if self.color == "white" else 1
        r, c = square
        if self.can_double_step(square):
            if in_board((r + 2 * dr, c)) and (r + 2 * dr, c) not in pieces:
                moves.append((square, (r + 2 * dr, c)))
        if in_board((r + dr, c)) and (r + dr, c) not in pieces:
            moves.append((square, (r + dr, c)))
        if in_board((r + dr, c - 1)):
            if (r + dr, c - 1) in pieces and pieces[
                (r + dr, c - 1)
            ].color != self.color:
                moves.append((square, (r + dr, c - 1)))
        if in_board((r + dr, c + 1)):
            if (r + dr, c + 1) in pieces and pieces[
                (r + dr, c + 1)
            ].color != self.color:
                moves.append((square, (r + dr, c + 1)))
        return moves


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_type(self):
        return "N" if self.color == "white" else "n"

    def possible_move(self, pieces, move):
        if (abs(move[0][0] - move[1][0]), abs(move[0][1] - move[1][1])) not in {
            (1, 2),
            (2, 1),
        }:
            return False
        if not is_same_color(pieces, *move):
            return True
        return False

    def generate_moves(self, pieces, square):
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
        return [
            (square, (r + dr, c + dc))
            for (dr, dc) in directions
            if in_board((r + dr, c + dc))
            and not is_same_color(pieces, (r + dr, c + dc), square)
        ]


class Rook:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_type(self):
        return "R" if self.color == "white" else "r"

    def possible_move(self, pieces, move):
        return has_line_of_sight(pieces, *move)

    def generate_moves(self, pieces, square):
        moves = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = square[0] + dr, square[1] + dc
            while in_board((r, c)):
                if is_same_color(pieces, (r, c), square):
                    break
                if (r, c) in pieces:
                    moves.append((square, (r, c)))
                    break
                moves.append((square, (r, c)))
                r += dr
                c += dc
        return moves


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_type(self):
        return "B" if self.color == "white" else "b"

    def possible_move(self, pieces, move):
        return has_line_of_sight(pieces, *move)

    def generate_moves(self, pieces, square):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = square[0] + dr, square[1] + dc
            while in_board((r, c)):
                if is_same_color(pieces, (r, c), square):
                    break
                if (r, c) in pieces:
                    moves.append((square, (r, c)))
                    break
                moves.append((square, (r, c)))
                r += dr
                c += dc
        return moves


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_type(self):
        return "Q" if self.color == "white" else "q"

    def possible_move(self, pieces, move):
        return has_line_of_sight(pieces, *move)

    def generate_moves(self, pieces, square):
        moves = []
        directions = [
            (1, 1),
            (-1, 0),
            (1, -1),
            (1, 0),
            (-1, -1),
            (0, 1),
            (-1, 1),
            (0, -1),
        ]
        for dr, dc in directions:
            r, c = square[0] + dr, square[1] + dc
            while in_board((r, c)):
                if is_same_color(pieces, (r, c), square):
                    break
                if (r, c) in pieces:
                    moves.append((square, (r, c)))
                    break
                moves.append((square, (r, c)))
                r += dr
                c += dc
        return moves


class King:
    def __init__(self, color):
        self.color = color
        self.danger = None
        self.location = (7, 4) if color == "white" else (0, 4)
        self.moved = False

    def get_color(self):
        return self.color

    def get_type(self):
        return "K" if self.color == "white" else "k"

    def possible_move(self, pieces, move):
        if abs(move[1][0] - move[0][0]) <= 1 and abs(move[0][1] - move[1][1]) <= 1:
            if not is_same_color(pieces, *move):
                return True
        return False

    def set_danger(self, square):
        self.danger = square

    def remove_danger(self):
        self.danger = None

    def set_location(self, square):
        self.location = square
        self.moved = True

    def generate_moves(self, pieces, square):
        r, c = square
        return [
            (square, (r + dr, c + dc))
            for dr in range(-1, 2)
            for dc in range(-1, 2)
            if not is_same_color(pieces, (r + dr, c + dc), square)
            and in_board((r + dr, c + dc))
        ]


# dictionary representing possible move_directions of each piece (EXCLUDING PAWNS/KNIGHTS):
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

### Helper functions ###


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
    Returns: tuple of integers (dy, dx) that describe direction of STRAIGHT LINE
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
            r += dr
            c += dc
            continue
        if (
            is_same_color(pieces, king, (r, c))
            or not isinstance(pieces[(r, c)], move_directions[(dr, dc)])
            or (
                isinstance(pieces[(r, c)], King)
                and (r, c) != (king[0] + dr, king[1] + dc)
            )
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


def is_valid_castling_move(pieces, move, castling_privileges):
    if not isinstance(pieces[move[0]], King):
        return False
    castling_moves = {
        ((7, 4), (7, 2)): "Q",
        ((7, 4), (7, 6)): "K",
        ((0, 4), (0, 2)): "q",
        ((0, 4), (0, 6)): "k",
    }
    if castling_moves.get(move) not in castling_privileges or in_check(pieces, move[0]):
        return False
    print(move)
    dc = -1 if move[0][1] > move[1][1] else 1
    king_pos = move[0]
    for i in range(1, 3):
        new_king_pos = king_pos[0], king_pos[1] + i * dc
        if new_king_pos in pieces or not is_threat_resolved(
            pieces, king_pos, (king_pos, new_king_pos)
        ):
            return False
    return not (dc == -1 and ((king_pos[0], king_pos[1] + 3 * dc) in pieces))


def is_valid_enpassant_move(pieces, move, enpassant_squares: set):
    if not isinstance(pieces[move[0]], Pawn):
        return False
    valid_directions = (
        [(-1, 1), (-1, -1)]
        if pieces[move[0]].get_color() == "white" and move[1][0] != 5
        else (
            [(1, 1), (1, -1)]
            if pieces[move[0]].get_color() == "black" and move[1][0] != 2
            else []
        )
    )
    return (
        get_pawn_displacement(move) in valid_directions and move[1] in enpassant_squares
    )


def get_pawn_displacement(move):
    return move[1][0] - move[0][0], move[1][1] - move[0][1]


def is_pawn_promoting(pieces, move):
    if not isinstance(pieces[move[0]], Pawn):
        return False
    return (
        move[1][0] == 0 if pieces[move[0]].get_color() == "white" else move[1][0] == 7
    )


def update_board(pieces, move, castled, enpassant):
    """
    Parameter(s): Takes current board state, validated move (coordinate tuple (square1, square2))
    Returns: None, just alters board state to reflect move being made.
    """
    if isinstance(pieces[move[0]], King):  # update king position
        pieces[move[0]].set_location(move[1])
    pieces[move[1]] = pieces.pop(move[0])
    
    if castled: # need to update castled rook position
        (_, coli), (rowf, colf) = move
        if coli > colf: 
            pieces[(rowf, colf + 1)] = pieces.pop((rowf, 0))
        else:
            pieces[(rowf, colf - 1)] = pieces.pop((rowf, 7))

    elif enpassant: # remove caputured pawn
        (rowi, _), (_, colf) = move
        pieces.pop((rowi, colf))



def is_threat_resolved(pieces, king, move):
    """
    Parameter(s): Takes current board state, current location of king, move to be simulated.
    Returns: True if the king is no longer in check after move is made, else False
    """
    if not in_board(move[1]):
        return False
    new_pieces = simulate_move(pieces, move)
    new_king = move[1] if isinstance(pieces[move[0]], King) else king
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
    return False


def checkmate(pieces, king):
    """
    Parameter(s): Takes current board state, player who is represented by "white" or "black"
    Returns: True if player is in checkmate, else False
    """
    threat = pieces[king].danger

    # attempt to handle threat by king escaping
    if can_king_evade_check(pieces, king):
        pieces[king].remove_danger()  # danger is defused so set to None
        return False

    # Knight or Pawn threat
    if isinstance(pieces[threat], (Knight, Pawn)):
        # must capture to handle threat
        for location in pieces:
            if isinstance(pieces[location], King):
                continue
            if is_square_attacked_by_piece(pieces, location, threat):
                if is_threat_resolved(pieces, king, (location, threat)):
                    pieces[king].remove_danger()
                    return False
    else:
        # can block or capture to handle threat
        line_of_attack = get_line_of_attack(king, threat)
        for location in pieces:
            if isinstance(pieces[location], King) or not is_same_color(
                pieces, king, location
            ):
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


class game:

    def __init__(self, board_state):
        self.checkmate, self.stalemate, self.check = False, False, False
        (
            self.piece_placement,
            (self.pieces, self.white_king, self.black_king),
            self.turn,
            self.castling_privileges,
            self.enpassant_squares,
        ) = board_state
        self.castled, self.enpassant, self.promotion = False, False, False
        self.fen = None

    def update_player_turn(self):
        self.turn = "w" if self.turn == "b" else "b"

    def update_castling_privileges(self, square):
        if isinstance(self.pieces[square], King):
            if square == (0, 4):
                self.castling_privileges.discard("k")
                self.castling_privileges.discard("q")
            elif square == (7, 4):
                self.castling_privileges.discard("K")
                self.castling_privileges.discard("Q")

        elif isinstance(self.pieces[square], Rook):
            if square == (0, 0):
                self.castling_privileges.discard("q")
            elif square == (0, 7):
                self.castling_privileges.discard("k")
            elif square == (7, 0):
                self.castling_privileges.discard("Q")
            elif square == (7, 7):
                self.castling_privileges.discard("K")

    def update_enpassant_squares(self, move):
        self.enpassant_squares = set()
        if isinstance(self.pieces[move[0]], Pawn):
            dr = -1 if self.pieces[move[0]].get_color() == "white" else 1
            double_step = (2 * dr, 0)
            if get_pawn_displacement(
                move
            ) == double_step and self.is_enemy_piece_adjacent(move[1]):
                self.enpassant_squares.add(self.get_enpassant_square(move))

    def is_enemy_piece_adjacent(self, square):
        r, c = square
        adjacent_squares = [(r, c + dc) for dc in [-1, 1]]
        return any(
            adjacent_square in self.pieces
            and not is_same_color(self.pieces, square, adjacent_square)
            for adjacent_square in adjacent_squares
        )

    def get_enpassant_square(self, move):
        return (move[0][0] + move[1][0]) // 2, move[0][1]

    def stringify_enpassant_squares(self):
        return (
            "".join(f"{chr(ord('a') + c)}{8-r}" for r, c in self.enpassant_squares)
            or "-"
        )

    def stringify_castling_privileges(self):
        return "".join(self.castling_privileges) or "-"

    def stringify_piece_placement(self, move):
        # Split the string into tokens and then jump to token describing row, find where to place,
        # rewrite token, and join the tokens back together.
        rows = self.piece_placement.split("/")

        # Vacate intitial square with moving piece
        start_row, start_col_index = rows[move[0][0]], move[0][1]
        col_index, i, moved_piece = 0, 0, None
        new_row = []
        while i < len(start_row):
            ch = start_row[i]
            if col_index == start_col_index:  # Reached piece to move
                moved_piece = ch
                ch = "1"
            try:
                new_row[-1] = f"{int(new_row[-1]) + int(ch)}"
            except (ValueError, IndexError):
                new_row.append(ch)
            try:
                col_index += int(ch)
            except ValueError:
                col_index += 1
            i += 1
        rows[move[0][0]] = "".join(new_row)

        assert (
            moved_piece is not None
        ), "Did not grab piece from starting square row. :("

        # Move piece to new square
        end_row, end_col_index = rows[move[1][0]], move[1][1]
        col_index, i, piece_moved = 0, 0, False
        new_row = []
        while i < len(end_row) or not piece_moved:
            try:
                ch = end_row[i]
            except IndexError:
                ch = None
            if col_index >= end_col_index and not piece_moved:
                piece_moved = True
                if end_col_index == col_index:  # Replace occupied square
                    new_row.append(moved_piece)
                    try:
                        if int(ch) > 1:
                            new_row.append(f"{int(ch) - 1}")
                    except ValueError:
                        self.captured_piece = ch # store captured piece
                else:
                    empty_squares_after_piece = col_index - end_col_index - 1
                    try:
                        new_row[-1] = (
                            f"{int(new_row[-1]) - empty_squares_after_piece - 1}"
                        )
                    except (ValueError, IndexError):
                        print("Caught Unexpected Error")
                    try:
                        if not int(new_row[-1]):
                            new_row[-1] = moved_piece
                        else:
                            new_row.append(moved_piece)
                        if empty_squares_after_piece:
                            new_row.append(f"{empty_squares_after_piece}")
                        if ch is not None:
                            new_row.append(ch)
                    except (ValueError, IndexError):
                        print("Caught Unexpected Error")
            elif ch is not None:
                new_row.append(ch)
            try:
                col_index += int(ch)
            except:
                col_index += 1
            i += 1
        rows[move[1][0]] = "".join(new_row)

        if self.enpassant:
            # Vacate square with pawn that is captured by enpassant
            captured_pawn_row_index = 3 if move[1][0] == 2 else 4
            captured_pawn_col_index = move[1][1]
            captured_pawn_row = rows[captured_pawn_row_index]
            col_index, i, new_row = 0, 0, []
            while i < len(captured_pawn_row):
                ch = captured_pawn_row[i]
                if col_index == captured_pawn_col_index:
                    self.captured_piece = ch # store piece captured by enpassant
                    ch = "1"
                try:
                    new_row[-1] = f"{int(new_row[-1]) + int(ch)}"
                except (ValueError, IndexError):
                    new_row.append(ch)
                try:
                    col_index += int(ch)
                except ValueError:
                    col_index += 1
                i += 1
            rows[captured_pawn_row_index] = "".join(new_row)

        elif self.castled:
            # Vacate square with rook to be moved
            castled_rook_start_col_index = 7 if move[1][1] > move[0][1] else 0
            castled_rook_row = rows[move[0][0]]
            col_index, i, new_row = 0, 0, []
            while i < len(castled_rook_row):
                ch = castled_rook_row[i]
                if col_index == castled_rook_start_col_index:
                    castled_rook = ch
                    ch = "1"
                try:
                    new_row[-1] = f"{int(new_row[-1]) + int(ch)}"
                except (ValueError, IndexError):
                    new_row.append(ch)
                try:
                    col_index += int(ch)
                except ValueError:
                    col_index += 1
                i += 1
            rows[move[0][0]] = "".join(new_row)

            # Move castled rook to new vacant square
            castled_rook_end_col_index = 5 if castled_rook_start_col_index == 7 else 3
            castled_rook_row = new_row
            col_index, i, new_row, rook_moved = 0, 0, [], False
            while i < len(castled_rook_row) or not rook_moved:
                try:
                    ch = castled_rook_row[i]
                except IndexError:
                    ch = None
                if col_index >= castled_rook_end_col_index and not rook_moved:
                    rook_moved = True
                    if col_index == castled_rook_end_col_index:
                        new_row.append(castled_rook)
                        try:
                            if int(ch) > 1:
                                new_row.append(f"{int(ch) - 1}")
                        except ValueError:
                            pass
                    else:
                        empty_squares_after_rook = (
                            col_index - castled_rook_end_col_index - 1
                        )
                        try:
                            empty_squares_before_rook = (
                                int(new_row[-1]) - empty_squares_after_rook - 1
                            )
                            if empty_squares_before_rook:
                                new_row[-1] = f"{empty_squares_before_rook}"
                                new_row.append(castled_rook)
                            else:
                                new_row[-1] = castled_rook
                            if empty_squares_after_piece:
                                new_row.append(f"{empty_squares_after_rook}")
                            if ch is not None:
                                new_row.append(ch)
                        except (ValueError, IndexError):
                            print("Caught Unexpected Error.")
                else:
                    new_row.append(ch)
                try:
                    col_index += int(ch)
                except ValueError:
                    col_index += 1
                i += 1
            rows[move[1][0]] = "".join(new_row)

        return "/".join(rows)

    def make_move(self, move):
        # self.enpassant, self.castled, self.promotion = False, False, False
        self.captured_piece = None
        try: # Get piece type of moved piece
            self.moved_piece = self.pieces[move[0]].get_type()
        except:
            self.moved_piece = None
        player_color, king = (
            ("white", self.white_king)
            if self.turn == "w"
            else ("black", self.black_king)
        )
        if (
            move[0] not in self.pieces
            or self.pieces[move[0]].get_color() != player_color
        ):
            return False
        if in_board(move[1]) and not is_same_color(self.pieces, *move):
            # Validate move
            if is_valid_castling_move(self.pieces, move, self.castling_privileges):
                self.castled = True
            elif is_valid_enpassant_move(self.pieces, move, self.enpassant_squares):
                self.enpassant = True
            else:
                if not self.pieces[move[0]].possible_move(
                    self.pieces, move
                ) or not is_threat_resolved(self.pieces, king, move):
                    return False
                if isinstance(self.pieces[move[0]], Pawn):
                    if is_pawn_promoting(self.pieces, move):
                        self.promotion = True
            self.update_castling_privileges(move[0])
            self.update_enpassant_squares(move)
            self.update_player_turn()
            self.fen = " ".join(
                [
                    self.stringify_piece_placement(move),
                    self.turn,
                    self.stringify_castling_privileges(),
                    self.stringify_enpassant_squares(),
                ]
            )
            if isinstance(self.pieces[move[0]], King):
                self.black_king, self.white_king = (
                    (self.black_king, move[1])
                    if player_color == "white"
                    else (move[1], self.white_king)
                )
            # Make move and determine game state
            update_board(self.pieces, move, self.castled, self.enpassant)
            opp_king = self.black_king if player_color == "white" else self.white_king
            print("Looking for check...")
            if in_check(self.pieces, opp_king):
                print("Check!")
                self.check = True
                if checkmate(self.pieces, opp_king):
                    print("Mate!")
                    self.checkmate = True
            elif stalemate(self.pieces, opp_king):
                print("Stalemate!")
                self.stalemate = True
            return True
        return False


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
    "k": King("black"),
}


if __name__ == "__main__":
    pass

    # ### Helper Functions ###
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
            parse_algebraic_notation(squares[i : i + 2])
            for i in range(0, len(squares), 2)
        }

    def parse_algebraic_notation(square: str) -> tuple:
        return 8 - int(square[1]), ord(square[0]) - ord("a")

    def parse_castling_privileges(privileges: str) -> set:
        return set(privileges)

        #########################

        # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqKQ -"
        # board = parse_FEN(fen)[1][0]
        # pieces = {location: piece.get_type() for (location, piece) in board.items()}
        # print(pieces)
        # print(parse_FEN(fen))

        # def stringify_enpassant_squares(enpassant_squares):
        # for r, c in enpassant_squares:
        #     print(8 - r)
        # return "".join(f"{chr(ord('a') + c)}{8-r}" for r, c in enpassant_squares) or "-"

        # def parse_algebraic_notation(square: str) -> tuple:
        # return 8 - int(square[1]), ord(square[0]) - ord("a")

        # def get_enpassant_squares(squares: str):
        # if squares == "-":
        #     return set()
        # return {
        #     parse_algebraic_notation(squares[i : i + 2])
        #     for i in range(0, len(squares), 2)
        # }

    # enpassant_squares = "c5f3f2c1"

    # enpassant_squares_set = get_enpassant_squares(enpassant_squares)

    # print (enpassant_squares_set)
    # print(stringify_enpassant_squares(enpassant_squares_set))

    # move = ((7, 4), (7, 6))
    # fen = 'q3kb1r/4ppp1/2n1bn1p/pB6/8/2N2N2/PPPP1PPP/R1BQK2R w qkQK -'
    move = ((2, 4), (1, 5))
    fen = "r4bnr/ppp1p1kp/2n1Qp2/6pQ/8/8/PP1P1PPP/RNB2KNR w - -"

    # move = ((0,4), (0,2))
    # fen1 = 'rn2kbnr/pppbqppp/4P3/8/8/2PP4/PP3PPP/RNBQKBNR b qkKQ -'
    # fen2 = 'r3kbnr/pppbqppp/2n1P3/8/8/1PPP4/P4PPP/RNBQKBNR b qkKQ -'
    # fen3 = 'r3kbnr/pppq1ppp/2n1b3/8/2P5/3PB3/PP3PPP/RN1QKBNR b kKQq -'

    board_state = parse_FEN(fen)
    new_game = game(board_state)
    print(new_game.make_move(move))
    print(new_game.check)
    print(new_game.game_over)

    # _, (pieces, _, _), _, privileges, _ = parse_FEN(fen1)
    # _, (pieces, _, _), _, privileges, _ = parse_FEN(fen3)

    # print(is_valid_castling_move(pieces, move, privileges))

    # print(pieces.get((move[0][0], move[0][1] - 3)))
