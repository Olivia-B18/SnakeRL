from . import db
from flask_login import UserMixin

class AI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    high_score = db.Column(db.Integer)
    avg_score = db.Column(db.Integer)
    eat = db.Column(db.Integer)
    alive = db.Column(db.Integer)
    die = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    grade_level = db.Column(db.Integer)
    ais = db.relationship("AI", backref="user")