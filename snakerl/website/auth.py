from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .extensions import db
from .dbmodels import User
from . import flow

auth = Blueprint('auth', __name__)

@auth.route("signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        first_name = request.form.get('first-name', '').strip()
        last_name = request.form.get('last-name', '').strip()
        xp_level = request.form.get('xp-level', '')
        if valid_input(first_name, xp_level, last_name):
            new_user = User(first_name=first_name, last_name=last_name, xp_level=xp_level)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flow.reset()
            return redirect(url_for("views.intro"))
    return render_template("signin.html", form=request.form)

@auth.route("logout")
def logout():
    logout_user()
    flow.clear()
    return redirect(url_for("auth.signin"))

def valid_input(first_name, xp_level, last_name):

    # Track list of error messages
    error_msg = []

    # Check for any errors
    if len(first_name) < 2:
        error_msg.append("First name must be greater than 1 character.")
    if len(last_name) != 1:
        error_msg.append("Last initial must be exactly 1 character long.")
    if len(xp_level) == 0:
        error_msg.append("Experience can't be empty.")
    if xp_level == "-1":
        error_msg.append("Experience can't be empty.")

    # Flash error messages, if any
    if error_msg:
        for msg in error_msg:
            flash(msg, category="error")
        return False
    
    return True
