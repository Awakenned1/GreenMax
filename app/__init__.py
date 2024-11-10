from flask import Flask
from config import Config
import firebase_admin
from firebase_admin import credentials


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Firebase Admin
    cred = credentials.Certificate("Service-key.json")
    firebase_admin.initialize_app(cred)

    # Register blueprints
    from app.auth import auth_bp
    from app.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
