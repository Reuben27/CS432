from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

lm = LoginManager()
db = SQLAlchemy()

mysql = MySQL()


tables_dict = {
    'Users' : ['user_ID', 'user_name', 'email','password'],
    'Students' : ['user_ID', 'discipline', 'year_of_joining', 'programme'],
    'Faculty' : ['user_ID', 'department'],
    'Staff' : ['user_ID', 'job_profile', 'working_hours', 'salary'],
    'Transactions' : ['transaction_ID', 'issue_time', 'return_time', 'damage_status'],
    'Vendor': ['vendor_ID', 'vendor_name', 'vendor_email', 'address'],
    'Sports': ['Sport', 'sports_ID'],
    'Inventory': ['equipment_ID', 'name', 'model', 'total_quantity', 'current_availability', 'deadstock_quantity', 'reserved_quantity'],
    'Location': ['location_ID', 'Room_no', 'Location_Type'],
    'Purchase': ['purchase_ID', 'amount', 'purchase_date', 'mode_of_payment', 'receipt'],
    'Penalty': ['fee_receipt_ID', 'Description'],
    'Storage': ['equipment_ID', 'location_ID'],
    'Equip_Issue': ['transaction_ID', 'equipment_ID'],
    'User_Issue': ['transaction_ID', 'user_ID'],
    'New_stock': ['equipment_ID', 'purchase_ID', 'purchase_quantity'],
    'Orders': ['vendor_ID', 'purchase_ID'],
    'Strike': ['transaction_ID', 'fee_receipt_ID', 'Delay', 'Fees'],
    'Reserved_stock': ['sports_ID', 'equipment_ID', 'reserved_quantity'],
    'Event_coordinator': ['user_ID', 'sports_ID', 'event_name'],
    'User_phone': ['user_ID', 'phone_number'],
    'Vendor_phone': ['vendor_ID', 'phone_number']
}

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