
// asset imports 
import P from "./images/white_pawn.png";
import N from "./images/white_knight.png";
import B from "./images/white_bishop.png";
import K from "./images/white_king.png";
import Q from "./images/white_queen.png";
import R from "./images/white_rook.png";
import p from "./images/black_pawn.png";
import n from "./images/black_knight.png";
import b from "./images/black_bishop.png";
import k from "./images/black_king.png";
import q from "./images/black_queen.png";
import r from "./images/black_rook.png";

const BOARDSIZE = 8;
const pieceMapping = { P, N, B, K, Q, R, p, n, b, k, q, r };

function Tile({ piece, position, handleClick, highlight }) {

  return (
    <div 
      id={`${position[0]},${position[1]}`} 
      className={`tile ${(row + col) % 2 ? "light" : "dark"} ${highlight ? "highlight" : ""}`} 
      onClick={() => handleClick(piece, position)}
    >
      {piece && <img src={pieceMapping[piece]} alt={`piece at ${position}`} />}
    </div>
  );
}

export default function Board({ pieces, onTileClick, highlightedSquares }) {

  return (
    <div className="chessboard">
      {pieces.map((piece, index) => {
        let row = Math.floor(index / BOARDSIZE);
        let col = index % BOARDSIZE;
        return (
          <Tile key={index} handleClick={onTileClick} piece={piece} position={[row, col]} highlight={
            highlightedSquares.includes([row, col])
          } />
        )
      })}
    </div>
  )
}
