"""
Training inputs used by training.html (UI), events.py (validation), and
views.py (rendering).

Dict order is render order: Python preserves insertion order, so the sliders
appear on the page in the order declared below.
"""

PARAMS = {
    # --- Agent hyperparameters -------------------------------------------
    "alpha": {
        "label": "Learning rate",
        "group": "agent",
        "type": float,
        "min": 0.001,
        "max": 0.01,
        "step": 0.001,
        "default": 0.001,
        "ticks": [0.001, 0.005, 0.01],
    },
    "gamma": {
        "label": "Discount factor",
        "group": "agent",
        "type": float,
        "min": 0.8,
        "max": 0.99,
        "step": 0.01,
        "default": 0.9,
        "ticks": [0.8, 0.9, 0.99],
    },
    "epsilon": {
        "label": "Starting exploration",
        "group": "agent",
        "type": int,
        "min": 0,
        "max": 100,
        "step": 10,
        "default": 80,
        "ticks": [0, 50, 100],
    },

    # --- Reward function --------------------------------------------------
    "eat": {
        "label": "Eat",
        "group": "reward",
        "type": int,
        "min": -10,
        "max": 10,
        "step": 10,
        "default": 0,
        "ticks": [-10, 0, 10],
    },
    "alive": {
        "label": "Alive",
        "group": "reward",
        "type": int,
        "min": -10,
        "max": 10,
        "step": 10,
        "default": 0,
        "ticks": [-10, 0, 10],
    },
    "die": {
        "label": "Die",
        "group": "reward",
        "type": int,
        "min": -10,
        "max": 10,
        "step": 10,
        "default": 0,
        "ticks": [-10, 0, 10],
    },
}
