import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Format: mysql+mysqlconnector://user:password@host/database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:password@localhost/traveloop')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'hackathon-super-secret-key')