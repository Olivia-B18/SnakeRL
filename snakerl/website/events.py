import functools
import threading
from flask import request
from flask_login import current_user
from .dbmodels import AI
from flask_socketio import disconnect, emit
from .extensions import socketio
from .params import PARAMS

REQ_TRAINING_INPUTS = tuple(name for name, spec in PARAMS.items())
VALID_NUM_EPISODES = [1, 10]

# One stop flag per connected client that is currently training, keyed by
# socket session id. Each user gets their own flag, so stopping one user's
# training never affects anyone else's.
stop_flags = {}

# DEV: socket auth is commented out to match views.py where "# @login_required"
# is disabled while pages are being built. Re-enable "# @authenticated_only"
# lines below at the same time as the decorators in views.py.

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on("connect")
# @authenticated_only
def handle_connect():
    print("client connected")

@socketio.on("disconnect")
def handle_disconnect():
    # Closing or leaving the page stops that client's training run.
    flag = stop_flags.get(request.sid)
    if flag:
        flag.set()

@socketio.on("user_join")
def handle_user_join(username):
    print(f"user {username} joined")

def clean(payload):
    """
    Validate data type and values of training input against expected PARAMS.
    """

    # Validate that payload (training input) is converted to a dictionary
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JS object, got {type(payload).__name__}")

    # Fill cleaned with validated payload
    cleaned = {}
    for name, spec in PARAMS.items():
        # Missing required key
        if name not in payload:
            raise ValueError(f"missing {name}")

        # Cast training input to required data type
        try:
            value = spec["type"](payload[name])
        except (TypeError, ValueError):
            raise ValueError(
                f"{name}: {payload[name]!r} is not a {spec['type'].__name__}"
            )

        # Ensure training input is wihtin expected bounds
        if not spec["min"] <= value <= spec["max"]:
            raise ValueError(
                f"{name}: {value} outside {spec['min']}..{spec['max']}"
            )

        # Fill cleaned dictionary with cleaned training input
        cleaned[name] = value

    # Return
    return cleaned

@socketio.on("train")
# @authenticated_only
def handle_train(training_inputs):
    """
    Server trains an Agent.
    """

    # Check if "train" button was hit while training is already in progress
    sid = request.sid
    if sid in stop_flags:
        print("train: already training")
        return

    # Clean training input
    try:
        values = clean(training_inputs)
    except ValueError as err:
        print(f"train: {err}")
        emit("training_done", {"completed": False})
        return

    # Begin training: runs until 100 games finish or the client asks to stop
    from .agent import start
    stop_flags[sid] = threading.Event()
    completed = False
    num_games_completed = -1
    try:
        completed, num_games_completed = start(**{key: values[key] for key in REQ_TRAINING_INPUTS},
                                               should_stop=stop_flags[sid].is_set)
    finally:
        del stop_flags[sid]

        # Report training results
        emit("training_done", {"completed": completed,
                            "num_games_completed": num_games_completed,
                            })

@socketio.on("evaluate")
# @ authenticated_only
def handle_evaluate(evaluation_inputs):
    """
    Server evaluates an agent.
    """

    # Check if "evaluate" button was hit while evaluation is already is in progress
    sid = request.sid
    if sid in stop_flags:
        print("evaluate: already evaluating")
        return

    # Validate the number of episodes to evaluate for
    num_episodes = evaluation_inputs.get("numEpisodes")
    if num_episodes not in VALID_NUM_EPISODES:
        emit("evaluation_done", {"completed": False})
        return
    
    # Get the row of the newest AI from the database
    if current_user.is_authenticated:
        ai = (AI.query
              .filter_by(user_id=current_user.id)
              .order_by(AI.id.desc())
              .first())
    else:
        emit("evaluation_done", {"completed": False})
        return

    # Check that an AI was created
    if ai is None:
        emit("evaluation_done", {"completed": False})
        return

    # Begin evaluation: run 1 or 10 episodes or until client asks to stop
    from .agent import evaluate
    stop_flags[sid] = threading.Event()
    scores = None
    try:
        scores = evaluate(ai_id=ai.id, episodes=num_episodes, should_stop=stop_flags[sid].is_set)
    finally:
        del stop_flags[sid]

        # Report evaluation results
        if scores is None:
            emit("evaluation_done", {"completed": False})
        else:
            emit("evaluation_done", {"completed": True,
                                    "scores": scores,
                                    })

@socketio.on("stop_episode")
# @authenticated_only
def handle_stop_episode():
    """
    Set stop flag if stop requested by game.
    """
    
    flag = stop_flags.get(request.sid)
    if flag:
        flag.set()