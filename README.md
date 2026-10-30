# SnakeRL: Teaching Reinforcement Learning to Undergraduate Students

## TODO:
1. Mandate users must be signed in.
2. Mandate pages must be visited in a certain flow.

<!-- ABOUT -->

## About

The field of reinforcement learning (RL) is quickly growing and shows
much promise; however, many research papers exploring the topic
are too jargon-heavy for newcomers to understand RL or what it
is about.

The goal of this project, SnakeRL, is to make RL more accessible to newcomers
by building on the tool TrainYourSnakeAI developed by Hinojosa et al.,
which was presented at the ACM Conference SIGCSE TS 2025. Their
project introduced RL to middle school students using the game Snake,
and my project seeks to reveal RL more in depth by exposing parameters involved
in the learning process and is geared towards undergraduate students.

This project was completed in Fall 2026.

<!-- INSTALLATION -->

## Installation

```
# Create a virtual environment with Python 3.12 (I used conda)
conda create -n <name_of_virtual_environment> python=3.12

# Activate the virtual environment (I used conda)
conda activate <name_of_virtual_environment>

# Install dependencies
pip install -r dependencies.txt
```

<!-- TRAINYOURSNAKEAI -->

## TrainYourSnakeAI

### Sources

The paper for TrainYourSnakeAI can be found at: https://doi.org/10.1145/3641554.3701907

The GitHub repo for TrainYourSnakeAI can be found at:
https://github.com/cesarihinojosa/train-your-ai

### Fixes by Me

The TrainYourSnakeAI repo has been copied into `trainyoursnakeai` with minor changes from me
to make the tool run on Windows, Linux, AND MacOS. The small fixes I made were:
* Commented out function in `game.py` since MacOS cannot handle the call.
* Set port for Snake from default 5000 to 5001 since the default port is 
sometimes busy on MacOS.
* Set `allow_unsafe_werkzeug=True` in `sockietio.run()` call because this app
is not production-level.
* Updated the `trainyoursnakeai/README.md` accordingly.

### Running TrainYourSnakeAI

```
cd trainyoursnakeai

python main.py

# MANUAL: open the port that loads in a browser <http://localhost:5001>
```

<!-- SNAKERL -->

## SnakeRL

### Description

TBD

### Running SnakeRL

```
cd snakerl

python main.py

# MANUAL: open the port that loads in a browser <http://localhost:5001>
```

<!-- DIRECTORIES -->

## Tour of Directories

* `trainyoursnakeai`: the original Snake web app tool developed by Hinojosa et
al. to teach RL to middle schoolers.
* `notes`: my personal notes on research, my progress, and terminal commands.
* `snakerl`: my new Snake web app developed to teach RL to undergraduate students.

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements and Credits

A huge thank you to my faculty mentor Professor Coleman for his guidance.

This project was developed with the use of Claude Code Opus 5.5, including:
debugging, writing new code, breaking down the steps to code what I wanted,
tracing through the logic of the TrainYourSnakeAI repo, and more.
