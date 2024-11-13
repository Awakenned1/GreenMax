import logging
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'your-secret-key'),
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=60),
        WTF_CSRF_SECRET_KEY=os.urandom(24),
        FIREBASE_DATABASE_URL=os.getenv('FIREBASE_DATABASE_URL', 'https://nifty-state-440816-u2-default-rtdb.firebaseio.com'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///greenmax.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Initialize Firebase
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("Service-key.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': app.config['FIREBASE_DATABASE_URL']
            })
            logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Firebase initialization error: {e}")
        raise

    # Import models here to avoid circular import
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import main_bp
    from .services.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
