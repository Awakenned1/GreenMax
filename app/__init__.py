import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template, session
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import os
import logging
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.update(
        SECRET_KEY='your-secret-key',  # Change this in production
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=60),
        WTF_CSRF_SECRET_KEY=os.urandom(24),
        FIREBASE_DATABASE_URL='your-firebase-database-url'  # Add your database URL
    )
    
    # Initialize extensions
    csrf = CSRFProtect(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Initialize Firebase Admin
    try:
        cred = credentials.Certificate("Service-key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': app.config['FIREBASE_DATABASE_URL']
        })
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Firebase initialization error: {e}")
        raise

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            user_ref = db.reference(f'users/{user_id}')
            user_data = user_ref.get()
            if user_data:
                from .models import User
                return User.from_dict(user_data, user_id)
            return None
        except Exception as e:
            logger.error(f"Error loading user: {e}")
            return None

    # Register blueprints
    from .routes import main_bp
    from .services.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    # Context processors
    @app.context_processor
    def utility_processor():
        def get_user_data():
            if 'user_id' in session:
                try:
                    user_ref = db.reference(f'users/{session["user_id"]}')
                    return user_ref.get()
                except Exception as e:
                    logger.error(f"Error fetching user data: {e}")
                    return None
            return None
        
        return dict(
            get_user_data=get_user_data,
            is_authenticated='user_id' in session
        )

    return app
