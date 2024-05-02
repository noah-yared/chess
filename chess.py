import math
import pygame

# Objectives:
# --------------------------------------------------------------------------------------------------------------------------------------
# 
# Complete in_check function ------ IMPLEMENTED! TESTING!
# Complete checkmate function ------ IMPLEMENTED! TESTING! (RESORTED TO COPYING DICTIONARIES FOR EACH ITERATION)
# Code stalemate function ------ IMPLEMENTED! NOT TESTED YET!
# Review my possible_moves function ------ TODO
# Code king-side/queen-side castle ------ TODO
# Code pawn double-step ------ TODO
# Code enpassant ------- TODO
# Optimize and transfer to C++ (if too slow) ------ TODO
# Implement with pygame/sfml/sdl ------ TODO
# Add AI opponent using minimax and alpha-beta pruning ------ TODO
# Add Flask SQL backend to add puzzle database ------ TODO
# Use Python sockets to add online multiplayer feature ------ TODO

# Some helper functions -- LIKELY NOT NEEDED (other than squares_between):

def in_board(position):
    return position[0]>=0 and position[0]<8 and position[1]>=0  and position[1]<8
    
def on_edge(self):
    return self.position[0] in {0,7} or self.position[1] in {0,7}

def corner(self):
    return self.position[0], self.position[1] in {(0,0), (0,7), (7,0), (7,7)}

def squares_between(loc1, loc2):
    x1, y1 = loc1; x2, y2 = loc2
    dx, dy = x2-x1, y2-y1

    if dx == 0:
        if dy > 0:
            return [(x1, y1+d+1) for d in range(dy)]
        return [(x1, y1-d-1) for d in range(-dy)]
    elif dy == 0:
        if dx > 0:
            return [(x1+d+1, y1) for d in range(dx)]
        return [(x1-d-1, y1) for d in range(-dx)]
    else:
        diff = abs(dx)
        if dx>0 and dy>0:
            return [(x1+d+1, y1+d+1) for d in range(diff)]
        elif dx>0:
            return [(x1+d+1, y1-d-1) for d in range(diff)]
        elif dy>0:
            return [(x1-d-1, y1+d+1) for d in range(diff)]
        return [(x1-d-1, y1-d-1) for d in range(diff)]


class Board():
    """
    Move is a tuple of original position on curr_board and final_position.
    Move has already been validated. 
    """
    def __init__(self):
        self.white_pieces = \
            {(i,1):Pawn() for i in range(8)} | \
            {
                (0,0):Rook(), (7,0):Rook(),
                (1,0):Knight(), (6,0):Knight(),
                (2,0):Bishop(),(5,0):Bishop(),
                (3,0):King(), (4,0):Queen()
            }
        self.black_pieces = \
            {(j,6):Pawn() for j in range(8)} | \
            {
                (0,7):Rook(), (7,7):Rook(), 
                (1,7):Knight(), (6,7):Knight(),
                (2,7):Bishop(), (5,7):Bishop(),
                (3,7):King(), (4,7):Queen()
            }
        
    def set_board(self, white_pieces, black_pieces):
        """
        Used to generate different positions for testing
        """
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces

    def update_board(self, is_white, move):
        """
        Move piece from original_location to final_location 
        """
        white, black = self.board.white_pieces, self.board.black_pieces
        same_side, opposing = white, black if is_white else black, white
        
        same_side[move[1]] = same_side.pop(move[0])
        opposing.pop(move[1], None)

    def get_board(self):
        return self.white_pieces, self.black_pieces
        
    def get_occupied_squares(self):
        occupied_squares = set()
        for locations in self.board.values():
            occupied_squares |= locations
        return occupied_squares


