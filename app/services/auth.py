from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from functools import wraps
import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

auth_bp = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if verify_credentials(username, password):
            session['user'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if create_user(username, hash_password(password)):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exists', 'error')

    return render_template('register.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('main.home'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_credentials(username, password):
    # Implement actual verification logic here
    # For testing purposes:
    return True


def create_user(username, hashed_password):
    # Implement user creation logic here
    # For testing purposes:
    return True