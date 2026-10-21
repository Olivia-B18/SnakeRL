
/*
JavaScript for the playsnake page.
*/

/* CONSTANTS AND VARIABLES */

// HTML text for snake stats
const scoreText = document.querySelector("#scoreText");
const gameText = document.querySelector("#gameText");

// Flag for if play is in progress
let running = false;

/*
Old bug: snake goes right, I hit the down arrow
key, then the left arrow key soon after, and the game is over
already because I "ran into myself" even though I made separate
keystrokes.

Solution: use directionChanged flag.
*/

// Flag for if direction has changed
let directionChanged = false;

// Speed, location, and start length of snake
let speed = 180;
let xVelocity = unitSize;
let yVelocity = 0;
let snake = [
    { x: unitSize * 4, y: 0 },
    { x: unitSize * 3, y: 0 },
    { x: unitSize * 2, y: 0 },
    { x: unitSize, y: 0 },
    { x: 0, y: 0 }
];

// Values for play stats
let score = 0;
let games = 0;

/* SET UP PLAY ARENA */

// Draw message to canvas
document.fonts.load(messageFont)
    .catch(() => { })
    .then(() => {
        drawMessage("press play", gameWidth / 2, gameHeight / 2);
        drawMessage("arrow keys to play", gameWidth / 2, gameHeight / 3);
    });

// Move the snake with arrow keys
window.addEventListener("keydown", function(event) {

    // Check if the direction already changed
    if (directionChanged) return;

    const keyPressed = event.keyCode;
    const LEFT = 37;
    const UP = 38;
    const RIGHT = 39;
    const DOWN = 40;

    const goingUp = (yVelocity == -unitSize);
    const goingDown = (yVelocity == unitSize);
    const goingRight = (xVelocity == unitSize);
    const goingLeft = (xVelocity == -unitSize);

    switch (true) {
        case (keyPressed == LEFT && !goingRight):
            xVelocity = -unitSize;
            yVelocity = 0;
            directionChanged = true;
            break;
        case (keyPressed == UP && !goingDown):
            xVelocity = 0;
            yVelocity = -unitSize;
            directionChanged = true;
            break;
        case (keyPressed == RIGHT && !goingLeft):
            xVelocity = unitSize;
            yVelocity = 0;
            directionChanged = true;
            break;
        case (keyPressed == DOWN && !goingUp):
            xVelocity = 0;
            yVelocity = unitSize;
            directionChanged = true;
            break;
    }
});

/* DEFINE ACTIVATION OF PLAY BUTTON (id is "resetBtn") */

// resetBtn: reset for new game
document.querySelector("#resetBtn").addEventListener("click", function() {

    // Set flag for running
    running = true;

    // Reset play stats
    score = 0;
    games++;
    gameText.textContent = "GAMES: " + games;
    scoreText.textContent = "SCORE: " + score;

    // Reset snake
    speed = 180;
    xVelocity = unitSize;
    yVelocity = 0;
    snake = [
        { x: unitSize * 4, y: 0 },
        { x: unitSize * 3, y: 0 },
        { x: unitSize * 2, y: 0 },
        { x: unitSize, y: 0 },
        { x: 0, y: 0 }
    ];

    // Spawn new apple
    createFood();
    drawFood();
    
    // Begin game
    nextTick();
})

// Keep the game running
function nextTick() {
    // If still running, keep playing.
    // Else, display game over message.
    if (running) {
        setTimeout(() => {
            clearBoard();
            drawFood();
            moveSnake();
            drawSnake();
            checkGameOver();
            nextTick();
        }, speed);
    }
    else {
        drawMessage("game over", gameWidth / 2, gameHeight / 2);
        running = false;
    }
};

// Move the snake
function moveSnake() {

    // Reset flag so that player can turn on next frame
    directionChanged = false;

    // Get new head of snake
    const head = {
        x: snake[0].x + xVelocity,
        y: snake[0].y + yVelocity
    };

    // Add head to beginning of snake
    snake.unshift(head);

    // If food is eaten, keep added length of snake and spawn next apple
    // Else, remove the tail of the snake to maintain current length
    if (snake[0].x == foodX && snake[0].y == foodY) {
        score += 1;
        scoreText.textContent = "SCORE: " + score;
        speedUp()
        createFood();
    }
    else {
        snake.pop();
    }
};

// Make snake go faster incrementally
function speedUp() {
    speed -= 20
}

// Randomly spawn food
function createFood() {
    function randomFood(min, max) {
        const randNum = Math.round((Math.random() * (max - min) + min) / unitSize) * unitSize;
        return randNum;
    }
    foodX = randomFood(0, gameWidth - unitSize);
    foodY = randomFood(0, gameHeight - unitSize);
};

// Check for a game over
function checkGameOver() {

    // Check if snake runs into wall
    switch (true) {
        case (snake[0].x < 0):
            running = false;
            break;
        case (snake[0].x >= gameWidth):
            running = false;
            break;
        case (snake[0].y < 0):
            running = false;
            break;
        case (snake[0].y >= gameHeight):
            running = false;
            break;
    }

    // Check if snake runs into itself
    for (let i = 1; i < snake.length; i += 1) {
        if (snake[i].x == snake[0].x && snake[i].y == snake[0].y) {
            running = false;
        }
    }
};

