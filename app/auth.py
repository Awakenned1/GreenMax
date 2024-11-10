from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import pyrebase
from config import Config

auth_bp = Blueprint('auth', __name__)

firebase = pyrebase.initialize_app(Config.FIREBASE_CONFIG)
auth = firebase.auth()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = {'email': email}
            return redirect(url_for('main.index'))
        except:
            flash('Invalid credentials')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.create_user_with_email_and_password(email, password)
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
        except:
            flash('Registration failed. Please try again.')
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))
