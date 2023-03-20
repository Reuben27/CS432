from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mysqldb import MySQL

lm = LoginManager()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Your Password'
    app.config['MYSQL_DB'] = 'Your Database Name'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/users'
    db = SQLAlchemy(app)

    mysql = MySQL(app)

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
    def load_user(id):
        return Users.query.get(int(id))

    return app 