import { useState } from "react";
import React from "react";

function Square({ value, setSquare }) {
  return (
    <button className="square" onClick={setSquare}>
      {value}
    </button>
  );
}


function Board({oIsNext, squares, onPlay}) {
  function handleClick(i) {
    if (squares[i] || calculateWinner(squares)){
      return;
    }
    const nextSquares = squares.slice();
    if (oIsNext) {
      nextSquares[i] = "O";
    } else {
      nextSquares[i] = "X";
    }
    onPlay(nextSquares);
  }
  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else if (squares.every((square) => square)) {
    status = "Draw";
  } else {
    status = "Next player: " + (oIsNext ? "O" : "X");
  }
  let buttons = [];
  let row = [];
  for (let index = 0; index <= 9; index++) {
    if (index % 3 === 0) {
      buttons.push(
        <div className="board-row" key={index}>
          {row}
        </div>
      );
      row = [];
    }
    row.push(
      <Square
        key={index}
        value={squares[index]}
        setSquare={() => handleClick(index)}
      />
    );
  }
  return (
    <>
      <div className="status">{status}</div>
      {buttons}
    </>
  );
}


export default function Game(){
  const [oIsNext, setOIsNext] = useState(true);
  const [history, setHistory] = useState([Array(9).fill(null)]); // [squares, squares, squares, ...
  const [currMove, setCurrMove] = useState(0);
  const currSquares = history[currMove];
  const moves = history.map((squares, move) => {
    let description;
    if (move == 0){
      description = 'go to start';
    } else {
      description = 'go to move# ' + move;
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    )
  });
  function handlePlay(squares){
    // const newHistory = history.slice();
    // newHistory.push(squares);
    // setHistory(newHistory);
    setHistory([...history.slice(0, currMove + 1), squares]); // same as above
    // Beware, the setHistory does not work directly bec it is React code. I think react sets all the history
    setCurrMove(currMove + 1); // maybe just add a one?
    setOIsNext(!oIsNext);
  }
  function jumpTo(move) {
    setCurrMove(move);
    setOIsNext(move % 2 == 0);
  }
  return (
    <div className="game">
      <div className="game-board">
        <Board oIsNext={oIsNext} squares={currSquares} onPlay={handlePlay} />
      </div>
      <div>
        <ul>
          {moves}
        </ul>
      </div>
    </div>
  );
}


function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
