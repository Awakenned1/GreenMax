from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    energy_data = db.relationship('EnergyData', backref='user', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)

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
