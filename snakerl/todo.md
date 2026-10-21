# TO DO

## Fix focus on snake.html

The page scrolls because pressing an arrow key does two things. Your keydown listener on window turns the snake, and then the browser runs its default action for that key, which is scrolling. Your listener never tells the browser to skip that default. Making the canvas focusable controls when the keys belong to the game, but on its own it won’t stop the scrolling. You need both pieces.

Step 1: Stop the scrolling with preventDefault()

Calling event.preventDefault() on an arrow keydown cancels the browser’s scroll. In changeDirection() (snake.js:113), call it for any arrow key, before the switch. If you call it only inside the cases that change direction, pressing the opposite direction (which the game ignores) would still scroll the page.

Step 2: Let the canvas take focus

By default a <canvas> can’t receive focus, so it never gets keyboard events of its own.

Add tabindex="0" to the canvas in snake.html:13. That makes it focusable by clicking or by Tab.
Move the listener from window to the canvas: gameBoard.addEventListener("keydown", changeDirection) instead of window.addEventListener(...) at snake.js:45. Now the arrow keys only steer the snake, and are only blocked from scrolling, while the canvas has focus. When the canvas doesn’t have focus, the page scrolls normally.
Step 3: Give the canvas focus at the right time
In resetGame() or gameStart(), call gameBoard.focus(). Clicking play then moves focus to the board, so the first arrow press goes to the game.
This also fixes a bug you may not have noticed. Right now focus stays on the play button after you click it. Pressing Space or Enter mid-game “clicks” it again and calls resetGame() while the game is running. That starts a second nextTick loop, and the snake moves twice per tick.
Decide what happens if the player clicks somewhere else mid-game. The canvas loses focus and arrow keys scroll again. Clicking the canvas focuses it automatically because of tabindex. You could also show “click the board to continue” on a blur event, or pause the game.
Step 4: Show when the canvas has focus

Browsers draw a focus outline on focused elements, and on your rounded board it can look odd. Don’t just remove it with outline: none. Players need a visible sign that the board is “listening”. Instead, add a .game-board:focus rule in snake.css that changes the border to your accent color, for example.

Optional cleanup
event.keyCode is deprecated. event.key gives readable names like "ArrowLeft", so you wouldn’t need the 37–40 constants.
Space also scrolls the page by default. If you ever use Space for pause, preventDefault() it too.
A simpler alternative

You could keep the listener on window and call preventDefault() only while running is true. Arrow keys would steer and not scroll during a game, and scroll normally otherwise. That’s one if and no focus handling. The focus approach is better if you want the page to stay scrollable during a game, or if you also want to fix the Space/Enter restart bug.

Checklist
 Add tabindex="0" to <canvas id="gameBoard"> in snake.html
 Move the keydown listener from window to gameBoard in snake.js
 In changeDirection(), call event.preventDefault() for all four arrow keys, before the direction checks
 Call gameBoard.focus() when play is clicked (resetGame() or gameStart())
 Add a .game-board:focus style in snake.css, e.g. an accent-colored border, and keep some visible indicator
 Decide what happens on blur mid-game: nothing, a “click to continue” message, or pause
 Optional: switch from keyCode to event.key
 Test: shrink the window so the page scrolls. Click play and use the arrows: the snake turns and the page doesn’t move. Click outside the canvas: the arrows scroll the page. Click the canvas: the arrows steer again.
 Test: mid-game, press Space and Enter. The game shouldn’t restart or speed up.
 Test: Tab to the canvas with the keyboard alone and play. The focus style should be visible.

