import logging
import os
from datetime import timedelta

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


# Initialize FCM Manager here
from .services.fcm_service import FCMManager
fcm_manager = FCMManager()  # Create instance here

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def init_gemini():
    """Initialize Gemini AI"""
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        logger.info("Gemini AI initialized successfully")
        return model
    except Exception as e:
        logger.error(f"Gemini AI initialization error: {e}")
        return None

def init_firebase():
    """Initialize Firebase"""
    try:
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'Service-key.json')
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
            })
            logger.info("Firebase initialized successfully")
            return True
    except Exception as e:
        logger.error(f"Firebase initialization error: {e}")
        return False

def create_app():
    # Initialize Firebase first
    init_firebase()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', os.urandom(24)),
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv('SESSION_LIFETIME', 60))),
        WTF_CSRF_SECRET_KEY=os.urandom(24),
        FIREBASE_DATABASE_URL=os.getenv('FIREBASE_DATABASE_URL'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///greenmax.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
        TEMPLATES_AUTO_RELOAD=True,
        DEBUG=os.getenv('FLASK_ENV') == 'development',
        FCM_API_KEY=os.getenv('FCM_API_KEY')
    )
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        # Import services
        from .services.energy_monitor import EnergyMonitoringSystem
        from .services.fcm_service import FCMManager
        
        # Initialize services
        app.energy_monitor = EnergyMonitoringSystem()
        app.fcm_manager = FCMManager()
        
        # Initialize Gemini AI
        app.config['GEMINI_MODEL'] = init_gemini()
        
        # Import models
        from .models import User
        
        # Create database tables
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            if app.config['DEBUG']:
                raise
        
        # Setup user loader
        @login_manager.user_loader
        def load_user(user_id):
            try:
                return User.query.get(int(user_id))
            except Exception as e:
                logger.error(f"Error loading user: {e}")
                return None
        
        # Register blueprints
        from .routes import main_bp
        from .services.auth import auth_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 error: {error}")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {error}")
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        logger.warning(f"403 error: {error}")
        return render_template('errors/403.html'), 403

    @app.after_request
    def add_security_headers(response):
        """Add security headers to response"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
