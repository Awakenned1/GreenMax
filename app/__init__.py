import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    # Initialize Firebase Admin
    cred = credentials.Certificate("Service-key.json")
    firebase_admin.initialize_app(cred)

    csrf = CSRFProtect(app)

    from .routes import main_bp
    from .services.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
