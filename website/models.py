from . import db
from flask_login import UserMixin
# from sqlalchemy.sql import func

# class Transactions(db.Model):
#     transaction_id = db.Column(db.Integer, primary_key=True)
#     issue_time = db.Column(db.DateTime(timezone=True), default=func.now())
#     return_time = db.Column(db.DateTime(timezone=True), default=None)
#     damage_status = db.Column(db.String(5), default="No")
#     user = db.relationship('User_issue')
#     def get_id(self):
#         return(self.transactions_id)

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(22))
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(150))
    # transactions = db.relationship('User_issue')

    def get_id(self):
        return(self.user_id)

# class User_issue(db.Model):
#     transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'),primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Admins(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(22))
    admin_email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(150))

    def get_id(self):
        return(self.admin_id)

