from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from functools import wraps
import hashlib
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import DataRequired, Length
import firebase_admin
from firebase_admin import auth, credentials

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
            session['user_id'] = 1  # Add user_id to session
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if form.validate_on_submit():
        try:
            # Create user in Firebase
            user = auth.create_user(
                email=form.email.data,
                password=form.password.data,
                display_name=form.fullname.data
            )

            # Create custom claims if needed
            auth.set_custom_user_claims(user.uid, {
                'role': 'user',
                'created_at': datetime.now().isoformat()
            })

            # Store additional user data in Firestore/Realtime Database if needed
            store_user_data(user.uid, {
                'fullname': form.fullname.data,
                'email': form.email.data,
                'created_at': datetime.now().isoformat(),
                'last_login': None
            })

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))

        except auth.EmailAlreadyExistsError:
            flash('Email already registered', 'error')
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')

    return render_template('register.html', form=form)

def store_user_data(uid, data):
    """Store additional user data in Firebase Realtime Database"""
    try:
        db = firebase_admin.db.reference(f'users/{uid}')
        db.set(data)
    except Exception as e:
        print(f"Error storing user data: {e}")

# When a user logs in or updates their token
def update_fcm_token(self, user_id, token):
    """Update user's FCM token in Firebase."""
    try:
        self.db.reference(f'users/{user_id}/fcm_token').set(token)
        return True
    except Exception as e:
        print(f"Error updating FCM token: {e}")
        return False

@auth_bp.route('/logout')
def logout():
    session.clear()
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
    return True

def create_user(username, hashed_password):
    # Implement user creation logic here
    return True
