import math
import pygame

# Current Objectives:
# ---------------------------------
# Complete in_check function ------ IMPLEMENTED! NOT TESTED YET!
# Complete checkmate function
# Code stalemate function
# Code king-side/queen-side castle
# Code pawn double-step
# Code enpassant
# Transfer to C++ (if slow)
# Optimize 
# Implement with pygame/sfml/sdl

# Some helper functions -- LIKELY NOT NEEDED:

def in_board(position):
    return position[0]>=0 and position[0]<8 and position[1]>=0  and position[1]<8
    
def on_edge(self):
    return self.position[0] in {0,7} or self.position[1] in {0,7}

def corner(self):
    return self.position[0], self.position[1] in {(0,0), (0,7), (7,0), (7,7)}


class Board():
    """
    Move is a tuple of original position on curr_board and final_position.
    Move has already been validated. 
    """
    def __init__(self):
        self.white_pieces = {(i,1):Pawn() for i in range(8)} | \
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
        
        
    def get_board(self):
        return self.board

    def update_board(self, move):
        """
        Move piece from original_location to final_location 
        """
        self.board[self.get_final_location()] = self.board.pop(self.get_original_location())

    def get_board(self):
        return self.board
        
    def get_occupied_squares(self):
        occupied_squares = set()
        for locations in self.board.values():
            occupied_squares |= locations
        return occupied_squares


class Piece():

    def __init__(self, board = None):
        if board is not None: 
            self.occupied = Board(board).get_occupied_squares() # DONT KNOW IF NEEDED - REMOVE IF NECESSARY                             
    
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

class Pawn(Piece):

    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1]

    def get_possible_moves(self):
        x,y = self.get_x(), self.get_y()
        
class Rook(Piece):

    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1]
        
        return True if x1==x2 or y1==y2 else False

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

class Knight(Piece):
    
    def check_move(self, move, board):
        x1, y1 = move[0]
        x2, y2 = move[1]

        if (math.abs(x2-x1), math.abs(y2-y1)) == (1,2) or \
            (math.abs(x2-x1), math.abs(y2-y1)) == (2,1):
            return True

    def get_possible_moves(self):
        x,y  = self.get_x(), self.get_y()

        return ({(x+i, y+j) for i in {-1, 1} for j in {-2, 2} \
                 if in_board(x+i,y+j)} | \
                    {(x+i, y+j) for i in {-2, 2} for j in {-1,1}\
                     if in_board(x+i,y+j)})

class Bishop(Piece):

    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1]

        return True if math.abs(x2-x1) == math.abs(y2-y1) else False

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

class King(Piece):
    
    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1]

        if math.abs(x1-x2) <= 1 and math.abs(y2-y1) <= 1:
            # if not in_check(): #TODO
                return True
        return False
    def get_possible_moves(self):
        return {(x,y) for x in range(max(0,self.get_x()-1), min(8, self.get_x()+2))
                for y in range(max(0,self.get_y()-1), min(8, self.get_y()+2))} - {self.pos}

class Queen(Piece):
    
    def check_move(self, move):
        x1, y1 = move[0]
        x2, y2 = move[1] 

        if x1 == x2 or y1 == y2 or math.abs(x2-x1) == math.abs(y2-y1):
            return True
        return False

    def get_possible_moves(self):
        return Bishop().get_possible_moves() | Rook().get_possible_moves()

