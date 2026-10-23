/*
JavaScript for the untrained agent page.
*/

/* CONSTANTS AND VARIABLES */

// Sidebar content to show/hide
const hideEvalSidebarDiv = document.getElementById("hideEvalSidebar");
const hideOneEpisodeScoreDiv = document.getElementById("hideOneEpisodeScore");
const hideHighestScoreDiv = document.getElementById("hideHighestScore");
const hideAvgScoreDiv = document.getElementById("hideAvgScore");

// HTML text for evaluation stats
const oneEpisodeScoreText = document.querySelector("#oneEpisodeScoreText");
const highestScoreText = document.querySelector("#highestScoreText");
const avgScoreText = document.querySelector("#avgScoreText");

// Connection to the server
const socket = io();

// The snake
snake = []

// Values for evaluation stats
let oneEpisodeScore = 0;
let highestScore = 0;
let avgScore = 0;

// Flags for if evaluation is in progress
let running = false;
let stopRequested = false;

/* SET UP EVALUATION ARENA */

// Hide sidebar
hideEvalSidebarDiv.style.display = "none";
hideOneEpisodeScoreDiv.style.display = "none";
hideHighestScoreDiv.style.display = "none";
hideAvgScoreDiv.style.display = "none";

// Draw message to canvas
document.fonts.load(messageFont)
    .catch(() => { })
    .then(() => drawMessage("untrained arena", gameWidth / 2, gameHeight / 2));

/* DEFINE ACTIVATION OF EVALUATION BUTTONS */

// evalOnceBtn: tell server to "evaluate" for 1 episode
document.getElementById("evalOnceBtn").addEventListener("click", function () {
    if (running) {
        showError("Current evaluation must be complete or be stopped before evaluating again.")
    }
    else {
        running = true;
        socket.emit("evaluate_untrained", {"numEpisodes": 1});
    }
})

// evalTenBtn: tell server to "evaluate" for 10 episodes
document.getElementById("evalTenBtn").addEventListener("click", function () {
    if (running) {
        showError("Current evaluation must be complete or be stopped before evaluating again.")
    }
    else {
        running = true;
        socket.emit("evaluate_untrained", {"numEpisodes": 10});
    }
})

// Server finished evaluation: either evaluation completed or stopped
socket.on("evaluation_done", function (data) {

    // Turn evaluation arena off
    running = false;
    stopRequested = false;
    clearBoard();

    // If evaluation completed, get and display evaluation stats.
    // Else, evaluation was stopped early.
    if (data["completed"]) {

        // Draw concluding message
        drawMessage("evaluation concluded", gameWidth / 2, gameHeight / 2);

        // Fill variables with scores to later draw to browser
        if (data["scores"].length == 1) {
            oneEpisodeScore = data["scores"][0];

            /* show/hide sidebar content */
            hideEvalSidebarDiv.style.display = "block";
            hideOneEpisodeScoreDiv.style.display = "block";
            hideHighestScoreDiv.style.display = "none";
            hideAvgScoreDiv.style.display = "none";
        }
        else {
            highestScore = Math.max(...data["scores"]);
            let sum = 0;
            for (let i = 0; i < data["scores"].length; i++) {
                sum += data["scores"][i];
            }
            avgScore = (sum / data["scores"].length).toFixed(1);

            /* show/hide sidebar content */
            hideEvalSidebarDiv.style.display = "block";
            hideOneEpisodeScoreDiv.style.display = "none";
            hideHighestScoreDiv.style.display = "block";
            hideAvgScoreDiv.style.display = "block";
        }
    }
    else {
        drawMessage("evaluation stopped", gameWidth / 2, gameHeight / 2);
    }

    // Draw stats
    drawEvaluationStats();   
})

// evalOffBtn: stop evaluation
document.getElementById("evalOffBtn").addEventListener("click", function () {
    if (running && !stopRequested) {
        stopRequested = true;
        socket.emit("stop_episode");
    }
})

/* DRAW SNAKE DURING EVALUATION */

socket.on("snake_data", function (data) {
    // ignore frames still in flight after "stop eval" was clicked
    if (stopRequested) {
        return;
    }
    clearBoard();
    foodX = data["data"]["apple"]["x"];
    foodY = data["data"]["apple"]["y"];
    snake = data["data"]["snake"];
    drawFood();
    drawSnake();
    drawEvaluationStats();
})

// Draw evaluation score stats
function drawEvaluationStats() {
    oneEpisodeScoreText.textContent = oneEpisodeScore;
    highestScoreText.textContent = highestScore;
    avgScoreText.textContent = avgScore;
}
