/*
JavaScript for the evaluation page.
*/

/* CONSTANTS AND VARIABLES */

// Sidebar content to show/hide
const hideEvalSidebarDiv = document.getElementById("hideEvalSidebar");
const hideOneEpisodeScoreDiv = document.getElementById("hideOneEpisodeScore");
const hidehighScoreDiv = document.getElementById("hidehighScore");
const hideAvgScoreDiv = document.getElementById("hideAvgScore");

// HTML text for game counter
const gamesText = document.querySelector("#games");

// HTML text for evaluation stats
const oneEpisodeScoreText = document.querySelector("#oneEpisodeScoreText");
const highScoreText = document.querySelector("#highScoreText");
const avgScoreText = document.querySelector("#avgScoreText");

// Flags and errors for if there is no trained agent
const hasTrainedAgent = hideEvalSidebarDiv.dataset.hasAgent === "true";
const noAgentMessage = "You must first completely train an agent to evaluate it.";

// Connection to the server
const socket = io();

// The snake
snake = []

// Values for game counter
let games = 0;
let maxGames = -1;

// Values for evaluation stats (null = no result yet, shown as "?")
let oneEpisodeScore = null;
let highScore = null;
let avgScore = null;

// Flags for if evaluation is in progress
let running = false;
let stopRequested = false;

/* SET UP EVALUATION ARENA */

// Hide sidebar
hideEvalSidebarDiv.style.display = "none";
hideOneEpisodeScoreDiv.style.display = "none";
hidehighScoreDiv.style.display = "none";
hideAvgScoreDiv.style.display = "none";

// Draw message to canvas
document.fonts.load(messageFont)
    .catch(() => { })
    .then(() => {
        drawMessages([
            "Use the buttons below to evaluate",
            "the score of your trained agent",
            "from the training page.",
            "",
            "Evaluate for 1 game or across",
            "10 games and watch the agent",
            "earn points.",
        ])
    });

/* DEFINE ACTIVATION OF EVALUATION BUTTONS */

// evalOnceBtn: tell server to "evaluate" for 1 episode
document.getElementById("evalOnceBtn").addEventListener("click", function () {
    if (!hasTrainedAgent) {
        showError(noAgentMessage);
    }
    else if (running) {
        showError("Current evaluation must be complete or be stopped before evaluating again.")
    }
    else {

        // Run evaluation; clear old results so they show "?" until it finishes
        running = true;
        oneEpisodeScore = null;
        highScore = null;
        avgScore = null;
        socket.emit("evaluate", {"numEpisodes": 1});

        // Set maxGames
        maxGames = 1;

        /* show/hide sidebar content */
        hideEvalSidebarDiv.style.display = "block";
        hideOneEpisodeScoreDiv.style.display = "block";
        hidehighScoreDiv.style.display = "none";
        hideAvgScoreDiv.style.display = "none";
    }
})

// evalTenBtn: tell server to "evaluate" for 10 episodes
document.getElementById("evalTenBtn").addEventListener("click", function () {
    if (!hasTrainedAgent) {
        showError(noAgentMessage);
    }
    else if (running) {
        showError("Current evaluation must be complete or be stopped before evaluating again.")
    }
    else {

        // Run evaluation; clear old results so they show "?" until it finishes
        running = true;
        oneEpisodeScore = null;
        highScore = null;
        avgScore = null;
        socket.emit("evaluate", {"numEpisodes": 10});

        // Set maxGames
        maxGames = 10;

        /* show/hide sidebar content */
        hideEvalSidebarDiv.style.display = "block";
        hideOneEpisodeScoreDiv.style.display = "none";
        hidehighScoreDiv.style.display = "block";
        hideAvgScoreDiv.style.display = "block";
    }
})

// evalOffBtn: stop evaluation
document.getElementById("evalOffBtn").addEventListener("click", function () {
    if (!running) {
        showError("There is no evaluation running to stop.");
    }
    else if (!stopRequested) {
        stopRequested = true;
        socket.emit("stop_episode");
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

        // Update game counter
        games = data["scores"].length;

        // Fill variables with scores to later draw to browser
        if (data["scores"].length == 1) {
            oneEpisodeScore = data["scores"][0];
        }
        else {
            highScore = Math.max(...data["scores"]);
            let sum = 0;
            for (let i = 0; i < data["scores"].length; i++) {
                sum += data["scores"][i];
            }
            avgScore = (sum / data["scores"].length).toFixed(1);
        }
    }
    else {
        drawMessage("evaluation stopped", gameWidth / 2, gameHeight / 2);
    }

    // Draw stats
    drawEvaluationStats();   
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
    games = data["data"]["stats"]["games"];
    drawFood();
    drawSnake();
    drawEvaluationStats();
})

// Draw evaluation score stats
function drawEvaluationStats() {
    gamesText.textContent = games + "/" + maxGames;
    oneEpisodeScoreText.textContent = scoreOrPending(oneEpisodeScore);
    highScoreText.textContent = scoreOrPending(highScore);
    avgScoreText.textContent = scoreOrPending(avgScore);
}

// A score, or "?" while it hasn't been calculated yet
function scoreOrPending(score) {
    return score === null ? "?" : score;
}
