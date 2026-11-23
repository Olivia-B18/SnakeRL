"""
Linear flow enforcement for the guided lesson.

The lesson is meant to be walked in one order:

    1. Intro
    2. How to Snake
    3. PlaySnake
    4. Untrained
    5. Parameters
    6. Training
    7. Evaluation
    8. Reflection

Flow maintained in this file because login_required only
answers if a person is signed in, not managing locking pages.
"""

from functools import wraps
from flask import flash, redirect, request, session, url_for

# The lesson pages in the order they must be visited. These are view function
# names on the `views` blueprint.
FLOW = ["intro",
        "howtosnake",
        "playsnake",
        "untrained",
        "parameters",
        "training",
        "evaluation",
        "reflection",
        ]

# Names shown for each page in the navigation sidebar
LABELS = {"intro": "Introduction",
          "howtosnake": "How to Play Snake",
          "playsnake": "Play Snake",
          "untrained": "Untrained Agent",
          "parameters": "Parameters",
          "training": "Training",
          "evaluation": "Evaluation",
          "reflection": "Reflection",
          }

# Sections inside a page that the sidebar lists, indented under that page.
# Each is (section id, sidebar label). The ids must match the
# <section class="lesson-step" id="..."> elements in that page's template,
# in the same order, so keep this in sync when sections change.
SUBSTEPS = {"parameters": [("untrained-agent", "Untrained Agent Discussion"),
                           ("mdp", "Markov Decision Processes"),
                           ("q-values", "What are Q-values?"),
                           ("bellman", "The Bellman Equation"),
                           ("parameters", "Hyperparameters"),
                           ("agent_parameters", "Agent Hyperparameters"),
                           ("env_parameters", "Environment Hyperparameters"),
                           ],
            }

# Pages actually guarded by @flow.step. Filled in as views are decorated, so
# the sidebar only shows a page as locked once its view enforces the order.
GUARDED = set()

SESSION_KEY = "flow_unlocked"

SKIP_MESSAGE = 'You must visit each page in order. Click "continue" for the next page.'


def reset():
    """Start the lesson over. Called when a new user signs in."""
    session[SESSION_KEY] = 0


def clear():
    """Forget progress entirely. Called on sign out."""
    session.pop(SESSION_KEY, None)


def unlocked():
    """Index of the furthest page the user is allowed to visit."""
    return session.get(SESSION_KEY, 0)


def step(name):
    """Guard a view as step `name` of the lesson.
    """
    stage = FLOW.index(name)  # raises at import time if `name` is misspelled
    GUARDED.add(name)

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if stage > unlocked():
                # Skipped ahead: say so, then leave them on the page they are
                # already on -- the furthest one they have reached, which is one
                # behind the next unlocked stage.
                flash(SKIP_MESSAGE, category="error")
                current = FLOW[max(unlocked() - 1, 0)]
                return redirect(url_for("views." + current))
            if stage + 1 > unlocked():
                session[SESSION_KEY] = stage + 1
            return f(*args, **kwargs)

        return wrapped

    return decorator


def is_locked(name):
    """True if the page is guarded by @flow.step and not yet unlocked."""
    return name in GUARDED and FLOW.index(name) > unlocked()


def nav_items():
    """The lesson pages, in order, for the navigation sidebar."""
    items = []
    for i, name in enumerate(FLOW):
        url = url_for("views." + name)
        items.append({"number": i + 1,
                      "label": LABELS[name],
                      "url": url,
                      "locked": is_locked(name),
                      "current": request.endpoint == "views." + name,
                      "substeps": [{"id": step_id,
                                    "label": label,
                                    "url": url + "#" + step_id,
                                    }
                                   for step_id, label in SUBSTEPS.get(name, [])],
                      })
    return items
