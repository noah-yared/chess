import chess_main as c
import test_chess as t

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

print(isinstance(t.reformat_board(chessboard)[rook], c.Rook))
# print([c.possible_move(t.reformatBoard(chessboard), (queen, square)) for square in squares])
print([c.possible_step(t.reformat_board(chessboard), (rook, square)) for square in squares])