class game():
    
    def __init__(self):
        self.board = Board()
        self.white = True
        self.white_king = (3,0)
        self.black_king = (3,7)
        self.Player1 = Player("white")
        self.Player2 = Player("black")
        self.current_player = self.Player1
        self.moves = 0

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
            if not self.white:
                self.current_player = self.Player2
            else:
                self.current_player = self.Player1

    def in_check(self, color, king):
        """
        Takes current board state, move that is attempted
        Returns boolean indicating whether [color] king is in check
        """
        x,y = king
        white, black = self.board.white_pieces, self.board.black_pieces
        same_side, opposing = white, black if color == "white" else black, white
           
    # vertical axis:
        col, row = x,y+1
        while row<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Rook(), Queen())): 
                    return True
            row+=1
        
        col, row = x, y-1
        while row>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col, row)], (Rook(), Queen())):
                    return True
            row-=1

    # horizontal axis:
        col, row = x+1, y
        while col<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Rook(), Queen())):
                    return True
            col+=1
        
        col, row = x-1, y
        while col>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Rook(), Queen())):
                    return True
            col-=1
        
    # left diagonal:
        col, row = x-1, y+1

        # quick pawn check:
        if (col, row) in opposing:
            if isinstance(opposing[(col, row)], Pawn()):
                return True

        while col>=0 and row<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop(), Queen())):
                    return True
            col-=1; row+=1
        
        col, row = x+1, y-1
        while col<8 and row>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop(), Queen())):
                    return True
            col+=1; row-=1

    # right diagonal:
        col, row = x+1, y+1
        
        # quick pawn check:
        if (col, row) in opposing:
            if isinstance(opposing[(col, row)], Pawn()):
                return True
            
        while col<8 and row<8:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop(), Queen())):
                    return True
            col+=1; row+=1

        while col>=0 and row>=0:
            if (col, row) in same_side:
                break
            if (col, row) in opposing:
                if isinstance(opposing[(col,row)], (Bishop(), Queen())):
                    return True
            col-=1; row-=1

    # knight check:
        displacements = [(dx,dy) for dx in {-1, 1} for dy in {-2, 2}]
        
        for dp in displacements:
            dx, dy = dp
            if (x+dx, y+dy) in opposing:
                if isinstance(opposing[(x+dx, y+dy)], Knight()):
                    return True
            if (x+dy, y+dx) in opposing:
                if isinstance(opposing[(x+dy, y+dx)], Knight()):
                    return True
        
        return False
            

    # call function if in_check returns true
    def checkmate(self, color, king_pos):
        """
        Takes in current state of board with [color] king in check
        Returns boolean indicating whether [color] king is in checkmate
        If true, game is over. 
        """
        raise NotImplementedError #TODO

    def stale_mate(self, white):
        raise NotImplementedError #TODO
    
    def game_over(self):
        raise NotImplementedError #TODO

    def valid_move(self, location, destination, white):
        if location != destination and in_board(destination):
            return self.board[location].check_move((location, destination))

    def possible_moves(self, piece, location):
        return location, Piece(piece, location, self.board).get_possible_moves()
    
    def get_valid_moves(self, piece, location):
        raise NotImplementedError #TODO

    def make_move(self, location, destination, color):
        raise NotImplementedError #TODO
    
    def promotion(self):
        raise NotImplementedError #TODO


class Player(game):

    def make_move(self):
        self.current_player.make_move()   

class White(Player):
    def make_move(self, move):
        curr, dest = move
        if curr != dest and self.in_range(dest) and curr in self.board.white_pieces:
            if self.board[curr].check_move(move):
                king_position = dest if isinstance(self.board[curr], King())\
                      else self.white_king
                if check: # make sure white king escapes check
                    if self.in_check("white", king_position):
                        return False
                self.board.update_board(move)
                self.white_king = king_position
                if self.in_check("black", self.black_king):
                    check = True
                    if self.checkmate("black", self.black_king):
                        self.game_over()
  

class Black(Player):
    def make_move(self, move):
        curr, dest = move
        if curr != dest and self.in_range(dest) and curr in self.board.black_pieces:
            if self.board[curr].check_move(move):
                king_position = dest if isinstance(self.board[curr], King())\
                      else self.black_king
                if check: # make sure white king escapes check
                    if self.in_check("black", king_position):
                        return False
                self.board.update_board(move)
                self.black_king = king_position
                if self.in_check("white", self.white_king):
                    check = True
                    if self.checkmate("white", self.white_king):
                        self.game_over()
                elif self.stalemate():
                    self.game_over()


class AI:
    """
    Implement Minimax/Alpha-Beta pruning for AI opponent
    """
    
    raise NotImplementedError # TODO
    