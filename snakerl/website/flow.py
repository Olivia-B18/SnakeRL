"""
Linear flow enforcement for the guided lesson.

The lesson is meant to be walked in one order:

    1. Intro
    2. Snake
    3. Untrained
    4. Parameters
    5. Training
    6. Evaluation
    7. Conclusion

Flow maintained in this file because login_required only
answers if a person is signed in, not managing locking pages.
"""

from functools import wraps

from flask import flash, redirect, session, url_for

# The lesson pages in the order they must be visited. These are view function
# names on the `views` blueprint.
FLOW = ["intro",
        "snake",
        "untrained",
        "parameters",
        "training",
        "evaluation",
        "conclusion",
        ]

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
