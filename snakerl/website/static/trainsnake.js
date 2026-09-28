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
let gameScore = 0;
let snake = [];
let numTrainings = 0;
let games = 0;
let running = false;

const socket = io();

hidemeDiv.style.display = "none";

/* Draw messages on game canvas */

const messageFont = `35px ${getComputedStyle(document.body).fontFamily}`;

function drawMessage(text) {
    ctx.font = messageFont;
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText(text, gameWidth / 2, gameHeight / 2);
}

document.fonts.load(messageFont)
    .catch(() => { })
    .then(() => drawMessage("training arena"));

/* Update the output element's value according to the slider value */

function updateDisplayOutput(inputEvent) {
    const trainingOutput = document.querySelector(`output[for="${inputEvent.target.id}"]`);
    trainingOutput.value = inputEvent.target.value;
}

const trainingInputElements = document.getElementById("training-sliders").querySelectorAll("input[type=range]");
trainingInputElements.forEach((trainingInputElement) => {
    trainingInputElement.addEventListener("input", updateDisplayOutput);
    trainingInputElement.dispatchEvent(new Event("input"));
})

/* call training when "train" button clicked */
document.getElementById("trainBtn").addEventListener("click", function () {
    if (!running) {
        running = true;
        const trainingInputValues = Object.fromEntries(
            Array.from(trainingInputElements, (slider) => [slider.id, slider.value])
        );
        socket.emit("train", trainingInputValues);
        hidemeDiv.style.display = "block";
    }

})

document.getElementById("offBtn").addEventListener("click", function () {
    running = false;
})

function updateRunning() {
    if (games > 98) {
        running = false;
        drawMessage("training concluded");
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
    gameScore = data["data"]["stats"]["record"];
    drawFood();
    drawSnake();
    drawStats();
    console.log("running: " + running)
    if (running) {
    }
    else {
        games = 0
        clearBoard();
        drawMessage("training concluded");
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
    highscoreText.textContent = gameScore;
    if (games == 1000) {
        gamesText.textContent = "0/100"
    }
    else {
        gamesText.textContent = games + "/100"
    }
}
