from .extensions import db
from flask_login import UserMixin

class AI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    high_score = db.Column(db.Integer) # from training
    avg_score = db.Column(db.Integer) # from training
    alpha = db.Column(db.Float)
    gamma = db.Column(db.Float)
    epsilon = db.Column(db.Integer)
    eat = db.Column(db.Integer)
    alive = db.Column(db.Integer)
    die = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    xp_level = db.Column(db.String(64))
    ais = db.relationship("AI", backref="user")