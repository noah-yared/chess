const startGame = async () => {
  let move = null;
  let startSquare = null;
  let startSquareElement = null;
  let endSquareElement = null;
  let isProcessingMove = false;
  let hasUserChosenPromotionPiece = false;

  const boardTiles = document.getElementsByClassName("square");
  const promotionPieces = window.gameType === "sockets" 
    ? document.querySelectorAll(`#promotion-options-${window.playerColor} > .promotion-piece`) 
    : document.getElementsByClassName("promotion-piece");

  const darkColor = getComputedStyle(boardTiles[0]).backgroundColor;
  const lightColor = getComputedStyle(boardTiles[1]).backgroundColor;

  let boardFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqKQ -";

  let moves = []
  let board_states = [boardFEN];

  window.promotionPieceElement = null;

  window.move = null;


  // document.addEventListener("click", (e) => {
  //   console.log("Click! Location is: ", e.pageX, e.pageY);
  //   console.log(getBoardCoordinates(e.pageX, e.pageY))
  // })

  for (let promotionPiece of promotionPieces) {
    promotionPiece.addEventListener("click", () => {
      console.log(window.move);
      let pawnToPromote = document.querySelector(`.square:nth-child(${getIndex(window.move[1]) + 1})`);
      pawnToPromote.innerHTML = promotionPiece.innerHTML;
      window.promotionPieceElement = promotionPiece.innerHTML; // store promotionPiece.innerHTML in global var
      console.log("FEN before update:", boardFEN);
      console.log("piece type", promotionPiece.id);
      updatePromotedPawnFEN(window.move, promotionPiece.id); // NEED TO IMPLEMENT 
      console.log("updated FEN:", boardFEN)
      let color = window.move[1][0] === 0 ? "white" : "black";
      let promotionOptionsGrid = document.getElementById(`promotion-options-${color}`);
      promotionOptionsGrid.style.display = "none";
      hasUserChosenPromotionPiece = true;
    })
  }

  for (let tile of boardTiles) {
    tile.addEventListener("click", async e => {
      if (isProcessingMove || (window.gameType == "sockets" && !window.isPlayersTurn)) return;
      // console.log(tile);
      let newSquare = getBoardCoordinates(e.pageX, e.pageY);
      if (!startSquare && tile.querySelectorAll("img").length) {
        if (window.gameType === "sockets" && !tile.querySelector("img").src.includes(window.playerColor)) {
          console.log("cant move this piece");
          return;
        }
        startSquare = newSquare;
        startSquareElement = tile;
        toggleSquareColor(startSquareElement, startSquare); // highlight square
      } else if (startSquare) {
        move = [startSquare, newSquare];
        console.log(move);
        endSquareElement = tile;
        toggleSquareColor(startSquareElement, startSquare); // de-highlight square
      }
      if (move) {
        isProcessingMove = true;
        await handleMove(move, startSquareElement, endSquareElement);
        move = null
      }
    })
  }

  const handleMove = async (playerMoveInfo, startSquareElement, endSquareElement) => {
    let moveMade = false, playerMove;
    if (window.gameType === "sockets") {
      playerMove = window.isPlayersTurn ? playerMoveInfo : playerMoveInfo.move;
    } else {
      playerMove = playerMoveInfo
    }
    window.move = playerMove;
    validateMove(playerMove)
    .then(async result => {
      console.log("Is move valid?", result["valid"])
      if (result["valid"]) {
        moveMade = true; 
        makeMove(startSquareElement, endSquareElement)
        boardFEN = result.fen;
        console.log("Board state", boardFEN)
        moves.push(playerMove); // push move into list of moves
        board_states.push(boardFEN); // store board state
        if (result["enpassant"]) {
          handleEnpassantMove(playerMove);
        } else if (result["castled"]) {
          handleCastledMove(playerMove);
        } else if (result["promotion"]) {
          if (window.gameType !== "sockets" || window.isPlayersTurn) {
            hasUserChosenPromotionPiece = false;
            handlePawnPromotion(playerMove);
            await pollHasUserChosenPromotionPiece();
          } else {
            displayOpponentPromotion(playerMoveInfo)
          }
        }
        if (window.gameType === "sockets" && window.isPlayersTurn) {
          window.socket.emit("move", { "move": playerMove, "promotionPiece": window.promotionPieceElement });
          window.promotionPieceElement = null;
        }
      } 
    })
    .catch(err => console.error(`Something went wrong with move validation. Here is the error: ${err}`))
    .finally(() => {
      move = null;
      startSquare = null;
      startSquareElement = null;
      endSquareElement = null;
      isProcessingMove = false;
      if (moveMade) window.isPlayersTurn = !window.isPlayersTurn;
    })
  }

  const validateMove = async (move) => {
    console.log(`Validating ${move}`);
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
    let color = move[1][0] === 0 ? "white" : "black";
    let promotionOptionsElement = document.getElementById(`promotion-options-${color}`);
    promotionOptionsElement.style.display = "grid"; 
    promotionOptionsElement.style.position = "absolute";
    let finalSquareRect = document.querySelector(`.square:nth-child(${pawnFinalIndex + 1})`).getBoundingClientRect();
    console.log(finalSquareRect);
    let width = promotionOptionsElement.offsetWidth;
    if (move[1][1] < 4) {
      promotionOptionsElement.style.left = `${finalSquareRect.left + window.scrollX}px`;
    } else {
      promotionOptionsElement.style.left = `${finalSquareRect.right + window.scrollX - width}px`; 
    }
    let height = promotionOptionsElement.offsetHeight;
    if (move[1][0] === 0) {
      promotionOptionsElement.style.top = `${finalSquareRect.bottom + window.scrollY}px`;
    } else {
      promotionOptionsElement.style.top = `${finalSquareRect.top + window.scrollY - height}px`;
    }
    // console.log('Computed Style:', getComputedStyle(promotionOptionsElement));
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

  // const pollHasOpponentChosenPromotionPiece = async () => {
  //   while (!window.promotionPieceElement !== null) {
  //     await new Promise ((resolve) => setTimeout(resolve, 100));
  //   }
  // }

  const displayOpponentPromotion = (playerMoveInfo) => {
    let promotionSquareElement = document.querySelector(`.square:nth-child(${getIndex(playerMoveInfo.move[1]) + 1})`);
    promotionSquareElement.innerHTML = playerMoveInfo.promotionPiece;
  }

  const updatePromotedPawnFEN = (move, piece_type) => {
    console.log("piece to replace with:", piece_type);
    console.log(move);
    let colIndex = 0, pawnColIndex = move[1][1];
    if (move[1][0] === 0) {
      // iterate until we get to first backwards slash
      let i = 0;
      while (boardFEN[i] != '/') {
        if (colIndex === pawnColIndex) {
          boardFEN = boardFEN.substring(0, i) + piece_type + boardFEN.substring(i+1);
          console.log(boardFEN[i]);
          break; // just need to replace piece
        } 
        if (!isNaN(Number(boardFEN[i]))) {
          colIndex += Number(boardFEN[i]);
        } else{
          colIndex++;
        }
        i++;
      }
    } else {
      // find index of last backwards slash and iterate until first space
      let i = boardFEN.lastIndexOf('/') + 1;
      while (boardFEN[i] != ' ') {
        if (colIndex === pawnColIndex) {
          boardFEN = boardFEN.substring(0, i) + piece_type + boardFEN.substring(i+1);
          console.log(boardFEN[i]);
          break;
        }
        if (!isNaN(Number(boardFEN[i]))) {
          colIndex += Number(boardFEN[i]);
        } else {
          colIndex++;
        }
        i++;
      }
    }
  }
  if (window.gameType === "sockets") {
    window.socket.on("displayMove", async playerMoveInfo => {
      console.log("displaying move!");
      let startSquareElement = document.querySelector(`.square:nth-child(${getIndex(playerMoveInfo.move[0]) + 1})`);
      let endSquareElement = document.querySelector(`.square:nth-child(${getIndex(playerMoveInfo.move[1]) + 1})`);
      await handleMove(playerMoveInfo, startSquareElement, endSquareElement);
    });
  }
}

  const pollSocketConnected = async () => {
    while (!window.socket.connected) {
      await new Promise((resolve) => {
        setTimeout(resolve, 100);
      });
    }
  }

const main = async () => {
  if (window.gameType === "sockets") {
    window.socket.on("startGame", async () => {
      try {
        await pollSocketConnected();
        await startGame();
        console.log("game started!")
      } catch (error) {
        console.error(error);
      } finally {
        console.log("End of promise chain!")
      }
    });
  } else {
    console.log("not sockets");
    try {
      await startGame();
    } catch (error) {
      console.error(error);
    } finally {
      console.log("End of promise chain!");
    }
  }
}

main();
