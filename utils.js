export function FENToBoard(fen) {
  let board = new Array(64).fill(null);
  let row = 0, col = 0;
  for (let i = 0; i < fen.length; i++) {
    if (isNaN(Number(fen[i]))) {
      if (fen[i] === '/') {
        row++; col = 0;
      } else {
        board[8*row + col] = fen[i];
      }
    } else {
      col += isNaN(Number(fen[i]));
    }
  }
  return board
}

export function BoardToFEN(board) {
  let fen = [];
  for (let row = 0; row < 8; row++) {
    let emptySquares = 0;
    for (let col = 0; col < 8; col++) {
      if (board[8*row + col]) {
        emptySquares && fen.push(`${emptySquares}`);
        emptySquares = 0;
      }
      else {
        emptySquares++;
      }
    }
    emptySquares && fen.push(`${emptySquares}`);
    row !== 7 && fen.push('/');
  }
  return fen.join();
}