class Piece():

    def __init__(self):
        raise NotImplementedError                       
    
    def get_color(self):
        return self.color    
    
    def get_possible_moves(self):
        if self.name == "Pawn": return Pawn().get_possible_moves()
        elif self.name == "Rook": return Rook().get_possible_moves()
        elif self.name == "Bishop": return Bishop().get_possible_moves()
        elif self.name == "Knight": return Knight().get_possible_moves()
        elif self.name == "King": return King().get_possible_moves()    
        else: return Queen().get_possible_moves() 
    
    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

class Pawn():

    def check_move(self, color, move, left, forward, right):
        x1,y1 = move[0]
        x2,y2 = move[1]

        dy, dx = (x2-x1, y2-y1) if color == "white" else (y1-y2, x1-x2)
        if (dx,dy) == (-1,1) and left:
            return True
        elif (dx,dy) == (0,1) and forward:
            return True
        elif (dx,dy) == (1,1) and right:
            return True
        return False

    def get_possible_moves(self):
        x,y = self.get_x(), self.get_y()
        
class Rook():

    def check_move(self, move, pieces):
        x1, y1 = move[0]
        x2, y2 = move[1]
        
        if x1 == x2 or y1 == y2:
            squares = squares_between(move[0], move[1])[:-1]
            for square in squares:
                if square in pieces[0] or square in pieces[1]:
                    print(square)
                    return False
            return True 
        return False

    def get_possible_moves(self):
        x,y =  self.get_x(), self.get_y()
        moves = set()

        col = x-1
        while col >= 0:
            if (col,y) in self.occupied:
                break
            moves.add((col,y)); col-=1

        col = x+1
        while col <= 7:
            if (col,y) in self.occupied:
                break
            moves.add((col,y)); col+=1

        row = y-1
        while row >= 0:
            if (x,row) in self.occupied:
                break
            moves.add((x,row)); row-=1

        row = y+1
        while row <= 7:
            if (x,row) in self.occupied:
                break
            moves.add((x,row)); row+=1

        return moves

class Knight():
    
    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1]

        if (abs(x2-x1), abs(y2-y1)) == (1,2) or \
            (abs(x2-x1), abs(y2-y1)) == (2,1):
            return True
        return False

    def get_possible_moves(self):
        x,y  = self.get_x(), self.get_y()

        return ({(x+i, y+j) for i in {-1, 1} for j in {-2, 2} \
                 if in_board(x+i,y+j)} | \
                    {(x+i, y+j) for i in {-2, 2} for j in {-1,1}\
                     if in_board(x+i,y+j)})

class Bishop():

    def check_move(self, move, pieces):
        x1, y1 = move[0]
        x2, y2 = move[1]

        if abs(x2-x1) == abs(y2-y1):
            squares = squares_between(move[0], move[1])[:-1]
            for square in squares:
                if square in pieces[0] or square in pieces[1]:
                    return False
            return True
        return False

    def get_possible_moves(self):
        x,y = self.get_x(), self.get_y()
        moves = set()

        col, row = x-1, y+1
        while col >= 0 and row <= 7:
            if (col, row) in self.occupied:
                break
            moves.add((col,row)); col-=1; row+=1
        
        col, row = x+1, y-1
        while col <= 7 and row >= 0:
            if (col, row) in self.occupied:
                break
            moves.add((col, row)); col+=1; row-=1

        col, row = x-1, y-1
        while col >= 0 and row >= 0:
            if (col, row) in self.occupied:
                break
            moves.add((col, row)); col-=1; row-=1

        col, row = x+1, y+1
        while col <= 7 and row <= 7:
            if (col, row) in self.occupied:
                break
            moves.add((col, row)); col+=1; row+=1

        return moves

class King():
    
    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1]

        if abs(x1-x2) <= 1 and abs(y2-y1) <= 1:
            return True
        return False
    
    def get_possible_moves(self):
        return {(x,y) for x in range(max(0,self.get_x()-1), min(8, self.get_x()+2))
                for y in range(max(0,self.get_y()-1), min(8, self.get_y()+2))} - {self.pos}

