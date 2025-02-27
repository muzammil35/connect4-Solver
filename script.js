const rows = 6;
const cols = 7;
let board = [];
let playerTurn = false;
let gameOver = false;  // Flag to track if the game is over

function initGame() {
  board = Array(rows).fill(null).map(() => Array(cols).fill(0));
  const boardDiv = document.getElementById("board");
  boardDiv.innerHTML = "";
  document.getElementById("message").textContent = "Player 1's turn";
  
  for (let i = 0; i < rows * cols; i++) {
    const cell = document.createElement("div");
    cell.classList.add("cell");
    cell.dataset.row = Math.floor(i / cols);
    cell.dataset.col = i % cols;
    cell.addEventListener("click", handleCellClick);
    boardDiv.appendChild(cell);
  }
}

function handleCellClick(e) {

  if (playerTurn) {
    const col = e.target.dataset.col;
    for (let row = rows - 1; row >= 0; row--) {
      if (board[row][col] === 0) {
        board[row][col] = currentPlayer;
        const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        cell.classList.add(currentPlayer === 1 ? "player1" : "player2");
    }
  }
  }
}

initGame();
gameLoop();

async function gameLoop() {
  // 1. Fetch next move for AI before player's turn
  await makeAIMove();
  playerTurn = true;

  // 2. Wait for player to make a move before continuing the loop
  
  // The player's move is handled by handlePlayerMove function
}

