import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///travelloop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