class Queen():
    
    def check_move(self, move, pieces):
        x1, y1 = move[0]
        x2, y2 = move[1] 

        if x1 == x2 or y1 == y2 or abs(x2-x1) == abs(y2-y1):
            squares = squares_between(move[0], move[1])[:-1]
            for square in squares:
                if square in pieces[0] or square in pieces[1]:
                    return False
            return True
        return False

    def get_possible_moves(self):
        return Bishop().get_possible_moves() | Rook().get_possible_moves()

class game():
    
    def __init__(self):
        # self.board = Board()
        self.white_king = (3,0)
        self.black_king = (3,7)
        self.Player1 = White()
        self.Player2 = Black()
        self.current_player = self.Player1
        self.moves = 0
        self.game_over = False

    def play_game(self):
        while not self.game_over: self.move()

        self.game_over()

    def get_current_player(self):
        return "white" if self.white else "black"

    def move(self):
        # wait for event -- pygame
        line1, line2 = "", ""
        while not line1:
            line1 = input().split()
        while not line2:
            line2 = input().split()
        move = (int(x) for x in line1), (int(y) for y in line2)
        if self.current_player.make_move(move):
            self.current_player = self.Player2 if self.current_player == self.Player1 else self.Player1

    def in_check(self, color, king, pieces=None):
        """
        Takes current board state, move that is attempted
        Returns boolean indicating whether [color] king is in check
        """
        x,y = king
        if pieces is None: 
            white, black = self.board.white_pieces, self.board.black_pieces
            same_side, opposing = (white, black) if color == "white" else (black, white)
        else:
            white, black = pieces 
            same_side, opposing = (white, black) if color == "white" else (black, white)
        self.danger = None # checking piece
           
    # vertical axis:
        col, row = x,y+1
        while row<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Rook, Queen)): 
                    self.danger = col, row
                    return True
            row+=1
        
        col, row = x, y-1
        while row>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col, row)], (Rook, Queen)):
                    self.danger = col, row
                    return True
            row-=1

    # horizontal axis:
        col, row = x+1, y
        while col<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Rook, Queen)):
                    self.danger = col, row
                    return True
            col+=1
        
        col, row = (x-1, y)
        while col>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Rook, Queen)):
                    self.danger = col, row
                    return True
            col-=1
        
    # left diagonal:
        col, row = x-1, y+1

        # quick pawn check:
        if (col, row) in opposing:
            if isinstance(opposing[(col, row)], Pawn):
                self.danger = col, row
                return True

        while col>=0 and row<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop, Queen)):
                    self.danger = col, row
                    return True
            col-=1; row+=1
        
        col, row = x+1, y-1
        while col<8 and row>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop, Queen)):
                    self.danger = col, row
                    return True
            col+=1; row-=1

    # right diagonal:
        col, row = x+1, y+1
        
        # quick pawn check:
        if (col, row) in opposing:
            if isinstance(opposing[(col, row)], Pawn):
                self.danger = col,row
                return True
            
        while col<8 and row<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop, Queen)):
                    self.danger = col, row
                    return True
            col+=1; row+=1

        col, row = x-1, y-1
        while col>=0 and row>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop, Queen)):
                    self.danger = col, row
                    return True
            col-=1; row-=1

    # knight check:
        displacements = [(dx,dy) for dx in {-1, 1} for dy in {-2, 2}]
        
        for dp in displacements:
            dx, dy = dp
            if (x+dx, y+dy) in opposing:
                if isinstance(opposing[(x+dx, y+dy)], Knight):
                    self.danger = x+dx, y+dy
                    return True
            if (x+dy, y+dx) in opposing:
                if isinstance(opposing[(x+dy, y+dx)], Knight):
                    self.danger = x+dx, y+dy
                    return True
        
        return False
    
    
    # call checkmate() if in_check() returns true
    def checkmate(self, color, king, pieces = None):
        # """
        # Takes in current state of board with [color] king in check
        # Returns boolean indicating whether [color] king is in checkmate
        # If true, game is over. 
        # """
        if pieces is None:
            white, black = self.board.white_pieces, self.board.black_pieces
            same_side, opposing = (white, black) if color == "white" else (black, white)
        else:
            white, black = pieces
            same_side, opposing = (white, black) if color == "white" else (black, white)

        if isinstance(opposing[self.danger], Knight): # knight case: MOVE KING TO SAFETY or CAPTURE KNIGHT
            for dx in range(-1,2):
                for dy in range(-1,2):
                    new_king = king[0]+dx, king[1]+dy
                    if in_board(new_king) and \
                        new_king not in same_side and \
                            not Knight().check_move((self.danger, new_king)):
                        new_same_side, new_opposing = self.simulate_move(same_side, opposing, (king, new_king))
                        pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                        if not self.in_check(color, new_king, pieces):
                            return False
            for loc in same_side:
                if loc != king:
                    piece = same_side[loc]
                    if isinstance(piece, Pawn):
                        if self.pawn_available_square(color, (loc, self.danger), (white, black)):
                            new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, self.danger))
                            pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                            if not self.in_check(color, king, pieces):
                                return False
                    elif isinstance(piece, Knight):
                        if piece.check_move((loc,self.danger)):
                            new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, self.danger))
                            pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                            if not self.in_check(color, king, pieces):
                                return False
                    else:
                        if piece.check_move((loc, self.danger),(white, black)):
                            new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, self.danger))
                            pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                            if not self.in_check(color, king, pieces):
                                return False

        else:
            defensive_squares = squares_between(king, self.danger)
            print("squares between",king, self.danger, defensive_squares)
            attacking_piece = opposing[self.danger]
            for dx in range(-1,2):
                for dy in range(-1,2):
                    new_king = king[0]+dx, king[1]+dy
                    if in_board(new_king) and \
                        new_king not in same_side and \
                            not attacking_piece.check_move((self.danger, new_king), (white, black)):
                        new_same_side, new_opposing = self.simulate_move(same_side, opposing, (king, new_king))
                        pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                        if not self.in_check(color, new_king, pieces):
                            return False
            for loc in same_side:
                if loc != king:
                    piece = same_side[loc]
                    for square in defensive_squares:
                        if isinstance(piece, Pawn):
                            if self.pawn_available_square(color, (loc, square), pieces):
                                new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, square))
                                pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                                if not self.in_check(color, king, pieces):
                                    return False
                        elif isinstance(piece, Knight):
                            if piece.check_move((loc, square)):
                                new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, square))
                                pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                                if not self.in_check(color, king, pieces):
                                    return False

                        else:
                            if isinstance(piece, Bishop) and square == (7,0): print(white, black)
                            if piece.check_move((loc, square), (white, black)):
                                new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, square))
                                pieces = (new_same_side, new_opposing) if color == "white" else (new_opposing, new_same_side)
                                if not self.in_check(color, king, pieces):
                                    return False
        return True

    def stalemate(self, color, king):
        white, black = self.board.white_pieces, self.board.black_pieces
        same_side, opposing = (white, black) if color == "white" else (black, white)

        for loc in same_side:
            piece = same_side[loc]
            if isinstance(piece, King()): # king position will change
                for dest in piece.get_possible_moves():
                    new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, dest))
                    if not self.in_check(color, dest, (new_same_side, new_opposing)):
                        king = dest
                        return False       
            else:
                for dest in piece.get_possible_moves():
                    new_same_side, new_opposing = self.simulate_move(same_side, opposing, (loc, dest))
                    if not self.in_check(color, king, (new_same_side, new_opposing)):
                        return False 
        return True
    
    def game_over(self):
        raise NotImplementedError #TODO

    def valid_move(self, location, destination, white):
        if location != destination and in_board(destination):
            return self.board[location].check_move((location, destination))

    def possible_moves(self, piece, location):
        return location, Piece(piece, location, self.board).get_possible_moves()
    
    def get_valid_moves(self, piece, location):
        raise NotImplementedError #TODO

    def simulate_move(self, same_side, opposing, move):
        same_side_copy = {(move[1] if key == move[0] else key):val
                          for key, val in same_side.items()}
        opposing_copy = {key:val 
                         for key, val in opposing.items()
                         if key != move[1]}
                
        return same_side_copy, opposing_copy

    def promotion(self):
        raise NotImplementedError #TODO
    
    def pawn_available_square(self, color, move, pieces):
        if pieces is not None:
            x,y = move[0]
            white_pieces, black_pieces = pieces
            forward = (x,y+1) not in black_pieces if color =="white" else (x,y+1) not in white_pieces
            left_diagonal, right_diagonal = (x-1,y+1) in black_pieces, (x+1,y+1) in black_pieces
            return Pawn().check_move(color, move, left_diagonal, forward, right_diagonal)
        else:
            x,y = move[0]
            forward = (x,y+1) not in self.board.black_pieces if color=="white" else (x,y+1) not in self.board.white_pieces
            left_diagonal, right_diagonal = (x-1,y+1) in self.board.black_pieces, (x+1,y+1) in self.board.black_pieces
            return Pawn().check_move(color, move, left_diagonal, forward, right_diagonal)


