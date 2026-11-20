const gameBoard = document.querySelector("#gameBoard");
const ctx = gameBoard.getContext("2d");
const scoreText = document.querySelector("#score");
const gamesText = document.querySelector("#games")
const hidemeDiv = document.getElementById("hideme")
const highscoreText = document.querySelector("#highscore");
const gameWidth = gameBoard.width;
const gameHeight = gameBoard.height;
const boardBackground = "white";
const snakeColor = "lightgreen";
const snakeBorder = "black";
const foodColor = "red";
const unitSize = 20;
let foodX;
let foodY;
let score = 0;
let game_score = 0;
let snake = [];
let num_trainings = 0;
let games = 0;
let running = false;

const socket = io();

ctx.font = "35px Quicksand";
ctx.fillStyle = "black";
ctx.textAlign = "center";
ctx.fillText("training arena", gameWidth / 2, gameHeight / 2);

hidemeDiv.style.display = "none";
//triggers when train button is clicked, sends call to train event that begins training
document.getElementById("btn-train").addEventListener("click", function () {
    if (!running) {
        running = true;
        let food = document.getElementById("food").value;
        let alive = document.getElementById("alive").value;
        let die = document.getElementById("die").value;
        if (food == "" || alive == "" || die == "") {
            running = false;
        }
        else {
            socket.emit("train", food, alive, die);
            hidemeDiv.style.display = "block";
        }
    }

})

document.getElementById("btn-off").addEventListener("click", function () {
    running = false;
})

function updateRunning() {
    if (games > 98) {
        running = false;
        ctx.font = "35px Quicksand";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText("training concluded", gameWidth / 2, gameHeight / 2);
    }
    else {
        running = true;
    }
}

//subscriber to training data
socket.on("snake_data", function (data, callback) {
    clearBoard();
    foodX = data["data"]["apple"]["x"];
    foodY = data["data"]["apple"]["y"];
    snake = data["data"]["snake"];
    games = data["data"]["stats"]["games"];
    score = data["data"]["stats"]["score"];
    game_score = data["data"]["stats"]["record"];
    drawFood();
    drawSnake();
    drawStats();
    console.log("running: " + running)
    if (running) {
    }
    else {
        games = 0
        clearBoard();
        ctx.font = "35px Quicksand";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText("training concluded", gameWidth / 2, gameHeight / 2);
        return callback(false)
    }
    updateRunning();
})

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

function drawStats() {
    scoreText.textContent = score;
    highscoreText.textContent = game_score;
    if (games == 1000) {
        gamesText.textContent = "0/100"
    }
    else {
        gamesText.textContent = games + "/100"
    }
}
