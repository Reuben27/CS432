from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json

lm = LoginManager()
db = SQLAlchemy()
mysql = MySQL()

with open('website/tables.json', 'r') as f:
  tables_dict = json.load(f)

print(tables_dict)

def create_app():
    app = Flask(__name__, template_folder='../templates',static_folder='../static')
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'reuben'
    app.config['MYSQL_DB'] = 'sports_management'
    app.config['SECRET_KEY'] = 'reuben'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:reuben@localhost/sports_management'
    db.init_app(app)
    mysql.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users, Transactions, User_issue

    with app.app_context():
        db.create_all()

    lm.login_view = 'auth.login'
    lm.init_app(app)

    @lm.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app 