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
from flask_login import current_user

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

# Furthest section reached on pages with SUBSTEPS: {page name: section index}
SUBSTEP_KEY = "flow_substeps"

SKIP_MESSAGE = 'You must visit each page in order. Click "continue" for the next page.'


def reset():
    """Start the lesson over. Called when a new user signs in."""
    session[SESSION_KEY] = 0
    session.pop(SUBSTEP_KEY, None)


def clear():
    """Forget progress entirely. Called on sign out."""
    session.pop(SESSION_KEY, None)
    session.pop(SUBSTEP_KEY, None)


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
                # Skipped ahead: say so, then send them back to the furthest
                # page they have reached
                flash(SKIP_MESSAGE, category="error")
                return redirect(url_for("views." + furthest_reached()))
            if name in SUBSTEPS:
                # Mark the page as visited; its sections unlock one by one
                # through record_substep()
                if name not in _substep_progress():
                    _set_substep_seen(name, -1)
            # Visiting a page unlocks the next one -- except on a page with
            # sections, where only reaching its last section does
            if stage + 1 > unlocked() and substeps_complete(name):
                session[SESSION_KEY] = stage + 1
            return f(*args, **kwargs)

        return wrapped

    return decorator


def furthest_reached():
    """Name of the furthest page the user has visited."""
    next_page = unlocked()
    # The next unlocked page normally hasn't been visited yet. A page with
    # sections is the exception: it stays the furthest unlocked page while
    # its sections are being worked through.
    if next_page < len(FLOW) and FLOW[next_page] in _substep_progress():
        return FLOW[next_page]
    return FLOW[max(next_page - 1, 0)]


def _substep_progress():
    return session.get(SUBSTEP_KEY, {})


def _set_substep_seen(name, index):
    progress = dict(_substep_progress())  # copy so Flask saves the change
    progress[name] = index
    session[SUBSTEP_KEY] = progress


def substeps_enforced(name):
    """True if the page's sections must be viewed in order."""
    return name in GUARDED and name in SUBSTEPS


def substeps_seen(name):
    """Index of the furthest section viewed on the page (-1 for none)."""
    return _substep_progress().get(name, -1)


def substeps_complete(name):
    """True once the page's last section has been viewed (or if not enforced)."""
    if not substeps_enforced(name):
        return True
    return substeps_seen(name) >= len(SUBSTEPS[name]) - 1


def record_substep(name, step_id):
    """Record that a section of a page was viewed.

    A section unlocks once the one before it has been viewed, so skipping
    ahead is ignored. Viewing the last section unlocks the next page.
    Returns the furthest section index viewed, or None for an unknown
    page or section.
    """
    if name not in SUBSTEPS:
        return None
    ids = [step for step, _ in SUBSTEPS[name]]
    if step_id not in ids:
        return None
    if not substeps_enforced(name):
        return len(ids) - 1
    index = ids.index(step_id)
    seen = substeps_seen(name)
    if FLOW.index(name) <= unlocked() and seen < index <= seen + 1:
        seen = index
        _set_substep_seen(name, seen)
        if substeps_complete(name):
            session[SESSION_KEY] = max(unlocked(), FLOW.index(name) + 1)
    return seen


def is_locked(name):
    """True if the page is guarded by @flow.step and not yet unlocked."""
    return name in GUARDED and FLOW.index(name) > unlocked()


def lock_reason(name):
    """Why the sidebar shows this page as locked, or None if it isn't."""
    # The lesson starts at the first page, which needs a signed-in user
    if name == FLOW[0] and not current_user.is_authenticated:
        return "Sign in to start the lesson"
    if is_locked(name):
        return "Finish the earlier pages first"
    return None


def nav_items():
    """The lesson pages, in order, for the navigation sidebar."""
    items = []
    for i, name in enumerate(FLOW):
        url = url_for("views." + name)
        reason = lock_reason(name)
        # Sections past the one after the furthest viewed are locked
        open_through = (substeps_seen(name) + 1 if substeps_enforced(name)
                        else len(SUBSTEPS.get(name, [])))
        items.append({"number": i + 1,
                      "label": LABELS[name],
                      "url": url,
                      "locked": reason is not None,
                      "lock_reason": reason,
                      "current": request.endpoint == "views." + name,
                      "substeps": [{"id": step_id,
                                    "label": label,
                                    "url": url + "#" + step_id,
                                    "locked": j > open_through,
                                    }
                                   for j, (step_id, label)
                                   in enumerate(SUBSTEPS.get(name, []))],
                      })
    return items
