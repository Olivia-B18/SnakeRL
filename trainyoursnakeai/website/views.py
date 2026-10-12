from flask import render_template, Blueprint
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template('home.html')

@views.route("/snakeai")
def snakeai():
    return render_template('snakeai.html')

@views.route("/snake")
def snake():
    return render_template('snake.html')

@views.route("/intro")
def intro():
    return render_template('intro.html')