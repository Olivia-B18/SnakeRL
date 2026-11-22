# SnakeRL: Teaching Reinforcement Learning to Undergraduate Students

## TODO:
1. Mandate users must be signed in.
2. Mandate pages must be visited in a certain flow.
3. Add description to SnakeRL section of `README.md`

## About

**Motivation for SnakeRL.** The field of reinforcement learning (RL)
is quickly growing and shows much promise; however, many research papers
exploring the topic are too jargon-heavy for newcomers to understand RL
or what it is about.

**Goal of SnakeRL.** The goal of this project is to make RL more accessible
to newcomers by building on the tool TrainYourAI developed by Hinojosa et al.,
which was presented at the ACM Conference SIGCSE TS 2025. Their
project introduced RL to middle school students using the game Snake,
and my project seeks to reveal RL more in depth by exposing parameters involved
in the learning process and is geared towards undergraduate students.

**Development Timeline.** The project began in Fall 2026. It extended the
TrainYourAI tool and concluded with a heuristic evaluation of SnakeRL, which can
be found in `notes/heuristic_eval.md`. The project will resume in Spring 2026
with student participants testing both tools.

## Installation

```
# Create a virtual environment with Python 3.12.
# I used conda, but other options like .venv's should work.
conda create -n <name_of_virtual_environment> python=3.12

# Activate the virtual environment (I used conda)
conda activate <name_of_virtual_environment>

# Install dependencies
pip install -r dependencies.txt
```

## TrainYourAI

### Sources

| Resource              | Link                                  |
| --------------------- | ------------------------------------- |
| TrainYourAI paper     | [dl.acm.org][paper]                   |
| TrainYourAI GitHub    | [cesarihinojosa/train-your-ai][repo]  |

<!-- nickname/URL mappings -->
[paper]: https://dl.acm.org/doi/abs/10.1145/3641554.3701907
[repo]: https://github.com/cesarihinojosa/train-your-ai

### Fixes by Me

The TrainYourAI repo has been copied into `trainyourai` with minor changes from me
to make the tool run on Windows, Linux, AND MacOS. The small fixes I made were:
* Commented out function in `game.py` since MacOS cannot handle the call.
* Set port for Snake from default 5000 to 5001 since the default port is 
sometimes busy on MacOS.
* Set `allow_unsafe_werkzeug=True` in `sockietio.run()` call because this app
is not production-level.
* Updated the `trainyourai/README.md` accordingly.

### Running TrainYourAI

```
cd trainyourai

python main.py

# MANUAL: open the port that loads in a browser <http://localhost:5001>
```

## SnakeRL

### Running SnakeRL

```
cd snakerl

python main.py

# MANUAL: open the port that loads in a browser <http://localhost:5001>
```

## Tour of Directories

* `notes`: my personal notes on my progress, terminal commands, and my heuristic
evaluation for SnakeRL.
* `snakerl`: my new Snake web app developed to teach RL to undergraduate students.
* `trainyourai`: the original Snake web app tool developed by Hinojosa et
al. to teach RL to middle schoolers.

## Acknowledgements and Credits

A huge thank you to my faculty mentor Professor Coleman for his guidance.

This project was developed with the use of Claude Code Opus 5.5, including:
debugging, writing new code, breaking down the steps to code what I wanted,
tracing through the logic of the TrainYourAI repo, and more.
