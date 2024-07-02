let move = null;
let startSquare = null;
let startSquareElement = null;
let endSquareElement = null;
let isProcessingMove = false;
let hasUserChosenPromotionPiece = false;

const boardTiles = document.getElementsByClassName("square");
const promotionPieces = document.getElementsByClassName("promotion-piece");

const darkColor = getComputedStyle(boardTiles[0]).backgroundColor;
const lightColor = getComputedStyle(boardTiles[1]).backgroundColor;

let boardFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqKQ -";

let moves = []
let board_states = [boardFEN];

console.log(boardTiles[0].getBoundingClientRect().top)

document.addEventListener("click", (e) => {
  console.log("Click! Location is: ", e.pageX, e.pageY);
  console.log(getBoardCoordinates(e.pageX, e.pageY))
})

for (let promotionPiece of promotionPieces) {
  promotionPiece.addEventListener("click", (move) => {
    let pawnToPromote = document.querySelector(`.square:nth-child(${getIndex(move) + 1})`);
    pawnToPromote.innerHTML = promotionPiece.innerHTML;
    updatePromotedPawnFEN(move, promotionPiece.id); // NEED TO IMPLEMENT 
    let promotionOptionsGrid = document.getElementById("promotion-options");
    promotionOptionsGrid.style.display = "none";
    hasUserChosenPromotionPiece = true;
  })
}

for (let tile of boardTiles) {
  tile.addEventListener("click", async e => {
    if (isProcessingMove) return;
    console.log(tile);
    let newSquare = getBoardCoordinates(e.pageX, e.pageY);
    if (!startSquare && tile.querySelectorAll("img").length) {
      startSquare = newSquare;
      startSquareElement = tile;
      toggleSquareColor(startSquareElement, startSquare); // highlight square
    } else if (startSquare) {
      move = [startSquare, newSquare];
      endSquareElement = tile;
      toggleSquareColor(startSquareElement, startSquare); // de-highlight square
    }
    if (move) {
      isProcessingMove = true;
      validateMove(move)
        .then(async result => {
          console.log("Is move valid?", result["valid"])
          if (result["valid"]) {
            makeMove(startSquareElement, endSquareElement)
            if (result["enpassant"]) {
              handleEnpassantMove(move);
            } else if (result["castled"]) {
              handleCastledMove(move);
            } else if (result["promotion"]) {
              hasUserChosenPromotionPiece = false;
              handlePawnPromotion(move);
              await pollHasUserChosenPromotionPiece();
            }
            boardFEN = result.fen;
            console.log("Board state", boardFEN)
            moves.push(move); // push move into list of moves
            board_states.push(boardFEN); // store board state
          } 
        })
        .catch(err => console.error(`Something went wrong with move validation. Here is the error: ${err}`))
        .finally(() => {
          move = null;
          startSquare = null;
          startSquareElement = null;
          endSquareElement = null;
          isProcessingMove = false;
        })
    }
  })
}


const validateMove = async (move) => {
  console.log(move);
  return fetch('http://127.0.0.1:5000/validate-move', {
    "method": "POST",
    "headers": {
      Accept: "application/json",
      "Content-Type": "application/json"
    }, 
    "body": JSON.stringify({
      "board": boardFEN,
      "move": move
    })
  })
    .then(response => response.json())
    .catch(err => {throw err})
}

const makeMove = (startTile, endTile) => {
  console.log(startTile, '\n' , endTile)
  endTile.innerHTML = startTile.innerHTML;
  startTile.innerHTML = "";
}

const handleEnpassantMove = (move) => {
  let capturedPieceIndex = move[1][0] === 2 ? getIndex([3, move[1][1]]) : getIndex([4, move[1][1]]);
  let capturedPiece = document.querySelector(`.square:nth-child(${capturedPieceIndex+1})`);
  capturedPiece.innerHTML = "";
}

const handleCastledMove = (move) => {
  let rookInitialIndex = getIndex([move[0][0], move[1][1] - move[0][1] > 0 ? 7 : 0])
  let rookFinalIndex = getIndex([move[0][0], rookInitialIndex % 8 === 7 ? 5 : 3])
  let rookInitialSquare = document.querySelector(`.square:nth-child(${rookInitialIndex + 1})`);
  let rookFinalSquare = document.querySelector(`.square:nth-child(${rookFinalIndex + 1})`);
  rookFinalSquare.innerHTML = rookInitialSquare.innerHTML;
  rookInitialSquare.innerHTML = "";
}

const handlePawnPromotion = (move) => {
  let pawnFinalIndex = getIndex(move[1]);
  let promotionOptionsElement = document.getElementById("promotion-options");
  promotionOptionsElement.style.display = "grid"; 
  promotionOptionsElement.style.position = "absolute";
  let finalSquareRect = document.querySelector(`square:nth-child(${pawnFinalIndex + 1})`);
  if (move[1][1] < 4) {
    promotionOptionsElement.style.left = `${finalSquareRect.left}`;
  } else {
    promotionOptionsElement.style.right = `${finalSquareRect.right}`;  
  }
  if (move[1][0] === 0) {
    promotionOptionsElement.style.top = `${finalSquareRect.bottom}`;
  } else {
    promotionOptionsElement.style.bottom = `${finalSquareRect.top}`;
  }
}

const getIndex = (square) => {
  return 8*square[0] + square[1];
}

const toggleSquareColor = (tileElement, coordinates) => {
  if (tileElement.style.backgroundColor === "yellow") {
    tileElement.style.backgroundColor = (coordinates[0] + coordinates[1]) % 2 == 1 ? lightColor : darkColor;
  } else {
    tileElement.style.backgroundColor = "yellow";
  }
}

const getBoardCoordinates = (x, y) => {
  const tileSize = 75;
  let rect = boardTiles[0].getBoundingClientRect()
  let boardX = rect.left + window.scrollX;
  let boardY = rect.top + window.scrollY;
  return [Math.floor((y - boardY) / tileSize), Math.floor((x - boardX) / tileSize)];
}

const pollHasUserChosenPromotionPiece = async () => {
  while (!hasUserChosenPromotionPiece) {
    await new Promise((resolve) => {
      setTimeout(resolve, 100);
    });
  }
}

const updatePromotedPawnFEN = (move, piece_type) => {
  throw new Error("Function not implemented.")
}
