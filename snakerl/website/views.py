from flask import render_template, Blueprint
from flask_login import login_required
from . import flow
from .params import PARAMS

views = Blueprint("views", __name__)

# DEV: login and page-order enforcement are commented out while pages are
# being built. To re-enable, uncomment every "# @login_required" and
# "# @flow.step(...)" line below.

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/intro")
# @login_required
# @flow.step("intro")
def intro():
    return render_template("intro.html")

@views.route("/snake")
# @login_required
# @flow.step("snake")
def snake():
    return render_template("snake.html")

@views.route("/untrained")
# @login_required
# @flow.step("untrained")
def untrained():
    return render_template("untrained.html")

@views.route("/parameters")
# @login_required
# @flow.step("parameters")
def parameters():
    return render_template("parameters.html")

@views.route("/training")
# @login_required
# @flow.step("training")
def training():
    return render_template("training.html", params=PARAMS)

@views.route("/evaluation")
# @login_required
# @flow.step("evaluation")
def evaluation():
    return render_template("evaluation.html")

@views.route("/conclusion")
# @login_required
# @flow.step("conclusion")
def conclusion():
    return render_template("conclusion.html")

