from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users, Admins
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Successfully!', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.transactions'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(user_name)< 2:
            flash('Name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords dont match', category='error')
        elif len(password1) < 7:
            flash('Passwords must be atleast 7 characters.', category='error')
        else:
            new_user = Users( user_name=user_name, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.transactions'))

    return render_template("sign_up.html",user=current_user)

@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_email = request.form.get('admin_email')
        password = request.form.get('password')

        admin = Admins.query.filter_by(admin_email=admin_email).first()
        if admin:
            if check_password_hash(admin.password,password):
                flash('Logged in Successfully!', category="success")
                login_user(admin, remember=True)
                return redirect(url_for('views.display'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('admin_login.html', user=current_user)