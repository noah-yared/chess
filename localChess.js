document.body.addEventListener("click", (e) => {
  console.log(`${e.pageX}, ${e.pageY}`);
})

var isWhitesTurn = true;
var numCapturedWhitePieces = 0, numCapturedBlackPieces = 0;
const elements = document.getElementsByClassName("square");
const darkColor = elements[0].style.color;
const lightColor = elements[1].style.color;

const allowMoves = () => {

  const getCoordinates = (x,y) => {
    const rect = document.getElementById("chessboard").getBoundingClientRect(); 
    const rectX = rect.left+4+window.scrollX, rectY = rect.top+4+window.scrollY;
    return [Math.floor((y-rectY)/75), Math.floor((x-rectX)/75)];
  }

  var startElement = null;
  var startSquare = null;
  var move = null;
  var isProcessingMove = false;

  for (let element of elements){
    element.addEventListener("click", function(e){
      if (isProcessingMove){
        return;
      }
      let coordinates = getCoordinates(e.pageX, e.pageY);
      const imageElement = this.querySelector("img");
      if (this.style.backgroundColor != "yellow") {
        console.log("target square background color is not yellow");
        console.log(`target element is ${this}`);
        if (startSquare) {
          console.log("start square is defined")
          move = [startSquare, coordinates];
          isProcessingMove = true;
        } else if (imageElement){ 
          console.log("image element is present in target");
          startSquare = coordinates;
          startElement = this;
          this.style.backgroundColor = "yellow";
        }
      } else{
        if ((coordinates[0] + coordinates[1]) % 2 === 1){ 
          this.style.backgroundColor = darkColor;
        } else {
          this.style.backgroundColor = lightColor;
        }
        startElement=null; startSquare=null;
      } 
      if (move){
        console.log(`The move to be checked is ${move}`);
        // validate move, then do the following if valid:
        validateMove(move)
          .then(valid => {
            console.log(valid);
            if (valid){
              console.log("valid");
              makeMove(startSquare, startElement, this);
              pauseTimer(isWhitesTurn);
              startTimer(!isWhitesTurn);
              isWhitesTurn = !isWhitesTurn;
            } 
            move = null;
            startSquare = null;
            startElement = null;
          })
          .catch(err => {
            console.log(`Error: ${err}`);
          })
        console.log("resetting color of highlighted square");
        resetSquareColor(startSquare, startElement);
        isProcessingMove = false;
      }
    });
  };
};

const makeMove = (startSquare, startElement, endElement) => {
  console.log("making move...")
  // if ((startSquare[0] + startSquare[1]) % 2 == 0) {
  //   startElement.style.backgroundColor = darkColor;
  // } else {
  //   startElement.style.backgroundColor = lightColor;
  // }
  const piece = startElement.querySelector("img");
  const endImageElement = endElement.querySelector("img");
  startElement.removeChild(piece);
  if (endImageElement) {
    endImageElement.src = piece.src;
  } else {
    endElement.appendChild(piece);
  }
}

const startGameButton = document.getElementById("start-game");
startGameButton.addEventListener("click", e => {
  // disable form inputs
  e.preventDefault();
  console.log("submit clicked!");
  const form = document.getElementById("form");
  const timeControlElement = form.querySelector("#time");
  const whiteNameElement = form.querySelector("#white-name");
  const blackNameElement = form.querySelector("#black-name");
  // timeControlElement.setAttribute("disabled", "true");
  // whiteNameElement.setAttribute("disabled", "true");
  // blackNameElement.setAttribute("disabled", "true");
  // form.querySelector("button").setAttribute("disabled", "true");
  document.getElementById("game-settings").removeChild(form);
  // compile user input
  const time = Number(timeControlElement.value);
  const whiteName = whiteNameElement.value;
  const blackName = blackNameElement.value;
  console.log(`${time}, ${whiteName}, ${blackName}`);
  // start game - add captured pieces columns and add clocks 
  startGame(time, whiteName, blackName);
})

var whiteMinutesLeft, blackMinutesLeft, whiteSecondsLeft = 0, blackSecondsLeft = 0;

const startGame = (time, whiteName, blackName) => {
  whiteMinutesLeft = time, blackMinutesLeft = time;
  setupTimers(time);
  allowMoves();
  displayName(whiteName, blackName);
};

const updateClock = () => {
  console.log("Updating clock!");
  let timeOut = false;
  if (isWhitesTurn) {
    if (whiteSecondsLeft) {
      whiteSecondsLeft--;
    } else if (whiteMinutesLeft) {
      whiteMinutesLeft--;
      whiteSecondsLeft = 59;
    } else{
      timeOut = true;
    }
  } else {
    if (blackSecondsLeft) {
      blackSecondsLeft--;
    } else if (blackMinutesLeft) {
      blackMinutesLeft--;
      blackSecondsLeft = 59;
    } else {
      timeOut = true;
    }
  }
  displayTimer(isWhitesTurn);
  if (timeOut){
    endGame();
  }
};

