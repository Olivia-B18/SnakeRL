from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .dbmodels import User

auth = Blueprint('auth', __name__)

@auth.route("signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        grade_level = request.form.get('grade-level')
        if valid_input(first_name, grade_level, last_name):
            new_user = User(first_name=first_name, last_name=last_name, grade_level=grade_level)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            return redirect(url_for("views.intro"))
    return render_template("signin.html")

@auth.route("logout")
def logout():
    logout_user()
    return redirect(url_for("auth.signin"))

def valid_input(first_name, grade_level, last_name):
    if len(first_name) < 2:
        flash("first name must be greater than 1 character", category="error")
        return False
    if len(grade_level) == 0:
        flash("grade level can't be empty", category="error")
        return False
    if grade_level == "0":
        flash("grade level can't be empty", category="error")
        return False
    if len(last_name) < 1:
        flash("last initial can't be empty", category="error")
        return False
    return True