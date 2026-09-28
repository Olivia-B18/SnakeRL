import functools
from flask_login import current_user
from flask_socketio import disconnect
from .extensions import socketio
from .params import PARAMS

REQ_TRAINING_INPUTS = tuple(name for name, spec in PARAMS.items())

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
    try:
        values = clean(training_inputs)
    except ValueError as err:
        print(f"train: {err}")
        return

    # Begin training
    from .agent import start
    start(**{key: values[key] for key in REQ_TRAINING_INPUTS})