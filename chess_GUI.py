import sys
import math
import pygame
from pygame.locals import (
  KEYDOWN,
  MOUSEBUTTONDOWN,
  MOUSEMOTION,
  K_ESCAPE,
  QUIT
)

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

pieces = []

class Board(pygame.sprite.Sprite):
  def __init__(self):
    super(Board, self).__init__()
    self.image = pygame.image.load("images/chessboard.png").convert_alpha()
    self.rect = self.image.get_rect()

class Pawn(pygame.sprite.Sprite):
  def __init__(self, color, pos):
    super(Pawn, self).__init__()
    self.pos = pos
    if color == "white": self.image = pygame.image.load("images/white_pawn.png").convert_alpha()
    else: self.image = pygame.image.load("images/black_pawn.png").convert_alpha() 
    self.rect = self.image.get_rect()
    self.rect.x = 60*pos[0]
    self.rect.y = 60*pos[1]  

class Knight(pygame.sprite.Sprite):
  def __init__(self, color, pos):
    super(Knight, self).__init__()
    self.pos = pos
    if color == "white": self.image = pygame.image.load("images/white_knight.png").convert_alpha()
    else: self.image = pygame.image.load("images/black_knight.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.x = 60*pos[0]
    self.rect.y = 60*pos[1] 

class Rook(pygame.sprite.Sprite):
  def __init__(self, color, pos):
    super(Rook, self).__init__()
    self.pos = pos
    if color == "white": self.image = pygame.image.load("images/white_rook.png").convert_alpha()
    else: self.image = pygame.image.load("images/black_rook.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.x = 60*pos[0]
    self.rect.y = 60*pos[1]

class Bishop(pygame.sprite.Sprite):
  def __init__(self, color, pos):
    super(Bishop, self).__init__()
    self.pos = pos
    if color == "white": self.image = pygame.image.load("images/white_bishop.png").convert_alpha()
    else: self.image = pygame.image.load("images/black_bishop.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.x = 60*pos[0]
    self.rect.y = 60*pos[1]

class Queen(pygame.sprite.Sprite):
  def __init__(self, color, pos):
    super(Queen, self).__init__()
    self.pos = pos
    if color == "white": self.image = pygame.image.load("images/white_queen.png").convert_alpha()
    else: self.image = pygame.image.load("images/black_queen.png") 
    self.rect = self.image.get_rect()
    self.rect.x = 60*pos[0]
    self.rect.y = 60*pos[1]

class King(pygame.sprite.Sprite):
  def __init__(self, color, pos):
    super(King, self).__init__()
    self.pos = pos
    if color == "white": self.image = pygame.image.load("images/white_king.png").convert_alpha()
    else: self.image = pygame.image.load("images/black_king.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.x = 60*pos[0]
    self.rect.y = 60*pos[1]


def adjust(pos):
  return pos[0]-160, pos[1]-60

def get_coordinate(mouse_pos):
  return (
    math.floor(mouse_pos[0]/60),
    math.floor(mouse_pos[1]/60)
  )

def make_move(move, piece1, piece2=None):
  # move logic from chess.py goes here
  print(move)
  piece1.rect.x, piece1.rect.y = 60*move[1][0], 60*move[1][1]
  print("move made!")


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
board = Board()

def get_pieces():
  pieces = pygame.sprite.Group() 

  # Pawns  
  for i in range(8): 
    pieces.add(Pawn("white", (i,1)))
    pieces.add(Pawn("black", (i,6)))

  # Rooks
  pieces.add(Rook("white", (0,0))); pieces.add(Rook("white", (7,0)))
  pieces.add(Rook("black", (0,7))); pieces.add(Rook("black", (7,7)))

  # Knights
  pieces.add(Knight("white", (1,0))); pieces.add(Knight("white", (6,0)))
  pieces.add(Knight("black", (1,7))); pieces.add(Knight("black", (6,7)))

  # Bishops
  pieces.add(Bishop("white", (2,0))); pieces.add(Rook("white", (5,0)))
  pieces.add(Bishop("black", (2,7))); pieces.add(Bishop("black", (5,7)))

  # Kings
  pieces.add(King("white", (3,0))); pieces.add(King("black", (3,7)))

  # Queens
  pieces.add(Rook("white", (4,0))); pieces.add(Rook("black", (4,7)))
  
  return pieces

pieces = get_pieces()

print ("loading board...")
running = True; clicked = False
move = [None, None]
while running:
  for event in pygame.event.get():
    if event.type == MOUSEBUTTONDOWN:
      mouse_pos = adjust(pygame.mouse.get_pos())
      if board.rect.collidepoint(mouse_pos):
        for piece in pieces:
          if piece.rect.collidepoint(mouse_pos):
            # ADD FUNCTIONALITY HERE
            # print("sprite_clicked!")
            # print("clicked before?", clicked)
            if not clicked: 
              move[0] = piece.pos; clicked = True; to_move = piece
            else: 
              move[1] = piece.pos
              make_move(move, to_move, piece)
              clicked = False; move = [None, None]
            break
        else:  
          # print("empty cell at", get_coordinate(mouse_pos), "clicked!")
          # print("clicked before?", clicked)
          if not clicked:
            move = [None, None]
          else:
            move[1] = get_coordinate(mouse_pos)
            print()
            make_move(move, to_move)
            clicked = False; move = [None, None]
      else:
        clicked = False; move = [None, None]
    
    elif event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        running = False

    elif event.type == QUIT:
      running = False

    board.image = pygame.image.load("images/chessboard.png").convert()
    for piece in pieces:
      board.image.blit(piece.image, piece.rect)

    screen.blit(board.image, (160,60))

    pygame.display.flip()

pygame.quit()
sys.exit()




