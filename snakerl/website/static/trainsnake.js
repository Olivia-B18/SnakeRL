/* 
JavaScript for the training page.
*/

/* CONSTANTS AND VARIABLES */

// Sidebar to show/hide
const hideTrainingSidebarDiv = document.getElementById("hideTrainingSidebar")

// HTML text for training stats
const scoreText = document.querySelector("#score");
const gamesText = document.querySelector("#games")
const highscoreText = document.querySelector("#highscore");

// Slider elements
const trainingInputElements = document.getElementById("training-sliders").querySelectorAll("input[type=range]");

// Connection to the server
const socket = io();

// Values training stats
let score = 0;
let gameScore = 0;
let games = 0;
let numTrainings = 0;

// The snake
snake = []

// Flags for if training is in progress
let running = false;
let stopRequested = false;

/* SET UP TRAINING ARENA */

// Hide sidebar
hideTrainingSidebarDiv.style.display = "none";

// Draw message to canvas
document.fonts.load(messageFont)
    .catch(() => { })
    .then(() => drawMessage("training arena", gameWidth / 2, gameHeight / 2));

/* JAVASCRIPT FOR SLIDERS */

// Update selected value of each slider by calling updateDisplayOutput()
trainingInputElements.forEach((trainingInputElement) => {
    trainingInputElement.addEventListener("input", updateDisplayOutput);
    trainingInputElement.dispatchEvent(new Event("input"));
})

// Update selected value of a single slider
function updateDisplayOutput(inputEvent) {
    const trainingOutput = document.querySelector(`output[for="${inputEvent.target.id}"]`);
    trainingOutput.value = inputEvent.target.value;
}

/* DEFINE ACTIVATION OF TRAINING BUTTONS */

// trainBtn: tell server to "train"
document.getElementById("trainBtn").addEventListener("click", function () {
    if (running) {
        showError("Current training must complete or be stopped before training again.");
    }
    else {
        running = true;

        // Get selected slider settings from browser
        const trainingInputValues = Object.fromEntries(
            Array.from(trainingInputElements, (slider) => [slider.id, slider.value])
        );

        socket.emit("train", trainingInputValues);
        hideTrainingSidebarDiv.style.display = "block";
    }
})

// trainOffBtn: stop training
document.getElementById("trainOffBtn").addEventListener("click", function () {
    if (running && !stopRequested) {
        stopRequested = true;
        socket.emit("stop_episode");
    }
})

// Server finished training: either all training completed or stopped early */
socket.on("training_done", function (data) {

    // Turn training arena off
    running = false;
    stopRequested = false;
    clearBoard();

    // If training completed, get and display training stats.
    // Else, training was stopped early.
    if (data["completed"]) {
        drawMessage("training concluded", gameWidth / 2, gameHeight / 2);
        games = data["num_games_completed"];
    }
    else {
        drawMessage("training stopped", gameWidth / 2, gameHeight / 2);
    }

    // Draw stats 
    drawTrainingStats();   
})

/* DRAW SNAKE DURING TRAINIG */

socket.on("snake_data", function (data) {
    // ignore frames still in flight after "stop training" was clicked
    if (stopRequested) {
        return;
    }
    clearBoard();
    foodX = data["data"]["apple"]["x"];
    foodY = data["data"]["apple"]["y"];
    snake = data["data"]["snake"];
    games = data["data"]["stats"]["games"];
    score = data["data"]["stats"]["score"];
    gameScore = data["data"]["stats"]["record"];
    drawFood();
    drawSnake();
    drawTrainingStats();
})

/* Draw training stats */
function drawTrainingStats() {
    scoreText.textContent = score;
    highscoreText.textContent = gameScore;
    gamesText.textContent = games + "/100"
}
