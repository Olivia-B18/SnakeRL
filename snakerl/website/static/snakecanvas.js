/*
JavaScript functions and variables shared across
all pages that display a snake game board.
*/

/* CONSTANTS */

// Game board
const gameBoard = document.querySelector("#gameBoard");
const gameWidth = gameBoard.width;
const gameHeight = gameBoard.height;
const ctx = gameBoard.getContext("2d");

// Game colors and "pixel" size
const boardBackground = "white";
const snakeColor = "lightgreen";
const snakeBorder = "black";
const foodColor = "red";
const unitSize = 20;

// Load text font
const messageFont = `35px ${getComputedStyle(document.body).fontFamily}`;

// Location of food and snake
let foodX;
let foodY;

/* FUNCTIONS TO CLEAR AND DRAW ON CANVAS */

function clearBoard() {
    ctx.fillStyle = boardBackground;
    ctx.fillRect(0, 0, gameWidth, gameHeight);
};

function drawFood() {
    ctx.fillStyle = foodColor;
    ctx.fillRect(foodX, foodY, unitSize, unitSize);
};

function drawSnake() {
    ctx.fillStyle = snakeColor;
    ctx.strokeStyle = snakeBorder;
    snake.forEach(snakePart => {
        ctx.fillRect(snakePart.x, snakePart.y, unitSize, unitSize);
        ctx.strokeRect(snakePart.x, snakePart.y, unitSize, unitSize);
    })
};

function drawMessage(text, posX, posY) {
    ctx.font = messageFont;
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText(text, posX, posY);
}
