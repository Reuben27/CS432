from . import mysql as db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_time = db.Column(db.DateTime(timezone=True), default=func.now())
    return_time = db.Column(db.DateTime(timezone=True), default=None)
    damage_status = db.Column(db.String(5), default="No")

class User_issue(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(22))
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(150))