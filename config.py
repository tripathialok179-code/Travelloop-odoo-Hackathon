import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use MySQL for industry standard, SQLite for rapid testing
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'mysql+mysqlconnector://root:password@localhost/traveloop'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'odoo-hackathon-2026-secret')
