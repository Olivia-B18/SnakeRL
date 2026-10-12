# SnakeRL: Teaching Reinforcement Learning to Undergraduate Students

## About

The field of reinforcement learning is quickly growing and shows
much promise; however, many research papers exploring the topic
are too jargon-heavy for newcomers to understand RL or what it
is about.

The goal of this project, SnakeRL, is to make RL more accessible to newcomers
by building on the tool TrainYourSnakeAI developed by Hinojosa et al.,
which was presented at the ACM Conference SIGCSE TS 2025. Their
project introduced RL to middle school students using the game Snake,
and my project seeks to reveal RL more in depth by exposing parameters involved
in the learning process and is geared towards undergraduate students.

## Installation

```
# Create a virtual environment with Python 3.12 (I used conda)
conda create -n sim python=3.12

# Install dependencies
pip install -r dependencies.txt
```

## TrainYourSnakeAI Tool

### Sources

The paper for TrainYourSnakeAI can be found at: https://dl.acm.org/doi/abs/10.1145/3641554.3701907?__cf_chl_tk=1JzGPd_DFYq4fCy4w0JChaSYk3Zoor3PPA.xu3b0fSo-1788186886-1.0.1.1-LWrl.lPRfxWrd_V.4uFaWngBNk2N92Pbbjb8qB_9J.c

The GitHub repo for TrainYourSnakeAI can be found at:
https://github.com/cesarihinojosa/train-your-ai

### Fixes by Me

Their repo has been copied into `trainyoursnakeai` with minor changes from me
to make the tool run on Windows, Linux, AND MacOS. The small fixes I made were to:
* Commented out function in `game.py` to make Snake platform agnostic (runs on
Windows, Linux, and now macOS too).
* Set port for Snake from default 5000 to 5001 since the default port is 
sometimes busy on macOS.
* Set `allow_unsafe_werkzeug=True` in `sockietio.run()` call because this app
is not production-level.
* Update the `trainyoursnakeai/README.md` accordingly.

### Running TrainYourSnakeAI

```
cd trainyoursnakeai

python main.py

# MANUAL: open the port that loads in a browser <http://localhost:5001>
```

## SnakeRL Tool

### Description

TBD

### Running SnakeRL

```
cd snakerl

python main.py

# MANUAL: open the port that loads in a browser <http://localhost:5001>
```

## Tour of Directories

* `trainyoursnakeai`: the original Snake web app tool developed by Hinojosa et
al. to teach reinforcement learning to middle schoolers.
* `notes`: my personal notes on research, my progress, and terminal commands.
* `snakerl`: my new Snake web app developed to teach reinforcement learning to
undergraduate students.