class Player():

    def make_move(self):
        self.current_player.make_move()  

    def pawn_available_square(self, white, move):
        x,y = move[0]
        forward = (x,y+1) not in self.board.black_pieces if white else (x,y+1) not in self.board.white_pieces
        left_diagonal, right_diagonal = (x-1,y+1) in self.board.black_pieces, (x+1,y+1) in self.board.black_pieces
        return Pawn().check_move(white, move, left_diagonal, forward, right_diagonal)

class White(Player):
    
    def make_move(self, move):
        curr, dest = move
        if curr != dest and self.in_range(dest) and curr in self.board.white_pieces and dest not in self.board.black_pieces:
            piece = self.board.white_pieces[curr]
            valid_move = self.pawn_available_square(True, move) if isinstance(piece, Pawn()) else piece.check_move()      
            if valid_move:
                king_position = dest if isinstance(piece, King())\
                      else self.white_king
                if self.check: # make sure white king escapes check
                    if self.in_check("white", king_position):
                        return False
                self.board.update_board(True, move)
                self.white_king = king_position
                if self.in_check("black", self.black_king):
                    self.check = True
                    possible_defenses = self.defend("black", self.black_king)
                    if self.checkmate("black", possible_defenses):
                        self.game_over = "Checkmate"
                        return False
                elif self.stalemate():
                    self.game_over = "Stalemate"
                    return False
                self.check = False
                return True
  

class Black(Player):
    def make_move(self, move):
        curr, dest = move
        if curr != dest and self.in_range(dest) and curr in self.board.black_pieces and dest not in self.board.black_pieces:
            piece = self.board.black_pieces[curr]
            valid_move = self.pawn_available_square(False, move) if isinstance(piece, Pawn()) else piece.check_move()      
            if valid_move:
                king_position = dest if isinstance(self.board[curr], King())\
                      else self.black_king
                if self.check: # make sure black king escapes check
                    if self.in_check("black", king_position):
                        return False
                self.board.update_board(False, move)
                self.black_king = king_position
                if self.in_check("white", self.white_king):
                    self.check = True
                    possible_defenses = self.defend("white", self.white_king)
                    if not possible_defenses or self.checkmate("white", self.white_king, possible_defenses):
                        self.game_over = "Checkmate"
                        return False
                elif self.stalemate():
                    self.game_over = "Stalemate"
                    return False  
                return True


# class AI:
#     """
#     Implement Minimax/Alpha-Beta pruning for AI opponent
#     """
    
#     raise NotImplementedError # TODO
    


# if __name__ == "__main__":
#     """
#     Run Game Here
#     """
