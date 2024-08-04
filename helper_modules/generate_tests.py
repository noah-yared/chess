import random


def generate_board():
  board = [["." for _ in range(8)] for _ in range(8)]

  pieces = "Pp"*8 + "Rr"*2 + "Bb"*2 + "Nn"*2 + "Qq"

  for piece in pieces:
    # use binary val to choose whether to include piece or not
    if random.randint(0,1):
      r,c = random.randint(0,7), random.randint(0,7)
      while board[r][c] != ".":
        r,c = random.randint(0,7), random.randint(0,7)
      board[r][c] = piece

  return board

# board = generate_board()
# for row in board:
#   print(f"{row},")

def generate_squares(n):
  return [
    (random.randint(0,7), random.randint(0,7)) for _ in range(n)
  ]

# print(generate_squares(10))

def flip_case(board):
  visited = set()
  for row in range(8):
    for col in range(8):
      if board[row][col] != "." and (row, col) not in visited:
        board[7-row][col], board[row][col] = board[row][col], board[7-row][col]
        visited.add((7-row, col))
  return board

chessboard = \
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


board = flip_case(chessboard)
for row in board:
  print(f"{row},")