const setupTimers = (timeControl) => {
  if (Number(timeControl)) {
    const rect = document.getElementById("chessboard").getBoundingClientRect();
    const whiteTimeElement = document.getElementById("white-clock");
    const blackTimeElement = document.getElementById("black-clock");

    blackTimeElement.innerHTML = `${String(timeControl).padStart(2,"0")}:00`;
    blackTimeElement.style.margin = "0";
    blackTimeElement.style.opacity = "0.5";
    blackTimeElement.style.position = "absolute";
    blackTimeElement.style.top = `${rect.top - blackTimeElement.offsetHeight + window.scrollY}px`;
    blackTimeElement.style.left = `${rect.right - blackTimeElement.offsetWidth + window.scrollX}px`;

    whiteTimeElement.innerHTML = `${String(timeControl).padStart(2,"0")}:00`;
    whiteTimeElement.style.margin = "0";
    whiteTimeElement.style.position = "absolute";
    whiteTimeElement.style.top = `${rect.bottom + window.scrollY}px`;
    whiteTimeElement.style.left = `${rect.right - whiteTimeElement.offsetWidth + window.scrollX}px`;

    setInterval(updateClock, 1000);
  }
}

const pauseTimer = (isWhite) => {
  if (isWhite) {
    document.getElementById("white-clock").style.opacity = "0.5";
  } else {
    document.getElementById("black-clock").style.opacity = "0.5";
  }
}

const startTimer = (isWhite) => {
  if (isWhite){
    document.getElementById("white-clock").style.opacity = "1";
  } else{
    document.getElementById("black-clock").style.opacity = "1";
  }
}

const endGame = () => {
  return null;
};

const displayTimer = (isWhite) => {
  if (isWhite){
    document.getElementById("white-clock").innerHTML = `${String(whiteMinutesLeft).padStart(2,"0")}:${String(whiteSecondsLeft).padStart(2,"0")}`;
  } else{
    document.getElementById("black-clock").innerHTML = `${String(blackMinutesLeft).padStart(2,"0")}:${String(blackSecondsLeft).padStart(2,"0")}`;
  }  
};

const displayName = (whiteName, blackName) => {
  if (!whiteName){
    whiteName = "White";
  }
  if (!blackName){
    blackName = "Black";
  }
  const rect = document.getElementById("chessboard").getBoundingClientRect();
  const blackNameElement = document.createElement("p");
  const whiteNameElement = document.createElement("p");
  const namesElement = document.getElementById("names");

  console.log(`left: ${rect.left}, top: ${rect.top}, bottom: ${rect.bottom}`);

  blackNameElement.setAttribute("class", "player-names");
  blackNameElement.innerHTML = blackName;
  blackNameElement.style.margin = "0";
  blackNameElement.style.padding = "0";
  blackNameElement.style.position = "absolute";
  blackNameElement.style.left = `${rect.left + window.scrollX}px`;
  console.log(blackNameElement.style.left);
  setTimeout(() => {
    blackNameElement.style.top = `${rect.top - blackNameElement.offsetHeight + window.scrollY}px`;
  },0);
  blackNameElement.style.fontSize = "20px";
  blackNameElement.style.padding = "2px";
  
  whiteNameElement.setAttribute("class", "player-names");
  whiteNameElement.innerHTML = whiteName;
  whiteNameElement.style.margin = "0";
  whiteNameElement.style.padding = "0";
  whiteNameElement.style.position = "absolute";
  whiteNameElement.style.left = `${rect.left + window.scrollX}px`;
  whiteNameElement.style.top = `${rect.bottom + window.scrollY}px`;
  whiteNameElement.style.fontSize = "20px";
  setTimeout(() => {
    whiteNameElement.style.padding = "2px";
  }, 0);

  namesElement.appendChild(blackNameElement);
  namesElement.appendChild(whiteNameElement);
};

const themeElement = document.getElementById("theme");
const lightMode = "rgb(250, 243, 224)";
const darkMode = "rgb(44, 44, 44)";
themeElement.addEventListener("click", () => {
  if (getComputedStyle(document.body).backgroundColor == lightMode){
    console.log("currenly light theme, switching to dark");
    document.body.style.backgroundColor = darkMode;
    for (let element of document.getElementsByClassName("player-names")) {
      element.style.color = "white";
    }
    document.getElementById("names").style.color = "white";
    if (document.getElementById("form")){
      document.getElementById("form").style.color = "white";
    }
    document.getElementById("black-clock").style.color = "white";
    document.getElementById("white-clock").style.color = "white";
  } else {
    console.log("currently dark theme, switching to light");
    document.body.style.backgroundColor = lightMode;
    for (let element of document.getElementsByClassName("player-names")) {
      element.style.color = "black";
    }
    document.getElementById("names").style.color = "black";
    if (document.getElementById("form")) {
      document.getElementById("form").style.color = "black";
    }
    document.getElementById("black-clock").style.color = "black";
    document.getElementById("white-clock").style.color = "black";
  }
});

const resetSquareColor = (square, element) => {
  if ((square[0] + square[1])%2 == 1) {
    element.style.backgroundColor = lightColor;
  } else {
    element.style.backgroundColor = darkColor
  }
}


const validateMove = async (move) => {
  console.log("Fetching...");
  console.log(move);
  return fetch("http://127.0.0.1:5000/validate_move", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-type": "application/json" 
    },
    body: JSON.stringify(move)
  })
    .then(response => response.json())
    .then(result => {
      console.log("valid attribute of json response", result["valid"]);
      return result["valid"];
    })
    .catch(err => {
      console.error(err);
      throw err;
    });
} 