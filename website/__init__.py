from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
import yaml


lm = LoginManager()
db = SQLAlchemy()
mysql = MySQL()

conf = yaml.safe_load(open('db.yaml'))
sql_host = conf['mysql_host']
sql_user = conf['mysql_user']
sql_pass = conf['mysql_password']
sql_db = conf['mysql_db']

with open('website/tables.json', 'r') as f:
  tables_dict = json.load(f)

print(tables_dict)

def create_app():
    app = Flask(__name__, template_folder='../templates',static_folder='../static')
    app.config['MYSQL_HOST'] = sql_host 
    app.config['MYSQL_USER'] = sql_user
    app.config['MYSQL_PASSWORD'] = sql_pass
    app.config['MYSQL_DB'] = sql_db
    app.config['SECRET_KEY'] = 'asdfdbds'

    sqlalchemy_config = 'mysql://'+str(sql_user)+':'+str(sql_pass)+'@'+str(sql_host)+'/'+str(sql_db)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_config
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