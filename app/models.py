from datetime import datetime
from flask_login import UserMixin
from . import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User model with FCM and notification preferences."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # FCM and notification preferences
    fcm_token = db.Column(db.String(255))
    notification_preferences = db.Column(JSON, default={
        'high_usage': True,
        'peak_alert': True,
        'daily_limit': True
    })
    
    # Energy monitoring settings
    energy_settings = db.Column(JSON, default={
        'daily_limit': 50.0,
        'high_usage_threshold': 4.0,
        'peak_alert_threshold': 4.5
    })

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<User {self.username}>'

class EnergyData(db.Model):
    __tablename__ = 'energy_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    current_power = db.Column(db.Float, nullable=False)
    peak_value = db.Column(db.Float, nullable=False)
    peak_time = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    daily_total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<EnergyData {self.timestamp}>'

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Recommendation {self.id}>'
