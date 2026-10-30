# Progress

## Weeks 1-3, Aug. 24 - Sept. 11

* Draft feasible timeline for project:
    * Make basic Snake work and make it platform agnostic.
    * Make SnakeRL.
    * Design experiment.
    * Evaluate both Snake apps (heuristic or student beta testers).
* Make and share repo with faculty mentor.
* Fixes to basic Snake (`hinojosa_snake`):
    * Commented out function in `game.py` to make Snake platform agnostic
    (runs on Windows, Linux, and now macOS too).
    * Set port for Snake from default 5000 to 5001 since the default port
    is sometimes busy on macOS.
* Explore basic Snake.
* Begin making SnakeRL...
    * Created skeleton of main pages.
    * Cleaned up CSS.
    * Cleaned up HTML indentation.
    * Fixed CSS/HTML bugs that came with those changes.
    * Added more error messages and fixed close button.
    * Added flow enforcement (currently commented out).
* Create `write_dependencies.py` script to generate `dependencies.txt`
* Rewrote git history to remove `model` that was accidentally cached.

## Weeks 4-5, Sept. 14 - Sept. 25

* Continue making SnakeRL.
    * Misc HTML/CSS (spacing, alignment, font type, font size, etc.),
    bug fixes, and variable name consistency updates.
    * Made train button work by commenting out "@authenticated_only" in
    `events.py` (works with "@login_required" in `views.py`).
    * Replaced dropdowns with sliders.
    * Added `params.py` to store training input values as single source of
    truth.
    * Connected `alpha`, `gamma`, and `epsilon` to training process.
    * Fixed `write_dependencies.py` to include simple-websocket (missed
    b/c that is from runtime, not env).

* Submit registration to conferences.

## Weeks 6-7, Sept. 28 - Oct. 9

* Nothing for SnakeRL.
* Design and print memory poster.
* Present poster at CCSC.

# Weeks 8-9, Oct. 12 - Oct. 23

Small bug fixes and error handling:
* Fix `allow_unsafe_werkzeug` bug.
* Removed `GAMES` so that "stop training" stops the entire server
and no longer saves an agent.
* Added error message to Training: "Current training must finish
before training another agent."
* Fixed `log_to_db()` to actually save the new agent settings alpha,
gamma, and epsilon (reward function already saved) by updating AI
class in `dbmodels.py`. Deleted the old `database.db` so that the new
schema would work.
* Fixed the one-frame lag in the Training sidebar display.

Improve training by randomizing start spot:
* Made it so that snake starts at a different spot each episode.

Miscellaneous CSS and HTM improvements:
* Sidebar on Evaluation displays training settings and results
depending on which evaluation button was selected.
* Various CSS fixes to Training.
* Also clarified the "games" counter to "Games completed."

Change how agents are saved:
* Now save agents that complete training as "model_{ai_id}.pth"
* Somehow, got a really good agent `model_20.pth` that earns
about 47 rewards.

Complete evaluation and untrained agent pages:
* Done. Finallyyyyy.

General codebase improvements:
* Add comments and docstrings throughout JavaScript, agent, events, and game.
* Split training/eval/playsnake JavaScript into separate files and put
shared code in new file `snakecanvas.js`
* Moved error banner JavaScript to separate file `flasherror.js`

# Weeks 10-11, Oct. 26 - Nov. 6

* Tweaked signin dropdown and database to use xp_level instead of grade
* Disabled arrow keys on playsnake page
* Added back buttons
* Removed button to conclusion