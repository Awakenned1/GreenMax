# app/services/firebase_service.py

import firebase_admin
from firebase_admin import credentials, db
import os

def initialize_firebase():
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
    })
