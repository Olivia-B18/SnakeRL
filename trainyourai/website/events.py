import functools
from flask import flash, render_template
from flask_login import current_user
from flask_socketio import disconnect
from .extensions import socketio

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect(current_user)
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on("connect")
@authenticated_only
def handle_connect():
    print(f"{current_user.first_name} connected")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"user {username} joined")

@socketio.on("train")
@authenticated_only
def handle_train(food, alive, die):
    if(food != "" and alive != "" and die != ""):
        from .agent import start
        start(food, alive, die)
    else:
        print("error")