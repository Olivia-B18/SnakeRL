import functools
import threading
from flask import request
from flask_login import current_user
from flask_socketio import disconnect, emit
from .extensions import socketio
from .params import PARAMS

REQ_TRAINING_INPUTS = tuple(name for name, spec in PARAMS.items())

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
    """Convert and bounds-check a train payload against PARAMS.

    Returns {name: converted value}. Raises ValueError describing the first
    problem found.
    """
    # Validate that payload is converted to a dictionary
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JS object, got {type(payload).__name__}")

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
        if not spec["min"] <= value <= spec["max"]:
            raise ValueError(
                f"{name}: {value} outside {spec['min']}..{spec['max']}"
            )
        cleaned[name] = value
    return cleaned

@socketio.on("train")
# @authenticated_only
def handle_train(training_inputs):
    sid = request.sid
    if sid in stop_flags:
        print("train: already training")
        return

    try:
        values = clean(training_inputs)
    except ValueError as err:
        print(f"train: {err}")
        emit("training_done", {"completed": False})
        return

    # Begin training; runs until 100 games finish or the client asks to stop
    from .agent import start
    stop_flags[sid] = threading.Event()
    try:
        completed, num_games_completed = start(**{key: values[key] for key in REQ_TRAINING_INPUTS},
                          should_stop=stop_flags[sid].is_set)
    finally:
        del stop_flags[sid]
    emit("training_done", {"completed": completed,
                           "num_games_completed": num_games_completed,
                           })

@socketio.on("stop_training")
# @authenticated_only
def handle_stop_training():
    flag = stop_flags.get(request.sid)
    if flag:
        flag.set()