from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(100))
    end_location =db.Column(db.String(100))
    story = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='trips')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    trips = db.relationship('Trip', back_populates='user')