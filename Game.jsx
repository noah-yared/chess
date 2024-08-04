import React, { useState } from 'react';
import Board from './Board.jsx';
import { getMoveData, processMoveData } from './moveValidator.js';
import { FENToBoard, BoardToFEN } from './utils.js'

const firstRank = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'];
const initialPieces = [
  ...firstRank,
  ...Array(8).fill('p'),
  ...Array(32).fill(null),
  ...Array(8).fill('P'),
  ...firstRank.map(piece => piece.toUpperCase())
];
const boardFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';

export default async function Game (){

  const [isWhitesTurn, setIsWhitesTurn] = useState(true);
  const [boardHistory, setBoardHistory] = useState([initialPieces]);
  const [FENHistory, setFENHistory] = useState([boardFEN])
  const [capturedPiecesHistory, setCapturedPiecesHistory] = useState([[]]);
  const [clickedSquare, setClickedSquare] = useState(null);
  
  const currentPieces = boardHistory[boardHistory.length - 1];
  const currentFEN = boardFENHistory[boardFENHistory.length - 1];

  const updateBoard = newBoard => setBoardHistory(...boardHistory, newBoard);
  const updateFEN = newFEN => setFENHistory(...FENHistory, newFEN);
  const updateCapturedPieces =  setCapturedPiecesHistory()

  async function onTileClick(piece, newSquare) {
    let candidateMoveMade = false;
    if (piece) {
      let isPieceWhite = piece === piece.toUpperCase();
      candidateMoveMade ||= clickedSquare && (isPieceWhite !== isWhitesTurn);
      !clickedSquare && (isPieceWhite === isWhitesTurn) && setClickedSquare(newSquare);
    } else {
      candidateMoveMade ||= clickedSquare;
    }
    if (candidateMoveMade) {
      try {
        let moveData = await getMoveData([currentFEN, [clickedSquare, newSquare]]);
        await processMoveData(moveData, [clickedSquare, newSquare], updateFEN, );
      } catch (error) {
        console.error(error)
      }
    }
    clickedSquare && clickedSquare !== newSquare && setClickedSquare(null);
  }
}