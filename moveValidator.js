export async function getMoveData(boardFEN, move /* Expecting [row, col] format */) {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/validate-move", {
      "method": "POST",
      "headers": {
        Accept: "application/json",
        "Content-type": "application/json"
      },
      "body": JSON.stringify({
        "board": boardFEN,
        "move": move
      })
    })
    const data = await res.json();
    return data;
  } catch (error) {
    throw new Error("Error with move validation:", error)
  }
}

export async function processMoveData(moveData, move) {
  if (!moveData["valid"]) return; // move is invalid
    
  moveData["valid"] && makeMove(move);
  if (moveData["castle"]) {
    handleCastle(move);
  }
  moveData["check"] && handleCheck(moveData["oppKing"]);
  moveData["checkmate"] && handleCastle(move);
  moveData[""]
}
